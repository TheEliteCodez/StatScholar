# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Find menus; context globals live on STFIND.
import STCORE
import STFIND


def find_menu():
    while True:
        key=STCORE.menu('FIND A QUESTION',[('1','SEARCH WORDS'),('2','WHAT DOES IT LOOK LIKE?'),('3','WHAT DOES IT ASK?'),('4','HOMEWORK / PRACTICE ID'),('5','GUIDE ID'),('6','TI-84 / FORMULA REFERENCE'),('7','QUESTION STARTERS')])
        if key=='0': return
        if key=='1': STCORE.call('STFIND','search_words')
        elif key=='2': looks_finder()
        elif key=='3': asks_finder()
        elif key=='4': STFIND.question_lookup()
        elif key=='5':
            gid=input('GUIDE ID (ENTER=BROWSE): ').strip().upper()
            if gid in STFIND.GUIDES: STFIND.show_identified(gid)
            else: STFIND.browse_matrix()
        elif key=='6':
            c=STCORE.menu('FIND > REFERENCE',[('1','TI-84 METHODS'),('2','FORMULA WIZARD'),('3','COUNT / CHOOSE / ARRANGE')])
            if c=='1': STFIND.ti84_methods()
            elif c=='2': STFIND.wizard_formula()
            elif c=='3': STFIND.wizard_counting()
        elif key=='7': STFIND.question_starters()


def looks_finder():
    key=STCORE.menu('FIND > WHAT DO YOU SEE?',[('1','LIST OF NUMBERS'),('2','VALUE + FREQUENCY'),('3','ROW / COLUMN TABLE'),('4','X + P(X)'),('5','BELL CURVE'),('6','GRAPH'),('7','STORY / WORD PROBLEM')])
    if key=='1':
        c=STCORE.menu('FIND > LIST OF NUMBERS',[('1','FIND STATISTICS'),('2','FIND OUTLIERS'),('3','MAKE GRAPH'),('4','COMPARE TWO LISTS'),('5','NORMAL / Z')])
        if c=='3': STFIND.graph_tasks()
        elif c!='0': STCORE.call(*{'1':('STDATA','raw_session'),'2':('STGRAPH','raw_outliers'),'4':('STDATA','compare_session'),'5':('STNORM','normal_session')}[c])
    elif key=='2': STCORE.call('STDESC','frequency_session')
    elif key=='3': STCORE.call('STPROB','two_way_session')
    elif key=='4': STCORE.call('STCOUNT','distribution_session')
    elif key=='5': STCORE.call('STNORM','normal_session')
    elif key=='6': STFIND.graph_tasks()
    elif key=='7': asks_finder()


def asks_finder():
    key=STCORE.menu('FIND > WHAT DOES IT ASK?',[('1','MEAN / MEDIAN / SD'),('2','PROBABILITY'),('3','EXACTLY / AT MOST / AT LEAST'),('4','GRAPH / SHAPE'),('5','SAMPLE / STUDY TYPE'),('6','UNUSUAL / Z-SCORE'),('7','EXPECTED VALUE / MONEY')])
    if key=='1': STFIND.data_tasks()
    elif key=='2': STFIND.probability_tasks()
    elif key=='3': STFIND.trial_tasks()
    elif key=='4': STFIND.graph_tasks()
    elif key=='5': STFIND.study_tasks()
    elif key=='6': STCORE.call('STNORM','normal_session')
    elif key=='7': STCORE.call('STCOUNT','payoff_tasks')
