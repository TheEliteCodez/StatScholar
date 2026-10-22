import STCORE as c
def missing_probability():
    c.heading('R05 MISSING PROBABILITY')
    print('EACH P MUST BE 0 TO 1')
    known = []
    count = c.read_size('HOW MANY KNOWN P? ', c.MAX_ROWS)
    for i in range(count):
        while True:
            p = c.read_exact('KNOWN P ' + str(i + 1) + '/' + str(count) + ': ')
            if c.compare_exact(p, 0) >= 0 and c.compare_exact(p, 1) <= 0:
                break
            c.view('R05', ['PROBABILITIES ARE 0..1', 'TRY AGAIN'])
        known.append(p)
    total = c.rsum(known)
    if c.compare_exact(total, 1) > 0:
        c.view('R05', ['KNOWN SUM=' + c.exact_text(total), 'SUM CANNOT EXCEED 1', 'CHECK YOUR P VALUES'])
        return
    missing = c.radd((1, 1), (-total[0], total[1]))
    c.results('R05', [('MISSING P', missing)], ['P=1-SUM(KNOWN P)', 'KNOWN SUM=' + c.exact_text(total), 'ONE UNKNOWN CAN BE FOUND', 'X LABELS NOT NEEDED'])
def read_sample_distribution():
    total=c.read_int('TOTAL OBJECTS N: ')
    targets=c.read_int('TARGET OBJECTS K: ')
    draws=c.read_int('NUMBER SELECTED n: ')
    return c.call('STCOUNT', 'hyper_distribution', total, targets, draws)
def rounded_distribution_session():
    rows,approximate=c.call('STCOUNT', 'read_distribution', True)
    c.call('STCOUNT', 'distribution_session', rows, approximate)
def heights_page(rows, approximate):
    c.paged_results('APPROXIMATE HEIGHTS' if approximate else 'PROBABILITY HISTOGRAM',len(rows),lambda i:('x='+c.exact_text(rows[i][0]),rows[i][1]),['BAR HEIGHT=P(X)', 'INCLUDE EVERY X, INCLUDING ZERO', 'NUMERIC x AXIS; PROBABILITY y AXIS', 'APPROXIMATE HEIGHTS: ROUNDED TABLE' if approximate else 'USE EQUAL-WIDTH BARS'])
def check_table(rows, note, approximate):
    valid = all((c.compare_exact(p, 0) >= 0 and c.compare_exact(p, 1) <= 0 for x, p in rows)) and c.rsum([p for x, p in rows]) == (1, 1)
    lines = note + ['VALID=' + ('UNKNOWN (ROUNDED)' if approximate else str(valid))]
    lines += [c.exact_text(x) + ': ' + c.answer_text(p, 'F') for x, p in rows]
    c.view('R01 TABLE', lines)
