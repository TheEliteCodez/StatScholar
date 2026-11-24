import STCORE as c

def show(ts,df,alpha,p,cv,key):
  try: import ti_plotlib as plt
  except ImportError: return False
  rejection=key=='1';cutoff=cv if rejection else abs(ts)
  extent=max(4,abs(ts)+.5,cv+.5)
  at=lambda x:166+140*x/extent
  plt.cls();plt.window(0,319,0,209);plt.pen('thin','solid');plt.color(0,0,0)
  plt.text_at(1,'CORRELATION '+('REJECTION' if rejection else 'p-VALUE'),'center')
  plt.text_at(2,'t AXIS; df=%d; TWO TAILS' % df,'center')
  plt.color(210,45,45);plt.text_at(3,'CV=+/-%.8g (RED)' % cv,'center')
  plt.color(0,135,55);plt.text_at(4,'TS=%.8g (GREEN)' % ts,'center')
  plt.color(0,0,0);plt.line(26,54,306,54)
  previous=None
  for i in range(161):
    x=-extent+2*extent*i/160;px=26+280*i/160
    y=54+70*(1+x*x/df)**(-(df+1)/2)
    if abs(x)>=cutoff:
      plt.color(0,100,210);plt.line(px,54,px,y)
    plt.color(0,0,0)
    if previous:plt.line(previous[0],previous[1],px,y)
    previous=(px,y)
  plt.color(210,45,45)
  for x in (-cv,cv):plt.line(at(x),54,at(x),124)
  plt.color(0,135,55);plt.line(at(ts),54,at(ts),124)
  plt.color(0,0,0);plt.line(at(0),50,at(0),57)
  plt.text_at(10,'AXIS: %.6g TO %.6g' % (-extent,extent),'center')
  plt.text_at(11,('alpha=%.7g' % alpha) if rejection else ('p-VALUE=%.7g' % p),'center')
  plt.text_at(12,'LEFT = BACK  RIGHT = NEXT','center')
  return c.call('STGKEY','wait',plt)
