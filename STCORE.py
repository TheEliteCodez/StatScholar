# Author: TheEliteCodez
# STCORE.py - shared input, display and exact arithmetic
# Shared by STAT1 and the on-demand topic/reference modules.


# Prefer the physical-key reader. wait_key availability does not identify a CE.
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
    # Keep the confirmed native-input workaround on wait_key-only devices.
    HAS_KEYS=False

_LAST_RAW=None


def read_raw_key():
    global _LAST_RAW
    if KEY_STYLE=='ce': return ti_wait_key()
    # Poll the physical keys; do not infer CE codes from wait_key's presence.
    # One event per press, including when a key remains held across screens.
    while True:
        raw=get_key(0)
        if raw in (0,None,''):
            _LAST_RAW=None
        elif raw!=_LAST_RAW:
            _LAST_RAW=raw
            return raw


VIEW_LINES = 7


def cls():
    # clear the visible shell by pushing prior output upward
    print("\n" * 18)


def heading(text):
    # print a compact menu heading
    cls()
    print(text[:30])
    print("-" * min(30,len(text)))


def fmt(x):
    # format numerical answers compactly
    try:
        if abs(x - int(x)) < 0.0000000001:
            return str(int(x))
    except:
        pass
    return str(round(x, 10))


def gcd(a, b):
    # calculate greatest common divisor
    a = abs(int(a))
    b = abs(int(b))
    while b != 0:
        a, b = b, a % b
    return a




def read_int(prompt):
    # read a whole number
    while True:
        try:
            return int(input(prompt))
        except:
            print("ENTER WHOLE NUMBER")




def yesno(prompt):
    # ask a yes or no classifier question
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
    # TI get_key scan codes and CE wait_key codes use different layouts.
    # String-valued readers and desktop U/D/B input remain supported.
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
    key=input("ENTER NEXT, - PREV, 0 BACK: ").strip().lower()
    return {"":"right","-":"left","0":"esc"}.get(key,normalize_key(key))


def read_choice():
    if not HAS_KEYS:
        key=input('> ').strip().upper()
        return {'':'N','-':'P'}.get(key,key)
    text=''
    while True:
        raw=read_raw_key()
        key=normalize_key(raw)
        if key=='left': return 'P'
        if key=='right': return 'N'
        if key=='esc': return '0'
        if key=='delete':
            text=text[:-1]
            print('CHOICE: '+text)
            continue
        if key=='enter':
            return text or input('CHOICE / ID: ').strip().upper()
        char=''
        if isinstance(raw,str) and len(raw)==1: char=raw.upper()
        elif KEY_STYLE=='ce':
            if 142<=raw<=151: char=str(raw-142)
            elif 243<=raw<=251: char=str(raw-242)
            elif raw==62: char='0'
            # Menu digits mean physical number keys even in ALPHA lock.
            # Letter IDs remain available via empty ENTER -> text entry.
            elif raw in (178,179,204,173,174,175,168,169,170,153):
                char=str((178,179,204,173,174,175,168,169,170,153).index(raw)+1)[-1]
            elif 154<=raw<=179: char=chr(65+raw-154)
        else:
            char={102:'0',92:'1',93:'2',94:'3',82:'4',83:'5',84:'6',72:'7',73:'8',74:'9'}.get(raw,'')
        if char:
            text+=char
            print('> '+text)


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
    return call('STVIEW','view',title,lines)




