import math
import STCORE as c

def survival(value,df):
    if df<=0 or value<0: raise ValueError('USE df>0 AND chi-square>=0')
    return _tail(value,df,c.call('STTCRIT','_log_gamma',df/2))

def _tail(value,df,log_gamma):
    if value==0: return 1.0
    a,x=df/2,value/2
    factor=math.exp(a*math.log(x)-x-log_gamma)
    if x<a+1:
        term=total=1/a
        for i in range(1,1001):
            term*=x/(a+i);total+=term
            if abs(term)<abs(total)*1e-12: break
        return max(0,min(1,1-factor*total))
    b=x+1-a;d=1/b;v=1e30;total=d
    for i in range(1,1001):
        an=-i*(i-a);b+=2
        d=an*d+b;v=b+an/v
        if abs(d)<1e-30: d=1e-30
        if abs(v)<1e-30: v=1e-30
        d=1/d;delta=d*v;total*=delta
        if abs(delta-1)<1e-12: break
    return max(0,min(1,factor*total))

def critical(alpha,df):
    if not 0<alpha<1 or df<=0: raise ValueError('USE 0<alpha<1 AND df>0')
    log_gamma=c.call('STTCRIT','_log_gamma',df/2)
    low,high=0.0,max(1.0,float(df))
    while _tail(high,df,log_gamma)>alpha: high*=2
    for i in range(55):
        mid=(low+high)/2
        if _tail(mid,df,log_gamma)>alpha: low=mid
        else: high=mid
    return (low+high)/2

def goodness(observed,expected,fitted=0):
    if len(observed)!=len(expected) or len(observed)<2:
        raise ValueError('NEED MATCHING COUNTS IN 2+ CATEGORIES')
    if any(o<0 or int(o)!=o for o in observed) or any(e<=0 for e in expected):
        raise ValueError('OBSERVED: WHOLE COUNTS >=0; EXPECTED: >0')
    total=sum(observed)
    if total<=0 or abs(total-sum(expected))>1e-7*max(1,total):
        raise ValueError('OBSERVED AND EXPECTED TOTALS MUST MATCH')
    df=len(observed)-1-fitted
    if int(fitted)!=fitted or fitted<0 or df<=0: raise ValueError('CHECK FITTED PARAMETERS / df')
    return sum((o-e)**2/e for o,e in zip(observed,expected)),df

def independence(rows):
    nr=len(rows);nc=len(rows[0]) if nr else 0
    if nr<2 or nc<2 or any(len(row)!=nc for row in rows):
        raise ValueError('NEED A RECTANGULAR 2x2 OR LARGER TABLE')
    flat=[o for row in rows for o in row]
    if any(o<0 or int(o)!=o for o in flat): raise ValueError('USE NONNEGATIVE WHOLE COUNTS')
    rt=[sum(row) for row in rows];ct=[sum(row[j] for row in rows) for j in range(nc)]
    if min(rt+ct)<=0: raise ValueError('REMOVE EMPTY ROWS / COLUMNS')
    total=sum(rt)
    expected=[rt[i]*ct[j]/total for i in range(nr) for j in range(nc)]
    ts=sum((o-e)**2/e for o,e in zip(flat,expected))
    return expected,ts,(nr-1)*(nc-1),rt,ct
