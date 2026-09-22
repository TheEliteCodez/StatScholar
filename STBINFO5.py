# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Model pages (MEAN/SD and USUAL COUNTS) for the binomial follow-up.
import STCORE as c
from STBINFO9 import ratio, radd, rmul, fixed


def model_of(n, p, cache):
    if 'model' not in cache:
        mean = rmul((n, 1), p)
        variance = rmul(mean, radd((1, 1), (-p[0], p[1])))
        cache['model'] = (mean, variance, c.call('STBINFO2', 'usual_counts', n, p))
    return cache['model']


def page(n, p, event, answer, threshold, cache, target):
    mean, variance, model = model_of(n, p, cache)
    mu, sd, lo, hi, low, high, first = model
    if target == 0:
        return ['MEAN / SD / USUAL','MEAN='+fixed(mean,4),'SD='+fixed(sd,4),
            'VARIANCE='+fixed(variance,4),'MIN USUAL='+fixed(lo,4),'MAX USUAL='+fixed(hi,4),'USUAL=MEAN +/- 2SD']
    return ['USUAL COUNTS','MIN COUNT='+str(low),'MAX COUNT='+str(high),
        'UNUSUALLY LOW='+str(low-1 if low > 0 else 'NONE'),'UNUSUALLY HIGH='+str(first if first is not None else 'NONE'),
        'BOUNDARIES USUAL','COUNTS 0 TO '+str(n)]
