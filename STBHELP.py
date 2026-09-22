# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Binomial reference and parameter screens, loaded after event UI.
import STCORE as c


def cheat_sheet():
    c.view('BINOMIAL > CHEAT SHEET',[
        'EXACTLY r: X=r; PDF(r)', 'binompdf(n,p,r)',
        'AT MOST r: X<=r; CDF(r)', 'binomcdf(n,p,r); r INCLUDED',
        'LESS/FEWER r: X<r', 'binomcdf(n,p,r-1)',
        'AT LEAST r: X>=r', '1-binomcdf(n,p,r-1)',
        'MORE THAN r: X>r', '1-binomcdf(n,p,r)',
        'a THROUGH b INCLUSIVE:', 'CDF(b)-CDF(a-1)',
        'AT LEAST ONE: 1-P(0)', '1-(1-p)^n FOR INDEPENDENT TRIALS',
        'FOUR BINOMIAL REQUIREMENTS:', 'FIXED n; TWO OUTCOMES', 'SAME p; INDEPENDENT TRIALS',
        'SUCCESS=OUTCOME BEING COUNTED', 'IT CAN BE A DEFECT OR FAILURE'])


def parameter_results(kind,n,p):
    import math
    from STBMATH import usual_counts, binomial_exact_event, binomial_exact_ratio, binomial_shape
    mean=c.rmul((n,1),p)
    variance=c.rmul(mean,c.radd((1,1),(-p[0],p[1])))
    if kind=='full':
        c.paged_results('BINOMIAL > DISTRIBUTION',n+1,lambda k:('P('+str(k)+')',binomial_exact_ratio(n,p,k)),['X=COUNT; BAR HEIGHT=P(X)', 'SHAPE='+binomial_shape(p)])
    elif kind=='shape':
        c.results('BINOMIAL > SHAPE',[('CENTER',mean),('SHAPE',binomial_shape(p))],['CENTER=np; USE WHOLE SHAPE', 'SYMMETRIC DOES NOT MEAN UNIFORM'])
    elif kind=='model':
        c.results('BINOMIAL > DEFINE',[('n',n),('p',p),('X','COUNT OF TARGET OUTCOMES')],['SUCCESS=OUTCOME COUNTED, NOT NECESSARILY GOOD', 'FIXED n; TWO OUTCOMES; SAME p; INDEPENDENT'])
    else:
        mu,sd,lo,hi,low,high,first=usual_counts(n,p)
        cache={}
        c.call('STBINFO','show_answer',n,p,None,None,'BINOMIAL > MEAN / USUAL',None,(1,20),cache)
        raw=input('CHECK COUNT (ENTER=SKIP): ').strip()
        if raw:
            c.call('STBINFO','show_answer',n,p,('=',c.as_ratio(raw),0),None,'BINOMIAL > COUNT CHECK',None,(1,20),cache)
        if kind=='usual':
            c.results('BINOMIAL > EXACT TAILS',[('P(INSIDE)',binomial_exact_event(n,p,('[]',low,high))),('P(BELOW)',binomial_exact_event(n,p,('<',low,0))),('P(ABOVE)',binomial_exact_event(n,p,('>',high,0)))],['TAIL PROBABILITY IS NOT POINT PROBABILITY'])


def event_unusual(answer,event,threshold=(1,20)):
    raw=input('PROBABILITY CUTOFF (ENTER='+c.exact_text(threshold)+'): ').strip()
    threshold=c.as_ratio(raw) if raw else threshold
    c.results('BINOMIAL > EVENT UNUSUAL',[('EVENT',event),('P(EVENT)',answer),('CUTOFF',threshold),('UNUSUAL','YES' if c.compare_exact(answer,threshold)<=0 else 'NO')],['COMPARE THE WHOLE REQUESTED EVENT TO THE PROBABILITY CUTOFF.','FEW: LOWER TAIL; MANY: UPPER TAIL.','AN EXACT POINT PROBABILITY IS NOT A TAIL TEST.','THIS IS NOT THE MEAN +/- 2 SD RULE.','EVIDENCE UNDER THE MODEL; NOT PROOF THE CLAIM IS FALSE.'])

    return threshold
