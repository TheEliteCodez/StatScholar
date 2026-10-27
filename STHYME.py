import math
import STCORE as c

def validate(sd,n):
    if sd<0 or n<2 or int(n)!=n: raise ValueError('USE s >= 0 AND WHOLE n >= 2')

def one(mean,sd,n,null):
    validate(sd,n)
    se=sd/math.sqrt(n)
    if se==0: raise ValueError('SAMPLE SE=0; t TEST IS UNDEFINED')
    return {'estimate':mean,'se':se,'ts':(mean-null)/se,'df':n-1,
            'se_work':c.call('STWORK','mean_se',sd,n,se)+['df=n-1=%d-1=%d' % (n,n-1)],
            'formula':'t=(x-bar-mu0)/(s/sqrt(n))',
            'inputs':['x-bar=%.8g; s=%.8g; n=%d' % (mean,sd,n)],'checks':[]}

def two(mean1,sd1,n1,mean2,sd2,n2,null=0):
    validate(sd1,n1);validate(sd2,n2)
    a,b=sd1*sd1/n1,sd2*sd2/n2
    if a+b==0: raise ValueError('COMBINED SE=0; t TEST IS UNDEFINED')
    se=math.sqrt(a+b)
    degrees=(a+b)**2/(a*a/(n1-1)+b*b/(n2-1))
    return {'estimate':mean1-mean2,'se':se,'ts':(mean1-mean2-null)/se,'df':degrees,
            'se_work':c.call('STWORK','mean_two',sd1,n1,sd2,n2,se,degrees),
            'formula':'t=((x1-bar-x2-bar)-d0)/sqrt(s1^2/n1+s2^2/n2)',
            'inputs':['GROUP 1: x-bar=%.8g; s=%.8g; n=%d' % (mean1,sd1,n1),
                      'GROUP 2: x-bar=%.8g; s=%.8g; n=%d' % (mean2,sd2,n2),
                      'WELCH df=(a+b)^2/(a^2/(n1-1)+b^2/(n2-1))',
                      'a=s1^2/n1; b=s2^2/n2; NO EQUAL-VARIANCE ASSUMPTION'], 'checks':[]}

def session(two_sample=False):
    setup=c.call('STHYIO','setup','mu1-mu2' if two_sample else 'mu')
    if setup is None: return
    data=[];requirements=[]
    if two_sample:
        independent=c.call('STHYIO','check','INDEPENDENT GROUPS (NOT PAIRED)?')
        if independent is None: return
        requirements.append('INDEPENDENT / NOT PAIRED: '+independent)
    for i in range(2 if two_sample else 1):
        label='GROUP '+str(i+1)
        values=c.call('STHYIO','mean_data',label)
        if values is None: return
        mean,sd,n=values
        validate(sd,n)
        data.append(values)
        requirements.append(c.call('STHYIO','population',n,label))
        if n<=30:
            normal=c.call('STHYIO','check',label+' NORMAL, NO STRONG SKEW / OUTLIERS?')
            if normal is None: return
            requirements.append(label+' NORMALITY: '+normal)
        else: requirements.append(label+' n > 30: PASS; CHECK EXTREME OUTLIERS')
    result=two(*(data[0]+data[1]+(setup['null'],))) if two_sample else one(*(data[0]+(setup['null'],)))
    result['checks']=requirements
    result['name']='TWO-MEAN WELCH t TEST' if two_sample else 'ONE-MEAN t TEST'
    result['command']='2-SampTTest; Pooled: No' if two_sample else 'T-Test'
    c.call('STHYRES','show',setup,result)
