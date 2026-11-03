import math

def normal_cdf(z):
    x = abs(z)
    t = 1/(1+0.2316419*x)
    density = 0.3989422804014327*math.exp(-x*x/2)
    tail = density*t*(0.319381530+t*(-0.356563782+t*(1.781477937+t*(-1.821255978+t*1.330274429))))
    return 1-tail if z >= 0 else tail

def normal_sf(z):
    return normal_cdf(-z)

def normal_interval(low,high):
    if low > high:
        raise ValueError('LOWER z VALUE MUST NOT EXCEED UPPER z VALUE')
    if low >= 0:
        return normal_sf(low)-normal_sf(high)
    if high <= 0:
        return normal_cdf(high)-normal_cdf(low)
    return 1-normal_cdf(low)-normal_sf(high)

def mean_standard_error(sigma,n):
    if sigma < 0 or n < 1:
        raise ValueError('SD MUST BE NONNEGATIVE AND SAMPLE SIZE POSITIVE')
    return sigma/math.sqrt(n)

def proportion_standard_error(p,n):
    if not 0 <= p <= 1 or n < 1:
        raise ValueError('USE 0 <= p <= 1 AND SAMPLE SIZE POSITIVE')
    return math.sqrt(p*(1-p)/n)
