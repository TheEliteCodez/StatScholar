import math
import STCORE as c
_read_number=c.read_number
def _sample_check():
  key = c.menu('RANDOM / INDEPENDENT SAMPLE',[
    ('1','YES / GIVEN'),
    ('2','NO'),
    ('3','NOT GIVEN / UNSURE')])
  return {'1':'PASS','2':'FAIL','3':'VERIFY'}.get(key)
def _population_check(n,details=None):
  raw = input('POPULATION SIZE N (ENTER=SKIP): ').strip()
  if not raw:
    if details is not None: details.append(None)
    return 'NOT CHECKED',1.0
  try:
    population = int(raw)
  except ValueError:
    raise ValueError('POPULATION SIZE MUST BE A WHOLE NUMBER')
  if population < 1:
    raise ValueError('POPULATION SIZE MUST BE POSITIVE')
  if n > population:
    raise ValueError('SAMPLE SIZE CANNOT EXCEED POPULATION SIZE')
  if details is not None: details.append(population)
  if n <= 0.05*population:
    return 'PASS',1.0
  correction = math.sqrt((population-n)/(population-1)) if n < population else 0.0
  return 'FAIL; FINITE CORRECTION APPLIED',correction
def _result(*args):
  return c.call('STCLTR','_result',*args)
