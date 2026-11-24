import STCORE as c
SUMMARY_KEYS = ('n', 'SUM', 'MEAN', 'SAMPLE SD Sx', 'SAMPLE VARIANCE s^2', 'MIN', 'Q1', 'MEDIAN', 'Q3', 'MAX', 'MODE', 'RANGE', 'IQR', 'MIDRANGE')
def summary_results(stats, title='DATA > RAW > SUMMARY', population=False, values=None, rows=None):
  keys=['n','MEAN','MEDIAN','POPULATION SD' if population else 'SAMPLE SD Sx','MIN','Q1','Q3','MAX']
  keys+=[k for k in SUMMARY_KEYS+('POPULATION SD','POPULATION VARIANCE') if k not in keys]
  answers=[(k,stats[k]) for k in keys]
  if stats['n']>1:
    answers.extend((k,stats[k]) for k in ('LOWER FENCE','UPPER FENCE','LOW WHISKER','HIGH WHISKER','OUTLIERS'))
  sd=stats['POPULATION SD' if population else 'SAMPLE SD Sx']
  if sd!='DNE':
    distance=c.as_ratio(str(2*sd))
    answers.extend([('MIN USUAL',c.radd(stats['MEAN'],(-distance[0],distance[1]))),('MAX USUAL',c.radd(stats['MEAN'],distance))])
  c.results(title,answers,['MEAN=SUM/n','VAR=SUM((x-MEAN)^2)/'+('n' if population else '(n-1)'),
    'QUARTILES: MEDIANS OF HALVES','ODD n: OMIT CENTER FROM HALVES','MODE: >2 MODES OR NO PEAK = DNE',
    'IQR OUTLIERS AND 2-SD UNUSUAL ARE DIFFERENT']+
    c.call('STWORK','Chain',c.call('STDWK','descriptive',stats,values,rows)),drawing=[
    'POPULATION: mu=MEAN; sigma=POPULATION SD.',
    'SAMPLE: x-bar=MEAN; s=SAMPLE SD Sx.',
    'SUM SQUARED DEVIATIONS='+c.exact_text(c.rmul(stats['POPULATION VARIANCE'],(stats['n'],1))),
    'sigma=SQRT(SUM SQUARED DEVIATIONS/n).',
    's=SQRT(SUM SQUARED DEVIATIONS/(n-1)).'])
def data_normal(stats,first,population=False):
  sd=stats['POPULATION SD' if population else 'SAMPLE SD Sx']
  if sd=='DNE':
    c.view('DATA',['NEED TWO VALUES FOR SAMPLE SD']);return
  c.call('STNORM','normal_session',stats['MEAN'],c.as_ratio(str(sd)),first,
    stats['POPULATION VARIANCE' if population else 'SAMPLE VARIANCE s^2'])
def choose_population(population):
  key=c.menu('VARIANCE / SD USE',[('1','SAMPLE (n-1)'),('2','POPULATION (n)')])
  return population if key=='0' else key=='2'
def raw_session(values=None):
  return c.call('STDATA2', 'raw_session', values)
def comparison(a, b):
  return c.call('STDATA2', 'comparison', a, b)
def compare_session(a=None, boxes=False):
  return c.call('STDATA3', 'compare_session', a, boxes)
def frequency_data_session():
  return c.call('STDATA3', 'frequency_data_session')
