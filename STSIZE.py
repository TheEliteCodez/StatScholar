import math
import STCORE as c
from STZCRIT import z_critical
_read_number=c.read_number
def _read_confidence():
  while True:
    confidence = _read_number('CONFIDENCE LEVEL (E.G. 95%): ')
    if 0 < confidence < 1:
      return confidence
    print('ENTER A PERCENT OR DECIMAL BETWEEN 0 AND 1')
def proportion_sample_size(estimate,margin,confidence):
  if not 0 <= estimate <= 1 or margin <= 0:
    raise ValueError('USE 0 <= p-hat <= 1 AND POSITIVE MARGIN OF ERROR')
  critical = z_critical(confidence)
  return critical*critical*estimate*(1-estimate)/(margin*margin)
def mean_sample_size(sigma,margin,confidence):
  if sigma < 0 or margin <= 0:
    raise ValueError('POPULATION SD MUST BE NONNEGATIVE AND MARGIN POSITIVE')
  critical = z_critical(confidence)
  return (critical*sigma/margin)**2
def mean_sample_size_estimate(sample_sd,margin,confidence):
  return mean_sample_size(sample_sd,margin,confidence)
def _required_sample_size():
  key = c.menu('REQUIRED SAMPLE SIZE',[
    ('1','PERCENT / PROPORTION'),
    ('2','AVERAGE / MEAN')])
  if key == '0':
    return
  confidence = _read_confidence()
  if key == '1':
    raw = input('EXPECTED PROPORTION (ENTER=UNKNOWN): ').strip()
    estimate = c.number(c.as_ratio(raw)) if raw else 0.5
    margin = _read_number('MARGIN E (E.G. 5% OR 0.05): ')
    raw_n = proportion_sample_size(estimate,margin,confidence)
    formula = 'n=(z*^2 p-hat(1-p-hat))/E^2'
    substitution = '(%.4f^2*%.4f*%.4f)/%.4f^2' % (
      z_critical(confidence),estimate,1-estimate,margin)
  else:
    sigma = _read_number('POPULATION SD sigma (OR SAMPLE SD s): ')
    margin = _read_number('MAXIMUM MARGIN OF ERROR E: ')
    raw_n = mean_sample_size(sigma,margin,confidence)
    formula = 'n=(z* SD / E)^2'
    substitution = '(%.4f*%.4f/%.4f)^2' % (
      z_critical(confidence),sigma,margin)
  n = max(1,int(math.ceil(raw_n)))
  if key == '1':
    achieved = z_critical(confidence)*math.sqrt(estimate*(1-estimate)/n)
  else:
    achieved = z_critical(confidence)*sigma/math.sqrt(n)
  c.view('REQUIRED SAMPLE SIZE',[
    'ROUND UP: n='+str(n),
    'CONFIDENCE=%.5g%%; E=%.6g' % (100*confidence,margin),
    'z*=%.6g; ACTUAL E=%.6g' % (z_critical(confidence),achieved),
    'UNROUNDED n=%.6g' % raw_n,
    'CONFIDENCE='+('%.2f' % (100*confidence))+'%',
    'z*='+('%.4f' % z_critical(confidence)),
    'FORMULA: '+formula,
    'SUBSTITUTE: '+substitution,
    'UNROUNDED n='+('%.4f' % raw_n),
    'ROUND UP: n='+str(n),
    'CHECK AT n: APPROX E='+('%.4f' % achieved)]+(
    ['IF SD IS ESTIMATED: n IS APPROXIMATE.'] if key == '2' else []))
