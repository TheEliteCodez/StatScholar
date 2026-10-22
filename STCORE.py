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
VIEW_LINES = 7
def cls():
    print("\n" * 18)
def heading(text):
    cls()
    print(text[:30])
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
    if KEY_STYLE == "ce":
        return {3:"up",4:"down",2:"left",14:"left",1:"right",15:"right",5:"enter",13:"enter",9:"esc",10:"delete",11:"delete"}.get(key, "")
    return {25:"up",34:"down",24:"left",26:"right",105:"enter",45:"esc",23:"delete"}.get(key, "")
def wait_key():
    if HAS_KEYS:
        while True:
            raw = read_raw_key()
            key = normalize_key(raw)
            if key in ("up","down","left","right","enter","esc","u","d","b"):
                return key
    key = input("ENTER NEXT, - PREV, 0 BACK: ").strip().lower()
    return {"":"right","-":"left","0":"esc"}.get(key, normalize_key(key))
def read_choice():
    return call('STVIN', 'read_choice')
def wrapped_lines(lines):
    for line in lines:
        line = str(line)
        while len(line) > 30:
            cut = line.rfind(" ", 0, 31)
            if cut < 1: cut = 30
            yield line[:cut]
            line = line[cut:].lstrip()
        yield line
def view(title, lines):
    return call('STVDISP','view',title,lines)
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
def results(title, answers, steps=None, default_places=4, drawing=()):
    return call('STVRES','results',title,answers,steps,default_places,drawing)
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
    return lambda: call(module_name, function_name)
def unpack_guide(text, field=None):
    return call('STEVENT', 'unpack_guide', text, field)
MAX_ROWS = 25
MAX_OUTCOMES = 60
def read_size(prompt, maximum, minimum=1):
    return call('STEVENT', 'read_size', prompt, maximum, minimum)
def paged_results(title, count, row_at, steps=None, drawing=()):
    return call('STVRES','paged_results',title,count,row_at,steps,drawing)
def choice_pages(title, pages):
    return call('STVCP','choice_pages',title,pages)
