import STCORE as c
from STCLTC import _read_number, _sample_check, _population_check, _result
from STCLTM import mean_standard_error

def _sample_mean(find_probability=False):
  context = input('MEASURE / UNITS (ENTER=SKIP): ').strip()
  mean = _read_number('POPULATION MEAN mu: ')
  sigma = _read_number('POPULATION SD sigma (OR GIVEN s): ')
  n = c.read_int('SAMPLE SIZE n: ')
  if sigma < 0 or n < 1:
    raise ValueError('SD MUST BE NONNEGATIVE AND SAMPLE SIZE POSITIVE')
  random = _sample_check()
  if random is None:
    return
  details=[]
  population_check,population_correction = _population_check(n,details)
  normal = c.menu('POPULATION APPROXIMATELY NORMAL?',[
    ('1','YES / GIVEN NORMAL'),
    ('2','NO / SKEWED'),
    ('3','NOT GIVEN / UNSURE')])
  if normal == '0':
    return
  if normal == '1':
    shape = 'PASS: NORMAL POPULATION'
    distribution = 'NORMAL (IF RANDOM / INDEPENDENT)'
  elif n >= 30:
    shape = 'PASS: n >= 30; CLT APPROXIMATION'
    distribution = 'APPROXIMATELY NORMAL BY CLT'
  elif normal == '2':
    shape = 'FAIL: NONNORMAL POPULATION AND n < 30'
    distribution = 'NOT JUSTIFIED AS NORMAL'
  else:
    shape = 'VERIFY: POPULATION SHAPE UNKNOWN AND n < 30'
    distribution = 'NORMALITY NOT ESTABLISHED'
  base_se = mean_standard_error(sigma,n)
  se = base_se*population_correction
  correction_line = (['FINITE POPULATION CORRECTION APPLIED: %.4f' %
            population_correction] if population_correction != 1 else [])
  _result('CLT > SAMPLE MEAN','x-bar',mean,se,n,[
    'RANDOM / INDEPENDENT: '+random,
    '5% POPULATION CONDITION: '+population_check,
    'NORMALITY / CLT: '+shape,
    'SE=sigma/sqrt(n)=%.4f/sqrt(%d)=%.4f' % (sigma,n,base_se)]+
    correction_line,
    distribution,context,
    (normal == '1' or n >= 30) and random != 'FAIL' and population_correction == 1,
    find_probability,'mu',sigma,('mean_fallback',mean,sigma,n,random,details[0],normal=='1'))
