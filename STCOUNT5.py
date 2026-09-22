# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Expected-value / money solvers.
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
    c.results('R08 ' + who, [('EXPECTED PROFIT', mean), ('SD', sd)], ['NET=VALUE-SEPARATE COST', 'P=WEIGHT/TOTAL WEIGHTS', 'E=SUM(NET*P)', 'LOSS IS NEGATIVE', 'EV IS DOLLARS, NOT WIN %'], default_places=2)
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
    c.results('R08 INSURANCE', [('COMPANY EXPECTED PROFIT' if perspective=='1' else 'POLICY NET EXPECTED VALUE', mean)], ['PREMIUM-P(DEATH)*BENEFIT', 'P(DEATH)=' + c.exact_text(death), 'ROUND MONEY TO 2 PLACES'], default_places=2)


def raffle_session():
    total = c.read_int('TOTAL TICKETS: ')
    cost = c.read_exact('PRICE PER TICKET: ')
    prize = c.read_exact('ONE PRIZE VALUE/COST: ')
    bought = c.read_int('TICKETS YOU BUY: ')
    gross = c.rdiv(prize, (total, 1))
    buyer = c.radd(gross, (-cost[0], cost[1]))
    org = (-buyer[0], buyer[1])
    c.results('R08 RAFFLE', [('BUYER ONE', buyer), ('BUYER ALL BOUGHT', c.rmul(buyer, (bought, 1))), ('ORGANIZER ONE', org), ('ORGANIZER ALL SOLD', c.rmul(org, (total, 1)))], ['BUYER=PRIZE/TOTAL-PRICE', 'MULTIPLY UNROUNDED E', 'ONE PRIZE; NO OTHER COSTS', 'PRIZE VALUE ASSUMED COST', 'ROUND MONEY TO 2 PLACES'], default_places=2)



