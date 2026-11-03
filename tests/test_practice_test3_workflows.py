"""Actual STAT1 routes supported by Jones Practice Test 3; no invented menus."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parent.parent


class PracticeTestThree(unittest.TestCase):
    def test_supported_tests_interval_critical_values_and_table_probabilities(self):
        code=r'''
import builtins,contextlib,io,sys,weakref
import STAT1,STCORE as c
viewer=c.view;c.wait_key=lambda:'right'
cases=[
 ('Q1',['15','1','proportion of Santa Rosans supporting the tax measure','1','1','.53','.10','45','100','','0','0','0'],
  ['H0: p = 0.53','H1: p < 0.53','POINT ESTIMATE PE=0.45','REJECT H0'],.0544797138940525,-1.6028877994017225),
 ('Q2',['15','1','proportion of voters preferring the Democrat','3','5','.5','.05','513','1068','','0','0','0'],
  ['CLAIM: p >= 0.5','H1: p < 0.5','FAIL TO REJECT H0'],.09936484761063002,-1.285179128860419),
 ('Q3',['15','2','smoker proportion age 20-24 minus age 25-29','1','6','.01','110','500','','63','450','','1','0','0','0'],
  ['H0: p1 = p2','H1: p1-p2 != 0','POINT ESTIMATE PE=0.08','REJECT H0'],.0014220480861436011,3.1901381279259944),
 ('Q4',['11','4','110','500','63','450','95%','0','0'],
  ['p1-hat - p2-hat=0.0800','INTERVAL=(0.0316, 0.1284)'],None,None),
 ('Q10',['14','1','95%','2','40','0','0'],
  ['CRITICAL VALUES=+/-2.022691','df=39.0000'],None,None),
 ('Q11',['14','1','90%','2','17','0','0'],
  ['CRITICAL VALUES=+/-1.745884','df=16.0000'],None,None),
 ('Q13',['15','3','mean annual salary of adults in the town','1','1','30000','.05','1','22298','14200','17','','1','0','0','0'],
  ['H0: mu = 30000','H1: mu < 30000','REJECT H0'],.019961411945432442,-2.2363492625709314),
 ('Q14',['15','3','mean lithium battery capacity in watt hours','1','1','1280','.02','1','1269','13','16','','3','0','0','0'],
  ['H0: mu = 1280','H1: mu < 1280','REJECT H0'],.002042355689855885,-3.3846153846153846),
 ('Q15 z',['15','2','men minus women planning to vote','1','6','.01','170','300','','185','300','','1','0','0','0'],
  ['H0: p1 = p2','POINT ESTIMATE PE=-0.05','FAIL TO REJECT H0'],.21281535168388532,-1.2458612137153107),
 ('Q16 probabilities',['4','4','2','3','WALKERS','NON-WALKERS','LOW','MODERATE','HIGH',
   '35','62','20','21','65','33','1','3','3','2','3','1','2','3','3','2','3','1','0','0','0'],
  ['P(COLUMN)=53/236','P(OR)=75/118','COLUMN GIVEN ROW=20/117','COLUMN GIVEN ROW=33/119',
   'P(COLUMN)=0.225','P(OR)=0.636','COLUMN GIVEN ROW=0.171','COLUMN GIVEN ROW=0.277'],None,None)]
for question,answers,expected,probability,statistic in cases:
 pending=iter(answers);pages=[];refs=[]
 def read(prompt=''):
  try:return next(pending)
  except StopIteration:raise AssertionError((question,prompt))
 def view(title,lines):
  assert title!='CHECK ENTERED VALUES',(question,lines)
  lines=list(lines);pages.append((title,lines))
  refs.extend(weakref.ref(sys.modules[n]) for n in c.topic_modules())
  return viewer(title,lines)
 builtins.input=read;c.view=view
 with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
 assert list(pending)==[],question
 assert not c.topic_modules() and all(ref() is None for ref in refs),question
 text='\n'.join(line for title,lines in pages for line in lines)
 for value in expected:assert value in text,(question,value,text)
 if probability is not None:
  p=float(next(line.split('=')[1] for title,lines in pages for line in lines if line.startswith('p-VALUE=')))
  ts=float(next(line.rsplit('=',1)[1] for title,lines in pages for line in lines if line.startswith('TS=')))
  assert abs(p-abs(probability))<2e-7,(question,p,probability)
  assert abs(ts-statistic)<1e-7,(question,ts,statistic)
print('PRACTICE_TEST3_SUPPORTED_WORKFLOWS=PASS')
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,
                           capture_output=True,text=True,timeout=45)
        self.assertEqual(run.returncode,0,run.stdout[-4000:]+run.stderr)
        self.assertIn('PRACTICE_TEST3_SUPPORTED_WORKFLOWS=PASS',run.stdout)


if __name__=='__main__': unittest.main()
