from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parent.parent


class HypothesisMemory(unittest.TestCase):
    def test_failed_page_import_unwinds_loader_and_next_home_route_runs(self):
        code=r'''
import builtins,contextlib,gc,io
import STAT1,STCORE as c
original=builtins.__import__;target=[''];hits=[];c.wait_key=lambda:'right'
def guarded(name,*args,**kwargs):
    if name==target[0]:hits.append(name);raise MemoryError('Injected import failure: '+name)
    return original(name,*args,**kwargs)
builtins.__import__=guarded
data=['15','3','scores','1','2','65','.05','1','68.84','7.424314','10','','1']
for name in ('STHYMNU','STHYFLOW','STHYANS','STHYREQ','STHYTS','STHYDRAW','STHYPVAL','STHYEND'):
    target[0]=name;pending=iter(data);builtins.input=lambda prompt='':next(pending)
    try:
        with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
    except MemoryError:pass
    else:raise AssertionError(('Failure not reached',name))
    gc.collect();assert not c.topic_modules() and not c._call_depth,name
    target[0]='';pending=iter(['1','0','0']);builtins.input=lambda prompt='':next(pending)
    with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
    assert not list(pending) and not c.topic_modules()
assert len(hits)==8,hits
'''
        self.run_fresh(code)

    def test_all_result_stages_and_previous_problem_data_are_released(self):
        code="import sys;sys.path.insert(0,'tests');from hypothesis_memory_walk import run;r=run();assert not r['failures'];print('HYPOTHESIS_STAGES_PASS')"
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,capture_output=True,text=True,timeout=180)
        self.assertEqual(run.returncode,0,run.stdout[-2500:]+run.stderr)
        self.assertIn('HYPOTHESIS_STAGES_PASS',run.stdout)

    def run_fresh(self,code):
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,
                           capture_output=True,text=True,timeout=20)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)

    def test_t_module_does_not_load_normal_quantile_code(self):
        self.run_fresh("""
import builtins,sys
original=builtins.__import__
def guarded(name,*args,**kwargs):
 if name=='STZCRIT':raise AssertionError('t calculations must not import normal quantile code')
 return original(name,*args,**kwargs)
builtins.__import__=guarded
import STTCRIT
assert abs(STTCRIT.t_critical(.95,9)-2.2621571628)<1e-8
assert abs(STTCRIT.t_sf(1,1)-.25)<1e-8
""")

    def test_real_mean_tests_finish_inference_before_loading_result_pages(self):
        self.run_fresh("""
import builtins,sys
import STAT1,STCORE as c
original=builtins.__import__
loaded=[]
def guarded(name,*args,**kwargs):
 if name=='STTCRIT':
  assert 'STHYRES' not in sys.modules,'Result pages resident during t import'
  assert 'STZCRIT' not in sys.modules,'Normal quantile code resident during t import'
  loaded.append('math')
 if name in ('STHYANS','STHYREQ','STHYTS','STHYEND','STHYDRAW','STHYPVAL'):
  assert 'STTCRIT' not in sys.modules,'t module retained when loading result pages'
  assert 'STHYME' not in sys.modules,'Mean input/calculation module retained during results'
  assert not any(n in sys.modules for n in ('STHYANS','STHYREQ','STHYTS','STHYEND','STHYDRAW','STHYPVAL')),'Text renderers resident together'
  assert 'STHYINF' not in sys.modules,'Inference code resident during text display'
  assert 'math' in loaded,loaded
  loaded.append('results')
 return original(name,*args,**kwargs)
builtins.__import__=guarded
pages=[]
c.view=lambda title,lines:pages.append((title,list(lines)))
cases=[['15','3','grades','1','2','65','.05','1','68.84','7.424314','10','','1','0','0','0'],
 ['15','4','difference','1','2','0','.05','1','1','105','15','100','','1','100','8','100','','0','0','0'],
 ['15','3','measurements','1','2','3','.05','2','5','1','2','3','4','5','','1','0','0','0']]
for repeat in range(2):
 for answers in cases:
  pending=iter(answers);builtins.input=lambda prompt='':next(pending)
  STAT1.main()
  assert not list(pending),answers
  assert not c.topic_modules(),c.topic_modules()
assert loaded.count('results')==60,loaded
assert any(title=='HT 9: FINAL CONCLUSION' for title,lines in pages)
assert any('FAIL TO REJECT H0' in lines for title,lines in pages)
""")

    def test_real_viewer_releases_text_renderer_before_loading_graph(self):
        self.run_fresh("""
import builtins,sys,types,weakref,gc
import STAT1,STCORE as c
original=builtins.__import__;refs=[];graphs=[]
def guarded(name,*args,**kwargs):
 if name=='STHTPLOT':
  gc.collect()
  assert not any(n in sys.modules for n in ('STHYANS','STHYREQ','STHYTS','STHYRES','STHYMNU')),'Text/menu code still loaded at graph import'
  assert 'STHYEND' not in sys.modules,'Conclusion renderer still loaded at graph import'
  assert 'STHYME' not in sys.modules and 'STHYPR' not in sys.modules,'Calculation module retained at graph import'
  assert 'STVDISP' not in sys.modules,'Text viewer still loaded at graph import'
  assert all(ref() is None for ref in refs),'Text renderer still retained in memory'
  graphs.append(True)
 module=original(name,*args,**kwargs)
 if name in ('STHYANS','STHYREQ','STHYTS','STHYEND','STHYDRAW','STHYPVAL'):refs.append(weakref.ref(module))
 return module
builtins.__import__=guarded
plot=types.ModuleType('ti_plotlib')
plot.cls=lambda:None
plot.window=plot.pen=plot.color=plot.line=plot.text_at=lambda *args:None
def blocked():raise AssertionError('Graph must use the exit-key reader')
plot.show_plot=blocked;sys.modules['ti_plotlib']=plot
keys=types.ModuleType('ti_system');sys.modules['ti_system']=keys
c.ON_TI=True;c.KEY_STYLE='scan';c.wait_key=lambda:'right'
for close in (45,105):
 for option,data in [('1',['approval','1','2','.5','.05','60','100','']),
                     ('3',['scores','1','2','65','.05','1','68.84','7.424314','10','','1'])]:
  events=iter([0,close,close,0]*(2 if close==105 else 1));keys.get_key=lambda mode:next(events)
  answers=iter(['15',option]+data+['0','0','0'])
  builtins.input=lambda prompt='':next(answers)
  STAT1.main()
  assert not list(answers) and not list(events)
  assert not c.topic_modules(),c.topic_modules()
# Enter renders two separate stages; Back renders one, for each test type.
assert len(graphs)==6,graphs
""")
