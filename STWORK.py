import STCORE as c

def num(value):
    if not isinstance(value,tuple): return '%.10g' % value
    a,b=value
    if b==1: return str(a)
    tail=b;twos=fives=0
    while tail%2==0: tail//=2;twos+=1
    while tail%5==0: tail//=5;fives+=1
    if tail!=1: return str(a)+'/'+str(b)
    places=max(twos,fives)
    digits=str(abs(a)*10**places//b)
    digits='0'*max(0,places+1-len(digits))+digits
    return ('-' if a<0 else '')+digits[:-places]+'.'+digits[-places:]

class Lines:
    def __init__(self,count,row): self.count,self.row=count,row
    def __len__(self): return self.count
    def __iter__(self):
        for i in range(self.count): yield self.row(i)

class Chain:
    def __init__(self,*parts): self.parts=parts
    @property
    def graph(self):
        for part in self.parts:
            graph=getattr(part,'graph',None)
            if graph: return graph
    def __radd__(self,other): return Chain(other,self)
    def __add__(self,other): return Chain(self,other)
    def __len__(self): return sum(len(part) for part in self.parts)
    def __iter__(self):
        for part in self.parts:
            for line in part: yield line

def sum_work(label,count,term,total):
    def row(i):
        if i==0: return label+' ='
        if i==count+1: return '= '+num(total)
        return ('  ' if i==1 else '+ ')+term(i-1)
    return Lines(count+2,row)

def mean_se(sd,n,se,label='s'):
    return ['SE='+label+'/sqrt(n)','SE='+num(sd)+'/sqrt('+str(n)+')='+num(se)]

def prop_se(p,n,se,label='p-hat'):
    return ['SE=sqrt('+label+'*(1-'+label+')/n)',
            'SE=sqrt('+num(p)+'*(1-'+num(p)+')/'+str(n)+')='+num(se)]

def mean_two(sd1,n1,sd2,n2,se,df):
    a,b=sd1*sd1/n1,sd2*sd2/n2
    return ['a=s1^2/n1='+num(sd1)+'^2/'+str(n1)+'='+num(a),
            'b=s2^2/n2='+num(sd2)+'^2/'+str(n2)+'='+num(b),
            'SE=sqrt(s1^2/n1+s2^2/n2)',
            'SE=sqrt('+num(sd1)+'^2/'+str(n1)+'+'+num(sd2)+'^2/'+str(n2)+')='+num(se),
            'Welch df=(a+b)^2/(a^2/(n1-1)+b^2/(n2-1))',
            'df=('+num(a)+'+'+num(b)+')^2/('+num(a)+'^2/('+str(n1)+'-1)+'+num(b)+'^2/('+str(n2)+'-1))='+num(df)]

def prop_two(p1,n1,p2,n2,se):
    return ['SE=sqrt(p1-hat*(1-p1-hat)/n1+p2-hat*(1-p2-hat)/n2)',
            'SE=sqrt('+num(p1)+'*(1-'+num(p1)+')/'+str(n1)+'+'+num(p2)+'*(1-'+num(p2)+')/'+str(n2)+')='+num(se)]

def endpoints(estimate,margin,interval):
    return ['LOWER=estimate-E='+num(estimate)+'-'+num(margin)+'='+num(interval[0]),
            'UPPER=estimate+E='+num(estimate)+'+'+num(margin)+'='+num(interval[1])]

def ratio_work(label,a,b):
    if b==0: return [label+'=UNDEFINED (ZERO DENOMINATOR)']
    value=a/b
    return [label+'='+str(a)+'/'+str(b)+'='+num(value),
            label+' PERCENT=('+str(a)+'/'+str(b)+')*100='+num(value*100)+'%']
