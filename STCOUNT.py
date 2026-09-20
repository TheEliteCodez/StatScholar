# Author: TheEliteCodez
# STCOUNT - solver code; references load separately.
import STCORE
import math
from STCOMB import factorial, ncr, npr







def solver_sample_space():
    stages = STCORE.read_int('# STAGES: ')
    total = 1
    work = []
    for i in range(stages):
        choices = STCORE.read_int('CHOICES ' + str(i + 1) + ': ')
        total *= choices
        work.append('STAGE ' + str(i + 1) + '=' + str(choices))
    STCORE.results('C01 SAMPLE SPACE', [('TOTAL', (total, 1))], ['MULTIPLY CHOICES'] + work)

def solver_ncr():
    n = STCORE.read_int('n: ')
    r = STCORE.read_int('r: ')
    STCORE.results('C03', [('ANSWER', (ncr(n, r), 1))], [str(n) + ' ncr ' + str(r)])

def solver_npr():
    n = STCORE.read_int('n: ')
    r = STCORE.read_int('r: ')
    STCORE.results('C04', [('ANSWER', (npr(n, r), 1))], [str(n) + ' npr ' + str(r)])

def solver_expected():
    distribution_session()

def table_probability(rows, event):
    return STCORE.rsum([p for x, p in rows if STCORE.event_match(x, *event)])

def distribution_moments(rows):
    mean = STCORE.rsum([STCORE.rmul(x, p) for x, p in rows])
    second = STCORE.rsum([STCORE.rmul(STCORE.rmul(x, x), p) for x, p in rows])
    square = STCORE.rmul(mean, mean)
    var = STCORE.radd(second, (-square[0], square[1]))
    return (mean, var, math.sqrt(max(0, STCORE.number(var))))

def read_distribution(approximate=False):
    print("ENTER x BY LABEL, EVEN IF x IS THE SECOND COLUMN")
    rows = []
    missing = []
    STCORE.heading('X / P(X): MATCH COLUMNS')
    print('X=VALUE; P=PROBABILITY')
    print('0+ OR ~.123 ROUNDED; ? MISSING')
    for i in range(STCORE.read_size('NUMBER OF ROWS: ', STCORE.MAX_ROWS)):
        print('ROW ' + str(i + 1))
        x = STCORE.read_exact('X VALUE: ')
        raw = input('P(X), 0+, OR ?: ').strip()
        if raw == '?':
            missing.append(i)
            p = (0, 1)
        elif raw == '0+':
            approximate = True
            p = (0, 1)
        else:
            if raw.startswith('~'):
                approximate=True
                raw=raw[1:]
            p = STCORE.as_ratio(raw)
        rows.append((x, p))
    if missing:
        if len(missing) > 1 or approximate:
            raise ValueError('MISSING P NEEDS ALL OTHER P')
        total = STCORE.rsum([p for x, p in rows])
        i = missing[0]
        rows[i] = (rows[i][0], STCORE.radd((1, 1), (-total[0], total[1])))
        STCORE.results('R05 COMPLETED TABLE', [('MISSING P', rows[i][1])], ['1-SUM(KNOWN P)'])
    return (rows, approximate)

def unusual_result(prob):
    raw = input('UNUSUAL CUTOFF (ENTER=.05): ').strip()
    threshold = STCORE.as_ratio(raw or '.05')
    STCORE.results('R06 UNUSUAL EVENT', [('P(EVENT)', prob), ('UNUSUAL', 'YES' if STCORE.compare_exact(prob, threshold) <= 0 else 'NO')], ['UNUSUAL IF P<=CUTOFF', 'CUTOFF=' + STCORE.exact_text(threshold), 'USE LOWER TAIL FOR FEW', 'UPPER TAIL FOR MANY', 'EVIDENCE UNDER THE MODEL', 'NOT PROOF OF A CAUSE'])

