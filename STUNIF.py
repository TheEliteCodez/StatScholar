import math
import STCORE as c
from STDIST import _number, _probability, _probability_text

def _uniform_cdf(value, low, high):
  if value <= low:
    return 0.0
  if value >= high:
    return 1.0
  return (value-low)/(high-low)

def _uniform_probability(low, high):
  event = c.menu('UNIFORM > FIND PROBABILITY', [
    ('1', 'BELOW A VALUE'),
    ('2', 'ABOVE A VALUE'),
    ('3', 'BETWEEN TWO VALUES')])
  if event == '0':
    return
  if event == '1':
    value = _number('VALUE x: ')
    probability = _uniform_cdf(value, low, high)
    label = 'P(X < %.4f)' % value
  elif event == '2':
    value = _number('VALUE x: ')
    probability = 1-_uniform_cdf(value, low, high)
    label = 'P(X > %.4f)' % value
  else:
    lower = _number('LOWER VALUE: ')
    upper = _number('UPPER VALUE: ')
    if lower > upper:
      raise ValueError('LOWER VALUE MUST NOT EXCEED UPPER VALUE')
    probability = max(0.0, min(upper, high)-max(lower, low))/(high-low)
    label = 'P(%.4f < X < %.4f)' % (lower, upper)
  clipped=(max(low,min(high,value))-low) if event=='1' else (high-max(low,min(high,value))) if event=='2' else max(0.0,min(upper,high)-max(lower,low))
  work=['P=SHADED WIDTH/(b-a)', 'P=%g/(%g-%g)=%.6f' % (clipped,high,low,probability)]
  c.view('UNIFORM > PROBABILITY', [
    'P=%.7g; a=%.5g; b=%.5g' % (probability,low,high),
    'X UNIFORM ON [%.4f, %.4f]' % (low, high),
    label,
    _probability_text(probability)]+work+c.call('STSKETCH','curve','UNIFORM',low,high,event,
      (lower,upper) if event=='3' else (value,)))

def _uniform_percentile(low, high):
  request=c.call('STDIST','cutoff_request')
  if request is None: return
  probability,shading,work=request
  cutoff = low+probability*(high-low)
  answer='VALUE CUTOFF x=%.4f' % cutoff
  if c.view('UNIFORM > PERCENTILE ANSWER',[
    answer,'a=%.6g; b=%.6g' % (low,high),'AREA TO LEFT=%.6f' % probability,
    'x=a+LEFT AREA*(b-a)']+work) in ('back','exit'): return
  c.view('UNIFORM > PERCENTILE', [
    answer,
    'X UNIFORM ON [%.4f, %.4f]' % (low, high),
    'AREA TO LEFT=%.4f (%.2f%%)' % (probability, 100*probability),
    'x=a+LEFT AREA*(b-a)']+
    ['x=%g+%g*(%g-%g)=%g' % (low,probability,high,low,cutoff)]+
    c.call('STSKETCH','curve','UNIFORM',low,high,shading,(cutoff,)))

def _uniform_axes(low, high, draw=True):
  lines=[
    'X UNIFORM ON [a,b]=[%.4f, %.4f]' % (low, high),
    'MEAN=(a+b)/2=%.4f' % ((low+high)/2),
    'VAR=(b-a)^2/12=%.4f' % ((high-low)**2/12),
    'SD=(b-a)/sqrt(12)=%.4f' % ((high-low)/math.sqrt(12)),
    'CONSTANT HEIGHT=1/(b-a)=%.4f' % (1/(high-low)),
    ]
  if draw: lines.append('DRAW A RECTANGLE FROM a TO b; SHADE REQUESTED AREA.')
  if draw: c.call('STGCURV','show','UNIFORM',low,high)
  else: c.view('UNIFORM > MEAN / SD / HEIGHT',lines)

def uniform_menu():
  low=high=None
  while True:
    key=c.menu('UNIFORM DISTRIBUTION',[
      ('1','FIND A PROBABILITY'),
      ('2','FIND A PERCENTILE / CUTOFF'),
      ('3','MEAN / VAR / SD / HEIGHT'),
      ('4','DRAW / LABEL RECTANGLE'),
      ('5','CHANGE ENDPOINTS a / b')])
    if key=='0': return
    if low is None or key=='5':
      low=_number('LOWER ENDPOINT a: ')
      high=_number('UPPER ENDPOINT b: ')
      if low>=high:
        low=high=None
        raise ValueError('UPPER ENDPOINT b MUST EXCEED LOWER ENDPOINT a')
    if key=='1': _uniform_probability(low,high)
    elif key=='2': _uniform_percentile(low,high)
    elif key=='3': _uniform_axes(low,high,False)
    elif key=='4': _uniform_axes(low,high)
