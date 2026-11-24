"""Real regression line graph choices on a native MicroPython fixed heap."""
import builtins
import gc
import sys
import STAT1
import STCORE as c

class Plot:
  frames=0
  drawing=False
  title=''
  equation=False
  rgb=(0,0,0)
  blue=0
  red=0
  def cls(self):
    if self.drawing:
      line=self.title in ('SCATTER + REGRESSION LINE','REGRESSION LINE')
      assert self.equation==line
      assert self.red==(1 if line or self.title=='RESIDUAL PLOT' else 0)
      assert self.blue==(0 if self.title=='REGRESSION LINE' else 2*self.n)
      self.frames+=1
    self.drawing=False;self.blue=0;self.red=0;self.equation=False
  def window(self,*args):pass
  def pen(self,*args):pass
  def color(self,*rgb):self.rgb=rgb
  def line(self,*args):
    self.drawing=True
    if self.rgb==(0,100,210):self.blue+=1
    if self.rgb==(210,45,45):self.red+=1
  def text_at(self,row,text,align):
    if row==1:self.title=text
    if row==3:self.equation=text.startswith('yhat=')

class Keys:
  index=0
  def get_key(self,mode):
    value=(0,105,0)[self.index%3];self.index+=1
    return value

sys.modules['ti_system']=Keys()
plot=Plot();sys.modules['ti_plotlib']=plot
c.ON_TI=True;c.KEY_STYLE='scan';c.wait_key=lambda:'right'
heap=gc.mem_free()+gc.mem_alloc()
datasets=[[(248,25.36),(680,47.6),(286,29.02),(906,70.42),(453,35.71),(907,69.49),(838,54.66),(301,18.07),(434,25.38)],
 [(1,9),(2,7),(3,6),(4,2)],[(1,3),(2,3),(3,3)],
 [(2008,55),(2010,95),(2012,141),(2014,182),(2016,227),(2018,273),(2020,338),(2022,435)]]
for index in range(5):
  points=datasets[index] if index<4 else [(i,2*i+3+i%2) for i in range(100)]
  plot.n=len(points)
  answers=['16','1','1',str(len(points))]+[str(v) for pair in points for v in pair]+['pages','dollars','.05','2','6','7','11','0','0','0']
  points=None
  # Consume simulated keystrokes so the fixture does not retain a second raw data set.
  builtins.input=lambda prompt='':answers.pop(0)
  STAT1.main()
  assert answers==[]
  assert not c.topic_modules() and not c._call_depth
  gc.collect()
  assert gc.mem_free()+gc.mem_alloc()==heap
  print('REGRESSION_NATIVE_CASE_PASS',plot.n)
assert plot.frames==20,plot.frames
print('REGRESSION_NATIVE_PASS',plot.frames,heap)
