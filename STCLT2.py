import STCORE as c
from STCLTC import _read_number, _sample_check, _population_check, _result
from STCLTM import proportion_standard_error

def _sample_proportion(find_probability=False):
  context = input('EVENT / GROUP (ENTER=SKIP): ').strip()
  exact_p = c.read_exact('POPULATION PROPORTION p: ')
  p = c.number(exact_p)
  n = c.read_int('SAMPLE SIZE n: ')
  if not 0 <= p <= 1 or n < 1:
    raise ValueError('USE 0 <= p <= 1 AND SAMPLE SIZE POSITIVE')
  random = _sample_check()
  if random is None:
    return
  details=[]
  population_check,population_correction = _population_check(n,details)
  success = n*p
  failure = n*(1-p)
  normal = success >= 10 and failure >= 10
  base_se = proportion_standard_error(p,n)
  se = base_se*population_correction
  shape = ('PASS: np=%.2f AND n(1-p)=%.2f >= 10' %
      (success,failure) if normal else
      'FAIL: np=%.2f; n(1-p)=%.2f; NEED BOTH >= 10' %
      (success,failure))
  distribution = ('APPROXIMATELY NORMAL' if normal else
          'NORMAL APPROXIMATION NOT JUSTIFIED')
  _result('CLT > SAMPLE PROPORTION','p-hat',p,se,n,[
    'RANDOM / INDEPENDENT: '+random,
    '5% POPULATION CONDITION: '+population_check,
    'SUCCESS / FAILURE: '+shape,
    'SE=sqrt(p(1-p)/n)=sqrt(%.4f*%.4f/%d)=%.4f' %
    (p,1-p,n,base_se)]+
    (['FINITE POPULATION CORRECTION APPLIED: %.4f' %
     population_correction] if population_correction != 1 else []),
    distribution,context,
    normal and random != 'FAIL' and population_correction == 1,
    find_probability,'p',None,('proportion_fallback',exact_p,n,random,details[0]))
