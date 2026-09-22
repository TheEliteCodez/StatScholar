# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STCOUNT - counting / expected-value dispatcher; heavy code loads per group.
import STCORE as c


def solver_sample_space():
    return c.call('STCOUNT1', 'solver_sample_space')


def solver_ncr():
    return c.call('STCOUNT1', 'solver_ncr')


def solver_npr():
    return c.call('STCOUNT1', 'solver_npr')


def solver_expected():
    return c.call('STCOUNT1', 'solver_expected')

def table_probability(rows, event):
    return c.call('STCOUNT2', 'table_probability', rows, event)


def distribution_moments(rows):
    return c.call('STCOUNT2', 'distribution_moments', rows)


def read_distribution(approximate=False):
    return c.call('STCOUNT2', 'read_distribution', approximate)


def unusual_result(prob):
    return c.call('STCOUNT2', 'unusual_result', prob)

def distribution_session(rows=None, approximate=False, source=None, first_word=None):
    return c.call('STCOUNT3', 'distribution_session', rows, approximate, source, first_word)

def missing_probability():
    return c.call('STCOUNT4', 'missing_probability')


def hyper_distribution(npop, targets, draws):
    return c.call('STSAMPLE', 'hyper_distribution', npop, targets, draws)


def sample_session():
    return c.call('STSAMPLE', 'sample_session')


def payoff_session():
    return c.call('STCOUNT5', 'payoff_session')


def insurance_session():
    return c.call('STCOUNT5', 'insurance_session')


def raffle_session():
    return c.call('STCOUNT5', 'raffle_session')


def win_loss_session():
    return c.call('STCOUNT6', 'win_loss_session')


def payoff_tasks():
    return c.call('STCOUNT6', 'payoff_tasks')


def sample_word_session(word=None):
    return c.call('STSAMPLE', 'sample_word_session', word)


def read_sample_distribution():
    return c.call('STCOUNT4', 'read_sample_distribution')


def rounded_distribution_session():
    return c.call('STCOUNT4', 'rounded_distribution_session')


def money_session():
    return c.call('STCOUNT6', 'money_session')
