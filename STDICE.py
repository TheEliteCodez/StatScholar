# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.
# STDICE - dice dispatcher; heavy code loads per group.
import STCORE

def solver_dice_space(): return STCORE.call('STMDICE','solver_dice_space')
def solver_multi_dice(n=None): return STCORE.call('STMDICE','solver_multi_dice',n)
def dice_event_count(n,event,value=0): return STCORE.call('STMDICE','dice_event_count',n,event,value)
def dice_sum_at_most(n,value): return STCORE.call('STMDICE','dice_sum_at_most',n,value)
def experiment_session(kind): return STCORE.call('STEXPER','experiment_session',kind)
def experiment_indices(outcomes,kind,query): return STCORE.call('STEXPER','experiment_indices',outcomes,kind,query)


def pair_matches(pair,event):
    return STCORE.call('STDICE1', 'pair_matches', pair, event)


def pair_probability(first,second=None,join='AND'):
    return STCORE.call('STDICE1', 'pair_probability', first, second, join)


def pair_outcomes(first,second=None,join='AND'):
    return STCORE.call('STDICE1', 'pair_outcomes', first, second, join)


def read_pair_event():
    return STCORE.call('STDICE2', 'read_pair_event')


def dice_session(word=None):
    return STCORE.call('STDICE2', 'dice_session', word)
