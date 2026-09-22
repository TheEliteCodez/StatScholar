# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Normal axis drawing; helpers load back through the dispatcher.
import STCORE as c


def axis_lines(mean,sd,start,observations=()):
    def labels(values):
        line=''
        for value in values:
            gap=10-len(value)
            line+=' '*(gap//2)+value+' '*(gap-gap//2)
        return line.rstrip()
    ticks=range(start,start+3)
    values=[c.fixed(c.call('STNORM','x_value',(z,1),mean,sd),4).rstrip('0').rstrip('.') for z in ticks]
    keys=[]
    for i,value in enumerate(values):
        if len(value)>9:
            name=chr(65+i)
            keys.append(name+'='+value)
            values[i]=name
    marks=[' ']*30
    for x in observations:
        z=c.call('STNORM','z_value',x,mean,sd)
        offset=c.rdiv(c.call('STNORM','sub',z,(start,1)),(2,1))
        if c.compare_exact(offset,0)>=0 and c.compare_exact(offset,1)<=0:
            marks[4+int(round(20*offset[0]/offset[1]))]='*'
    axis='    |---------|---------|'
    lines=['z: '+str(start)+' TO '+str(start+2),labels([str(z) for z in ticks]),axis,axis,labels(values),'x: SAME TICKS AS z']
    if observations: lines.insert(0,''.join(marks).rstrip() or 'NO OBSERVATION IN THIS PANEL')
    return lines+keys


def show_axes(title,mean,sd,observations=()):
    if not sd[0]:
        c.view(title,['SD=0: z AXIS UNDEFINED','ALL MODEL VALUES EQUAL MEAN']);return
    lines=[]
    for start in (-3,-1,1):
        panel=axis_lines(mean,sd,start,observations)
        lines+=panel+['']*((-len(panel))%c.VIEW_LINES)
    c.view(title,lines)
