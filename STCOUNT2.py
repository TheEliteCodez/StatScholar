# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Distribution-table math: moments, event totals, entry, unusual result.
import STCORE as c
import math


def table_probability(rows, event):
    return c.rsum([p for x, p in rows if c.event_match(x, *event)])


def distribution_moments(rows):
    mean = c.rsum([c.rmul(x, p) for x, p in rows])
    second = c.rsum([c.rmul(c.rmul(x, x), p) for x, p in rows])
    square = c.rmul(mean, mean)
    var = c.radd(second, (-square[0], square[1]))
    return (mean, var, math.sqrt(max(0, c.number(var))))


def read_distribution(approximate=False):
    print("ENTER x BY LABEL, EVEN IF x IS THE SECOND COLUMN")
    rows = []
    missing = []
    c.heading('X / P(X): MATCH COLUMNS')
    print('X=VALUE; P=PROBABILITY')
    print('0+ OR ~.123 ROUNDED; ? MISSING')
    for i in range(c.read_size('NUMBER OF ROWS: ', c.MAX_ROWS)):
        print('ROW ' + str(i + 1))
        x = c.read_exact('X VALUE: ')
        raw = input('P(X), 0+, OR ?: ').strip()
        if raw == '?':
            missing.append(i)
            p = (0, 1)
        elif raw == '0+':
            approximate = True
            p = (0, 1)
        else:
            if raw.startswith('~'):
                approximate=True
                raw=raw[1:]
            p = c.as_ratio(raw)
        rows.append((x, p))
    if missing:
        if len(missing) > 1 or approximate:
            raise ValueError('MISSING P NEEDS ALL OTHER P')
        total = c.rsum([p for x, p in rows])
        i = missing[0]
        rows[i] = (rows[i][0], c.radd((1, 1), (-total[0], total[1])))
        c.results('R05 COMPLETED TABLE', [('MISSING P', rows[i][1])], ['1-SUM(KNOWN P)'])
    return (rows, approximate)


def unusual_result(prob):
    raw = input('UNUSUAL CUTOFF (ENTER=.05): ').strip()
    threshold = c.as_ratio(raw or '.05')
    c.results('R06 UNUSUAL EVENT', [('P(EVENT)', prob), ('UNUSUAL', 'YES' if c.compare_exact(prob, threshold) <= 0 else 'NO')], ['UNUSUAL IF P<=CUTOFF', 'CUTOFF=' + c.exact_text(threshold), 'USE LOWER TAIL FOR FEW', 'UPPER TAIL FOR MANY', 'EVIDENCE UNDER THE MODEL', 'NOT PROOF OF A CAUSE'])
