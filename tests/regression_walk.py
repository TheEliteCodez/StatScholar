"""Fresh-process regression stage/retention audit; no calculator heap claims."""
import builtins
import contextlib
import gc
import hashlib
import io
import itertools
import json
import math
from pathlib import Path
import sys
import traceback
import types
import weakref

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import STAT1
import STCORE as c

STAGES=('STREGIN','STREG','STTCRIT','STREGWK','STREGPR','STREGDEF','STREGTXT','STGSCAT','STGRT','STREGSUM')
BLOCKED=('STVIN','STWORK','STDEFS','STSTUDY','STGPEN','STGCURV')
BOOKS=list(zip([248,680,286,906,453,907,838,301,434],
               [25.36,47.6,29.02,70.42,35.71,69.49,54.66,18.07,25.38]))

class Plot(types.ModuleType):
    def __init__(self):
        super().__init__('ti_plotlib')
        self.frames=[];self.labels=[];self.lines=0
    def cls(self):
        if self.lines:self.frames.append(self.labels)
        self.labels=[];self.lines=0
    def window(self,*args):pass
    def color(self,*args):pass
    def pen(self,*args):pass
    def line(self,*coords):
        assert all(math.isfinite(x) for x in coords),coords
        self.lines+=1
    def text_at(self,*args):self.labels.append(args[1])

