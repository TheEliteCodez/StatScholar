"""Real Home 15 paging and stage lifetime checks; desktop, not TI heap proof."""
import builtins
import contextlib
import gc
import hashlib
import io
import itertools
import json
from pathlib import Path
import sys
import types
import weakref

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import STAT1
import STCORE as c

LEAVES=('STHYANS','STHYREQ','STHYTS','STHYDRAW','STHYPVAL','STHYEND')
MATH=('STHYPR','STHYME','STHYIO','STMEAN','STHYINF','STTCRIT','STZCRIT','STWORK','STSEWORK','STTBETA')
WATCH=('STHOME','STHYFLOW','STHYMNU','STHYSH','STHTPLOT','STVDISP','STGPEN','STHTLAB','STHTHEAD','STGINK','STGKEY')+LEAVES+MATH

class Model(dict):pass

class Plot(types.ModuleType):
    def __init__(self):super().__init__('ti_plotlib');self.frames=0;self.drawing=False
    def cls(self):
        if self.drawing:self.frames+=1
        self.drawing=False
    def line(self,*args):self.drawing=True
    def text_at(self,*args):pass
    def color(self,*args):pass
    def pen(self,*args):pass
    def window(self,*args):pass

def run():
    original_import=builtins.__import__;original_call=c.call;original_input=builtins.input
    viewer=c.view;wait=c.wait_key;old_ti=c.ON_TI;old_style=c.KEY_STYLE
    refs={};models=[];phase=['menu'];records=[];current={};seen=set()
    sizes={p.stem:p.stat().st_size for p in ROOT.glob('ST*.py')}
    def dead(names):
        gc.collect()
        for name in names:
            assert name not in sys.modules,('Module retained',name,phase[0])
            assert all(r() is None for r in refs.get(name,())),('Code retained',name,phase[0])
    def guarded(name,*args,**kwargs):
        assert name not in ('STHYRES','STHYSH','STHYP','STVIN','STGPEN','STWORK'),('Old formatter/input helper loaded',name)
        if name in ('STHYMNU',)+LEAVES+('STHTPLOT',):dead(('STHOME','STHYFLOW'))
        if name=='STHYMNU':
            dead(('STHYSH','STHTPLOT')+LEAVES+MATH)
            assert all(r() is None for r in models),'Previous result retained into next problem'
        elif name in ('STHYPR','STHYME'):
            dead(('STHYMNU','STHYSH')+LEAVES)
            assert all(r() is None for r in models),'Previous model retained at next calculation'
        elif name=='STHYSH':dead(('STHYMNU',)+MATH+LEAVES)
        elif name in LEAVES:dead(('STHYMNU',)+MATH+tuple(n for n in LEAVES if n!=name))
        elif name=='STVDISP':dead(('STHYMNU',)+LEAVES+MATH)
        elif name=='STHTPLOT':dead(('STHYMNU','STVDISP')+LEAVES+MATH)
        if name=='STHTLAB':dead(('STHTPLOT','STGPEN','STGINK'))
        elif name=='STHTHEAD':dead(('STHTPLOT','STHTLAB','STGINK','STGPEN'))
        elif name=='STGKEY':dead(('STHTPLOT','STHTLAB','STHTHEAD','STGINK','STGPEN'))
        module=original_import(name,*args,**kwargs)
        if name in WATCH:
            refs.setdefault(name,[]).append(weakref.ref(module))
            refs[name].extend(weakref.ref(v) for v in vars(module).values()
                if isinstance(v,(types.FunctionType,type)) and v.__module__==name)
        names=tuple(n for n in sys.modules if n in sizes)
        amount=sum(sizes[n] for n in names)
        if amount>current.get('peak_loaded_source_bytes',0):
            current['peak_loaded_source_bytes']=amount;current['peak_modules']=names
        return module
    def call(module,function,*args):
        if module=='STHYMNU':phase[0]='menu'
        if module in ('STHYPR','STHYME') and function=='session':phase[0]='input'
        value=original_call(module,function,*args)
        if module in ('STHYPR','STHYME') and function=='session' and value is not None:
            setup,result,inference=value
            setup=Model(setup);result=Model(result)
            models.extend((weakref.ref(setup),weakref.ref(result)))
            value=setup,result,inference;phase[0]='results'
        return value
    def view(title,rows):
        assert title!='CHECK ENTERED VALUES',(title,list(rows))
        dead(('STHOME','STHYFLOW','STHYMNU')+LEAVES+MATH)
        seen.add(title)
        return viewer(title,rows)
    ti=types.ModuleType('ti_system');events=itertools.cycle((0,105,0));ti.get_key=lambda mode:next(events)
    sys.modules['ti_system']=ti;c.KEY_STYLE='scan';c.wait_key=lambda:'right'
    cases=[
        ('one proportion','1',['rates','1','2','.5','.05','60','100','']),
        ('two proportions','2',['rates','1','3','.05','45','64','','34','80','','1']),
        ('one mean','3',['grades','1','2','65','.05','1','68.84','7.424314','10','','1']),
        ('two means','4',['difference','1','3','0','.05','1','1','105','15','100','','1','100','8','100','']),
        ('raw100','3',['measurements','1','1','100','.05','2','100']+[str(i) for i in range(1,101)]+[''])]
    builtins.__import__=guarded;c.call=call;c.view=view
    try:
        for graphics in (False,True):
            c.ON_TI=graphics;plot=Plot()
            if graphics:sys.modules['ti_plotlib']=plot
            else:sys.modules.pop('ti_plotlib',None)
            for repeat in range(2):
                answers=['15']
                for label,option,data in cases:
                    answers+=[option]+data+[str(i) for i in range(1,13)]+['0']
                answers+=['0','0']
                pending=iter(answers);builtins.input=lambda prompt='':next(pending)
                current.clear();seen.clear();start=plot.frames
                with contextlib.redirect_stdout(io.StringIO()):STAT1.main()
                assert not list(pending)
                dead(WATCH);assert not c.topic_modules() and not c._call_depth
                assert all(r() is None for r in models),'Result retained after exit'
                for index in range(1,10):assert any(t.startswith('HT '+str(index)+':') for t in seen) or (graphics and index==6)
                assert 'HYPOTHESIS: ANSWER' in seen
                if graphics:assert plot.frames-start==40,plot.frames-start
                records.append(dict(current,graphics=graphics,repeat=repeat,problems=5,graph_frames=plot.frames-start))
    finally:
        builtins.__import__=original_import;builtins.input=original_input;c.call=original_call
        c.view=viewer;c.wait_key=wait;c.ON_TI=old_ti;c.KEY_STYLE=old_style
    return {'scope':'20 real problems in four continuous runs; all nine steps, review 1..12, text and TI plot/key stubs. Module/function/class and previous-model lifetime checks; not physical heap measurements.',
        'runs':records,'failures':[],
        'runtime_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.glob('ST*.py'))}}

if __name__=='__main__':
    result=run();(ROOT/'artifacts'/'hypothesis_memory.json').write_text(json.dumps(result,indent=2)+'\n')
    print('20 continuous hypothesis problems; all review choices; zero lifetime failures')
