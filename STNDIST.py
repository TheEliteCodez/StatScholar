import math
import STCORE as c
from STDIST import _number, _probability, _probability_text

def _normal_cdf(value, mean, sd):
  return c.call('STCLTM', 'normal_cdf', (value-mean)/sd)

def _normal_sf(value, mean, sd):
  return c.call('STCLTM', 'normal_sf', (value-mean)/sd)

def _normal_interval(low, high, mean, sd):
  zlow=(low-mean)/sd
  zhigh=(high-mean)/sd
  return c.call('STCLTM','normal_interval',zlow,zhigh)

def _normal_probability(mean, sd):
  event = c.menu('NORMAL > FIND PROBABILITY', [
    ('1', 'BELOW A VALUE'),
    ('2', 'ABOVE A VALUE'),
    ('3', 'BETWEEN TWO VALUES')])
  if event == '0':
    return
  if event == '1':
    value = _number('VALUE x: ')
    probability = _normal_cdf(value, mean, sd)
    label = 'P(X < %.4f)' % value
  elif event == '2':
    value = _number('VALUE x: ')
    probability = _normal_sf(value, mean, sd)
    label = 'P(X > %.4f)' % value
  else:
    low = _number('LOWER VALUE: ')
    high = _number('UPPER VALUE: ')
    if low > high:
      raise ValueError('LOWER VALUE MUST NOT EXCEED UPPER VALUE')
    probability = _normal_interval(low,high,mean,sd)
    label = 'P(%.4f < X < %.4f)' % (low, high)
  bounds=(low,high) if event=='3' else (value,)
  lower,upper=('-1E99',str(value)) if event=='1' else (str(value),'1E99') if event=='2' else (str(low),str(high))
  work=['z=(x-mu)/sigma']+['z=(%g-%g)/%g=%.6f' % (x,mean,sd,(x-mean)/sd) for x in bounds]
  work+=['normalcdf('+lower+','+upper+','+str(mean)+','+str(sd)+')']
  c.view('NORMAL > INDIVIDUAL PROBABILITY', [
    'X: INDIVIDUAL MEASUREMENT',
    'MEAN mu=%.4f; SD sigma=%.4f' % (mean, sd),
    label,
    _probability_text(probability)]+work+c.call('STSKETCH','curve','NORMAL',mean,sd,event,
      (low,high) if event=='3' else (value,)))
  raw_count = input('NUMBER OF INDIVIDUALS (ENTER=SKIP): ').strip()
  if raw_count:
    try:
      count = int(raw_count)
    except ValueError:
      raise ValueError('NUMBER OF INDIVIDUALS MUST BE A WHOLE NUMBER')
    if count < 0:
      raise ValueError('NUMBER OF INDIVIDUALS MUST NOT BE NEGATIVE')
    c.view('NORMAL > EXPECTED COUNT', [
      'EXPECTED COUNT=N*P',
      'N=%d; P=%.6f' % (count, probability),
      'EXPECTED NUMBER=%.4f' % (count*probability)])

def _normal_percentile(mean, sd):
  request=c.call('STDIST','cutoff_request')
  if request is None: return
  probability,shading,work=request
  if probability == 0:
    cutoff = '-INFINITY'
  elif probability == 1:
    cutoff = 'INFINITY'
  else:
    z = c.call('STZCRIT', 'standard_normal_quantile', probability)
    cutoff = mean + z*sd
  answer='VALUE CUTOFF x='+('%.4f' % cutoff if 0 < probability < 1 else cutoff)
  zanswer='z CUTOFF='+('%.4f' % z if 0 < probability < 1 else cutoff)
  if c.view('NORMAL > PERCENTILE ANSWER',[
    answer,zanswer,'AREA TO LEFT=%.6f' % probability,
    'x=mu+z*sigma']+work) in ('back','exit'): return
  c.view('NORMAL > DRAW CUTOFF', [answer,
    'X: INDIVIDUAL MEASUREMENT',
    'MEAN mu=%.4f; SD sigma=%.4f' % (mean, sd),
    'AREA TO LEFT=%.4f (%.2f%%)' % (probability, 100*probability),
    zanswer,'invNorm(%g,%g,%g)' % (probability,mean,sd)]+
    c.call('STSKETCH','curve','NORMAL',mean,sd,shading,(cutoff,)))

