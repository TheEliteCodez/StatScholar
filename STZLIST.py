# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Multiple observations with one mean/SD; loaded only for this report.
import STCORE as c


def z_list(mean,sd,variance,inclusive=False,values=None):
    import STNORM as normal
    owned=values is None
    values=values if values is not None else [c.read_exact('OBSERVATION x: ') for i in range(c.read_size('HOW MANY OBSERVATIONS: ',c.MAX_ROWS))]
    while True:
        key=c.menu('SAVED OBSERVATIONS',[('1','Z / LOW-HIGH REPORT'),('2','x AND z AXES / MARK VALUES'),('3','EDIT OBSERVATION'),('4','BOUNDARY RULE')])
        if key=='0': return
        if key=='3':
            if not owned: values=list(values);owned=True
            index=c.read_size('OBSERVATION NUMBER: ',len(values))-1
            values[index]=c.read_exact('NEW x: ');continue
        if key=='4':
            rule=normal.boundary_rule()
            if rule is not None: inclusive=rule
            continue
        if key=='1':
            c.results('USUAL LIMITS',[('MIN USUAL',normal.x_value((-2,1),mean,sd)),('MAX USUAL',normal.x_value((2,1),mean,sd))],['BOUNDARIES UNUSUAL' if inclusive else 'BOUNDARIES USUAL'])
            c.paged_results('OBSERVATION REPORT',len(values),lambda i:('x='+c.exact_text(values[i]),'z='+c.answer_text(normal.z_value(values[i],mean,sd))+' '+normal.usual_classification(values[i],mean,variance,inclusive)),['CLASSIFY BEFORE ROUNDING z'])
        else:
            normal.show_axes('ALIGNED AXES (* = OBSERVATION)',mean,sd,values)
            c.results('LABEL AXES',[('z='+str(z)+' x',normal.x_value((z,1),mean,sd)) for z in range(-3,4)],['CENTER MODEL BELL AT z=0','MARK OBSERVATIONS BELOW AT THEIR z'])
            c.paged_results('MARK OBSERVATIONS',len(values),lambda i:('x='+c.exact_text(values[i])+' AT z',normal.z_value(values[i],mean,sd)))
