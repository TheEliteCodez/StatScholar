import contextlib
from fractions import Fraction
from itertools import product
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
from test_expansion import flow
import STCORE as c
import STDIST
import STNDIST
import STUNIF
import STTDIST
import STMDICE2
import STSAMP1
import STHOME


class DistributionConstruction(unittest.TestCase):
    def test_sorted_cdf_work_columns_and_moments_with_duplicates(self):
        rows=[((2,1),(1,4)),((-1,1),(1,4)),((2,1),(1,2))]
        tables=[];answers=[]
        def table(title,count,at,*args,**kwargs): tables.append((title,[at(i) for i in range(count)]))
        with patch.object(c,'menu',side_effect=['1','2','3','6','0']),patch.object(c,'paged_results',side_effect=table),patch.object(c,'results',side_effect=lambda title,values,*a,**kw:answers.append(dict(values))):
            STDIST.discrete_tools(3,lambda i:rows[i],'TEST')
        self.assertEqual([Fraction(*v) for k,v in tables[0][1]],[Fraction(1,4),Fraction(3,4)])
        self.assertEqual([Fraction(*v) for k,v in tables[1][1]],[Fraction(1,4),1])
        self.assertEqual([Fraction(*v) for k,v in tables[2][1]],
                         [Fraction(1,4),Fraction(-1,4),Fraction(1,4),Fraction(3,4),Fraction(3,2),3])
        self.assertEqual(Fraction(*answers[0]['SUM xP / MEAN']),Fraction(5,4))
        self.assertEqual(Fraction(*answers[0]['VAR']),Fraction(27,16))

    def test_percentiles_honor_cdf_jumps_and_duplicate_rows(self):
        rows=[((2,1),(1,4)),((-1,1),(1,4)),((2,1),(1,2))]
        for area,cut,below,left in [('0',-1,0,Fraction(1,4)),('25%',-1,0,Fraction(1,4)),
                                     ('26%',2,Fraction(1,4),1),('100%',2,Fraction(1,4),1)]:
            with patch.object(c,'menu',side_effect=['4','0']),patch('builtins.input',side_effect=[area]),patch.object(c,'results') as results:
                STDIST.discrete_tools(3,lambda i:rows[i],'TEST')
            ans=dict(results.call_args.args[1])
            self.assertEqual(Fraction(*ans['x CUTOFF']),cut)
            self.assertEqual(Fraction(*ans['P(X<x)']),below)
            self.assertEqual(Fraction(*ans['P(X<=x)']),left)

    def test_expected_counts_and_rounded_table_moments_behavior(self):
        rows=[((0,1),(1,4)),((1,1),(3,4))]
        with patch.object(c,'menu',side_effect=['5','6','4','0']),patch('builtins.input',side_effect=['20']),patch.object(c,'paged_results') as table,patch.object(c,'view') as view:
            STDIST.discrete_tools(2,lambda i:rows[i],'TEST',True)
            at=table.call_args.args[2]
            self.assertEqual(Fraction(*at(0)[1]),5)
            self.assertEqual(Fraction(*at(1)[1]),15)
            self.assertEqual(view.call_count,2)

    def test_dice_tables_and_summary_against_independent_enumeration(self):
        for n in (1,2,3,4):
            for face_count in (False,True):
                with patch.object(c,'call') as call,patch.object(c,'read_size',return_value=3):
                    STMDICE2.dice_distribution(n,face_count)
                module,func,count,at,title=call.call_args.args
                self.assertEqual((module,func),('STDIST','discrete_tools'))
                outcomes=list(product(range(1,7),repeat=n))
                observed={}
                for outcome in outcomes:
                    value=outcome.count(3) if face_count else sum(outcome)
                    observed[value]=observed.get(value,0)+1
                # Callback uses the real lazy dispatch after the mock is removed.
                probs=[]
                for i in range(count):
                    x,p=at(i);probs.append((x[0],Fraction(*p)))
                    self.assertEqual(Fraction(*p),Fraction(observed.get(x[0],0),6**n))
                self.assertEqual(sum(p for x,p in probs),1)
                mean=sum(x*p for x,p in probs)
                variance=sum((x-mean)**2*p for x,p in probs)
                self.assertEqual(mean,Fraction(n,6) if face_count else Fraction(7*n,2))
                self.assertEqual(variance,Fraction(5*n,36) if face_count else Fraction(35*n,12))

    def test_hypergeometric_table_retains_numbers_for_reformatting(self):
        with patch.object(c,'paged_results') as table:
            STSAMP1.show_distribution(8,5,2)
        row=table.call_args.args[2]
        self.assertEqual(row(0)[1],(3,28))
        self.assertEqual(c.answer_text(row(0)[1],'F'),'3/28')
        self.assertEqual(c.answer_text(row(0)[1],'P',2),'10.71%')

    def test_normal_shared_model_and_replacement(self):
        out,prompts=flow(STNDIST.normal_menu,
            ['6','40','4','3','1','44','1','0','4','2','1','0','8','100','10','3','2','2','1','0','0'])
        self.assertIn('z=1.0000',out)
        self.assertIn('x=120.0000',out)
        self.assertEqual(prompts.count('POPULATION MEAN mu: '),2)
        self.assertNotIn('MEAN: ',prompts)
        self.assertIn('LOW x=32.0000',out)

    def test_empirical_parameter_change_updates_the_parent_model(self):
        out,prompts=flow(STNDIST.normal_menu,['4','8','100','10','0','3','2','2','1','0','0'])
        self.assertIn('x=120.0000',out)
        self.assertNotIn('POPULATION MEAN mu: ',prompts)

    def test_normal_bounds_and_native_commands_use_entered_cutoffs(self):
        for event,values,command in [('1',['10'],'normalcdf(-1E99,10.0,9.3,2.0)'),
                                      ('2',['10'],'normalcdf(10.0,1E99,9.3,2.0)'),
                                      ('3',['3.4','5.8'],'normalcdf(3.4,5.8,9.3,2.0)')]:
            out,_=flow(STNDIST.normal_menu,['1','9.3','2',event]+values+['','0'])
            self.assertIn(command,out)
            self.assertIn('z=(x-mu)/sigma',out)

    def test_uniform_variance_and_clipped_probability_work(self):
        out,_=flow(STUNIF.uniform_menu,['3','2','12','1','3','-2','8','0'])
        self.assertIn('VAR=(b-a)^2/12=8.3333',out)
        self.assertIn('P=6/(12-2)=0.600000',out)

    def test_fractional_df_t_probability_and_main_route(self):
        out,_=flow(STHOME.quick_main,['8','2','8.5','1','0','0','0'])
        self.assertIn('DEGREES OF FREEDOM df=8.5',out)
        self.assertIn('PROBABILITY=0.5000000',out)
        self.assertIn('tcdf(-1E99,0.0,8.5)',out)

    def test_real_home_dice_table_and_t_workflows_release_modules(self):
        code="""
import builtins,contextlib,io,STAT1,STCORE as c
c.view=lambda *args:'exit'
for answers in (['3','4','1','2','7','1','0','0','0','0','0'],
                ['8','2','8.5','1','0','0','0'],
                ['3','14','1','8','5','2','10','3','0','0','0','0']):
 for repeat in range(2):
  pending=iter(answers)
  builtins.input=lambda prompt='':next(pending)
  with contextlib.redirect_stdout(io.StringIO()): STAT1.main()
  assert list(pending)==[],list(pending)
  assert not c.topic_modules(),c.topic_modules()
  assert c._call_depth==0
"""
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=Path(__file__).resolve().parent.parent,capture_output=True,text=True,timeout=15)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
