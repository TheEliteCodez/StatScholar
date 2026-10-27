import math
import STCORE as c

def fit(points,alpha=.05):
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
    tc=c.call('STTCRIT','t_critical',1-alpha,n-2)
    rc=tc/math.sqrt(tc*tc+n-2)
    # Residual sum is more stable than 1-r^2 near a perfect fit.
    sse=sum((y-(my+slope*(x-mx)))**2 for x,y in points)
    if r is None: ts=p=None
    elif sse==0: ts=None;p=0.0
    else:
        ts=slope*math.sqrt(xx)/math.sqrt(sse/(n-2))
        p=2*c.call('STTCRIT','t_sf',abs(ts),n-2)
    return {'n':n,'mx':mx,'my':my,'xx':xx,'yy':yy,'xy':xy,'slope':slope,
            'intercept':intercept,'r':r,'r2':None if r is None else r*r,
            'ts':ts,'p':p,'rc':rc,'sse':sse,'df':n-2}

def predict(result,x):
    return result['my']+result['slope']*(x-result['mx'])

def scatter(points):
    xmin=min(x for x,y in points);xmax=max(x for x,y in points)
    ymin=min(y for x,y in points);ymax=max(y for x,y in points)
    grid=[[' ']*25 for i in range(9)]
    for x,y in points:
        col=int(round(24*(x-xmin)/(xmax-xmin))) if xmax>xmin else 12
        row=8-int(round(8*(y-ymin)/(ymax-ymin))) if ymax>ymin else 4
        grid[row][col]='*' if grid[row][col]==' ' else '#'
    return ['SCATTERPLOT (* PAIR; # OVERLAP)','y MAX=%.8g' % ymax]+[
        '|'+''.join(row) for row in grid]+['+'+'-'*25,
        'x MIN=%.8g; MAX=%.8g' % (xmin,xmax),'y MIN=%.8g' % ymin]
