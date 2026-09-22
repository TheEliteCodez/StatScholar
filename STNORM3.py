# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Normal/z main loop and the observation report.
import STCORE as c


def normal_session(mean=None,sd=None,first=None,variance=None):
    inclusive=False
    while True:
        key=first or c.menu('GRAPH > NORMAL / Z',[('1','FIND Z FROM x'),('2','FIND x FROM Z'),('3','LABEL x AND Z AXES'),('4','EMPIRICAL RULE'),('5','USUAL RANGE +/- 2 SD'),('6','CHANGE MEAN / SD'),('7','BOUNDARY RULE < OR <='),('8','SEVERAL x: Z / USUAL / AXES')])
        first=None
        if key=='0': return
        if key=='7':
            rule=c.call('STNORM','boundary_rule')
            if rule is not None: inclusive=rule
            continue
        if key=='4':
            c.call('STNORM','empirical_session',mean,sd)
            continue
        if mean is None or key=='6':
            mean=c.read_exact('MEAN: '); sd=c.read_exact('SD: ')
            variance=None
            if key=='6': continue
        if key=='8':
            c.call('STZLIST','z_list',mean,sd,variance if variance is not None else c.rmul(sd,sd),inclusive)
            continue
        if key=='1':
            x=c.read_exact('x: ')
            c.call('STNORM','observation_report',x,mean,sd,variance,inclusive)
        elif key=='2':
            z=c.read_exact('z: ')
            c.results('GRAPH > FIND x',[('x',c.call('STNORM','x_value',z,mean,sd))],['x=MEAN+z*SD',c.exact_text(mean)+'+'+c.exact_text(z)+'*'+c.exact_text(sd)])
        elif key=='3':
            c.call('STNORM','show_axes','ALIGNED x / z AXES',mean,sd)
            c.results('GRAPH > AXES', [('z='+str(z)+' x',c.call('STNORM','x_value',(z,1),mean,sd)) for z in range(-3,4)],['DRAW BELL CENTERED AT z=0', 'x=MEAN+z*SD; EVEN TICK SPACING'])
            while True:
                raw=input('OBSERVATION x (ENTER=DONE): ').strip()
                if not raw: break
                x=c.as_ratio(raw)
                z=c.call('STNORM','z_value',x,mean,sd)
                if isinstance(z,str):
                    c.view('Z-SCORE',[z]);continue
                c.call('STNORM','show_axes','AXES (* = OBSERVATION)',mean,sd,(x,))
                import math
                v=c.number(z)
                place='AT z='+c.exact_text(z) if v==int(v) else 'BETWEEN z='+str(math.floor(v))+' AND '+str(math.ceil(v))
                c.results('GRAPH > PLACE OBSERVATION',[('z',z),('PLACE',place)],['LEFT OF MEAN IF z<0', 'RIGHT OF MEAN IF z>0'])
        elif key=='5':
            c.results('GRAPH > USUAL RANGE',[('MIN USUAL',c.call('STNORM','x_value',(-2,1),mean,sd)),('MAX USUAL',c.call('STNORM','x_value',(2,1),mean,sd)),('UNUSUAL RULE','x<=MIN OR x>=MAX' if inclusive else 'x<MIN OR x>MAX')],['MEAN +/- 2 SD','CHANGE RULE: NORMAL MENU 7'])
            raw=input('CHECK NUMBER (ENTER=SKIP): ').strip()
            if raw:
                x=c.as_ratio(raw)
                c.call('STNORM','observation_report',x,mean,sd,variance,inclusive)

