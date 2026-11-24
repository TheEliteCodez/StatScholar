import STCORE as c

def read_pairs(minimum=3):
  key=c.menu('PAIRED DATA INPUT',[('1','ENTER x,y PAIRS'),('2','TI LISTS L1-L6 (KEEP PAIRS)')])
  if key=='0': return
  if key=='1':
    n=c.read_size('NUMBER OF PAIRS: ',100,minimum)
    return [(c.read_number('x%d: ' % (i+1)),c.read_number('y%d: ' % (i+1))) for i in range(n)]
  # Do not use read_raw: it sorts each list, destroying pair correspondence.
  try: from ti_system import recall_list
  except ImportError: raise ValueError('TI LIST IMPORT REQUIRES ti_system.recall_list')
  lx=c.read_size('x LIST NUMBER (1..6): ',6);ly=c.read_size('y LIST NUMBER (1..6): ',6)
  xs=recall_list(str(lx));ys=recall_list(str(ly))
  if xs is None or ys is None or len(xs)!=len(ys) or not minimum<=len(xs)<=100:
    raise ValueError('LISTS NEED MATCHING %d..100 VALUES' % minimum)
  return [(float(xs[i]),float(ys[i])) for i in range(len(xs))]

def read():
  points=read_pairs()
  if points is None: return
  xlabel=input('x VARIABLE / UNITS (ENTER=SKIP): ').strip() or 'x'
  ylabel=input('y VARIABLE / UNITS (ENTER=SKIP): ').strip() or 'y'
  alpha=c.read_number('CORRELATION SIGNIFICANCE alpha: ')
  return points,xlabel,ylabel,alpha
