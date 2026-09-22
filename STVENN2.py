# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Two-circle Venn / contingency solver.
import STCORE as c


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
        else: c.call('STVENN','selection_session',total,a if key=='4' else b)
