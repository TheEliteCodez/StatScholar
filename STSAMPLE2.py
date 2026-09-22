# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Sampling-without-replacement sessions and entry helpers.
import STCORE as c


def sample_session():
    c.heading('R07 WITHOUT REPLACEMENT')
    total=c.read_int('TOTAL OBJECTS IN BOX: ')
    targets=c.read_int('DEFECTIVE/TARGET OBJECTS: ')
    draws=c.read_int('HOW MANY SELECTED: ')
    c.call('STSAMPLE','show_distribution',total,targets,draws,True)
    sample_tasks(total,targets,draws)


def sample_word_session(word=None):
    total,targets,draws=read_parameters()
    sample_tasks(total,targets,draws,word)


def read_parameters():
    return c.read_int('TOTAL OBJECTS N: '),c.read_int('TARGET OBJECTS K: '),c.read_int('NUMBER SELECTED n: ')


def sample_tasks(total,targets,draws,word=None):
    while True:
        key='1' if word else c.menu('WITHOUT REPLACEMENT / SAME DATA',[('1','EVENT PROBABILITY'),('2','MEAN / VAR / SD'),('3','AT LEAST ONE'),('4','UNUSUAL EVENT'),('5','SHOW DISTRIBUTION'),('6','BINOMIAL CONDITIONS'),('7','CHANGE DATA'),('9','BAR HEIGHTS / DRAWING STEPS')])
        if key=='0': return
        if key=='7':
            total,targets,draws=read_parameters()
        elif key=='6': c.call('STBEXTRA','binomial_conditions')
        elif key in ('5','9'):
            c.call('STSAMPLE','show_distribution',total,targets,draws)
            if key=='9': c.view('DRAW HISTOGRAM',['x=NUMBER OF TARGETS','BAR HEIGHT=P(X)','EQUAL-WIDTH BARS'])
        elif key=='2':
            mean,var,sd=c.call('STSAMPLE','moments',total,targets,draws)
            c.results('R02/R03',[('mu',mean),('VAR',var),('sigma',sd)],['mu=n*K/N','VAR=n*(K/N)*(1-K/N)*(N-n)/(N-1)','SD=SQRT(VAR)'])
        else:
            if word:
                event=c.call('STBWE','read_event',word)
                word=None
            else: event=('>=',1,0) if key=='3' else c.event_input()
            if event is None: continue
            p=c.call('STSAMPLE','event_probability',total,targets,draws,event)
            if key=='4':
                cutoff=c.as_ratio(input('UNUSUAL CUTOFF (ENTER=.05): ').strip() or '.05')
                c.results('R06 UNUSUAL EVENT',[('P(EVENT)',p),('UNUSUAL','YES' if c.compare_exact(p,cutoff)<=0 else 'NO')],['UNUSUAL IF P<=CUTOFF','CUTOFF='+c.exact_text(cutoff),'USE LOWER TAIL FOR FEW','UPPER TAIL FOR MANY','EVIDENCE UNDER THE MODEL','NOT PROOF OF A CAUSE'])
            else: c.results('R07 EVENT',[('P',p)],['WITHOUT REPLACEMENT','ADD MATCHING EXACT PROBABILITIES'])


def box_session():
    key=c.menu('DEFECTIVE ITEMS / BOX',[('1','DRAW WITHOUT REPLACEMENT'),('2','REPLACE AFTER EACH DRAW'),('3','ALREADY GIVEN X / P TABLE')])
    if key=='1': sample_session()
    elif key=='2':
        total=c.read_int('TOTAL IN BOX: ');targets=c.read_int('DEFECTIVE IN BOX: ')
        draws=c.read_int('NUMBER DRAWN: ')
        c.call('STBWORD','wording_session',None,draws,c.ratio(targets,total))
    elif key=='3': c.call('STCOUNT','distribution_session')
