# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Printed Practice Test 1 numbering; independent of legacy PT IDs.
import STCORE as c
TITLES=('Whole class: statistic or parameter', 'Building stories: discrete', 'Sample 100 of 800 teachers', 'Compare test scores / z axes', 'Gym age: usual range', 'Men / women pulse lists', 'Same mean and mode, different spread', 'Unusual z and empirical rule', 'Relative frequency / large numbers', 'Select a woman', 'At least one covid case', 'Wood OR defective rackets', 'Marbles / replacement ambiguity', 'Five flips distribution', 'School sample: binomial eligible', 'Certain and impossible events', 'Engineers: random versus SRS', 'Regroup frequency / histogram shape', 'Defective coils / two methods', 'Die twice: both twos', 'Sports poll sample proportion', 'Airline table / conditional / draws', 'Homework hours z-score', 'Twin birth weights / several z values', 'Exercise study / significance', 'Lottery ticket expected value', 'Reusable containers dotplot', 'Computer literacy X/P table', 'Circuit boards: improvement claim', 'Cracked eggs / usual and tails')
ROUTES={
'basic':('STPROB','solver_basic_prob'),'parameter':('STSTUDY','parameter_classifier'),
'measurement':('STSTUDY','measurement_menu'),'sampling':('STSTUDY','sampling_menu'),
'relative':('STNORM','relative_session'),'normal':('STNORM','normal_session'),
'compare':('STDATA','compare_session'),'empirical':('STNORM','empirical_session'),
'lln':('STSTUDY','large_numbers'),'binomial':('STBWORD','wording_session'),
'venn':('STVENN','venn_session'),'table':('STPROB','two_way_session'),
'selection':('STVENN','selection_session'),'finite':('STFINITE','finite_check'),
'conditions':('STBEXTRA','binomial_conditions'),'valid':('STPROB','valid_probability'),
'histogram':('STHIST','histogram_session'),'dice':('STDICE','dice_session'),
'study':('STSTUDY','study_menu'),'raffle':('STCOUNT','raffle_session'),
'dotplot':('STGRAPH','dotplot_session'),'distribution':('STCOUNT','distribution_session')}


def get_record(number):
    return c.call('STPRE'+str((number-1)//10+1),'get_record',number)


def pretest_menu(first=None):
    while True:
        key=str(first) if first is not None else c.menu('PRACTICE TEST 1 / Q1-30',[(str(i+1),title) for i,title in enumerate(TITLES)])
        first=None
        if key=='0': return
        number=int(key)
        while True:
            title,body,route=get_record(number)
            routes=route.split(',')
            action=c.menu('PRETEST Q'+key,[('1','WORKED ANSWER / CAVEATS')]+[(str(i+2),'OPEN '+name.upper()) for i,name in enumerate(routes)])
            if action=='0': break
            if action=='1': c.call('STPAGE','text_pages','PRETEST Q'+key,body)
            else:
                target=ROUTES[routes[int(action)-2]]
                body=None
                c.call(*target)


def search(query):
    query=' '.join(query.lower().split())
    if query in ('practice test 1','pretest','pretest 1 paper','practice test'):
        return []
    if query.startswith('pretest') and query[7:].isdigit():
        query='pretest '+query[7:]
    words=query.split()
    if words and words[-1].isdigit() and ('pretest' in words or 'practice' in words):
        number=int(words[-1])
        if 1<=number<=30: return [('PR:'+str(number),'PRETEST '+str(number)+' '+TITLES[number-1])]
    return [('PR:'+str(i+1),'PRETEST '+str(i+1)+' '+title) for i,title in enumerate(TITLES) if all(word in title.lower() for word in words)]
