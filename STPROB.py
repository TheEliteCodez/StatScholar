# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STPROB - solver code; references load separately.
import STCORE

def solver_basic_prob():
    a = STCORE.read_int('FAVORABLE: ')
    b = STCORE.read_int('TOTAL: ')
    STCORE.results('P01 BASIC PROBABILITY', [('P', STCORE.ratio(a, b))], ['P=FAVORABLE/TOTAL', str(a) + '/' + str(b)])

def solver_complement():
    p = STCORE.read_exact('P(E): ')
    STCORE.results('P02 COMPLEMENT', [('P(NOT E)', STCORE.radd((1, 1), (-p[0], p[1])))], ['1-' + STCORE.exact_text(p)])

def solver_general_or():
    a = STCORE.read_exact('P(A): ')
    b = STCORE.read_exact('P(B): ')
    both = STCORE.read_exact('P(BOTH): ')
    STCORE.results('P04 OR', [('P(OR)', STCORE.radd(STCORE.radd(a, b), (-both[0], both[1])))], [STCORE.exact_text(a) + '+' + STCORE.exact_text(b) + '-' + STCORE.exact_text(both)])

def solver_mut_or():
    a = STCORE.read_exact('P(A): ')
    b = STCORE.read_exact('P(B): ')
    STCORE.results('P03 EXCLUSIVE OR', [('P(OR)', STCORE.radd(a, b))], ['MUTUALLY EXCLUSIVE: BOTH=0', STCORE.exact_text(a) + '+' + STCORE.exact_text(b)])

def solver_indep_and():
    a = STCORE.read_exact('P(A): ')
    b = STCORE.read_exact('P(B): ')
    STCORE.results('P05 INDEPENDENT AND', [('P(BOTH)', STCORE.rmul(a, b))], ['INDEPENDENT EVENTS', STCORE.exact_text(a) + '*' + STCORE.exact_text(b)])

def solver_general_and():
    a = STCORE.read_exact('P(A): ')
    bg = STCORE.read_exact('P(B GIVEN A): ')
    STCORE.results('P06 GENERAL AND', [('P(BOTH)', STCORE.rmul(a, bg))], ['P(A)*P(B GIVEN A)', STCORE.exact_text(a) + '*' + STCORE.exact_text(bg)])

def solver_conditional():
    c = STCORE.menu('P07 CONDITIONAL', [('1', 'PROBABILITIES'), ('2', 'COUNTS FROM TABLE')])
    if c == '0':
        return
    both = STCORE.read_exact('BOTH A AND B: ')
    given = STCORE.read_exact('GIVEN GROUP B TOTAL: ')
    STCORE.results('P07 GIVEN', [('P(A GIVEN B)', STCORE.rdiv(both, given))], ['BOTH / GIVEN GROUP', STCORE.exact_text(both) + ' / ' + STCORE.exact_text(given)])

def solver_at_least_one():
    p = STCORE.read_exact('SUCCESS p: ')
    n = STCORE.read_int('TRIALS n: ')
    ans = STCORE.ratio(p[1] ** n - (p[1] - p[0]) ** n, p[1] ** n)
    STCORE.results('P09 AT LEAST ONE', [('P', ans)], ['1-(1-' + STCORE.exact_text(p) + ')^' + str(n)])

def category_session():
    labels = []
    counts = []
    STCORE.heading('F02 CATEGORY COUNTS')
    for i in range(STCORE.read_size('NUMBER OF CATEGORIES: ', STCORE.MAX_OUTCOMES)):
        labels.append(input('CATEGORY NAME: '))
        counts.append(STCORE.read_int('COUNT: '))
    total = sum(counts)
    selected = None
    while True:
        key = STCORE.menu('SELECT CATEGORY', [(str(i + 1), x) for i, x in enumerate(labels)] + [('E', 'COMPARE EXPECTED P'),('C','EDIT CATEGORY COUNT'),('T','SHOW ALL PROPORTIONS')])
        if key == '0':
            return
        if key=='T':
            STCORE.paged_results('CATEGORY PROPORTIONS',len(labels),lambda i:(labels[i],STCORE.ratio(counts[i],total)));continue
        if key=='C':
            i=STCORE.read_size('CATEGORY NUMBER: ',len(labels))-1
            labels[i]=input('CATEGORY NAME: ');counts[i]=STCORE.read_int('COUNT: ');total=sum(counts);continue
        if key == 'E':
            if selected is None:
                STCORE.view('SELECT CATEGORY FIRST', ['CHOOSE THE CATEGORY TO COMPARE'])
                continue
            target = STCORE.read_exact('EXPECTED PROBABILITY: ')
            estimate = STCORE.ratio(counts[selected], total)
            delta = STCORE.radd(estimate, (-target[0], target[1]))
            STCORE.results('F02 COMPARE', [('ESTIMATED P', estimate), ('EXPECTED P', target), ('DIFFERENCE (PERCENT POINTS)', STCORE.rmul(delta, (100, 1)))], ['ESTIMATE=COUNT/TOTAL', 'USE CLASS RULE FOR CLOSE'])
            continue
        i = int(key) - 1
        selected = i
        STCORE.results('F02 / P01 / P02', [('P(' + labels[i] + ')', STCORE.ratio(counts[i], total)), ('P(NOT)', STCORE.ratio(total - counts[i], total))], ['CATEGORY COUNT / TOTAL', str(counts[i]) + '/' + str(total), 'LONG-RUN PROPORTION', 'ESTIMATES PROBABILITY'])

def two_way_values(cells, r, c):
    total = sum((sum(row) for row in cells))
    a = sum(cells[r])
    b = sum((row[c] for row in cells))
    both = cells[r][c]
    return (total, a, b, both)

