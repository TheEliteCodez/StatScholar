import STCORE as c
from STCLTC import _read_number
from STCLTM import normal_cdf, normal_sf, normal_interval

def _event_probability(mean,se,sketch=None):
    event = c.menu('WHAT PROBABILITY IS ASKED?',[
        ('1','BELOW A VALUE'),
        ('2','ABOVE A VALUE'),
        ('3','BETWEEN TWO VALUES')])
    if event == '0':
        return None
    if event == '1':
        bound = _read_number('CUTOFF VALUE: ')
        if sketch is not None:
            sketch.extend(['MARK CUTOFF: %.4f' % bound,'SHADE LEFT OF CUTOFF.'])
        if se == 0:
            return ('P(BELOW)',1.0 if mean < bound else 0.0,
                    'BOUNDARY z: DNE (SD=0)')
        z = (bound-mean)/se
        return ('P(BELOW)',normal_cdf(z),'z=(cutoff-mean)/SE=(%.10g-%.10g)/%.10g=%.4f' % (bound,mean,se,z))
    if event == '2':
        bound = _read_number('CUTOFF VALUE: ')
        if sketch is not None:
            sketch.extend(['MARK CUTOFF: %.4f' % bound,'SHADE RIGHT OF CUTOFF.'])
        if se == 0:
            return ('P(ABOVE)',1.0 if mean > bound else 0.0,
                    'BOUNDARY z: DNE (SD=0)')
        z = (bound-mean)/se
        return ('P(ABOVE)',normal_sf(z),'z=(cutoff-mean)/SE=(%.10g-%.10g)/%.10g=%.4f' % (bound,mean,se,z))
    low = _read_number('LOWER VALUE: ')
    high = _read_number('UPPER VALUE: ')
    if low > high:
        raise ValueError('LOWER VALUE MUST NOT EXCEED UPPER VALUE')
    if sketch is not None:
        sketch.extend(['MARK LOWER: %.4f' % low,'MARK UPPER: %.4f' % high,
                       'SHADE BETWEEN THE CUTOFFS.'])
    if se == 0:
        probability = 1.0 if low <= mean <= high else 0.0
        return ('P(BETWEEN)',probability,'MEAN=%.4f; SE=0' % mean)
    zlow,zhigh = (low-mean)/se,(high-mean)/se
    probability = normal_interval(zlow,zhigh)
    return ('P(BETWEEN)',probability,
            'z lower=(%.10g-%.10g)/%.10g=%.4f; z upper=(%.10g-%.10g)/%.10g=%.4f' % (low,mean,se,zlow,high,mean,se,zhigh))

def _result(title,statistic,mean,se,n,conditions,distribution,context,
            probability_allowed,find_probability,input_label,population_sd=None,fallback=None):
    lines = ['INPUT CHECK: n=%d; %s=%.4f; SE=%.4f' %
             (n,input_label,mean,se)]
    if context:
        lines.append('CONTEXT: '+context)
    lines.extend(['SAMPLING DISTRIBUTION: '+distribution,
                  'MEAN OF '+statistic+'=%.4f' % mean,
                  'SD OF '+statistic+'=SE=%.4f' % se])
    lines.extend(conditions)
    if find_probability and not probability_allowed:
        lines.append('NORMAL PROBABILITY NOT CALCULATED: CHECK FAILED ASSUMPTIONS.')
        c.view(title,lines)
        if fallback:
            c.call('STCLTF',*fallback)
        return
    sketch = []
    if find_probability:
        event = _event_probability(mean,se,sketch)
        if event is None:
            return
        label,probability,work = event
        if probability < 1e-6:
            answer='%s=%.6e (%.6e%%)' % (
                label,probability,100*probability)
        else:
            answer='%s=%.6f (%.4f%%)' % (
                label,probability,100*probability)
        lines.extend([work,answer])
    lines.extend(['HOW TO DRAW: '+statistic,
                  'HORIZONTAL AXIS: '+statistic,
                  'CENTER / MEAN: %.4f' % mean,
                  'SD / TICK SPACING: %.4f' % se])
    if se == 0:
        lines.append('ONE POINT AT MEAN; SD=0.')
    elif 'NOT' in distribution:
        lines.append('BELL SHAPE NOT ESTABLISHED.')
    else:
        lines.extend(['DRAW A SYMMETRIC BELL.',
                      'TALLEST AT THE CENTER.',
                      'TAPER BOTH TAILS TO AXIS.',
                      'AXIS TICKS (LEFT TO RIGHT):'])
        lines.extend(['%+d SD: %.4f' % (i,mean+i*se) for i in range(-3,4)])
    if find_probability:
        lines.extend(sketch+[answer])
        if se > 0:
            lines.extend(['SAME SHADED AREA ON z CURVE:',
                          'CENTER=0; SD=1',work,
                          'USE SAME SHADING DIRECTION.'])
    if population_sd is not None:
        lines.extend(['COMPARE WITH INDIVIDUAL X:',
                      'SAME CENTER: %.4f' % mean,
                      'INDIVIDUAL SD: %.4f' % population_sd,
                      'x-bar IS NARROWER IF SE<SD.',
                      'USE SAME AXIS SCALE TO COMPARE.',
                      'NORMAL POPULATION: BOTH BELLS.',
                      'CLT ALONE DOES NOT MAKE X NORMAL.'])
    graph=None
    if se==0 or (probability_allowed and 'NOT' not in distribution):
        bounds=tuple(float(x.split(': ')[1]) for x in sketch if x.startswith(('MARK CUTOFF:','MARK LOWER:','MARK UPPER:')))
        shading=('3' if len(bounds)==2 else '1' if event[0]=='P(BELOW)' else '2') if find_probability else None
        graph=('STGCURV','show',('NORMAL',mean,se,shading,bounds,statistic,probability if find_probability else None))
    if graph: c.view(title,c.graph_lines(lines,graph))
    else: c.view(title,lines)
