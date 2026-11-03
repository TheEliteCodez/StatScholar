import STCORE as c

def read_event():
    key=c.menu('EXACT SAMPLING PROBABILITY',[
        ('1','BELOW A VALUE'),('2','ABOVE A VALUE'),
        ('3','BETWEEN (ENDS INCLUDED)')])
    if key=='0': return None
    a=c.read_exact('LOWER VALUE: ' if key=='3' else 'CUTOFF VALUE: ')
    b=c.read_exact('UPPER VALUE: ') if key=='3' else (0,1)
    if key=='3' and c.compare_exact(a,b)>0:
        raise ValueError('LOWER VALUE MUST NOT EXCEED UPPER VALUE')
    return ({'1':'<','2':'>','3':'[]'}[key],a,b)

def design(random,population):
    if random=='PASS' and population is None: return '1'
    return c.menu('EXACT METHOD: SAMPLE DESIGN',[
        ('1','INDEPENDENT / WITH REPLACEMENT'),
        ('2','RANDOM WITHOUT REPLACEMENT'),('3','NOT KNOWN / OTHER DEPENDENCE')])

def show(title,probability,event,lines,graph=None):
    c.results(title,[('P',probability)],drawing=lines+[
        'REQUESTED EVENT: '+event[0]+' '+c.exact_text(event[1])+
        (' TO '+c.exact_text(event[2]) if event[0]=='[]' else '')],graph=graph)

def proportion_fallback(p,n,random,population):
    model=design(random,population)
    if model=='0': return
    if model=='3':
        c.view('EXACT METHOD NEEDS A MODEL',['DEPENDENT OUTCOMES NEED THEIR JOINT DISTRIBUTION.'])
        return
    if model=='2':
        population=population or c.read_int('POPULATION SIZE N: ')
        inferred=c.rmul(p,(population,1))
        targets=inferred[0] if inferred[1]==1 else c.read_int('EXACT POPULATION SUCCESS COUNT K: ')
        if not 1<=n<=population or not 0<=targets<=population:
            raise ValueError('REQUIRE 0<=K<=N AND 1<=n<=N')
        model_lines=['EXACT HYPERGEOMETRIC; WITHOUT REPLACEMENT.',
                     'N=%d; K=%d; n=%d' % (population,targets,n)]
    else:
        model_lines=['EXACT BINOMIAL; INDEPENDENT TRIALS.',
                     'n=%d; p=%s' % (n,c.exact_text(p))]
    c.view('SWITCH TO EXACT PROPORTION',model_lines+['p-hat=X/n; USE PROPORTION CUTOFFS.'])
    event=read_event()
    if event is None: return
    op,a,b=event
    counts=(op,c.rmul(a,(n,1)),c.rmul(b,(n,1)))
    if model=='2':
        probability=c.call('STSAMP1','event_probability',population,targets,n,counts)
        low,high=max(0,n-population+targets),min(n,targets)
    else:
        probability=c.call('STBMATH','binomial_exact_event',n,p,counts)
        low,high=0,n
    show('EXACT SAMPLE PROPORTION',probability,event,model_lines+
         c.call('STSKETCH','bars',low,high,counts)+['COUNT AXIS X; p-hat=X/n.'],('STGBARS','show',(('hyper',population,targets,n) if model=='2' else ('binomial',n,p),counts,'EXACT SAMPLE PROPORTION',False,n)))

