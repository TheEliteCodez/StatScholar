# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

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
STCORE.view=lambda title,lines:print(title,list(lines))
for repeat in range(3):
 answers=iter(['2','N','N','3','8','5','2','5','1','2','1','1','1','1','1','0','0','0'])
 builtins.input=lambda prompt='':next(answers)
 STAT1.main()
 assert list(answers)==[]
 assert not set(STCORE.topic_modules()).intersection(sys.modules)
"""
        result=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        for answer in ('mu=1.2500','P=0.5357'):
            self.assertIn(answer,result.stdout)

    def test_distribution_paging_does_not_build_probability_list(self):
        pages=[]
        with patch.object(sample,'hyper_distribution',side_effect=AssertionError('Do not allocate table')),patch.object(c,'view',side_effect=lambda title,lines:pages.append(list(lines))),patch.object(c,'read_choice',side_effect=['N']*14+['0']),contextlib.redirect_stdout(io.StringIO()):
            sample.show_distribution(200,100,100,True)
        # 101 probabilities plus expected value: 102 rows, at most 7 per page.
        self.assertEqual(len(pages),15)
        self.assertIn('ROWS 97..102/102',pages[-1])
        self.assertIn('E(X)=50.0000',pages[-1])


if __name__=='__main__': unittest.main()


class ApproximateInputMemory(unittest.TestCase):
    def test_clt_changed_values_do_not_import_exact_or_format_modules(self):
        code = """
import builtins, sys
import STAT1, STCORE
original = builtins.__import__
def guarded(name,*args,**kwargs):
    if name in ('STEXACT','STEFMT'):
        raise AssertionError('CLT numeric input loaded '+name)
    return original(name,*args,**kwargs)
builtins.__import__ = guarded
lines = []
STCORE.view = lambda title,values: lines.extend(values)
for repeat in range(3):
    answers = iter(['9','2','','100','30/2','36','1','','2','2','105','0','0'])
    builtins.input = lambda prompt='': next(answers)
    STAT1.main()
    assert list(answers) == []
    assert not set(STCORE.topic_modules()).intersection(sys.modules)
assert 'P(ABOVE)=0.022750 (2.2750%)' in lines, lines
"""
        run = subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)

    def test_direct_numeric_reader_formats_and_retry(self):
        with patch('builtins.input',side_effect=['bad','1/0','3/8','12.5%','-2.5e2','1/8%']),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual([c.read_number('VALUE: ') for _ in range(4)], [.375,.125,-250,.00125])


class RuntimeModuleCleanup(unittest.TestCase):
    def test_cleanup_discovers_loaded_topics_without_static_registry(self):
        code = """
import sys, types
import STAT1, STCORE
sys.modules['STTEMP'] = types.ModuleType('STTEMP')
sys.modules['OTHER_TEMP'] = types.ModuleType('OTHER_TEMP')
assert 'STTEMP' in STCORE.topic_modules()
STCORE.release_topics()
assert 'STTEMP' not in sys.modules
assert 'OTHER_TEMP' in sys.modules
assert 'STAT1' in sys.modules and 'STCORE' in sys.modules
"""
        run = subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
