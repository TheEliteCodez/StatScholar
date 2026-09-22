# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Binomial wording -> bounds/command translation, loaded only while an event is shown.
import STCORE as c
from STBWORD import WORDS


def floor_ratio(x):
    a, b = c.to_ratio(x)
    return a // b


def ceil_ratio(x):
    a, b = c.to_ratio(x)
    return -(-a // b)


def event_bounds(n, event):
    op, a, b = event
    if op == '=':
        k = floor_ratio(a)
        return (k, k) if c.compare_exact(a, k) == 0 else (1, 0)
    if op == '<=': return 0, floor_ratio(a)
    if op == '<': return 0, ceil_ratio(a) - 1
    if op == '>=': return ceil_ratio(a), n
    if op == '>': return floor_ratio(a) + 1, n
    return (ceil_ratio(a) if op[0] == '[' else floor_ratio(a) + 1,
            floor_ratio(b) if op[-1] == ']' else ceil_ratio(b) - 1)


def translation(n, p, event):
    op, a, b = event
    text = c.exact_text(a)
    words = WORDS[op] + ' ' + text
    if op in ('[]', '()', '[)', '(]'): words += ' TO ' + c.exact_text(b)
    low, high = event_bounds(n, event)
    def cdf(k):
        if k < 0: return '0'
        if k >= n: return '1'
        return 'binomcdf(' + str(n) + ',' + c.exact_text(p) + ',' + str(k) + ')'
    if op == '=':
        command = 'binompdf(' + str(n) + ',' + c.exact_text(p) + ',' + text + ')' if low <= high and 0 <= low <= n else '0'
        why = 'PDF COUNTS ONE EXACT VALUE; CDF ADDS A LOWER TAIL.'
    elif op in ('<', '<='):
        command = cdf(high)
        why = 'KEEP 0 THROUGH ' + str(min(n, high)) + '. ' + ('CUTOFF INCLUDED.' if op == '<=' else 'CUTOFF EXCLUDED: USE THE INTEGER BELOW IT.')
    elif op in ('>', '>='):
        command = '1-' + cdf(low - 1)
        why = 'KEEP ' + str(max(0, low)) + ' THROUGH ' + str(n) + '. REMOVE 0 THROUGH ' + str(low - 1) + '. AT LEAST INCLUDES THE CUTOFF; MORE THAN EXCLUDES IT.'
    else:
        command = cdf(high) + ' - ' + cdf(low - 1)
        why = 'KEEP INTEGERS ' + str(low) + ' THROUGH ' + str(high) + '. SUBTRACT THE TAIL BELOW THE LOWER INCLUDED VALUE.'
    if low > high: command = '0'
    math_text = 'P(X ' + op + ' ' + text + ')' if len(op) == 1 or op in ('<=', '>=') else 'P(' + str(low) + ' <= X <= ' + str(high) + ')'
    return words, math_text, command, why
