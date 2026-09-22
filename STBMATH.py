# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STBMATH - loaded on demand.
import STCORE
import math
import STEXACT
from STCOMB import ncr

def binomial_exact_ratio(n, p, k):
    if k < 0 or k > n:
        return (0, 1)
    return STCORE.ratio(ncr(n, k) * p[0] ** k * (p[1] - p[0]) ** (n - k), p[1] ** n)

def binomial_exact_event(n, p, event):
    # Scalar recurrence: no probability list and no repeated combination builds.
    a,den=p
    b=den-a
    if a==0: return (1,1) if STCORE.event_match(0,*event) else (0,1)
    if b==0: return (1,1) if STCORE.event_match(n,*event) else (0,1)
    if event[0]=='=':
        value=STCORE.to_ratio(event[1])
        if value[0]%value[1]: return (0,1)
        return binomial_exact_ratio(n,p,value[0]//value[1])
    term=b**n
    numerator=0
    for k in range(n+1):
        if STCORE.event_match(k,*event): numerator+=term
        if k<n: term=term*(n-k)*a//((k+1)*b)
    return STCORE.ratio(numerator,den**n)


def usual_counts(n, p):
    exact_p = STCORE.to_ratio(p)
    mean = STCORE.rmul((n, 1), exact_p)
    variance = STCORE.rmul(mean, STCORE.radd((1, 1), (-exact_p[0], exact_p[1])))
    mu = STCORE.number(mean)
    sd = math.sqrt(STCORE.number(variance))
    lo = mu - 2 * sd
    hi = mu + 2 * sd
    start, end = (0, n + 1)
    while start < end:
        mid = (start + end) // 2
        if STCORE.range_relation(mid, mean, variance) < 0:
            start = mid + 1
        else:
            end = mid
    low = start
    start, end = (0, n + 1)
    while start < end:
        mid = (start + end) // 2
        if STCORE.range_relation(mid, mean, variance) <= 0:
            start = mid + 1
        else:
            end = mid
    high = start - 1
    first = start if start <= n else None
    return (mu, sd, lo, hi, low, high, first)

def binomial_shape(p):
    if STCORE.compare_exact(p, 0) == 0 or STCORE.compare_exact(p, 1) == 0:
        return 'ONE POINT'
    if STCORE.compare_exact(p, (1, 2)) == 0:
        return 'SYMMETRIC'
    return 'RIGHT SKEW' if STCORE.compare_exact(p, (1, 2)) < 0 else 'LEFT SKEW'
