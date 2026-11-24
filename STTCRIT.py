from STTBETA import _log_gamma,_beta_fraction,_regularized_beta

def _t_cdf(value, degrees):
  x = degrees/(degrees+value*value)
  tail = 0.5*_regularized_beta(x,degrees/2,0.5)
  return 1-tail if value >= 0 else tail
def t_critical(confidence, degrees):
  if not 0 < confidence < 1:
    raise ValueError('CONFIDENCE LEVEL MUST BE BETWEEN 0 AND 1')
  if degrees <= 0:
    raise ValueError('DEGREES OF FREEDOM MUST BE POSITIVE')
  return t_quantile((1+confidence)/2,degrees)

def t_cdf(value, degrees):
  if degrees <= 0:
    raise ValueError('DEGREES OF FREEDOM MUST BE POSITIVE')
  return _t_cdf(value,degrees)
def t_sf(value,degrees):
  return t_cdf(-value,degrees)
def t_interval(low,high,degrees):
  if low > high:
    raise ValueError('LOWER t VALUE MUST NOT EXCEED UPPER t VALUE')
  if low >= 0:
    return t_sf(low,degrees)-t_sf(high,degrees)
  if high <= 0:
    return t_cdf(high,degrees)-t_cdf(low,degrees)
  return 1-t_cdf(low,degrees)-t_sf(high,degrees)
def t_quantile(probability, degrees):
  if not 0 < probability < 1:
    raise ValueError('AREA TO LEFT MUST BE BETWEEN 0 AND 1')
  if degrees <= 0:
    raise ValueError('DEGREES OF FREEDOM MUST BE POSITIVE')
  if probability == 0.5:
    return 0.0
  if probability < 0.5:
    return -t_quantile(1-probability,degrees)
  low,high = 0.0,1.0
  while _t_cdf(high,degrees) < probability:
    high *= 2
    if high > 1e100:
      raise ValueError('PERCENTILE IS TOO EXTREME TO CALCULATE')
  for _ in range(60):
    middle=(low+high)/2
    if _t_cdf(middle,degrees) < probability:
      low=middle
    else:
      high=middle
  return (low+high)/2

def regression_inference(ts,df,alpha):
  return t_critical(1-alpha,df),0.0 if ts is None else 2*t_sf(abs(ts),df)
