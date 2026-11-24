import STCORE as c

def pairs(values,method):
  n=len(values)
  points=[]
  for i,x in enumerate(values):
    rank=i+1
    p=(rank-.375)/(n+.25) if method=='1' else (rank-.5)/n if method=='2' else rank/(n+1)
    points.append((c.call('STZCRIT','standard_normal_quantile',p),c.number(x)))
  return points

def show(values,method):
  points=pairs(values,method)
  return c.call('STGSCAT','show',points,'NORMAL z','ORDERED x')
