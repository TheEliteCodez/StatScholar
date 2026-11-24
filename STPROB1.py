import STCORE as c
def solver_basic_prob():
  c.heading('P01 BASIC PROBABILITY')
  print('FAVORABLE = THE OUTCOMES THAT COUNT')
  print('TOTAL = ALL POSSIBLE OUTCOMES')
  a = c.read_int('FAVORABLE OUTCOMES: ')
  b = c.read_int('TOTAL OUTCOMES: ')
  c.results('P01 BASIC PROBABILITY', [('P', c.ratio(a, b))], ['P=FAVORABLE/TOTAL', str(a) + '/' + str(b)])
def solver_complement():
  p = c.read_exact('P(E): ')
  c.results('P02 COMPLEMENT', [('P(NOT E)', c.radd((1, 1), (-p[0], p[1])))], ['1-' + c.exact_text(p)])
def solver_general_or():
  a = c.read_exact('P(A): ')
  b = c.read_exact('P(B): ')
  both = c.read_exact('P(BOTH): ')
  c.results('P04 OR', [('P(OR)', c.radd(c.radd(a, b), (-both[0], both[1])))], [c.exact_text(a) + '+' + c.exact_text(b) + '-' + c.exact_text(both)])
def solver_mut_or():
  a = c.read_exact('P(A): ')
  b = c.read_exact('P(B): ')
  c.results('P03 EXCLUSIVE OR', [('P(OR)', c.radd(a, b))], ['MUTUALLY EXCLUSIVE: BOTH=0', c.exact_text(a) + '+' + c.exact_text(b)])
def solver_indep_and():
  a = c.read_exact('P(A): ')
  b = c.read_exact('P(B): ')
  c.results('P05 INDEPENDENT AND', [('P(BOTH)', c.rmul(a, b))], ['INDEPENDENT EVENTS', c.exact_text(a) + '*' + c.exact_text(b)])
def solver_general_and():
  a = c.read_exact('P(A): ')
  bg = c.read_exact('P(B GIVEN A): ')
  c.results('P06 GENERAL AND', [('P(BOTH)', c.rmul(a, bg))], ['P(A)*P(B GIVEN A)', c.exact_text(a) + '*' + c.exact_text(bg)])
def _subtract(a,b):
  return c.radd(a,(-b[0],b[1]))

def _given(both,group):
  return c.rdiv(both,group) if group[0] else 'UNDEFINED (GIVEN GROUP HAS P=0)'

def _prob(prompt):
  value=c.read_exact(prompt)
  if c.compare_exact(value,0)<0 or c.compare_exact(value,1)>0:
    raise ValueError('USE A PROBABILITY FROM 0 TO 1')
  return value

def _regions(a,b,both):
  parts=(both,_subtract(a,both),_subtract(b,both),
     _subtract(_subtract((1,1),a),_subtract(b,both)))
  if any(c.compare_exact(x,0)<0 for x in parts):
    raise ValueError('A, B AND THEIR OVERLAP ARE INCONSISTENT')
  return parts

def _area(parts,mask):
  value=(0,1)
  for i,p in enumerate(parts):
    if mask & (1<<i): value=c.radd(value,p)
  return value

def _event():
  key=c.menu('CHOOSE EVENT',[
    ('1','A'),('2','B'),('3','NOT A / A COMPLEMENT'),
    ('4','NOT B / B COMPLEMENT'),('5','A AND B / INTERSECTION'),
    ('6','A OR B / UNION'),('7','A AND NOT B / A ONLY'),
    ('8','NOT A AND B / B ONLY'),('9','NEITHER A NOR B'),
    ('10','EXACTLY ONE OF A, B')])
  if key=='0': return None
  return {'1':('A',3),'2':('B',5),'3':('NOT A',12),
    '4':('NOT B',10),'5':('A AND B',1),'6':('A OR B',7),
    '7':('A AND NOT B',2),'8':('NOT A AND B',4),
    '9':('NOT A AND NOT B',8),'10':('EXACTLY ONE',6)}[key]

