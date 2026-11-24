class Lines:
  def __init__(self,lines,graph,parts=False):
    self.lines=lines;self.graph=graph;self.parts=parts
  def __len__(self):
    return sum(len(x) for x in self.lines) if self.parts else len(self.lines)
  def __getitem__(self,index):
    if isinstance(index,slice):return list(self)[index]
    if index<0:index+=len(self)
    for i,line in enumerate(self):
      if i==index:return line
    raise IndexError(index)
  def __iter__(self):
    for x in self.lines:
      if self.parts:
        for line in x:yield line
      else:yield x
  def __add__(self,other):return Lines((self,other),self.graph,True)
  def __radd__(self,other):return Lines((other,self),self.graph,True)

def attach(lines,module,function,args):
  return Lines(lines,(module,function,args))
