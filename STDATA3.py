# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Compare-two-lists and frequency-table sessions.
import STCORE as c


def compare_session(a=None, boxes=False):
    a = c.call('STDMATH','read_raw','DATA > COMPARE > A') if a is None else a
    b = c.call('STDMATH','read_raw','DATA > COMPARE > B')
    sa=c.call('STDMATH','descriptive',a)
    sb=c.call('STDMATH','descriptive',b)
    show=True
    population=False
    while True:
        if show and boxes:
            c.results('GRAPH > SAME SCALE', [('AXIS MIN',c.call('STDMATH','min_exact',a[0],b[0])),('AXIS MAX',c.call('STDMATH','max_exact',a[-1],b[-1]))], ['USE SAME AXIS AND TICK SPACING'])
            c.call('STGRAPH','boxplot_data',a,'GRAPH > BOX A')
            c.call('STGRAPH','boxplot_data',b,'GRAPH > BOX B')
        elif show:
            c.call('STDATA','summary_results',sa,'DATA > COMPARE > A',population)
            c.call('STDATA','summary_results',sb,'DATA > COMPARE > B',population)
            for title, keys in [('CENTERS',('MEAN','MEDIAN')),('SPREAD',(('POPULATION SD','POPULATION VARIANCE','IQR','RANGE') if population else ('SAMPLE SD Sx','SAMPLE VARIANCE s^2','IQR','RANGE')))]:
                c.results('DATA > COMPARE > '+title, [(name+' '+label,stats[label]) for label in keys for name,stats in [('A',sa),('B',sb)]], ['COMPARE EACH MEASURE IN CONTEXT'])
        key=c.menu('DATA > COMPARE', [('1','SHOW AGAIN'),('2','CHANGE SET A'),('3','CHANGE SET B'),('4','SIDE-BY-SIDE BOXPLOTS'),('5','COMPARE CENTERS / SPREAD'),('6','USUAL / UNUSUAL BOTH SETS'),('7','SAMPLE / POPULATION')])
        if key=='0': return
        show=key in ('1','2','3','4','5','7')
        if key=='7': population=c.call('STDATA','choose_population',population)
        if key=='6':
            rule=c.call('STNORM','boundary_rule')
            if rule is not None:
                c.call('STNORM','usual_data',a,sa,'USUAL > A',rule,population)
                c.call('STNORM','usual_data',b,sb,'USUAL > B',rule,population)
        if key=='4': boxes=True
        if key=='5': boxes=False
        if key=='2':
            a=c.call('STDMATH','read_raw','DATA > COMPARE > A');sa=c.call('STDMATH','descriptive',a)
        if key=='3':
            b=c.call('STDMATH','read_raw','DATA > COMPARE > B');sb=c.call('STDMATH','descriptive',b)


def frequency_data_session():
    rows=c.call('STDMATH','read_frequency_rows')
    population=False
    stats=c.call('STDMATH','weighted_stats',rows)
    c.call('STDATA','summary_results',stats,'DATA > FREQUENCY',population)
    while True:
        key=c.menu('DATA > FREQUENCY > NEXT',[('1','FULL SUMMARY / FENCES'),('2','HISTOGRAM / GROUP CLASSES'),('3','CHANGE DATA'),('4','RELATIVE / CUM / EVENT'),('5','Z-SCORE A VALUE'),('6','USUAL / UNUSUAL'),('7','EDIT ONE ROW'),('8','SAMPLE / POPULATION'),('9','CHECK ALL VALUES')])
        if key=='0': return
        if key=='3': rows=c.call('STDMATH','read_frequency_rows')
        if key=='7': rows=c.call('STDMATH','edit_frequency',rows)
        if key in ('3','7'): stats=c.call('STDMATH','weighted_stats',rows)
        if key=='8': population=c.call('STDATA','choose_population',population)
        if key in ('1','3','7','8'): c.call('STDATA','summary_results',stats,'DATA > FREQUENCY',population)
        elif key=='2': c.call('STHIST','histogram_session',None,False,rows)
        elif key=='4': c.call('STQUIZ','frequency_tools',rows)
        elif key in ('5','6'): c.call('STDATA','data_normal',stats,'1' if key=='5' else '5',population)
        elif key=='9':
            rule=c.call('STNORM','boundary_rule')
            if rule is not None: c.call('STNORM','usual_data',[x for x,f in rows if f>0],stats,'FREQUENCY OBSERVATIONS',rule,population)
