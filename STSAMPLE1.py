# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Hypergeometric math: probabilities, moments, distribution, event sums.
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


def hyper_distribution(npop, targets, draws):
    low = max(0, draws - (npop - targets))
    high = min(draws, targets)
    if high - low + 1 > c.MAX_ROWS:
        raise ValueError("MAX " + str(c.MAX_ROWS) + " DISTRIBUTION ROWS")
    denom = ncr(npop, draws)
    return [((k, 1), c.ratio(ncr(targets, k) * ncr(npop-targets, draws-k), denom))
            for k in range(low, high+1)]
