# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Context-sensitive AND, OR and GIVEN helper.
import STCORE as c


def choose_probability(context):
    while True:
        word=c.choice_pages('WHICH WORDS MATCH?',(
            (('GIVEN THAT / AMONG THOSE','given'),('AND / BOTH HAPPEN','and'),('OR / EITHER HAPPENS','or'),('AT LEAST ONE','one'),('NONE / NOT / DOES NOT','not')),
            (('EXACTLY / AT MOST / AT LEAST','count'),('ALL 2, 3, ... SELECTED','all'),('VENN / TWO OVERLAPPING GROUPS','venn'),('DICE / COINS / CARDS','dice'),('AVERAGE MONEY WON OR LOST','money'))))
        if word is None: return
        if word in ('given','and','or'): probability_words(word)
        elif word=='one': c.call('STWORDS','word_route','one',context)
        elif word=='not': complement_words(context)
        elif word=='count':
            key=c.menu('WHAT NUMBERS DO YOU HAVE?', [('1','n TRIALS AND ONE CHANCE p'),('2','X VALUES AND P(X) TABLE'),('3','DRAW WITHOUT REPLACEMENT')])
            if key=='1': c.call('STBWORD','wording_session')
            elif key=='2': c.call('STCOUNT','distribution_session')
            elif key=='3': c.call('STSAMPLE','sample_word_session')
        elif word=='all': c.call('STVENN','selection_session')
        elif word=='venn': c.call('STVENN','venn_session')
        elif word=='dice': context['experiment_tasks']()
        elif word=='money':
            if 'money_tasks' in context: context['money_tasks']()
            else: c.call('STCOUNT','money_session')


def probability_words(word):
    key=c.menu('PROB > WHAT IS GIVEN?',[('1','COUNTS IN ROWS AND COLUMNS'),('2','P(A), P(B), P(BOTH)'),('3','CHANCES, NO COUNT TABLE'),('4','DICE EVENTS'),('5','TOTAL, GROUP A, B AND BOTH'),('6','EXPLAIN WORDING')])
    if key=='6':
        c.view('WORDS',[{'given':'GIVEN: USE GIVEN GROUP AS DENOMINATOR','and':'AND: BOTH CONDITIONS','or':'OR: EITHER; COUNT OVERLAP ONCE'}[word]]);return
    if key=='1': c.call('STPROB','two_way_session')
    elif key=='2': c.call('STPROB','supplied_session')
    elif key=='4': c.call('STDICE','dice_session',word if word in ('and','or') else None)
    elif key=='5': c.call('STVENN','venn_session')
    elif key=='3':
        if word=='given': c.call('STPROB','solver_conditional')
        elif word=='or':
            if c.yesno('CAN BOTH EVENTS OCCUR?'): c.call('STPROB','solver_general_or')
            else: c.call('STPROB','solver_mut_or')
        elif c.yesno('ARE THE EVENTS INDEPENDENT?'): c.call('STPROB','solver_indep_and')
        else: c.call('STPROB','solver_general_and')


def complement_words(context):
    key=c.menu('WHAT INFORMATION IS GIVEN?', [('1','CHANCE OF OPPOSITE EVENT'),('2','COUNTS IN A TABLE'),('3','NONE IN n TRIALS'),('4','DICE / COINS / CARDS')])
    if key=='1': c.call('STPROB','solver_complement')
    elif key=='2': c.call('STPROB','two_way_session')
    elif key=='3':
        c.call('STBWORD','wording_session','none')
    elif key=='4': context['experiment_tasks']()
