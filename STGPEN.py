from STGINK import ink,tag

def wait(plt):
  import STCORE as c
  try: import ti_system as keys
  except ImportError:
    plt.show_plot()
    return 'next'
  poll=getattr(keys,'get_key',None)
  read=(lambda:poll(0)) if poll else getattr(keys,'wait_key',None)
  if read is None:
    plt.show_plot()
    return 'next'
  if poll:
    while read() not in (0,None,''): pass
  while True:
    raw=read();key=c.normalize_key(raw)
    if key in ('left','esc','clear','back','0') or raw in ((142,62,153) if c.KEY_STYLE=='ce' else (102,)):
      action='back'
    elif key in ('enter','right'): action='next'
    else: continue
    if poll:
      while read() not in (0,None,''): pass
    c._LAST_RAW=None
    plt.cls()
    return action

BLACK=(0,0,0);RED=(210,45,45);GREEN=(0,135,55);BLUE=(0,100,210)

def line(plt,x1,y1,x2,y2):
  plt.line(x1,209-y1,x2,209-y2)

def position(score,extent):
  return 8+303*(score+extent)/(2*extent)


def number(x):
  return x[0]/x[1] if isinstance(x,tuple) else x

def frame(title,xlabel='',ylabel=''):
  try: import ti_plotlib as plt
  except ImportError: return None
  plt.cls();plt.window(0,319,0,209);plt.pen('thin','solid');plt.color(*BLACK)
  plt.text_at(1,title[:40],'center')
  plt.text_at(2,xlabel[:40],'center');plt.text_at(11,ylabel[:40],'center')
  plt.text_at(12,'LEFT = BACK  RIGHT = NEXT','center')
  return plt

def scale(value,low,high,a=26,b=306):
  return (a+b)/2 if high==low else a+(b-a)*(value-low)/(high-low)

def dot(plt,x,y,color=BLUE):
  plt.color(*color);plt.pen('medium','solid')
  line(plt,x-1,y,x+1,y);line(plt,x,y-1,x,y+1)
  plt.pen('thin','solid')

def axes(plt,low,high,ymax=1):
  plt.color(*BLACK);line(plt,26,164,306,164);line(plt,26,36,26,164)
  ink(plt,'%.4g'%low,26,170,BLACK);ink(plt,'%.4g'%high,278,170,BLACK)
  ink(plt,'%.4g'%ymax,2,38,BLACK);ink(plt,'0',14,157,BLACK)
