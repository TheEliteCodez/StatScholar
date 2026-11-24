import subprocess
import sys
from pathlib import Path
import unittest
import STREGSUM as solver

ROOT=Path(__file__).resolve().parent.parent

class GivenRegression(unittest.TestCase):
    def test_both_equation_forms_copy_a_and_b_without_changing_their_roles(self):
        code=r'''
import builtins,contextlib,io
import STAT1,STCORE as c
c.wait_key=lambda:'right';viewer=c.view;shown=[]
def view(title,rows):
    rows=list(rows);shown.append((title,rows));return viewer(title,rows)
c.view=view
cases=[(['1','.3858','2.02','.65','8','.1','16.7','30','45','mpg','36.5','1'],'ANSWER=16.1 mpg','y=0.3858*x+2.02'),
       (['2','2.02','.3858','.65','8','.1','16.7','30','45','mpg','36.5','1'],'ANSWER=16.1 mpg','y=2.02+0.3858*x'),
       (['2','35.417','-.016024','-.69','9','','','1980','2018','kg/$','2008','3'],'ANSWER=3.241 kg/$','y=35.417-0.016024*x')]
for entries,answer,equation in cases:
    shown.clear();pending=iter(['16','3']+entries+['0','0','0']);prompts=[]
    def read(prompt=''):
        prompts.append(prompt);return next(pending)
    builtins.input=read
    with contextlib.redirect_stdout(io.StringIO()) as output:STAT1.main()
    assert not list(pending) and not c.topic_modules()
    expected_prompts=['SLOPE (a=) (x COEFFICIENT): ','INTERCEPT (b=) (CONSTANT): '] if entries[0]=='1' else ['INTERCEPT (a=) (CONSTANT): ','SLOPE (b=) (x COEFFICIENT): ']
    assert prompts[3:5]==expected_prompts,prompts
    assert 'r^2 IS NOT NEEDED HERE.' in output.getvalue()
    rows=next(rows for title,rows in shown if title=='GIVEN REGRESSION: ANSWER')
    assert rows[0]==answer,(rows[0],answer)
    assert rows[7]==equation,(rows[7],equation)
pending=iter(['16','3','0','0','0']);builtins.input=lambda prompt='':next(pending)
with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
assert not list(pending) and not c.topic_modules()
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(run.returncode,0,run.stdout[-2000:]+run.stderr)

    def test_equation_mean_and_dne_rules(self):
        data=solver.prepare(.3858,2.02,.65,8,16.7,30,45)
        self.assertAlmostEqual(data['rc'],.706734400730638,11)
        self.assertAlmostEqual(data['p'],.081020351562499,11)
        self.assertEqual(solver.choose(data,36.5)[:2],('USE MEAN y',16.7))
        for x in (30,45):self.assertEqual(solver.choose(data,x)[0],'USE MEAN y')
        self.assertEqual(solver.choose(data,46)[0],'DNE')
        data=solver.prepare(.3858,2.02,.95,8,16.7,30,45)
        self.assertEqual(solver.choose(data,36.5)[0],'USE EQUATION')
        self.assertAlmostEqual(solver.choose(data,36.5)[1],16.1017)
        data=solver.prepare(-.3858,30,-.95,8,None,30,45)
        self.assertAlmostEqual(solver.choose(data,36.5)[1],15.9183)
        self.assertEqual(solver.choose(solver.prepare(.3858,2.02,.65,8,None,30,45),36.5)[0],'DNE')
        self.assertEqual(solver.choose(solver.prepare(.3858,2.02,.95,8,16.7,None,None),36.5)[0],'DNE')
        self.assertEqual(solver.choose(solver.prepare(.3858,2.02,.65,8,16.7,30,45,.1),36.5)[0],'USE EQUATION')
        self.assertEqual(solver.prepare(2,1,-1,8,None,0,10)['p'],0)

    def test_real_home_route_first_screen_and_reuse_without_heavy_imports(self):
        code=r'''
import builtins,contextlib,gc,io,sys,types,weakref
import STAT1,STCORE as c
original=builtins.__import__;refs=[];trefs=[];stages=[]
def guarded(name,*args,**kwargs):
    assert name not in ('STVIN','STWORK','STREG','STREGIN','STREGWK','STREGPR','STDEFS','STGPEN','STGCURV'),name
    module=original(name,*args,**kwargs)
    if name in ('STTCRIT','STREGSUM'):
        stages.append(name)
        refs.extend(weakref.ref(v) for v in vars(module).values() if isinstance(v,(types.FunctionType,type)) and v.__module__==name)
        if name=='STTCRIT':trefs.extend(weakref.ref(v) for v in vars(module).values() if isinstance(v,types.FunctionType) and v.__module__==name)
    return module
builtins.__import__=guarded;viewer=c.view;pages=[];c.wait_key=lambda:'right'
def view(title,lines):
    assert title!='CHECK ENTERED VALUES',(title,list(lines))
    assert 'STTCRIT' not in sys.modules
    gc.collect();assert all(ref() is None for ref in trefs)
    rows=list(lines);pages.append((title,rows))
    return viewer(title,rows)
c.view=view
for repeat in range(2):
    pages.clear();stages.clear()
    pending=iter(['16','3','1','.3858','2.02','.65','8','','16.7','30','45','mpg','36.5','1','1','46','1','1','30','1','0','0','0'])
    builtins.input=lambda prompt='':next(pending)
    with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
    assert not list(pending)
    first='\n'.join(list(c.wrapped_lines(pages[0][1]))[:8])
    for value in ('ANSWER=16.7 mpg','USE MEAN y','x=36.5','30..45','r=0.65','0.70673','p=0.0810204','alpha=0.05','MEAN y=16.7'):
        assert value in first,(value,first)
    assert pages[1][1][0]=='ANSWER=DNE'
    assert 'ANSWER=16.7 mpg'==pages[2][1][0]
    assert stages.count('STTCRIT')==1,stages
    gc.collect();assert not c.topic_modules() and not c._call_depth
    assert all(ref() is None for ref in refs)
print('GIVEN_REGRESSION_PASS')
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(run.returncode,0,run.stdout[-2000:]+run.stderr)
        self.assertIn('GIVEN_REGRESSION_PASS',run.stdout)

if __name__=='__main__':unittest.main()