def _report(a,b,both,work):
  parts=_regions(a,b,both)
  union=c.radd(c.radd(a,b),(-both[0],both[1]))
  while True:
    key=c.menu('A / B: FIND',[
      ('1','ALL PROBABILITIES / GIVEN'),('2','BUILD AN EVENT / GIVEN'),
      ('3','VENN REGIONS / TWO-WAY TABLE'),('4','INDEPENDENT / EXCLUSIVE')])
    if key=='0': return
    if key=='1':
      answers=[('P(A)',a),('P(B)',b),('P(A AND B)',both),
        ('P(A OR B)',union),('P(NOT A)',_subtract((1,1),a)),
        ('P(NOT B)',_subtract((1,1),b)),('P(A ONLY)',parts[1]),
        ('P(B ONLY)',parts[2]),('P(NEITHER)',parts[3]),
        ('P(EXACTLY ONE)',c.radd(parts[1],parts[2]))]
      for name,den,num in [('A|B',b,both),('B|A',a,both),
        ('NOT A|B',b,parts[2]),('NOT B|A',a,parts[1]),
        ('A|NOT B',_subtract((1,1),b),parts[1]),
        ('B|NOT A',_subtract((1,1),a),parts[2])]:
        answers.append(('P('+name+')',_given(num,den)))
      c.results('AND / OR / GIVEN',answers,work+[
        'AND=INTERSECTION; OR=UNION (INCLUDES BOTH)',
        'P(A OR B)=P(A)+P(B)-P(A AND B)',
        c.exact_text(a)+'+'+c.exact_text(b)+'-'+c.exact_text(both)+'='+c.exact_text(union),
        'P(A|B)=P(A AND B)/P(B)',
        c.exact_text(both)+'/'+c.exact_text(b)+'='+c.answer_text(_given(both,b),'F'),
        'P(B|A)=P(A AND B)/P(A)',
        'NOT E=1-P(E); NEITHER=1-P(A OR B)'],graph=('STGDIAG','venn',(1,c.number(a),c.number(b),c.number(both))))
    elif key=='2':
      target=_event()
      if target is None: continue
      how=c.menu('PROBABILITY TYPE',[('1','P(EVENT)'),('2','P(EVENT | GIVEN EVENT)')])
      if how=='0': continue
      numerator=_area(parts,target[1])
      label='P('+target[0]+')'
      formula=['ADD THE SELECTED VENN REGIONS.']
      answer=numerator
      if how=='2':
        group=_event()
        if group is None: continue
        numerator=_area(parts,target[1]&group[1])
        denominator=_area(parts,group[1])
        answer=_given(numerator,denominator)
        label='P(('+target[0]+')|('+group[0]+'))'
        formula=['P(E|G)=P(E AND G)/P(G)',
          'INTERSECTION WITH GIVEN GROUP='+c.exact_text(numerator),
          'GIVEN GROUP='+c.exact_text(denominator),
          c.exact_text(numerator)+'/'+c.exact_text(denominator),
          'RESTRICT TO GIVEN GROUP; DIVIDE BY ITS AREA.']
      c.results('EVENT ANSWER',[(label,answer)],work+formula,graph=('STGDIAG','venn',(1,c.number(a),c.number(b),c.number(both),None,target[1],group[1] if how=='2' else None)))
    elif key=='3':
      c.view('VENN / TWO-WAY PROBABILITIES',c.graph_lines(work+[
        'A ONLY='+c.exact_text(parts[1]),'BOTH='+c.exact_text(parts[0]),
        'B ONLY='+c.exact_text(parts[2]),'NEITHER='+c.exact_text(parts[3]),
        'TABLE COLUMNS: B, NOT B, TOTAL',
        'A: '+', '.join(c.exact_text(x) for x in (parts[0],parts[1],a)),
        'NOT A: '+', '.join(c.exact_text(x) for x in (parts[2],parts[3],_subtract((1,1),a))),
        'TOTAL: '+', '.join(c.exact_text(x) for x in (b,_subtract((1,1),b),(1,1)))]+
        ['DRAW TWO CIRCLES IN A RECTANGLE OF AREA 1.',
        'BOTH IN OVERLAP; NEITHER OUTSIDE CIRCLES.',
        'LABEL REMAINING REGIONS A ONLY AND B ONLY.'],('STGDIAG','venn',(1,c.number(a),c.number(b),c.number(both)))))
    else:
      product=c.rmul(a,b)
      c.results('EVENT RELATIONSHIPS',[
        ('INDEPENDENT','YES' if c.compare_exact(both,product)==0 else 'NO'),
        ('MUTUALLY EXCLUSIVE','YES' if not both[0] else 'NO')],work+[
        'INDEPENDENT: P(A AND B)=P(A)*P(B)',
        c.exact_text(both)+' COMPARED WITH '+c.exact_text(product),
        'MUTUALLY EXCLUSIVE: P(A AND B)=0'])