def ratio(a, b=1):
    if b == 0:
        raise ValueError("ZERO DENOMINATOR")
    a, b = int(a), int(b)
    g = gcd(a, b)
    if b < 0:
        g = -g
    return (a//g, b//g)


def as_ratio(text):
    text = str(text).strip()
    if text.endswith("%"):
        a = as_ratio(text[:-1])
        return ratio(a[0], a[1]*100)
    if "/" in text:
        a, b = text.split("/")
        return rdiv(as_ratio(a), as_ratio(b))
    if "e" in text.lower():
        a, e = text.lower().split("e")
        a = as_ratio(a)
        e = int(e)
        if e >= 0:
            return ratio(a[0]*10**e, a[1])
        return ratio(a[0], a[1]*10**(-e))
    sign = -1 if text.startswith("-") else 1
    text = text.lstrip("+-")
    if "." in text:
        whole, part = text.split(".")
        return ratio(sign*int((whole or "0")+part), 10**len(part))
    return ratio(sign*int(text))


def to_ratio(value):
    if isinstance(value,tuple): return value
    return as_ratio(str(value))


def compare_exact(a,b):
    a=to_ratio(a);b=to_ratio(b)
    delta=a[0]*b[1]-b[0]*a[1]
    return (delta>0)-(delta<0)


def exact_sorted(values):
    # Small input tables; insertion ordering avoids converting keys to floats.
    ordered=[]
    for value in values:
        i=len(ordered)
        while i>0 and compare_exact(value,ordered[i-1])<0: i-=1
        ordered.insert(i,value)
    return ordered


def exact_text(value):
    a,b=to_ratio(value)
    if b==1: return str(a)
    tail=b;twos=0;fives=0
    while tail%2==0: tail//=2;twos+=1
    while tail%5==0: tail//=5;fives+=1
    if tail==1: return fixed((a,b),max(twos,fives))
    return str(a)+"/"+str(b)


def range_relation(count,mean,variance):
    # Returns -1 below, 0 inside/on the boundary, +1 above mu +/- 2 SD.
    delta=radd(to_ratio(count),(-mean[0],mean[1]))
    if compare_exact(rmul(delta,delta),rmul((4,1),variance))<=0: return 0
    return -1 if delta[0]<0 else 1


def radd(a, b):
    return ratio(a[0]*b[1]+b[0]*a[1], a[1]*b[1])


def rmul(a, b):
    return ratio(a[0]*b[0], a[1]*b[1])


def rdiv(a, b):
    return ratio(a[0]*b[1], a[1]*b[0])


def rsum(values):
    total = (0, 1)
    for value in values:
        total = radd(total, value)
    return total


def number(value):
    if isinstance(value, tuple):
        return value[0]/value[1]
    return value


def read_exact(prompt):
    while True:
        try:
            return as_ratio(input(prompt))
        except (ValueError, ZeroDivisionError):
            print("USE NUMBER, A/B OR %")


def fixed(value, places):
    # Round exact ratios without passing through a decimal approximation.
    if isinstance(value, tuple):
        a, b = value
        scaled, rem = divmod(abs(a)*10**places, b)
        if rem*2 >= b:
            scaled += 1
        sign = "-" if a < 0 and scaled else ""
        digits = str(scaled)
        while len(digits) <= places:
            digits = "0"+digits
        if places:
            return sign+digits[:-places]+"."+digits[-places:]
        return sign+digits
    return ("%.*f" % (places, value))


def answer_text(value, style="D", places=4):
    if isinstance(value, str):
        return value
    if style == "F":
        if isinstance(value, tuple):
            return str(value[0])+"/"+str(value[1])
        return fmt(value)+" (APPROX)"
    if style == "P":
        value = rmul(value, (100,1)) if isinstance(value, tuple) else value*100
        return fixed(value, places)+"%"
    return fixed(value, places)


def menu(title, items, shortcuts=(), other_shortcuts=(), page_size=5):
    return call('STVIEW','menu',title,items,shortcuts,other_shortcuts,page_size)


def results(title, answers, steps=None, default_places=4):
    return call('STVIEW','results',title,answers,steps,default_places)


def event_match(x, op, a, b=0):
    left=compare_exact(x,a)
    if op == "=": return left == 0
    if op == "<": return left < 0
    if op == "<=": return left <= 0
    if op == ">": return left > 0
    if op == ">=": return left >= 0
    if op == "!=": return left != 0
    right=compare_exact(x,b)
    if op == "[]": return left >= 0 and right <= 0
    if op == "()": return left > 0 and right < 0
    if op == "[)": return left >= 0 and right < 0
    return left > 0 and right <= 0


def event_input(binomial=False):
    key=menu("BINOMIAL > EVENT" if binomial else "WHAT DOES IT ASK?",[("1","EXACTLY ="),("2","AT MOST <="),
          ("3","LESS THAN <"),("4","AT LEAST >="),("5","MORE THAN >"),
          ("6","BETWEEN x AND y")]+([("7","AT LEAST ONE"),("8","NOT =")] if binomial else [("7","NOT =")]), page_size=6)
    if key=="0": return None
    if binomial and key=="7": return ">=",(1,1),0
    if key=="8": key="7"
    op={"1":"=","2":"<=","3":"<","4":">=","5":">","7":"!="}.get(key,"[]")
    a=read_exact("VALUE / LOWER: ")
    b=0
    if key=="6":
        b=read_exact("UPPER: ")
        c=menu("INCLUDE ENDPOINTS?",[("1","BOTH [a,b]"),("2","NEITHER (a,b)"),
               ("3","LOWER ONLY [a,b)"),("4","UPPER ONLY (a,b]")])
        op={"1":"[]","2":"()","3":"[)","4":"(]"}.get(c,"[]")
    return op,a,b


# A topic and its dependencies live only for the active task.
import sys
import gc
TOPIC_MODULES = ('STBINFO','STSAMPLE','STPRE','STPRE1','STPRE2','STPRE3','STFINITE','STZLIST','STVIEW','STNAV','STINDEX','STPAGE','STEXPER','STMDICE','STQUIZ5','STVENN','STQUIZ4','STQUIZ3','STQUIZ','STDESC','STPROB','STDICE','STBINOM','STCOUNT',
                 'STGDESC','STGPROB','STGDICE','STGBIN','STGCNT','STREF','STDMATH','STDATA','STGRAPH',
                 'STNORM','STHIST','STSTUDY','STFIND','STQUEST','STGNEW','STCOMB','STBMATH','STBEXTRA','STBWORD','STBHELP','STWORDS','STPWORD','STPTIDX','STPT1','STPT2','STPT3','STPT4','STQ1','STQ2','STQ3','STQ4','STQ5')
_call_depth = 0

def release_topics(keep=()):
    for name in TOPIC_MODULES:
        if name not in keep and name in sys.modules:
            del sys.modules[name]
    gc.collect()

def call(module_name, function_name, *args):
    global _call_depth
    gc.collect()
    # Keep active callers and their dependencies, release completed nested work.
    keep = tuple(name for name in TOPIC_MODULES if name in sys.modules)
    _call_depth += 1
    module = None
    try:
        module = __import__(module_name)
        return getattr(module, function_name)(*args)
    finally:
        module = None
        _call_depth -= 1
        release_topics(keep if _call_depth else ())

def task(module_name, function_name):
    return lambda: call(module_name, function_name)


def unpack_guide(text, field=None):
    # Decode one requested section without constructing the other sections.
    names = ("title","recognize","values","byhand","ti84",
             "example","mistakes","related","solver")
    if field is not None:
        index = names.index(field)
        start = 0
        for i in range(index):
            start = text.find("\n", start) + 1
        end = text.find("\n", start)
        section = text[start:] if end < 0 else text[start:end]
        return section if index in (0,8) else section.split("\t")
    fields = text.split("\n")
    result = {}
    for i in range(9):
        result[names[i]] = fields[i] if i in (0,8) else fields[i].split("\t")
    return result


MAX_ROWS = 25
MAX_OUTCOMES = 60

def read_size(prompt, maximum, minimum=1):
    while True:
        n = read_int(prompt)
        if minimum <= n <= maximum:
            return n
        print("ENTER " + str(minimum) + ".." + str(maximum))


def paged_results(title, count, row_at, steps=None):
    return call('STVIEW','paged_results',title,count,row_at,steps)


def choice_pages(title, pages):
    return call('STVIEW','choice_pages',title,pages)
