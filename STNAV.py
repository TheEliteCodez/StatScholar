# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STNAV - navigation dispatcher; heavy code loads per group.
import STCORE


def get_guide(gid, field=None):
    return STCORE.call('STNAV1', 'get_guide', gid, field)


def show_identified(qid):
    return STCORE.call('STNAV1', 'show_identified', qid)


def run_solver(name):
    return STCORE.call('STNAV1', 'run_solver', name)


def concept_session():
    return STCORE.call('STNAV1', 'concept_session')


def launch_route(route):
    return STCORE.call('STNAV1', 'launch_route', route)


def homework_tag(qid):
    return STCORE.call('STNAV1', 'homework_tag', qid)


def question_lookup(qid=None):
    return STCORE.call('STNAV2', 'question_lookup', qid)


def open_navigation(name, context, *args):
    for key, value in context.items():
        if key not in globals(): globals()[key] = value
    return globals()[name](*args)
