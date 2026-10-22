import STCORE as c
from STTCRIT import t_cdf, t_sf, t_interval
_read_number=c.read_number

def t_probability_session(degrees,event):
    if degrees <= 0:
        raise ValueError('DEGREES OF FREEDOM MUST BE POSITIVE')
    if event == '1':
        value=_read_number('t VALUE: ')
        probability=t_cdf(value,degrees)
        label='P(T < %.4f)' % value
    elif event == '2':
        value=_read_number('t VALUE: ')
        probability=t_sf(value,degrees)
        label='P(T > %.4f)' % value
    else:
        low=_read_number('LOWER t VALUE: ')
        high=_read_number('UPPER t VALUE: ')
        if low > high:
            raise ValueError('LOWER t VALUE MUST NOT EXCEED UPPER t VALUE')
        probability=t_interval(low,high,degrees)
        label='P(%.4f < T < %.4f)' % (low,high)
    probability_text=('%.6e (%.6e%%)' % (probability,100*probability)
                     if probability<1e-6 else
                     '%.7f (%.4f%%)' % (probability,100*probability))
    c.view('STUDENT t PROBABILITY',[
        'DEGREES OF FREEDOM df=%d' % degrees,
        label,
        'PROBABILITY='+probability_text]+c.call('STSKETCH','curve','t',0,degrees,event,
            (low,high) if event=='3' else (value,)))
