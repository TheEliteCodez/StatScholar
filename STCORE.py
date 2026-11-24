try:
  from ti_system import get_key
  ON_TI=True
  HAS_KEYS=True
  KEY_STYLE='scan'
except ImportError:
  try:
    from ti_system import wait_key as ti_wait_key
    ON_TI=True
    KEY_STYLE='ce'
  except ImportError:
    ON_TI=False
    KEY_STYLE='text'
  HAS_KEYS=False
REVISION = '261124-R14'
_LAST_RAW = None
_menu_pages = {}
def read_raw_key():
  global _LAST_RAW
  if KEY_STYLE == 'ce':
    return ti_wait_key()
  while True:
    raw = get_key(0)
    if raw in (0, None, ''):
      _LAST_RAW = None
    elif raw != _LAST_RAW:
      _LAST_RAW = raw
      return raw
VIEW_LINES = 8
def cls():
  print("\n" * 18)
def heading(text):
  cls()
  print(('STAT1 '+REVISION) if text=='STAT1' else text[:30])
  print("-" * min(30,len(text)))
def _real(text):
  if text.endswith('%'): return _real(text[:-1])/100
  if '/' in text:
    a,b=text.split('/')
    return _real(a)/_real(b)
  return float(text)
def read_number(prompt):
  while True:
    try: return _real(input(prompt).strip())
    except (ValueError,ZeroDivisionError): print('USE NUMBER, A/B OR %')
def read_int(prompt):
  while True:
    try:
      return int(input(prompt))
    except ValueError:
      print("ENTER WHOLE NUMBER")
def yesno(prompt):
  while True:
    print()
    print(prompt)
    s = input("Y/N: ").strip().upper()
    if s == "Y" or s == "YES":
      return True
    if s == "N" or s == "NO":
      return False
    print("ENTER Y OR N")
def normalize_key(key):
  if isinstance(key, str):
    return key.strip().lower()
  if KEY_STYLE=='ce':
    codes=(3,4,2,14,1,15,5,13,9,10,11)
    names=('up','down','left','left','right','right','enter','enter','esc','delete','delete')
  else:
    codes=(25,34,24,26,105,45,23)
    names=('up','down','left','right','enter','esc','delete')
  return names[codes.index(key)] if key in codes else ''

def wait_key():
  if HAS_KEYS:
    while True:
      raw = read_raw_key()
      key = normalize_key(raw)
      if raw in ((148,248,175) if KEY_STYLE=='ce' else (84,)) or raw=='6': return '6'
      if key in ("up","down","left","right","enter","esc","u","d","b"):
        return key
  key = input("ENTER NEXT, - PREV, 0 BACK: ").strip().lower()
  return {"":"right","-":"left","0":"esc"}.get(key, normalize_key(key))
def read_choice():
  if not HAS_KEYS:
    key = input('> ').strip().upper()
    return {'':'N','-':'P'}.get(key, key)
  text = ''
  while True:
    raw = read_raw_key()
    key = normalize_key(raw)
    if key == 'left': return 'P'
    if key == 'right': return 'N'
    if key == 'esc': return '0'
    if key == 'delete':
      text = text[:-1]
      print('CHOICE: ' + text)
      continue
    if key == 'enter':
      return text or input('CHOICE / ID: ').strip().upper()
    char = ''
    if isinstance(raw, str) and len(raw) == 1:
      char = raw.upper()
    elif KEY_STYLE == 'ce':
      if 142 <= raw <= 151: char = str(raw-142)
      elif 243 <= raw <= 251: char = str(raw-242)
      elif raw == 62: char = '0'
      elif raw in (178,179,204,173,174,175,168,169,170,153):
        char = str((178,179,204,173,174,175,168,169,170,153).index(raw)+1)[-1]
      elif 154 <= raw <= 179: char = chr(65+raw-154)
    else:
      digits=(102,92,93,94,82,83,84,72,73,74)
      if raw in digits: char=str(digits.index(raw))
    if char:
      text += char
      print('> ' + text)
def wrapped_lines(lines):
  for line in lines:
    line = str(line)
    while len(line) > 30:
      cut = line.rfind(" ", 0, 31)
      if cut < 1: cut = 30
      yield line[:cut]
      line = line[cut:].lstrip()
    yield line

