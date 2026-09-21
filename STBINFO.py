# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Compact binomial follow-up pages; loaded only after an event is calculated.
import STCORE as c


def binomial_quartiles(n,p):
    # Discrete quantile: smallest k with CDF(k) >= .25 or .75.
    a,den=c.to_ratio(p)
    if a==0: return 0,0
    if a==den: return n,n
    b=den-a
    total=den**n
    term=b**n
    cumulative=0
    q1=None
    for k in range(n+1):
        cumulative+=term
        if q1 is None and 4*cumulative>=total: q1=k
        if 4*cumulative>=3*total: return q1,k
        if k<n: term=term*(n-k)*a//((k+1)*b)


def append_page(lines,page):
    count=sum(1 for line in c.wrapped_lines(page))
    lines.extend(page)
    lines.extend(['']*((-count)%c.VIEW_LINES))


def report_pages(n,p,event=None,answer=None,threshold=(1,20),cache=None):
    cache={} if cache is None else cache
    if 'model' not in cache:
        mean=c.rmul((n,1),p)
        variance=c.rmul(mean,c.radd((1,1),(-p[0],p[1])))
        model=c.call('STBMATH','usual_counts',n,p)
        cache['model']=(mean,variance,model)
    mean,variance,model=cache['model']
    mu,sd,lo,hi,low,high,first=model
    yield ['MEAN / SD / USUAL LIMITS','MEAN='+c.fixed(mean,4),'SD='+c.fixed(sd,4),
        'VARIANCE='+c.fixed(variance,4),'MIN USUAL='+c.fixed(lo,4),'MAX USUAL='+c.fixed(hi,4),'USUAL = MEAN +/- 2 SD']
    yield ['WHOLE-NUMBER USUAL COUNTS','MIN USUAL COUNT='+str(low),'MAX USUAL COUNT='+str(high),
        'LAST UNUSUALLY LOW='+str(low-1 if low>0 else 'NONE'),'FIRST UNUSUALLY HIGH='+str(first if first is not None else 'NONE'),
        'BOUNDARIES COUNT AS USUAL','COUNTS RANGE FROM 0 TO '+str(n)]
    if 'quartiles' not in cache: cache['quartiles']=binomial_quartiles(n,p)
    q1,q3=cache['quartiles'];iqr=q3-q1
    lower=c.ratio(2*q1-3*iqr,2);upper=c.ratio(2*q3+3*iqr,2)
    yield ['IQR FENCES / BINOMIAL MODEL','Q1='+str(q1),'Q3='+str(q3),'IQR='+str(iqr),
        'LOWER FENCE='+c.exact_text(lower),'UPPER FENCE='+c.exact_text(upper),'CDF QUARTILES; NOT RAW DATA']
    observations=[] if event is None else ([('LOWER CUTOFF',event[1]),('UPPER CUTOFF',event[2])] if event[0] in ('[]','()','[)','(]') else [('CUTOFF',event[1])])
    for label,x in observations:
        delta=c.radd(c.to_ratio(x),(-mean[0],mean[1]))
        z=c.fixed(c.number(delta)/sd,4) if sd else 'DNE (SD=0)'
        relation=c.range_relation(x,mean,variance)
        position='UNUSUALLY LOW' if relation<0 else 'UNUSUALLY HIGH' if relation>0 else 'NOT UNUSUAL'
        outlier=c.compare_exact(x,lower)<0 or c.compare_exact(x,upper)>0
        yield [label+'='+c.exact_text(x),'z='+z,'2 SD: '+position,'IQR OUTLIER='+('YES' if outlier else 'NO'),
            'z=(CUTOFF-MEAN)/SD','2 SD USES UNROUNDED LIMITS','IQR USES Q1/Q3 +/- 1.5 IQR']
    if answer is not None:
        yield ['REQUESTED EVENT / PROBABILITY','P(EVENT)='+c.fixed(answer,4),'PROBABILITY CUTOFF='+c.exact_text(threshold),
            'EVENT UNUSUAL='+('YES' if c.compare_exact(answer,threshold)<=0 else 'NO'),'EVENT P AND 2 SD DIFFER',
            'EXACT POINT P IS NOT A TAIL','NEXT PART KEEPS SAME n,p']


def followup(n,p,event,answer,threshold=(1,20)):
    lines=[]
    for page in report_pages(n,p,event,answer,threshold): append_page(lines,page)
    return lines


def show_answer(n,p,event,answer,title,first_page=None,threshold=(1,20),cache=None):
    cache={} if cache is None else cache
    index=0
    while True:
        if first_page is not None and index==0: page=first_page
        else:
            target=index-(1 if first_page is not None else 0)
            page=None
            for i,part in enumerate(report_pages(n,p,event,answer,threshold,cache)):
                if i==target: page=part;break
            if page is None: return
        action=c.view(title,page)
        if action=='exit': return
        if action=='back':
            if index==0: return
            index-=1
        else: index+=1
