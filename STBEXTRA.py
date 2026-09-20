# STBEXTRA - loaded on demand.
import STCORE
import math
from STBMATH import *

def binomial_model_session():
    STCORE.heading('B01 IDENTIFY DISTRIBUTION')
    print('COUNT OF INDEPENDENT RESULTS')
    n = STCORE.read_int('NUMBER OF TRIALS n: ')
    p = STCORE.read_exact('CHANCE EACH TRIAL p: ')
    STCORE.results('B01 DISTRIBUTION', [('X', 'NUMBER OF SUCCESSES'), ('DISTRIBUTION', 'X~Binomial(' + str(n) + ',' + STCORE.exact_text(p) + ')')], ['FIXED n; SAME p; INDEPENDENT', 'n=' + str(n) + ' p=' + STCORE.exact_text(p)])
    STCORE.call('STBINOM','binomial_session',n,p)

def symmetry_session():
    STCORE.heading('B12 COMPARE TAILS')
    n = STCORE.read_int('NUMBER OF TRIALS n: ')
    lower = STCORE.read_exact('LEFT EVENT: X LESS THAN: ')
    upper = STCORE.read_exact('RIGHT EVENT: X MORE THAN: ')
    raw = input('p (ENTER IF NOT GIVEN): ').strip()
    left = ('<', lower, 0)
    right = ('>', upper, 0)
    work = ['LEFT: X<' + STCORE.exact_text(lower), 'RIGHT: X>' + STCORE.exact_text(upper), 'n=' + str(n)]
    if raw:
        p = STCORE.as_ratio(raw)
        a = binomial_exact_event(n, p, left)
        b = binomial_exact_event(n, p, right)
        STCORE.results('B12 TAIL EQUALITY', [('P(LEFT)', a), ('P(RIGHT)', b), ('EQUAL', 'YES' if STCORE.compare_exact(a, b) == 0 else 'NO')], work + ['p=' + STCORE.exact_text(p)])
    else:
        same = all((STCORE.event_match(k, *left) == STCORE.event_match(k, *right) for k in range(n + 1)))
        reflected = all((STCORE.event_match(k, *left) == STCORE.event_match(n - k, *right) for k in range(n + 1)))
        STCORE.results('B12 GENERAL CLAIM', [('ALWAYS EQUAL', 'YES' if same else 'NO')], work + ['NO p GIVEN: NOT GENERALLY .5', 'AT p=.5 REFLECTED TAILS MATCH' if reflected else 'CHECK THE ACTUAL EVENTS', 'A FIXED n ALONE IS NOT ENOUGH'])

def shape_tasks():
    c = STCORE.menu('B12 SHAPE / SYMMETRY', [('1', 'MATCH HISTOGRAM'), ('2', 'COMPARE TAILS')])
    if c == '1':
        shape_session()
    elif c == '2':
        symmetry_session()

def shape_session():
    n = STCORE.read_int('BINOMIAL n ON GRAPH: ')
    candidates = []
    for i in range(STCORE.read_size('NUMBER OF p OPTIONS: ', 10)):
        candidates.append(STCORE.read_exact('CANDIDATE p: '))
    lines = ['MATCH CENTER, NOT JUST PEAK', 'CENTER mu=n*p', 'p=.5: SYMMETRIC TAILS', 'TAIL SYMMETRY NOT GENERAL']
    for p in candidates:
        lines += ['p=' + STCORE.exact_text(p) + ' CENTER=' + STCORE.exact_text(STCORE.rmul((n, 1), p)), binomial_shape(p)]
    STCORE.view('B12 GRAPH MATCH', lines)
    for p in candidates:
        if STCORE.yesno('SHOW TABLE FOR p=' + STCORE.exact_text(p) + '?'):
            STCORE.paged_results('B12 BAR HEIGHTS', n + 1, lambda k: ('P(' + str(k) + ')', binomial_exact_ratio(n, p, k)))

def binomial_conditions():
    conditions = [('IS THE NUMBER OF TRIALS FIXED?', 'FIXED NUMBER OF TRIALS NEEDED'), ('IS EACH RESULT SUCCESS OR NOT?', 'NEED TWO RESULT CATEGORIES'), ('IS THE CHANCE THE SAME EACH TIME?', 'SUCCESS CHANCE MUST STAY SAME'), ('ARE TRIALS INDEPENDENT OR APPROX SO?', 'DEPENDENT TRIALS NOT BINOMIAL')]
    for prompt, reason in conditions:
        if not STCORE.yesno(prompt):
            STCORE.results('B01', [('BINOMIAL', 'NO')], [reason, 'SMALL BOX, NO REPLACEMENT: R07'])
            return
    STCORE.results('B01', [('BINOMIAL', 'YES')], ['X=NUMBER OF SUCCESSES', 'n=TRIALS; p=CHANCE EACH', 'REPLACED + SHUFFLED: INDEPENDENT', 'LARGE POP, SMALL SAMPLE:', 'MAY BE APPROX INDEPENDENT', 'FINITE N,n CHECK: BINOMIAL PAGE2 OPTION7'])
