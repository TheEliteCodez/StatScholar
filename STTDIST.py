import math
import STCORE as c
from STDIST import _number, _probability, _probability_text

def t_menu():
  while True:
    key = c.menu('STUDENT t DISTRIBUTION', [
      ('1', 'CRITICAL t*: CONFIDENCE + df'),
      ('2', 'FIND A t PROBABILITY'),
      ('3', 'FIND A t PERCENTILE'),
      ('4', 'CRITICAL t*: OTHER INPUTS'),
      ('5', 'DRAW / INTERPRET t CURVE')])
    if key == '0':
      return
    if key == '1':
      c.call('STCIIO','critical_session','t','1',True)
    elif key == '2':
      degrees = c.read_number('DEGREES OF FREEDOM df: ')
      event = c.menu('t PROBABILITY EVENT', [
        ('1', 'BELOW A VALUE'),
        ('2', 'ABOVE A VALUE'),
        ('3', 'BETWEEN TWO VALUES')])
      if event == '0':
        continue
      c.call('STTPROB', 't_probability_session', degrees, event)
    elif key == '4':
      c.call('STCIIO','tstar_session')
    elif key=='5':
      degrees=c.read_number('DEGREES OF FREEDOM df: ')
      if degrees<=0: raise ValueError('df MUST BE POSITIVE')
      c.call('STGCURV','show','t',0,degrees)
    else:
      degrees = c.read_number('DEGREES OF FREEDOM df: ')
      request=c.call('STDIST','cutoff_request')
      if request is None: continue
      probability,shading,work=request
      value = c.call('STTCRIT', 't_quantile', probability, degrees)
      answer='t CUTOFF=%.6f' % value
      if c.view('t PERCENTILE ANSWER',[
        answer,'df=%g' % degrees,
        'AREA TO LEFT=%.6f' % probability]+work) in ('back','exit'): continue
      c.view('t PERCENTILE', [
        answer,
        'df=%g; AREA TO LEFT=%.4f (%.2f%%)' %
        (degrees, probability, 100*probability),
        't CUTOFF=%.6f' % value]+
        c.call('STSKETCH','curve','t',0,degrees,shading,(value,)))
