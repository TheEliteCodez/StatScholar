# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STDATA - loaded only when needed.
import STCORE
from STDMATH import *
SUMMARY_KEYS = ('n', 'SUM', 'MEAN', 'SAMPLE SD Sx', 'SAMPLE VARIANCE s^2', 'MIN', 'Q1', 'MEDIAN', 'Q3', 'MAX', 'MODE', 'RANGE', 'IQR', 'MIDRANGE')


def summary_results(stats, title='DATA > RAW > SUMMARY', population=False):
    keys=list(SUMMARY_KEYS)
    if population:
        keys[3:5]=['POPULATION SD','POPULATION VARIANCE']
    answers=[(k,stats[k]) for k in keys]
    if stats['n']>1:
        answers.extend((k,stats[k]) for k in ('LOWER FENCE','UPPER FENCE','LOW WHISKER','HIGH WHISKER','OUTLIERS'))
    sd=stats['POPULATION SD' if population else 'SAMPLE SD Sx']
    if sd!='DNE':
        distance=STCORE.as_ratio(str(2*sd))
        answers.extend([('MIN USUAL',sub(stats['MEAN'],distance)),('MAX USUAL',STCORE.radd(stats['MEAN'],distance))])
    STCORE.results(title,answers,['MEAN=SUM/n','VAR=SUM((x-MEAN)^2)/'+('n' if population else '(n-1)'),
        'QUARTILES: MEDIANS OF HALVES','ODD n: OMIT CENTER FROM HALVES','MODE: >2 MODES OR NO PEAK = DNE',
        'IQR OUTLIERS AND 2-SD UNUSUAL ARE DIFFERENT'])


def data_normal(stats,first,population=False):
    sd=stats['POPULATION SD' if population else 'SAMPLE SD Sx']
    if sd=='DNE':
        STCORE.view('DATA',['NEED TWO VALUES FOR SAMPLE SD']);return
    STCORE.call('STNORM','normal_session',stats['MEAN'],STCORE.as_ratio(str(sd)),first,
        stats['POPULATION VARIANCE' if population else 'SAMPLE VARIANCE s^2'])


def choose_population(population):
    key=STCORE.menu('VARIANCE / SD USE',[('1','SAMPLE (n-1)'),('2','POPULATION (n)')])
    return population if key=='0' else key=='2'


def raw_session(values=None):
    values = read_raw() if values is None else values
    stats = descriptive(values)
    population=False
    summary_results(stats)
    while True:
        key = STCORE.menu('DATA > RAW > NEXT', [('1','FULL SUMMARY'),('2','Z-SCORE A VALUE'),('3','USUAL / UNUSUAL'),('4','OUTLIERS / FENCES'),('5','GRAPH THIS DATA'),('6','COMPARE ANOTHER LIST'),('7','CHANGE DATA'),('8','SAMPLE / POPULATION'),('9','EDIT ONE VALUE'),('10','CHECK ALL VALUES')])
        if key=='0': return
        if key=='1': summary_results(stats,population=population)
        elif key in ('2','3'): data_normal(stats,'1' if key=='2' else '5',population)
        elif key=='4': STCORE.call('STGRAPH','boxplot_data',values)
        elif key=='5': STCORE.call('STGRAPH','graph_data',values)
        elif key=='6': compare_session(values)
        elif key=='7':
            values = read_raw()
            stats = descriptive(values)
            summary_results(stats,population=population)
        elif key=='8': population=choose_population(population)
        elif key=='9':
            values=edit_raw(values);stats=descriptive(values)
            summary_results(stats,population=population)
        elif key=='10':
            rule=STCORE.call('STNORM','boundary_rule')
            if rule is not None: STCORE.call('STZLIST','z_list',stats['MEAN'],STCORE.as_ratio(str(stats['POPULATION SD' if population else 'SAMPLE SD Sx'])),stats['POPULATION VARIANCE' if population else 'SAMPLE VARIANCE s^2'],rule,values) if stats['n']>1 or population else STCORE.view('DATA',['NEED TWO VALUES FOR SAMPLE SD'])


