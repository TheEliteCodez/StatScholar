"""Numerical references and real Home routes for the missing test topics."""
import contextlib
import io
import math
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest.mock import patch

import STCHIM as chi
import STREG as reg
import STREGIO as ui

ROOT=Path(__file__).resolve().parent.parent
POINTS=list(zip([2008,2010,2012,2014,2016,2018,2020,2022],
                [55,95,141,182,227,273,338,435]))


class NumericalTests(unittest.TestCase):
    def test_gof_and_both_contingency_tables(self):
        ts,df=chi.goodness([12,15,16,18,19],[16]*5)
        self.assertEqual((ts,df),(1.875,4))
        self.assertAlmostEqual(chi.survival(ts,df),.758735901686298,10)
        self.assertAlmostEqual(chi.critical(.05,df),9.487729036781154,8)
        expected,ts,df,rt,ct=chi.independence([[170,185],[130,115]])
        self.assertEqual(expected,[177.5,177.5,122.5,122.5])
        self.assertAlmostEqual(ts,1.552170163840184,10)
        self.assertAlmostEqual(chi.survival(ts,df),.212815351683882,9)
        expected,ts,df,rt,ct=chi.independence([[35,62,20],[21,65,33]])
        self.assertAlmostEqual(expected[0],27.76271186440678,10)
        self.assertEqual(df,2)
        self.assertAlmostEqual(ts,6.743080512016168,10)
        self.assertAlmostEqual(chi.survival(ts,df),.034336709269794,10)
        self.assertEqual(rt,[117,119]);self.assertEqual(ct,[56,127,53])

    def test_chi_tail_extremes_and_inverse(self):
        for x in (0,1,5,100,1000):
            self.assertAlmostEqual(chi.survival(x,2),math.exp(-x/2),11)
        for df in (1,2,4,10,81):
            for alpha in (.001,.01,.05,.5,.99):
                self.assertAlmostEqual(chi.survival(chi.critical(alpha,df),df),alpha,9)
        self.assertAlmostEqual(chi.critical(.01,1),6.6348966010212145,8)

    def test_changed_data_and_invalid_models(self):
        self.assertEqual(chi.goodness([10,20,30],[10,20,30],1),(0,1))
        for observed,expected in [([1,2],[1,1]),([-1,3],[1,1]),([1.5,2.5],[2,2]),([0,0],[0,0])]:
            with self.assertRaises(ValueError): chi.goodness(observed,expected)
        for rows in ([[0,0],[1,2]],[[1,2],[3]],[[1,-2],[3,4]]):
            with self.assertRaises(ValueError): chi.independence(rows)

    def test_regression_question17(self):
        r=reg.fit(POINTS)
        self.assertAlmostEqual(r['r'],.9883149983136859,12)
        self.assertAlmostEqual(r['r2'],.9767665358917809,12)
        self.assertAlmostEqual(r['slope'],25.69047619047619,11)
        self.assertAlmostEqual(r['rc'],.7067344007306537,6)
        self.assertAlmostEqual(r['p'],3.95377995824197e-6,10)
        self.assertAlmostEqual(reg.predict(r,2021),372.392857142857,9)
        self.assertAlmostEqual(435-reg.predict(r,2022),36.916666666667,9)

    def test_regression_changed_pairs_and_degenerate_data(self):
        r=reg.fit([(1,8),(2,6),(3,4),(4,2)])
        self.assertEqual(r['slope'],-2);self.assertEqual(r['r'],-1);self.assertEqual(r['p'],0)
        r=reg.fit([(1,3),(2,3),(3,3)])
        self.assertIsNone(r['r']);self.assertIsNone(r['p'])
        with self.assertRaises(ValueError): reg.fit([(2,1),(2,3),(2,5)])
        # Sorting lists separately would turn this negative relationship positive.
        ti=types.ModuleType('ti_system')
        ti.recall_list=lambda number: {'1':[3,1,2],'2':[2,6,4]}[number]
        with patch.dict(sys.modules,{'ti_system':ti}),patch('builtins.input',side_effect=['2','1','2']):
            self.assertEqual(ui.read_pairs(),[(3,2),(1,6),(2,4)])
        self.assertIn('SCATTERPLOT',reg.scatter(POINTS)[0])


class HomeReplay(unittest.TestCase):
    def test_all_new_routes_real_viewer_and_unloading(self):
        code=r'''
import builtins,contextlib,io,sys,types,weakref
import STAT1,STCORE as c
c.wait_key=lambda:'right';viewer=c.view
base=['1','8','2008','55','2010','95','2012','141','2014','182','2016','227','2018','273','2020','338','2022','435','year','billion kWh','.05']
cases=[
('GOF equal',['15','5','','1','.05','5','12','15','16','18','19','1','0','0','0'],['chi-square=SUM((O-E)^2/E)=1.875','FAIL TO REJECT H0']),
('GOF counts',['15','5','','1','.05','3','10','20','30','2','10','20','30','0','0','0'],['chi-square=SUM((O-E)^2/E)=0']),
('GOF probabilities',['15','5','','1','.05','3','10','20','30','3','1/6','1/3','.5','0','0','0'],['chi-square=SUM((O-E)^2/E)=0']),
('Vote table',['15','6','','1','.01','2','2','170','185','130','115','0','0'],['E=355*300/600=177.5','FAIL TO REJECT H0']),
('Walking table',['15','6','','1','.05','2','3','35','62','20','21','65','33','0','0'],['chi-square=SUM((O-E)^2/E)=6.743080512','REJECT H0']),
('Regression',['4','8']+base+['2','3','2021','4','2022','435','5','1','0','0','0'],['r^2=0.9767665359','372.3928571','36.91666667','SCATTERPLOT']),
('Hypothesis link',['15','7']+base+['0','0','0'],['r^2=0.9767665359']),
('Graph link',['5','1']+base+['2','0','0','0'],['SCATTERPLOT'])]
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
    text='\n'.join(pages)
    for value in expected:assert value in text,(name,value,text)
    assert not c.topic_modules() and all(ref() is None for ref in refs),name
print('NEW_ROUTES_PASS')
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,capture_output=True,text=True,timeout=60)
        self.assertEqual(run.returncode,0,run.stdout[-2000:]+run.stderr)
        self.assertIn('NEW_ROUTES_PASS',run.stdout)


if __name__=='__main__': unittest.main()
