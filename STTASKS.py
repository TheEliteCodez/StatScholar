# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Home-menu task routes, loaded only when a task is dispatched.
import STCORE


def data_tasks(g):
    while True:
        key=STCORE.menu('DATA / STATISTICS',[('1','RAW LIST OF NUMBERS'),('2','VALUE + FREQUENCY'),('3','X + P(X)'),('4','ROW / COLUMN TABLE'),('5','CATEGORY COUNTS'),('6','COMPARE TWO DATA SETS'),('7','PERCENT OF TOTAL')],page_size=7)
        if key=='0': return
        routes={'1':('STDATA','raw_session'),'2':('STDATA','frequency_data_session'),'3':('STCOUNT','distribution_session'),'4':('STPROB','two_way_session'),'5':('STPROB','category_session'),'6':('STDATA','compare_session'),'7':('STQUIZ','percent_session')}
        if key in routes: STCORE.call(*routes[key])


def table_tasks(g):
    g['data_tasks']()


def graph_tasks(g):
    while True:
        key=STCORE.menu('GRAPHS / NORMAL',[('1','Z / USUAL / EMPIRICAL RULE'),('2','BOXPLOT'),('3','DOTPLOT'),('4','HISTOGRAM'),('5','INTERPRET SHAPE / NORMALITY'),('6','OUTLIERS'),('7','COMPARE RELATIVE POSITION')])
        if key=='0': return
        if key=='5': STCORE.call('STGRAPH','shape_guide')
        elif key=='6':
            choice=STCORE.menu('GRAPH > OUTLIERS',[('1','FROM RAW DATA'),('2','GIVEN Q1 AND Q3')])
            if choice=='1': STCORE.call('STGRAPH','raw_outliers')
            elif choice=='2': STCORE.call('STDESC','solver_outlier')
        elif key!='0': STCORE.call(*{'1':('STNORM','normal_session'),'2':('STGRAPH','boxplot_session'),'3':('STGRAPH','dotplot_session'),'4':('STHIST','histogram_session'),'7':('STNORM','relative_session')}[key])


def experiment_tasks(g, word=None):
    while True:
        key=STCORE.menu('PROB > RANDOM EXPERIMENT',[('1','ONE / MULTIPLE DICE'),('2','DIE + COIN'),('3','COIN FLIPS'),('4','52 CARDS'),('5','ROULETTE'),('6','SPINNER')],page_size=6)
        if key=='0': return
        if key=='1': STCORE.call('STDICE','dice_session',word)
        elif key=='3': STCORE.call('STBWORD','wording_session',word,None,(1,2))
        elif key!='0': STCORE.call('STEXPER','experiment_session',{'2':'coin','4':'cards','5':'roulette','6':'spinner'}[key],word)
        word=None
