# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Observation (z-score) and requested-event pages for the binomial follow-up.
import STCORE as c
from STBINFO9 import ratio, radd, rmul, to_ratio, compare_exact, number, range_relation, fixed, exact_text


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
    mean, variance, model = model_of(n, p, cache)
    mu, sd, lo, hi, low, high, first = model
    observations = [] if event is None else ([('LOWER CUTOFF', event[1]), ('UPPER CUTOFF', event[2])] if event[0] in ('[]','()','[)','(]') else [('CUTOFF', event[1])])
    if target - 3 < len(observations):
        label, x = observations[target - 3]
        lower, upper = fences_of(n, p, cache)
        delta = radd(to_ratio(x), (-mean[0], mean[1]))
        z = fixed(number(delta)/sd, 4) if sd else 'DNE (SD=0)'
        relation = range_relation(x, mean, variance)
        position = 'UNUSUALLY LOW' if relation < 0 else 'UNUSUALLY HIGH' if relation > 0 else 'NOT UNUSUAL'
        outlier = compare_exact(x, lower) < 0 or compare_exact(x, upper) > 0
        return [label+'='+exact_text(x),'z='+z,'2 SD: '+position,'OUTLIER='+('YES' if outlier else 'NO'),
            'z=(X-MEAN)/SD','2 SD UNROUNDED','IQR: Q1/Q3 +/-1.5IQR']
    if answer is not None and target - 3 == len(observations):
        return ['REQUESTED EVENT','P(EVENT)='+fixed(answer,4),'PROBABILITY CUTOFF='+exact_text(threshold),
            'EVENT UNUSUAL='+('YES' if compare_exact(answer, threshold) <= 0 else 'NO'),'EVENT P VS 2SD',
            'POINT P NOT A TAIL','NEXT: SAME n,p']
    return None
