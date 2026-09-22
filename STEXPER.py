# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Experiment dispatch; the heavy sessions live in STEXPER1/STEXPER2.
import STCORE


def experiment_session(kind, word=None):
    STCORE.call('STEXPER1', 'experiment_session', kind, word)


def experiment_indices(outcomes, kind, query):
    return STCORE.call('STEXPER2', 'experiment_indices', outcomes, kind, query)
