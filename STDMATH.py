# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STDMATH - loaded only when needed.
import STCORE
RAW_LIMIT = 100  # Desktop tested; physical Evo limit pending.


def sub(a, b):
    return STCORE.radd(a, (-b[0], b[1]))

def read_raw(title='DATA > RAW'):
    STCORE.heading(title)
    n = STCORE.read_size('NUMBER OF VALUES (1..100): ', RAW_LIMIT)
    values = [STCORE.read_exact('VALUE '+str(i+1)+': ') for i in range(n)]
    # Sort in place: retain one raw list, not an additional sorted copy.
    for i in range(1, n):
        x, j = values[i], i
        while j and STCORE.compare_exact(values[j-1], x) > 0:
            values[j] = values[j-1]
            j -= 1
        values[j] = x
    return values

def median_span(values, start, end):
    length = end-start
    if not length: return None
    mid = start+length//2
    return values[mid] if length%2 else STCORE.rdiv(STCORE.radd(values[mid-1], values[mid]), (2,1))

def quartiles(values):
    # Sorted input. TI 1-Var Stats: medians of halves, omit odd center.
    n = len(values)
    return (median_span(values, 0, n//2), median_span(values, 0, n),
            median_span(values, (n+1)//2, n))

def descriptive(values):
    return weighted_stats(value_counts(values))


def weighted_stats(rows):
    import math
    counts={}
    for x,f in rows:
        x=STCORE.to_ratio(x)
        if f>0: counts[x]=counts.get(x,0)+f
    ordered=STCORE.exact_sorted(counts)
    n=sum(counts.values())
    if not n: raise ValueError('NO OBSERVATIONS')
    def at(index):
        running=0
        for x in ordered:
            running+=counts[x]
            if index<running: return x
    def middle(start,end):
        length=end-start
        if not length: return 'DNE'
        m=start+length//2
        return at(m) if length%2 else STCORE.rdiv(STCORE.radd(at(m-1),at(m)),(2,1))
    total=STCORE.rsum(STCORE.rmul(x,(counts[x],1)) for x in ordered)
    mean=STCORE.rdiv(total,(n,1))
    ss=STCORE.rsum(STCORE.rmul(STCORE.rmul(sub(x,mean),sub(x,mean)),(counts[x],1)) for x in ordered)
    var=STCORE.rdiv(ss,(n-1,1)) if n>1 else 'DNE'
    pop=STCORE.rdiv(ss,(n,1))
    q1,med,q3=middle(0,n//2),middle(0,n),middle((n+1)//2,n)
    peak=max(counts.values())
    modes=[x for x in ordered if counts[x]==peak]
    mode='DNE' if peak==1 or len(modes)>2 or (len(modes)==len(ordered) and len(ordered)>1) else ','.join(STCORE.exact_text(x) for x in modes)
    result={'n':n,'SUM':total,'MEAN':mean,'SAMPLE VARIANCE s^2':var,
        'SAMPLE SD Sx':math.sqrt(STCORE.number(var)) if n>1 else 'DNE',
        'POPULATION VARIANCE':pop,'POPULATION SD':math.sqrt(STCORE.number(pop)),
        'MIN':ordered[0],'Q1':q1,'MEDIAN':med,'Q3':q3,'MAX':ordered[-1],
        'MODE':mode,'RANGE':sub(ordered[-1],ordered[0]),'IQR':sub(q3,q1) if n>1 else 'DNE',
        'MIDRANGE':STCORE.rdiv(STCORE.radd(ordered[0],ordered[-1]),(2,1))}
    if n>1:
        distance=STCORE.rmul(result['IQR'],(3,2))
        lo,hi=sub(q1,distance),STCORE.radd(q3,distance)
        inside=[x for x in ordered if STCORE.compare_exact(x,lo)>=0 and STCORE.compare_exact(x,hi)<=0]
        result.update({'LOWER FENCE':lo,'UPPER FENCE':hi,'LOW WHISKER':inside[0],'HIGH WHISKER':inside[-1],
            'OUTLIERS':','.join(STCORE.exact_text(x) for x in ordered if STCORE.compare_exact(x,lo)<0 or STCORE.compare_exact(x,hi)>0) or 'NONE'})
    return result


def edit_raw(values):
    STCORE.paged_results('SORTED VALUES / EDIT INDEX',len(values),lambda i:(str(i+1),values[i]))
    index=STCORE.read_size('SORTED INDEX TO CHANGE: ',len(values))-1
    values[index]=STCORE.read_exact('NEW VALUE: ')
    return STCORE.exact_sorted(values)


def edit_frequency(rows):
    STCORE.paged_results('FREQUENCY ROWS',len(rows),lambda i:(str(i+1),STCORE.exact_text(rows[i][0])+' COUNT='+str(rows[i][1])))
    index=STCORE.read_size('ROW TO CHANGE: ',len(rows))-1
    x=STCORE.read_exact('VALUE: ');f=STCORE.read_int('FREQUENCY: ')
    if f<0: raise ValueError('FREQUENCY MUST BE NONNEGATIVE')
    rows[index]=(x,f)
    return rows


def min_exact(a,b): return a if STCORE.compare_exact(a,b)<=0 else b

def max_exact(a,b): return a if STCORE.compare_exact(a,b)>=0 else b

def value_counts(values):
    counts={}
    for x in values: counts[x]=counts.get(x,0)+1
    return [(x,counts[x]) for x in STCORE.exact_sorted(counts)]

def read_frequency_rows():
    print('EXACT VALUES, NOT CLASS LIMITS')
    rows=[]
    for i in range(STCORE.read_size('NUMBER OF ROWS: ',STCORE.MAX_ROWS)):
        x=STCORE.read_exact('VALUE: '); f=STCORE.read_int('FREQUENCY: ')
        if f<0: raise ValueError('FREQUENCY MUST BE NONNEGATIVE')
        rows.append((x,f))
    return rows



def probe_summary(size):
    # Called only by the optional hardware probe, with STAT1 resident.
    values=[(i,1) for i in range(size)]
    stats=descriptive(values)
    print('RAW '+str(size)+' MEAN='+STCORE.exact_text(stats['MEAN']))
    return stats['MEAN']
