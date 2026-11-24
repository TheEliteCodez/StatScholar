"""CH9c calculation audit, including raw summaries/boxplots reused for t tests."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parent.parent


class CH9CWorkflows(unittest.TestCase):
    def test_seven_t_tests_and_both_modified_boxplots(self):
        code='''
import builtins,contextlib,io,sys,weakref
import STAT1,STCORE as c
fly=[392,383,382,400,400,389,364,385,414,413,402,412,385,399,368,406]
prenatal=[96.23,91.8,100,100,95.8,100,91.8,86.3,92.47,98.2,87.76,98.2,92.1,92.47,96.24,100,98.2,95.8,100,93.63,99,93.63,92.1,87.7,98.2,90.7,95,87.76,96.23,99,92.1,87.76,93.4,93.63]
co2=[7.32,5.93,6.02,7.93,1.8,3.45,7.48,1.46,9.11,.14,.2,6.72,.86,2.45,3.02,.06,1.45,3.01,2.26,1.36,7.84,2.86,4.56,3.45,5.86,2.87,2.44,1.42,3.46,.28,5.94,.79,.78,5.36,1.35,2.27,2.62,2.86]
cases=[
 ('1',['15','3','mean eggs laid by gene-modified fruit flies','3','2','382','.01','2','16']+list(map(str,fly))+['','1','0','0','0'],3.0151851650351666,.004349735637640163,True,15),
 ('2',['15','3','mean clotting time in minutes','1','3','12.8','.01','1','11.9','2.98','48','','0','0','0'],-2.092410371559718,.04182830077705758,False,47),
 ('3',['15','3','mean single-person salary in dollars','1','2','40800','.10','1','42955','7050','69','','0','0','0'],2.5391169396579363,.006702928988372595,True,68),
 ('4',['15','3','mean annual accidents at camera intersections','1','2','4.6','.01','1','5.1','1.56','59','','0','0','0'],2.4619056884194257,.008406967959097702,True,58),
 ('5',['15','3','mean highway mpg','3','3','34','.10','1','36.8','10.6','63','','0','0','0'],2.0966331144285415,.04011263476379944,True,62)]
for question,values,mean,sd,null,alpha,claim,ts,p,df in [
 ('6',prenatal,'94.50617647','4.14486686','80.1','.06','2',20.26644637606731,1.706835225227206e-20,33),
 ('7',co2,'3.39578947','2.53250931','4.87','.01','1',-3.588395102713018,.00047956145479928876,37)]:
 # Summary at 8 places -> existing-data boxplot -> Home -> HT summary input.
 answers=['4','1',str(len(values))]+list(map(str,values))+['2','8','1','4','1','0','0',
          '15','3','mean country measurement','1',claim,null,alpha,'1',mean,sd,str(len(values)),
          '','0','0','0']
 cases.append((question,answers,ts,p,True,df))
viewer=c.view;c.wait_key=lambda:'right'
for question,answers,expected_ts,expected_p,reject,df in cases:
 pages={};pending=iter(answers);refs=[]
 def read(prompt=''):
  try:return next(pending)
  except StopIteration:raise AssertionError((question,prompt))
 def record(title,lines):
  assert title!='CHECK ENTERED VALUES',(question,lines)
  pages[title]=list(lines)
  refs.extend(weakref.ref(sys.modules[n]) for n in c.topic_modules())
  return viewer(title,lines)
 builtins.input=read;c.view=record
 with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
 assert list(pending)==[],question
 assert not c.topic_modules() and all(ref() is None for ref in refs),question
 def step(i):return next(v for title,v in pages.items() if title.startswith('HT '+str(i)+':'))
 ts=float(next(line.rsplit('=',1)[1] for line in step(5) if line.startswith('TS=')))
 p=float(next(line.split('=')[1] for line in step(7) if line.startswith('p-VALUE=')))
 assert abs(ts-expected_ts)<1e-6,(question,ts,expected_ts)
 assert abs(p-expected_p)<1e-8,(question,p,expected_p)
 assert 'df='+str(df) in step(4)
 assert ('REJECT H0' if reject else 'FAIL TO REJECT H0') in step(8)
 if question in ('6','7'):
  box=pages['BOXPLOT VALUES / DRAWING']
  assert 'OUTLIERS=NONE' in box
  expected=['MIN=86.3000','Q1=92.1000','MEDIAN=94.3150','Q3=98.2000','MAX=100.0000'] if question=='6' else ['MIN=0.0600','Q1=1.4200','MEDIAN=2.8600','Q3=5.8600','MAX=9.1100']
  assert all(any(line in row.split('; ') for row in box) for line in expected),(question,box)
print('CH9C_CALCULATION_WORKFLOWS=PASS')
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,
                           capture_output=True,text=True,timeout=30)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
        self.assertIn('CH9C_CALCULATION_WORKFLOWS=PASS',run.stdout)


if __name__=='__main__': unittest.main()
