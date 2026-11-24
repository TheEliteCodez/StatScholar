from STGPEN import frame,line,ink,scale,dot,wait,BLACK,BLUE,RED,GREEN

def show(estimate,low,high,level=None,label='ESTIMATE',bound=None):
  estimate=float(estimate);low=float(low);high=float(high)
  difference=('1' in label and '-' in label) or 'DIFFERENCE' in label or label=='d-bar'
  a=min(low,estimate,0 if difference else low)
  b=max(high,estimate,0 if difference else high)
  pad=(b-a)*.15 or 1;a-=pad;b+=pad
  plt=frame('CONFIDENCE INTERVAL' if not bound else 'ONE-SIDED CONFIDENCE',label,
    ('CONFIDENCE=%.5g%%'%(100*level)) if level is not None else 'E=%.6g'%max(estimate-low,high-estimate))
  if plt is None:return False
  at=lambda x:scale(x,a,b)
  line(plt,26,125,306,125)
  plt.color(*BLUE)
  left=26 if bound=='upper' else at(low)
  right=306 if bound=='lower' else at(high)
  line(plt,left,100,right,100)
  if bound:
    edge=left if bound=='upper' else right
    line(plt,edge,100,edge+(6 if bound=='upper' else -6),94)
    line(plt,edge,100,edge+(6 if bound=='upper' else -6),106)
  for i,x in enumerate((low,high) if not bound else ((high,) if bound=='upper' else (low,))):
    line(plt,at(x),90,at(x),110);ink(plt,'%.6g'%x,at(x)-18,132+i*10,BLUE)
  dot(plt,at(estimate),100,GREEN);ink(plt,'PE=%.6g'%estimate,at(estimate)-24,65,GREEN)
  if a<=0<=b:ink(plt,'0',at(0)-3,157,BLACK)
  plt.color(*RED);plt.text_at(2,'E=%.6g'%max(abs(estimate-low),abs(high-estimate)),'center')
  return wait(plt)
