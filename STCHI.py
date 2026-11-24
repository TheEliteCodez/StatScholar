import STCORE as c

def session(table=False,display=True):
  fitted=0;rt=ct=None
  label=input('POPULATION / CATEGORY LABEL (ENTER=SKIP): ').strip()
  random=c.call('STHYIO','check','RANDOM INDEPENDENT OBSERVATIONS?')
  if random is None: return
  alpha=c.read_number('SIGNIFICANCE alpha: ')
  if not 0<alpha<1: raise ValueError('USE 0<alpha<1')
  if table:
    nr=c.read_size('ROW COUNT: ',10,2);nc=c.read_size('COLUMN COUNT: ',10,2)
    rows=[[c.read_int('COUNT R%d C%d: ' % (i+1,j+1)) for j in range(nc)] for i in range(nr)]
    expected,ts,df,rt,ct=c.call('STCHIM','independence',rows)
    observed=[o for row in rows for o in row]
  else:
    nr=1;nc=c.read_size('NUMBER OF CATEGORIES: ',c.MAX_OUTCOMES,2)
    observed=[c.read_int('OBSERVED COUNT %d: ' % (i+1)) for i in range(nc)]
    key=c.menu('EXPECTED FREQUENCIES',[('1','ALL EQUALLY LIKELY'),('2','GIVEN EXPECTED COUNTS'),('3','GIVEN PROBABILITIES')])
    if key=='0': return
    total=sum(observed)
    if key=='1': expected=[total/nc]*nc
    else:
      expected=[c.read_number(('EXPECTED COUNT ' if key=='2' else 'PROBABILITY ')+str(i+1)+': ') for i in range(nc)]
      if key=='3':
        if abs(sum(expected)-1)>1e-7: raise ValueError('PROBABILITIES MUST SUM TO 1')
        expected=[total*p for p in expected]
    fitted=c.read_int('PARAMETERS ESTIMATED FROM SAMPLE (0 IF NONE): ')
    ts,df=c.call('STCHIM','goodness',observed,expected,fitted)
  probability=c.call('STCHIM','survival',ts,df)
  cv=c.call('STCHIM','critical',alpha,df)
  payload=(table,label,random,alpha,nc,observed,expected,ts,df,probability,cv,fitted,rt,ct)
  if not display: return payload
  return c.call('STCHISH','show',payload)
