# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Value/frequency descriptive session.
import STCORE

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
    if peak==1 or len(modes) == len(ordered) and len(ordered) > 1 or len(modes) > 2:
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
