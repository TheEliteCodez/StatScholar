import STCORE as c
from STEXACT import to_ratio, rdiv, compare_exact
from STEFMT import radd, rmul, rsum, exact_sorted, exact_text
def sub(a,b):
  return radd(a,(-b[0],b[1]))
def weighted_stats(rows):
  import math
  counts={}
  for x,f in rows:
    x=to_ratio(x)
    if f>0: counts[x]=counts.get(x,0)+f
  ordered=exact_sorted(counts)
  n=sum(counts.values())
  if not n: raise ValueError('NO OBSERVATIONS')
  def at(index):
    running=0
    for x in ordered:
      running+=counts[x]
      if index<running: return x
  def middle(start,end):
    length=end-start
    if not length: return 'DNE'
    m=start+length//2
    return at(m) if length%2 else rdiv(radd(at(m-1),at(m)),(2,1))
  total=rsum(rmul(x,(counts[x],1)) for x in ordered)
  mean=rdiv(total,(n,1))
  ss=rsum(rmul(rmul(sub(x,mean),sub(x,mean)),(counts[x],1)) for x in ordered)
  var=rdiv(ss,(n-1,1)) if n>1 else 'DNE'
  pop=rdiv(ss,(n,1))
  q1,med,q3=middle(0,n//2),middle(0,n),middle((n+1)//2,n)
  peak=max(counts.values())
  modes=[x for x in ordered if counts[x]==peak]
  mode='DNE' if peak==1 or len(modes)>2 or (len(modes)==len(ordered) and len(ordered)>1) else ','.join(exact_text(x) for x in modes)
  result={'n':n,'SUM':total,'MEAN':mean,'SAMPLE VARIANCE s^2':var,
    'SAMPLE SD Sx':math.sqrt(c.number(var)) if n>1 else 'DNE',
    'POPULATION VARIANCE':pop,'POPULATION SD':math.sqrt(c.number(pop)),
    'MIN':ordered[0],'Q1':q1,'MEDIAN':med,'Q3':q3,'MAX':ordered[-1],
    'MODE':mode,'RANGE':sub(ordered[-1],ordered[0]),'IQR':sub(q3,q1) if n>1 else 'DNE',
    'MIDRANGE':rdiv(radd(ordered[0],ordered[-1]),(2,1))}
  if n>1:
    distance=rmul(result['IQR'],(3,2))
    lo,hi=sub(q1,distance),radd(q3,distance)
    inside=[x for x in ordered if compare_exact(x,lo)>=0 and compare_exact(x,hi)<=0]
    result.update({'LOWER FENCE':lo,'UPPER FENCE':hi,'LOW WHISKER':inside[0],'HIGH WHISKER':inside[-1],
      'OUTLIERS':','.join(exact_text(x) for x in ordered if compare_exact(x,lo)<0 or compare_exact(x,hi)>0) or 'NONE'})
  return result
