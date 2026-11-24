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
BOOKS=list(zip([248,680,286,906,453,907,838,301,434],
               [25.36,47.6,29.02,70.42,35.71,69.49,54.66,18.07,25.38]))


class NumericalTests(unittest.TestCase):
    def test_textbook_model_and_rounding(self):
        result=reg.fit(BOOKS)
        self.assertAlmostEqual(result['slope'],.06895963765320982,14)
        self.assertAlmostEqual(result['intercept'],3.0285501042589686,12)
        self.assertAlmostEqual(reg.predict(result,451),34.1293466858566,12)
        with patch('builtins.input',side_effect=['4','2','451']),patch.object(ui.c,'view') as view:
            ui.rounded_prediction(result,'dollars')
        lines=view.call_args.args[1]
        self.assertIn('yhat=0.06896*x + 3.029',lines)
        self.assertIn('PREDICTED y=34.13',lines)

    def test_rounding_keeps_significant_zeros_and_unrounded_prediction(self):
        result=reg.fit([(1,-.87655),(2,-.75310),(3,-.62965)])
        with patch('builtins.input',side_effect=['2','2','100']),patch.object(ui.c,'view') as view:
            ui.rounded_prediction(result,'units')
        lines=view.call_args.args[1]
        self.assertIn('yhat=0.12*x - 1.0',lines)
        self.assertIn('INTERCEPT=-1.0',lines)
        # Rounding the slope first would instead give 11.00.
        self.assertIn('PREDICTED y=11.35',lines)

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
    def test_regression_streams_work_without_shared_formatter_or_prediction_imports(self):
        code=r'''
import builtins,contextlib,io,sys,types,weakref,gc
import STAT1,STCORE as c
original=builtins.__import__;refs=[];phase=['fit'];seen=[]
def guarded(name,*args,**kwargs):
    if name=='STWORK':raise AssertionError('Regression imported STWORK')
    if name=='STREG' and phase[0]!='fit':raise AssertionError('Prediction reimported fit module')
    module=original(name,*args,**kwargs)
    if name in ('STREG','STTCRIT'):
        refs.append(weakref.ref(module))
        refs.extend(weakref.ref(v) for v in vars(module).values()
                    if isinstance(v,(types.FunctionType,type)) and v.__module__==name)
    return module
builtins.__import__=guarded
viewer=c.view;c.wait_key=lambda:'right'
def view(title,lines):
    assert title!='CHECK ENTERED VALUES',(title,list(lines))
    phase[0]='results';gc.collect()
    assert 'STREG' not in sys.modules and 'STTCRIT' not in sys.modules
    assert all(ref() is None for ref in refs),'Fit functions retained during results'
    if title in ('REGRESSION WORK / RESULTS','PAIRED WORK TABLE'):
        assert not isinstance(lines,(list,tuple)),'Work was materialized'
        assert sum(1 for line in lines)==len(lines)
        assert sum(1 for line in lines)==len(lines),'Work cannot be replayed'
        seen.append(title)
    return viewer(title,lines)
c.view=view
books=['1','9','248','25.36','680','47.6','286','29.02','906','70.42','453','35.71','907','69.49','838','54.66','301','18.07','434','25.38']
ti=types.ModuleType('ti_system');xs=list(range(100));ys=[2*x+3+x%2 for x in xs]
ti.recall_list=lambda number:xs if number=='1' else ys
sys.modules['ti_system']=ti
cases=[books,['2','1','2'],['1','3','1','3','2','3','3','3'],['1','3','1','2','2','4','3','6']]
for repeat in range(2):
    for data in cases:
        phase[0]='fit'
        pending=iter(['16','1']+data+['x','y','.05','5','9','4','2','451','3','451','4','451','30','1','0','0','0'])
        builtins.input=lambda prompt='':next(pending)
        with contextlib.redirect_stdout(io.StringIO()) as output:STAT1.main()
        assert not list(pending)
        assert not c.topic_modules(),c.topic_modules()
        if data is books:assert 'PREDICTED y=34.13' in output.getvalue()
assert len(seen)==24,len(seen)
print('STREAMED_REGRESSION_PASS')
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,capture_output=True,text=True,timeout=60)
        self.assertEqual(run.returncode,0,run.stdout[-2000:]+run.stderr)
        self.assertIn('STREAMED_REGRESSION_PASS',run.stdout)

    def test_all_new_routes_real_viewer_and_unloading(self):
        code=r'''
import builtins,contextlib,io,sys,types,weakref
import STAT1,STCORE as c
c.wait_key=lambda:'right';viewer=c.view
base=['1','8','2008','55','2010','95','2012','141','2014','182','2016','227','2018','273','2020','338','2022','435','year','billion kWh','.05']
books=['1','9','248','25.36','680','47.6','286','29.02','906','70.42','453','35.71','907','69.49','838','54.66','301','18.07','434','25.38','pages','dollars','.05']
cases=[
('Home regression',['16','1']+books+['9','4','2','451','3','451','10','6','0','0','0','0','0'],['yhat=0.06896*x + 3.029','PREDICTED y=34.13','34.12934669','PREDICTED y WHEN x=0']),
('Regression definitions before data',['16','2','1','0','0','0','0'],['FITS A STRAIGHT LINE']),
('Study regression definitions',['6','7','7','8','0','0','0','0','0'],['OBSERVED MINUS PREDICTED']),
('Search regression definitions',['6','7','5','slope','1','0','0','0','0','0'],['m=b IS SLOPE']),
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
    with contextlib.redirect_stdout(io.StringIO()) as output:STAT1.main()
    assert not list(pending),name
    text=' '.join(('\n'.join(pages)+'\n'+output.getvalue()).split())
    for value in expected:assert value in text,(name,value,text)
    assert not c.topic_modules() and all(ref() is None for ref in refs),name
print('NEW_ROUTES_PASS')
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,capture_output=True,text=True,timeout=60)
        self.assertEqual(run.returncode,0,run.stdout[-2000:]+run.stderr)
        self.assertIn('NEW_ROUTES_PASS',run.stdout)


if __name__=='__main__': unittest.main()
