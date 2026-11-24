import STCORE as c

def summary(setup,result,probability,critical,reject):
  return c.summary([
    'REJECT H0' if reject else 'FAIL TO REJECT H0',
    ('t' if result['df'] is not None else 'z')+'=%.6g' % result['ts'],'p=%.6g' % probability,'alpha=%.5g' % setup['alpha'],
    'CV='+', '.join('%.6g' % v for v in critical),
    'PE=%.6g' % result['estimate'],'H0=%.6g' % setup['null'],'SE=%.6g' % result['se']]+
    (['df=%.6g' % result['df']] if result['df'] is not None else [])+result.get('summary_inputs',result['inputs']))
