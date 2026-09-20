# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Sampling without replacement; no general counting or binomial imports.
import STCORE as c
from STCOMB import ncr


def probability(total,targets,draws,k):
    return c.ratio(ncr(targets,k)*ncr(total-targets,draws-k),ncr(total,draws))


def moments(total,targets,draws):
    import math
    mean=c.ratio(draws*targets,total)
    variance=c.ratio(draws*targets*(total-targets)*(total-draws),total*total*(total-1)) if total>1 else (0,1)
    return mean,variance,math.sqrt(c.number(variance))


def show_distribution(total,targets,draws,summary=False):
    low=max(0,draws-(total-targets))
    count=min(draws,targets)-low+1
    def row(i):
        if i==count: return ('E(X)',c.ratio(draws*targets,total))
        k=low+i
        p=probability(total,targets,draws,k)
        return ('P(X='+str(k)+')',p if summary else c.answer_text(p,'F'))
    work=['C(K,k)*C(N-K,n-k)/C(N,n)','N='+str(total)+' K='+str(targets)+' n='+str(draws),'E(X)=n*K/N','WITHOUT REPLACEMENT']
    if draws==2:
        work+=['EXACTLY ONE IN TWO:','D THEN G + G THEN D',str(targets)+'/'+str(total)+' * '+str(total-targets)+'/'+str(total-1)+' + '+str(total-targets)+'/'+str(total)+' * '+str(targets)+'/'+str(total-1)]
    c.paged_results('R07 DISTRIBUTION',count+(1 if summary else 0),row,work)


def event_probability(total,targets,draws,event):
    low=max(0,draws-(total-targets))
    high=min(draws,targets)
    denom=ncr(total,draws)
    favorable=0
    for k in range(low,high+1):
        if c.event_match((k,1),*event):
            favorable+=ncr(targets,k)*ncr(total-targets,draws-k)
    return c.ratio(favorable,denom)


def sample_session():
    c.heading('R07 WITHOUT REPLACEMENT')
    total=c.read_int('TOTAL OBJECTS IN BOX: ')
    targets=c.read_int('DEFECTIVE/TARGET OBJECTS: ')
    draws=c.read_int('HOW MANY SELECTED: ')
    show_distribution(total,targets,draws,True)
    sample_tasks(total,targets,draws)


def sample_word_session(word=None):
    total,targets,draws=read_parameters()
    sample_tasks(total,targets,draws,word)


def read_parameters():
    return c.read_int('TOTAL OBJECTS N: '),c.read_int('TARGET OBJECTS K: '),c.read_int('NUMBER SELECTED n: ')


def sample_tasks(total,targets,draws,word=None):
    while True:
        key='1' if word else c.menu('WITHOUT REPLACEMENT / SAME DATA',[('1','EVENT PROBABILITY'),('2','MEAN / VAR / SD'),('3','AT LEAST ONE'),('4','UNUSUAL EVENT'),('5','SHOW DISTRIBUTION'),('6','BINOMIAL CONDITIONS'),('7','CHANGE DATA'),('9','GRAPH THIS DISTRIBUTION')])
        if key=='0': return
        if key=='7':
            total,targets,draws=read_parameters()
        elif key=='6': c.call('STBEXTRA','binomial_conditions')
        elif key in ('5','9'):
            show_distribution(total,targets,draws)
            if key=='9': c.view('DRAW HISTOGRAM',['x=NUMBER OF TARGETS','BAR HEIGHT=P(X)','EQUAL-WIDTH BARS'])
        elif key=='2':
            mean,var,sd=moments(total,targets,draws)
            c.results('R02/R03',[('mu',mean),('VAR',var),('sigma',sd)],['mu=n*K/N','VAR=n*(K/N)*(1-K/N)*(N-n)/(N-1)','SD=SQRT(VAR)'])
        else:
            if word:
                event=c.call('STBWORD','read_event',word)
                word=None
            else: event=('>=',1,0) if key=='3' else c.event_input()
            if event is None: continue
            p=event_probability(total,targets,draws,event)
            if key=='4':
                cutoff=c.as_ratio(input('UNUSUAL CUTOFF (ENTER=.05): ').strip() or '.05')
                c.results('R06 UNUSUAL EVENT',[('P(EVENT)',p),('UNUSUAL','YES' if c.compare_exact(p,cutoff)<=0 else 'NO')],['UNUSUAL IF P<=CUTOFF','CUTOFF='+c.exact_text(cutoff),'USE LOWER TAIL FOR FEW','UPPER TAIL FOR MANY','EVIDENCE UNDER THE MODEL','NOT PROOF OF A CAUSE'])
            else: c.results('R07 EVENT',[('P',p)],['WITHOUT REPLACEMENT','ADD MATCHING EXACT PROBABILITIES'])

def hyper_distribution(npop, targets, draws):
    low = max(0, draws - (npop - targets))
    high = min(draws, targets)
    if high - low + 1 > c.MAX_ROWS:
        raise ValueError("MAX " + str(c.MAX_ROWS) + " DISTRIBUTION ROWS")
    denom = ncr(npop, draws)
    return [((k, 1), c.ratio(ncr(targets, k) * ncr(npop-targets, draws-k), denom))
            for k in range(low, high+1)]
