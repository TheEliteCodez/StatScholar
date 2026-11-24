import STCORE as c

def chi(ts,df,alpha,p,cv):
  key=c.menu('CHI-SQUARE GRAPH',[('1','REJECTION REGION'),('2','p-VALUE REGION')])
  if key=='0':return 'back'
  return chi_region(ts,df,alpha,p,cv,key)

def chi_region(ts,df,alpha,p,cv,key):
  return c.call('STGCHI','show',ts,df,alpha,p,cv,key)

def chi_screens(ts,df,alpha,p,cv):
  for key in ('1','2'):
    action=chi_region(ts,df,alpha,p,cv,key)
    if action!='next': return action
  return 'next'

def correlation(ts,df,alpha,p,critical):
  key=c.menu('CORRELATION TEST GRAPH',[('1','REJECTION REGION'),('2','p-VALUE REGION')])
  if key=='0':return 'back'
  if ts is None:
    return c.view('PERFECT CORRELATION',['|t| IS INFINITE; p=0.','NO FINITE TEST-STATISTIC MARK.'])
  return c.call('STGRT','show',ts,df,alpha,p,critical,key)
