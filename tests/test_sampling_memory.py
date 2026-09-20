import contextlib
from fractions import Fraction
import io
from itertools import combinations
import subprocess
import sys
import unittest
from unittest.mock import patch
import STCORE as c
import STSAMPLE as sample


class SamplingMemory(unittest.TestCase):
    def test_original_and_changed_population_against_enumeration(self):
        for total,targets,draws in [(8,5,2),(6,4,2),(17,5,3),(9,2,4),(5,5,3)]:
            outcomes=[sum(i<targets for i in group) for group in combinations(range(total),draws)]
            for op,cut in [('=',1),('<',2),('>=',1),('<=',0)]:
                predicate={'=':lambda k:k==cut,'<':lambda k:k<cut,'>=':lambda k:k>=cut,'<=':lambda k:k<=cut}[op]
                expected=Fraction(sum(predicate(k) for k in outcomes),len(outcomes))
                self.assertEqual(Fraction(*sample.event_probability(total,targets,draws,(op,cut,0))),expected)
            mean,var,sd=sample.moments(total,targets,draws)
            expected_mean=sum(Fraction(k,len(outcomes)) for k in outcomes)
            expected_var=sum((Fraction(k)-expected_mean)**2 for k in outcomes)/len(outcomes)
            self.assertEqual(Fraction(*mean),expected_mean)
            self.assertEqual(Fraction(*var),expected_var)

    def test_binomial_to_sampling_has_no_counting_or_binomial_engine(self):
        code="""
import builtins,contextlib,io,sys
import STAT1,STCORE
original=builtins.__import__
def guarded(name,*args,**kwargs):
 if name in ('STCOUNT','STBMATH'): raise AssertionError('Unneeded heavy import: '+name)
 return original(name,*args,**kwargs)
builtins.__import__=guarded
STCORE.view=lambda title,lines:print(title,lines)
for repeat in range(3):
 answers=iter(['2','N','6','8','5','2','1','2','1','1','1','1','1','0','0','0'])
 builtins.input=lambda prompt='':next(answers)
 STAT1.main()
 assert list(answers)==[]
 assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
"""
        result=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        for answer in ('E(X)=1.2500','mu=1.2500','P=0.5357'):
            self.assertIn(answer,result.stdout)

    def test_distribution_paging_does_not_build_probability_list(self):
        pages=[]
        with patch.object(sample,'hyper_distribution',side_effect=AssertionError('Do not allocate table')),patch.object(c,'view',side_effect=lambda title,lines:pages.append(list(lines))),patch.object(c,'read_choice',side_effect=['N']*14+['0']),contextlib.redirect_stdout(io.StringIO()):
            sample.show_distribution(200,100,100,True)
        # 101 probabilities plus expected value: 102 rows, at most 7 per page.
        self.assertEqual(len(pages),15)
        self.assertIn('ROWS 99..102/102',pages[-1])
        self.assertIn('E(X)=50.0000',pages[-1])


if __name__=='__main__': unittest.main()
