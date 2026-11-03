import STCORE as c

def drawing(setup,result,critical):
    ts=result['ts'];null=setup['null'];se=result['se']
    scale=max(3,abs(ts),max(abs(v) for v in critical))*1.15
    axis=['-']*29
    for label,value in [('0',0)]+[('C',v) for v in critical]+[('T',ts)]:
        i=max(0,min(28,int(round(14+14*value/scale))))
        axis[i]=label if axis[i]=='-' else '*'
    return ['DRAW A SYMMETRIC BELL ABOVE:', ''.join(axis),
            'STANDARDIZED AXIS: 0=CENTER; C=CV; T=TS; *=OVERLAP',
            '0 ALIGNS WITH H0 VALUE %.8g' % null,
            'TS %.8g ALIGNS WITH PE %.8g' % (ts,result['estimate'])]+[
            'CV %.8g ALIGNS WITH %.8g' % (v,null+v*se) for v in critical]+[
            'DRAW A SECOND, ALIGNED PARAMETER AXIS BELOW.',
            'SHADE '+('LEFT TAIL' if setup['alternative']=='<' else 'RIGHT TAIL' if setup['alternative']=='>' else 'BOTH TAILS')+' BEYOND CV FOR REJECTION.',
            'FOR THE p-VALUE, SHADE BEYOND THE TEST STATISTIC IN THE TAIL(S) CHOSEN BY H1.']

def step(index,setup,result,probability,critical,reject):
    return drawing(setup,result,critical)
