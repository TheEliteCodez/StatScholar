"""Run with the official MicroPython WASM runner; not a TI heap emulator."""
import builtins
import gc
import sys
import STAT1
import STCORE as c

c.wait_key=lambda:'right'
cases=[
    ('1',['rates','1','2','.5','.05','60','100','']),
    ('2',['rates','1','3','.05','45','64','','34','80','','1']),
    ('3',['grades','1','2','65','.05','1','68.84','7.424314','10','','1']),
    ('4',['difference','1','3','0','.05','1','1','105','15','100','','1','100','8','100','']),
    ('3',['measurements','1','1','100','.05','2','100']+[str(i) for i in range(1,101)]+[''])]

class Plot:
    frames=0
    drawing=False
    def cls(self):
        if self.drawing:self.frames+=1
        self.drawing=False
    def line(self,*args):self.drawing=True
    def text_at(self,*args):pass
    def color(self,*args):pass
    def pen(self,*args):pass
    def window(self,*args):pass

class Keys:
    index=0
    def get_key(self,mode):
        value=(0,105,0)[self.index%3];self.index+=1
        return value

for graphics in (False,True):
    c.ON_TI=graphics
    plot=Plot()
    if graphics:
        sys.modules['ti_plotlib']=plot
        sys.modules['ti_system']=Keys()
        c.KEY_STYLE='scan'
    for repeat in range(2):
        answers=['15']
        for option,data in cases:
            answers+=[option]+data+[str(i) for i in range(1,13)]+['0']
        answers+=['0','0']
        pending=iter(answers);builtins.input=lambda prompt='':next(pending)
        STAT1.main()
        assert list(pending)==[]
        assert not c.topic_modules() and not c._call_depth
        gc.collect()
        print('MPY_BATCH_PASS',graphics,repeat)
    if graphics:assert plot.frames==80,plot.frames
print('MPY_PASS',sys.version)
