import STCORE as c

def num(value):
  return c.call('STWORK','num',value) if isinstance(value,tuple) else '%.10g' % value

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
