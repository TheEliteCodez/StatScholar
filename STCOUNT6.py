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
    c.results('P05/R08 WIN OR LOSE', [('P(LOSE)', rows[0][1]), ('P(WIN)', p), ('E(PROFIT)', mean), ('SD', sd)],
              c.call('STWORK','Chain',['P(WIN)=(%s)^%d=%s' % (c.exact_text(chance),trials,c.exact_text(p)),
                     'P(LOSE)=1-%s=%s' % (c.exact_text(p),c.exact_text(rows[0][1]))],
                     c.call('STDWK','moments',len(rows),lambda i:rows[i],mean,var,sd)))
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
    answer=ncr(n,r)
    work=['nCr=n!/(r!*(n-r)!)',
          'C(%d,%d)=%d!/(%d!*%d!)=%d' % (n,r,n,r,n-r,answer)] if 0<=r<=n else ['INVALID n,r: COUNT=0']
    c.results('C03', [('ANSWER', (answer, 1))],work)
def solver_npr():
    n = c.read_int('n: ')
    r = c.read_int('r: ')
    answer=npr(n,r)
    work=['nPr=n!/(n-r)!',
          'P(%d,%d)=%d!/%d!=%d' % (n,r,n,n-r,answer)] if 0<=r<=n else ['INVALID n,r: COUNT=0']
    c.results('C04', [('ANSWER', (answer, 1))],work)
def solver_expected():
    c.call('STCOUNT', 'distribution_session')
