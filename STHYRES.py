import STCORE as c

def inference(ts,alpha,alternative,degrees=None):
    if not 0<alpha<1 or alternative not in ('<','>','!='):
        raise ValueError('CHECK alpha AND ALTERNATIVE')
    if degrees is None:
        left=c.call('STCLTM','normal_cdf',ts)
        right=c.call('STCLTM','normal_sf',ts)
        quantile=lambda area:c.call('STZCRIT','standard_normal_quantile',area)
    else:
        left=c.call('STTCRIT','t_cdf',ts,degrees)
        right=c.call('STTCRIT','t_sf',ts,degrees)
        quantile=lambda area:c.call('STTCRIT','t_quantile',area,degrees)
    if alternative=='<': probability=left;critical=(quantile(alpha),)
    elif alternative=='>': probability=right;critical=(quantile(1-alpha),)
    else:
        probability=min(1,2*min(left,right))
        positive=quantile(1-alpha/2)
        critical=(-positive,positive)
    return probability,critical,probability<=alpha

def conclusion(setup,reject):
    statement=(setup['context'] or 'THE POPULATION PARAMETER')+' ('+setup['parameter']+') '+setup['claim']+' '+('%.8g' % setup['null'])
    action='REJECT' if setup['claim'] in ('=','<=','>=') else 'SUPPORT'
    return ('SUFFICIENT' if reject else 'INSUFFICIENT')+' EVIDENCE TO '+action+' THE CLAIM THAT '+statement+'.'

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
            'FOR p-VALUE, SHADE AS / MORE EXTREME THAN TS IN H1 DIRECTION.']

def step(index,setup,result,probability,critical,reject):
    null=setup['null'];alt=setup['alternative'];alpha=setup['alpha']
    parameter=setup['parameter'];kind='z' if result['df'] is None else 't'
    if index==1:
        return [result['name'],'SRS / RANDOM INDEPENDENT: '+setup['random']]+result['checks']+[
            'IF A CHECK FAILS / IS UNVERIFIED, THE TEST CONCLUSION IS CONDITIONAL ON RESOLVING IT.']
    if index==2:
        lines=['CLAIM: '+parameter+' '+setup['claim']+' %.8g' % null,
               'H0: '+parameter+' = %.8g' % null,'H1: '+parameter+' '+alt+' %.8g' % null,
               'TEST THE EQUALITY BOUNDARY IN H0; H1 DETERMINES THE TAIL.']
        if parameter in ('p1-p2','mu1-mu2') and null==0:
            lines.append('H0: '+('p1 = p2' if parameter=='p1-p2' else 'mu1 = mu2'))
        return lines
    if index==3:
        return result['inputs']+['POINT ESTIMATE PE=%.8g' % result['estimate'],
            'PE=p-hat OR p1-hat-p2-hat FOR PROPORTIONS; x-bar OR x1-bar-x2-bar FOR MEANS.',
            'RAW MEANS USE THE SAME n, MEAN AND SAMPLE SD AS 1-Var Stats.']
    if index==4:
        area=alpha if alt=='<' else 1-alpha if alt=='>' else 1-alpha/2
        lines=['alpha=%.8g; LEFT-CDF AREA=%.8g' % (alpha,area),
               ('invNorm(area,0,1)' if kind=='z' else 'invT(area,df)'),
               'CV='+', '.join('%.8g' % v for v in critical)]
        if result['df'] is not None: lines.append('df=%.8g' % result['df'])
        lines.append('REJECT TO THE '+('LEFT OF CV' if alt=='<' else 'RIGHT OF CV' if alt=='>' else 'OUTSIDE THE TWO CVs'))
        return lines
    if index==5:
        return [result['formula'],'SE UNDER H0=%.8g' % result['se'],
                'TS=(%.8g-%.8g)/%.8g=%.8g' % (result['estimate'],null,result['se'],result['ts']),
                'TI TEST: '+result['command']]
    if index==6: return drawing(setup,result,critical)
    if index==7:
        return ['ASSUME H0 IS TRUE: PROBABILITY OF A RESULT AS OR MORE EXTREME IN H1 DIRECTION.',
                'p-VALUE=%.10g' % probability,
                'LEFT: CDF(TS); RIGHT: SURVIVAL(TS); TWO: 2*SMALLER TAIL.',
                'USE normalcdf FOR z; tcdf WITH df FOR t.',
                'p IS NOT THE PROBABILITY THAT H0 IS TRUE.']
    if index==8:
        return ['p=%.10g; alpha=%.8g' % (probability,alpha),
                'REJECT H0' if reject else 'FAIL TO REJECT H0',
                'RULE: REJECT IF UNROUNDED p <= alpha; OTHERWISE FAIL TO REJECT.',
                'CRITICAL-REGION AND p-VALUE METHODS DESCRIBE THE SAME TEST.']
    return [conclusion(setup,reject),'STATISTICAL EVIDENCE IS CONDITIONAL ON STEP 1 REQUIREMENTS.',
            'FAILING TO REJECT DOES NOT PROVE / ACCEPT H0 OR ITS CLAIM.']

def show(setup,result):
    probability,critical,reject=inference(result['ts'],setup['alpha'],setup['alternative'],result['df'])
    labels=('REQUIREMENTS','H0 AND H1','POINT ESTIMATE','CRITICAL VALUES','TEST STATISTIC',
            'DRAW SAMPLING DISTRIBUTION','p-VALUE','INITIAL CONCLUSION','FINAL CONCLUSION')
    def display(index):
        return c.view('HT '+str(index)+': '+labels[index-1],step(index,setup,result,probability,critical,reject))
    for index in range(1,10):
        if display(index) in ('back','exit'): break
    while True:
        key=c.menu('HYPOTHESIS > REVIEW STEPS',[(str(i+1),label) for i,label in enumerate(labels)]+[('10','ALL NINE STEPS')])
        if key=='0': return
        if key=='10':
            for index in range(1,10):
                if display(index) in ('back','exit'): break
        else: display(int(key))
