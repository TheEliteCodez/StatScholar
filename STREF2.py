# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Guide browsing and TI-84 methods; context globals live on STREF.
import STCORE
import STREF


def browse_matrix():
    groups = [('D', 'DATA'), ('F', 'FREQUENCY'), ('S', 'DESCRIPTIVE'), ('G', 'GRAPHS'), ('P', 'PROBABILITY'), ('C', 'COUNTING'), ('R', 'RANDOM VARIABLE'), ('B', 'BINOMIAL')]
    while True:
        key = STCORE.menu('GUIDE GROUP', [(a, b) for a, b in groups])
        if key == '0':
            return
        browse_ids(key, sorted([gid for gid in STREF.GUIDES if gid.startswith(key)]))


def browse_ids(title, ids):
    page = 0
    per_page = 7
    while True:
        STCORE.heading(title)
        start = page * per_page
        end = min(start + per_page, len(ids))
        i = start
        n = 1
        while i < end:
            qid = ids[i]
            print(str(n) + ' ' + qid + ' ' + STREF.GUIDES[qid][0][:16])
            i += 1
            n += 1
        if end < len(ids):
            print('N NEXT')
        if page > 0:
            print('P PREV')
        print('0 BACK')
        c = input('> ').upper()
        if c == '0':
            return
        elif c == 'N' and end < len(ids):
            page += 1
        elif c == 'P' and page > 0:
            page -= 1
        else:
            try:
                idx = int(c)
                real = start + idx - 1
                if idx >= 1 and idx <= per_page and (real < len(ids)):
                    STREF.show_identified(ids[real])
            except:
                pass


def ti84_methods():
    while True:
        STCORE.heading('TI-84 EVO METHODS')
        print('1 1-VAR STATS')
        print('2 BOXPLOT')
        print('3 HISTOGRAM')
        print('4 nCr / nPr')
        print('5 BINOM PDF/CDF')
        print('6 EXPECTED VALUE')
        print('0 BACK')
        c = input('> ')
        if c == '1':
            STCORE.view('1-VAR STATS', ['STAT > EDIT.', 'ENTER DATA IN L1.', '', 'STAT > CALC.', '1-VAR STATS.', 'LIST=L1.', '', 'READ:', 'xbar MEAN', 'Sx SAMPLE SD', 'n SAMPLE SIZE', 'minX,Q1,Med,Q3,maxX.'])
        elif c == '2':
            STCORE.view('BOXPLOT', ['ENTER DATA IN L1.', 'STAT PLOT / PLOT1 ON.', 'CHOOSE BOX PLOT.', 'Xlist=L1.', 'Freq=1.', 'ZOOM > ZoomStat.'])
        elif c == '3':
            STCORE.view('HISTOGRAM', ['ENTER DATA IN L1.', 'STAT PLOT / PLOT1 ON.', 'CHOOSE HISTOGRAM.', 'Xlist=L1.', 'Freq=1.', 'ZOOM > ZoomStat.'])
        elif c == '4':
            STCORE.view('nCr / nPr', ['TYPE n.', 'MATH > PRB.', '', 'nCr IF ORDER', 'DOES NOT MATTER.', '', 'nPr IF ORDER MATTERS.', '', 'TYPE r, ENTER.'])
        elif c == '5':
            STCORE.view('BINOMIAL', ['EXACTLY x:', 'binompdf(n,p,x)', '', 'AT MOST x:', 'binomcdf(n,p,x)', '', 'LESS THAN x:', 'binomcdf(n,p,x-1)', '', 'AT LEAST x:', '1-binomcdf(n,p,x-1)', '', 'MORE THAN x:', '1-binomcdf(n,p,x)'])
        elif c == '6':
            STCORE.view('EXPECTED VALUE', ['L1=x VALUES.', 'L2=P(x).', '', '1-VAR STATS.', 'LIST=L1.', 'FREQ=L2.', '', 'xbar = E(X).'])
        elif c == '0':
            return
