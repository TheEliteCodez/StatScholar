import STCORE as c

def rounded_prediction(result,ylabel):
  digits=c.read_int('EQUATION SIGNIFICANT DIGITS: ')
  places=c.read_int('PREDICTION DECIMAL PLACES: ')
  x=c.read_number('x TO PREDICT: ')
  predicted=result['my']+result['slope']*(x-result['mx'])
  slope=('%#.'+str(digits)+'g') % result['slope']
  intercept=('%#.'+str(digits)+'g') % abs(result['intercept'])
  sign=' - ' if result['intercept']<0 else ' + '
  c.view('ROUNDED MODEL / PREDICTION',[
    'PREDICTED y='+('%.'+str(places)+'f') % predicted,
    'x=%.8g' % x,'UNITS: '+ylabel,
    'EQUATION: %d SIGNIFICANT DIGITS' % digits,
    'yhat='+slope+'*x'+sign+intercept,
    'SLOPE='+slope,
    'INTERCEPT='+('' if result['intercept']>=0 else '-')+intercept,
    'x=%.10g; yhat=%.10g' % (x,predicted),
    'PREDICTED y='+('%.'+str(places)+'f') % predicted,
    'PREDICTION UNITS: '+ylabel,
    'PREDICTION USES UNROUNDED COEFFICIENTS.'])

def show(result,points,ylabel,residual=False):
  x=c.read_number('x TO PREDICT: ')
  predicted=result['my']+result['slope']*(x-result['mx'])
  lines=['yhat=ybar+b*(x-xbar)',
    'yhat=%.10g+%.10g*(%.10g-%.10g)=%.10g' % (result['my'],result['slope'],x,result['mx'],predicted),
    'PREDICTION UNITS: '+ylabel]
  if x<min(p[0] for p in points) or x>max(p[0] for p in points):
    lines.append('EXTRAPOLATION: OUTSIDE OBSERVED x RANGE.')
  if residual:
    y=c.read_number('OBSERVED y: ')
    lines=['RESIDUAL=%.8g' % (y-predicted),'OBSERVED y=%.8g' % y]+lines
    lines.append('RESIDUAL=y-yhat=%.10g-%.10g=%.10g' % (y,predicted,y-predicted))
  c.view('PREDICTION / RESIDUAL',c.summary(['PREDICTED y=%.8g' % predicted,'x=%.8g' % x])+lines)
