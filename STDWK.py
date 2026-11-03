import math
import STCORE as c
from STEXACT import to_ratio, rdiv
from STEFMT import radd, rmul
from STWORK import Lines, Chain, num, sum_work

def descriptive(stats,values=None,rows=None):
    n=stats['n'];mean=stats['MEAN']
    ss=rmul(stats['POPULATION VARIANCE'],(n,1))
    count=len(rows) if rows is not None else len(values) if values is not None else 0
    def pair(i): return (to_ratio(rows[i][0]),rows[i][1]) if rows is not None else (to_ratio(values[i]),1)
    def deviation(i):
        x,f=pair(i)
        return radd(x,(-mean[0],mean[1]))
    def cell(i):
        j,part=divmod(i,4);x,f=pair(j);d=deviation(j)
        if part==0: return 'x=%s; f=%d; x*f=%s*%d=%s' % (num(x),f,num(x),f,num(rmul(x,(f,1))))
        if part==1: return 'd=x-mean=%s-(%s)=%s' % (num(x),num(mean),num(d))
        square=rmul(d,d)
        if part==2: return 'd^2=(%s)^2=%s' % (num(d),num(square))
        return 'f*d^2=%d*(%s)=%s' % (f,num(square),num(rmul(square,(f,1))))
    end=['MEAN=SUM(x*f)/n=%s/%d=%s' % (num(stats['SUM']),n,num(mean)),
         'POP VAR=SS/n=%s/%d=%s' % (num(ss),n,num(stats['POPULATION VARIANCE'])),
         'POP SD=sqrt(%s)=%s' % (num(stats['POPULATION VARIANCE']),num(stats['POPULATION SD']))]
    if n>1:
        end+=['SAMPLE VAR=SS/(n-1)=%s/(%d-1)=%s' % (num(ss),n,num(stats['SAMPLE VARIANCE s^2'])),
              'SAMPLE SD=sqrt(%s)=%s' % (num(stats['SAMPLE VARIANCE s^2']),num(stats['SAMPLE SD Sx']))]
    if not count: return end
    return Chain(sum_work('n=SUM(f)',count,lambda i:str(pair(i)[1]),n),
                 sum_work('SUM(x*f)',count,lambda i:'('+num(pair(i)[0])+'*'+str(pair(i)[1])+')',stats['SUM']),
                 ['MEAN=%s/%d=%s' % (num(stats['SUM']),n,num(mean)), 'WORK TABLE: x, f, d, f*d^2'],
                 Lines(4*count,cell),
                 sum_work('SS=SUM(f*(x-mean)^2)',count,lambda i:str(pair(i)[1])+'*('+num(pair(i)[0])+'-('+num(mean)+'))^2',ss),end)

def moments(count,row_at,mean,variance,sd):
    second=radd(variance,rmul(mean,mean))
    return Chain(sum_work('E(X)=SUM(x*P(x))',count,
                         lambda i:'('+num(row_at(i)[0])+'*'+num(row_at(i)[1])+')',mean),
                 sum_work('E(X^2)=SUM(x^2*P(x))',count,
                          lambda i:'(('+num(row_at(i)[0])+')^2*'+num(row_at(i)[1])+')',second),
                 ['VAR=E(X^2)-E(X)^2=%s-(%s)^2=%s' % (num(second),num(mean),num(variance)),
                  'SD=sqrt(%s)=%s' % (num(variance),num(sd))])

def payoff(rows,cost,total,mean,variance,sd):
    def row(i):
        x,p=rows[i]
        return 'NET=%s-%s=%s; P=%s/%s=%s' % (num(radd(x,cost)),num(cost),num(x),num(rmul(p,total)),num(total),num(p))
    return Chain(Lines(len(rows),row),moments(len(rows),lambda i:rows[i],mean,variance,sd))
