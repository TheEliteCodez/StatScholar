import math
import STCORE as c

def read_raw(label):
  c.heading(label)
  raw=input('NUMBER OF VALUES (2..100) OR L1: ').strip().upper()
  values=None
  if raw in ('L1','L2','L3','L4','L5','L6'):
    from ti_system import recall_list
    values=recall_list(raw[1])
    n=len(values) if values is not None else 0
  else:
    n=int(raw)
  if not 2<=n<=100: raise ValueError('USE 2..100 MEASUREMENTS')
  mean=0.0; m2=0.0
  for i in range(n):
    x=float(values[i]) if values is not None else c.read_number('VALUE '+str(i+1)+': ')
    delta=x-mean
    mean+=delta/(i+1)
    m2+=delta*(x-mean)
  return mean,math.sqrt(max(0,m2)/(n-1)),n
