import STCORE
def solver_dice_space(): return STCORE.call('STMDICE','solver_dice_space')
def solver_multi_dice(n=None): return STCORE.call('STMDICE','solver_multi_dice',n)
def dice_event_count(n,event,value=0): return STCORE.call('STMDICE','dice_event_count',n,event,value)
def dice_sum_at_most(n,value): return STCORE.call('STMDICE','dice_sum_at_most',n,value)
def experiment_session(kind): return STCORE.call('STEXPER','experiment_session',kind)
def experiment_indices(outcomes,kind,query): return STCORE.call('STEXPER','experiment_indices',outcomes,kind,query)
def pair_matches(pair,event):
  kind,op,value=event[:3]
  upper=event[3] if len(event)>3 else 0
  a,b=pair
  if kind=='sumodd': return (a+b)%2==1
  if kind=='sumeven': return (a+b)%2==0
  if kind=='anyeven': return a%2==0 or b%2==0
  if kind=='sum': return STCORE.event_match(a+b,op,value,upper)
  if kind=='first': return STCORE.event_match(a,op,value,upper)
  if kind=='second': return STCORE.event_match(b,op,value,upper)
  if kind=='doubles': return a==b
  if kind=='even': return a%2==0 and b%2==0
  if kind=='odd': return a%2==1 and b%2==1
  if kind=='face': return a==value or b==value
  raise ValueError('UNKNOWN DICE EVENT')
def pair_probability(first,second=None,join='AND'):
  return STCORE.ratio(sum(1 for pair in pair_outcomes(first,second,join)),36)
def pair_outcomes(first,second=None,join='AND'):
  for a in range(1,7):
    for b in range(1,7):
      x=pair_matches((a,b),first)
      y=pair_matches((a,b),second) if second else x
      if (x and y) if join=='AND' else (x or y): yield a,b
def read_pair_event():
  return STCORE.call('STDICE2', 'read_pair_event')
def dice_session(word=None):
  return STCORE.call('STDICE2', 'dice_session', word)
