# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

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

_LAST_RAW = None
_menu_pages = {}


def read_raw_key():
    return call('STVIN', 'read_raw_key')


VIEW_LINES = 7


def cls():
    # clear the visible shell by pushing prior output upward
    print("\n" * 18)


def heading(text):
    # print a compact menu heading
    cls()
    print(text[:30])
    print("-" * min(30,len(text)))


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
    return call('STVIN', 'normalize_key', key)


def wait_key():
    return call('STVIN', 'wait_key')


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
    return call('STEFMT', 'number', value)


def read_exact(prompt):
    return call('STEXACT', 'read_exact', prompt)


def fixed(value, places):
    return call('STEFMT', 'fixed', value, places)


def answer_text(value, style="D", places=4):
    return call('STEFMT', 'answer_text', value, style, places)


def menu(title, items, shortcuts=(), other_shortcuts=(), page_size=5):
    return call('STVMENU', 'menu', title, items, shortcuts, other_shortcuts, page_size)


def results(title, answers, steps=None, default_places=4):
    return call('STVRES','results',title,answers,steps,default_places)


def event_match(x, op, a, b=0):
    return call('STEXACT', 'event_match', x, op, a, b)


def event_input(binomial=False):
    return call('STEVENT', 'event_input', binomial)


# A topic and its dependencies live only for the active task.
import sys
import gc
TOPIC_MODULES = ('STDEFS','STBINFO','STBINFO2','STBINFO4','STBINFO5','STBINFO6','STBINFO7','STBINFO9','STPROB1','STPROB2','STPROB3','STPROB4','STCOUNT1','STCOUNT2','STCOUNT3','STCOUNT4','STCOUNT5','STCOUNT6','STCOUNT7','STNORM1','STNORM2','STNORM3','STNORM4','STNORM5','STNORM6','STDMATH1','STDMATH2','STDMATH3','STVENN1','STVENN2','STDATA1','STDATA2','STDATA3','STSAMPLE','STSAMPLE1','STSAMPLE2','STPRE','STPRE1','STPRE2','STPRE3','STFINITE','STZLIST','STVIN','STVMENU','STVCP','STVDISP','STVRES','STNAV','STNAV1','STNAV2','STINDEX','STPAGE','STEXPER','STEXPER1','STEXPER2','STEXPER3','STMDICE','STMDICE1','STMDICE2','STQUIZ5','STVENN','STQUIZ4','STQUIZ3','STQUIZ','STDESC','STDESC1','STDESC2','STPROB','STDICE','STDICE1','STDICE2','STBINOM','STBINOM1','STBINOM2','STCOUNT',
                 'STGDESC','STGDESC1','STGDESC2','STGDESC3','STGDESC4','STGDESC5','STGDESC6','STGDESC7','STGDESC8','STGDESC9','STGPROB','STGPROB1','STGPROB2','STGPROB3','STGPROB4','STGPROB5','STGDICE','STGBIN','STGBIN1','STGBIN2','STGBIN3','STGBIN4','STGBIN5','STGCNT','STGCNT1','STGCNT2','STGCNT3','STGCNT4','STREF','STREF1','STREF2','STDMATH','STDATA','STGRAPH',
                 'STNORM','STHIST','STHIST1','STHIST2','STSTUDY','STSTU1','STSTU2','STFIND','STFIND1','STFIND2','STQUEST','STGNEW','STGNEW1','STGNEW2','STGNEW3','STGNEW4','STGNEW5','STGNEW6','STCOMB','STBMATH','STBEXTRA','STBWORD','STBW2','STBWE','STEFMT','STBHELP','STWORDS','STPWORD','STPTIDX','STPT1','STPT2','STPT3','STPT4','STQ1','STQ2','STQ3','STQ4','STQ5','STHOME','STEXACT','STEVENT','STTASKS','STPROBM','STWIZM')
_call_depth = 0

def release_topics(keep=()):
    for name in TOPIC_MODULES:
        if name not in keep and name in sys.modules:
            del sys.modules[name]
    gc.collect()

def call(module_name, function_name, *args):
    global _call_depth
    module = sys.modules.get(module_name)
    if module is not None:
        return getattr(module, function_name)(*args)
    gc.collect()
    # Keep active callers and their dependencies, release completed nested work.
    keep = tuple(name for name in TOPIC_MODULES if name in sys.modules)
    _call_depth += 1
    try:
        module = __import__(module_name)
        return getattr(module, function_name)(*args)
    finally:
        _call_depth -= 1
        release_topics(keep if _call_depth else ())

def task(module_name, function_name):
    return lambda: call(module_name, function_name)


def unpack_guide(text, field=None):
    return call('STEVENT', 'unpack_guide', text, field)


MAX_ROWS = 25
MAX_OUTCOMES = 60

def read_size(prompt, maximum, minimum=1):
    return call('STEVENT', 'read_size', prompt, maximum, minimum)


def paged_results(title, count, row_at, steps=None):
    return call('STVRES','paged_results',title,count,row_at,steps)


def choice_pages(title, pages):
    return call('STVCP','choice_pages',title,pages)
