import STCORE as c

def step(index,setup,result,probability,critical,reject):
  null=setup['null'];alt=setup['alternative'];alpha=setup['alpha']
  parameter=setup['parameter'];kind='z' if result['df'] is None else 't'
  if index==7:
    ts=result['ts'];df=result['df']
    variable='Z' if df is None else 'T'
    distribution='STANDARD NORMAL (z)' if df is None else 't DISTRIBUTION; df=%.10g' % df
    command='normalcdf' if df is None else 'tcdf'
    suffix=',0,1)' if df is None else ',%.10g)' % df
    lower=command+'(-9999,%.10g' % ts+suffix
    upper=command+'(%.10g,9999' % ts+suffix
    expression=lower if alt=='<' else upper if alt=='>' else '2*'+(lower if ts<0 else upper)
    if alt=='<':
      work=['LEFT-TAILED TEST',
         'p=P(%s <= %.10g)' % (variable,ts),
         'LEFT-TAIL AREA=%.10g' % probability]
    elif alt=='>':
      work=['RIGHT-TAILED TEST',
         'p=P(%s >= %.10g)' % (variable,ts),
         'p=1-P(%s <= %.10g)' % (variable,ts),
         'p=1-%.10g=%.10g' % (1-probability,probability)]
    else:
      work=['TWO-TAILED TEST',
         'p=P(%s <= -%.10g)+P(%s >= %.10g)' % (variable,abs(ts),variable,abs(ts)),
         'p=2*P(%s >= %.10g)' % (variable,abs(ts)),
         'TWO TAILS: p=2*%.10g=%.10g' % (probability/2,probability)]
    return [distribution]+work+[
        'TI APPROX: '+expression,
        'p-VALUE=%.10g' % probability,
        'SHADE '+('LEFT OF TS.' if alt=='<' else 'RIGHT OF TS.' if alt=='>' else 'BOTH TAILS BEYOND +/-abs(TS).'),
        '9999 APPROXIMATES INFINITY ON THE TI.',
        'IF H0 WERE TRUE, ABOUT %.6g%% OF RANDOM SAMPLES WOULD GIVE A TEST STATISTIC THIS EXTREME OR MORE EXTREME IN THE TESTED TAIL(S).' % (100*probability),
        'p IS NOT THE PROBABILITY THAT H0 IS TRUE.']
