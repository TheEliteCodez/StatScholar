import STCORE as c

def menu():
  while True:
    key=c.menu('LINEAR REGRESSION',[('1','ENTER DATA / FIT / PREDICT'),('2','REGRESSION DEFINITIONS'),('3','GIVEN EQUATION / r / n')])
    if key=='0': return
    if key=='1': session()
    elif key=='2': c.call('STREGDEF','menu')
    else: c.call('STREGSUM','session')

def read_pairs(minimum=3): return c.call('STREGIN','read_pairs',minimum)
def rounded_prediction(result,ylabel): return c.call('STREGPR','rounded_prediction',result,ylabel)

def session():
  data=c.call('STREGIN','read')
  if data is None: return
  points,xlabel,ylabel,alpha=data
  data=None
  result=c.call('STREG','fit',points,alpha,False)
  if result['r'] is not None:
    tc,p=c.call('STTCRIT','regression_inference',result['ts'],result['df'],alpha)
    result['tc']=tc;result['p']=p;result['rc']=tc/(tc*tc+result['df'])**.5
  first=True
  while True:
    key='1' if first else c.menu('REGRESSION / CORRELATION',[('1','ALL WORK / RESULTS'),('2','SCATTER + REGRESSION LINE'),
      ('3','PREDICT y FROM x'),('4','RESIDUAL: OBSERVED - PREDICTED'),('5','PAIRED WORK TABLE'),('6','REGRESSION LINE ONLY'),('7','RESIDUAL GRAPH'),('8','TEST DISTRIBUTION GRAPH'),('9','ROUND EQUATION / PREDICTION'),('10','REGRESSION DEFINITIONS'),('11','SCATTERPLOT ONLY')])
    first=False
    if key=='0': return
    if key=='9': rounded_prediction(result,ylabel)
    elif key=='10': c.call('STREGDEF','menu')
    elif key in ('2','6','7','11'):
      if not c.call('STGSCAT','show',points,xlabel,ylabel,(result['intercept'],result['slope']) if key!='11' else None,key=='7',key=='6'):
        c.call('STREGTXT','show',points,xlabel,ylabel,(result['intercept'],result['slope']) if key!='11' else None,key=='7',key=='6')
    elif key=='8':
      if result['r'] is None: c.view('NO CORRELATION INFERENCE',['CONSTANT y: CORRELATION UNDEFINED.'])
      else:
        critical=result['tc']
        c.call('STGINFER','correlation',result['ts'],result['df'],alpha,result['p'],critical)
    elif key in ('3','4'): c.call('STREGPR','show',result,points,ylabel,key=='4')
    elif key=='5': c.call('STREGWK','show',points,result,alpha,xlabel,ylabel,True)
    else:
      c.call('STREGWK','show',points,result,alpha,xlabel,ylabel)