def solver_conditional():
  while True:
    key=c.menu('GIVEN / AND / OR / NOT',[
      ('1','FIND A GIVEN B / B GIVEN A'),
      ('2','FIND AND FROM A GIVEN PROBABILITY'),
      ('3','GIVEN P(A), P(B), P(AND)'),
      ('4','GIVEN P(A), P(B), P(OR)'),
      ('5','GIVEN P(A), P(B), P(A|B)'),
      ('6','GIVEN P(A), P(B), P(B|A)'),
      ('7','TOTAL / A / B / BOTH COUNTS'),
      ('8','ENTER A TWO-WAY COUNT TABLE'),
      ('9','SYMBOLS / WORDING GUIDE'),
      ('10','EVENTS EXPLICITLY INDEPENDENT'),
      ('11','EVENTS MUTUALLY EXCLUSIVE')])
    if key=='0': return
    if key=='9':
      c.view('PROBABILITY SYMBOLS',[
        'A|B: A GIVEN B; B IS THE GIVEN GROUP.',
        'A cap B: INTERSECTION = A AND B = BOTH.',
        'A cup B: UNION = A OR B, INCLUDING BOTH.',
        "A PRIME / A^c: COMPLEMENT = NOT A.",
        '(A cup B)^c: NEITHER A NOR B.',
        'A cap B^c: A ONLY / A BUT NOT B.',
        'P(A|B)=P(A cap B)/P(B).',
        'P(A cup B)=P(A)+P(B)-P(A cap B).',
        'CHOOSE WORDS IN MENUS; NO SYMBOL TYPING.'])
      continue
    if key=='8':
      c.call('STPROB','two_way_session');continue
    if key in ('1','2'):
      direction=c.menu('CONDITIONAL DIRECTION',[('1','A GIVEN B: P(A|B)'),('2','B GIVEN A: P(B|A)')])
      if direction=='0': continue
      target,group=('A','B') if direction=='1' else ('B','A')
      counts=False
      if key=='1':
        mode=c.menu('GIVEN VALUES',[('1','PROBABILITIES'),('2','BOTH / GIVEN GROUP COUNTS')])
        if mode=='0': continue
        counts=mode=='2'
      den=(c.read_int('COUNT IN GIVEN GROUP '+group+': '),1) if counts else _prob('P('+group+') GIVEN GROUP: ')
      if key=='1':
        both=(c.read_int('COUNT IN BOTH A AND B: '),1) if counts else _prob('P(A AND B) / INTERSECTION: ')
        if den[0]<0 or both[0]<0: raise ValueError('COUNTS MUST BE NONNEGATIVE')
        if c.compare_exact(both,den)>0: raise ValueError('OVERLAP EXCEEDS GIVEN GROUP')
        answer=_given(both,den)
        label='P('+target+'|'+group+')'
        formula=label+('=n(A AND B)/n('+group+')' if counts else '=P(A AND B)/P('+group+')')
        numbers=c.exact_text(both)+'/'+c.exact_text(den)
      else:
        conditional=_prob('P('+target+'|'+group+'): ')
        answer=c.rmul(conditional,den)
        label='P(A AND B)'
        formula=label+'=P('+target+'|'+group+')*P('+group+')'
        numbers=c.exact_text(conditional)+'*'+c.exact_text(den)
        if not den[0]:
          answer='UNDEFINED (GIVEN GROUP HAS P=0)'
      c.results('CONDITIONAL / INTERSECTION',[(label,answer)],
        [formula,numbers,'| MEANS GIVEN; AND MEANS INTERSECTION.',
        'GIVEN GROUP IS '+group],drawing=[formula,numbers,'GIVEN GROUP IS '+group])
      continue
    if key=='7':
      total=c.read_int('TOTAL PEOPLE / ITEMS: ')
      ac=c.read_int('COUNT A INCLUDING BOTH: ')
      bc=c.read_int('COUNT B INCLUDING BOTH: ')
      overlap=c.read_int('COUNT BOTH / INTERSECTION: ')
      c.call('STVENN','regions',total,ac,bc,overlap)
      a,b,both=[c.ratio(x,total) for x in (ac,bc,overlap)]
      work=['TOTAL='+str(total)+' A='+str(ac)+' B='+str(bc)+' BOTH='+str(overlap)]
    else:
      a=_prob('P(A): ');b=_prob('P(B): ')
      work=['P(A)='+c.exact_text(a)+'; P(B)='+c.exact_text(b)]
      if key=='3': both=_prob('P(A AND B) / INTERSECTION: ')
      elif key=='4':
        union=_prob('P(A OR B) / UNION: ')
        both=_subtract(c.radd(a,b),union)
        work+=['P(AND)=P(A)+P(B)-P(OR)',c.exact_text(a)+'+'+c.exact_text(b)+'-'+c.exact_text(union)]
      elif key in ('5','6'):
        group=b if key=='5' else a
        conditional=_prob('P('+('A|B' if key=='5' else 'B|A')+'): ')
        if not group[0]: raise ValueError('GIVEN CONDITIONAL REQUIRES NONZERO GIVEN GROUP')
        both=c.rmul(conditional,group)
        work+=['P(AND)=CONDITIONAL*GIVEN GROUP',c.exact_text(conditional)+'*'+c.exact_text(group)]
      else:
        both=c.rmul(a,b) if key=='10' else (0,1)
        work+=['GIVEN INDEPENDENT: P(AND)=P(A)*P(B)' if key=='10' else 'GIVEN MUTUALLY EXCLUSIVE: P(AND)=0']
      work+=['P(A AND B)='+c.exact_text(both)]
    _report(a,b,both,work)

def solver_at_least_one():
  p = c.read_exact('SUCCESS p: ')
  n = c.read_int('TRIALS n: ')
  ans = c.ratio(p[1] ** n - (p[1] - p[0]) ** n, p[1] ** n)
  c.results('P09 AT LEAST ONE', [('P', ans)], ['1-(1-' + c.exact_text(p) + ')^' + str(n)])
