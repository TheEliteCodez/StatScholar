import math
import STCORE as c

# Numeric ticks only: 14 five-column glyphs, without the general font bank.
_DIGITS=(b'\x3e\x51\x49\x45\x3e\x00\x42\x7f\x40\x00'
  b'\x42\x61\x51\x49\x46\x21\x41\x45\x4b\x31'
  b'\x18\x14\x12\x7f\x10\x27\x45\x45\x45\x39'
  b'\x3c\x4a\x49\x49\x30\x01\x71\x09\x05\x03'
  b'\x36\x49\x49\x49\x36\x06\x49\x49\x29\x1e'
  b'\x00\x60\x60\x00\x00\x08\x08\x08\x08\x08'
  b'\x08\x08\x3e\x08\x08\x38\x54\x54\x54\x18')

def axis_number(plt,value,x,y,right=False):
  text='%.4g' % (0 if value==0 else value)
  width=6*len(text)-1
  x=max(1,min(318-width,x-width if right else x-width/2))
  for char in text:
    start=5*'0123456789.-+e'.index(char)
    for col in range(5):
      bits=_DIGITS[start+col]
      for row in range(7):
        if bits & (1<<row):plt.line(x+col,y+3-row,x+col+.5,y+3-row)
    x+=6

def axis_range(low,high):
  pad=(high-low)*.06 or max(1,abs(low)*.06)
  low-=pad;high+=pad
  unit=10**math.floor(math.log((high-low)/4)/math.log(10))
  scale=(high-low)/(4*unit)
  step=unit*(1 if scale<=1 else 2 if scale<=2 else 5 if scale<=5 else 10)
  return math.floor(low/step)*step,math.ceil(high/step)*step,step

def show(points,xlabel='x',ylabel='y',fit=None,residual=False,line_only=False):
  try: import ti_plotlib as plt
  except ImportError: return False
  def value(x,y):return y-(fit[0]+fit[1]*x) if residual else y
  xmin=min(x for x,y in points);xmax=max(x for x,y in points)
  ymin=min(value(x,y) for x,y in points);ymax=max(value(x,y) for x,y in points)
  if line_only and fit and not residual:
    endpoints=(fit[0]+fit[1]*xmin,fit[0]+fit[1]*xmax)
    ymin=min(endpoints);ymax=max(endpoints)
  if residual:ymin=min(0,ymin);ymax=max(0,ymax)
  xa,xb,xstep=axis_range(xmin,xmax);ya,yb,ystep=axis_range(ymin,ymax)
  at=lambda x:60+246*(x-xa)/(xb-xa)
  height=88 if fit and not residual else 104
  yof=lambda y:61+height*(y-ya)/(yb-ya)
  plt.cls();plt.window(0,319,0,209);plt.pen('thin','solid');plt.color(0,0,0)
  plt.text_at(1,'RESIDUAL PLOT' if residual else 'REGRESSION LINE' if line_only and fit else 'SCATTER + REGRESSION LINE' if fit else 'SCATTER / QQ PLOT','center')
  plt.text_at(2,'y: '+('RESIDUAL y-yhat' if residual else ylabel[:34]),'left')
  if fit and not residual:
    plt.color(210,45,45)
    plt.text_at(3,'yhat=%.6g*x %s %.6g' % (fit[1],'-' if fit[0]<0 else '+',abs(fit[0])),'center')
    plt.color(0,0,0)
  plt.line(60,61,306,61);plt.line(60,61,60,61+height)
  plt.color(0,100,210);plt.pen('medium','solid')
  if not line_only:
    for x,y in points:
      px,py=at(x),yof(value(x,y))
      plt.line(px-1,py,px+1,py);plt.line(px,py-1,px,py+1)
  plt.pen('thin','solid');plt.color(210,45,45)
  if residual:plt.line(60,yof(0),306,yof(0))
  elif fit:
    a,b=fit;left,right=xa,xb
    if b:
      limits=sorted(((ya-a)/b,(yb-a)/b));left=max(left,limits[0]);right=min(right,limits[1])
    if left<=right:plt.line(at(left),yof(a+b*left),at(right),yof(a+b*right))
  plt.color(0,0,0)
  nx=int(round((xb-xa)/xstep));ny=int(round((yb-ya)/ystep))
  for i in range(nx+1):
    value=xa+i*xstep;px=at(value)
    plt.line(px,58,px,64)
    if nx<=4 or i%2==0 or i==nx:axis_number(plt,value,px,49)
  for i in range(ny+1):
    value=ya+i*ystep;py=yof(value)
    plt.line(57,py,63,py);axis_number(plt,value,53,py,True)
  plt.text_at(11,'x: '+xlabel[:34],'center')
  plt.text_at(12,'LEFT = BACK  RIGHT = NEXT','center')
  return c.call('STGKEY','wait',plt)
