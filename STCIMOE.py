import STCORE as c
from STCIIO import _read_number, _read_confidence, _show_zstar
from STCINUM import proportion_margin_error, mean_margin_error, proportion_margin_error_estimate
def _margin_error():
    key = c.menu('MARGIN OF ERROR',[
        ('1','PROPORTION (x,n)'),
        ('2','MEAN (sigma OR estimated s,n)'),
        ('3','PROPORTION (p-hat,n)')])
    if key == '0':
        return
    confidence = _read_confidence()
    if key == '1':
        successes = c.read_int('NUMBER WITH EVENT (successes x): ')
        n = c.read_int('TOTAL NUMBER SAMPLED (n): ')
        estimate,se,critical,margin = proportion_margin_error(successes,n,confidence)
        values = ['p-hat='+('%.4f' % estimate),
                  'STANDARD ERROR='+('%.4f' % se),
                  'MARGIN OF ERROR='+('%.4f' % margin)]
    elif key == '2':
        sigma = _read_number('POPULATION SD sigma (OR SAMPLE SD s): ')
        n = c.read_int('TOTAL NUMBER SAMPLED (n): ')
        se,critical,margin = mean_margin_error(sigma,n,confidence)
        values = ['STANDARD ERROR='+('%.4f' % se),
                  'MARGIN OF ERROR='+('%.4f' % margin)]
    else:
        estimate=_read_number('SAMPLE PROPORTION p-hat (DECIMAL OR PERCENT): ')
        n=c.read_int('TOTAL NUMBER SAMPLED (n): ')
        estimate,se,critical,margin=proportion_margin_error_estimate(
            estimate,n,confidence)
        values=['p-hat='+('%.4f' % estimate),
                'STANDARD ERROR='+('%.4f' % se),
                'MARGIN OF ERROR='+('%.4f' % margin)]
    _show_zstar('MARGIN OF ERROR',confidence,critical,values)
def _interval_from_estimate_and_margin():
    kind=c.menu('GIVEN POINT ESTIMATE + MARGIN OF ERROR',[
        ('1','PROPORTION p-hat'),
        ('2','MEAN x-bar')])
    if kind == '0':
        return
    estimate=_read_number('POINT ESTIMATE / CENTER: ')
    margin=_read_number('MARGIN OF ERROR E: ')
    if margin < 0:
        raise ValueError('MARGIN OF ERROR MUST NOT BE NEGATIVE')
    if kind == '1' and not 0 <= estimate <= 1:
        raise ValueError('PROPORTION ESTIMATE MUST BE BETWEEN 0 AND 1')
    low,high=estimate-margin,estimate+margin
    lines=['POINT ESTIMATE='+('%.4f' % estimate),
           'MARGIN OF ERROR E=%.4f' % margin,
           'INTERVAL=(%.4f, %.4f)' % (low,high)]
    if kind == '1':
        lines.append('PROPORTION BOUNDS '+(
            'EXTEND OUTSIDE [0,1]; NOT CLAMPED.' if low < 0 or high > 1
            else 'ARE WITHIN [0,1].'))
    c.view('INTERVAL FROM ESTIMATE +/- E',lines+[
        'HOW TO DRAW: INTERVAL', 'DRAW A HORIZONTAL NUMBER LINE.',
        'MARK LEFT=%.4f; RIGHT=%.4f' % (low,high),
        'CONNECT ENDS; CENTER=%.4f' % estimate])
