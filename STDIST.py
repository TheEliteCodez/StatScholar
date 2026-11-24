import STCORE as c
_number=c.read_number

def _probability(prompt):
  value = _number(prompt)
  if not 0 <= value <= 1:
    raise ValueError('PROBABILITY MUST BE BETWEEN 0 AND 1')
  return value

def _probability_text(probability):
  if probability < 1e-6:
    return 'PROBABILITY=%.6e (%.6e%%)' % (
      probability,100*probability)
  return 'PROBABILITY=%.6f (%.4f%%)' % (
    probability,100*probability)

def cutoff_request():
  key=c.menu('CUTOFF: QUESTION WORDING',[
    ('1','AT MOST / BELOW / LESS THAN'),
    ('2','AT LEAST / ABOVE / MORE THAN'),
    ('3','PERCENTILE / AREA TO LEFT')])
  if key=='0': return None
  area=_probability('GIVEN PERCENT / AREA (E.G. 30%): ')
  left=1-area if key=='2' else area
  work=['GIVEN '+('RIGHT' if key=='2' else 'LEFT')+' AREA=%.6f' % area,
     'LEFT=1-%.6f=%.6f' % (area,left) if key=='2' else 'LEFT=GIVEN AREA=%.6f' % left]
  return left,('2' if key=='2' else '1'),work

def normal_menu():
  return c.call('STNDIST','normal_menu')

def uniform_menu():
  return c.call('STUNIF','uniform_menu')

def normal_probability_plot(values=None):
  return c.call('STNDIST','normal_probability_plot',values)

def t_menu():
  return c.call('STTDIST','t_menu')

def discrete_tools(count,row_at,title,approximate=False):
  return c.call('STCOUNT4','discrete_tools',count,row_at,title,approximate)
