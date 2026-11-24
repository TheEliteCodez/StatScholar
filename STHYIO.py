import STCORE as c

def check(title):
  key=c.menu(title,[('1','YES / GIVEN'),('2','NO'),('3','NOT GIVEN / UNSURE')])
  return {'1':'PASS','2':'FAIL','3':'VERIFY'}.get(key)

def setup(parameter,null=None):
  context=input('POPULATION / MEASURE / UNIT LABEL (ENTER=SKIP): ').strip()
  random=check('SRS / RANDOM INDEPENDENT SAMPLE(S)?')
  if random is None: return
  key=c.menu('CLAIM ABOUT '+parameter,[('1','< LESS THAN'),('2','> GREATER THAN'),('3','!= NOT EQUAL TO'),
       ('4','<= LESS THAN OR EQUAL TO'),('5','>= GREATER THAN OR EQUAL TO'),('6','= EQUAL TO')],page_size=6)
  if key=='0': return
  claim=('<','>','!=','<=','>=','=')[int(key)-1]
  alternative={'<':'<','>':'>','!=':'!=','<=':'>','>=':'<','=':'!='}[claim]
  if null is None: null=c.read_number('VALUE IN H0: ')
  alpha=c.read_number('SIGNIFICANCE alpha (5% OR .05): ')
  if not 0<alpha<1: raise ValueError('USE 0 < alpha < 1')
  return {'parameter':parameter,'context':context,'random':random,'claim':claim,
      'alternative':alternative,'null':null,'alpha':alpha}

def population(n,label):
  raw=input(label+' POPULATION N (ENTER=SKIP): ').strip()
  if not raw: return label+' 5% CHECK: VERIFY N >= 20*n'
  total=int(raw)
  if total<n or total<1: raise ValueError('POPULATION N MUST BE >= SAMPLE n')
  return label+' 20*n <= N: '+('PASS' if 20*n<=total else 'FAIL')

def mean_data(label):
  key=c.menu(label+' MEAN INPUT',[('1','SUMMARY: x-bar, s, n'),('2','RAW MEASUREMENTS')])
  if key=='0': return
  if key=='2':
    return c.call('STMEAN','read_raw',label+' MEASUREMENTS')
  return (c.read_number(label+' SAMPLE AVERAGE x-bar: '),
      c.read_number(label+' SAMPLE STANDARD DEVIATION s: '),
      c.read_int(label+' SAMPLE SIZE n: '))
