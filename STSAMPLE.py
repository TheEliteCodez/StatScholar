# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STSAMPLE - sampling dispatcher; heavy code loads per group.
import STCORE



def probability(total,targets,draws,k):
    return STCORE.call('STSAMPLE1', 'probability', total, targets, draws, k)



def moments(total,targets,draws):
    return STCORE.call('STSAMPLE1', 'moments', total, targets, draws)



def show_distribution(total,targets,draws,summary=False):
    return STCORE.call('STSAMPLE1', 'show_distribution', total, targets, draws, summary)



def event_probability(total,targets,draws,event):
    return STCORE.call('STSAMPLE1', 'event_probability', total, targets, draws, event)



def hyper_distribution(npop, targets, draws):
    return STCORE.call('STSAMPLE1', 'hyper_distribution', npop, targets, draws)



def sample_session():
    return STCORE.call('STSAMPLE2', 'sample_session')



def sample_word_session(word=None):
    return STCORE.call('STSAMPLE2', 'sample_word_session', word)



def read_parameters():
    return STCORE.call('STSAMPLE2', 'read_parameters')



def sample_tasks(total,targets,draws,word=None):
    return STCORE.call('STSAMPLE2', 'sample_tasks', total, targets, draws, word)



def box_session():
    return STCORE.call('STSAMPLE2', 'box_session')
