import contextlib
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import STCORE as c
import STHYIO as inputs
import STHYPR as prop
import STHYME as means
import STHYRES as output

ROOT=Path(__file__).resolve().parent.parent


class Hypothesis(unittest.TestCase):
    def test_one_proportion_uses_null_standard_error(self):
        result=prop.one(60,100,.5)
        self.assertAlmostEqual(result['estimate'],.6)
        self.assertAlmostEqual(result['se'],.05)
        self.assertAlmostEqual(result['ts'],2)
        self.assertIn('PASS',' '.join(result['checks']))

    def test_two_proportions_pooled_variance(self):
        result=prop.two(45,64,34,80)
        pooled=79/144
        expected=(pooled*(1-pooled)*(1/64+1/80))**.5
        self.assertAlmostEqual(result['se'],expected)
        self.assertAlmostEqual(result['ts'],(45/64-34/80)/expected)

    def test_mean_statistics_and_fractional_welch_df(self):
        result=means.one(105,15,25,100)
        self.assertAlmostEqual(result['ts'],5/3)
        self.assertEqual(result['df'],24)
        result=means.two(105,15,25,100,8,40,2)
        a,b=225/25,64/40
        self.assertAlmostEqual(result['ts'],3/(a+b)**.5)
        self.assertAlmostEqual(result['df'],(a+b)**2/(a*a/24+b*b/39))
        self.assertNotEqual(result['df'],int(result['df']))

    def test_all_claim_operators_map_to_the_correct_tail(self):
        for key,claim,alt in [('1','<','<'),('2','>','>'),('3','!=','!='),
                              ('4','<=','>'),('5','>=','<'),('6','=','!=')]:
            with patch('builtins.input',side_effect=['support for proposal','.05']), \
                 patch.object(c,'menu',side_effect=['1',key]):
                result=inputs.setup('p',.5)
            self.assertEqual((result['claim'],result['alternative']),(claim,alt))
        with patch('builtins.input',return_value=''),patch.object(c,'menu',return_value='0'):
            self.assertIsNone(inputs.setup('p',.5))

    def test_z_tails_rejection_and_equality_rule(self):
        for alt,expected in [('<',.977249868),('>',.022750132),('!=',.045500264)]:
            p,critical,reject=output.inference(2,.05,alt)
            self.assertAlmostEqual(p,expected,places=6)
            self.assertEqual(reject,alt!='<')
            self.assertEqual(len(critical),2 if alt=='!=' else 1)
        p,_,_=output.inference(2,.05,'>')
        self.assertTrue(output.inference(2,p,'>')[2])
        self.assertEqual(output.inference(0,.5,'>')[0],.5)
        self.assertTrue(output.inference(0,.5,'>')[2])
        self.assertLess(output.inference(8,.05,'>')[0],1e-14)

    def test_conclusions_distinguish_claims_from_alternatives(self):
        base={'context':'voters approving','parameter':'p','null':.5}
        for claim in ('=','<=','>=','<','>','!='):
            setup=dict(base,claim=claim)
            for reject in (True,False):
                text=output.conclusion(setup,reject)
                if claim in ('=','<=','>='):
                    self.assertTrue(text.startswith('THERE IS '+('SUFFICIENT' if reject else 'NOT SUFFICIENT')+' EVIDENCE TO WARRANT REJECTION OF THE CLAIM THAT '))
                else:
                    self.assertTrue(text.startswith('THERE IS '+('SUFFICIENT' if reject else 'NOT SUFFICIENT')+' EVIDENCE TO SUPPORT THE CLAIM THAT '))
                self.assertIn('THE POPULATION PROPORTION FOR voters approving',text)
        setup={'context':'','parameter':'mu','null':56.8,'claim':'<'}
        self.assertEqual(output.conclusion(setup,False),'THERE IS NOT SUFFICIENT EVIDENCE TO SUPPORT THE CLAIM THAT THE POPULATION MEAN IS LESS THAN 56.8.')
        self.assertEqual(output.conclusion(setup,True),'THERE IS SUFFICIENT EVIDENCE TO SUPPORT THE CLAIM THAT THE POPULATION MEAN IS LESS THAN 56.8.')

    def test_invalid_counts_and_zero_standard_errors(self):
        for function,args in [(prop.one,(101,100,.5)),(prop.one,(2,10,1)),
                              (prop.two,(0,10,0,20)),(means.one,(5,0,10,5)),
                              (means.two,(5,0,10,5,0,10)),(means.one,(5,2,1,5))]:
            with self.assertRaises(ValueError): function(*args)

    def test_final_conclusion_states_decision_and_numeric_reason(self):
        setup={'context':'mean score','parameter':'mu','null':23,'alpha':.05,
               'claim':'=','alternative':'!='}
        result=means.one(23.5,4.23,37,23)
        for probability,reject,comparison in [(.01,True,'<='),(.2,False,'>'),(.05,True,'<=')]:
            lines=output.step(9,setup,result,probability,(),reject)
            self.assertEqual(lines[0],'REJECT H0' if reject else 'FAIL TO REJECT H0')
            self.assertEqual(lines[1],'BECAUSE p=%.10g %s alpha=0.05.' % (probability,comparison))
            self.assertEqual(lines[2],'FINAL CONCLUSION ('+('TISE' if reject else 'TINSE')+'):')
            self.assertEqual(lines[-1],'AT THE 5% SIGNIFICANCE LEVEL, THERE IS '+
                             ('SUFFICIENT' if reject else 'NOT SUFFICIENT')+
                             ' EVIDENCE TO WARRANT REJECTION OF THE CLAIM THAT THE POPULATION MEAN FOR mean score IS EQUAL TO 23.')

    def test_requirements_and_hypotheses_show_checks_and_selected_tail_directly(self):
        result=means.one(105,15,25,100)
        result.update(name='ONE-MEAN t TEST',checks=['NORMALITY: VERIFY'])
        for alt,tail in [('<','LEFT-TAILED TEST'),('>','RIGHT-TAILED TEST'),('!=','TWO-TAILED TEST')]:
            setup={'context':'scores','parameter':'mu','null':100,'alpha':.05,
                   'claim':alt,'alternative':alt,'random':'PASS'}
            requirements=output.step(1,setup,result,.2,(),False)
            hypotheses=output.step(2,setup,result,.2,(),False)
            self.assertEqual(requirements,['ONE-MEAN t TEST','SRS / RANDOM INDEPENDENT: PASS','NORMALITY: VERIFY'])
            self.assertIn('TAIL: '+tail,hypotheses)
            self.assertNotIn('EQUALITY BOUNDARY',' '.join(hypotheses))

    def test_written_initial_and_final_conclusions_cover_each_claim_and_decision(self):
        result=means.one(105,15,25,100)
        for claim,alt in [('<','<'),('>','>'),('!=','!='),('<=','>'),('>=','<'),('=','!=')]:
            setup={'context':'test scores','parameter':'mu','null':100,'alpha':.01,
                   'claim':claim,'alternative':alt}
            for p,reject in [(.001,True),(.2,False),(.01,True)]:
                initial=' '.join(output.step(8,setup,result,p,(),reject))
                final=output.step(9,setup,result,p,(),reject)
                self.assertIn('WE '+('REJECT' if reject else 'FAIL TO REJECT')+' THE NULL HYPOTHESIS.',initial)
                self.assertIn('LESS THAN OR EQUAL TO' if reject else 'GREATER THAN',initial)
                self.assertTrue(final[-1].startswith('AT THE 1% SIGNIFICANCE LEVEL, THERE IS '+
                                                     ('SUFFICIENT' if reject else 'NOT SUFFICIENT')+' EVIDENCE'))
                self.assertIn('WARRANT REJECTION OF THE CLAIM' if claim in ('=','<=','>=') else 'SUPPORT THE CLAIM',final[-1])
                self.assertIn('THE POPULATION MEAN FOR test scores',final[-1])
                self.assertNotIn('CONDITIONAL',' '.join(final))

    def test_pvalue_paper_work_for_each_tail_and_distribution(self):
        for df in (None,9):
            variable='Z' if df is None else 'T'
            for alt in ('<','>','!='):
                setup={'null':65,'alpha':.05,'alternative':alt,'parameter':'mu'}
                result={'ts':1.6355915908,'df':df}
                p,cv,reject=output.inference(result['ts'],.05,alt,df)
                text=' '.join(output.step(7,setup,result,p,cv,reject))
                self.assertIn('p=P('+variable if alt!='!=' else 'p=2*P('+variable,text)
                self.assertIn('normalcdf' if df is None else 'tcdf',text)
                self.assertNotIn('SF_',text)
                if alt=='>': self.assertIn('p=1-',text)
                if alt=='!=': self.assertIn('TWO TAILS: p=2*',text)

    def test_pvalue_explanation_uses_the_actual_percentage_and_null_assumption(self):
        import STDEFS
        definition=dict(STDEFS.DEFINITIONS)['p value']
        self.assertIn('IF H0 WERE TRUE',definition)
        self.assertIn('TESTED TAIL(S)',definition)
        self.assertIn('IT IS NOT THE CHANCE THAT H0 IS TRUE',definition)
        for probability,percent in [(.068177,'6.8177%'),(.01,'1%'),(.2,'20%')]:
            setup={'null':65,'alpha':.05,'alternative':'>','parameter':'mu'}
            text=' '.join(output.step(7,setup,{'ts':1.6,'df':9},probability,(),False))
            self.assertIn('IF H0 WERE TRUE, ABOUT '+percent+' OF RANDOM SAMPLES',text)
            self.assertIn('THIS EXTREME OR MORE EXTREME',text)
            self.assertNotIn('NOT SIMPLE ARITHMETIC',text)

    def test_all_nine_steps_include_graph_formulas_and_correct_hypotheses(self):
        setup={'context':'approval','parameter':'p1-p2','null':0,'alpha':.05,
               'claim':'!=','alternative':'!=','random':'PASS'}
        result=prop.two(60,100,40,100)
        result.update(name='TWO-PROPORTION z TEST',command='2-PropZTest')
        p,critical,reject=output.inference(result['ts'],.05,'!=')
        pages=[output.step(i,setup,result,p,critical,reject) for i in range(1,10)]
        self.assertIn('H0: p1 = p2',pages[1])
        self.assertIn('PE',str(pages[2]))
        self.assertIn('p-pool',str(pages[4]))
        self.assertIn('ALIGNS WITH PE',str(pages[5]))
        self.assertIn('p IS NOT THE PROBABILITY',str(pages[6]))
        self.assertIn('REJECT H0',pages[7])

    def test_fresh_home_flows_all_four_tests_and_raw_data_release(self):
        code='''
import builtins,weakref,sys
import STAT1,STCORE as c
refs=[];titles=[]
def view(title,lines):
 assert title!='CHECK ENTERED VALUES',lines
 titles.append(title)
 refs.extend(weakref.ref(sys.modules[n]) for n in c.topic_modules())
c.view=view
common=['approval','1','2']
cases=[['15','1']+common+['.5','.05','60','100','','0','0','0'],
 ['15','2']+common+['.05','60','100','','40','100','','1','0','0','0'],
 ['15','3']+common+['100','.05','1','105','15','100','','0','0','0'],
 ['15','4']+common+['0','.05','1','1','105','15','100','','1','100','8','100','','0','0','0'],
 ['15','3']+common+['3','.05','2','5','1','2','3','4','5','','1','0','0','0']]
for repeat in range(3):
 for answers in cases:
  pending=iter(answers)
  builtins.input=lambda prompt='':next(pending)
  STAT1.main()
  assert list(pending)==[],answers
  assert not c.topic_modules(),c.topic_modules()
  assert all(ref() is None for ref in refs)
  refs=[]
assert all(any(title.startswith('HT '+str(i)+':') for title in titles) for i in range(1,10))
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,
                           capture_output=True,text=True,timeout=30)
        self.assertEqual(run.returncode,0,run.stdout[-2000:]+run.stderr)


if __name__=='__main__': unittest.main()
