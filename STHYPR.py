import math
import STCORE as c

def counts(x,n):
    if n<1 or x<0 or x>n or int(x)!=x or int(n)!=n:
        raise ValueError('USE WHOLE COUNTS 0 <= x <= n AND n > 0')

def one(x,n,p0):
    counts(x,n)
    if not 0<p0<1: raise ValueError('NORMAL z TEST NEEDS 0 < p0 < 1')
    estimate=x/n
    se=math.sqrt(p0*(1-p0)/n)
    return {'estimate':estimate,'se':se,'ts':(estimate-p0)/se,'df':None,
            'formula':'z=(p-hat-p0)/sqrt(p0*(1-p0)/n)',
            'inputs':['x=%d; n=%d; p0=%.6g' % (x,n,p0)],
            'checks':['n*p0=%.4f >= 10: %s' % (n*p0,'PASS' if n*p0>=10 else 'FAIL'),
                      'n*(1-p0)=%.4f >= 10: %s' % (n*(1-p0),'PASS' if n*(1-p0)>=10 else 'FAIL')]}

def two(x1,n1,x2,n2):
    counts(x1,n1);counts(x2,n2)
    pooled=(x1+x2)/(n1+n2)
    se=math.sqrt(pooled*(1-pooled)*(1/n1+1/n2))
    if se==0: raise ValueError('POOLED SE=0; NORMAL z TEST IS UNDEFINED')
    checks=[]
    for i,n in enumerate((n1,n2)):
        checks+=['GROUP %d: n*p-pool=%.4f; n*q-pool=%.4f: %s' %
                 (i+1,n*pooled,n*(1-pooled),'PASS' if min(n*pooled,n*(1-pooled))>=10 else 'FAIL')]
    return {'estimate':x1/n1-x2/n2,'se':se,'ts':(x1/n1-x2/n2)/se,'df':None,
            'formula':'z=(p1-hat-p2-hat)/sqrt(p-pool*q-pool*(1/n1+1/n2))',
            'inputs':['x1/n1=%d/%d; x2/n2=%d/%d' % (x1,n1,x2,n2),
                      'p-pool=(x1+x2)/(n1+n2)=%.8g' % pooled], 'checks':checks}

def session(two_sample=False):
    setup=c.call('STHYIO','setup','p1-p2' if two_sample else 'p',0 if two_sample else None)
    if setup is None: return
    x1=c.read_int('GROUP 1 SUCCESSES x: ');n1=c.read_int('GROUP 1 SAMPLE SIZE n: ')
    requirements=[c.call('STHYIO','population',n1,'GROUP 1')]
    if two_sample:
        x2=c.read_int('GROUP 2 SUCCESSES x: ');n2=c.read_int('GROUP 2 SAMPLE SIZE n: ')
        requirements.append(c.call('STHYIO','population',n2,'GROUP 2'))
        independent=c.call('STHYIO','check','TWO GROUPS INDEPENDENT?')
        if independent is None: return
        requirements.append('GROUP INDEPENDENCE: '+independent)
        result=two(x1,n1,x2,n2)
    else: result=one(x1,n1,setup['null'])
    result['checks']+=requirements
    result['name']='TWO-PROPORTION z TEST' if two_sample else 'ONE-PROPORTION z TEST'
    result['command']='2-PropZTest' if two_sample else '1-PropZTest'
    c.call('STHYRES','show',setup,result)
