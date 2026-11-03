import STCORE as c
from STGPEN import frame,line,ink,scale,number,wait,BLACK,BLUE,RED

def count(source):
    if source[0]=='accessor':return source[1]
    if source[0]=='binomial':return source[1]+1
    if source[0]=='hyper':return min(source[2],source[3])-max(0,source[3]-source[1]+source[2])+1
    return len(source[1])

def row(source,i):
    kind=source[0]
    if kind=='accessor':return source[2](i)
    if kind=='binomial':
        n,p=source[1],number(source[2]);k=i
        if p==0 or p==1:return (k,1),float(k==n*p)
        if p>.5:k=n-k;p=1-p
        # Multiply factors in probability scale; no factorial buffers.
        v=(1-p)**(n-k)
        for j in range(k):v*=((n-j)*p/(j+1))
        return (i,1),v
    if kind=='hyper':
        N,K,n=source[1:];x=max(0,n-N+K)+i
        value=c.call('STSAMP1','event_probability',N,K,n,('=',(x,1),0))
        return (x,1),number(value)
    return source[1][i]

def ordered(rows):
    order=list(range(len(rows)))
    def compare(a,b):
        a=a if isinstance(a,tuple) else (a,1)
        b=b if isinstance(b,tuple) else (b,1)
        return a[0]*b[1]-b[0]*a[1]
    for i in range(1,len(order)):
        k=order[i];j=i
        while j and compare(rows[order[j-1]][0],rows[k][0])>0:
            order[j]=order[j-1];j-=1
        order[j]=k
    starts=[i for i in range(len(order)) if i==0 or compare(rows[order[i]][0],rows[order[i-1]][0])!=0]
    def at(i):
        low=starts[i];high=starts[i+1] if i+1<len(starts) else len(order)
        return rows[order[low]][0],sum(number(rows[order[j]][1]) for j in range(low,high))
    return 'accessor',len(starts),at

def show(source,event=None,title='PROBABILITY BARS',cdf=False,divisor=1):
    if source[0]=='rows':source=ordered(source[1])
    n=count(source)
    if not n:return False
    peak=max(1,sum(number(row(source,i)[1]) for i in range(n))) if cdf else max(number(row(source,i)[1]) for i in range(n)) or 1
    selected_probability=sum(number(row(source,i)[1]) for i in range(n) if c.event_match(row(source,i)[0],*event)) if event else None
    cumulative=0
    for start in range(0,n,16):
        end=min(n,start+16)
        first=number(row(source,start)[0]);last=number(row(source,end-1)[0])
        gap=(last-first)/max(1,end-start-1) if end-start>1 else 1
        low,high=first-gap*.6,last+gap*.6
        plt=frame(title+(' CDF' if cdf else ''),'X %.5g..%.5g; ROWS %d-%d/%d'%(first,last,start+1,end,n),'P(X<=x)' if cdf else 'P(EVENT)=%.7g'%selected_probability if event else 'HEIGHT = P(X)')
        if plt is None:return False
        line(plt,26,160,306,160);line(plt,26,40,26,160)
        ink(plt,'%.4g'%peak,1,40,BLACK)
        previous=(26,160-110*(cumulative/peak)) if cdf else None
        for i in range(start,end):
            exact,p=row(source,i);x=number(exact);p=number(p)
            chosen=event is not None and c.event_match(exact,*event)
            cumulative+=p
            y=160-110*(cumulative if cdf else p)/peak
            at=scale(x,low,high)
            plt.color(*(RED if chosen else BLUE))
            if cdf:
                if previous:
                    line(plt,previous[0],previous[1],at,previous[1]);line(plt,at,previous[1],at,y)
                line(plt,at,y,min(306,at+5),y);previous=(at,y)
            else:
                width=min(10,100/max(1,end-start))
                for dx in range(-int(width),int(width)+1):line(plt,at+dx,160,at+dx,y)
            if i==start or i==end-1 or end-start<=6:ink(plt,'%.4g'%x,at-10,165,BLACK)
        if cdf and previous:line(plt,previous[0],previous[1],306,previous[1])
        plt.color(*BLACK)
        if divisor!=1:plt.text_at(2,'p-hat=X/%g; %.4g..%.4g'%(divisor,first/divisor,last/divisor),'center')
        elif event:plt.text_at(2,'RED = INCLUDED OUTCOMES','center')
        action=wait(plt)
        if action=='back':return action
    return 'next'
