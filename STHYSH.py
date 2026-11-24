import STCORE as c

def show(setup,result,inference_result=None):
  if inference_result is None:
    inference_result=c.call('STHYP','inference',result['ts'],setup['alpha'],setup['alternative'],result['df'])
  probability,critical,reject=inference_result
  action=c.view('HYPOTHESIS: ANSWER',c.call('STHYANS','summary',setup,result,probability,critical,reject))
  labels=('REQUIREMENTS','H0 AND H1','POINT ESTIMATE','CRITICAL VALUES','TEST STATISTIC',
      'DRAW SAMPLING DISTRIBUTION','p-VALUE','INITIAL CONCLUSION','FINAL CONCLUSION')
  def display(index):
    if index==6 and c.ON_TI:
      action=c.call('STHTPLOT','screens',setup,result,probability,critical)
      if action: return 'back' if action=='back' else None
    return c.view('HT '+str(index)+': '+labels[index-1],c.call(c.call('STHYP','page_module',index),'step',index,setup,result,probability,critical,reject))
  for index in (() if action in ('back','exit') else range(1,10)):
    if display(index) in ('back','exit'): break
  while True:
    key=c.menu('HYPOTHESIS > REVIEW STEPS',[(str(i+1),label) for i,label in enumerate(labels)]+[('10','ALL NINE STEPS'),('11','FULL-SCREEN p-VALUE GRAPH'),('12','FULL-SCREEN REJECTION GRAPH')])
    if key=='0': return
    if key in ('11','12'):
      if not c.call('STHTPLOT','show',setup,result,probability,critical,'p' if key=='11' else 'alpha'):
        c.view('GRAPHICS UNAVAILABLE',['THIS GRAPH USES ti_plotlib.']+c.call('STHYDRAW','drawing',setup,result,critical))
    elif key=='10':
      for index in range(1,10):
        if display(index) in ('back','exit'): break
    else: display(int(key))
