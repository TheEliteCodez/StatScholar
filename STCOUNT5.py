import STCORE as c
def payoff_session():
    c.heading('R08 PAYOFF TABLE')
    print('WHOSE MONEY? USE THEIR SIGNS')
    print('USE ALL COUNTS OR ALL P VALUES')
    who = input('PERSPECTIVE (PLAYER ETC): ')
    print('NET OUTCOMES: ENTER COST 0')
    cost = c.read_exact('SEPARATE COST PER PLAY: ')
    rows = []
    for i in range(c.read_size('NUMBER OF OUTCOMES: ', c.MAX_ROWS)):
        x = c.read_exact('PRIZE OR SIGNED NET VALUE: ')
        p = c.read_exact('CHANCE WEIGHT (COUNT OR P): ')
        rows.append((c.radd(x, (-cost[0], cost[1])), p))
    total = c.rsum([p for x, p in rows])
    rows = [(x, c.rdiv(p, total)) for x, p in rows]
    mean, var, sd = c.call('STCOUNT', 'distribution_moments', rows)
    c.results('R08 ' + who, [('EXPECTED PROFIT', mean), ('SD', sd)],
              c.call('STDWK','payoff',rows,cost,total,mean,var,sd),default_places=2)
    c.call('STCOUNT', 'distribution_session', rows)
def insurance_session():
    perspective=c.menu('WHOSE EXPECTED PROFIT?', [('1','INSURANCE COMPANY'),('2','POLICYHOLDER / BENEFICIARY')])
    if perspective=='0': return
    survive = c.read_exact('P(SURVIVE): ')
    premium = c.read_exact('PREMIUM RECEIVED: ')
    benefit = c.read_exact('DEATH BENEFIT PAID: ')
    death = c.radd((1, 1), (-survive[0], survive[1]))
    payout = c.rmul(death, benefit)
    mean = c.radd(premium, (-payout[0], payout[1]))
    if perspective=='2': mean=(-mean[0],mean[1])
    work=['P(DEATH)=1-%s=%s' % (c.exact_text(survive),c.exact_text(death)),
          'EXPECTED PAYOUT=%s*%s=%s' % (c.exact_text(death),c.exact_text(benefit),c.exact_text(payout))]
    work+=['E=PREMIUM-PAYOUT=%s-%s=%s' % (c.exact_text(premium),c.exact_text(payout),c.exact_text(mean))] if perspective=='1' else [
          'E=PAYOUT-PREMIUM=%s-%s=%s' % (c.exact_text(payout),c.exact_text(premium),c.exact_text(mean))]
    c.results('R08 INSURANCE', [('COMPANY EXPECTED PROFIT' if perspective=='1' else 'POLICY NET EXPECTED VALUE', mean)],work,default_places=2)
def raffle_session():
    total = c.read_int('TOTAL TICKETS: ')
    cost = c.read_exact('PRICE PER TICKET: ')
    prize = c.read_exact('ONE PRIZE VALUE/COST: ')
    bought = c.read_int('TICKETS YOU BUY: ')
    gross = c.rdiv(prize, (total, 1))
    buyer = c.radd(gross, (-cost[0], cost[1]))
    org = (-buyer[0], buyer[1])
    work=['E(BUYER ONE)=PRIZE/TOTAL-PRICE=%s/%d-%s=%s' % (c.exact_text(prize),total,c.exact_text(cost),c.exact_text(buyer)),
          'E(BUYER ALL)=%d*(%s)=%s' % (bought,c.exact_text(buyer),c.exact_text(c.rmul(buyer,(bought,1)))),
          'E(ORGANIZER ONE)=-(%s)=%s' % (c.exact_text(buyer),c.exact_text(org)),
          'E(ORGANIZER SOLD)=%d*%s-%s=%s' % (total,c.exact_text(cost),c.exact_text(prize),c.exact_text(c.rmul(org,(total,1)))),
          'ONE PRIZE; NO OTHER COSTS; ROUND MONEY TO 2 PLACES']
    c.results('R08 RAFFLE', [('BUYER ONE', buyer), ('BUYER ALL BOUGHT', c.rmul(buyer, (bought, 1))), ('ORGANIZER ONE', org), ('ORGANIZER ALL SOLD', c.rmul(org, (total, 1)))],work,default_places=2)
