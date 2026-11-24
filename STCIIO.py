from STSIZE import _read_number, _read_confidence
import STCORE as c
def _show_result(title, estimate, se, critical, interval, confidence, df=None,
        warning=None, estimate_label='ESTIMATE', parameter='POPULATION VALUE',
        critical_label='CRITICAL VALUE', input_summary=(), work=(), summary_inputs=()):
  lines=c.summary(['CI=(%.6g, %.6g)' % interval,'C=%.5g%%' % (100*confidence),'alpha=%.5g' % (1-confidence),
    estimate_label+'=%.6g' % estimate,'SE=%.6g' % se,'E=%.6g' % (critical*se),
    critical_label+'=%.6g' % critical]+(['df=%.6g' % df] if df is not None else [])+list(summary_inputs))
  lines+=list(input_summary)
  lines.extend(['CONFIDENCE='+('%.1f' % (100*confidence))+'%',
      'ALPHA='+('%.4f' % (1-confidence)),
      estimate_label+'='+('%.4f' % estimate),
      'STANDARD ERROR='+('%.4f' % se),
      critical_label+'='+('%.4f' % critical),
      'MARGIN OF ERROR='+('%.4f' % (critical*se))])
  if df is not None:
    lines.append('DF='+('%.2f' % df))
  lines.extend(work)
  lines.extend(['E='+critical_label+'*SE=%.10g*%.10g=%.10g' % (critical,se,critical*se)])
  lines.extend(c.call('STWORK','endpoints',estimate,critical*se,interval))
  lines.extend(['INTERVAL=('+('%.4f' % interval[0])+', '+('%.4f' % interval[1])+')',
         'INTERPRETATION: '+parameter+' IS ESTIMATED WITH THIS INTERVAL.'])
  if warning:
    lines.append(warning)
  lines=lines+c.call('STSKETCH','confidence',estimate,interval[0],interval[1],
         confidence,critical,'t' if df is not None else 'z')
  c.view(title,lines)
def zstar_session():
  critical_session('z')

def tstar_session():
  critical_session('t')

def critical_session(kind,first=None,direct_df=False):
  key=first or c.menu(kind.upper()+'* CRITICAL VALUE: GIVEN',[
    ('1','TWO-SIDED CONFIDENCE LEVEL'),('2','TWO-SIDED alpha'),
    ('3','AREA TO RIGHT OF CUTOFF'),('4','AREA TO LEFT / PERCENTILE'),
    ('5','ONE-SIDED CONFIDENCE LEVEL'),('6','AREA BETWEEN 0 AND CUTOFF')])
  if key=='0': return
  area=_read_number({'1':'CONFIDENCE LEVEL: ','2':'TOTAL alpha: ',
    '3':'RIGHT-TAIL AREA: ','4':'LEFT-TAIL AREA: ',
    '5':'ONE-SIDED CONFIDENCE: ','6':'AREA FROM 0 TO CUTOFF: '}[key])
  if not 0<area<1 or (key=='6' and area>=.5):
    raise ValueError('USE 0<AREA<1; FROM ZERO USE AREA<0.5')
  side=None
  if key in ('5','6'):
    side=c.menu('WHICH CUTOFF?',[('1','LOWER CUTOFF / LEFT TAIL'),('2','UPPER CUTOFF / RIGHT TAIL')])
    if side=='0': return
  left=(1+area)/2 if key=='1' else 1-area/2 if key=='2' else 1-area if key=='3' else area
  if key=='5': left=1-area if side=='1' else area
  if key=='6': left=.5-area if side=='1' else .5+area
  details=['INPUT AREA=%.6f' % area,'AREA TO LEFT=%.6f' % left]
  details+=[{'1':'LEFT=(1+C)/2','2':'LEFT=1-alpha/2','3':'LEFT=1-RIGHT AREA',
       '4':'LEFT=GIVEN PERCENTILE','5':'LEFT=1-C (LOWER) OR C (UPPER)',
       '6':'LEFT=0.5-AREA (LOWER) OR 0.5+AREA (UPPER)'}[key]]
  if kind=='t':
    source='1' if direct_df else c.menu('t DEGREES OF FREEDOM',[('1','ENTER df DIRECTLY'),('2','ONE-SAMPLE / PAIRED: ENTER n')])
    if source=='0': return
    degrees=_read_number('df: ') if source=='1' else c.read_int('SAMPLE SIZE / NUMBER OF PAIRS n: ')-1
    value=c.call('STTCRIT','t_quantile',left,degrees)
    details+=['df=%.4f' % degrees,'invT(%.6f,%.4f)' % (left,degrees)]
    if source=='2': details+=['df=n-1=%.0f-1=%.4f' % (degrees+1,degrees)]
  else:
    degrees=1
    value=c.call('STZCRIT','standard_normal_quantile',left)
    details+=['invNorm(%.6f,0,1)' % left]
  if key in ('1','2'):
    details+=['CRITICAL VALUES=+/-%.6f' % value,
         'EACH TAIL=%.6f' % (1-left)]
    bounds=(-value,value); shading='3' if key=='1' else 'outside'
  else:
    details+=['SIGNED CRITICAL CUTOFF=%.6f' % value]
    bounds=(value,); shading='2' if key=='3' or (key=='5' and side=='2') else '1'
    if key=='6': bounds=(min(0,value),max(0,value)); shading='3'
  if key=='5': details+=['ONE-SIDED alpha=%.6f; SHADE THAT TAIL.' % (1-area)]
  details=details+c.call('STSKETCH','curve','t' if kind=='t' else 'NORMAL',0,degrees,shading,bounds,kind)
  c.view(kind.upper()+'* CRITICAL VALUE',c.summary([
    'CV='+('+/-' if key in ('1','2') else '')+'%.6g' % value,
    'LEFT AREA=%.6g' % left]+(['df=%.6g' % degrees] if kind=='t' else []))+details)
  estimate_work(value,key,side)

