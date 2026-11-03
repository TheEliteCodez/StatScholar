"""Original paired measurements, both directions, and automatic test/CI work."""
from pathlib import Path
import subprocess
import sys
import unittest

class PairedWorkflow(unittest.TestCase):
    def test_original_pairs_and_lists_real_home_routes(self):
        code=r"""
import builtins,contextlib,io,sys,types,weakref
import STAT1,STCORE as c
c.wait_key=lambda:'right';viewer=c.view
before=[64,145,78,59,78,88,60,78,50,68,85,84,49,76,76,80,56]
after=[126,155,141,92,168,150,104,132,90,136,131,140,83,150,88,146,110]
manual=['1','17']+[str(v) for pair in zip(before,after) for v in pair]
setup=['BEFORE','AFTER','1','pulse bpm','1','1','0','.03','1','94%']
ti=types.ModuleType('ti_system');ti.recall_list=lambda n:before if n=='1' else after
sys.modules['ti_system']=ti
cases=[
 ('full test',['15','8']+manual+setup+['1','2','3','4','5','1','0','0','0'],['d-bar=-51.05882353','TS=(-51.058824-0)/5.0740622=-10.062711','INTERVAL=(-61.32872635, -40.78892071)','REJECT H0']),
 ('CI only',['11','8']+manual+['BEFORE','AFTER','1','1','1','94%','0','0','0'],['INTERVAL=(-61.32872635, -40.78892071)']),
 ('reversed lists',['15','8','2','1','2','BEFORE','AFTER','2','pulse bpm','1','2','0','.03','1','94%','0','0','0'],['d=AFTER MINUS BEFORE','d-bar=51.05882353','REJECT H0','INTERVAL=(40.78892071, 61.32872635)']),
 ('two pairs',['11','8','1','2','1','4','2','6','A','B','1','1','3','90%','0','0','0'],['n=2; df=n-1=1','d-bar=-3.5'])]
for name,answers,expected in cases:
 pending=iter(answers);pages=[];refs=[]
 def read(prompt=''):
  try:return next(pending)
  except StopIteration:raise AssertionError((name,prompt))
 def view(title,lines):
  assert title!='CHECK ENTERED VALUES',(name,list(lines))
  lines=list(lines);pages.extend(lines)
  refs.extend(weakref.ref(sys.modules[n]) for n in c.topic_modules())
  return viewer(title,lines)
 builtins.input=read;c.view=view
 with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
 assert not list(pending),name
 assert not c.topic_modules() and all(ref() is None for ref in refs),name
 text='\n'.join(pages)
 for value in expected:assert value in text,(name,value,text)
print('PAIRED_ROUTES_PASS')
"""
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=Path(__file__).resolve().parent.parent,capture_output=True,text=True,timeout=60)
        self.assertEqual(run.returncode,0,run.stdout[-3000:]+run.stderr)
        self.assertIn('PAIRED_ROUTES_PASS',run.stdout)

if __name__=='__main__': unittest.main()
