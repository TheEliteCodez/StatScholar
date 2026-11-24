import STCORE as c

def scatter(points):
  xmin=min(x for x,y in points);xmax=max(x for x,y in points)
  ymin=min(y for x,y in points);ymax=max(y for x,y in points)
  grid=[' '*25 for i in range(9)]
  for x,y in points:
    col=int(round(24*(x-xmin)/(xmax-xmin))) if xmax>xmin else 12
    row=8-int(round(8*(y-ymin)/(ymax-ymin))) if ymax>ymin else 4
    mark='*' if grid[row][col]==' ' else '#'
    grid[row]=grid[row][:col]+mark+grid[row][col+1:]
  return ['SCATTERPLOT (* PAIR; # OVERLAP)','y MAX=%.8g' % ymax]+[
    '|'+row for row in grid]+['+'+'-'*25,
    'x MIN=%.8g; MAX=%.8g' % (xmin,xmax),'y MIN=%.8g' % ymin]

def show(points,xlabel,ylabel,fit=None,residual=False,line_only=False):
  if residual:
    points=[(x,y-(fit[0]+fit[1]*x)) for x,y in points]
    ylabel='RESIDUAL y-yhat'
  lines=['x: '+xlabel,'y: '+ylabel]
  if fit and not residual:
    a,b=fit
    lo=min(x for x,y in points);hi=max(x for x,y in points)
    lines+=['yhat=%.6g*x %s %.6g' % (b,'-' if a<0 else '+',abs(a)),
      'PLOT TWO POINTS ON THE LINE:',
      '(%.8g, %.8g)' % (lo,a+b*lo),'(%.8g, %.8g)' % (hi,a+b*hi),
      'DRAW A STRAIGHT LINE THROUGH THEM.']
  if not line_only:lines+=scatter(points)
  c.view('REGRESSION LINE' if fit and not residual else 'RESIDUAL PLOT' if residual else 'SCATTERPLOT',lines)