def comparison(a,b):
    return descriptive(a), descriptive(b)

def compare_session(a=None, boxes=False):
    a = read_raw('DATA > COMPARE > A') if a is None else a
    b = read_raw('DATA > COMPARE > B')
    sa,sb=comparison(a,b)
    show=True
    population=False
    while True:
        if show and boxes:
            STCORE.results('GRAPH > SAME SCALE', [('AXIS MIN',min_exact(a[0],b[0])),('AXIS MAX',max_exact(a[-1],b[-1]))], ['USE SAME AXIS AND TICK SPACING'])
            STCORE.call('STGRAPH','boxplot_data',a,'GRAPH > BOX A')
            STCORE.call('STGRAPH','boxplot_data',b,'GRAPH > BOX B')
        elif show:
            summary_results(sa,'DATA > COMPARE > A',population)
            summary_results(sb,'DATA > COMPARE > B',population)
            for title, keys in [('CENTERS',('MEAN','MEDIAN')),('SPREAD',(('POPULATION SD','POPULATION VARIANCE','IQR','RANGE') if population else ('SAMPLE SD Sx','SAMPLE VARIANCE s^2','IQR','RANGE')))]:
                STCORE.results('DATA > COMPARE > '+title, [(name+' '+label,stats[label]) for label in keys for name,stats in [('A',sa),('B',sb)]], ['COMPARE EACH MEASURE IN CONTEXT'])
        key=STCORE.menu('DATA > COMPARE', [('1','SHOW AGAIN'),('2','CHANGE SET A'),('3','CHANGE SET B'),('4','SIDE-BY-SIDE BOXPLOTS'),('5','COMPARE CENTERS / SPREAD'),('6','USUAL / UNUSUAL BOTH SETS'),('7','SAMPLE / POPULATION')])
        if key=='0': return
        show=key in ('1','2','3','4','5','7')
        if key=='7': population=choose_population(population)
        if key=='6':
            rule=STCORE.call('STNORM','boundary_rule')
            if rule is not None:
                STCORE.call('STNORM','usual_data',a,sa,'USUAL > A',rule,population)
                STCORE.call('STNORM','usual_data',b,sb,'USUAL > B',rule,population)
        if key=='4': boxes=True
        if key=='5': boxes=False
        if key=='2':
            a=read_raw('DATA > COMPARE > A');sa=descriptive(a)
        if key=='3':
            b=read_raw('DATA > COMPARE > B');sb=descriptive(b)

def frequency_data_session():
    rows=read_frequency_rows()
    population=False
    stats=weighted_stats(rows)
    summary_results(stats,'DATA > FREQUENCY',population)
    while True:
        key=STCORE.menu('DATA > FREQUENCY > NEXT',[('1','FULL SUMMARY / FENCES'),('2','HISTOGRAM / GROUP CLASSES'),('3','CHANGE DATA'),('4','RELATIVE / CUM / EVENT'),('5','Z-SCORE A VALUE'),('6','USUAL / UNUSUAL'),('7','EDIT ONE ROW'),('8','SAMPLE / POPULATION'),('9','CHECK ALL VALUES')])
        if key=='0': return
        if key=='3': rows=read_frequency_rows()
        if key=='7': rows=edit_frequency(rows)
        if key in ('3','7'): stats=weighted_stats(rows)
        if key=='8': population=choose_population(population)
        if key in ('1','3','7','8'): summary_results(stats,'DATA > FREQUENCY',population)
        elif key=='2': STCORE.call('STHIST','histogram_session',None,False,rows)
        elif key=='4': STCORE.call('STQUIZ','frequency_tools',rows)
        elif key in ('5','6'): data_normal(stats,'1' if key=='5' else '5',population)
        elif key=='9':
            rule=STCORE.call('STNORM','boundary_rule')
            if rule is not None: STCORE.call('STNORM','usual_data',[x for x,f in rows if f>0],stats,'FREQUENCY OBSERVATIONS',rule,population)
