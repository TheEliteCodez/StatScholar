# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STMDICE - dice dispatcher; heavy code loads per group.
import STCORE



def solver_dice_space():
    return STCORE.call('STMDICE1', 'solver_dice_space')



def dice_sum_at_most(n, value):
    return STCORE.call('STMDICE1', 'dice_sum_at_most', n, value)



def dice_event_count(n, event, value=0):
    return STCORE.call('STMDICE1', 'dice_event_count', n, event, value)



def solver_multi_dice(n=None):
    return STCORE.call('STMDICE2', 'solver_multi_dice', n)



def word_event(n,word,sum_only=False):
    return STCORE.call('STMDICE2', 'word_event', n, word, sum_only)
