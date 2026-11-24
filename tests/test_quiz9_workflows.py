"""Quiz 9 Jones: run the real Home menus, calculations and paged viewers."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parent.parent


class QuizNineWorkflows(unittest.TestCase):
    def test_bike_original_changed_count_and_coffee(self):
        code='''
import builtins,contextlib,io,sys,weakref
import STAT1,STCORE as c
view=c.view
c.wait_key=lambda:'right'
cases=[
 (['15','1','SRJC students considering bike commuting','3','2','.1','.01','30','267','','0','0','0'],
  .11235955056179775,.6731890674983145,.2504135077313332,2.3263478740408408,False),
 (['15','1','SRJC students considering bike commuting','3','2','.1','.01','40','267','','0','0','0'],
  .149812734082397,2.71315593870533,.0033322868149438466,2.3263478740408408,True),
 (['15','3','mean daily coffee ounces for SRJC coffee-drinking students','1','1','19','.05','1','11.7','7.9','111','','0','0','0'],
  11.7,-9.73547751845886,7.906058275920912e-17,-1.6588241874019436,True)]
for answers,pe,ts,p,cv,reject in cases:
 pages={};refs=[];pending=iter(answers)
 def read(prompt=''):
  try:return next(pending)
  except StopIteration:raise AssertionError((answers,prompt))
 def record(title,lines):
  assert title!='CHECK ENTERED VALUES',lines
  pages[title]=list(lines)
  refs.extend(weakref.ref(sys.modules[n]) for n in c.topic_modules())
  return view(title,lines)
 builtins.input=read;c.view=record
 with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
 assert list(pending)==[]
 assert not c.topic_modules() and all(ref() is None for ref in refs)
 assert len(pages)==10,pages
 def lines(step):return next(value for title,value in pages.items() if title.startswith('HT '+str(step)+':'))
 actual_pe=float(next(line.split('=')[1] for line in lines(3) if line.startswith('POINT ESTIMATE PE=')))
 actual_ts=float(next(line.rsplit('=',1)[1] for line in lines(5) if line.startswith('TS=')))
 actual_p=float(next(line.split('=')[1] for line in lines(7) if line.startswith('p-VALUE=')))
 actual_cv=float(next(line.split('=')[1] for line in lines(4) if line.startswith('CV=')))
 assert abs(actual_pe-pe)<1e-7
 assert abs(actual_ts-ts)<1e-7
 assert abs(actual_cv-cv)<1e-7
 assert abs(actual_p-p)<1e-7 if p>.001 else abs(actual_p/p-1)<1e-6
 assert ('REJECT H0' if reject else 'FAIL TO REJECT H0') in lines(8)
 assert lines(9)[0]==('REJECT H0' if reject else 'FAIL TO REJECT H0')
 assert any('CLAIM THAT ' in line for line in lines(9))
 assert any('ALIGNS WITH PE' in line for line in lines(6))
 if answers[1]=='1':
  assert 'SRS / RANDOM INDEPENDENT: VERIFY' in lines(1)
  assert 'H0: p = 0.1' in lines(2) and 'H1: p > 0.1' in lines(2)
  assert any('RIGHT TAIL BEYOND CV' in line for line in lines(6))
 else:
  assert 'df=110' in lines(4)
  assert 'H0: mu = 19' in lines(2) and 'H1: mu < 19' in lines(2)
  assert any('LEFT TAIL BEYOND CV' in line for line in lines(6))
print('QUIZ9_WORKFLOWS=PASS')
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,
                           capture_output=True,text=True,timeout=30)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
        self.assertIn('QUIZ9_WORKFLOWS=PASS',run.stdout)


if __name__=='__main__': unittest.main()
