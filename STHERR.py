import STCORE as c

DEFINITIONS=(
  'TYPE I: REJECT H0 WHEN H0 IS TRUE. FALSE POSITIVE; ITS PROBABILITY IS alpha.',
  'TYPE II: FAIL TO REJECT H0 WHEN H0 IS FALSE. FALSE NEGATIVE; ITS PROBABILITY IS beta.',
  'POWER=1-beta: REJECT H0 WHEN IT IS FALSE.',
  'FAIL TO REJECT DOES NOT MEAN ACCEPT OR PROVE H0.',
  'A DECISION ALONE DOES NOT TELL YOU WHETHER AN ERROR OCCURRED. YOU ALSO NEED THE ACTUAL TRUTH.')

def model(parameter,relation,value,context='',given_null=False,alternative=None,claim_side=None):
  opposite={'<':'>=','>':'<=','!=':'=','<=':'>','>=':'<','=':'!='}
  if given_null:
    null=relation
    alt=alternative if relation=='=' else opposite[relation]
    side=claim_side
  else:
    side='H0' if '=' in relation and relation!='!=' else 'H1'
    null=relation if side=='H0' else opposite[relation]
    alt=opposite[relation] if side=='H0' else relation
  return {'h0':parameter+' '+null+' %.10g' % value,
          'h1':parameter+' '+alt+' %.10g' % value,'claim':side,'context':context}

def describe(m):
  if m['claim']=='H1':
    first=['I: SUPPORT A FALSE CLAIM','II: MISS A TRUE CLAIM']
  elif m['claim']=='H0':
    first=['I: REJECT A TRUE CLAIM','II: FAIL TO REJECT FALSE CLAIM']
  else:first=['I: REJECT A TRUE H0','II: FAIL TO REJECT FALSE H0']
  rows=first+['H0: '+m['h0'],'H1: '+m['h1']]
  if m['claim']:rows.append('CLAIM IS '+m['claim'])
  if m['context']:rows.append('CONTEXT: '+m['context'])
  rows+=['TYPE I IN THIS QUESTION:',
    'CONCLUDE '+m['h1']+' WHEN ACTUALLY '+m['h0']+'.',
    'TYPE II IN THIS QUESTION:',
    'FAIL TO FIND EVIDENCE FOR '+m['h1']+' WHEN ACTUALLY '+m['h1']+'.',
    'H0 CONTAINS EQUALITY. MANY COURSES WRITE A ONE-SIDED H0 WITH = AT THE BOUNDARY.']
  return rows

def classify(reject,null_true):
  if null_true is None:return 'CANNOT DETERMINE'
  if reject and null_true:return 'TYPE I ERROR'
  if not reject and not null_true:return 'TYPE II ERROR'
  return 'CORRECT DECISION (NO ERROR)'

def outcome(m=None):
  key=c.menu('TEST DECISION',[('1','REJECT H0: EVIDENCE FOR H1'),('2','FAIL TO REJECT H0')])
  if key=='0':return
  reject=key=='1'
  key=c.menu('WHAT IS ACTUALLY TRUE?',[
    ('1','H0 IS TRUE'),('2','H0 IS FALSE / H1 TRUE'),('3','TRUTH IS NOT GIVEN')])
  if key=='0':return
  truth={'1':True,'2':False,'3':None}[key]
  answer=classify(reject,truth)
  rows=[answer,'DECISION: '+('REJECT H0' if reject else 'FAIL TO REJECT H0'),
        'REALITY: '+('NOT GIVEN' if truth is None else 'H0 TRUE' if truth else 'H0 FALSE')]
  if m:rows+=['H0: '+m['h0'],'H1: '+m['h1']]
  if truth is None:rows.append('THE ACTUAL TRUTH IS NEEDED TO IDENTIFY AN ERROR.')
  elif answer=='TYPE I ERROR':rows.append('A TRUE NULL WAS REJECTED.')
  elif answer=='TYPE II ERROR':rows.append('A FALSE NULL WAS NOT REJECTED.')
  else:rows.append('THE DECISION MATCHES REALITY.')
  rows.append('FAIL TO REJECT DOES NOT PROVE H0 TRUE.')
  c.view('TYPE I / II: ANSWER',rows)

def read_model(given_null):
  key=c.menu('POPULATION PARAMETER',[
    ('1','PROPORTION p'),('2','MEAN mu'),('3','DIFFERENCE p1-p2'),('4','DIFFERENCE mu1-mu2')])
  if key=='0':return
  parameter=('p','mu','p1-p2','mu1-mu2')[int(key)-1]
  context=input('CONTEXT / UNITS (ENTER=SKIP): ').strip()
  signs=('=','<=','>=') if given_null else ('<','>','!=','<=','>=','=')
  words={'<':'LESS THAN','>':'GREATER THAN','!=':'NOT EQUAL','<=':'AT MOST','>=':'AT LEAST','=':'EQUAL'}
  key=c.menu('GIVEN H0 SIGN' if given_null else 'CLAIM SIGN',
    [(str(i+1),sign+' '+words[sign]) for i,sign in enumerate(signs)],page_size=6)
  if key=='0':return
  relation=signs[int(key)-1]
  value=c.read_number('VALUE IN H0 / CLAIM: ')
  alt=None;side=None
  if given_null:
    if relation=='=':
      key=c.menu('GIVEN H1 SIGN',[('1','< LESS THAN'),('2','> GREATER THAN'),('3','!= NOT EQUAL')])
      if key=='0':return
      alt=('<','>','!=')[int(key)-1]
    key=c.menu('WHICH IS THE ORIGINAL CLAIM?',[('1','H0'),('2','H1'),('3','NOT SPECIFIED')])
    if key=='0':return
    side={'1':'H0','2':'H1','3':None}[key]
  return model(parameter,relation,value,context,given_null,alt,side)

def menu():
  while True:
    key=c.menu('TYPE I / TYPE II ERRORS',[
      ('1','FROM A CLAIM: BUILD H0/H1'),('2','FROM GIVEN H0 AND H1'),
      ('3','IDENTIFY DECISION + TRUTH'),('4','DEFINITIONS / alpha / beta')])
    if key=='0':return
    if key=='4':c.view('TYPE I / II DEFINITIONS',DEFINITIONS)
    elif key=='3':outcome()
    else:
      m=read_model(key=='2')
      if m is not None:
        c.view('TYPE I / II: YOUR QUESTION',describe(m))
        if c.menu('IDENTIFY AN OUTCOME',[('1','ENTER DECISION AND TRUTH')])=='1':outcome(m)
