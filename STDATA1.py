# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Summary table, normal/z bridge, population toggle.
import STCORE as c

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
        distance=c.as_ratio(str(2*sd))
        answers.extend([('MIN USUAL',c.radd(stats['MEAN'],(-distance[0],distance[1]))),('MAX USUAL',c.radd(stats['MEAN'],distance))])
    c.results(title,answers,['MEAN=SUM/n','VAR=SUM((x-MEAN)^2)/'+('n' if population else '(n-1)'),
        'QUARTILES: MEDIANS OF HALVES','ODD n: OMIT CENTER FROM HALVES','MODE: >2 MODES OR NO PEAK = DNE',
        'IQR OUTLIERS AND 2-SD UNUSUAL ARE DIFFERENT'])


def data_normal(stats,first,population=False):
    sd=stats['POPULATION SD' if population else 'SAMPLE SD Sx']
    if sd=='DNE':
        c.view('DATA',['NEED TWO VALUES FOR SAMPLE SD']);return
    c.call('STNORM','normal_session',stats['MEAN'],c.as_ratio(str(sd)),first,
        stats['POPULATION VARIANCE' if population else 'SAMPLE VARIANCE s^2'])


def choose_population(population):
    key=c.menu('VARIANCE / SD USE',[('1','SAMPLE (n-1)'),('2','POPULATION (n)')])
    return population if key=='0' else key=='2'
