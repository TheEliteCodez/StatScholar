def heading(setup,result,probability,critical,region):
  import ti_plotlib as plt
  BLACK=(0,0,0);RED=(210,45,45);BLUE=(0,100,210)
  ts=result['ts'];df=result['df'];alt=setup['alternative'];alpha=setup['alpha']
  plt.color(*BLACK)
  kind='z' if df is None else 't'
  plt.text_at(1,'STANDARD NORMAL (z)' if df is None else 't DISTRIBUTION df=%.5g' % df,'center')
  tail={'<':'LEFT','>':'RIGHT','!=':'TWO-TAILED'}[alt]
  plt.text_at(2,tail+(' REJECTION REGION' if region!='p' else ' p-VALUE REGION'),'center')
  if region=='p':
    plt.text_at(10,'SHADE '+('LEFT OF TS' if alt=='<' else 'RIGHT OF TS' if alt=='>' else 'BEYOND +/-abs(TS)'),'center')
    plt.color(*BLUE);plt.text_at(11,'p-VALUE=%.6g' % probability,'center')
  else:
    comparison=('TS' if alt!='!=' else '|TS|')
    a,b=(abs(ts),critical[-1]) if alt=='!=' else (ts,critical[0])
    comparison+=' > CV' if a>b else ' < CV' if a<b else ' = CV'
    plt.text_at(10,comparison+(': REJECT H0' if probability<=alpha else ': FAIL TO REJECT H0'),'center')
    plt.color(*RED);plt.text_at(11,'SHADE '+('LEFT OF CV' if alt=='<' else 'RIGHT OF CV' if alt=='>' else 'BOTH OUTSIDE CVs')+'; alpha=%.4g' % alpha,'center')
  plt.color(*BLACK);plt.text_at(12,'LEFT/CLEAR:BACK ENTER:NEXT','center')
  return plt
