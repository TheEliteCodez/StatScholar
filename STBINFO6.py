# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# IQR fences page for the binomial follow-up.
import STCORE as c
from STBINFO9 import ratio, exact_text


def fences_of(n, p, cache):
    if 'quartiles' not in cache: cache['quartiles'] = c.call('STBINFO2', 'binomial_quartiles', n, p)
    q1, q3 = cache['quartiles']
    iqr = q3 - q1
    return ratio(2*q1-3*iqr, 2), ratio(2*q3+3*iqr, 2)


def page(n, p, event, answer, threshold, cache, target):
    lower, upper = fences_of(n, p, cache)
    q1, q3 = cache['quartiles']; iqr = q3 - q1
    return ['IQR FENCES','Q1='+str(q1),'Q3='+str(q3),'IQR='+str(iqr),
        'LOWER FENCE='+exact_text(lower),'UPPER FENCE='+exact_text(upper),'CDF QUARTILES']
