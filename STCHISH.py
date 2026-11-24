import STCORE as c

def show(data):
  table,label,random,alpha,nc,observed,expected,ts,df,p,cv,fitted,rt,ct=data
  graph=('STGINFER','chi',(ts,df,alpha,p,cv))
  action=c.view('CHI '+('INDEPENDENCE' if table else 'GOF')+' ANSWER',
    c.graph_lines(c.call('STCHRES','summary',ts,df,alpha,p,cv),graph))
  if action in ('back','exit'): return
  plotted=False
  if c.ON_TI:
    for key in ('1','2'):
      plotted=c.call('STGCHI','show',ts,df,alpha,p,cv,key)
      if plotted!='next': break
  action=c.view('TI-84 CHI-SQUARE STEPS',
    c.call('STCHITI','steps',observed,expected,nc,df,alpha,ts,p,cv,table))
  if action in ('back','exit'): return
  action=c.view('CHI-SQUARE TEST',c.call('STCHRES','work',data,bool(plotted)))
  if action in ('back','exit'):return
  c.view('CHI-SQUARE FINAL CONCLUSION',c.call('STCHEND','conclusion',data))
