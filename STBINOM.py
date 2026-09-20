# Author: TheEliteCodez
# STBINOM - solver code; references load separately.
import STCORE
from STBMATH import *
import math




def solver_bin_exact():
    n = STCORE.read_int('n TRIALS: ')
    p = STCORE.read_exact('p SUCCESS: ')
    x = STCORE.read_int('x CUTOFF: ')
    STCORE.results('BINOMIAL =', [('P', binomial_exact_event(n, p, ('=', x, 0)))], ['n=' + str(n) + ' p=' + STCORE.exact_text(p), 'X = ' + str(x)])

def solver_bin_at_most():
    n = STCORE.read_int('n TRIALS: ')
    p = STCORE.read_exact('p SUCCESS: ')
    x = STCORE.read_int('x CUTOFF: ')
    STCORE.results('BINOMIAL <=', [('P', binomial_exact_event(n, p, ('<=', x, 0)))], ['n=' + str(n) + ' p=' + STCORE.exact_text(p), 'X <= ' + str(x)])

def solver_bin_less():
    n = STCORE.read_int('n TRIALS: ')
    p = STCORE.read_exact('p SUCCESS: ')
    x = STCORE.read_int('x CUTOFF: ')
    STCORE.results('BINOMIAL <', [('P', binomial_exact_event(n, p, ('<', x, 0)))], ['n=' + str(n) + ' p=' + STCORE.exact_text(p), 'X < ' + str(x)])

def solver_bin_at_least():
    n = STCORE.read_int('n TRIALS: ')
    p = STCORE.read_exact('p SUCCESS: ')
    x = STCORE.read_int('x CUTOFF: ')
    STCORE.results('BINOMIAL >=', [('P', binomial_exact_event(n, p, ('>=', x, 0)))], ['n=' + str(n) + ' p=' + STCORE.exact_text(p), 'X >= ' + str(x)])

def solver_bin_more():
    n = STCORE.read_int('n TRIALS: ')
    p = STCORE.read_exact('p SUCCESS: ')
    x = STCORE.read_int('x CUTOFF: ')
    STCORE.results('BINOMIAL >', [('P', binomial_exact_event(n, p, ('>', x, 0)))], ['n=' + str(n) + ' p=' + STCORE.exact_text(p), 'X > ' + str(x)])

def solver_bin_between():
    n = STCORE.read_int('n TRIALS: ')
    p = STCORE.read_exact('p SUCCESS: ')
    a = STCORE.read_int('LOWER: ')
    b = STCORE.read_int('UPPER: ')
    STCORE.results('B10 BETWEEN', [('P', binomial_exact_event(n, p, ('[]', a, b)))], [str(a) + '<=X<=' + str(b), 'n=' + str(n) + ' p=' + STCORE.exact_text(p)])

def solver_bin_mean_sd():
    n = STCORE.read_int('n TRIALS: ')
    p = STCORE.read_exact('p SUCCESS: ')
    mean = STCORE.rmul((n, 1), p)
    var = STCORE.rmul(mean, STCORE.radd((1, 1), (-p[0], p[1])))
    STCORE.results('B08/B09', [('mu', mean), ('VAR', var), ('sigma', math.sqrt(STCORE.number(var)))], ['mu=np; VAR=np(1-p)'])









