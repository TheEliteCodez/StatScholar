import math
import STCORE as c

def fit(points,alpha=.05,inference=True):
  n=len(points)
  if n<3: raise ValueError('REGRESSION INFERENCE NEEDS 3+ PAIRS')
  if not 0<alpha<1: raise ValueError('USE 0<alpha<1')
  # Center relative to the first pair to retain precision for calendar years.
  ox,oy=points[0]
  mx=ox+sum(x-ox for x,y in points)/n;my=oy+sum(y-oy for x,y in points)/n
  xx=sum((x-mx)**2 for x,y in points);yy=sum((y-my)**2 for x,y in points)
  xy=sum((x-mx)*(y-my) for x,y in points)
  if xx<=0: raise ValueError('x VALUES MUST VARY')
  slope=xy/xx;intercept=my-slope*mx
  r=max(-1,min(1,xy/math.sqrt(xx*yy))) if yy>0 else None
  # Residual sum is more stable than 1-r^2 near a perfect fit.
  sse=sum((y-(my+slope*(x-mx)))**2 for x,y in points)
  if r is None: ts=p=tc=rc=None
  else:
    ts=None if sse==0 else slope*math.sqrt(xx)/math.sqrt(sse/(n-2))
    if inference:
      tc,p=c.call('STTCRIT','regression_inference',ts,n-2,alpha)
      rc=tc/math.sqrt(tc*tc+n-2)
    else:tc=p=rc=None
  return {'n':n,'mx':mx,'my':my,'xx':xx,'yy':yy,'xy':xy,'slope':slope,
      'intercept':intercept,'r':r,'r2':None if r is None else r*r,
      'ts':ts,'p':p,'rc':rc,'tc':tc,'sse':sse,'df':n-2}

def predict(result,x):
  return result['my']+result['slope']*(x-result['mx'])

def scatter(points): return c.call('STREGTXT','scatter',points)
