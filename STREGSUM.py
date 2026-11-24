import math
import STCORE as c

def optional(prompt,default=None):
  while True:
    text=input(prompt).strip()
    if not text:return default
    try:return c._real(text)
    except (ValueError,ZeroDivisionError):print('USE NUMBER, A/B OR %')

def prepare(slope,intercept,r,n,mean,low,high,alpha=.05):
  if n<3:raise ValueError('CORRELATION TEST NEEDS n>=3')
  if not -1<=r<=1:raise ValueError('ENTER r BETWEEN -1 AND 1')
  if not 0<alpha<1:raise ValueError('USE 0<alpha<1')
  if low is not None and high is not None and low>high:raise ValueError('x MIN MUST NOT EXCEED x MAX')
  ts=None if abs(r)==1 else r*math.sqrt((n-2)/(1-r*r))
  tc,p=c.call('STTCRIT','regression_inference',ts,n-2,alpha)
  return {'slope':slope,'intercept':intercept,'r':r,'n':n,'mean':mean,
    'low':low,'high':high,'alpha':alpha,'p':p,'rc':tc/math.sqrt(tc*tc+n-2)}

def choose(data,x):
  if data['low'] is None or data['high'] is None:return 'DNE',None,'OBSERVED x RANGE NOT GIVEN.'
  if not data['low']<=x<=data['high']:return 'DNE',None,'x IS OUTSIDE OBSERVED RANGE.'
  if data['p']<=data['alpha']:
    return 'USE EQUATION',data['slope']*x+data['intercept'],'SIGNIFICANT LINEAR CORRELATION.'
  if data['mean'] is None:return 'DNE',None,'NO SIGNIFICANT CORRELATION; MEAN y NOT GIVEN.'
  return 'USE MEAN y',data['mean'],'NO SIGNIFICANT LINEAR CORRELATION.'

class PredictionRows:
  def __init__(self,data,x,places,units):
    self.data=data;self.x=x;self.places=places;self.units=units
  def __len__(self):return 20
  def __iter__(self):
    data=self.data;x=self.x;places=self.places;units=self.units
    method, value, reason = choose(data, x)
    answer = 'DNE' if value is None else ('%.' + str(places) + 'f') % value
    significant = data['p'] <= data['alpha']
    bounds = 'NOT GIVEN' if data['low'] is None or data['high'] is None else '%.6g..%.6g' % (data['low'], data['high'])
    yield ('ANSWER=' + answer + (' ' + units if value is not None and len(answer) + len(units) < 23 else ''))
    yield ('METHOD: ' + method)
    yield ('x=%.6g; RANGE: ' % x + bounds)
    yield ('r=%.5g; CRIT r=%.5g' % (data['r'], data['rc']))
    yield ('n=%d; alpha=%.5g' % (data['n'], data['alpha']))
    yield ('p=%.6g %s alpha' % (data['p'], '<=' if significant else '>'))
    yield ('MEAN y=' + ('NOT GIVEN' if data['mean'] is None else '%.6g' % data['mean']))
    yield data.get('equation','y=%.6g*x%+.6g' % (data['slope'],data['intercept']))
    yield ('UNITS: ' + units)
    yield reason
    yield 'H0: rho=0; H1: rho!=0'
    yield ('REJECT H0' if significant else 'FAIL TO REJECT H0')
    yield ('BECAUSE p=%.8g %s alpha=%.8g' % (data['p'], '<=' if significant else '>', data['alpha']))
    yield (('SUFFICIENT' if significant else 'INSUFFICIENT') + ' EVIDENCE OF LINEAR CORRELATION.')
    yield ('|r|=%.8g %s CRITICAL r=%.8g' % (abs(data['r']), '>=' if significant else '<', data['rc']))
    yield ('TWO-SIDED TEST; df=n-2=%d' % (data['n'] - 2))
    yield 'TEXTBOOK PREDICTION RULE:'
    yield 'OUTSIDE OBSERVED RANGE: DNE.'
    yield 'WITHIN RANGE: SIGNIFICANT r -> EQUATION; OTHERWISE MEAN y.'
    yield ('EQUATION SUBSTITUTION: %.8g*%.8g%+.8g=%.8g' % (data['slope'], x, data['intercept'], data['slope'] * x + data['intercept']))

def show(data,x,places,units):
  c.view('GIVEN REGRESSION: ANSWER',PredictionRows(data,x,places,units))

def session():
  form=c.menu('GIVEN EQUATION FORM',[('1','y=ax+b'),('2','y=a+bx')])
  if form=='0':return
  c.heading('COPY GIVEN REGRESSION')
  print('y=ax+b' if form=='1' else 'y=a+bx')
  print('a: x COEFFICIENT; b: CONSTANT' if form=='1' else 'a: CONSTANT; b: x COEFFICIENT')
  print('r^2 IS NOT NEEDED HERE.')
  a=c.read_number('SLOPE (a=) (x COEFFICIENT): ' if form=='1' else 'INTERCEPT (a=) (CONSTANT): ')
  b=c.read_number('INTERCEPT (b=) (CONSTANT): ' if form=='1' else 'SLOPE (b=) (x COEFFICIENT): ')
  slope,intercept=(a,b) if form=='1' else (b,a)
  r=c.read_number('CORRELATION r (NOT r^2): ')
  n=c.read_int('NUMBER OF PAIRS n: ')
  alpha=optional('alpha (ENTER=.05): ',.05)
  mean=optional('MEAN y (ENTER=NOT GIVEN): ')
  low=optional('OBSERVED x MIN (ENTER=UNKNOWN): ')
  high=optional('OBSERVED x MAX (ENTER=UNKNOWN): ')
  units=input('y VARIABLE / UNITS (ENTER=SKIP): ').strip() or 'y'
  data=prepare(slope,intercept,r,n,mean,low,high,alpha)
  data['equation']=('y=%.6g*x%+.6g' if form=='1' else 'y=%.6g%+.6g*x') % (a,b)
  while True:
    x=c.read_number('x TO PREDICT: ')
    places=c.read_int('ANSWER DECIMAL PLACES: ')
    show(data,x,places,units)
    if c.menu('GIVEN REGRESSION > NEXT',[('1','ANOTHER x / SAME MODEL')])=='0':return