def run():
    original_import=builtins.__import__;original_call=c.call
    original_menu=c.menu;original_choice=c.read_choice
    original_input=builtins.input;original_wait=c.wait_key
    refs={};imports=[];menus={};runs=[];failures=[];current={}
    sizes={p.stem:p.stat().st_size for p in ROOT.glob('ST*.py')}
    def observe(name):
        names=tuple(n for n in sys.modules if n in sizes)
        size=sum(sizes[n] for n in names)
        if size>current.get('peak_loaded_source_bytes',0):
            current['peak_loaded_source_bytes']=size;current['peak_modules']=names
        imports.append(name)
    def guarded(name,*args,**kwargs):
        assert name not in BLOCKED,('Unnecessary regression dependency',name)
        if name=='STTCRIT':assert 'STREG' not in sys.modules,'Fitting code retained during inference'
        if name in STAGES and name not in sys.modules:
            active=[n for n in STAGES if n in sys.modules]
            assert not active or (name=='STTCRIT' and active in (['STREG'],['STREGSUM'])),('Stage overlap',name,active)
        module=original_import(name,*args,**kwargs)
        if name in STAGES:
            refs.setdefault(name,[]).append(weakref.ref(module))
            refs[name].extend(weakref.ref(v) for v in vars(module).values()
                if isinstance(v,(types.FunctionType,type)) and v.__module__==name)
        observe(name)
        return module
    def call(name,function,*args):
        result=original_call(name,function,*args)
        if name in STAGES:
            gc.collect()
            assert name not in sys.modules,('Stage module retained',name)
            assert all(r() is None for r in refs.get(name,())),('Stage functions/classes retained',name)
            refs.pop(name,None)
        return result
    def menu(title,items,*args,**kwargs):
        key=original_menu(title,items,*args,**kwargs)
        menus.setdefault(title,set()).add(key)
        return key
    def choice():
        if sys._getframe(1).f_globals.get('__name__')=='STPAGE':return 'N'
        return original_choice()
    ti=types.ModuleType('ti_system');events=itertools.cycle((0,105,0))
    ti.get_key=lambda mode:next(events)
    ti.recall_list=lambda number:current['xs'] if number=='1' else current['ys']
    sys.modules['ti_system']=ti
    datasets=[('textbooks',BOOKS,451),
        ('manual100',[(i,2*i+3+i%2) for i in range(100)],45),
        ('lists100',[(i,2*i+3+i%2) for i in range(100)],45),
        ('negative',[(1,9),(2,7),(3,6),(4,2)],2.5),
        ('constant',[(1,3),(2,3),(3,3)],2),
        ('perfect',[(1,2),(2,4),(3,6)],2),
        ('calendar',[(2008,55),(2010,95),(2012,141),(2014,182),(2016,227),(2018,273),(2020,338),(2022,435)],2021)]
    routes=[('Home16',['16','1']),('Data',['4','8']),('Graphs',['5','1']),('Hypothesis',['15','7'])]
    builtins.__import__=guarded;c.call=call;c.menu=menu;c.read_choice=choice
    c.wait_key=lambda:'right';c.HAS_KEYS=False;c.KEY_STYLE='scan'
    try:
        for graphics in (False,True):
            for repeat in range(2):
                for label,points,x in datasets:
                    for route,prefix in routes:
                        plot=Plot()
                        if graphics:sys.modules['ti_plotlib']=plot
                        else:sys.modules.pop('ti_plotlib',None)
                        current.clear();current.update(xs=[p[0] for p in points],ys=[p[1] for p in points])
                        start=len(imports)
                        data=['2','1','2'] if label=='lists100' else ['1',str(len(points))]+[str(v) for pair in points for v in pair]
                        inference=['8'] if label=='constant' else ['8','1','8','2']
                        answers=prefix+data+['x','y','.05','1','2','3',str(x),'4',str(x),'30','5','6','7','11']+inference+[
                            '9','4','2',str(x),'10']+[str(i) for i in range(1,16)]+['0','3',str(x),'0','0','0']
                        pending=iter(answers)
                        def read(prompt=''):
                            try:return next(pending)
                            except StopIteration:raise AssertionError(('Unexpected prompt',prompt))
                        builtins.input=read
                        record={'dataset':label,'route':route,'graphics':graphics,'repeat':repeat}
                        try:
                            with contextlib.redirect_stdout(io.StringIO()) as output:STAT1.main()
                            assert not list(pending),'Unconsumed inputs'
                            assert not c.topic_modules() and not c._call_depth,('Topics retained',c.topic_modules())
                            assert not refs,('Stage references retained',tuple(refs))
                            text=output.getvalue()
                            if label=='textbooks':assert 'PREDICTED y=34.13' in text
                            if label=='calendar':assert '372.3928571' in text
                            expected=0 if not graphics else 4 if label in ('constant','perfect') else 6
                            assert len(plot.frames)==expected,(len(plot.frames),expected)
                            record['status']='PASS'
                        except Exception:
                            record['status']='FAIL';record['error']=traceback.format_exc();failures.append(record)
                        record.update({k:v for k,v in current.items() if k not in ('xs','ys')})
                        record['imports']=imports[start:];record['graph_labels']=plot.frames
                        runs.append(record)
        for r,x,expected in (('.65','36.5','16.7'),('.95','36.5','16.1'),('.95','46','DNE')):
            current.clear()
            pending=iter(['16','3','1','.3858','2.02',r,'8','','16.7','30','45','mpg',x,'1','0','0','0'])
            builtins.input=lambda prompt='':next(pending)
            with contextlib.redirect_stdout(io.StringIO()) as output:STAT1.main()
            assert 'ANSWER='+expected in output.getvalue()
            assert not list(pending) and not c.topic_modules() and not refs
            runs.append({'dataset':'given-regression','r':r,'x':x,'answer':expected,'status':'PASS'})
        # Definitions without observations; cancellation before fitting.
        for answers in (['16','2']+[str(i) for i in range(1,16)]+['0','0','0'],['16','1','0','0','0']):
            current.clear();pending=iter(answers);builtins.input=lambda prompt='':next(pending)
            with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
            assert not list(pending) and not c.topic_modules() and not refs
            runs.append({'dataset':'definitions/cancel','status':'PASS'})
    finally:
        builtins.__import__=original_import;builtins.input=original_input
        c.call=original_call;c.menu=original_menu;c.read_choice=original_choice;c.wait_key=original_wait
    choices=menus.get('REGRESSION / CORRELATION',set())
    assert set(map(str,range(12)))<=choices,choices
    assert set(map(str,range(16)))<=menus['REGRESSION DEFINITIONS']
    return {'scope':'Desktop stage lifetimes, real menus/math/viewers, stubbed TI lists/plot/keys; source bytes are not heap bytes.',
        'blocked_imports':BLOCKED,'runs':runs,'failures':failures,
        'menus':{title:sorted(keys) for title,keys in menus.items()},
        'runtime_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.glob('ST*.py'))}}

if __name__=='__main__':
    result=run()
    (ROOT/'artifacts'/'regression_memory.json').write_text(json.dumps(result,indent=2)+'\n')
    print('%d regression runs; %d failures' % (len(result['runs']),len(result['failures'])))
    for failure in result['failures'][:3]:print(failure['error'])
    sys.exit(bool(result['failures']))
