# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Empirical rule solver.
import STCORE as c


def empirical_percent(k, region='within'):
    within=((68,1),(95,1),(997,10))[k-1]
    outside=c.call('STNORM','sub',(100,1),within)
    return within if region=='within' else outside if region=='outside' else c.rdiv(outside,(2,1))


def empirical_session(mean=None,sd=None):
    while True:
        key=c.menu('GRAPH > EMPIRICAL RULE',[(str(i),label) for i,label in enumerate(('WITHIN 1 SD','WITHIN 2 SD','WITHIN 3 SD','OUTSIDE 1 SD','OUTSIDE 2 SD','OUTSIDE 3 SD','ONE TAIL','ENTER / CHANGE MEAN AND SD','BETWEEN SD MARKS'),1)])
        if key=='0': return
        if key=='8':
            mean=c.read_exact('MEAN: ');sd=c.read_exact('SD: ');continue
        if key=='9':
            low=c.read_int('LOWER z (-3..3): ');high=c.read_int('UPPER z (-3..3): ')
            marks={-3:.15,-2:2.5,-1:16,0:50,1:84,2:97.5,3:99.85}
            if low not in marks or high not in marks or low>high: raise ValueError('USE ORDERED INTEGER z -3..3')
            answers=[('APPROX PERCENT',c.as_ratio(str(marks[high]-marks[low])))]
            if mean is not None: answers += [('LOW x',c.call('STNORM','x_value',(low,1),mean,sd)),('HIGH x',c.call('STNORM','x_value',(high,1),mean,sd))]
            c.results('EMPIRICAL > BETWEEN',answers,['APPROX NORMAL ONLY','OPTION 8 ENTERS MEAN / SD']);continue
        k=(int(key)-1)%3+1
        region='within' if int(key)<=3 else 'outside'
        if key=='7':
            k=c.read_size('HOW MANY SD (1..3): ',3)
            side=c.menu('GRAPH > TAIL',[('1','BELOW -k SD'),('2','ABOVE +k SD')])
            if side=='0': continue
            region='tail'
        label=(('BELOW -' if side=='1' else 'ABOVE +')+str(k)+' SD') if region=='tail' else region.upper()+' '+str(k)+' SD'
        answers=[('APPROX PERCENT',empirical_percent(k,region)),('REGION',label)]
        if mean is not None:
            if region=='tail':
                answers.append(('BELOW x' if side=='1' else 'ABOVE x',c.call('STNORM','x_value',(-k if side=='1' else k,1),mean,sd)))
            else:
                answers += [('LOW x',c.call('STNORM','x_value',(-k,1),mean,sd)),('HIGH x',c.call('STNORM','x_value',(k,1),mean,sd))]
        c.results('GRAPH > EMPIRICAL ANSWER',answers,['PERCENT UNITS, NOT PROBABILITY', 'APPROX NORMAL / BELL-SHAPED ONLY', 'OPTION 8 ENTERS MEAN / SD','68 / 95 / 99.7 WITHIN', 'OUTSIDE=100-WITHIN', 'ONE TAIL=OUTSIDE/2'])
