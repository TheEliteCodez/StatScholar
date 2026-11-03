import STCORE as c
import math
def usual_counts(n, p):
    a, b = p
    mn, md = n*a, b
    vn, vd = n*a*(b-a), b*b
    mu = mn/md
    sd = math.sqrt(vn/vd)
    lo = mu - 2*sd
    hi = mu + 2*sd
    def rel(k):
        d = k*md - mn
        if d*d*vd <= 4*vn*md*md: return 0
        return -1 if d < 0 else 1
    start, end = 0, n + 1
    while start < end:
        mid = (start + end) // 2
        if rel(mid) < 0: start = mid + 1
        else: end = mid
    low = start
    start, end = 0, n + 1
    while start < end:
        mid = (start + end) // 2
        if rel(mid) <= 0: start = mid + 1
        else: end = mid
    high = start - 1
    first = start if start <= n else None
    return (mu, sd, lo, hi, low, high, first)
def binomial_quartiles(n, p):
    a, den = p
    if a == 0: return 0, 0
    if a == den: return n, n
    b = den - a
    total = den**n
    term = b**n
    cumulative = 0
    q1 = None
    for k in range(n + 1):
        cumulative += term
        if q1 is None and 4*cumulative >= total: q1 = k
        if 4*cumulative >= 3*total: return q1, k
        if k < n: term = term*(n-k)*a//((k+1)*b)
def page(n, p, event, answer, threshold, cache, target):
    if target <= 2:
        return c.call('STBINFO5', 'page', n, p, event, answer, threshold, cache, target)
    return c.call('STBINFO7', 'page', n, p, event, answer, threshold, cache, target)
