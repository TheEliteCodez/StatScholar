from STGPEN import frame,line,ink,scale,dot,number,wait,BLACK,BLUE,RED

def show(rows,kind='histogram',title='DATA PLOT',selected=None):
  # Rows contain x,count or class-low,class-high,count or category,count.
  categories=kind=='category'
  if kind in ('histogram','dot') and any(number(rows[i][0])>=number(rows[i+1][0]) for i in range(len(rows)-1)):
    counts={}
    for x,f in rows:counts[x]=counts.get(x,0)+number(f)
    rows=sorted(counts.items(),key=lambda row:number(row[0]))
  n=len(rows)
  if not n:return False
  ymax=max(number(r[-1]) for r in rows) or 1
  xmin=0 if categories else min(number(r[0]) for r in rows)
  xmax=n if categories else max(number(r[1] if len(r)==3 else r[0]) for r in rows)
  gap=min(number(rows[i+1][0])-number(rows[i][0]) for i in range(n-1)) if not categories and n>1 else 1
  if gap<=0:gap=1
  if kind!='classes':xmin-=gap*.5;xmax+=gap*.5
  for start in range(0,n,12 if categories else n):
    end=min(n,start+(12 if categories else n))
    low,high=(start-.5,end-.5) if categories else (xmin,xmax)
    plt=frame(title,'CATEGORY INDEX' if categories else 'VALUE / CLASS','COUNT; ROWS %d-%d/%d'%(start+1,end,n))
    if plt is None:return False
    line(plt,26,160,306,160);line(plt,26,40,26,160);ink(plt,'%.4g'%ymax,1,40,BLACK)
    at=lambda x:scale(x,low,high)
    for i in range(start,end):
      r=rows[i];x=i if categories else number(r[0]);f=number(r[-1]);y=160-110*f/ymax
      if kind=='dot':
        for j in range(int(f)):dot(plt,at(x),160-110*(j+1)/ymax)
      else:
        a,b=(at(x),at(number(r[1]))) if kind=='classes' else (at(x-gap*.42),at(x+gap*.42))
        if categories:a,b=at(i-.35),at(i+.35)
        plt.color(*(RED if i==selected else BLUE))
        line(plt,a,160,a,y);line(plt,a,y,b,y);line(plt,b,y,b,160)
      if categories or i in (start,end-1):ink(plt,str(i+1) if categories else '%.4g'%x,at(x)-6,167,BLACK)
    action=wait(plt)
    if action=='back':return action
    if categories:
      import STCORE as c
      if c.view('CATEGORY KEY',['%d %s'%(j+1,rows[j][0]) for j in range(start,end)]) in ('back','exit'):return 'back'
  return 'next'
