import math
import STCORE as c
from STDIST import _number, _probability, _probability_text

def _uniform_cdf(value, low, high):
    if value <= low:
        return 0.0
    if value >= high:
        return 1.0
    return (value-low)/(high-low)

def _uniform_probability(low, high):
    event = c.menu('UNIFORM > FIND PROBABILITY', [
        ('1', 'BELOW A VALUE'),
        ('2', 'ABOVE A VALUE'),
        ('3', 'BETWEEN TWO VALUES')])
    if event == '0':
        return
    if event == '1':
        value = _number('VALUE x: ')
        probability = _uniform_cdf(value, low, high)
        label = 'P(X < %.4f)' % value
    elif event == '2':
        value = _number('VALUE x: ')
        probability = 1-_uniform_cdf(value, low, high)
        label = 'P(X > %.4f)' % value
    else:
        lower = _number('LOWER VALUE: ')
        upper = _number('UPPER VALUE: ')
        if lower > upper:
            raise ValueError('LOWER VALUE MUST NOT EXCEED UPPER VALUE')
        probability = max(0.0, min(upper, high)-max(lower, low))/(high-low)
        label = 'P(%.4f < X < %.4f)' % (lower, upper)
    c.view('UNIFORM > PROBABILITY', [
        'X UNIFORM ON [%.4f, %.4f]' % (low, high),
        label,
        _probability_text(probability)]+c.call('STSKETCH','curve','UNIFORM',low,high,event,
            (lower,upper) if event=='3' else (value,)))

def _uniform_percentile(low, high):
    request=c.call('STDIST','cutoff_request')
    if request is None: return
    probability,shading,work=request
    cutoff = low+probability*(high-low)
    answer='VALUE CUTOFF x=%.4f' % cutoff
    if c.view('UNIFORM > PERCENTILE ANSWER',[
        answer,'AREA TO LEFT=%.6f' % probability,
        'x=a+LEFT AREA*(b-a)']+work) in ('back','exit'): return
    c.view('UNIFORM > PERCENTILE', [
        answer,
        'X UNIFORM ON [%.4f, %.4f]' % (low, high),
        'AREA TO LEFT=%.4f (%.2f%%)' % (probability, 100*probability),
        'x=a+LEFT AREA*(b-a)']+
        c.call('STSKETCH','curve','UNIFORM',low,high,shading,(cutoff,)))

def _uniform_axes(low, high):
    c.view('UNIFORM > DRAW / LABEL', [
        'X UNIFORM ON [a,b]=[%.4f, %.4f]' % (low, high),
        'MEAN=(a+b)/2=%.4f' % ((low+high)/2),
        'SD=(b-a)/sqrt(12)=%.4f' % ((high-low)/math.sqrt(12)),
        'CONSTANT HEIGHT=1/(b-a)=%.4f' % (1/(high-low)),
        'DRAW A RECTANGLE FROM a TO b; SHADE REQUESTED AREA.'])

def uniform_menu():
    low = _number('LOWER ENDPOINT a: ')
    high = _number('UPPER ENDPOINT b: ')
    if low >= high:
        raise ValueError('UPPER ENDPOINT b MUST EXCEED LOWER ENDPOINT a')
    while True:
        key = c.menu('UNIFORM > CONTINUOUS DISTRIBUTION', [
            ('1', 'MEAN / STANDARD DEVIATION / GRAPH'),
            ('2', 'FIND A PROBABILITY'),
            ('3', 'FIND A PERCENTILE / CUTOFF')])
        if key == '0':
            return
        if key == '1':
            _uniform_axes(low, high)
        elif key == '2':
            _uniform_probability(low, high)
        else:
            _uniform_percentile(low, high)
