# Author: TheEliteCodez
# Wording-led binomial UI; imports only small arithmetic dependencies.
import STCORE as c

PAGES = (
 (('EXACTLY / P(X=n)','='),('AT MOST / X<=n','<='),('AT LEAST / X>=n','>='),
  ('LESS THAN / X<n','<'),('MORE THAN / X>n','>'),('BETWEEN TWO VALUES','[]'),
  ('AT LEAST ONE','one'),('MEAN / SD / USUAL','stats'),('IS THIS BINOMIAL?','conditions')),
 (('FULL DISTRIBUTION','full'),('GRAPH / SHAPE','shape'),('DEFINE X, n, p','model'),
  ('USUAL COUNTS / TAILS','usual'),('FORMULA / CHEAT SHEET','cheat'),('WITHOUT REPLACEMENT','sample'),('FINITE SAMPLE / 5% CHECK','finite')))
WORDS={'=':'EXACTLY','<=':'AT MOST','>=':'AT LEAST','<':'LESS THAN','>':'MORE THAN','[]':'BETWEEN','()':'BETWEEN','[)':'BETWEEN','(]':'BETWEEN','!=':'NOT EQUAL'}


def floor_ratio(x):
    a,b=c.to_ratio(x)
    return a//b


def ceil_ratio(x):
    a,b=c.to_ratio(x)
    return -(-a//b)


def event_bounds(n,event):
    op,a,b=event
    if op=='=':
        k=floor_ratio(a)
        return (k,k) if c.compare_exact(a,k)==0 else (1,0)
    if op=='<=': return 0,floor_ratio(a)
    if op=='<': return 0,ceil_ratio(a)-1
    if op=='>=': return ceil_ratio(a),n
    if op=='>': return floor_ratio(a)+1,n
    return (ceil_ratio(a) if op[0]=='[' else floor_ratio(a)+1,
            floor_ratio(b) if op[-1]==']' else ceil_ratio(b)-1)


def translation(n,p,event):
    op,a,b=event
    text=c.exact_text(a)
    words=WORDS[op]+' '+text
    if op in ('[]','()','[)','(]'): words+=' TO '+c.exact_text(b)
    low,high=event_bounds(n,event)
    def cdf(k):
        if k<0: return '0'
        if k>=n: return '1'
        return 'binomcdf('+str(n)+','+c.exact_text(p)+','+str(k)+')'
    if op=='=':
        command='binompdf('+str(n)+','+c.exact_text(p)+','+text+')' if low<=high and 0<=low<=n else '0'
        why='PDF COUNTS ONE EXACT VALUE; CDF ADDS A LOWER TAIL.'
    elif op in ('<','<='):
        command=cdf(high)
        why='KEEP 0 THROUGH '+str(min(n,high))+'. '+('CUTOFF INCLUDED.' if op=='<=' else 'CUTOFF EXCLUDED: USE THE INTEGER BELOW IT.')
    elif op in ('>','>='):
        command='1-'+cdf(low-1)
        why='KEEP '+str(max(0,low))+' THROUGH '+str(n)+'. REMOVE 0 THROUGH '+str(low-1)+'. AT LEAST INCLUDES THE CUTOFF; MORE THAN EXCLUDES IT.'
    else:
        command=cdf(high)+' - '+cdf(low-1)
        why='KEEP INTEGERS '+str(low)+' THROUGH '+str(high)+'. SUBTRACT THE TAIL BELOW THE LOWER INCLUDED VALUE.'
    if low>high: command='0'
    math_text='P(X '+op+' '+text+')' if len(op)==1 or op in ('<=','>=') else 'P('+str(low)+' <= X <= '+str(high)+')'
    return words,math_text,command,why


def read_event(op):
    if op=='one': return '>=',(1,1),0
    a=c.read_exact('LOWER: ' if op=='[]' else 'CUTOFF r: ')
    b=0
    if op=='[]':
        b=c.read_exact('UPPER: ')
        key=c.menu('BINOMIAL > ENDPOINTS',[('1','BOTH INCLUDED [a,b]'),('2','NEITHER (a,b)'),('3','LOWER ONLY [a,b)'),('4','UPPER ONLY (a,b]')])
        if key=='0': return None
        op={'1':'[]','2':'()','3':'[)','4':'(]'}[key]
    return op,a,b


def read_parameters():
    return c.read_int('TRIALS n: '),c.read_exact('CHANCE p (DECIMAL OR %): ')


def wording_session(first=None,n=None,p=None):
    while True:
        op=first or c.choice_pages('BINOMIAL > QUESTION WORDS',PAGES)
        first=None
        if op is None: return
        if op=='conditions':
            c.call('STBEXTRA','binomial_conditions');continue
        if op=='cheat':
            c.call('STBHELP','cheat_sheet');continue
        if op=='finite':
            c.call('STFINITE','finite_check');continue
        if op=='sample':
            c.call('STSAMPLE','sample_session');continue
        if n is None: n,p=read_parameters()
        if op in ('stats','usual','shape','model','full'):
            c.call('STBHELP','parameter_results',op,n,p)
            continue
        event=read_event(op)
        if event is None: continue
        answer=c.call('STBMATH','binomial_exact_event',n,p,event)
        words,math_text,command,why=translation(n,p,event)
        style,places='D',4
        while True:
            lines=['ANSWER='+c.answer_text(answer,style,places),math_text,'RIGHT: STATS / USUAL / z' if c.HAS_KEYS else 'ENTER: STATS / USUAL / z']
            count=sum(1 for line in c.wrapped_lines(lines))
            lines+=['']*((-count)%c.VIEW_LINES)
            lines+=c.call('STBINFO','followup',n,p,event,answer)
            c.view('BINOMIAL > '+WORDS[event[0]],lines)
            lines=None
            key=c.menu('BINOMIAL > SAME n,p',[('1','NEXT PART, SAME n,p'),('2','SHOW WHY'),('3','TRANSLATION / FORMULA'),('4','CHANGE n,p'),('5','ANSWER FORMAT'),('6','IS THIS EVENT UNUSUAL?'),('7','MEAN / SD / VAR / USUAL')])
            if key=='0': return
            if key=='1': break
            if key=='2': c.view('BINOMIAL > WHY',[why,'n='+str(n)+' p='+c.exact_text(p)])
            elif key=='3': c.view('BINOMIAL > FORMULA',[words,math_text,'TI-84:',command,'P(X=k)=C(n,k)*p^k*(1-p)^(n-k)','SUM OVER INCLUDED INTEGER k'])
            elif key=='4':
                n,p=read_parameters();break
            elif key=='7': c.call('STBHELP','parameter_results','stats',n,p)
            elif key=='6': c.call('STBHELP','event_unusual',answer,math_text)
            elif key=='5':
                fmt=c.menu('BINOMIAL > FORMAT',[('1','DECIMAL'),('2','FRACTION'),('3','PERCENT')])
                if fmt=='0': continue
                style={'1':'D','2':'F','3':'P'}[fmt]
                if style!='F': places=c.read_int('DECIMAL PLACES: ')
