import STCORE as c

LABELS=('REQUIREMENTS','H0 AND H1','POINT ESTIMATE','CRITICAL VALUES','TEST STATISTIC','DRAW SAMPLING DISTRIBUTION','p-VALUE','INITIAL CONCLUSION','FINAL CONCLUSION')

def advance(s,value):
  if s is None:s={'phase':'menu'}
  phase=s['phase']
  def invoke(module,function,args,next_phase):
    s['phase']=next_phase
    return 'call',(module,function,args),s
  def page():
    i=s['index']
    if i==6 and c.ON_TI:
      s['phase']='plot'
      return 'plot',s['data'][:4]+(('alpha','p'),),s
    module='STHYREQ' if i<=3 else 'STHYTS' if i<=5 else 'STHYDRAW' if i==6 else 'STHYPVAL' if i==7 else 'STHYEND'
    return invoke(module,'step',(i,)+s['data'],'rows')
  def review():
    s['phase']='review'
    return 'menu',('HYPOTHESIS > REVIEW STEPS',[(str(i+1),label) for i,label in enumerate(LABELS)]+[('10','ALL NINE STEPS'),('11','FULL-SCREEN p-VALUE GRAPH'),('12','FULL-SCREEN REJECTION GRAPH')]),s
  if phase=='menu':
    s.clear()
    return invoke('STHYMNU','choose',(),'chosen')
  if phase=='chosen':
    if value is None:return 'done',(),None
    kind,module,function,args=value
    s['kind']=kind
    return invoke(module,function,args,'input')
  if phase=='input':
    if value is None or s['kind']=='call':
      s['phase']='menu'
      return advance(s,None)
    if s['kind']=='chi':return invoke('STCHISH','show',(value,),'menu')
    setup,result,inference=value
    s['data']=(setup,result)
    return invoke('STHYINF','inference',(result['ts'],setup['alpha'],setup['alternative'],result['df']),'inferred')
  if phase=='inferred':
    s['data']+=value
    return invoke('STHYANS','summary',s['data'],'answer')
  if phase=='answer':
    s['phase']='start'
    return 'view',('HYPOTHESIS: ANSWER',value),s
  if phase=='start':
    if value in ('back','exit'):return review()
    s['index']=1;s['all']=True
    return page()
  if phase=='rows':
    s['phase']='page'
    return 'view',('HT '+str(s['index'])+': '+LABELS[s['index']-1],value),s
  if phase=='plot':
    if not value:return invoke('STHYDRAW','step',(6,)+s['data'],'rows')
    value='back' if value=='back' else None
    phase='page'
  if phase=='page':
    if value in ('back','exit') or not s['all'] or s['index']==9:return review()
    s['index']+=1
    return page()
  if phase=='review':
    if value=='0':
      s['phase']='menu'
      return advance(s,None)
    if value in ('11','12'):
      s['phase']='graph'
      return 'plot',s['data'][:4]+(('p',) if value=='11' else ('alpha',),),s
    s['index']=1 if value=='10' else int(value)
    s['all']=value=='10'
    return page()
  if phase=='graph':
    if value:return review()
    return invoke('STHYDRAW','drawing',s['data'][:2]+(s['data'][3],),'fallback')
  if phase=='fallback':
    s['phase']='finished'
    return 'view',('GRAPHICS UNAVAILABLE',['THIS GRAPH USES ti_plotlib.']+value),s
  return review()
