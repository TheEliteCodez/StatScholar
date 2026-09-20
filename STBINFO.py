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


def followup(n,p,event,answer):
    mean=c.rmul((n,1),p)
    variance=c.rmul(mean,c.radd((1,1),(-p[0],p[1])))
    mu,sd,lo,hi,low,high,first=c.call('STBMATH','usual_counts',n,p)
    q1,q3=binomial_quartiles(n,p)
    iqr=q3-q1
    lower=c.ratio(2*q1-3*iqr,2)
    upper=c.ratio(2*q3+3*iqr,2)
    lines=[]
    append_page(lines,['MEAN / SD / USUAL LIMITS',
        'MEAN='+c.fixed(mean,4),'SD='+c.fixed(sd,4),
        'VARIANCE='+c.fixed(variance,4),
        'MIN USUAL='+c.fixed(lo,4),'MAX USUAL='+c.fixed(hi,4),
        'USUAL = MEAN +/- 2 SD'])
    append_page(lines,['WHOLE-NUMBER USUAL COUNTS',
        'MIN USUAL COUNT='+str(low),'MAX USUAL COUNT='+str(high),
        'LAST UNUSUALLY LOW='+str(low-1 if low>0 else 'NONE'),
        'FIRST UNUSUALLY HIGH='+str(first if first is not None else 'NONE'),
        'BOUNDARIES COUNT AS USUAL','COUNTS RANGE FROM 0 TO '+str(n)])
    append_page(lines,['IQR FENCES / BINOMIAL MODEL',
        'Q1='+str(q1),'Q3='+str(q3),'IQR='+str(iqr),
        'LOWER FENCE='+c.exact_text(lower),'UPPER FENCE='+c.exact_text(upper),
        'CDF QUARTILES; NOT RAW DATA'])
    for label,x in ([('LOWER CUTOFF',event[1]),('UPPER CUTOFF',event[2])]
                    if event[0] in ('[]','()','[)','(]') else [('CUTOFF',event[1])]):
        delta=c.radd(c.to_ratio(x),(-mean[0],mean[1]))
        z=c.fixed(c.number(delta)/sd,4) if sd else 'DNE (SD=0)'
        relation=c.range_relation(x,mean,variance)
        position='UNUSUALLY LOW' if relation<0 else 'UNUSUALLY HIGH' if relation>0 else 'NOT UNUSUAL'
        outlier=c.compare_exact(x,lower)<0 or c.compare_exact(x,upper)>0
        append_page(lines,[label+'='+c.exact_text(x),'z='+z,
            '2 SD: '+position,'IQR OUTLIER='+('YES' if outlier else 'NO'),
            'z=(CUTOFF-MEAN)/SD','2 SD USES UNROUNDED LIMITS',
            'IQR USES Q1/Q3 +/- 1.5 IQR'])
    append_page(lines,['REQUESTED EVENT / PROBABILITY',
        'P(EVENT)='+c.fixed(answer,4),'PROBABILITY CUTOFF=0.05',
        'EVENT UNUSUAL='+('YES' if c.compare_exact(answer,(1,20))<=0 else 'NO'),
        'EVENT P AND 2 SD DIFFER',
        'EXACT POINT P IS NOT A TAIL','NEXT PART KEEPS SAME n,p'])
    return lines
