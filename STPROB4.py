# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Category-count proportion solver.
import STCORE as c


def category_session():
    labels = []
    counts = []
    c.heading('F02 CATEGORY COUNTS')
    for i in range(c.read_size('NUMBER OF CATEGORIES: ', c.MAX_OUTCOMES)):
        labels.append(input('CATEGORY NAME: '))
        counts.append(c.read_int('COUNT: '))
    total = sum(counts)
    selected = None
    while True:
        key = c.menu('SELECT CATEGORY', [(str(i + 1), x) for i, x in enumerate(labels)] + [('E', 'COMPARE EXPECTED P'),('C','EDIT CATEGORY COUNT'),('T','SHOW ALL PROPORTIONS')])
        if key == '0':
            return
        if key=='T':
            c.paged_results('CATEGORY PROPORTIONS',len(labels),lambda i:(labels[i],c.ratio(counts[i],total)));continue
        if key=='C':
            i=c.read_size('CATEGORY NUMBER: ',len(labels))-1
            labels[i]=input('CATEGORY NAME: ');counts[i]=c.read_int('COUNT: ');total=sum(counts);continue
        if key == 'E':
            if selected is None:
                c.view('SELECT CATEGORY FIRST', ['CHOOSE THE CATEGORY TO COMPARE'])
                continue
            target = c.read_exact('EXPECTED PROBABILITY: ')
            estimate = c.ratio(counts[selected], total)
            delta = c.radd(estimate, (-target[0], target[1]))
            c.results('F02 COMPARE', [('ESTIMATED P', estimate), ('EXPECTED P', target), ('DIFFERENCE (PERCENT POINTS)', c.rmul(delta, (100, 1)))], ['ESTIMATE=COUNT/TOTAL', 'USE CLASS RULE FOR CLOSE'])
            continue
        i = int(key) - 1
        selected = i
        c.results('F02 / P01 / P02', [('P(' + labels[i] + ')', c.ratio(counts[i], total)), ('P(NOT)', c.ratio(total - counts[i], total))], ['CATEGORY COUNT / TOTAL', str(counts[i]) + '/' + str(total), 'LONG-RUN PROPORTION', 'ESTIMATES PROBABILITY'])
