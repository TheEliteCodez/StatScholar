import math

def height(x,degrees):
  if degrees is None: return math.exp(-x*x/2)
  return (1+x*x/degrees)**(-(degrees+1)/2)

def shaded(x,statistic,alternative):
  if alternative=='<': return x<=statistic
  if alternative=='>': return x>=statistic
  return abs(x)>=abs(statistic)

def line(plt,x1,y1,x2,y2):
  plt.line(x1,209-y1,x2,209-y2)

def position(score,extent):
  return 8+303*(score+extent)/(2*extent)

def curve(setup,result,probability,critical,region='p'):
  try: import ti_plotlib as plt
  except ImportError: return False
  BLACK=(0,0,0);RED=(210,45,45);GREEN=(0,135,55);BLUE=(0,100,210)
  ts=result['ts'];df=result['df'];alt=setup['alternative'];alpha=setup['alpha']
  extent=max(3.5,abs(ts)+.7,max(abs(v) for v in critical)+.7)
  at=lambda score:position(score,extent)
  y=lambda score:100-60*height(score,df)
  plt.cls();plt.window(0,319,0,209)
  plt.pen('medium','solid');plt.color(*(BLUE if region=='p' else RED))
  boundary=ts if region=='p' else (critical[0] if alt=='<' else critical[-1])
  for i in range(241):
    score=-extent+2*extent*i/240
    if shaded(score,boundary,alt): line(plt,at(score),100,at(score),y(score))
  for score in ((boundary,) if alt!='!=' else (-abs(boundary),abs(boundary))):
    line(plt,at(score),100,at(score),y(score))
  plt.pen('thin','solid');plt.color(*BLACK)
  previous=(-extent,y(-extent))
  for i in range(1,241):
    score=-extent+2*extent*i/240
    line(plt,at(previous[0]),previous[1],at(score),y(score));previous=(score,y(score))
  line(plt,8,100,311,100);line(plt,8,132,311,132)
  plt.color(140,140,140);line(plt,at(0),100,at(0),y(0))
  for score in (0,ts)+tuple(critical):
    line(plt,at(score),100,at(score),132)
  for score in (0,)+tuple(critical)+(ts,):
    plt.color(*(GREEN if score==ts else RED if score in critical else BLACK))
    line(plt,at(score),100,at(score),104);line(plt,at(score),132,at(score),136)
  return extent

def show(setup,result,probability,critical,region='p'):
  import STCORE as c
  return c.ht_plot(setup,result,probability,critical,(region,))

def screens(setup,result,probability,critical):
  for region in ('alpha','p'):
    action=show(setup,result,probability,critical,region)
    if not action or action=='back': return action
  return 'next'
