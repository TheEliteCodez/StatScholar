import STCORE as c
from STWORK import Lines, num
from STBW2 import event_bounds, floor_ratio, ceil_ratio, translation

def work(n,p,event,answer=None):
    op,a,b=event
    q=c.radd((1,1),(-p[0],p[1]))
    complement=op in ('>=','>','!=')
    if op=='>=': low,high=0,ceil_ratio(a)-1
    elif op=='>': low,high=0,floor_ratio(a)
    elif op=='!=': low,high=event_bounds(n,('=',a,0))
    else: low,high=event_bounds(n,event)
    low,high=max(0,low),min(n,high)
    count=max(0,high-low+1)
    if answer is None: answer=c.call('STBMATH','binomial_exact_event',n,p,event)
    command=translation(n,p,event)[2]
    def row(i):
        if i==0: return 'P(X=k)=C(n,k)*p^k*q^(n-k)'
        if i==1: return 'n=%d; p=%s; q=1-%s=%s' % (n,num(p),num(p),num(q))
        if i==2: return 'P=1-(' if complement else 'P=('
        if i==count+3: return (('0' if not count else '')+') = '+num(answer))
        if i==count+4: return 'TI: '+command
        k=low+i-3
        return ('+ ' if i>3 else '')+'C(%d,%d)*(%s)^%d*(%s)^%d' % (n,k,num(p),k,num(q),n-k)
    return Lines(count+5,row)
