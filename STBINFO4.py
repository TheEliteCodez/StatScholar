# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Self-contained binomial stats (usual counts and quartiles), loaded only while computing.
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
    # Discrete quantile: smallest k with CDF(k) >= .25 or .75.
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
