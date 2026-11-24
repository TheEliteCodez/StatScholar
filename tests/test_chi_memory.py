from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parent.parent

class ChiMemory(unittest.TestCase):
    def test_small_graph_key_reader_consumes_held_keys_and_handles_back(self):
        import types
        from unittest.mock import patch
        import STCORE as c
        import STGKEY
        for style,raw,expected in (('scan',105,'next'),('scan',45,'back'),('scan',102,'back'),('ce',5,'next'),('ce',9,'back'),('ce',142,'back')):
            with self.subTest(style=style,raw=raw):
                keys=types.ModuleType('ti_system');plot=types.SimpleNamespace(cls=lambda:None)
                pending=iter([raw,raw,0,raw,raw,0] if style=='scan' else [raw])
                if style=='scan':keys.get_key=lambda mode:next(pending)
                else:keys.wait_key=lambda:next(pending)
                with patch.dict(sys.modules,ti_system=keys),patch.object(c,'KEY_STYLE',style),patch.object(c,'_LAST_RAW',raw):
                    self.assertEqual(STGKEY.wait(plot),expected)
                    self.assertIsNone(c._LAST_RAW)
                    self.assertEqual(list(pending),[])

    def test_dedicated_graph_shapes_and_extremes(self):
        import math
        import STGCHI as graph
        from test_graph_expansion import ExpandedGraphs
        self.assertAlmostEqual(graph.height(4,2),math.exp(-2),places=12)
        self.assertAlmostEqual(graph.height(4,4),math.exp(math.log(2)-1),places=12)
        self.assertGreater(graph.height(.01,1),graph.height(1,1))
        self.assertEqual(graph.height(2,4),1)
        render=ExpandedGraphs()
        for df,ts,p,cv in ((1,20,.0000077442,3.841459),(3,0,1,7.814728),(59,200,0,77.930524),(81,81,.48,103.0095)):
            for key in ('1','2'):
                with self.subTest(df=df,key=key):
                    plot=render.render('STGCHI','show',ts,df,.05,p,cv,key)
                    self.assertEqual(len(plot.frames),1)
                    lines,labels=plot.frames[0]
                    self.assertTrue(any('CV=' in item[1] for item in labels))
                    self.assertTrue(any('TS=' in item[1] for item in labels))
                    self.assertTrue(all(26<=points[0]<=306 and 26<=points[2]<=306
                        for rgb,points in lines if rgb==(0,100,210)))

    def test_home_routes_release_calculation_and_instructions_before_every_graph(self):
        code=r'''
import builtins,sys,types,weakref,gc,contextlib,io,itertools
import STAT1,STCORE as c
original=builtins.__import__;refs=[];graphs=[]
stages=('STCHI','STCHIM','STCHRES','STCHITI','STTCRIT','STVDISP')
def guarded(name,*args,**kwargs):
    if name in ('STGCURV','STGPEN','STWORK'):raise AssertionError('Large helper imported by chi-square: '+name)
    if name=='STGCHI':
        gc.collect()
        assert not any(n in sys.modules for n in stages),c.topic_modules()
        assert all(r() is None for r in refs),'Stage module or its functions retained'
        graphs.append(True)
    module=original(name,*args,**kwargs)
    if name in stages:
        refs.append(weakref.ref(module))
        refs.extend(weakref.ref(v) for v in vars(module).values()
                    if isinstance(v,(types.FunctionType,type)) and v.__module__==name)
    return module
builtins.__import__=guarded
plot=types.ModuleType('ti_plotlib');frames=[]
plot.cls=plot.window=plot.pen=plot.color=plot.line=lambda *a:None
plot.text_at=lambda *a:frames.append(a) if a[0]==1 else None
plot.show_plot=lambda:None;sys.modules['ti_plotlib']=plot
keys=types.ModuleType('ti_system');sys.modules['ti_system']=keys
c.ON_TI=True;c.KEY_STYLE='scan'
events=itertools.cycle((0,105,0));keys.get_key=lambda mode:next(events)
viewer=c.view;reopened=set();pages=[]
def key():
    if current[0] in ('CHI GOF ANSWER','CHI INDEPENDENCE ANSWER','CHI-SQUARE TEST') and current[0] not in reopened:
        reopened.add(current[0]);return '6'
    return 'right'
def view(title,lines):
    current[0]=title;pages.append(title)
    return viewer(title,lines)
c.view=view;c.wait_key=key;current=['']
cases=[['15','5','','1','.05','4','30','10','20','20','1','0'],
       ['15','5','','1','.1','4','1240','1129','359','140','3','.438','.395','.12','.047','0'],
       ['15','5','','1','.1','4','1240','1129','359','140','2','1256','1133','344','135','0'],
       ['15','5','','1','.05','60']+['20']*60+['1','0'],
       ['15','6','','1','.05','2','2','30','10','10','30'],
       ['15','6','','1','.05','10','10']+['20']*100]
with contextlib.redirect_stdout(io.StringIO()):
    for repeat in range(2):
        for answers in cases:
            reopened.clear()
            pending=iter(answers+['2','1','0','0'])
            builtins.input=lambda prompt='':next(pending)
            STAT1.main()
            assert not list(pending)
            assert not c.topic_modules(),c.topic_modules()
assert len(graphs)==48,len(graphs)
assert len(frames)==48,len(frames)
assert pages.count('TI-84 CHI-SQUARE STEPS')==12,pages
print('CHI_MEMORY_PASS')
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,capture_output=True,text=True,timeout=60)
        self.assertEqual(run.returncode,0,run.stdout[-2000:]+run.stderr)
        self.assertIn('CHI_MEMORY_PASS',run.stdout)

if __name__=='__main__':unittest.main()
