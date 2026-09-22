# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STPROB - solver code; references load separately.
import STCORE as c


def solver_basic_prob():
    return c.call('STPROB1', 'solver_basic_prob')


def solver_complement():
    return c.call('STPROB1', 'solver_complement')


def solver_general_or():
    return c.call('STPROB1', 'solver_general_or')


def solver_mut_or():
    return c.call('STPROB1', 'solver_mut_or')


def solver_indep_and():
    return c.call('STPROB1', 'solver_indep_and')


def solver_general_and():
    return c.call('STPROB1', 'solver_general_and')


def solver_conditional():
    return c.call('STPROB1', 'solver_conditional')


def solver_at_least_one():
    return c.call('STPROB1', 'solver_at_least_one')


def category_session():
    return c.call('STPROB4', 'category_session')


def supplied_session():
    return c.call('STPROB2', 'supplied_session')


def valid_probability():
    return c.call('STPROB2', 'valid_probability')


def probability_class(p):
    return c.call('STPROB2', 'probability_class', p)


def two_way_session():
    return c.call('STPROB3', 'two_way_session')


def read_two_way():
    return c.call('STPROB3', 'read_two_way')


def two_way_values(cells, r, cc):
    return c.call('STPROB3', 'two_way_values', cells, r, cc)
