import contextlib
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
import STHERR as errors

ROOT=Path(__file__).resolve().parent.parent


class HypothesisErrors(unittest.TestCase):
    def test_decision_and_actual_truth_table(self):
        for reject,truth,expected in [(True,True,'TYPE I ERROR'),(False,False,'TYPE II ERROR'),
            (True,False,'CORRECT DECISION (NO ERROR)'),(False,True,'CORRECT DECISION (NO ERROR)'),
            (True,None,'CANNOT DETERMINE'),(False,None,'CANNOT DETERMINE')]:
            self.assertEqual(errors.classify(reject,truth),expected)

    def test_all_six_claim_relations_and_claim_specific_errors(self):
        for sign,null,alternative,side in [('<','>=','<','H1'),('>','<=','>','H1'),('!=','=','!=','H1'),
            ('<=','<=','>','H0'),('>=','>=','<','H0'),('=','=','!=','H0')]:
            m=errors.model('p',sign,.4,'adults who smoke')
            self.assertEqual((m['h0'],m['h1'],m['claim']),('p '+null+' 0.4','p '+alternative+' 0.4',side))
            rows=errors.describe(m)
            self.assertIn('CONTEXT: adults who smoke',rows)
            self.assertIn('CONCLUDE '+m['h1']+' WHEN ACTUALLY '+m['h0']+'.',rows)
            self.assertIn('II: MISS A TRUE CLAIM' if side=='H1' else 'II: FAIL TO REJECT FALSE CLAIM',rows[:2])

    def test_given_null_direction_difference_and_zero_boundary(self):
        for sign,alt in [('<=','>'),('>=','<'),('=','!='),('=','>'),('=','<')]:
            m=errors.model('p1-p2',sign,0,given_null=True,alternative=alt,claim_side='H1')
            self.assertEqual(m['h0'],'p1-p2 '+sign+' 0')
            self.assertEqual(m['h1'],'p1-p2 '+alt+' 0')
        m=errors.model('mu','>',-2.5)
        self.assertEqual(m['h0'],'mu <= -2.5')

    def test_first_answer_rows_show_errors_hypotheses_and_claim(self):
        rows=errors.describe(errors.model('mu','=',150))
        self.assertEqual(rows[:5],['I: REJECT A TRUE CLAIM','II: FAIL TO REJECT FALSE CLAIM',
                                  'H0: mu = 150','H1: mu != 150','CLAIM IS H0'])

    def test_real_routes_and_cleanup_without_math_or_definition_bank(self):
        code=r'''
import builtins,contextlib,io,sys
import STAT1,STCORE as c
c.wait_key=lambda:'right'
original=builtins.__import__
def guard(name,*args,**kwargs):
 if name in ('STDEFS','STTCRIT','STZCRIT','STHYME','STHYPR','STHTPLOT'):
  raise AssertionError('Unneeded import: '+name)
 return original(name,*args,**kwargs)
builtins.__import__=guard
cases=[
 ['15','9','1','1','adults who smoke','2','40%','1','1','1','0','0','0'],
 ['15','9','2','2','battery life','1','150','3','1','0','0','0','0'],
 ['15','9','3','2','2','0','0','0'],
 ['15','9','3','1','3','0','0','0'],
 ['15','9','4','0','0','0'],
 ['15','9','1','0','0','0','0']]
output=''
for answers in cases:
 pending=iter(answers);builtins.input=lambda prompt='':next(pending)
 with contextlib.redirect_stdout(io.StringIO()) as rendered:STAT1.main()
 assert not list(pending),answers
 assert not c.topic_modules() and not c._call_depth,c.topic_modules()
 output+=rendered.getvalue()
assert 'TYPE I ERROR' in output and 'TYPE II ERROR' in output
assert 'p > 0.4' in output and 'mu != 150' in output
assert 'CANNOT DETERMINE' in output
print('ERROR_ROUTES_PASS')
'''
        result=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,capture_output=True,text=True,timeout=15)
        self.assertEqual(result.returncode,0,result.stdout[-1500:]+result.stderr)
        self.assertIn('ERROR_ROUTES_PASS',result.stdout)
