import contextlib
import io
import unittest
from unittest.mock import patch

import STCORE as c
import STCIPROP as prop
import STCIMEAN as means
import STCIMOE as moe
import STHYPR as hp
import STHYME as hm
import STHYRES as hr
import STBNWK as binwork
import STWORK as work
import STDWK as datawork
import STDMATH as data
import STCOUNT as count
import STCOUNT5 as money
import STCOUNT6 as counting
import STCOMB
import STPROB as probability
import STPCT


def flow(function,answers):
    pending=iter(answers);pages=[]
    with patch('builtins.input',side_effect=lambda prompt='':next(pending)), \
         patch.object(c,'view',side_effect=lambda title,lines:pages.append((title,list(lines)))), \
         contextlib.redirect_stdout(io.StringIO()):
        function()
    if list(pending): raise AssertionError('Unused fixture entries')
    return '\n'.join(line for title,lines in pages for line in lines)


class WorkedSubstitutions(unittest.TestCase):
    def test_all_confidence_interval_modes_show_substituted_se_and_endpoints(self):
        cases=[(prop._one_proportion,['60','100','95%'],'p-hat=x/n=60/100=0.6','SE=sqrt(0.6*(1-0.6)/100)'),
               (prop._one_proportion_estimate,['','.6','100','95%'],'p-hat=0.6000','SE=sqrt(0.6*(1-0.6)/100)'),
               (prop._two_proportions,['60','100','40','80','95%'],'PE=x1/n1-x2/n2=60/100-40/80','SE=sqrt(0.6*(1-0.6)/100+0.5*(1-0.5)/80)'),
               (means._one_mean,['1','100','15','36','95%',''],'x-bar=100','SE=15/sqrt(36)=2.5'),
               (means._two_means,['1','100','15','25','1','105','8','40','95%'],'PE=x-bar1-x-bar2=100-105','SE=sqrt(15^2/25+8^2/40)')]
        for function,entries,estimate,se in cases:
            text=flow(function,entries)
            for expected in (estimate,se,'E=','LOWER=estimate-E=','UPPER=estimate+E='):
                self.assertIn(expected,text)
        text=flow(means._two_means,['1','100','15','25','1','105','8','40','95%'])
        self.assertIn('df=(9+1.6)^2/(9^2/(25-1)+1.6^2/(40-1))=',text)

    def test_margin_error_and_supplied_margin_modes(self):
        for entries,expected in [(['1','95%','60','100'],'SE=sqrt(0.6*(1-0.6)/100)'),
                                  (['2','95%','15','36'],'SE=15/sqrt(36)=2.5'),
                                  (['3','95%','.6','100'],'SE=sqrt(0.6*(1-0.6)/100)')]:
            text=flow(moe._margin_error,entries)
            self.assertIn(expected,text);self.assertIn('E=z*SE=',text)
        text=flow(moe._interval_from_estimate_and_margin,['1','.6','.05'])
        self.assertIn('LOWER=estimate-E=0.6-0.05=0.55',text)
        self.assertIn('UPPER=estimate+E=0.6+0.05=0.65',text)

    def test_ht_null_pooled_and_welch_work(self):
        result=hp.one(30,267,.1)
        self.assertIn('SE=sqrt(0.1*(1-0.1)/267)',str(result['se_work']))
        pooled=hp.two(60,100,40,100)
        self.assertIn('p-pool=(60+40)/(100+100)=0.5',pooled['se_work'])
        self.assertIn('SE=sqrt(0.5*(1-0.5)*(1/100+1/100))',str(pooled['se_work']))
        result=hm.two(100,15,25,105,8,40)
        self.assertIn('df=(9+1.6)^2/(9^2/(25-1)+1.6^2/(40-1))=',str(result['se_work']))
        for alternative,expression in [('<','TI APPROX: tcdf(-9999,'),('>','TI APPROX: tcdf('),('!=','TI APPROX: 2*tcdf(')]:
            setup={'null':0,'alpha':.05,'alternative':alternative,'parameter':'mu1-mu2','claim':alternative,'context':'mean difference','random':'PASS'}
            p,cv,reject=hr.inference(result['ts'],.05,alternative,result['df'])
            lines=hr.step(7,setup,result,p,cv,reject)
            self.assertIn(expression,str(lines))

    def test_binomial_exact_interval_cumulative_and_complement_expansions(self):
        text='\n'.join(binwork.work(10,(1,5),('=',3,0)))
        self.assertIn('C(10,3)*(0.2)^3*(0.8)^7',text)
        self.assertIn('binompdf(10,0.2,3)',text)
        text='\n'.join(binwork.work(10,(1,5),('>=',3,0)))
        self.assertIn('P=1-(',text)
        for k in range(3): self.assertIn('C(10,'+str(k)+')',text)
        self.assertNotIn('C(10,3)',text)
        self.assertIn('1-binomcdf(10,0.2,2)',text)
        text='\n'.join(binwork.work(10,(1,5),('[)',3,5)))
        self.assertIn('C(10,3)',text);self.assertIn('C(10,4)',text)
        self.assertNotIn('C(10,5)',text)
        self.assertIn('binomcdf(10,0.2,4) - binomcdf(10,0.2,2)',text)
        text='\n'.join(binwork.work(10,(1,5),('!=',3,0)))
        self.assertIn('1-binompdf(10,0.2,3)',text)

    def test_descriptive_expanded_equations_and_each_work_table_column(self):
        rows=[((1,1),2),((4,1),1)]
        stats=data.weighted_stats(rows)
        result=datawork.descriptive(stats,None,rows)
        self.assertNotIsInstance(result,list)
        text='\n'.join(result)
        for expected in ('(1*2)','(4*1)','MEAN=6/3=2','d=x-mean=1-(2)=-1',
                         'd^2=(-1)^2=1','f*d^2=2*(1)=2','SS=SUM(f*(x-mean)^2)',
                         'SAMPLE VAR=SS/(n-1)=6/(3-1)=3','SAMPLE SD=sqrt(3)'):
            self.assertIn(expected,text)
        visits=[]
        lazy=work.Lines(100000,lambda i:visits.append(i) or str(i))
        self.assertEqual(len(lazy),100000);self.assertEqual(visits,[])
        self.assertEqual(next(iter(lazy)),'0');self.assertEqual(visits,[0])

    def test_discrete_moments_assemble_actual_terms(self):
        rows=[((0,1),(1,4)),((2,1),(3,4))]
        mean,var,sd=count.distribution_moments(rows)
        text='\n'.join(datawork.moments(2,lambda i:rows[i],mean,var,sd))
        for expected in ('(0*0.25)','(2*0.75)','((2)^2*0.75)',
                         'VAR=E(X^2)-E(X)^2=3-(1.5)^2=0.75','SD=sqrt(0.75)'):
            self.assertIn(expected,text)

    def test_money_and_counting_work_without_factorial_allocation(self):
        text=flow(money.insurance_session,['1','.99','15','1000','1'])
        self.assertIn('EXPECTED PAYOUT=0.01*1000=10',text)
        self.assertIn('E=PREMIUM-PAYOUT=15-10=5',text)
        text=flow(money.insurance_session,['2','.99','15','1000','1'])
        self.assertIn('E=PAYOUT-PREMIUM=10-15=-5',text)
        text=flow(money.raffle_session,['100','2','50','3','1'])
        self.assertIn('E(BUYER ONE)=PRIZE/TOTAL-PRICE=50/100-2=-1.5',text)
        text=flow(money.payoff_session,['PLAYER','1','2','0','3','10','1','1','0'])
        self.assertIn('NET=0-1=-1; P=3/4=0.75',text)
        self.assertIn('(-1*0.75)',text);self.assertIn('(9*0.25)',text)
        text=flow(counting.win_loss_session,['.5','2','10','3','1','0'])
        self.assertIn('P(WIN)=(0.5)^2=0.25',text)
        self.assertIn('(-3*0.75)',text);self.assertIn('(10*0.25)',text)
        with patch.object(STCOMB,'factorial',side_effect=AssertionError('Do not allocate factorials')):
            self.assertIn('P(100000,2)=100000!/99998!=9999900000',flow(counting.solver_npr,['100000','2','1']))
            self.assertIn('C(100000,2)=100000!/(2!*99998!)=4999950000',flow(counting.solver_ncr,['100000','2','1']))

    def test_percent_category_and_contingency_work(self):
        self.assertIn('ANSWER=250*(0.12)=30',flow(STPCT.percent_session,['250','12%','1']))
        text=flow(probability.category_session,['2','A','10','B','30','1','1','E','.2','1','0'])
        self.assertIn('P(A)=10/40=0.25',text)
        self.assertIn('DIFFERENCE=(0.25-0.2)*100=5',text)
        text=flow(probability.two_way_session,['2','2','A','NOT A','B','NOT B','10','20','30','40','1','1','1','0'])
        self.assertIn('ROW GIVEN COLUMN=10/40=0.25',text)
        self.assertIn('OR=(30+40-10)/100',text)

    def test_method_is_visible_without_selecting_show_method(self):
        pages=[]
        with patch.object(c,'view',side_effect=lambda title,lines:pages.append(list(lines))), \
             patch.object(c,'menu',return_value='1'):
            c.results('ANSWER',[('X',2)],['X=1+1=2'])
        self.assertIn('X=1+1=2',pages[0])

    def test_paged_table_shows_assembled_work_after_last_rows(self):
        pages=[]
        with patch.object(c,'view',side_effect=lambda title,lines:pages.append(list(lines))), \
             patch.object(c,'menu',side_effect=['N','0']):
            c.paged_results('TABLE',8,lambda i:('ROW '+str(i),i),['TOTAL=0+1+2+3+4+5+6+7=28'])
        self.assertNotIn('TOTAL=0+1+2+3+4+5+6+7=28',pages[0])
        self.assertIn('TOTAL=0+1+2+3+4+5+6+7=28',pages[1])


if __name__=='__main__': unittest.main()