def uniform_cdf(x,a,b,n):
    t=c.rdiv(c.rmul(c.radd(x,(-a[0],a[1])),(n,1)),c.radd(b,(-a[0],a[1])))
    if c.compare_exact(t,0)<=0: return (0,1)
    if c.compare_exact(t,n)>=0: return (1,1)
    total=(0,1)
    for k in range(t[0]//t[1]+1):
        delta=c.radd(t,(-k,1))
        term=c.rmul(((-1)**k*c.call('STCOMB','ncr',n,k),1),(delta[0]**n,delta[1]**n))
        total=c.radd(total,term)
    factorial=1
    for k in range(2,n+1): factorial*=k
    return c.rdiv(total,(factorial,1))

def mean_fallback(mean,sigma,n,random,population,normal_known=False):
    model=design(random,population)
    if model=='0': return
    if model=='2' and population==n:
        event=read_event()
        if event is not None:
            probability=(1,1) if c.event_match(c.as_ratio(str(mean)),*event) else (0,1)
            show('EXACT CENSUS MEAN',probability,event,[
                'ENTIRE POPULATION: x-bar=mu=%.4f' % mean,
                'HOW TO DRAW: ONE POINT AT mu.', 'STANDARD ERROR=0.'])
        return
    if model=='3':
        c.view('MEAN NEEDS MORE INFORMATION',[
            'FINITE / DEPENDENT SAMPLE MEANS NEED THE POPULATION VALUES OR JOINT MODEL.',
            'MEAN AND SD ALONE DO NOT DETERMINE THIS PROBABILITY.'])
        return
    if model=='1' and (normal_known or n>=30):
        c.call('STCLTR','_result','INDEPENDENT SAMPLE MEAN','x-bar',
               mean,sigma/n**.5,n,['CONFIRMED INDEPENDENT / WITH REPLACEMENT.'],
               'NORMAL POPULATION' if normal_known else 'APPROXIMATELY NORMAL BY CLT',
               '',True,True,'mu',sigma)
        return
    key='2' if model=='2' else c.menu('SMALL SAMPLE: POPULATION MODEL',[
        ('1','KNOWN UNIFORM POPULATION'),('2','KNOWN DISCRETE X / P(X) TABLE'),
        ('3','ONLY MEAN / SD KNOWN')])
    if key=='0': return
    if key=='3':
        c.view('INSUFFICIENT DISTRIBUTION DATA',[
            'MEAN AND SD DO NOT DETERMINE THE SMALL-SAMPLE PROBABILITY.',
            't IS NOT A REPLACEMENT FOR A NONNORMAL POPULATION MODEL.'])
        return
    if key=='1':
        a=c.read_exact('POPULATION LOWER ENDPOINT a: ')
        b=c.read_exact('POPULATION UPPER ENDPOINT b: ')
        if c.compare_exact(a,b)>=0: raise ValueError('REQUIRE a<b')
        lines=['EXACT MEAN OF %d INDEPENDENT UNIFORMS.' % n,
               'POPULATION [a,b]=[%s,%s]' % (c.exact_text(a),c.exact_text(b)),
               'HOW TO DRAW: SAMPLE MEAN',
               'SUPPORT a TO b; CENTER=(a+b)/2.',
               'n=1: RECTANGLE; n=2: TRIANGLE.',
               'n>2: SYMMETRIC CONVOLUTION CURVE.',
               'SD=(b-a)/sqrt(12*n).']
        width=c.number(c.radd(b,(-a[0],a[1])))
        lines+=['CENTER=%.4f; SD=%.4f' %
                (c.number(c.radd(a,b))/2,width/(12*n)**.5)]
    else:
        if model=='2':
            values=c.call('STDMATH','read_raw','ENTIRE FINITE POPULATION')
            if n>len(values) or (population is not None and len(values)!=population):
                raise ValueError('NEED ALL N VALUES AND n<=N')
            ways=[{} for i in range(n+1)]
            ways[0][(0,1)]=1
            for i,x in enumerate(values):
                for j in range(min(n,i+1),0,-1):
                    for total,count in ways[j-1].items():
                        value=c.radd(total,x)
                        ways[j][value]=ways[j].get(value,0)+count
            denom=c.call('STCOMB','ncr',len(values),n)
            sums={x:c.ratio(count,denom) for x,count in ways[n].items()}
        else:
            rows,approximate=c.call('STCOUNT','read_distribution')
            if approximate or any(c.compare_exact(p,0)<0 for x,p in rows) or c.rsum(p for x,p in rows)!=(1,1):
                raise ValueError('EXACT METHOD NEEDS NONNEGATIVE P SUMMING TO 1')
            sums={(0,1):(1,1)}
            for i in range(n):
                next_sums={}
                for total,prob in sums.items():
                    for x,p in rows:
                        value=c.radd(total,x)
                        next_sums[value]=c.radd(next_sums.get(value,(0,1)),c.rmul(prob,p))
                sums=next_sums
        rows=[(c.rdiv(x,(n,1)),p) for x,p in sums.items()]
        lines=['EXACT DISCRETE SAMPLE MEAN; n=%d.' % n,
               'RANDOM WITHOUT REPLACEMENT.' if model=='2' else 'INDEPENDENT DRAWS FROM ENTERED TABLE.',
               'HOW TO DRAW: x-bar PROBABILITY BARS',
               'HEIGHT=P(x-bar); NO NORMAL CURVE.']
        actual_mean,variance,sd=c.call('STCOUNT','distribution_moments',rows)
        lines+=['CENTER=%s; SD=%.4f' % (c.exact_text(actual_mean),sd)]
    lines+=['ENTERED ENDPOINTS / TABLE DEFINE THE EXACT MODEL.',
            'ORIGINAL mu=%.4f; SD=%.4f; n=%d' % (mean,sigma,n)]
    c.view('SWITCH TO EXACT SAMPLE MEAN',lines)
    event=read_event()
    if event is None: return
    op,low,high=event
    if key=='1':
        left=uniform_cdf(low,a,b,n)
        probability=left if op=='<' else c.radd((1,1),(-left[0],left[1])) if op=='>' else c.radd(uniform_cdf(high,a,b,n),(-left[0],left[1]))
    else:
        probability=c.call('STCOUNT','table_probability',rows,event)
    graph=('STGUMEA','show',(c.number(a),c.number(b),n,event,c.number(probability))) if key=='1' else ('STGBARS','show',(('rows',sorted(rows,key=lambda row:c.number(row[0]))),event,'EXACT SAMPLE MEAN'))
    show('EXACT SAMPLE MEAN',probability,event,lines+[
        'SHADE LEFT / RIGHT / BETWEEN AS REQUESTED.'],graph)
    if key=='2':
        rows=sorted(rows,key=lambda row:c.number(row[0]))
        c.paged_results('EXACT x-bar HEIGHTS',len(rows),lambda i:(c.exact_text(rows[i][0]),rows[i][1]))