def binomial_session(n=None, exact_p=None, first_action=None):
    STCORE.heading('BINOMIAL: COUNT A RESULT')
    print('FIXED n, SAME p, INDEPENDENT')
    if n is None:
        n = STCORE.read_int('HOW MANY TRIALS n: ')
    if exact_p is None:
        exact_p = STCORE.read_exact('CHANCE EACH TRIAL p: ')
    mean = STCORE.rmul((n, 1), exact_p)
    variance = STCORE.rmul(mean, STCORE.radd((1, 1), (-exact_p[0], exact_p[1])))
    while True:
        key = first_action or STCORE.menu('BINOMIAL > NEXT', [('1', 'EVENT PROBABILITY'), ('2', 'MEAN / SD / SYMBOLS'), ('3', 'FULL TABLE / SHAPE'), ('4', 'USUAL RANGE / TAILS'), ('5', 'GRAPH / SHAPE'), ('6', 'UNUSUAL PROBABILITY'), ('7', 'CHANGE n,p')])
        first_action = None
        if key == '0':
            return
        if key=='7':
            n=STCORE.read_int('HOW MANY TRIALS n: ')
            exact_p=STCORE.read_exact('CHANCE EACH TRIAL p: ')
            mean=STCORE.rmul((n,1),exact_p)
            variance=STCORE.rmul(mean,STCORE.radd((1,1),(-exact_p[0],exact_p[1])))
            continue
        if key=='5':
            STCORE.results('BINOMIAL > SHAPE',[('SHAPE',binomial_shape(exact_p)),('CENTER',mean)],['BAR HEIGHT=P(X=k)', 'USE FULL DISTRIBUTION FOR HEIGHTS'])
            continue
        if key in ('1', '6'):
            event = STCORE.event_input(True)
            if event is None:
                continue
            answer = binomial_exact_event(n, exact_p, event)
            if key == '6':
                STCORE.call('STCOUNT','unusual_result',answer)
            else:
                op, a, b = event
                guide_id = {'=': 'B02', '<=': 'B03', '<': 'B04', '>=': 'B05', '>': 'B06'}.get(op, 'B10')
                STCORE.results(guide_id, [('P', answer)], ['X ' + op + ' ' + STCORE.exact_text(a) + (',' + STCORE.exact_text(b) if len(op) == 2 and op[0] in '[(' else ''), 'n=' + str(n) + ' p=' + STCORE.exact_text(exact_p), 'SUM MATCHING BINOMIAL P'] + binomial_method(n,exact_p,event))
        elif key == '2':
            STCORE.results('B08/B09', [('mu', mean), ('VAR', variance), ('sigma', math.sqrt(STCORE.number(variance)))], ['mu=n*p', 'sigma=SQRT(n*p*(1-p))', 'UNITS: NUMBER OF SUCCESSES', 'mu: LONG-RUN AVERAGE COUNT', 'sigma: DISTRIBUTION SD', 'X: COUNT; n: TRIALS; p: CHANCE'])
        elif key == '3':
            STCORE.paged_results('B11 DISTRIBUTION', n + 1, lambda k: ('P(' + str(k) + ')', binomial_exact_ratio(n, exact_p, k)), ['X=NUMBER OF SUCCESSES', 'X VALUES: 0 THROUGH n', 'SHAPE=' + binomial_shape(exact_p), 'mu=' + STCORE.exact_text(STCORE.rmul((n, 1), exact_p)), 'P(k)=nCk*p^k*(1-p)^(n-k)'])
        else:
            mu, sd, lo, hi, low, high, first = usual_counts(n, exact_p)
            inside = binomial_exact_event(n, exact_p, ('[]', low, high))
            answers = [('mu', mean), ('sigma', sd), ('MIN USUAL', lo), ('MAX USUAL', hi), ('MIN USUAL COUNT', str(low) if low <= high else 'NONE'), ('MAX USUAL COUNT', str(high) if low <= high else 'NONE'), ('USUAL INTEGERS', str(low) + '..' + str(high) if low <= high else 'NONE'), ('FIRST UNUSUALLY HIGH', str(first) if first is not None else 'NONE ATTAINABLE'), ('P(INSIDE)', inside), ('P(BELOW)', binomial_exact_event(n, exact_p, ('<', low, 0))), ('P(ABOVE)', binomial_exact_event(n, exact_p, ('>', high, 0)))]
            if first is not None:
                answers.append(('P(X>=FIRST HIGH)', binomial_exact_event(n, exact_p, ('>=', first, 0))))
            STCORE.results('B13 RANGE RULE', answers, ['mu +/- 2*sigma', 'ROUND INWARD FOR INTEGERS', 'HIGH UNUSUAL: STRICTLY >', 'TAILS USE BINOMIAL SUMS', 'APPROX 95% ONLY IF BELL-SHAPED'])
            print('IS A NUMBER UNUSUAL?')
            observed = input('COUNT (ENTER=SKIP): ').strip()
            if observed:
                k = int(observed)
                mean = STCORE.rmul((n, 1), exact_p)
                variance = STCORE.rmul(mean, STCORE.radd((1, 1), (-exact_p[0], exact_p[1])))
                position = STCORE.range_relation(k, mean, variance)
                STCORE.results('B13 OBSERVATION', [('NUMBER', k), ('UNUSUAL', 'YES' if position else 'NO'), ('CLASSIFICATION', 'UNUSUALLY LOW' if position < 0 else 'UNUSUALLY HIGH' if position > 0 else 'NOT UNUSUAL')], ['COMPARE WITH mu +/- 2 SD'])














def binomial_method(n,p,event):
    op,a,b=event
    prefix='n='+str(n)+' p='+STCORE.exact_text(p)
    if op=='=': return [prefix,'P(X=x)=nCx*p^x*(1-p)^(n-x)','binompdf(n,p,x)']
    import math
    x=STCORE.number(a)
    if op=='<=': text='binomcdf(n,p,'+str(math.floor(x))+')'
    elif op=='<': text='binomcdf(n,p,'+str(math.ceil(x)-1)+')'
    elif op=='>=': text='1-binomcdf(n,p,'+str(math.ceil(x)-1)+')'
    elif op=='>': text='1-binomcdf(n,p,'+str(math.floor(x))+')'
    else: text='SUM binompdf OVER MATCHING INTEGERS'
    return [prefix,text]
