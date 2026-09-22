# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Category counts, supplied probabilities, and validity check.
import STCORE as c


def supplied_session():
    c.heading('P04/P07/P10/P11')
    print('ENTER DECIMAL, FRACTION, %')
    a = c.read_exact('P(A): ')
    b = c.read_exact('P(B): ')
    both = c.read_exact('P(BOTH): ')
    union = c.radd(c.radd(a, b), (-both[0], both[1]))
    product = c.rmul(a, b)
    c.results('SUPPLIED PROBABILITIES', [('P(A)', a), ('P(B)', b), ('P(BOTH)', both), ('P(NOT A)', c.radd((1,1),(-a[0],a[1]))), ('P(NOT B)', c.radd((1,1),(-b[0],b[1]))), ('P(OR)', union), ('A GIVEN B', c.rdiv(both, b) if b[0] else 'UNDEFINED'), ('B GIVEN A', c.rdiv(both, a) if a[0] else 'UNDEFINED'), ('MUTUALLY EXCLUSIVE', 'YES' if both[0] == 0 else 'NO'), ('INDEPENDENT', 'YES' if both == product else 'NO')], ['OR=A+B-BOTH', 'GIVEN=BOTH/GIVEN GROUP', 'EXCLUSIVE: BOTH=0', 'INDEPENDENT: BOTH=A*B', 'A*B=' + c.exact_text(product), 'USE GIVEN BOTH DIRECTLY'])


def valid_probability():
    p = c.read_exact('PROBABILITY VALUE: ')
    c.results('P13', [('CLASSIFICATION', probability_class(p)), ('CAN BE PROBABILITY', 'YES' if c.compare_exact(p, 0) >= 0 and c.compare_exact(p, 1) <= 0 else 'NO')], ['0<=P<=1; ENDPOINTS VALID', 'NOT A WHOLE TABLE TEST'])


def probability_class(p):
    if c.compare_exact(p,0)<0 or c.compare_exact(p,1)>0: return "INVALID"
    if c.compare_exact(p,0)==0: return "IMPOSSIBLE"
    if c.compare_exact(p,1)==0: return "CERTAIN"
    return "POSSIBLE"
