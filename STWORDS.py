# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Question wording narrows context before selecting an engine.
import STCORE as c

PAGES=(
 (('EXACTLY / P(X=n)','= '),('AT MOST / NO MORE THAN','<='),('AT LEAST / OR MORE','>='),('LESS / FEWER THAN','<'),('MORE / GREATER THAN','>'),('BETWEEN','[]'),('GIVEN','given'),('AND / BOTH','and'),('OR','or')),
 (('AT LEAST ONE','one'),('WITHOUT REPLACEMENT','sample'),('UNUSUAL / HIGH / LOW','unusual'),('MEAN / EXPECTED','mean'),('SD / VARIANCE','sd'),('Q1 / SHORTEST 25%','q1'),('MEDIAN / HALF BELOW','median'),('PARAMETER / STATISTIC','parameter'),('SAMPLE / POPULATION','population')),
 (('RANDOM SAMPLE','sampling'),('SAMPLING METHOD','sampling'),('OBSERVATIONAL / EXPERIMENT','experiment'),('BOXPLOT','box'),('DOTPLOT','dot'),('HISTOGRAM','hist'),('BELL CURVE / NORMAL','normal'),('EXPECTED VALUE / MONEY','money'),("I STILL DON'T KNOW",'find')),
 (('VENN / COMPOST / RECYCLE','venn'),('ALL SELECTED / REPLACEMENT','all'),('DICE / ODD / EVEN / SUBSETS','dice'),('QUIZ 4 EXAMPLES','quiz4'),('QUIZ 5 / ROUNDED TABLE','quiz5'),('PRACTICE TEST 1','pretest'),('NOT / COMPLEMENT','not')))


def words_menu(context):
    while True:
        word=c.choice_pages('WHAT WORDS DO YOU SEE?',PAGES)
        if word is None: return
        word_route(word.strip(),context)


def word_route(word,context=None):
    context=context or {}
    if word in ('=','<=','>=','<','>','[]','one'):
        key=c.menu('WHAT ELSE IS GIVEN?',[('1','TRIAL COUNT + CHANCE EACH'),('2','X / P(X) TABLE'),('3','WITHOUT REPLACEMENT'),('4','DICE / COIN / CARDS'),('5','MATCHING COUNTS / TOTAL'),('6','EXPLAIN WORDING')])
        if key=='6':
            c.view('WORDING',[{'=':'EXACTLY: X=r','<=':'AT MOST: X<=r','>=':'AT LEAST: X>=r','<':'LESS: X<r','>':'MORE: X>r','[]':'BETWEEN: CHOOSE ENDPOINTS','one':'AT LEAST ONE: X>=1'}[word]]);return
        if key=='1': c.call('STBWORD','wording_session',word)
        elif key=='2': c.call('STCOUNT','distribution_session',None,False,None,word)
        elif key=='3': c.call('STSAMPLE','sample_word_session',word)
        elif key=='4': context['experiment_tasks'](word)
        elif key=='5':
            c.view('COUNT MATCHING OUTCOMES',['COUNT ONLY OUTCOMES SATISFYING '+word,'FOR BETWEEN, APPLY BOTH ENDPOINTS FIRST.','USE TABLE / DICE IF YOU NEED HELP COUNTING.'])
            c.call('STPROB','solver_basic_prob')
    elif word=='not': c.call('STPWORD','complement_words',context)
    elif word in ('given','and','or'):
        c.call('STPWORD','probability_words',word)
    elif word=='sample': c.call('STSAMPLE','sample_word_session',None)
    elif word=='unusual':
        key=c.menu('WHAT DOES UNUSUAL USE?',[('1','MEAN AND SD / Z'),('2','BINOMIAL n,p COUNTS'),('3','PROBABILITY / .05 CUTOFF'),('4','BELL SHAPE / SD PERCENT')])
        if key=='1': c.call('STNORM','normal_session',None,None,'5')
        elif key=='2': c.call('STBWORD','wording_session','usual')
        elif key=='3': c.call('STCOUNT','unusual_result',c.read_exact('EVENT OR TAIL PROBABILITY: '))
        elif key=='4': c.call('STNORM','empirical_session')
    elif word in ('mean','sd'):
        key=c.menu('WHAT DATA ARE GIVEN?',[('1','LIST OF NUMBERS'),('2','VALUE + FREQUENCY'),('3','X + P(X)'),('4','BINOMIAL n,p'),('5','PRIZES / MONEY')])
        if key=='1': c.call('STDATA','raw_session')
        elif key=='2': c.call('STDATA','frequency_data_session')
        elif key=='3': c.call('STCOUNT','distribution_session')
        elif key=='4': c.call('STBWORD','wording_session','stats')
        elif key=='5': c.call('STCOUNT','money_session')
    elif word in ('q1','median'):
        key=c.menu('WHAT DATA ARE GIVEN?',[('1','RAW LIST'),('2','VALUE + FREQUENCY')])
        if key!='0': c.call('STDATA','raw_session' if key=='1' else 'frequency_data_session')
    elif word in ('parameter','population','sampling','experiment'):
        c.call('STSTUDY',{'parameter':'parameter_classifier','population':'population_classifier','sampling':'sampling_menu','experiment':'experiment_classifier'}[word])
    elif word=='money':
        if 'money_tasks' in context: context['money_tasks']()
        else: c.call('STCOUNT','money_session')
    elif word in ('box','dot','hist','normal'):
        routes={'box':('STGRAPH','boxplot_session'),'dot':('STGRAPH','dotplot_session'),'hist':('STHIST','histogram_session'),'normal':('STNORM','normal_session'),'money':('STCOUNT','payoff_tasks')}
        c.call(*routes[word])
    elif word in ('venn','all','dice','quiz4','quiz5','pretest'):
        c.call(*{'venn':('STVENN','venn_session'),'all':('STVENN','selection_session'),'dice':('STDICE','dice_session'),'quiz4':('STQUIZ4','quiz_menu'),'quiz5':('STQUIZ5','quiz_menu'),'pretest':('STPRE','pretest_menu')}[word])
    elif word=='find': context['find_tasks']()
