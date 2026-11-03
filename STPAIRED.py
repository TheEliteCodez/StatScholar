import STCORE as c

def session(test=True):
    points=c.call('STREGIO','read_pairs',2)
    if points is None: return
    first=input('FIRST MEASUREMENT LABEL: ').strip() or 'FIRST'
    second=input('SECOND MEASUREMENT LABEL: ').strip() or 'SECOND'
    direction=c.menu('PAIRED DIFFERENCE d',[('1',first+' MINUS '+second),('2',second+' MINUS '+first)])
    if direction=='0': return
    sign=1 if direction=='1' else -1
    label=(first+' MINUS '+second) if sign==1 else (second+' MINUS '+first)
    differences=[c.to_ratio(sign*(x-y)) for x,y in points]
    stats=c.call('STDMATH','descriptive',differences)
    n=stats['n'];mean=c.number(stats['MEAN']);sd=stats['SAMPLE SD Sx']
    setup=c.call('STHYIO','setup','mu_d') if test else None
    if test and setup is None: return
    random=setup['random'] if test else c.call('STHYIO','check','RANDOM INDEPENDENT PAIRS?')
    if random is None: return
    normal=c.call('STHYIO','check','DIFFERENCES NORMAL / NO STRONG SKEW?') if n<=30 else 'n > 30; CHECK EXTREME OUTLIERS'
    if normal is None: return
    confidence=c.read_number('CONFIDENCE LEVEL (94% OR .94): ')
    interval=c.call('STCINUM','one_mean',mean,sd,n,confidence)
    result=c.call('STHYME','one',mean,sd,n,setup['null']) if test else None
    if test:
        result['name']='PAIRED t TEST ON DIFFERENCES'
        result['command']='T-Test ON PAIRED DIFFERENCES; NOT 2-SampTTest'
        result['inputs']=['d='+label,'PAIRS n=%d; d-bar=%.10g; sd=%.10g' % (n,mean,sd)]
        result['formula']='t=(d-bar-d0)/(sd/sqrt(n))'
        result['checks']=['PAIRED OBSERVATIONS; INDEPENDENCE IS BETWEEN PAIRS.',
            'DIFFERENCE SHAPE: '+normal,'DIFFERENCE OUTLIERS: '+stats['OUTLIERS']]
        inference=c.call('STHYP','inference',result['ts'],setup['alpha'],setup['alternative'],n-1)
    def table():
        def row(i):
            x,y=points[i];d=c.number(differences[i])
            return 'PAIR %d: %s=%.10g; %s=%.10g; d=%s=%.10g; d-dbar=%.10g; (d-dbar)^2=%.10g' % (i+1,first,x,second,y,
                ('%.10g-%.10g' % (x,y)) if sign==1 else ('%.10g-%.10g' % (y,x)),d,d-mean,(d-mean)**2)
        return c.view('PAIRED WORK TABLE',c.call('STWORK','Lines',n,row))
    def summary():
        mx=sum(x for x,y in points)/n;my=sum(y for x,y in points)/n
        sx=(sum((x-mx)**2 for x,y in points)/(n-1))**.5
        sy=(sum((y-my)**2 for x,y in points)/(n-1))**.5
        lines=['d='+label,'PARAMETER mu_d=POPULATION MEAN PAIRED DIFFERENCE.',
            'DEPENDENT MEASUREMENTS; %d INDEPENDENT PAIRS.' % n,'RANDOM PAIRS: '+random,
            'n=%d; df=n-1=%d' % (n,n-1),'d-bar=%.10g; sd=%.10g' % (mean,sd),
            'SHAPE CHECK APPLIES TO DIFFERENCES: '+normal,
            'Q1=%s; MEDIAN=%s; Q3=%s' % tuple(c.exact_text(stats[k]) for k in ('Q1','MEDIAN','Q3')),
            'LOWER FENCE=%s; UPPER FENCE=%s' % (c.exact_text(stats['LOWER FENCE']),c.exact_text(stats['UPPER FENCE'])),
            'DIFFERENCE OUTLIERS: '+stats['OUTLIERS'],
            'NO OUTLIERS ALONE DOES NOT PROVE NORMALITY.',
            'FIRST mean=%.10g; s=%.10g; n=%d' % (mx,sx,n),
            'SECOND mean=%.10g; s=%.10g; n=%d' % (my,sy,n),
            'USE SD OF DIFFERENCES; DO NOT TREAT THE TWO LISTS AS INDEPENDENT GROUPS.']
        c.view('PAIRED SUMMARY / REQUIREMENTS',lines)
    def hypothesis():
        p,critical,reject=inference
        for index in range(1,10):
            if index==6 and c.ON_TI:
                action=c.call('STHTPLOT','screens',setup,result,p,critical)
                if action=='back': return 'back'
                if action: continue
            if c.view('PAIRED HT STEP '+str(index),c.call(c.call('STHYP','page_module',index),'step',index,setup,result,p,critical,reject)) in ('back','exit'): break
        c.view('PAIRED ERROR INTERPRETATION',[
            'TYPE I ERROR: REJECT H0 EVEN THOUGH IT IS TRUE.',
            'TYPE II ERROR: FAIL TO REJECT H0 EVEN THOUGH H1 IS TRUE.',
            'WHEN H0 IS TRUE, alpha=%.10g IS THE CHANCE OF REJECTING IT BY MISTAKE.' % setup['alpha']])
    def ci():
        estimate,se,critical,bounds=interval
        margin=critical*se
        c.view('PAIRED CONFIDENCE INTERVAL',['d='+label,'CONFIDENCE=%.8g%%' % (100*confidence),
            'df=%d; t*=%.10g' % (n-1,critical)]+c.call('STWORK','mean_se',sd,n,se,'sd')+[
            'E=t*SE=%.10g*%.10g=%.10g' % (critical,se,margin)]+c.call('STWORK','endpoints',mean,margin,bounds)+[
            'INTERVAL=(%.10g, %.10g)' % bounds,
            'WE ARE %.8g%% CONFIDENT THE POPULATION MEAN %s IS BETWEEN %.10g AND %.10g.' % (100*confidence,label,bounds[0],bounds[1]),
            'ZERO IS '+('INSIDE' if bounds[0]<=0<=bounds[1] else 'OUTSIDE')+' THIS INTERVAL.',
            'CI IS TWO-SIDED; COMPARE ITS CONFIDENCE LEVEL WITH THE TEST TAILS.',
            'THIS INTERVAL ESTIMATES THE AVERAGE DIFFERENCE FOR THE POPULATION OF PAIRS.']+
            c.call('STSKETCH','confidence',mean,bounds[0],bounds[1],confidence,critical,'t'))
    summary();table()
    if not test or hypothesis()!='back': ci()
    while True:
        key=c.menu('PAIRED DATA > REVIEW',[('1','SUMMARY / REQUIREMENTS'),('2','PAIR / DIFFERENCE WORK'),
            ('3','HYPOTHESIS TEST' if test else 'DIFFERENCE BOXPLOT'),('4','CONFIDENCE INTERVAL'),('5','DIFFERENCE BOXPLOT' if test else 'SUMMARY AGAIN')])
        if key=='0': return
        if key=='1' or (not test and key=='5'): summary()
        elif key=='2': table()
        elif key=='4': ci()
        elif key=='3' and test: hypothesis()
        else: c.call('STGRAPH','boxplot_data',c.exact_sorted(differences),'PAIRED DIFFERENCE BOXPLOT')
