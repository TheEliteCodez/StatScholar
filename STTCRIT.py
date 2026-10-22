import math
from STZCRIT import _validate_confidence
def _log_gamma(z):
    coefficients = (676.5203681218851, -1259.1392167224028,
                    771.32342877765313, -176.61502916214059,
                    12.507343278686905, -0.13857109526572012,
                    9.9843695780195716e-6, 1.5056327351493116e-7)
    if z < 0.5:
        return math.log(math.pi) - math.log(math.sin(math.pi*z)) - _log_gamma(1-z)
    z -= 1
    x = 0.99999999999980993
    for i in range(len(coefficients)):
        x += coefficients[i] / (z+i+1)
    t = z + len(coefficients) - 0.5
    return 0.5*math.log(2*math.pi) + (z+0.5)*math.log(t) - t + math.log(x)
def _beta_fraction(a, b, x):
    qab, qap, qam = a+b, a+1, a-1
    cval = 1.0
    dval = 1 - qab*x/qap
    if abs(dval) < 1e-30:
        dval = 1e-30
    dval = 1/dval
    result = dval
    for m in range(1, 201):
        m2 = 2*m
        aa = m*(b-m)*x/((qam+m2)*(a+m2))
        dval = 1+aa*dval
        if abs(dval) < 1e-30:
            dval = 1e-30
        cval = 1+aa/cval
        if abs(cval) < 1e-30:
            cval = 1e-30
        dval = 1/dval
        result *= dval*cval
        aa = -(a+m)*(qab+m)*x/((a+m2)*(qap+m2))
        dval = 1+aa*dval
        if abs(dval) < 1e-30:
            dval = 1e-30
        cval = 1+aa/cval
        if abs(cval) < 1e-30:
            cval = 1e-30
        dval = 1/dval
        delta = dval*cval
        result *= delta
        if abs(delta-1) < 3e-7:
            break
    return result
def _regularized_beta(x, a, b):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    factor = math.exp(_log_gamma(a+b)-_log_gamma(a)-_log_gamma(b)
                      + a*math.log(x) + b*math.log(1-x))
    if x < (a+1)/(a+b+2):
        return factor*_beta_fraction(a,b,x)/a
    return 1-factor*_beta_fraction(b,a,1-x)/b
def _t_cdf(value, degrees):
    x = degrees/(degrees+value*value)
    tail = 0.5*_regularized_beta(x,degrees/2,0.5)
    return 1-tail if value >= 0 else tail
def t_critical(confidence, degrees):
    _validate_confidence(confidence)
    if degrees <= 0:
        raise ValueError('DEGREES OF FREEDOM MUST BE POSITIVE')
    target = (1+confidence)/2
    low, high = 0.0, 1.0
    while _t_cdf(high,degrees) < target:
        high *= 2
    for _ in range(60):
        middle = (low+high)/2
        if _t_cdf(middle,degrees) < target:
            low = middle
        else:
            high = middle
    return (low+high)/2
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
