# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Data input, quartiles, descriptive summary, value counts.
import STCORE as c

RAW_LIMIT = 100


def sub(a, b):
    return c.radd(a, (-b[0], b[1]))


def read_raw(title='DATA > RAW'):
    c.heading(title)
    n = c.read_size('NUMBER OF VALUES (1..100): ', RAW_LIMIT)
    values = [c.read_exact('VALUE '+str(i+1)+': ') for i in range(n)]
    for i in range(1, n):
        x, j = values[i], i
        while j and c.compare_exact(values[j-1], x) > 0:
            values[j] = values[j-1]
            j -= 1
        values[j] = x
    return values


def median_span(values, start, end):
    length = end-start
    if not length: return None
    mid = start+length//2
    return values[mid] if length%2 else c.rdiv(c.radd(values[mid-1], values[mid]), (2,1))


def quartiles(values):
    n = len(values)
    return (median_span(values, 0, n//2), median_span(values, 0, n),
            median_span(values, (n+1)//2, n))


def descriptive(values):
    return c.call('STDMATH2', 'weighted_stats', value_counts(values))


def value_counts(values):
    counts={}
    for x in values: counts[x]=counts.get(x,0)+1
    return [(x,counts[x]) for x in c.exact_sorted(counts)]


def min_exact(a,b): return a if c.compare_exact(a,b)<=0 else b

def max_exact(a,b): return a if c.compare_exact(a,b)>=0 else b
