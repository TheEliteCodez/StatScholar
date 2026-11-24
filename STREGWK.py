import STCORE as c

class PairWork:
  def __init__(self,points,result):
    self.points=points;self.result=result
  def __len__(self): return len(self.points)
  def __iter__(self):
    for i in range(len(self.points)):
      x,y=self.points[i];dx=x-self.result['mx'];dy=y-self.result['my']
      predicted=self.result['my']+self.result['slope']*(x-self.result['mx'])
      yield 'PAIR %d: x=%g y=%g; dx=%g dy=%g; dx^2=%g dy^2=%g dx*dy=%g; yhat=%.10g; e=%g-%.10g=%.10g' % (i+1,x,y,dx,dy,dx*dx,dy*dy,dx*dy,predicted,y,predicted,y-predicted)

class RegressionWork(PairWork):
  def __init__(self,points,result,alpha,xlabel,ylabel):
    PairWork.__init__(self,points,result)
    self.alpha=alpha;self.xlabel=xlabel;self.ylabel=ylabel
  def __len__(self): return len(self.points)+(26 if self.result['r'] is None else 36)
  def __iter__(self):
    result=self.result;alpha=self.alpha;xlabel=self.xlabel;ylabel=self.ylabel
    r = result['r']
    p = result['p']
    yield 'y=%.6g*x%+.6g' % (result['slope'],result['intercept'])
    yield 'n=%d; df=%d' % (result['n'],result['df'])
    yield 'r: UNDEFINED (CONSTANT y)' if r is None else 'r=%.6g; r^2=%.6g' % (r,result['r2'])
    yield 'p: UNDEFINED' if p is None else 'p=%.6g; alpha=%.5g' % (p,alpha)
    yield 'CRITICAL r: UNDEFINED' if r is None else 'CRITICAL |r|=%.6g' % result['rc']
    yield 'xbar=%.6g; ybar=%.6g' % (result['mx'],result['my'])
    yield 'SLOPE=%.5g; INT=%.5g' % (result['slope'],result['intercept'])
    yield 'NO CORRELATION TEST' if r is None else 'REJECT H0' if p<=alpha else 'FAIL TO REJECT H0'
    yield ('yhat=%.10g*x %s %.10g' % (result['slope'], '-' if result['intercept'] < 0 else '+', abs(result['intercept'])))
    yield ('SLOPE b=%.10g' % result['slope'])
    yield ('INTERCEPT a=%.10g' % result['intercept'])
    yield ('x: ' + xlabel)
    yield ('y: ' + ylabel)
    yield ('n=%d; df=n-2=%d' % (result['n'], result['df']))
    yield ('xbar=%.10g; ybar=%.10g' % (result['mx'], result['my']))
    yield ('Sxx=SUM((x-xbar)^2)=%.10g' % result['xx'])
    yield ('Syy=SUM((y-ybar)^2)=%.10g' % result['yy'])
    yield ('Sxy=SUM((x-xbar)*(y-ybar))=%.10g' % result['xy'])
    yield ('b=Sxy/Sxx=%.10g/%.10g=%.10g' % (result['xy'], result['xx'], result['slope']))
    yield ('a=ybar-b*xbar=%.10g-%.10g*%.10g=%.10g' % (result['my'], result['slope'], result['mx'], result['intercept']))
    yield ('yhat=%.10g+%.10g*x' % (result['intercept'], result['slope']))
    yield 'USE CENTERED FORM FOR PREDICTION: ybar+b*(x-xbar)'
    yield ('SLOPE: FITTED y CHANGES BY %.10g y UNITS PER 1 x UNIT.' % result['slope'])
    yield 'H0: rho=0; H1: rho!=0; TWO-SIDED'
    yield 'REQUIRE INDEPENDENT RANDOM PAIRS, APPROXIMATELY LINEAR RELATIONSHIP; NORMAL HOMOSCEDASTIC ERRORS FOR t INFERENCE; CHECK OUTLIERS.'
    if r is None:
      yield 'CONSTANT y: r, r^2 AND CORRELATION INFERENCE UNDEFINED.'
    else:
      yield ('r=Sxy/sqrt(Sxx*Syy)=%.10g/sqrt(%.10g*%.10g)=%.10g' % (result['xy'], result['xx'], result['yy'], r))
      yield ('r^2=%.10g; EXPLAINED VARIATION=%.6g%%' % (result['r2'], 100 * result['r2']))
      yield ('About %.4g%% of the variation in %s is explained by its linear relationship with %s. Variation means how much the %s values differ from their average. This is not the percent of predictions that are correct.' % (100*result['r2'],ylabel,xlabel,ylabel))
      yield ('CRITICAL r=+/-%.10g AT alpha=%.8g' % (result['rc'], alpha))
      yield 'r*=t*/sqrt(t*^2+df); SAME TWO-SIDED THRESHOLD AS r TABLE.'
      yield 't=r*sqrt((n-2)/(1-r^2))'
      yield ('PERFECT FIT: |t| IS INFINITE.' if result['ts'] is None else 't=%.10g*sqrt(%d/(1-%.10g^2))=%.10g' % (r, result['df'], r, result['ts']))
      yield ('p=2*P(T_%d >= |t|)=%.10g' % (result['df'], p))
      yield ('REJECT H0' if p <= alpha else 'FAIL TO REJECT H0')
      yield (('SUFFICIENT' if p <= alpha else 'INSUFFICIENT') + ' EVIDENCE OF LINEAR CORRELATION, IF REQUIREMENTS HOLD.')
      yield 'ASSOCIATION DOES NOT ESTABLISH CAUSATION.'
    for line in PairWork.__iter__(self): yield line

def show(points,result,alpha,xlabel,ylabel,paired=False):
  if paired: c.view('PAIRED WORK TABLE',PairWork(points,result))
  else: c.view('REGRESSION WORK / RESULTS',RegressionWork(points,result,alpha,xlabel,ylabel))
