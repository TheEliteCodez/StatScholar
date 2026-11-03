from STGPEN import frame,line,ink,scale,dot,wait,BLACK,BLUE,RED

def show(points,xlabel='x',ylabel='y',fit=None,residual=False):
    def value(x,y):return y-(fit[0]+fit[1]*x) if residual else y
    xmin=min(x for x,y in points);xmax=max(x for x,y in points)
    ymin=min(value(x,y) for x,y in points);ymax=max(value(x,y) for x,y in points)
    if residual:ymin=min(0,ymin);ymax=max(0,ymax)
    xp=(xmax-xmin)*.06 or 1;yp=(ymax-ymin)*.06 or 1
    xa,xb=xmin-xp,xmax+xp;ya,yb=ymin-yp,ymax+yp
    plt=frame('RESIDUAL PLOT' if residual else 'SCATTER / FITTED LINE' if fit else 'SCATTER / QQ PLOT',xlabel,'RESIDUAL y-yhat' if residual else ylabel)
    if plt is None:return False
    at=lambda x:scale(x,xa,xb)
    yof=lambda y:scale(y,ya,yb,160,40)
    line(plt,26,160,306,160);line(plt,26,40,26,160)
    for x,y in points:dot(plt,at(x),yof(value(x,y)))
    if residual:plt.color(*RED);line(plt,26,yof(0),306,yof(0))
    elif fit:
        a,b=fit;plt.color(*RED)
        left,right=xa,xb
        if b:
            limits=sorted(((ya-a)/b,(yb-a)/b));left=max(left,limits[0]);right=min(right,limits[1])
        if left<=right:line(plt,at(left),yof(a+b*left),at(right),yof(a+b*right))
    for text,x,y in [('%.5g'%xmin,26,168),('%.5g'%xmax,270,168),('%.5g'%ymin,1,153),('%.5g'%ymax,1,40)]:ink(plt,text,x,y,BLACK)
    return wait(plt)
