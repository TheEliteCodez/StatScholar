# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Question starters and wizards; context globals live on STREF.
import STCORE
import STREF


def question_starters():
    items = [(str(i + 1), STREF.STARTERS[i][0]) for i in range(len(STREF.STARTERS))]
    while True:
        key = STCORE.menu('QUESTION STARTERS', items, page_size=6)
        if key == '0':
            return
        phrase, qid = STREF.STARTERS[int(key) - 1]
        STCORE.view('QUESTION WORDING', [phrase, '', 'MATRIX TYPE:', qid, STREF.GUIDES[qid][0]])
        STREF.show_identified(qid)


def wizard_raw_data():
    STCORE.call('STDATA','raw_session')


def wizard_counting():
    STCORE.heading('COUNTING WIZARD')
    if STCORE.yesno('DOES IT SAY CHOOSE / SELECT / GROUP / PAIR?'):
        if STCORE.yesno('DOES ORDER MATTER?'):
            STREF.show_identified('C04')
        else:
            STREF.show_identified('C03')
        return
    if STCORE.yesno('DOES IT SAY ARRANGE / RANK / ORDER / POSITIONS?'):
        STREF.show_identified('C04')
        return
    if STCORE.yesno('DOES IT ASK TOTAL POSSIBLE OUTCOMES FROM STAGES?'):
        STREF.show_identified('C01')
        return
    STCORE.view('NOT IDENTIFIED', ['TRY QUESTION STARTERS.', 'ASK YOURSELF WHETHER', 'ORDER MATTERS.'])


def wizard_formula():
    while True:
        STCORE.heading('FORMULA WIZARD')
        print('WHICH LOOKS CLOSE?')
        print('1 (x-mean)/SD')
        print('2 mean+2(SD)')
        print('3 Q3-Q1')
        print('4 f/n')
        print('5 P(A and B)/P(B)')
        print('6 A+B-BOTH')
        print('7 nCr*p^x*(1-p)^(n-x)')
        print('8 SUM[x*P(x)]')
        print('9 n*p')
        print('A sqrt(n*p*(1-p))')
        print('0 BACK')
        c = input('> ').upper()
        if c == '1':
            STREF.show_identified('S12')
        elif c == '2':
            STREF.show_identified('S10')
        elif c == '3':
            STREF.show_identified('S08')
        elif c == '4':
            STREF.show_identified('F02')
        elif c == '5':
            STREF.show_identified('P07')
        elif c == '6':
            STREF.show_identified('P04')
        elif c == '7':
            STREF.show_identified('B07')
        elif c == '8':
            STREF.show_identified('R02')
        elif c == '9':
            STREF.show_identified('B08')
        elif c == 'A':
            STREF.show_identified('B09')
        elif c == '0':
            return
