import contextlib
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
import STCORE as c
import STCHEND

ROOT=Path(__file__).resolve().parent.parent


def payload(table=False,p=.01,label='car colors'):
    return (table,label,'PASS',.05,2,[20,20],[20,20],4,1,p,3.841459,0,[20,20] if table else None,[20,20] if table else None)


class ChiConclusion(unittest.TestCase):
    def test_both_tests_both_decisions_and_alpha_boundary(self):
        for table in (False,True):
            for p,reject in ((.01,True),(.05,True),(.2,False)):
                rows=STCHEND.conclusion(payload(table,p))
                self.assertEqual(rows[0],'REJECT H0' if reject else 'FAIL TO REJECT H0')
                self.assertIn('<= alpha=0.05' if reject else '> alpha=0.05',rows[1])
                self.assertEqual(rows[2],('SUFFICIENT' if reject else 'NOT SUFFICIENT')+
                    (' EVIDENCE OF AN ASSOCIATION.' if table else ' EVIDENCE OF A DIFFERENCE FROM THE MODEL.'))
                self.assertIn('CONTEXT: car colors',rows)
                text=' '.join(rows)
                self.assertIn('AT THE 5% SIGNIFICANCE LEVEL',text)
                self.assertIn('ROW AND COLUMN VARIABLES' if table else 'SPECIFIED MODEL',text)
                self.assertIn('FAILURE TO REJECT DOES NOT PROVE',text)

    def test_final_step_follows_work_and_back_still_exits(self):
        for stop in (False,True):
            pages=[]
            def view(title,rows):
                pages.append((title,list(rows)))
                if stop and title=='CHI-SQUARE TEST':return 'back'
            with patch.object(c,'ON_TI',False),patch.object(c,'view',side_effect=view):
                c.call('STCHISH','show',payload())
            titles=[t for t,r in pages]
            self.assertEqual(titles[-1],'CHI-SQUARE TEST' if stop else 'CHI-SQUARE FINAL CONCLUSION')
            if not stop:self.assertEqual(titles[-2],'CHI-SQUARE TEST')

    def test_real_home_results_release_work_before_final_formatter(self):
        code=r'''
import builtins,contextlib,gc,io,sys,types,weakref
import STAT1,STCORE as c
c.wait_key=lambda:'right'
original=builtins.__import__;refs=[];finals=[]
def guard(name,*args,**kwargs):
 if name=='STCHEND':
  gc.collect()
  assert not any(n in sys.modules for n in ('STCHI','STCHIM','STCHRES','STCHROW','STCHITI','STVDISP','STGCHI'))
  assert all(r() is None for r in refs),'Work code retained before final conclusion'
 module=original(name,*args,**kwargs)
 if name in ('STCHRES','STCHROW','STCHITI'):
  refs.append(weakref.ref(module))
  refs.extend(weakref.ref(v) for v in vars(module).values() if isinstance(v,(types.FunctionType,type)) and v.__module__==name)
 return module
builtins.__import__=guard
viewer=c.view
def view(title,rows):
 if title=='CHI-SQUARE FINAL CONCLUSION':
  rows=list(rows);finals.append(rows)
 return viewer(title,rows)
c.view=view
cases=[['15','5','car colors','1','.05','4','30','10','20','20','1','0','0','0'],
 ['15','5','car colors','1','.05','4','20','20','20','20','1','0','0','0'],
 ['15','6','smoking and illness','1','.05','2','2','30','10','10','30','0','0'],
 ['15','6','smoking and illness','1','.05','2','2','20','20','20','20','0','0']]
for repeat in range(2):
 for answers in cases:
  pending=iter(answers);builtins.input=lambda prompt='':next(pending)
  with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
  assert not list(pending) and not c.topic_modules() and not c._call_depth
assert len(finals)==8
assert sum(rows[0]=='REJECT H0' for rows in finals)==4
assert sum(rows[0]=='FAIL TO REJECT H0' for rows in finals)==4
print('CHI_FINAL_PASS')
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(run.returncode,0,run.stdout[-1800:]+run.stderr)
        self.assertIn('CHI_FINAL_PASS',run.stdout)