def _normal_axes(mean, sd):
  lines = ['X: INDIVIDUAL MEASUREMENT',
      'mu=%.4f; sigma=%.4f' % (mean, sd),
      'DRAW A NORMAL CURVE CENTERED AT mu.']
  for z in range(-3, 4):
    lines.append('z=%+d  x=%.4f' % (z, mean+z*sd))
  lines.append('LABEL BOTH x AND z AXES; SHADE THE REQUESTED AREA.')
  c.view('NORMAL > DRAW / LABEL', lines)

def normal_menu():
  mean=sd=None
  while True:
    key=c.menu('NORMAL DISTRIBUTION',[
      ('1','FIND A PROBABILITY'),
      ('2','FIND A PERCENTILE / CUTOFF'),
      ('3','Z-SCORE / FIND x'),
      ('4','EMPIRICAL RULE'),
      ('5','USUAL / UNUSUAL VALUES'),
      ('6','DRAW / LABEL x AND z AXES'),
      ('7','SEVERAL VALUES: z / USUAL / AXES'),
      ('8','CHANGE MEAN / SD'),('9','CRITICAL z* VALUE')])
    if key=='0': return
    if key=='9':
      c.call('STCIIO','zstar_session');continue
    if key=='4':
      params=c.call('STNORM','empirical_session',c.as_ratio(str(mean)) if mean is not None else None,c.as_ratio(str(sd)) if sd is not None else None)
      if params[0] is not None:
        mean,sd=[c.number(x) for x in params]
        if sd<=0: raise ValueError('SD MUST BE POSITIVE')
      continue
    if mean is None or key=='8':
      mean=_number('POPULATION MEAN mu: ')
      sd=_number('POPULATION SD sigma: ')
      if sd<=0:
        mean=sd=None
        raise ValueError('POPULATION SD sigma MUST BE POSITIVE')
    exact_mean=c.as_ratio(str(mean));exact_sd=c.as_ratio(str(sd))
    if key=='3': c.call('STNORM','z_menu',exact_mean,exact_sd)
    elif key in ('5','7'):
      c.call('STNORM','normal_session',exact_mean,exact_sd,'5' if key=='5' else '8',None,True)
    if key=='1': _normal_probability(mean,sd)
    elif key=='2': _normal_percentile(mean,sd)
    elif key=='6': _normal_axes(mean,sd)


def normal_probability_plot(values=None):
  if values is None:
    values=c.call('STDMATH','read_raw','QQ PLOT > RAW MEASUREMENTS')
  if len(values) < 2:
    raise ValueError('QQ PLOT NEEDS AT LEAST TWO VALUES')
  values=c.exact_sorted(values)
  method=c.menu('NORMAL QUANTILE PLOTTING POSITIONS',[
    ('1','BLOM: (i-0.375)/(n+0.25)'),
    ('2','HAZEN: (i-0.5)/n'),
    ('3','RANK: i/(n+1)')])
  if method=='0':
    return
  n=len(values)
  def row_at(index):
    rank=index+1
    if method=='1':
      position=(rank-0.375)/(n+0.25)
    elif method=='2':
      position=(rank-0.5)/n
    else:
      position=rank/(n+1)
    quantile=c.call('STZCRIT','standard_normal_quantile',position)
    return (str(rank), 'x='+c.exact_text(values[index])+
        '; normal z=%.4f' % quantile)
  formula={
    '1':'BLOM NORMAL SCORES; USE THE CONVENTION THAT MATCHES THE PROVIDED PLOT.',
    '2':'HAZEN NORMAL SCORES; USE THE CONVENTION THAT MATCHES THE PROVIDED PLOT.',
    '3':'RANK/(n+1) NORMAL SCORES; USE THE CONVENTION THAT MATCHES THE PROVIDED PLOT.'
  }[method]
  method_name={'1':'BLOM','2':'HAZEN','3':'RANK'}[method]
  c.paged_results('QQ PLOT > '+method_name+' ORDERED PAIRS',n,row_at,[
    formula,
    'PLOT ORDERED x AGAINST NORMAL z QUANTILES.',
    'ASSESS LINEARITY AND OUTLIERS YOURSELF; NO AUTOMATIC NORMALITY VERDICT.'],drawing=['HOW TO DRAW: NORMAL QQ PLOT','HORIZONTAL AXIS: NORMAL z.','VERTICAL AXIS: ORDERED x.','PLOT EACH (z,x) TABLE PAIR.','NEAR A LINE: NORMAL IS PLAUSIBLE.'])
