import STCORE as c

def session(table=False):
    label=input('POPULATION / CATEGORY LABEL (ENTER=SKIP): ').strip()
    random=c.call('STHYIO','check','RANDOM INDEPENDENT OBSERVATIONS?')
    if random is None: return
    alpha=c.read_number('SIGNIFICANCE alpha: ')
    if not 0<alpha<1: raise ValueError('USE 0<alpha<1')
    if table:
        nr=c.read_size('ROW COUNT: ',10,2);nc=c.read_size('COLUMN COUNT: ',10,2)
        rows=[[c.read_int('COUNT R%d C%d: ' % (i+1,j+1)) for j in range(nc)] for i in range(nr)]
        expected,ts,df,rt,ct=c.call('STCHIM','independence',rows)
        observed=[o for row in rows for o in row]
        hypotheses=['H0: ROW AND COLUMN VARIABLES ARE INDEPENDENT.',
                    'H1: ROW AND COLUMN VARIABLES ARE ASSOCIATED.']
        work=['Eij=ROW TOTAL*COLUMN TOTAL/n','df=(%d-1)*(%d-1)=%d' % (nr,nc,df)]
    else:
        nr=1;nc=c.read_size('NUMBER OF CATEGORIES: ',c.MAX_OUTCOMES,2)
        observed=[c.read_int('OBSERVED COUNT %d: ' % (i+1)) for i in range(nc)]
        key=c.menu('EXPECTED FREQUENCIES',[('1','ALL EQUALLY LIKELY'),('2','GIVEN EXPECTED COUNTS'),('3','GIVEN PROBABILITIES')])
        if key=='0': return
        total=sum(observed)
        if key=='1': expected=[total/nc]*nc
        else:
            expected=[c.read_number(('EXPECTED COUNT ' if key=='2' else 'PROBABILITY ')+str(i+1)+': ') for i in range(nc)]
            if key=='3':
                if abs(sum(expected)-1)>1e-7: raise ValueError('PROBABILITIES MUST SUM TO 1')
                expected=[total*p for p in expected]
        fitted=c.read_int('PARAMETERS ESTIMATED FROM SAMPLE (0 IF NONE): ')
        ts,df=c.call('STCHIM','goodness',observed,expected,fitted)
        hypotheses=['H0: POPULATION CATEGORY PROBABILITIES MATCH THE SPECIFIED MODEL.',
                    'H1: AT LEAST ONE CATEGORY PROBABILITY DIFFERS.']
        work=['Ei=n*pi; EQUAL MODEL pi=1/k','df=%d-1-%d=%d' % (nc,fitted,df)]
    probability=c.call('STCHIM','survival',ts,df)
    cv=c.call('STCHIM','critical',alpha,df)
    reject=probability<=alpha
    def row(k):
        o,e=observed[k],expected[k]
        cell='R%d C%d' % (k//nc+1,k%nc+1) if table else 'CATEGORY '+str(k+1)
        expression=('E=%g*%g/%g=%g' % (rt[k//nc],ct[k%nc],sum(rt),e) if table else
                    'E=%g*(%g/%g)=%g' % (sum(observed),e,sum(observed),e))
        return cell+': O=%g; ' % o+expression+'; (O-E)^2/E=(%g-%g)^2/%g=%.8g' % (o,e,e,(o-e)**2/e)
    prefix=[label or 'CHI-SQUARE TEST','RANDOM INDEPENDENT: '+random]+hypotheses+[
        'EXPECTED >=5: '+('PASS' if min(expected)>=5 else 'NOT MET; ASYMPTOTIC RESULT MAY BE UNRELIABLE'),
        'COUNT CHECKS AND SAMPLING CONDITIONS MUST HOLD.']+work+[
        'chi-square=SUM((O-E)^2/E)=%.10g' % ts,'df=%d; alpha=%.8g' % (df,alpha),
        'RIGHT-TAIL CV=%.10g' % cv,'p=P(chi-square_%d >= %.10g)=%.10g' % (df,ts,probability),
        'REJECT H0' if reject else 'FAIL TO REJECT H0',
        ('SUFFICIENT' if reject else 'INSUFFICIENT')+' EVIDENCE OF '+('AN ASSOCIATION.' if table else 'A DIFFERENCE FROM THE MODEL.'),
        'IF H0 WERE TRUE, A chi-square VALUE THIS LARGE OR LARGER WOULD OCCUR ABOUT %.6g%% OF THE TIME. THIS IS NOT THE CHANCE H0 IS TRUE.' % (100*probability),
        'CELL WORK / EXPECTED MATRIX (ROW-MAJOR)']
    drawing=['HOW TO DRAW: chi-square AXIS >=0; df=%d' % df,
        'RIGHT-SKEWED FOR SMALL df; NO NEGATIVE TAIL.',
        'REJECTION GRAPH: MARK CV=%.8g; SHADE RIGHT; AREA=%.8g' % (cv,alpha),
        'p GRAPH: MARK TS=%.8g; SHADE RIGHT; AREA=%.8g' % (ts,probability),
        'NO ASSOCIATION DOES NOT MEAN PROVEN INDEPENDENCE.' if table else 'FAILURE TO REJECT DOES NOT PROVE THE MODEL.']
    lines=c.call('STWORK','Lines',len(observed),row)
    addition=c.call('STWORK','sum_work','chi-square',len(observed),
        lambda i:'(%g-%g)^2/%g' % (observed[i],expected[i],expected[i]),ts)
    c.view('CHI-SQUARE TEST',c.call('STWORK','Chain',prefix,lines,addition,drawing))
