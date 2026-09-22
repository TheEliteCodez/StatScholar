# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Small descriptive solvers: proportion, range/IQR, usual, z, outlier.
import STCORE

def solver_rel_freq():
    f = STCORE.read_int('FREQUENCY f: ')
    n = STCORE.read_int('TOTAL n: ')
    STCORE.results('F04 PROPORTION', [('f/n', STCORE.ratio(f, n))], [str(f) + '/' + str(n)])

def solver_range_iqr():
    c = STCORE.menu('RANGE / IQR', [('1', 'RANGE'), ('2', 'IQR'), ('3', 'BOTH')])
    if c == '0':
        return
    answers = []
    work = []
    if c in ('1', '3'):
        mx = STCORE.read_exact('MAX: ')
        mn = STCORE.read_exact('MIN: ')
        answers.append(('RANGE', STCORE.radd(mx, (-mn[0], mn[1]))))
        work.append(STCORE.exact_text(mx) + '-' + STCORE.exact_text(mn))
    if c in ('2', '3'):
        q3 = STCORE.read_exact('Q3: ')
        q1 = STCORE.read_exact('Q1: ')
        answers.append(('IQR', STCORE.radd(q3, (-q1[0], q1[1]))))
        work.append(STCORE.exact_text(q3) + '-' + STCORE.exact_text(q1))
    STCORE.results('S04/S08', answers, work)

def solver_usual():
    mean = STCORE.read_exact('MEAN: ')
    sd = STCORE.read_exact('SD: ')
    twosd = STCORE.rmul((2, 1), sd)
    low = STCORE.radd(mean, (-twosd[0], twosd[1]))
    high = STCORE.radd(mean, twosd)
    STCORE.results('RANGE RULE OF THUMB', [('MIN USUAL', low), ('MAX USUAL', high)], [STCORE.exact_text(mean) + ' +/- 2*' + STCORE.exact_text(sd)])
    print('IS A NUMBER UNUSUAL?')
    observed = input('NUMBER (ENTER=SKIP): ').strip()
    if observed:
        value = STCORE.as_ratio(observed)
        below = STCORE.compare_exact(value, low) < 0
        above = STCORE.compare_exact(value, high) > 0
        label = 'UNUSUALLY LOW' if below else 'UNUSUALLY HIGH' if above else 'NOT UNUSUAL'
        STCORE.results('CHECK NUMBER', [('NUMBER', value), ('UNUSUAL', 'YES' if below or above else 'NO'), ('CLASSIFICATION', label)], ['USUAL INCLUDES BOTH LIMITS', 'MIN USUAL=' + STCORE.exact_text(low), 'MAX USUAL=' + STCORE.exact_text(high)])

def solver_zscore():
    x = STCORE.read_exact('x: ')
    mean = STCORE.read_exact('MEAN: ')
    sd = STCORE.read_exact('SD: ')
    z = STCORE.rdiv(STCORE.radd(x, (-mean[0], mean[1])), sd)
    label = 'HIGH' if STCORE.compare_exact(z, 2) > 0 else 'LOW' if STCORE.compare_exact(z, -2) < 0 else 'NOT EXTREME'
    STCORE.results('S12 Z-SCORE', [('z', z), ('CLASSIFICATION', label)], ['(' + STCORE.exact_text(x) + '-' + STCORE.exact_text(mean) + ')/' + STCORE.exact_text(sd)])

def solver_outlier():
    q1 = STCORE.read_exact('Q1: ')
    q3 = STCORE.read_exact('Q3: ')
    iqr = STCORE.radd(q3, (-q1[0], q1[1]))
    distance = STCORE.rmul(iqr, (3, 2))
    STCORE.results('G03 OUTLIER FENCES', [('IQR', iqr), ('LOWER FENCE', STCORE.radd(q1, (-distance[0], distance[1]))), ('UPPER FENCE', STCORE.radd(q3, distance))], ['Q1-1.5*IQR; Q3+1.5*IQR'])
    while True:
        raw=input('CHECK VALUE (ENTER=DONE): ').strip()
        if not raw: return
        x=STCORE.as_ratio(raw)
        low=STCORE.radd(q1,(-distance[0],distance[1]));high=STCORE.radd(q3,distance)
        STCORE.results('IQR OUTLIER CHECK',[('x',x),('OUTLIER','YES' if STCORE.compare_exact(x,low)<0 or STCORE.compare_exact(x,high)>0 else 'NO')],['VALUES ON FENCES ARE NOT OUTLIERS'])
