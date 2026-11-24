import STCORE as c
from STBMATH import *
import math
def solver_bin_exact():
  n = c.read_int('n TRIALS: ')
  p = c.read_exact('p SUCCESS: ')
  x = c.read_int('x CUTOFF: ')
  c.results('BINOMIAL =', [('P', binomial_exact_event(n, p, ('=', x, 0)))], ['n=' + str(n) + ' p=' + c.exact_text(p), 'X = ' + str(x)] + binomial_method(n,p,('=',x,0)))
def solver_bin_at_most():
  n = c.read_int('n TRIALS: ')
  p = c.read_exact('p SUCCESS: ')
  x = c.read_int('x CUTOFF: ')
  c.results('BINOMIAL <=', [('P', binomial_exact_event(n, p, ('<=', x, 0)))], ['n=' + str(n) + ' p=' + c.exact_text(p), 'X <= ' + str(x)] + binomial_method(n,p,('<=',x,0)))
def solver_bin_less():
  n = c.read_int('n TRIALS: ')
  p = c.read_exact('p SUCCESS: ')
  x = c.read_int('x CUTOFF: ')
  c.results('BINOMIAL <', [('P', binomial_exact_event(n, p, ('<', x, 0)))], ['n=' + str(n) + ' p=' + c.exact_text(p), 'X < ' + str(x)] + binomial_method(n,p,('<',x,0)))
def solver_bin_at_least():
  n = c.read_int('n TRIALS: ')
  p = c.read_exact('p SUCCESS: ')
  x = c.read_int('x CUTOFF: ')
  c.results('BINOMIAL >=', [('P', binomial_exact_event(n, p, ('>=', x, 0)))], ['n=' + str(n) + ' p=' + c.exact_text(p), 'X >= ' + str(x)] + binomial_method(n,p,('>=',x,0)))
def solver_bin_more():
  n = c.read_int('n TRIALS: ')
  p = c.read_exact('p SUCCESS: ')
  x = c.read_int('x CUTOFF: ')
  c.results('BINOMIAL >', [('P', binomial_exact_event(n, p, ('>', x, 0)))], ['n=' + str(n) + ' p=' + c.exact_text(p), 'X > ' + str(x)] + binomial_method(n,p,('>',x,0)))
def solver_bin_between():
  n = c.read_int('n TRIALS: ')
  p = c.read_exact('p SUCCESS: ')
  a = c.read_int('LOWER: ')
  b = c.read_int('UPPER: ')
  c.results('B10 BETWEEN', [('P', binomial_exact_event(n, p, ('[]', a, b)))], [str(a) + '<=X<=' + str(b), 'n=' + str(n) + ' p=' + c.exact_text(p)] + binomial_method(n,p,('[]',a,b)))
def solver_bin_mean_sd():
  n = c.read_int('n TRIALS: ')
  p = c.read_exact('p SUCCESS: ')
  mean = c.rmul((n, 1), p)
  var = c.rmul(mean, c.radd((1, 1), (-p[0], p[1])))
  c.results('B08/B09', [('mu', mean), ('VAR', var), ('sigma', math.sqrt(c.number(var)))], ['mu=np; VAR=np(1-p)'])
def binomial_method(n,p,event):
  return c.call('STWORK','Chain',c.call('STBNWK','work',n,p,event))
