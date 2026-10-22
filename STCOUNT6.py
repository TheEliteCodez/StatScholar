import STCORE as c
from STCOMB import ncr, npr
def win_loss_session():
    chance = c.read_exact('CHANCE CORRECT EACH TRY: ')
    trials = c.read_int('CORRECT EVERY TIME: HOW MANY? ')
    win = c.read_exact('NET PROFIT IF WIN: ')
    loss = c.read_exact('AMOUNT LOST IF LOSE: ')
    p = c.ratio(chance[0] ** trials, chance[1] ** trials)
    rows = [((-abs(loss[0]), loss[1]), c.radd((1, 1), (-p[0], p[1]))), (win, p)]
    mean, var, sd = c.call('STCOUNT', 'distribution_moments', rows)
    c.results('P05/R08 WIN OR LOSE', [('P(LOSE)', rows[0][1]), ('P(WIN)', p), ('E(PROFIT)', mean), ('SD', sd)], ['INDEPENDENT TRIES', 'P(WIN)=p^n', 'USE NET PAYOFFS AS GIVEN', 'NO EXTRA FEE SUBTRACTED'])
    c.call('STCOUNT', 'distribution_session', rows)
def payoff_tasks():
    key = c.menu('GAME PAYOFFS', [('1', 'PRIZES / NET + P TABLE'), ('2', 'ALL GUESSES MUST WIN')])
    if key == '1':
        c.call('STCOUNT', 'payoff_session')
    elif key == '2':
        win_loss_session()
def money_session():
    while True:
        key=c.menu('EXPECTED VALUE / MONEY',[('1','X / P TABLE'),('2','PRIZES / PAYOFFS'),('3','INSURANCE'),('4','RAFFLE')])
        if key=='0': return
        if key=='1': c.call('STCOUNT', 'distribution_session')
        elif key=='2': payoff_tasks()
        elif key=='3': c.call('STCOUNT', 'insurance_session')
        elif key=='4': c.call('STCOUNT', 'raffle_session')
def solver_sample_space():
    stages = c.read_int('# STAGES: ')
    total = 1
    work = []
    for i in range(stages):
        choices = c.read_int('CHOICES ' + str(i + 1) + ': ')
        total *= choices
        work.append('STAGE ' + str(i + 1) + '=' + str(choices))
    c.results('C01 SAMPLE SPACE', [('TOTAL', (total, 1))], ['MULTIPLY CHOICES'] + work)
def solver_ncr():
    n = c.read_int('n: ')
    r = c.read_int('r: ')
    c.results('C03', [('ANSWER', (ncr(n, r), 1))], [str(n) + ' ncr ' + str(r)])
def solver_npr():
    n = c.read_int('n: ')
    r = c.read_int('r: ')
    c.results('C04', [('ANSWER', (npr(n, r), 1))], [str(n) + ' npr ' + str(r)])
def solver_expected():
    c.call('STCOUNT', 'distribution_session')
