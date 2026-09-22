# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Missing-probability and sampling-table entry helpers.
import STCORE as c


def missing_probability():
    c.heading('R05 MISSING PROBABILITY')
    known = []
    for i in range(c.read_size('HOW MANY KNOWN P? ', c.MAX_ROWS)):
        known.append(c.read_exact('KNOWN P: '))
    total = c.rsum(known)
    missing = c.radd((1, 1), (-total[0], total[1]))
    c.results('R05', [('MISSING P', missing)], ['P=1-SUM(KNOWN P)', 'KNOWN SUM=' + c.exact_text(total), 'ONE UNKNOWN CAN BE FOUND', 'X LABELS NOT NEEDED'])


def read_sample_distribution():
    total=c.read_int('TOTAL OBJECTS N: ')
    targets=c.read_int('TARGET OBJECTS K: ')
    draws=c.read_int('NUMBER SELECTED n: ')
    return c.call('STCOUNT', 'hyper_distribution', total, targets, draws)


def rounded_distribution_session():
    rows,approximate=c.call('STCOUNT', 'read_distribution', True)
    c.call('STCOUNT', 'distribution_session', rows, approximate)
