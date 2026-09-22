# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Multiple-dice menus; count arithmetic loads back through the dispatcher.
import STCORE


def solver_multi_dice(n=None):
    STCORE.heading('C07 MULTIPLE DICE')
    if n is None: n = STCORE.read_int('HOW MANY FAIR 6-SIDED DICE: ')
    if n < 1:
        raise ValueError('USE AT LEAST ONE DIE')
    while True:
        event = STCORE.menu('C07 EVENT', [('1', 'TOTAL OUTCOMES'), ('2', 'SUM ='), ('3', 'SUM <='), ('4', 'SUM >='), ('5', 'AT LEAST ONE FACE'), ('6', 'EXACTLY r OF A FACE'), ('7', 'NO DICE OF A FACE'), ('8', 'ALL EVEN'), ('9', 'ALL ODD'), ('10', 'AT LEAST ONE EVEN'), ('11', 'ALL SAME'), ('12', 'ALL = ONE FACE'),('13','SUM LESS / MORE / BETWEEN'),('14','CHANGE DICE COUNT'),('15','COUNT OF A FACE: ANY WORDING')])
        if event == '0':
            return
        if event=='14':
            n=STCORE.read_int('NUMBER OF DICE: ');continue
        if event=='13':
            word=STCORE.choice_pages('SUM WORDING',((('LESS THAN','<'),('MORE THAN','>'),('BETWEEN','[]')),))
            if word: word_event(n,word,True)
            continue
        if event=='15':
            face=STCORE.read_int('TARGET FACE (1-6): ')
            if face < 1 or face > 6:
                raise ValueError('FACE MUST BE 1-6')
            ev=STCORE.event_input(binomial=True)
            if ev is None:
                continue
            good=STCORE.call('STBMATH','binomial_exact_event',n,(1,6),ev)
            total=6 ** n
            successful=good[0]*(total//good[1])
            STCORE.results('C07 FACE COUNT',[('P',good),('SUCCESSFUL',str(successful))],['FAIR INDEPENDENT DICE','COUNT FACE '+str(face)+' IN n='+str(n)+' DICE','X~Binomial(n,1/6)'])
            continue
        value = 0
        steps = ['FAIR INDEPENDENT DICE', 'n=' + str(n), 'TOTAL=6^n=' + str(6 ** n)]
        if event in ('2', '3', '4'):
            value = STCORE.read_int('SUM: ')
            steps += ['COUNT ORDERED SUM RESULTS', 'SUM ' + {'2': '=', '3': '<=', '4': '>='}[event] + str(value)]
        if event in ('5', '6', '7', '12'):
            face = STCORE.read_int('TARGET FACE (1-6): ')
            if face < 1 or face > 6:
                raise ValueError('FACE MUST BE 1-6')
            steps.append('FACE=' + str(face))
        if event == '6':
            value = STCORE.read_int('EXACTLY HOW MANY r: ')
        formulas = {'5': 'P=1-(5/6)^n', '6': 'P=nCr*5^(n-r)/6^n', '7': 'P=(5/6)^n', '8': 'P=(1/2)^n', '9': 'P=(1/2)^n', '10': 'P=1-(1/2)^n', '11': 'P=6/6^n', '12': 'P=1/6^n'}
        if event in formulas:
            steps.append(formulas[event])
        if event=='5': steps += ['ONE DIE: P(NOT FACE)=5/6', 'NO TARGET IN n DICE: (5/6)^n', 'AT LEAST ONE=1-P(NONE)']
        good = STCORE.call('STMDICE','dice_event_count',n,event,value)
        answers = [('TOTAL OUTCOMES', str(6 ** n))] if event == '1' else [('P', STCORE.ratio(good, 6 ** n)), ('SUCCESSFUL', str(good))]
        STCORE.results('C07', answers, steps)


def word_event(n,word,sum_only=False):
    key='2' if sum_only else '1' if word=='one' else STCORE.menu('DICE: WHAT IS COUNTED?',[('1','DICE SHOWING ONE FACE'),('2','SUM OF ALL DICE')])
    if key=='0': return
    if key=='1':
        face=STCORE.read_size('TARGET FACE: ',6)
        event=STCORE.call('STBWE','read_event',word)
        if event is None: return
        answer=STCORE.call('STBMATH','binomial_exact_event',n,(1,6),event)
        STCORE.results('DICE SHOWING '+str(face),[('P',answer)],['COUNT TARGET FACES IN '+str(n)+' DICE'])
    else:
        event=STCORE.call('STBWE','read_event',word)
        if event is None: return
        low,high=STCORE.call('STBW2','event_bounds',6*n,event)
        good=max(0,STCORE.call('STMDICE','dice_sum_at_most',n,high)-STCORE.call('STMDICE','dice_sum_at_most',n,low-1))
        STCORE.results('DICE SUM',[('P',STCORE.ratio(good,6**n)),('SUCCESSFUL',good)],['COUNT ORDERED DICE OUTCOMES'])