def distribution_session(rows=None, approximate=False, source=None, first_word=None):
    if rows is None:
        rows, approximate = read_distribution()
    while True:
        key = '1' if first_word else STCORE.menu('R02-R06 TABLE TASK', [('1', 'EVENT PROBABILITY'), ('2', 'MEAN / VAR / SD'), ('3', 'X>=1 BY COMPLEMENT'), ('4', 'UNUSUAL EVENT'), ('5', 'CHECK / SHOW TABLE'), ('6', 'EXACT BINOMIAL MODEL'), ('7','CHANGE DATA'),('8','MARK TABLE AS ROUNDED'),('9','GRAPH THIS P(X) TABLE')])
        if key == '0':
            return
        if key == '9':
            STCORE.paged_results('APPROXIMATE HEIGHTS' if approximate else 'PROBABILITY HISTOGRAM',len(rows),lambda i:('x='+STCORE.exact_text(rows[i][0]),rows[i][1]),['BAR HEIGHT=P(X)', 'INCLUDE EVERY X, INCLUDING ZERO', 'NUMERIC x AXIS; PROBABILITY y AXIS', 'APPROXIMATE HEIGHTS: ROUNDED TABLE' if approximate else 'USE EQUAL-WIDTH BARS'])
            continue
        if key == '8':
            approximate=True
            continue
        if key == '7':
            if source=='sample':
                rows=read_sample_distribution()
                approximate=False
            else:
                rows,approximate=read_distribution(approximate)
            continue
        if key == '6':
            STCORE.call('STBWORD','wording_session')
            continue
        note = ['ENTERED P TOTAL=' + STCORE.exact_text(STCORE.rsum([p for x, p in rows]))]
        if approximate:
            note += ['ROUNDED TABLE: APPROXIMATE P', 'EXACT ANSWER UNAVAILABLE', 'ROUNDED ZERO NEED NOT BE IMPOSSIBLE', 'NO AUTOMATIC NORMALIZATION', 'USE MODEL IF ITS ASSUMPTIONS APPLY']
        if key == '2':
            if approximate or STCORE.rsum(p for x,p in rows)!=(1,1):
                STCORE.view('ROUNDED TABLE / TOTAL', note + ['EXACT MOMENTS REQUIRE KNOWN P SUMMING TO 1.', 'OPTION 8 MARKS ROUNDED INPUT.', 'OPTION 6: BINOMIAL ONLY IF JUSTIFIED.'])
                continue
            mean, var, sd = distribution_moments(rows)
            STCORE.results('R02/R03', [('mu', mean), ('VAR', var), ('sigma', sd)], note + ['mu=SUM(x*P(x))', 'VAR=SUM(x^2*P)-mu^2', 'SD=SQRT(VAR)'])
        elif key == '5':
            valid = all((STCORE.compare_exact(p, 0) >= 0 and STCORE.compare_exact(p, 1) <= 0 for x, p in rows)) and STCORE.rsum([p for x, p in rows]) == (1, 1)
            lines = note + ['VALID=' + ('UNKNOWN (ROUNDED)' if approximate else str(valid))]
            lines += [STCORE.exact_text(x) + ': ' + STCORE.answer_text(p, 'F') for x, p in rows]
            STCORE.view('R01 TABLE', lines)
        else:
            counts_only = all((x[1] == 1 and x[0] >= 0 for x, p in rows))
            if first_word:
                ev=STCORE.call('STBWORD','read_event',first_word)
                first_word=None
            else:
                ev = (('=', 0, 0) if counts_only else ('<', 1, 0)) if key == '3' else STCORE.event_input()
            if ev is None:
                continue
            p = table_probability(rows, ev)
            if key == '3':
                p = STCORE.radd((1, 1), (-p[0], p[1]))
            if key == '4' and (not approximate):
                unusual_result(p)
            else:
                selected = [STCORE.exact_text(x) for x, q in rows if STCORE.event_match(x, *ev)]
                STCORE.results('R04 TABLE EVENT', [('P APPROX' if approximate else 'P', p)], note + (['P=1-P(0)' if counts_only else 'P(X>=1)=1-P(X<1)'] if key == '3' else ['ADD MATCHING ROWS']) + ['ROWS: ' + ','.join(selected)])

def missing_probability():
    STCORE.heading('R05 MISSING PROBABILITY')
    known = []
    for i in range(STCORE.read_size('HOW MANY KNOWN P? ', STCORE.MAX_ROWS)):
        known.append(STCORE.read_exact('KNOWN P: '))
    total = STCORE.rsum(known)
    missing = STCORE.radd((1, 1), (-total[0], total[1]))
    STCORE.results('R05', [('MISSING P', missing)], ['P=1-SUM(KNOWN P)', 'KNOWN SUM=' + STCORE.exact_text(total), 'ONE UNKNOWN CAN BE FOUND', 'X LABELS NOT NEEDED'])

def hyper_distribution(npop, targets, draws):
    return STCORE.call('STSAMPLE','hyper_distribution',npop,targets,draws)


def sample_session():
    return STCORE.call('STSAMPLE','sample_session')


