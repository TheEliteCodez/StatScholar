import STCORE as c

def inference(ts,alpha,alternative,degrees=None):
  if not 0<alpha<1 or alternative not in ('<','>','!='):
    raise ValueError('CHECK alpha AND ALTERNATIVE')
  if degrees is None:
    left=c.call('STCLTM','normal_cdf',ts)
    right=c.call('STCLTM','normal_sf',ts)
    quantile=lambda area:c.call('STZCRIT','standard_normal_quantile',area)
  else:
    left=c.call('STTCRIT','t_cdf',ts,degrees)
    right=c.call('STTCRIT','t_sf',ts,degrees)
    quantile=lambda area:c.call('STTCRIT','t_quantile',area,degrees)
  if ts==0: left=right=.5
  if alternative=='<': probability=left;critical=(quantile(alpha),)
  elif alternative=='>': probability=right;critical=(quantile(1-alpha),)
  else:
    probability=min(1,2*min(left,right))
    positive=quantile(1-alpha/2)
    critical=(-positive,positive)
  return probability,critical,probability<=alpha

