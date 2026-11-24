import ast
import builtins
import contextlib
import importlib
import io
import itertools
import math
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest.mock import patch
import STCORE as c
import STGCURV as curve
import STGBARS as bars
import STGUMEA as uniform_mean
import STGQQ as qq

ROOT=Path(__file__).resolve().parent.parent

class Plot(types.ModuleType):
    def __init__(self):
        super().__init__('ti_plotlib');self.frames=[];self.labels=[];self.lines=[];self.rgb=(0,0,0)
    def cls(self):
        if self.lines:self.frames.append((self.lines,self.labels))
        self.lines=[];self.labels=[]
    def window(self,*args):pass
    def pen(self,*args):pass
    def color(self,*rgb):self.rgb=rgb
    def line(self,*points):
        assert all(math.isfinite(x) for x in points),points
        self.lines.append((self.rgb,points))
    def text_at(self,*args):self.labels.append(args)
    def show_plot(self):
        self.frames.append((self.lines,self.labels));self.lines=[]

class ExpandedGraphs(unittest.TestCase):
    def render(self,module,function,*args):
        plot=Plot();keys=types.ModuleType('ti_system');events=itertools.cycle((0,105,0));keys.get_key=lambda mode:next(events)
        with patch.dict(sys.modules,ti_plotlib=plot,ti_system=keys),patch.object(c,'view',return_value=None):
            action=getattr(importlib.import_module(module),function)(*args)
        self.assertTrue(action);self.assertTrue(plot.frames)
        self.assertTrue(all('LEFT = BACK  RIGHT = NEXT' in [x[1] for x in labels] for lines,labels in plot.frames))
        return plot

    def test_probability_oracles_and_degenerate_distribution(self):
        self.assertAlmostEqual(curve.area('NORMAL',0,1,'1',(0,)),.5)
        self.assertAlmostEqual(curve.area('NORMAL',0,1,'outside',(-1.96,1.96)),.0499957903,places=6)
        self.assertAlmostEqual(curve.area('t',0,1,'2',(1,)),.25)
        self.assertAlmostEqual(curve.area('CHI',0,2,'2',(2,)),math.exp(-1))
        self.assertAlmostEqual(curve.area('UNIFORM',2,12,'3',(4,8)),.4)
        self.assertEqual(curve.area('NORMAL',5,0,'1',(5,)),0)
        self.assertEqual(curve.area('NORMAL',5,0,'2',(5,)),0)
        self.assertEqual(curve.area('NORMAL',5,0,'3',(5,5)),1)

    def test_all_continuous_curves_draw_finite_coordinates(self):
        for kind,center,spread in [('NORMAL',100,15),('t',0,9),('UNIFORM',2,12),('CHI',0,1),('CHI',0,12),('NORMAL',5,0),('POSITION',10,2)]:
            for event,bounds in [(None,()),('1',(center,)),('2',(center+1,)),('3',(center-1,center+1)),('outside',(center-1,center+1))]:
                with self.subTest(kind=kind,event=event):self.render('STGCURV','show',kind,center,spread,event,bounds)

    def test_close_curve_labels_use_leaders_instead_of_overlapping(self):
        import STGINK as pen
        with patch.object(curve,'ink',wraps=curve.ink) as direct,patch.object(pen,'ink',wraps=pen.ink) as leaders:
            self.render('STGCURV','show','NORMAL',.4,.05,'3',(.3999,.4001),'p-hat')
        self.assertTrue(leaders.call_count)
        boxes=[]
        for call in direct.call_args_list+leaders.call_args_list:
            _,text,x,y,color=call.args
            box=(x,x+6*len(text)-1,y,y+7)
            for a,b,top,bottom in boxes:
                self.assertTrue(box[1]+1<a or box[0]>b+1 or box[3]+1<top or box[2]>bottom+1,(box,(a,b,top,bottom)))
            boxes.append(box)

    def test_exact_membership_and_discrete_heights(self):
        source=('binomial',4,(1,2))
        self.assertEqual([bars.row(source,i)[1] for i in range(5)],[1/16,4/16,6/16,4/16,1/16])
        for n,p in [(200,(1,100)),(200,(99,100)),(4,(0,1)),(4,(1,1))]:
            src=('binomial',n,p)
            self.assertAlmostEqual(sum(bars.row(src,i)[1] for i in range(n+1)),1,places=10)
        ordered=bars.ordered([((5,1),(1,4)),((0,1),(1,4)),((2,1),(1,4)),((2,1),(1,4))])
        self.assertEqual([bars.row(ordered,i) for i in range(bars.count(ordered))],[((0,1),.25),((2,1),.5),((5,1),.25)])
        hyper=('hyper',10,4,3)
        self.assertAlmostEqual(bars.row(hyper,1)[1],.5)
        for op,expected in [('[]',[1,2]),('() ',[]),('[)',[1]),('(]',[2]),('!=',[0,2,3,4])]:
            if op=='() ':op='()'
            matching=[i for i in range(5) if c.event_match((i,1),op,(1,1),(2,1))]
            self.assertEqual(matching,expected)

    def test_bars_cdf_paging_and_proportion_axis(self):
        p=self.render('STGBARS','show',('binomial',40,(1,2)),('>=',(20,1),0),'BINOMIAL',False,40)
        self.assertEqual(len(p.frames),3)
        self.assertTrue(all(any('p-hat=X/40' in t[1] for t in labels) for lines,labels in p.frames))
        self.render('STGBARS','show',('rows',[((0,1),(1,4)),((2,1),(3,4))]),None,'CDF',True)

    def test_intervals_bounds_and_data_families(self):
        for args in [(0,-.2,.3,.95,'p1-p2'),(10,8,12,.95),(10,10,12,.95,'MEAN','upper'),(10,8,10,.95,'MEAN','lower'),(5,5,5,None)]:
            self.render('STGINTR','show',*args)
        for rows,kind in [([((1,1),2),((4,1),3)],'histogram'),([((1,1),2),((4,1),3)],'dot'),([((0,1),(2,1),2),((2,1),(4,1),3)],'classes'),([('long category '+str(i),i) for i in range(25)],'category')]:
            self.render('STGDATA','show',rows,kind)
        self.render('STGBOX','show',(((1,2,3,4,20,1,5),(20,)),((2,3,4,5,6,2,6),())))
        for residual in (False,True):self.render('STGSCAT','show',[(1,2),(2,4),(3,5)],'x','y',(0,2),residual)
        self.render('STGSCAT','show',[(1,2)]*4)

    def test_qq_and_exact_uniform_mean_coordinates(self):
        for method in ('1','2','3'):
            points=qq.pairs([(1,1),(2,1),(3,1)],method)
            self.assertAlmostEqual(points[1][0],0);self.assertEqual(points[1][1],2)
            self.render('STGQQ','show',[(1,1),(2,1),(3,1)],method)
        self.assertAlmostEqual(uniform_mean.density(.5,0,1,2),2)
        self.assertAlmostEqual(uniform_mean.density(.25,0,1,2),1)
        self.render('STGUMEA','show',0,1,2,('[]',(1,4),(3,4)),.75)

    def test_venn_conditional_regions_and_dice_grid(self):
        for choice in map(str,range(1,8)):
            p=self.render('STGDIAG','venn',100,60,50,30,choice)
            if choice=='6':self.assertIn((11,'DENOM=60','center'),p.frames[0][1])
        p=self.render('STGDIAG','dice',('sum','=',7))
        self.assertIn((11,'FIRST DIE (ROWS); P=6/36','center'),p.frames[0][1])

    def test_cdf_jumps_and_histogram_boundaries_use_numeric_scale(self):
        from STGPEN import BLUE,scale
        p=self.render('STGBARS','show',('rows',[((0,1),(1,4)),((2,1),(1,2)),((5,1),(1,4))]),None,'CDF',True)
        edges=[points for rgb,points in p.frames[0][0] if rgb==BLUE and points[0]==points[2]]
        at0=scale(0,-1.5,6.5)
        self.assertTrue(any(abs(x-at0)<1e-8 and abs(y-49)<1e-8 and abs(b-76.5)<1e-8 for x,y,a,b in edges))
        self.render('STGDATA','show',[((5,1),1),((1,1),2),((1,1),3)],'histogram')
        p=self.render('STGDATA','show',[((0,1),(2,1),2),((2,1),(4,1),3)],'classes')
        lines=[points for rgb,points in p.frames[0][0] if rgb==BLUE]
        self.assertIn((166,49,166,159),lines)
        self.assertIn((166,159,306,159),lines)

    def test_skipping_graph_does_not_import_renderer(self):
        code="""
import builtins,contextlib,io
import STCORE as c
original=builtins.__import__
def guarded(name,*args,**kwargs):
 assert name!='forbidden_graph','Renderer imported without selection'
 return original(name,*args,**kwargs)
builtins.__import__=guarded;c.wait_key=lambda:'right'
with contextlib.redirect_stdout(io.StringIO()):c.view('ANSWER',['P=.5'],('forbidden_graph','show',()))
"""
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)

    def test_metadata_preserves_work_without_copying(self):
        from STGATT import attach
        from STWORK import Chain
        original=['B'];wrapped=attach(original,'STGCURV','show',('NORMAL',0,1))
        combined=['A']+wrapped+['C'];chain=Chain(['START'],combined)
        self.assertEqual(list(chain),['START','A','B','C'])
        self.assertIs(wrapped.lines,original)
        self.assertEqual(chain.graph[0],'STGCURV')

    def test_runtime_budget_and_calculator_argument_compatibility(self):
        files=list(ROOT.glob('ST*.py'))
        self.assertLess(sum(p.stat().st_size for p in files),384000)
        for p in files:
            for node in ast.walk(ast.parse(p.read_text())):
                if isinstance(node,ast.Call):
                    star=False
                    for arg in node.args:
                        if isinstance(arg,ast.Starred):star=True
                        else:self.assertFalse(star,(p.name,node.lineno))

    def test_graph_shortcut_releases_viewer_and_reopens_same_page(self):
        code="""
import builtins,sys,types,weakref,gc,contextlib,io
import STCORE as c
original=builtins.__import__;refs=[];seen=[]
module=types.ModuleType('fake_graph')
def draw():
 gc.collect()
 assert 'STVDISP' not in sys.modules
 assert all(r() is None for r in refs)
 seen.append(True)
module.show=draw;sys.modules['fake_graph']=module
def imported(name,*args,**kwargs):
 m=original(name,*args,**kwargs)
 if name=='STVDISP':refs.append(weakref.ref(m))
 return m
builtins.__import__=imported
keys=iter(['right','6','right','6','esc']);c.wait_key=lambda:next(keys)
with contextlib.redirect_stdout(io.StringIO()):c.view('PAGES',list(map(str,range(20))),('fake_graph','show',()))
assert len(seen)==2 and 'STVDISP' not in sys.modules
"""
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)

if __name__=='__main__':unittest.main()
