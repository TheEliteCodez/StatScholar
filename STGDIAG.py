import math
import STCORE as c
from STGPEN import frame,line,ink,dot,wait,BLACK,BLUE,RED

def venn(total,a,b,both,choice=None,event_mask=None,group_mask=None):
  if event_mask is not None: choice='event'
  choice=choice or c.menu('VENN GRAPH',[('1','ALL REGIONS'),('2','A OR B'),('3','A AND B'),('4','A ONLY'),('5','B ONLY'),('6','GIVEN A: B WITHIN A'),('7','GIVEN B: A WITHIN B')])
  if choice=='0':return 'back'
  total,a,b,both=[float(x) for x in (total,a,b,both)]
  parts=(both,a-both,b-both,total-a-b+both)
  denominator=sum(parts[i] for i in range(4) if group_mask & (1<<i)) if group_mask is not None else a if choice=='6' else b if choice=='7' else total
  numerator=a+b-both if choice=='2' else both if choice in ('3','6','7') else a-both if choice=='4' else b-both if choice=='5' else None
  if event_mask is not None:
    mask=event_mask & group_mask if group_mask is not None else event_mask
    numerator=sum(parts[i] for i in range(4) if mask & (1<<i))
  plt=frame('VENN: SCHEMATIC REGIONS','A LEFT / B RIGHT','DENOM=%.6g'%denominator)
  if plt is None:return False
  for x in range(53,268,3):
    for y in range(48,142,3):
      A=(x-127)**2+(y-95)**2<=42**2;B=(x-193)**2+(y-95)**2<=42**2
      selected=(A or B) if choice=='2' else (A and B) if choice in ('3','6','7') else (A and not B) if choice=='4' else (B and not A) if choice=='5' else False
      bit=1 if A and B else 2 if A else 4 if B else 8
      if event_mask is not None:selected=bool(mask & bit)
      if selected:plt.color(*BLUE);line(plt,x,y,x+2,y)
      elif group_mask is not None and group_mask & bit:plt.color(190,190,190);line(plt,x,y,x+2,y)
  plt.color(*BLACK)
  for x1,y1,x2,y2 in ((40,42,280,42),(40,42,40,150),(280,42,280,150),(40,150,280,150)):line(plt,x1,y1,x2,y2)
  for center in (127,193):
    for i in range(80):
      t=i*2*math.pi/80;u=(i+1)*2*math.pi/80
      line(plt,center+42*math.cos(t),95+42*math.sin(t),center+42*math.cos(u),95+42*math.sin(u))
  for value,x,y in ((a-both,93,92),(both,151,92),(b-both,211,92),(total-a-b+both,45,138)):ink(plt,'%.5g'%value,x,y,BLACK)
  plt.text_at(2,'A=%.5g B=%.5g TOTAL=%.5g'%(a,b,total),'center')
  if numerator is not None:plt.text_at(10,'P=%.6g'% (numerator/denominator) if denominator else 'CONDITIONAL UNDEFINED','center')
  return wait(plt)

def dice(first=None,second=None,join='AND'):
  outcomes=list(c.call('STDICE','pair_outcomes',first,second,join)) if first else [(a,b) for a in range(1,7) for b in range(1,7)]
  plt=frame('TWO DICE OUTCOMES','SECOND DIE (COLUMNS)','FIRST DIE (ROWS); P=%d/36'%len(outcomes))
  if plt is None:return False
  for i in range(7):line(plt,69+25*i,39,69+25*i,159);line(plt,69,39+20*i,219,39+20*i)
  for i in range(1,7):ink(plt,str(i),75+25*(i-1),28,BLACK);ink(plt,str(i),52,44+20*(i-1),BLACK)
  for a,b in outcomes:dot(plt,81+25*(b-1),49+20*(a-1))
  return wait(plt)
