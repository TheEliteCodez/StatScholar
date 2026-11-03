import STCORE as c
from STBINFO9 import ratio, radd, rmul, fixed, exact_text
def model_of(n, p, cache):
    if 'model' not in cache:
        mean = rmul((n, 1), p)
        variance = rmul(mean, radd((1, 1), (-p[0], p[1])))
        cache['model'] = (mean, variance, c.call('STBINFO2', 'usual_counts', n, p))
    return cache['model']
def fences_of(n, p, cache):
    if 'quartiles' not in cache: cache['quartiles'] = c.call('STBINFO2', 'binomial_quartiles', n, p)
    q1, q3 = cache['quartiles']
    iqr = q3 - q1
    return ratio(2*q1-3*iqr, 2), ratio(2*q3+3*iqr, 2)
def page(n, p, event, answer, threshold, cache, target):
    if target == 2:
        lower, upper = fences_of(n, p, cache)
        q1, q3 = cache['quartiles']; iqr = q3 - q1
        return ['IQR FENCES','Q1='+str(q1),'Q3='+str(q3),'IQR='+str(iqr),
            'LOWER FENCE='+exact_text(lower),'UPPER FENCE='+exact_text(upper),'CDF QUARTILES']
    mean, variance, model = model_of(n, p, cache)
    mu, sd, lo, hi, low, high, first = model
    if target == 0:
        return ['MEAN / SD / USUAL','MEAN='+fixed(mean,4),'SD='+fixed(sd,4),
            'VARIANCE='+fixed(variance,4),'MIN USUAL='+fixed(lo,4),'MAX USUAL='+fixed(hi,4),'USUAL=MEAN +/- 2SD']
    return ['USUAL COUNTS','MIN COUNT='+str(low),'MAX COUNT='+str(high),
        'UNUSUALLY LOW='+str(low-1 if low > 0 else 'NONE'),'UNUSUALLY HIGH='+str(first if first is not None else 'NONE'),
        'BOUNDARIES USUAL','COUNTS 0 TO '+str(n)]
