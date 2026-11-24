class Rows:
  def __init__(self,data,prefix=(),drawing=(),graph=None):
    self.data,self.prefix,self.drawing,self.graph=data,prefix,drawing,graph
  def __len__(self): return len(self.prefix)+2*len(self.data[5])+2+len(self.drawing)
  def __iter__(self):
    for line in self.prefix: yield line
    table,label,random,alpha,nc,observed,expected,ts,df,p,cv,fitted,rt,ct=self.data
    total=sum(observed)
    for k in range(len(observed)):
      o,e=observed[k],expected[k]
      cell='R%d C%d' % (k//nc+1,k%nc+1) if table else 'CATEGORY '+str(k+1)
      expression=('E=%g*%g/%g=%g' % (rt[k//nc],ct[k%nc],total,e) if table else
        'E=%g*(%g/%g)=%g' % (total,e,total,e))
      yield cell+': O=%g; ' % o+expression+'; (O-E)^2/E=(%g-%g)^2/%g=%.8g' % (o,e,e,(o-e)**2/e)
    yield 'chi-square ='
    for k in range(len(observed)):
      yield ('  ' if k==0 else '+ ')+'(%g-%g)^2/%g' % (observed[k],expected[k],expected[k])
    yield '= %.10g' % ts
    for line in self.drawing: yield line

def make(data,prefix=(),drawing=(),graph=None): return Rows(data,prefix,drawing,graph)
