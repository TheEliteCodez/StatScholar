# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Probability/money task menus, loaded only when selected.
import STCORE


def probability_tasks(g):
    while True:
        key=STCORE.menu('PROB: WHAT DOES IT ASK?',[
            ('1','HOW MANY OUT OF THE TOTAL?'),
            ('2','GIVEN P(A), P(B), P(BOTH)'),
            ('3','AT LEAST ONE OCCURS'),
            ('4','ROLL DICE / FLIP / DRAW CARD'),
            ('5','TABLE OF x AND ITS CHANCE'),
            ('6','AVERAGE WIN / LOSS / PAYOUT'),
            ('7','IS THIS PROBABILITY VALID?'),
            ('8','COUNTS IN ROWS AND COLUMNS'),
            ('9','FILL IN A MISSING CHANCE'),
            ('10','TOTAL, GROUP A, B AND BOTH'),
            ('11','ALL SELECTED ARE IN A GROUP'),
            ('12','QUIZ 4: DICE / SURVEY'),
            ('13','QUIZ 5: TABLE / BINOMIAL'),('14','DEFECTIVE ITEMS / BOX'),('15','HELP ME CHOOSE A SOLVER')])
        if key=='0': return
        if key=='15':
            STCORE.call('STPWORD','choose_probability',{'experiment_tasks':g['experiment_tasks'],'find_tasks':g['find_tasks'],'money_tasks':g['money_tasks']})
            continue
        if key=='3': STCORE.call('STWORDS','word_route','one',{'experiment_tasks':g['experiment_tasks'],'find_tasks':g['find_tasks'],'money_tasks':g['money_tasks']})
        elif key=='4': g['experiment_tasks']()
        elif key=='6': g['money_tasks']()
        elif key=='14': STCORE.call('STSAMPLE','box_session')
        elif key!='0':
            routes={'1':('STPROB','solver_basic_prob'),'2':('STPROB','supplied_session'),'3':('STPROB','solver_at_least_one'),'5':('STCOUNT','distribution_session'),'7':('STPROB','valid_probability'),'8':('STPROB','two_way_session'),'9':('STCOUNT','missing_probability'),'10':('STVENN','venn_session'),'11':('STVENN','selection_question'),'12':('STQUIZ4','quiz_menu'),'13':('STQUIZ5','quiz_menu')}
            STCORE.call(*routes[key])


def money_tasks(g):
    while True:
        key=STCORE.menu('PROB > EXPECTED / MONEY',[('1','X + P(X): EXPECTED VALUE'),('2','PRIZES / PAYOFFS'),('3','INSURER PROFIT'),('4','RAFFLE'),('5','COUNT / CHOOSE / ARRANGE')])
        if key=='0': return
        if key=='5': g['reference_call']('wizard_counting')
        elif key!='0': STCORE.call('STCOUNT',{'1':'distribution_session','2':'payoff_tasks','3':'insurance_session','4':'raffle_session'}[key])
