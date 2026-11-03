import STCORE as c

def read_pairs(minimum=3):
    key=c.menu('PAIRED DATA INPUT',[('1','ENTER x,y PAIRS'),('2','TI LISTS L1-L6 (KEEP PAIRS)')])
    if key=='0': return
    if key=='1':
        n=c.read_size('NUMBER OF PAIRS: ',100,minimum)
        return [(c.read_number('x%d: ' % (i+1)),c.read_number('y%d: ' % (i+1))) for i in range(n)]
    # Do not use read_raw: it sorts each list, destroying pair correspondence.
    try: from ti_system import recall_list
    except ImportError: raise ValueError('TI LIST IMPORT REQUIRES ti_system.recall_list')
    lx=c.read_size('x LIST NUMBER (1..6): ',6);ly=c.read_size('y LIST NUMBER (1..6): ',6)
    xs=recall_list(str(lx));ys=recall_list(str(ly))
    if xs is None or ys is None or len(xs)!=len(ys) or not minimum<=len(xs)<=100:
        raise ValueError('LISTS NEED MATCHING %d..100 VALUES' % minimum)
    return [(float(xs[i]),float(ys[i])) for i in range(len(xs))]

def session():
    points=read_pairs()
    if points is None: return
    xlabel=input('x VARIABLE / UNITS (ENTER=SKIP): ').strip() or 'x'
    ylabel=input('y VARIABLE / UNITS (ENTER=SKIP): ').strip() or 'y'
    alpha=c.read_number('CORRELATION SIGNIFICANCE alpha: ')
    result=c.call('STREG','fit',points,alpha)
    def work(i):
        x,y=points[i];dx=x-result['mx'];dy=y-result['my']
        predicted=result['my']+result['slope']*(x-result['mx'])
        return 'PAIR %d: x=%g y=%g; dx=%g dy=%g; dx^2=%g dy^2=%g dx*dy=%g; yhat=%.10g; e=%g-%.10g=%.10g' % (i+1,x,y,dx,dy,dx*dx,dy*dy,dx*dy,predicted,y,predicted,y-predicted)
    first=True
    while True:
        key='1' if first else c.menu('REGRESSION / CORRELATION',[('1','ALL WORK / RESULTS'),('2','SCATTERPLOT / AXES'),
            ('3','PREDICT y FROM x'),('4','RESIDUAL: OBSERVED - PREDICTED'),('5','PAIRED WORK TABLE'),('6','FITTED LINE GRAPH'),('7','RESIDUAL GRAPH'),('8','TEST DISTRIBUTION GRAPH')])
        first=False
        if key=='0': return
        if key in ('2','6','7'):
            if not c.call('STGSCAT','show',points,xlabel,ylabel,(result['intercept'],result['slope']) if key!='2' else None,key=='7'):
                c.view('SCATTERPLOT',['x: '+xlabel,'y: '+ylabel]+c.call('STREG','scatter',points))
        elif key=='8':
            if result['r'] is None: c.view('NO CORRELATION INFERENCE',['CONSTANT y: CORRELATION UNDEFINED.'])
            else:
                critical=c.call('STTCRIT','t_quantile',1-alpha/2,result['df'])
                c.call('STGINFER','correlation',result['ts'],result['df'],alpha,result['p'],critical)
        elif key in ('3','4'):
            x=c.read_number('x TO PREDICT: ');predicted=c.call('STREG','predict',result,x)
            lines=['yhat=ybar+b*(x-xbar)','yhat=%.10g+%.10g*(%.10g-%.10g)=%.10g' % (result['my'],result['slope'],x,result['mx'],predicted),
                   'PREDICTION UNITS: '+ylabel]
            if x<min(p[0] for p in points) or x>max(p[0] for p in points): lines.append('EXTRAPOLATION: OUTSIDE OBSERVED x RANGE.')
            if key=='4':
                y=c.read_number('OBSERVED y: ')
                lines.append('RESIDUAL=y-yhat=%.10g-%.10g=%.10g' % (y,predicted,y-predicted))
            c.view('PREDICTION / RESIDUAL',lines)
        elif key=='5': c.view('PAIRED WORK TABLE',c.call('STWORK','Lines',len(points),work))
        else:
            r=result['r'];p=result['p']
            lines=['x: '+xlabel,'y: '+ylabel,'n=%d; df=n-2=%d' % (result['n'],result['df']),
                'xbar=%.10g; ybar=%.10g' % (result['mx'],result['my']),
                'Sxx=SUM((x-xbar)^2)=%.10g' % result['xx'],
                'Syy=SUM((y-ybar)^2)=%.10g' % result['yy'],
                'Sxy=SUM((x-xbar)*(y-ybar))=%.10g' % result['xy'],
                'b=Sxy/Sxx=%.10g/%.10g=%.10g' % (result['xy'],result['xx'],result['slope']),
                'a=ybar-b*xbar=%.10g-%.10g*%.10g=%.10g' % (result['my'],result['slope'],result['mx'],result['intercept']),
                'yhat=%.10g+%.10g*x' % (result['intercept'],result['slope']),
                'USE CENTERED FORM FOR PREDICTION: ybar+b*(x-xbar)',
                'SLOPE: FITTED y CHANGES BY %.10g y UNITS PER 1 x UNIT.' % result['slope'],
                'H0: rho=0; H1: rho!=0; TWO-SIDED',
                'REQUIRE INDEPENDENT RANDOM PAIRS, APPROXIMATELY LINEAR RELATIONSHIP; NORMAL HOMOSCEDASTIC ERRORS FOR t INFERENCE; CHECK OUTLIERS.']
            if r is None: lines+=['CONSTANT y: r, r^2 AND CORRELATION INFERENCE UNDEFINED.']
            else:
                lines+=['r=Sxy/sqrt(Sxx*Syy)=%.10g/sqrt(%.10g*%.10g)=%.10g' % (result['xy'],result['xx'],result['yy'],r),
                    'r^2=%.10g; EXPLAINED VARIATION=%.6g%%' % (result['r2'],100*result['r2']),
                    'CRITICAL r=+/-%.10g AT alpha=%.8g' % (result['rc'],alpha),
                    'r*=t*/sqrt(t*^2+df); SAME TWO-SIDED THRESHOLD AS r TABLE.',
                    't=r*sqrt((n-2)/(1-r^2))',
                    ('PERFECT FIT: |t| IS INFINITE.' if result['ts'] is None else
                     't=%.10g*sqrt(%d/(1-%.10g^2))=%.10g' % (r,result['df'],r,result['ts'])),
                    'p=2*P(T_%d >= |t|)=%.10g' % (result['df'],p),
                    'REJECT H0' if p<=alpha else 'FAIL TO REJECT H0',
                    ('SUFFICIENT' if p<=alpha else 'INSUFFICIENT')+' EVIDENCE OF LINEAR CORRELATION, IF REQUIREMENTS HOLD.',
                    'r^2: FRACTION OF OBSERVED y VARIATION EXPLAINED BY THE FITTED LINE.',
                    'ASSOCIATION DOES NOT ESTABLISH CAUSATION.']
            c.view('REGRESSION WORK / RESULTS',c.call('STWORK','Chain',lines,c.call('STWORK','Lines',len(points),work)))
