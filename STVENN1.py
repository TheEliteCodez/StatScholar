# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# "All selected" solver and its menu entry.
import STCORE as c


def all_probability(total,good,n,replaced):
    if total<1 or good<0 or good>total or n<0 or (not replaced and n>total):
        raise ValueError('CHECK POPULATION / GROUP / DRAW COUNTS')
    answer=(1,1)
    for i in range(n):
        if not replaced and i>=good: return (0,1)
        answer=c.rmul(answer,c.ratio(good if replaced else good-i,total if replaced else total-i))
    return answer


def selection_session(total=None,good=None,model=None):
    if total is None:
        total=c.read_int('POPULATION TOTAL: ')
        good=c.read_int('NUMBER IN TARGET GROUP: ')
    while True:
        n=c.read_int('HOW MANY SELECTED: ')
        answers=[]
        if model in (None,'2','3'): answers.append(('WITHOUT REPLACEMENT',all_probability(total,good,n,False) if n<=total else 'NOT APPLICABLE: n>N'))
        if model in (None,'1','3'): answers.append(('WITH REPLACEMENT',all_probability(total,good,n,True)))
        answers += [('SAMPLE FRACTION',c.ratio(n,total)),('WITHIN 5% GUIDELINE','YES' if 20*n<=total else 'NO')]
        c.results('ALL SELECTED IN GROUP',answers,
            ['WITHOUT: MULTIPLY (K-i)/(N-i), i=0..n-1',
             'WITH: (K/N)^n', 'N='+str(total)+' K='+str(good)+' n='+str(n),
             '5% CHECK: n/N <= .05',
             'IF WITHIN 5%, (K/N)^n APPROXIMATES THE WITHOUT-REPLACEMENT ANSWER.',
             'WITHOUT REPLACEMENT REMAINS DEPENDENT. EXACT ANSWER SHOWN ABOVE.'])
        key=c.menu('SAME POPULATION / GROUP',[('1','CHANGE NUMBER SELECTED'),('2','CHANGE POPULATION / GROUP')])
        if key=='0': return
        if key=='2':
            total=c.read_int('POPULATION TOTAL: ');good=c.read_int('NUMBER IN TARGET GROUP: ')


def selection_question():
    key=c.menu('ALL SELECTED: REPLACEMENT?',[('1','WITH REPLACEMENT'),('2','WITHOUT REPLACEMENT'),('3','COMPARE BOTH METHODS')])
    if key!='0': selection_session(model=key)