def estimate_work(critical,method,side):
  options=[('1','POINT ESTIMATE + STANDARD ERROR'),
      ('2','POINT ESTIMATE + MARGIN OF ERROR')]
  if method!='5': options.append(('3','GIVEN TWO-SIDED INTERVAL ENDS'))
  source=c.menu('ESTIMATE / MARGIN: 0 SKIP',options)
  if source=='0': return
  if source=='3':
    low=_read_number('LOWER INTERVAL END: ')
    high=_read_number('UPPER INTERVAL END: ')
    if low>high: raise ValueError('LOWER END MUST NOT EXCEED UPPER END')
    estimate=(low+high)/2; margin=(high-low)/2
    work=['POINT ESTIMATE=(LOW+HIGH)/2',
       '(%.6f+%.6f)/2=%.6f' % (low,high,estimate),
       'E=(HIGH-LOW)/2',
       '(%.6f-%.6f)/2=%.6f' % (high,low,margin)]
  else:
    estimate=_read_number('POINT ESTIMATE (x-bar OR p-hat): ')
    work=['POINT ESTIMATE=%.6f (GIVEN)' % estimate]
    if source=='1':
      se=_read_number('STANDARD ERROR SE: ')
      if se<0: raise ValueError('SE MUST BE NONNEGATIVE')
      margin=abs(critical)*se
      work+=['E=abs(CRITICAL)*SE',
         'abs(%.6f)*%.6f=%.6f' % (critical,se,margin)]
    else:
      margin=_read_number('GIVEN MARGIN OF ERROR E: ')
      if margin<0: raise ValueError('MARGIN MUST BE NONNEGATIVE')
      work+=['E=%.6f (GIVEN)' % margin]
  if source!='1':
    if critical==0:
      se=None
      work+=['SE CANNOT BE RECOVERED FROM A ZERO CRITICAL VALUE.']
    else:
      se=margin/abs(critical)
      work+=['SE=E/abs(CRITICAL)',
         '%.6f/abs(%.6f)=%.6f' % (margin,critical,se)]
  lines=['POINT ESTIMATE=%.6f' % estimate,'MARGIN OF ERROR E=%.6f' % margin,
     'CRITICAL CUTOFF=%.6f' % critical]
  if se is not None: lines+=['STANDARD ERROR=%.6f' % se]
  lines+=work
  if method=='5':
    if source=='1': bound=estimate-critical*se
    else: bound=estimate-margin if critical>=0 else estimate+margin
    lines+=['UPPER ONE-SIDED BOUND' if side=='1' else 'LOWER ONE-SIDED BOUND',
        'BOUND=ESTIMATE-CRITICAL*SE' if source=='1' else 'BOUND=ESTIMATE +/- GIVEN E (USING CRITICAL SIGN)',
        'BOUND=%.6f' % bound,
        'DRAW A NUMBER LINE; MARK THE ESTIMATE AND BOUND.',
        'CONFIDENCE REGION EXTENDS LEFT.' if side=='1' else 'CONFIDENCE REGION EXTENDS RIGHT.']
  else:
    low,high=estimate-margin,estimate+margin
    lines+=['INTERVAL=ESTIMATE +/- E' if method in ('1','2') or source=='3' else 'SYMMETRIC RANGE USING abs(CUTOFF)',
        '(%.6f-%.6f, %.6f+%.6f)' % (estimate,margin,estimate,margin),
        'ENDS=(%.6f, %.6f)' % (low,high),
        'DRAW NUMBER LINE; MARK BOTH ENDS AND THE CENTER.']
  graph=('STGINTR','show',(estimate,bound if side=='2' else estimate, bound if side=='1' else estimate,None,'ESTIMATE','upper' if side=='1' else 'lower')) if method=='5' else ('STGINTR','show',(estimate,low,high,None))
  c.view('POINT ESTIMATE / MARGIN / WORK',c.graph_lines(lines,graph))

def _show_zstar(title, confidence, critical, values):
  lines = ['CONFIDENCE='+('%.2f' % (100*confidence))+'%',
      'z*='+('%.4f' % critical)]
  lines.extend(values)
  lines=lines+c.call('STSKETCH','curve','NORMAL',0,1,'3',(-critical,critical),'z')
  c.view(title,lines)
