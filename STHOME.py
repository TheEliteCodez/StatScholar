# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Home menu dispatcher, loaded only when the home menu runs.
import STCORE


def quick_main(g):
    GUIDES=g['GUIDES']
    QUESTION_INDEX=g['QUESTION_INDEX']
    TASKS={'1':('STHOME','words_tasks'),'2':('STHOME','trial_tasks'),'3':('STPROBM','probability_tasks'),'4':('STTASKS','data_tasks'),'5':('STTASKS','graph_tasks'),'6':('STHOME','study_tasks'),'8':('STWIZM','question_wizard')}
    while True:
        key=STCORE.menu('STAT1',[('1','QUESTION WORDS / HELP'),('2','BINOMIAL'),('3','PROBABILITY'),('4','DATA / STATS'),('5','NORMAL / Z / GRAPHS'),('6','STUDY / CONCEPTS'),('7','PRACTICE TEST 1 / Q1-30'),('8','QUESTION WIZARD')],GUIDES,QUESTION_INDEX,page_size=6)
        if key=='0': return
        try:
            if key=='7':
                STCORE.call('STPRE','pretest_menu')
            elif key in QUESTION_INDEX or key.startswith('PT'): g['question_lookup'](key)
            elif key in GUIDES: g['launch_route'](key)
            else:
                module, func = TASKS[key]
                STCORE.call(module, func, g)
        except (ValueError,ZeroDivisionError,IndexError) as exc:
            STCORE.view('CHECK ENTERED VALUES',[str(exc)])


def trial_tasks(g):
    STCORE.call('STBWORD','wording_session')


def words_tasks(g):
    STCORE.call('STWORDS','words_menu',{'experiment_tasks':g['experiment_tasks'],'find_tasks':g['find_tasks'],'money_tasks':g['money_tasks']})


def study_tasks(g):
    g['reference_call']('study_menu')


def find_tasks(g):
    g['reference_call']('find_menu')
