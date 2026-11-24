"""Real chi-square inputs/results with plot stubs on native MicroPython."""
import builtins
import gc
import sys
import STAT1
import STCORE as c

class Plot:
  def cls(self):pass
  def window(self,*args):pass
  def pen(self,*args):pass
  def color(self,*args):pass
  def line(self,*args):pass
  def text_at(self,*args):pass

class Keys:
  index=0
  def get_key(self,mode):
    value=(0,105,0)[self.index%3];self.index+=1
    return value

c.wait_key=lambda:'right'
viewer=c.view
finals=[]
def view(title,rows):
  if title=='CHI-SQUARE FINAL CONCLUSION':
    rows=list(rows);finals.append(rows[0])
    assert 'alpha=' in rows[1]
    assert 'EVIDENCE' in rows[2]
  return viewer(title,rows)
c.view=view
heap=gc.mem_free()+gc.mem_alloc()
cases=[
 ['15','5','car colors','1','.05','4','30','10','20','20','1','0','0','0'],
 ['15','5','car colors','1','.05','4','20','20','20','20','1','0','0','0'],
 ['15','6','smoking and illness','1','.05','2','2','30','10','10','30','0','0'],
 ['15','6','smoking and illness','1','.05','2','2','20','20','20','20','0','0'],
 ['15','5','categories','1','.05','60']+['20']*60+['1','0','0','0'],
 ['15','6','variables','1','.05','10','10']+['20']*100+['0','0']]
for graphics in (False,True):
  c.ON_TI=graphics
  if graphics:
    sys.modules['ti_plotlib']=Plot();sys.modules['ti_system']=Keys();c.KEY_STYLE='scan'
  for answers in cases:
    pending=iter(answers);builtins.input=lambda prompt='':next(pending)
    STAT1.main()
    assert list(pending)==[]
    assert not c.topic_modules() and not c._call_depth
    gc.collect()
    assert gc.mem_free()+gc.mem_alloc()==heap
assert len(finals)==12
assert finals.count('REJECT H0')==4
print('CHI_NATIVE_PASS',len(finals),heap)
