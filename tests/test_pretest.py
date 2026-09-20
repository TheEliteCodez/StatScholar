# Author: TheEliteCodez
import contextlib
import io
import math
import subprocess
import sys
import unittest
from fractions import Fraction
from unittest.mock import patch
from test_expansion import flow
import STAT1 as app
import STCORE as c
import STPRE as pre
import STCOUNT as count
import STBMATH as bm
import STFINITE as finite


class Pretest(unittest.TestCase):
    def test_all_thirty_examples_and_routes(self):
        self.assertEqual(len(pre.TITLES),30)
        for number in range(1,31):
            title,body,routes=pre.get_record(number)
            self.assertEqual(title,pre.TITLES[number-1])
            self.assertTrue(body)
            for route in routes.split(','):self.assertIn(route,pre.ROUTES)
        self.assertIn('REPLACEMENT IS NOT STATED',pre.get_record(13)[1])
        self.assertIn('EXACT INTEGER K',pre.get_record(15)[1])
        self.assertIn('DOES NOT STATE ASSIGNMENT',pre.get_record(25)[1])
        self.assertEqual(pre.search('birth weights')[0][0],'PR:24')

    def test_practice_home_worked_example_and_solver(self):
        out,_=flow(app.main,['7','10','1','0','2','69','137','1','0','0','0'])
        self.assertIn('69/137=.5036',out)
        self.assertIn('0.5036',out)

    def test_histogram_uses_same_exact_and_rounded_rows(self):
        rows=[((i,1),c.as_ratio(p)) for i,p in enumerate(['.16','.25','.36','.15','.08'])]
        for rounded in (False,True):
            with patch.object(count,'read_distribution',side_effect=AssertionError('Do not reenter')):
                out,_=flow(lambda:count.distribution_session(rows,rounded),['9','0','2','1','0'] if not rounded else ['9','5','0','0'])
            for text in ['x=0=0.1600','x=4=0.0800']:self.assertIn(text,out)
            self.assertIn('APPROXIMATE HEIGHTS' if rounded else 'mu=1.7400',out)

    def test_birth_weight_report_reuses_mean_sd_and_observations(self):
        out,prompts=flow(app.main,['5','1','8','2350','650','4','2353','2000','1200','3660','1','1','0','2','1','0','0','0','0'])
        for text in ['MIN USUAL=1050.0000','MAX USUAL=3650.0000','z=2.0154 UNUSUALLY HIGH','z=-1.7692 NOT UNUSUAL','z=-3 x=400.0000','z=3 x=4300.0000']:
            self.assertIn(text,out)
        self.assertEqual(prompts.count('MEAN: '),1)
        self.assertEqual(prompts.count('OBSERVATION x: '),4)

    def test_finite_population_model_check(self):
        out,prompts=flow(app.main,['2','N','7','871','80','N','1','0','0'])
        self.assertIn('NOT JUSTIFIED BY 5% RULE',out)
        self.assertNotIn('TRIALS n: ',prompts)
        for n,expected in [('5','YES'),('6','NO')]:
            out,_=flow(finite.finite_check,['100',n,'N','1'])
            self.assertIn('WITHIN COURSE 5% RULE='+expected,out)
        out,_=flow(finite.finite_check,['100','20','Y','1'])
        self.assertIn('YES IF RANDOM EACH DRAW',out)

    def test_new_binomial_fixtures_with_independent_oracle(self):
        for n,p,k,want in [(50,Fraction(14,100),4,'0.1528'),(18,Fraction(3,10),3,'0.1646')]:
            exact=sum(Fraction(math.comb(n,j))*p**j*(1-p)**(n-j) for j in range(k+1))
            actual=bm.binomial_exact_event(n,(p.numerator,p.denominator),('<=',k,0))
            self.assertEqual(Fraction(*actual),exact)
            self.assertEqual(c.fixed(actual,4),want)
        self.assertEqual(c.fixed(bm.binomial_exact_event(25,(3,100),('>=',1,0)),4),'0.5330')

    def test_pretest_banks_are_lazy_and_released(self):
        code="""
import builtins,contextlib,io,sys
import STAT1,STCORE
assert not any(name.startswith('STPRE') for name in sys.modules)
answers=iter(['7','24','1','0','0','0','0'])
def read(prompt=''):
 assert not any(name in sys.modules for name in ('STPRE1','STPRE2','STPRE3'))
 return next(answers)
builtins.input=read
with contextlib.redirect_stdout(io.StringIO()): STAT1.main()
assert list(answers)==[]
assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
"""
        result=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)


if __name__=='__main__': unittest.main()
