# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Two-dice pair matching and counting.
import STCORE


def pair_matches(pair,event):
    kind,op,value=event[:3]
    upper=event[3] if len(event)>3 else 0
    a,b=pair
    if kind=='sumodd': return (a+b)%2==1
    if kind=='sumeven': return (a+b)%2==0
    if kind=='anyeven': return a%2==0 or b%2==0
    if kind=='sum': return STCORE.event_match(a+b,op,value,upper)
    if kind=='first': return STCORE.event_match(a,op,value,upper)
    if kind=='second': return STCORE.event_match(b,op,value,upper)
    if kind=='doubles': return a==b
    if kind=='even': return a%2==0 and b%2==0
    if kind=='odd': return a%2==1 and b%2==1
    if kind=='face': return a==value or b==value
    raise ValueError('UNKNOWN DICE EVENT')


def pair_probability(first,second=None,join='AND'):
    return STCORE.ratio(sum(1 for pair in pair_outcomes(first,second,join)),36)


def pair_outcomes(first,second=None,join='AND'):
    for a in range(1,7):
        for b in range(1,7):
            x=pair_matches((a,b),first)
            y=pair_matches((a,b),second) if second else x
            if (x and y) if join=='AND' else (x or y): yield a,b
