import contextlib
import io
import unittest
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch
import STCORE as c

def first_page(function,answers,*args):
    pages=[];pending=iter(answers)
    with patch('builtins.input',side_effect=lambda prompt='':next(pending)),patch.object(c,'view',side_effect=lambda title,rows:pages.append((title,list(rows)))),contextlib.redirect_stdout(io.StringIO()):
        function(*args)
    assert not list(pending)
    return '\n'.join(list(c.wrapped_lines(pages[0][1]))[:c.VIEW_LINES])

class AnswerSummaries(unittest.TestCase):
    def test_hypothesis_opens_on_complete_summary_and_clear_goes_to_review(self):
        code=r'''
import builtins,contextlib,io
import STAT1,STCORE as c
pages=[]
def view(title,rows):
    pages.append((title,list(rows)))
    return 'exit' if title=='HYPOTHESIS: ANSWER' else None
c.view=view
pending=iter(['15','3','grades','1','2','65','.05','1','68.84','7.424314','10','','1','1','0','0','0'])
builtins.input=lambda prompt='':next(pending)
with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
assert not list(pending)
assert pages[0][0]=='HYPOTHESIS: ANSWER'
first='\n'.join(list(c.wrapped_lines(pages[0][1]))[:8])
for value in ('t=','p=','alpha=0.05','CV=','PE=68.84','H0=65','SE=','df=9','n=10'):
    assert value in first,(value,first)
assert not any(title.startswith('HT 5:') for title,rows in pages)
assert not c.topic_modules()
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=Path(__file__).resolve().parent.parent,capture_output=True,text=True,timeout=20)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)

    def test_distribution_planning_and_interval_values_are_on_first_screen(self):
        import STNDIST,STUNIF,STTPROB,STSIZE,STCIMEAN,STCIPROP,STCIMOE,STCLTR
        cases=[
            (STNDIST._normal_probability,['2','115',''],(100,15),('P=0.1586553','mu=100','SD=15','z=1')),
            (STUNIF._uniform_probability,['3','5','10'],(0,20),('P=0.25','a=0','b=20','5.0000','10.0000')),
            (STTPROB.t_probability_session,['1.5'],(9,'2'),('P=','df=9','1.5000')),
            (STSIZE._required_sample_size,['1','95%','','5%'],(),('ROUND UP: n=385','CONFIDENCE=95%','E=0.05','z*=1.95996')),
            (STCIMEAN._one_mean,['1','100','15','36','95%',''],(),('CI=','x-bar=100','SE=2.5','df=35','n=36')),
            (STCIPROP._one_proportion,['60','100','95%'],(),('CI=','p-hat=0.6','SE=','n=100','z*=')),
            (STCIMEAN._two_means,['1','100','15','25','1','105','8','40','95%'],(),('CI=','xbar1=100','s1=15','n1=25','xbar2=105','s2=8','n2=40')),
            (STCIPROP._two_proportions,['60','100','40','80','95%'],(),('CI=','x1=60','n1=100','x2=40','n2=80')),
            (STCIMOE._margin_error,['1','95%','60','100'],(),('E=','n=100','SE=','z*=')),
            (STCLTR._result,['2','105'],('CLT','x-bar',100,2.5,36,['CHECKS MET'],'NORMAL','',True,True,'mu',15),('P(ABOVE)=','n=36','MEAN=100','SE=2.5','105'))]
        for function,inputs,args,expected in cases:
            with self.subTest(solver=function.__module__):
                text=first_page(function,inputs,*args)
                for value in expected:self.assertIn(value,text)

    def test_regression_and_descriptive_summaries_precede_work(self):
        import STREG,STREGWK,STDATA,STDMATH,STBWORD
        from test_chi_regression import BOOKS
        result=STREG.fit(BOOKS)
        text=first_page(STREGWK.show,[],BOOKS,result,.05,'pages','dollars')
        for value in ('y=','n=9','r=','r^2=','p=','alpha=','CRITICAL |r|=','xbar=','ybar=','REJECT H0'):self.assertIn(value,text)
        stats=STDMATH.descriptive([c.as_ratio(str(i)) for i in (1,2,3,4,5)])
        text=first_page(STDATA.summary_results,['0'],stats)
        for value in ('n=','MEAN=','MEDIAN=','SAMPLE SD Sx=','MIN=','MAX='):self.assertIn(value,text)
        text=first_page(STBWORD.wording_session,['10','.05','1','0'],'=')
        for value in ('ANSWER=0.3151','n=10','p=0.05','MEAN=0.5','SD=0.6892'):self.assertIn(value,text)

if __name__=='__main__':unittest.main()