def summary(items):
  lines=[];row=''
  for item in items:
    if row and len(row)+len(item)+2>30:lines.append(row);row=''
    row=(row+'; ' if row else '')+item
  if row:lines.append(row)
  return lines
def view(title, lines, graph=None):
  graph=graph or getattr(lines,'graph',None)
  top=0
  while True:
    action=call('STVDISP','view',title,lines,bool(graph),top)
    if not isinstance(action,tuple): return action
    top=action[1]
    show_graph(graph)

def graph_lines(lines,graph):
  return call('STGATT','attach',lines,*graph) if graph else lines

def show_graph(graph):
  if graph:
    module,function,args=graph
    return call(module,function,*args)

def fmt(x):
  return call('STEFMT', 'fmt', x)
def gcd(a, b):
  return call('STEXACT', 'gcd', a, b)
def ratio(a, b=1):
  return call('STEXACT', 'ratio', a, b)
def as_ratio(text):
  return call('STEXACT', 'as_ratio', text)
def to_ratio(value):
  return call('STEXACT', 'to_ratio', value)
def compare_exact(a, b):
  return call('STEXACT', 'compare_exact', a, b)
def exact_sorted(values):
  return call('STEFMT', 'exact_sorted', values)
def exact_text(value):
  return call('STEFMT', 'exact_text', value)
def range_relation(count, mean, variance):
  return call('STEFMT', 'range_relation', count, mean, variance)
def radd(a, b):
  return call('STEFMT', 'radd', a, b)
def rmul(a, b):
  return call('STEFMT', 'rmul', a, b)
def rdiv(a, b):
  return call('STEXACT', 'rdiv', a, b)
def rsum(values):
  return call('STEFMT', 'rsum', values)
def number(value):
  return value[0]/value[1] if isinstance(value,tuple) else value
def read_exact(prompt):
  return call('STEXACT', 'read_exact', prompt)
def fixed(value, places):
  return call('STEFMT', 'fixed', value, places)
def answer_text(value, style="D", places=4):
  return call('STEFMT', 'answer_text', value, style, places)
def menu(title, items, shortcuts=(), other_shortcuts=(), page_size=5):
  return call('STVMENU', 'menu', title, items, shortcuts, other_shortcuts, page_size)
def results(title, answers, steps=None, default_places=4, drawing=(), graph=None):
  return call('STVRES','results',title,answers,steps,default_places,drawing,graph)
def event_match(x, op, a, b=0):
  return call('STEXACT', 'event_match', x, op, a, b)
def event_input(binomial=False):
  return call('STEVENT', 'event_input', binomial)
import sys
import gc
def topic_modules():
  return tuple(n for n in sys.modules if n.startswith('ST') and n not in ('STAT1','STCORE'))
_call_depth = 0
def release_topics(keep=()):
  for name in topic_modules():
    if name not in keep and name in sys.modules:
      del sys.modules[name]
  gc.collect()
def call(module_name, function_name, *args):
  global _call_depth
  module = sys.modules.get(module_name)
  if module is not None:
    return getattr(module, function_name)(*args)
  gc.collect()
  keep = topic_modules()
  _call_depth += 1
  try:
    module = __import__(module_name)
    return getattr(module, function_name)(*args)
  finally:
    _call_depth -= 1
    module = None
    release_topics(keep if _call_depth else ())
def task(module_name, function_name):
  return lambda *args: call(module_name, function_name, *args)
MAX_ROWS = 25
MAX_OUTCOMES = 60
def read_size(prompt, maximum, minimum=1):
  return call('STEVENT', 'read_size', prompt, maximum, minimum)
def paged_results(title, count, row_at, steps=None, drawing=(), graph=None):
  return call('STVRES','paged_results',title,count,row_at,steps,drawing,graph)
def choice_pages(title, pages):
  return call('STVCP','choice_pages',title,pages)

def ht_plot(setup,result,probability,critical,regions=('p',)):
  for region in regions:
    extent=call('STHTPLOT','curve',setup,result,probability,critical,region)
    if not extent:return False
    call('STHTLAB','labels',setup,result,probability,critical,region,extent)
    plot=call('STHTHEAD','heading',setup,result,probability,critical,region)
    action=call('STGKEY','wait',plot)
    plot=None
    if action=='back':return action
  return 'next'
