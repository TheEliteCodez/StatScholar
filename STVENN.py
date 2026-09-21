# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Counts, Venn regions and repeated selections; loaded on demand.
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


def regions(total,a,b,both):
    values=(both,a-both,b-both,total-a-b+both)
    if total<=0 or min(values)<0: raise ValueError('CHECK TOTAL / GROUP / OVERLAP COUNTS')
    return values


def venn_session():
    total=c.read_int('TOTAL PEOPLE / ITEMS: ')
    a=c.read_int('COUNT A (INCLUDES BOTH): ')
    b=c.read_int('COUNT B (INCLUDES BOTH): ')
    both=c.read_int('COUNT BOTH A AND B: ')
    both,only_a,only_b,neither=regions(total,a,b,both)
    while True:
        key=c.menu('VENN / SAME COUNTS',[('1','REGIONS / DRAWING STEPS'),('2','CONTINGENCY TABLE'),('3','OR / ONLY / GIVEN'),('4','ALL SELECTED FROM A'),('5','ALL SELECTED FROM B'),('6','CHANGE COUNTS')])
        if key=='0': return
        if key=='6':
            total=c.read_int('TOTAL PEOPLE / ITEMS: ');a=c.read_int('A INCLUDING BOTH: ');b=c.read_int('B INCLUDING BOTH: ');both=c.read_int('BOTH: ')
            both,only_a,only_b,neither=regions(total,a,b,both);continue
        if key=='1':
            c.results('VENN COUNTS',[('A ONLY',only_a),('BOTH',both),('B ONLY',only_b),('NEITHER',neither),('A OR B',a+b-both)],['TWO OVERLAPPING CIRCLES INSIDE TOTAL RECTANGLE','BOTH IN OVERLAP; NEITHER OUTSIDE CIRCLES','n(A OR B)=n(A)+n(B)-n(BOTH)',str(a)+'+'+str(b)+'-'+str(both)+'='+str(a+b-both)])
        elif key=='2':
            c.call('STSTUDY','definition_pages','CONTINGENCY COUNTS','COLUMNS: B, NOT B, TOTAL. ROW A: '+str(both)+', '+str(only_a)+', '+str(a)+'. ROW NOT A: '+str(only_b)+', '+str(neither)+', '+str(total-a)+'. TOTAL ROW: '+str(b)+', '+str(total-b)+', '+str(total)+'. A BUT NOT B IS ROW A / COLUMN NOT B: '+str(only_a)+'.')
        elif key=='3':
            c.results('VENN PROBABILITIES',[('A OR B',c.ratio(a+b-both,total)),('A BUT NOT B',c.ratio(only_a,total)),('B BUT NOT A',c.ratio(only_b,total)),('BOTH',c.ratio(both,total)),('NEITHER',c.ratio(neither,total)),('B GIVEN A',c.ratio(both,a) if a else 'UNDEFINED'),('A GIVEN B',c.ratio(both,b) if b else 'UNDEFINED')],['OR: (A+B-BOTH)/TOTAL','GIVEN: BOTH / GIVEN GROUP'])
        else: selection_session(total,a if key=='4' else b)


def selection_question():
    key=c.menu('ALL SELECTED: REPLACEMENT?',[('1','WITH REPLACEMENT'),('2','WITHOUT REPLACEMENT'),('3','COMPARE BOTH METHODS')])
    if key!='0': selection_session(model=key)
