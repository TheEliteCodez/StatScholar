"""Calculation-only CH9d audit: interval bounds and four real HT menu paths."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parent.parent


class CH9DWorkflows(unittest.TestCase):
    def test_interval_and_summary_raw_t_tests(self):
        code='''
import builtins,contextlib,io,sys,weakref
import STAT1,STCORE as c
salaries=['97.32','94.6','98.8','92.52','89.94','94.41','84.82','86.96',
'98.94','85.75','92.23','92.59','92.77','95.17','90.82','89.1',
'97.11','92.43','84.26','89.5','96.18','87.6','92.62','92.21',
'94.94','87.98','96.2','85.19','91.02','92.32','89.17','91.16']
# Numerical targets independently checked with SciPy's t distribution.
cases=[
 ('12',['11','7','1','.30','.025','0','0'],None),
 ('17',['15','3','mean throwing distance in yards','3','2','45','.10','1','51','21.9','15','','3','0','0','0'],
  (51,1.0610913277280596,1.345030374454649,.1533056439671085,False,14)),
 ('18',['15','3','mean doctor salary in thousands of dollars','1','2','89','.05','2','32']+salaries+['','0','0','0'],
  (91.7696875,3.8885538262484483,1.695518782545865,.00024872978836058314,True,31)),
 ('19',['15','3','mean sandwich sodium in milligrams','1','1','920','.01','1','915','18','46','','0','0','0'],
  (915,-1.88398055086813,-2.4121158757033587,.033019092418580656,False,45)),
 ('20',['15','3','mean AP Statistics exam completion time in hours','1','3','2.5','.05','1','2.73','.25','25','','1','0','0','0'],
  (2.73,4.6,2.0638985616280205,.00011483718110812959,True,24))]
viewer=c.view;c.wait_key=lambda:'right'
for question,answers,expected in cases:
 pages={};refs=[];pending=iter(answers)
 def read(prompt=''):
  try:return next(pending)
  except StopIteration:raise AssertionError((question,prompt))
 def view(title,lines):
  assert title!='CHECK ENTERED VALUES',(question,lines)
  pages[title]=list(lines)
  refs.extend(weakref.ref(sys.modules[name]) for name in c.topic_modules())
  return viewer(title,lines)
 builtins.input=read;c.view=view
 with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
 assert list(pending)==[],question
 assert not c.topic_modules() and all(ref() is None for ref in refs),question
 if question=='12':
  assert 'INTERVAL=(0.2750, 0.3250)' in pages['INTERVAL FROM ESTIMATE +/- E']
  continue
 assert len(pages)==10,(question,pages)
 def lines(step):return next(value for title,value in pages.items() if title.startswith('HT '+str(step)+':'))
 pe,ts,cv,p,reject,df=expected
 actual_pe=float(next(line.split('=')[1] for line in lines(3) if line.startswith('POINT ESTIMATE PE=')))
 actual_ts=float(next(line.rsplit('=',1)[1] for line in lines(5) if line.startswith('TS=')))
 actual_p=float(next(line.split('=')[1] for line in lines(7) if line.startswith('p-VALUE=')))
 cvs=[float(v) for v in next(line.split('=')[1] for line in lines(4) if line.startswith('CV=')).split(',')]
 assert abs(actual_pe-pe)<1e-6,(question,actual_pe,pe)
 assert abs(actual_ts-ts)<1e-7,(question,actual_ts,ts)
 assert abs(actual_p-p)<1e-8,(question,actual_p,p)
 assert abs(cvs[-1]-cv)<1e-7,(question,cvs,cv)
 assert 'df='+str(df) in lines(4)
 assert ('REJECT H0' if reject else 'FAIL TO REJECT H0') in lines(8)
 assert lines(9)[0]==('REJECT H0' if reject else 'FAIL TO REJECT H0')
 assert any('CLAIM THAT ' in line for line in lines(9))
 if question=='17':
  assert 'SRS / RANDOM INDEPENDENT: VERIFY' in lines(1)
  assert 'GROUP 1 NORMALITY: VERIFY' in lines(1)
 if question=='20':
  assert len(cvs)==2 and abs(cvs[0]+cv)<1e-7
  assert any('SHADE BOTH TAILS' in line for line in lines(6))
print('CH9D_CALCULATION_WORKFLOWS=PASS')
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,
                           capture_output=True,text=True,timeout=30)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
        self.assertIn('CH9D_CALCULATION_WORKFLOWS=PASS',run.stdout)


if __name__=='__main__': unittest.main()
