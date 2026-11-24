import math
import STCORE as c

def height(x,df):
  if df==2: return math.exp(-x/2)
  x=max(x,1e-8);mode=max(df-2,1e-8)
  return math.exp((df/2-1)*math.log(x/mode)-(x-mode)/2)

def show(ts,df,alpha,p,cv,key):
  try: import ti_plotlib as plt
  except ImportError: return False
  rejection=key=='1';cutoff=cv if rejection else ts
  high=max(df+6*math.sqrt(2*df),1.15*max(ts,cv))
  peak=max(height(high*i/160,df) for i in range(1 if df<2 else 0,161))
  plt.cls();plt.window(0,319,0,209);plt.pen('thin','solid');plt.color(0,0,0)
  plt.text_at(1,'CHI-SQUARE '+('REJECTION' if rejection else 'p-VALUE'),'center')
  plt.text_at(2,'chi-square AXIS; df=%d' % df,'center')
  plt.color(210,45,45);plt.text_at(3,'CV=%.8g (RED MARK)' % cv,'center')
  plt.color(0,135,55);plt.text_at(4,'TS=%.8g (GREEN MARK)' % ts,'center')
  plt.color(0,0,0);plt.line(26,54,306,54)
  previous=None
  for i in range(161):
    x=high*i/160;px=26+280*i/160
    y=54+70*min(1,height(x,df)/peak)
    if x>=cutoff:
      plt.color(0,100,210);plt.line(px,54,px,y)
    plt.color(0,0,0)
    if previous:plt.line(previous[0],previous[1],px,y)
    previous=(px,y)
  plt.color(210,45,45);px=26+280*cv/high;plt.line(px,54,px,124)
  plt.color(0,135,55);px=26+280*ts/high;plt.line(px,54,px,124)
  plt.color(0,0,0)
  plt.text_at(10,'AXIS: 0 TO %.6g' % high,'center')
  plt.text_at(11,('alpha=%.7g' % alpha) if rejection else ('p-VALUE=%.7g' % p),'center')
  plt.text_at(12,'LEFT = BACK  RIGHT = NEXT','center')
  return c.call('STGKEY','wait',plt)
