# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Relative-position (compare z-scores) solver.
import STCORE as c


def relative_session():
    inputs=[]
    for name in ('A','B'):
        c.heading('RELATIVE POSITION '+name)
        inputs.append((c.read_exact('x: '),c.read_exact('MEAN: '),c.read_exact('SD: ')))
    while True:
        vals=[c.call('STNORM','z_value',*entry) for entry in inputs]
        if any(isinstance(z,str) for z in vals): higher='UNDEFINED: SD=0'
        else:
            cmp=c.compare_exact(vals[0],vals[1]);higher='A' if cmp>0 else 'B' if cmp<0 else 'TIE'
        c.results('GRAPH > RELATIVE POSITION',[('z A',vals[0]),('z B',vals[1]),('HIGHER RELATIVE',higher)],['COMPARE Z-SCORES, NOT RAW x','HIGHER IS NOT ALWAYS BETTER'])
        while True:
            key=c.menu('RELATIVE > NEXT',[('1','LABEL BOTH x / Z AXES'),('2','CHANGE A'),('3','CHANGE B')])
            if key=='0': return
            if key in ('2','3'):
                inputs[int(key)-2]=(c.read_exact('x: '),c.read_exact('MEAN: '),c.read_exact('SD: '));break
            for name,(x,mean,sd) in zip(('A','B'),inputs):
                c.call('STNORM','show_axes','AXES '+name+' (* = OBSERVATION)',mean,sd,(x,))
                c.results('AXES '+name,[('z='+str(z)+' x',c.call('STNORM','x_value',(z,1),mean,sd)) for z in range(-3,4)]+[('OBSERVATION x',x),('OBSERVATION z',c.call('STNORM','z_value',x,mean,sd))],['DRAW BELL ONLY IF SD>0'])
