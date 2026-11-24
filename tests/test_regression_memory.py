from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parent.parent

class RegressionMemory(unittest.TestCase):
    def test_scatter_tick_values_align_with_axes_and_unit_labels(self):
        from unittest.mock import patch
        from test_graph_expansion import ExpandedGraphs
        import STGSCAT as scatter
        from test_chi_regression import BOOKS
        with patch.object(scatter,'axis_number',wraps=scatter.axis_number) as numbers:
            plot=ExpandedGraphs().render('STGSCAT','show',BOOKS,'pages','dollars')
        ticks=[call.args[1:] for call in numbers.call_args_list]
        self.assertEqual([tick[0] for tick in ticks if len(tick)==3],[200,400,600,800,1000])
        self.assertEqual([tick[0] for tick in ticks if len(tick)==4],[0,20,40,60,80])
        self.assertEqual(ticks[0],(200,60,49))
        self.assertEqual(ticks[4],(1000,306,49))
        self.assertEqual(ticks[5],(0,53,61,True))
        self.assertEqual(ticks[-1],(80,53,165,True))
        labels=plot.frames[0][1]
        self.assertIn((2,'y: dollars','left'),labels)
        self.assertIn((11,'x: pages','center'),labels)
        for points in ([(1,3)]*4,[(.01,-.5),(.02,-.25)],[(1e20,1e20)]*3):
            ExpandedGraphs().render('STGSCAT','show',points)

    def test_native_graphs_preserve_two_tails_signed_statistic_and_residuals(self):
        from test_graph_expansion import ExpandedGraphs
        renderer=ExpandedGraphs()
        for ts in (-3,3):
            counts=[]
            for key,cutoff in (('1',2.4),('2',3)):
                plot=renderer.render('STGRT','show',ts,7,.05,.01,2.4,key)
                lines,labels=plot.frames[0]
                blue=[coords for color,coords in lines if color==(0,100,210)]
                self.assertTrue(any(coords[0]<166 for coords in blue))
                self.assertTrue(any(coords[0]>166 for coords in blue))
                self.assertTrue(all(abs((coords[0]-166)*4/140)>=cutoff-1e-12 for coords in blue))
                green=[coords for color,coords in lines if color==(0,135,55)]
                self.assertEqual(len(green),1)
                self.assertAlmostEqual(green[0][0],166+140*ts/4)
                self.assertEqual(len([1 for color,coords in lines if color==(210,45,45)]),2)
                self.assertTrue(any('CV=+/-2.4' in args[1] for args in labels))
                counts.append(len(blue))
            self.assertLess(counts[1],counts[0])
        plot=renderer.render('STGSCAT','show',[(1,2),(2,4),(3,5),(4,4)],'pages','dollars',(2,.7),True)
        lines,labels=plot.frames[0]
        self.assertEqual(sum(color==(0,100,210) for color,coords in lines),8)
        self.assertIn((2,'y: RESIDUAL y-yhat','left'),labels)
        self.assertEqual(sum(color==(210,45,45) for color,coords in lines),1)

    def test_import_failure_releases_each_stage_and_allows_a_fresh_home_route(self):
        code=r'''
import builtins,contextlib,gc,io,sys
import STAT1,STCORE as c
original=builtins.__import__;target=[''];hit=[]
def guarded(name,*args,**kwargs):
    if name==target[0]:
        hit.append(name);raise MemoryError('Injected at '+name)
    return original(name,*args,**kwargs)
builtins.__import__=guarded;c.wait_key=lambda:'right'
data=['1','4','1','2','2','4','3','5','4','4','x','y','.05']
for name,answers in [
    ('STREGIN',[]),('STREG',data),('STTCRIT',data),('STREGWK',data),
    ('STREGPR',data+['3']),('STGSCAT',data+['2']),
    ('STREGTXT',data+['2']),('STGRT',data+['8','1']),('STREGDEF',None)]:
    target[0]=name
    pending=iter(['16','2'] if answers is None else ['16','1']+answers)
    builtins.input=lambda prompt='':next(pending)
    try:
        with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
    except MemoryError:pass
    else:raise AssertionError(('Fault not reached',name))
    gc.collect()
    assert hit[-1]==name
    assert not c.topic_modules() and not c._call_depth,(name,c.topic_modules())
    target[0]=''
    pending=iter(['1','0','0']);builtins.input=lambda prompt='':next(pending)
    with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
    assert not list(pending) and not c.topic_modules()
assert len(hit)==9,hit
print('9_IMPORT_FAILURE_CLEANUPS_PASS')
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(run.returncode,0,run.stdout[-2000:]+run.stderr)
        self.assertIn('9_IMPORT_FAILURE_CLEANUPS_PASS',run.stdout)

    def test_all_stages_and_choices_release_functions_before_next_stage(self):
        run=subprocess.run([sys.executable,'-B','-c',
            "import sys;sys.path.insert(0,'tests');from regression_walk import run;r=run();assert not r['failures'],r['failures'][:1];print(len(r['runs']))"],
            cwd=ROOT,capture_output=True,text=True,timeout=180)
        self.assertEqual(run.returncode,0,run.stdout[-2000:]+run.stderr)
        self.assertIn('117',run.stdout)

if __name__=='__main__':unittest.main()
