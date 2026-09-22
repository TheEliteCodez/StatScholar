# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Question wizard, loaded only when selected.
import STCORE


def question_wizard(g):
    while True:
        key = STCORE.menu('QUESTION WIZARD', [
            ('1', 'TABLE OF VALUES'),
            ('2', 'RAW LIST OF NUMBERS'),
            ('3', 'DICE / COIN / CARDS'),
            ('4', 'FIXED TRIALS + A PERCENT'),
            ('5', 'PERCENTS / CHANCES GIVEN'),
            ('6', 'X AND P(X) TABLE'),
            ('7', 'COUNT / CHOOSE / ARRANGE'),
            ('8', 'MATCH MY WORDING / SEARCH')])
        if key == '0':
            return
        if key == '1':
            _wizard_table()
        elif key == '2':
            STCORE.call('STDATA', 'raw_session')
        elif key == '3':
            g['experiment_tasks']()
        elif key == '4':
            g['trial_tasks']()
        elif key == '5':
            g['probability_tasks']()
        elif key == '6':
            STCORE.call('STCOUNT', 'distribution_session')
        elif key == '7':
            g['reference_call']('wizard_counting')
        elif key == '8':
            g['words_tasks']()
        return


def _wizard_table():
    if STCORE.yesno('VALUES WITH A FREQUENCY COLUMN?'):
        STCORE.call('STDATA', 'frequency_data_session')
    elif STCORE.yesno('ROWS AND COLUMNS (TWO-WAY)?'):
        STCORE.call('STPROB', 'two_way_session')
    elif STCORE.yesno('NAMED CATEGORIES WITH COUNTS?'):
        STCORE.call('STPROB', 'category_session')
    else:
        STCORE.call('STDATA', 'raw_session')