def payoff_session():
    STCORE.heading('R08 PAYOFF TABLE')
    print('WHOSE MONEY? USE THEIR SIGNS')
    print('USE ALL COUNTS OR ALL P VALUES')
    who = input('PERSPECTIVE (PLAYER ETC): ')
    print('NET OUTCOMES: ENTER COST 0')
    cost = STCORE.read_exact('SEPARATE COST PER PLAY: ')
    rows = []
    for i in range(STCORE.read_size('NUMBER OF OUTCOMES: ', STCORE.MAX_ROWS)):
        x = STCORE.read_exact('PRIZE OR SIGNED NET VALUE: ')
        p = STCORE.read_exact('CHANCE WEIGHT (COUNT OR P): ')
        rows.append((STCORE.radd(x, (-cost[0], cost[1])), p))
    total = STCORE.rsum([p for x, p in rows])
    rows = [(x, STCORE.rdiv(p, total)) for x, p in rows]
    mean, var, sd = distribution_moments(rows)
    STCORE.results('R08 ' + who, [('EXPECTED PROFIT', mean), ('SD', sd)], ['NET=VALUE-SEPARATE COST', 'P=WEIGHT/TOTAL WEIGHTS', 'E=SUM(NET*P)', 'LOSS IS NEGATIVE', 'EV IS DOLLARS, NOT WIN %'], default_places=2)
    distribution_session(rows)

def insurance_session():
    perspective=STCORE.menu('WHOSE EXPECTED PROFIT?', [('1','INSURANCE COMPANY'),('2','POLICYHOLDER / BENEFICIARY')])
    if perspective=='0': return
    survive = STCORE.read_exact('P(SURVIVE): ')
    premium = STCORE.read_exact('PREMIUM RECEIVED: ')
    benefit = STCORE.read_exact('DEATH BENEFIT PAID: ')
    death = STCORE.radd((1, 1), (-survive[0], survive[1]))
    payout = STCORE.rmul(death, benefit)
    mean = STCORE.radd(premium, (-payout[0], payout[1]))
    if perspective=='2': mean=(-mean[0],mean[1])
    STCORE.results('R08 INSURANCE', [('COMPANY EXPECTED PROFIT' if perspective=='1' else 'POLICY NET EXPECTED VALUE', mean)], ['PREMIUM-P(DEATH)*BENEFIT', 'P(DEATH)=' + STCORE.exact_text(death), 'ROUND MONEY TO 2 PLACES'], default_places=2)

def raffle_session():
    total = STCORE.read_int('TOTAL TICKETS: ')
    cost = STCORE.read_exact('PRICE PER TICKET: ')
    prize = STCORE.read_exact('ONE PRIZE VALUE/COST: ')
    bought = STCORE.read_int('TICKETS YOU BUY: ')
    gross = STCORE.rdiv(prize, (total, 1))
    buyer = STCORE.radd(gross, (-cost[0], cost[1]))
    org = (-buyer[0], buyer[1])
    STCORE.results('R08 RAFFLE', [('BUYER ONE', buyer), ('BUYER ALL BOUGHT', STCORE.rmul(buyer, (bought, 1))), ('ORGANIZER ONE', org), ('ORGANIZER ALL SOLD', STCORE.rmul(org, (total, 1)))], ['BUYER=PRIZE/TOTAL-PRICE', 'MULTIPLY UNROUNDED E', 'ONE PRIZE; NO OTHER COSTS', 'PRIZE VALUE ASSUMED COST', 'ROUND MONEY TO 2 PLACES'], default_places=2)

def win_loss_session():
    chance = STCORE.read_exact('CHANCE CORRECT EACH TRY: ')
    trials = STCORE.read_int('CORRECT EVERY TIME: HOW MANY? ')
    win = STCORE.read_exact('NET PROFIT IF WIN: ')
    loss = STCORE.read_exact('AMOUNT LOST IF LOSE: ')
    p = STCORE.ratio(chance[0] ** trials, chance[1] ** trials)
    rows = [((-abs(loss[0]), loss[1]), STCORE.radd((1, 1), (-p[0], p[1]))), (win, p)]
    mean, var, sd = distribution_moments(rows)
    STCORE.results('P05/R08 WIN OR LOSE', [('P(LOSE)', rows[0][1]), ('P(WIN)', p), ('E(PROFIT)', mean), ('SD', sd)], ['INDEPENDENT TRIES', 'P(WIN)=p^n', 'USE NET PAYOFFS AS GIVEN', 'NO EXTRA FEE SUBTRACTED'])
    distribution_session(rows)

def payoff_tasks():
    key = STCORE.menu('GAME PAYOFFS', [('1', 'PRIZES / NET + P TABLE'), ('2', 'ALL GUESSES MUST WIN')])
    if key == '1':
        payoff_session()
    elif key == '2':
        win_loss_session()


def sample_word_session(word=None):
    return STCORE.call('STSAMPLE','sample_word_session',word)


def read_sample_distribution():
    total=STCORE.read_int('TOTAL OBJECTS N: ')
    targets=STCORE.read_int('TARGET OBJECTS K: ')
    draws=STCORE.read_int('NUMBER SELECTED n: ')
    return hyper_distribution(total,targets,draws)


def rounded_distribution_session():
    rows,approximate=read_distribution(True)
    distribution_session(rows,approximate)
