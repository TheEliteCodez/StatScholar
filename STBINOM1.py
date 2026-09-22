# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Binomial cutoff solvers and the method-text helper.
import STCORE as c
from STBMATH import *
import math


def solver_bin_exact():
    n = c.read_int('n TRIALS: ')
    p = c.read_exact('p SUCCESS: ')
    x = c.read_int('x CUTOFF: ')
    c.results('BINOMIAL =', [('P', binomial_exact_event(n, p, ('=', x, 0)))], ['n=' + str(n) + ' p=' + c.exact_text(p), 'X = ' + str(x)])


def solver_bin_at_most():
    n = c.read_int('n TRIALS: ')
    p = c.read_exact('p SUCCESS: ')
    x = c.read_int('x CUTOFF: ')
    c.results('BINOMIAL <=', [('P', binomial_exact_event(n, p, ('<=', x, 0)))], ['n=' + str(n) + ' p=' + c.exact_text(p), 'X <= ' + str(x)])


def solver_bin_less():
    n = c.read_int('n TRIALS: ')
    p = c.read_exact('p SUCCESS: ')
    x = c.read_int('x CUTOFF: ')
    c.results('BINOMIAL <', [('P', binomial_exact_event(n, p, ('<', x, 0)))], ['n=' + str(n) + ' p=' + c.exact_text(p), 'X < ' + str(x)])


def solver_bin_at_least():
    n = c.read_int('n TRIALS: ')
    p = c.read_exact('p SUCCESS: ')
    x = c.read_int('x CUTOFF: ')
    c.results('BINOMIAL >=', [('P', binomial_exact_event(n, p, ('>=', x, 0)))], ['n=' + str(n) + ' p=' + c.exact_text(p), 'X >= ' + str(x)])


def solver_bin_more():
    n = c.read_int('n TRIALS: ')
    p = c.read_exact('p SUCCESS: ')
    x = c.read_int('x CUTOFF: ')
    c.results('BINOMIAL >', [('P', binomial_exact_event(n, p, ('>', x, 0)))], ['n=' + str(n) + ' p=' + c.exact_text(p), 'X > ' + str(x)])


def solver_bin_between():
    n = c.read_int('n TRIALS: ')
    p = c.read_exact('p SUCCESS: ')
    a = c.read_int('LOWER: ')
    b = c.read_int('UPPER: ')
    c.results('B10 BETWEEN', [('P', binomial_exact_event(n, p, ('[]', a, b)))], [str(a) + '<=X<=' + str(b), 'n=' + str(n) + ' p=' + c.exact_text(p)])


def solver_bin_mean_sd():
    n = c.read_int('n TRIALS: ')
    p = c.read_exact('p SUCCESS: ')
    mean = c.rmul((n, 1), p)
    var = c.rmul(mean, c.radd((1, 1), (-p[0], p[1])))
    c.results('B08/B09', [('mu', mean), ('VAR', var), ('sigma', math.sqrt(c.number(var)))], ['mu=np; VAR=np(1-p)'])


def binomial_method(n,p,event):
    op,a,b=event
    prefix='n='+str(n)+' p='+c.exact_text(p)
    if op=='=': return [prefix,'P(X=x)=nCx*p^x*(1-p)^(n-x)','binompdf(n,p,x)']
    import math
    x=c.number(a)
    if op=='<=': text='binomcdf(n,p,'+str(math.floor(x))+')'
    elif op=='<': text='binomcdf(n,p,'+str(math.ceil(x)-1)+')'
    elif op=='>=': text='1-binomcdf(n,p,'+str(math.ceil(x)-1)+')'
    elif op=='>': text='1-binomcdf(n,p,'+str(math.floor(x))+')'
    else: text='SUM binompdf OVER MATCHING INTEGERS'
    return [prefix,text]
