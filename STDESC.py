# Author: Gregory King
# STDESC - compact legacy descriptive solvers.
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
    STCORE.results('G03 OUTLIER FENCES', [('IQR', iqr), ('LOW', STCORE.radd(q1, (-distance[0], distance[1]))), ('HIGH', STCORE.radd(q3, distance))], ['Q1-1.5*IQR; Q3+1.5*IQR'])

def frequency_stats(rows):
    counts = {}
    for x, f in rows:
        counts[x] = counts.get(x, 0) + f
    ordered = STCORE.exact_sorted([x for x in counts if counts[x] > 0])
    total = sum((counts[x] for x in ordered))
    if total == 0:
        raise ValueError('NO OBSERVATIONS')
    weighted = STCORE.rsum([STCORE.rmul(x, (counts[x], 1)) for x in ordered])
    positions = [(total + 1) // 2, total // 2 + 1]
    mid = []
    running = 0
    for x in ordered:
        before = running
        running += counts[x]
        for pos in positions:
            if before < pos <= running:
                mid.append(x)
    median = STCORE.rdiv(STCORE.rsum(mid), (2, 1))
    peak = max(counts.values())
    modes = [x for x in ordered if counts[x] == peak]
    if len(modes) == len(ordered) and len(ordered) > 1 or len(modes) > 2:
        mode = 'DNE'
    else:
        mode = ','.join((STCORE.exact_text(x) for x in modes))
    return (total, weighted, STCORE.rdiv(weighted, (total, 1)), median, mode, positions)

def frequency_session(rows=None):
    STCORE.heading('F05-F07 VALUE/FREQUENCY')
    if rows is None:
        rows = []
        for i in range(STCORE.read_size('NUMBER OF ROWS: ', STCORE.MAX_ROWS)):
            print('ROW ' + str(i + 1))
            rows.append((STCORE.read_exact('DATA VALUE: '), STCORE.read_int('FREQUENCY: ')))
    n, w, mean, median, mode, pos = frequency_stats(rows)
    counts = {}
    for x, f in rows:
        counts[x] = counts.get(x, 0) + f
    cumulative = 0
    details = []
    for x in STCORE.exact_sorted(counts):
        f = counts[x]
        cumulative += f
        details += ['x=' + STCORE.exact_text(x) + ' f=' + str(f) + ' xf=' + STCORE.exact_text(STCORE.rmul(x, (f, 1))), 'CUMULATIVE f=' + str(cumulative), 'RELATIVE f=' + STCORE.answer_text(STCORE.ratio(f, n))]
    STCORE.results('F05/F06/F07/F03', [('MEAN', mean), ('MEDIAN', median), ('MODE', mode)], ['n=SUM(f)=' + str(n), 'SUM(x*f)=' + STCORE.exact_text(w), 'MEAN=SUM(x*f)/n', 'MIDDLE POS=' + str(pos[0]) + ',' + str(pos[1]), 'MODE=VALUE WITH MOST f', '2 MODES: COMMA; >2: DNE', 'EQUAL COUNTS: NO MODE', '1-VAR: VALUES L1, FREQ L2'] + details)
