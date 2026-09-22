# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Two-way table solver; row/column entry reads back through the dispatcher.
import STCORE as c


def two_way_values(cells, r, c):
    total = sum((sum(row) for row in cells))
    a = sum(cells[r])
    b = sum((row[c] for row in cells))
    both = cells[r][c]
    return (total, a, b, both)


def two_way_session():
    rl,cl,cells = c.call('STPROB', 'read_two_way')
    while True:
        print('SELECT ROW AND COLUMN')
        r = c.menu('ROW / C DATA / S SELECT MANY', [(str(i + 1), x) for i, x in enumerate(rl)], ('C','S'))
        if r == '0':
            return
        if r == 'S':
            groups=[(name,sum(cells[i])) for i,name in enumerate(rl)]+[(name,sum(row[i] for row in cells)) for i,name in enumerate(cl)]
            group=c.menu('TARGET ROW OR COLUMN',[(str(i+1),('ROW ' if i<len(rl) else 'COLUMN ')+name) for i,(name,count) in enumerate(groups)])
            if group!='0': c.call('STVENN','selection_session',sum(sum(row) for row in cells),groups[int(group)-1][1])
            continue
        if r == 'C':
            rl,cl,cells = c.call('STPROB', 'read_two_way')
            continue
        cc = c.menu('COLUMN', [(str(i + 1), x) for i, x in enumerate(cl)])
        if cc == '0':
            continue
        total, a, b, both = two_way_values(cells, int(r) - 1, int(cc) - 1)
        answers = [('P(ROW)', c.ratio(a, total)), ('P(COLUMN)', c.ratio(b, total)), ('P(BOTH)', c.ratio(both, total)), ('P(OR)', c.ratio(a + b - both, total)), ('P(NOT ROW)', c.ratio(total - a, total)), ('P(NOT COLUMN)', c.ratio(total - b, total))]
        answers += [('ROW GIVEN COLUMN', c.ratio(both, b) if b else 'UNDEFINED'), ('COLUMN GIVEN ROW', c.ratio(both, a) if a else 'UNDEFINED')]
        answers += [('INDEPENDENT', 'YES' if both*total==a*b else 'NO'), ('TWO COLUMN REPLACED', c.ratio(b*b,total*total)), ('TWO COLUMN NOT REPLACED', c.ratio(b*(b-1),total*(total-1)) if total>1 else 'UNDEFINED'), ('TWO ROW REPLACED', c.ratio(a*a,total*total)), ('TWO ROW NOT REPLACED', c.ratio(a*(a-1),total*(total-1)) if total>1 else 'UNDEFINED')]
        c.results('P14/P12/P07', answers, ['TOTAL=' + str(total), 'ROW '+rl[int(r)-1]+'=' + str(a), 'COLUMN '+cl[int(cc)-1]+'=' + str(b), 'BOTH=' + str(both), 'GIVEN: DIVIDE BY GIVEN', 'OTHERS: DIVIDE BY TOTAL'])


def read_two_way():
    c.heading('P14 TWO-WAY COUNTS')
    nr = c.read_size('ROW COUNT (NO TOTAL): ', 10)
    nc = c.read_size('COLUMN COUNT (NO TOTAL): ', 10)
    rl = [input('ROW NAME: ') for i in range(nr)]
    cl = [input('COLUMN NAME: ') for i in range(nc)]
    cells = []
    for r in range(nr):
        row = []
        for cc in range(nc):
            row.append(c.read_int(rl[r] + ' / ' + cl[cc] + ': '))
        cells.append(row)
    return rl,cl,cells
