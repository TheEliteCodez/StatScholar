# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Histogram binning helper.
import STCORE
from STDMATH import *


def grouped_rows(rows,start,width,count,closed_last=False):
    if STCORE.compare_exact(width,0)<=0: raise ValueError('WIDTH MUST BE POSITIVE')
    frequencies=[0]*count
    for x,f in rows:
        offset=STCORE.rdiv(sub(x,start),width)
        index=offset[0]//offset[1]
        if closed_last and index==count and offset[0]==count*offset[1]: index=count-1
        if index<0 or index>=count: raise ValueError('CLASSES DO NOT COVER DATA')
        frequencies[index]+=f
    total=sum(frequencies)
    if total<=0: raise ValueError('NO OBSERVATIONS')
    cumulative=0
    result=[]
    for i,f in enumerate(frequencies):
        low=STCORE.radd(start,STCORE.rmul((i,1),width)); high=STCORE.radd(low,width)
        cumulative+=f
        result.append((low,high,f,STCORE.ratio(f,total),cumulative))
    return result