def two_way_session():
    rl,cl,cells=read_two_way()
    while True:
        print('SELECT ROW AND COLUMN')
        r = STCORE.menu('ROW / C DATA / S SELECT MANY', [(str(i + 1), x) for i, x in enumerate(rl)], ('C','S'))
        if r == '0':
            return
        if r == 'S':
            groups=[(name,sum(cells[i])) for i,name in enumerate(rl)]+[(name,sum(row[i] for row in cells)) for i,name in enumerate(cl)]
            group=STCORE.menu('TARGET ROW OR COLUMN',[(str(i+1),('ROW ' if i<len(rl) else 'COLUMN ')+name) for i,(name,count) in enumerate(groups)])
            if group!='0': STCORE.call('STVENN','selection_session',sum(sum(row) for row in cells),groups[int(group)-1][1])
            continue
        if r == 'C':
            rl,cl,cells=read_two_way()
            continue
        c = STCORE.menu('COLUMN', [(str(i + 1), x) for i, x in enumerate(cl)])
        if c == '0':
            continue
        total, a, b, both = two_way_values(cells, int(r) - 1, int(c) - 1)
        answers = [('P(ROW)', STCORE.ratio(a, total)), ('P(COLUMN)', STCORE.ratio(b, total)), ('P(BOTH)', STCORE.ratio(both, total)), ('P(OR)', STCORE.ratio(a + b - both, total)), ('P(NOT ROW)', STCORE.ratio(total - a, total)), ('P(NOT COLUMN)', STCORE.ratio(total - b, total))]
        answers += [('ROW GIVEN COLUMN', STCORE.ratio(both, b) if b else 'UNDEFINED'), ('COLUMN GIVEN ROW', STCORE.ratio(both, a) if a else 'UNDEFINED')]
        answers += [('INDEPENDENT', 'YES' if both*total==a*b else 'NO'), ('TWO COLUMN REPLACED', STCORE.ratio(b*b,total*total)), ('TWO COLUMN NOT REPLACED', STCORE.ratio(b*(b-1),total*(total-1)) if total>1 else 'UNDEFINED'), ('TWO ROW REPLACED', STCORE.ratio(a*a,total*total)), ('TWO ROW NOT REPLACED', STCORE.ratio(a*(a-1),total*(total-1)) if total>1 else 'UNDEFINED')]
        STCORE.results('P14/P12/P07', answers, ['TOTAL=' + str(total), 'ROW '+rl[int(r)-1]+'=' + str(a), 'COLUMN '+cl[int(c)-1]+'=' + str(b), 'BOTH=' + str(both), 'GIVEN: DIVIDE BY GIVEN', 'OTHERS: DIVIDE BY TOTAL'])

def supplied_session():
    STCORE.heading('P04/P07/P10/P11')
    print('ENTER DECIMAL, FRACTION, %')
    a = STCORE.read_exact('P(A): ')
    b = STCORE.read_exact('P(B): ')
    both = STCORE.read_exact('P(BOTH): ')
    union = STCORE.radd(STCORE.radd(a, b), (-both[0], both[1]))
    product = STCORE.rmul(a, b)
    STCORE.results('SUPPLIED PROBABILITIES', [('P(A)', a), ('P(B)', b), ('P(BOTH)', both), ('P(NOT A)', STCORE.radd((1,1),(-a[0],a[1]))), ('P(NOT B)', STCORE.radd((1,1),(-b[0],b[1]))), ('P(OR)', union), ('A GIVEN B', STCORE.rdiv(both, b) if b[0] else 'UNDEFINED'), ('B GIVEN A', STCORE.rdiv(both, a) if a[0] else 'UNDEFINED'), ('MUTUALLY EXCLUSIVE', 'YES' if both[0] == 0 else 'NO'), ('INDEPENDENT', 'YES' if both == product else 'NO')], ['OR=A+B-BOTH', 'GIVEN=BOTH/GIVEN GROUP', 'EXCLUSIVE: BOTH=0', 'INDEPENDENT: BOTH=A*B', 'A*B=' + STCORE.exact_text(product), 'USE GIVEN BOTH DIRECTLY'])

def valid_probability():
    p = STCORE.read_exact('PROBABILITY VALUE: ')
    STCORE.results('P13', [('CLASSIFICATION', probability_class(p)), ('CAN BE PROBABILITY', 'YES' if STCORE.compare_exact(p, 0) >= 0 and STCORE.compare_exact(p, 1) <= 0 else 'NO')], ['0<=P<=1; ENDPOINTS VALID', 'NOT A WHOLE TABLE TEST'])


def probability_class(p):
    if STCORE.compare_exact(p,0)<0 or STCORE.compare_exact(p,1)>0: return "INVALID"
    if STCORE.compare_exact(p,0)==0: return "IMPOSSIBLE"
    if STCORE.compare_exact(p,1)==0: return "CERTAIN"
    return "POSSIBLE"


def read_two_way():
    STCORE.heading('P14 TWO-WAY COUNTS')
    nr = STCORE.read_size('ROW COUNT (NO TOTAL): ', 10)
    nc = STCORE.read_size('COLUMN COUNT (NO TOTAL): ', 10)
    rl = [input('ROW NAME: ') for i in range(nr)]
    cl = [input('COLUMN NAME: ') for i in range(nc)]
    cells = []
    for r in range(nr):
        row = []
        for c in range(nc):
            row.append(STCORE.read_int(rl[r] + ' / ' + cl[c] + ': '))
        cells.append(row)
    return rl,cl,cells
