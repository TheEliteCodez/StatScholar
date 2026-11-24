import STCORE as c

def wait(plt):
  try: import ti_system as keys
  except ImportError:
    plt.show_plot();return 'next'
  poll=getattr(keys,'get_key',None)
  read=(lambda:poll(0)) if poll else getattr(keys,'wait_key',None)
  if read is None:
    plt.show_plot();return 'next'
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
    plt.cls();return action
