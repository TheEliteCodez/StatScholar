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
    import math
    n = len(values)
    total = STCORE.rsum(values)
    mean = STCORE.rdiv(total, (n,1))
    q1, median, q3 = quartiles(values)
    variance = STCORE.rdiv(STCORE.rsum(STCORE.rmul(sub(x,mean),sub(x,mean)) for x in values), (n-1,1)) if n>1 else None
    counts = {}
    for x in values: counts[x] = counts.get(x,0)+1
    peak = max(counts.values())
    modes = [x for x in counts if counts[x]==peak]
    mode = 'DNE' if peak==1 or (len(modes)==len(counts) and len(counts)>1) else ','.join(STCORE.exact_text(x) for x in modes)
    return {'n':n, 'SUM':total, 'MEAN':mean, 'SAMPLE SD Sx':math.sqrt(STCORE.number(variance)) if variance else 'DNE',
            'SAMPLE VARIANCE s^2':variance if variance is not None else 'DNE', 'MIN':values[0],
            'Q1':q1 if q1 is not None else 'DNE', 'MEDIAN':median, 'Q3':q3 if q3 is not None else 'DNE',
            'MAX':values[-1], 'MODE':mode, 'RANGE':sub(values[-1],values[0]),
            'IQR':sub(q3,q1) if q1 is not None else 'DNE', 'MIDRANGE':STCORE.rdiv(STCORE.radd(values[0],values[-1]),(2,1))}

def min_exact(a,b): return a if STCORE.compare_exact(a,b)<=0 else b

def max_exact(a,b): return a if STCORE.compare_exact(a,b)>=0 else b

def value_counts(values):
    counts={}
    for x in values: counts[x]=counts.get(x,0)+1
    return [(x,counts[x]) for x in STCORE.exact_sorted(counts)]

def read_frequency_rows():
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
