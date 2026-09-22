# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Wording-led binomial UI; imports only small arithmetic dependencies.
import STCORE as c

WORDS={'=':'EXACTLY','<=':'AT MOST','>=':'AT LEAST','<':'LESS THAN','>':'MORE THAN','[]':'BETWEEN','()':'BETWEEN','[)':'BETWEEN','(]':'BETWEEN','!=':'NOT EQUAL'}


def read_parameters():
    return c.read_int('TRIALS n: '),c.read_exact('CHANCE p (DECIMAL OR %): ') 


def wording_session(first=None,n=None,p=None):
    style,places='D',4
    threshold=(1,20)
    cache={}
    while True:
        op=first or c.choice_pages('BINOMIAL > QUESTION WORDS',c.call('STBWE','pages'))
        first=None
        if op is None: return
        if op=='conditions':
            eligible=c.call('STBEXTRA','binomial_conditions')
            if eligible is None: continue
            key=c.menu('MODEL CHECK > NEXT',[('1','CONTINUE BINOMIAL')] if eligible else [('2','EXACT WITHOUT REPLACEMENT')])
            if key=='1': first='='
            elif key=='2': c.call('STSAMPLE','sample_session')
            continue
        if op=='cheat':
            c.call('STBHELP','cheat_sheet');continue
        if op=='finite':
            total,draws,replaced,small=c.call('STFINITE','finite_check')
            items=[('1','EXACT WITHOUT REPLACEMENT')] if not replaced else []
            if replaced or small: items.append(('2','CONTINUE BINOMIAL'))
            key=c.menu('FINITE MODEL > NEXT',items)
            if key=='1':
                targets=c.read_int('EXACT TARGET COUNT K: ')
                c.call('STSAMPLE','sample_tasks',total,targets,draws)
            elif key=='2':
                n=draws;p=c.read_exact('CHANCE EACH TRIAL p: ');cache={};first='='
            continue
        if op=='sample':
            c.call('STSAMPLE','sample_session');continue
        if n is None:
            if p is None: n,p=read_parameters()
            else: n=c.read_int('TRIALS n: ')
        if op in ('stats','usual','shape','model','full'):
            c.call('STBHELP','parameter_results',op,n,p)
            continue
        event=c.call('STBWE','read_event',op)
        if event is None: continue
        answer=c.call('STBMATH','binomial_exact_event',n,p,event)
        words,math_text,command,why=c.call('STBW2','translation',n,p,event)
        while True:
            lines=['ANSWER='+c.answer_text(answer,style,places),math_text,'RIGHT: STATS / USUAL / z' if c.HAS_KEYS else 'ENTER: STATS / USUAL / z']
            c.call('STBINFO','show_answer',n,p,event,answer,'BINOMIAL > '+WORDS[event[0]],lines,threshold,cache)
            lines=None
            key=c.menu('BINOMIAL > SAME n,p',[('1','NEXT PART, SAME n,p'),('2','SHOW WHY'),('3','TRANSLATION / FORMULA'),('4','CHANGE n,p'),('5','ANSWER FORMAT'),('6','IS THIS EVENT UNUSUAL?'),('7','MEAN / SD / VAR / USUAL')])
            if key=='0': return
            if key=='1': break
            if key=='2': c.view('BINOMIAL > WHY',[why,'n='+str(n)+' p='+c.exact_text(p)])
            elif key=='3': c.view('BINOMIAL > FORMULA',[words,math_text,'TI-84:',command,'P(X=k)=C(n,k)*p^k*(1-p)^(n-k)','SUM OVER INCLUDED INTEGER k'])
            elif key=='4':
                n,p=read_parameters();cache={};break
            elif key=='7': c.call('STBHELP','parameter_results','stats',n,p)
            elif key=='6': threshold=c.call('STBHELP','event_unusual',answer,math_text,threshold)
            elif key=='5':
                fmt=c.menu('BINOMIAL > FORMAT',[('1','DECIMAL'),('2','FRACTION'),('3','PERCENT')])
                if fmt=='0': continue
                style={'1':'D','2':'F','3':'P'}[fmt]
                if style!='F': places=c.read_int('DECIMAL PLACES: ')
