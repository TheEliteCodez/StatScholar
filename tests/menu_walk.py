"""Desktop menu exploration. Run separately so real module cleanup stays enabled.

This exercises calculations and real renderers, not a TI heap emulator.
"""
import builtins
import contextlib
import hashlib
import json
from pathlib import Path
import sys
import traceback
import weakref

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import STAT1
import STCORE as c


class Sink:
    def write(self, value):
        return len(value)

    def flush(self):
        pass


class Walker:
    def __init__(self):
        self.menu_impl = c.menu
        self.pages_impl = c.choice_pages
        self.view_impl = c.view
        self.menus = {}
        self.queue = [[]]
        self.scheduled = set()
        self.failures = []
        self.runs = []
        self.sizes = {p.stem:p.stat().st_size for p in ROOT.glob('ST*.py')}
        self.passed=set()
        self.replacement='Y'
        self.search='sample'
        self.large=False
        self.small_clt=False

    def profile(self, frame, event, arg):
        if event != 'call' or frame.f_globals.get('__name__') not in self.sizes:
            return
        # Observe helper imports, not every scalar operation while paging work.
        if (frame.f_globals.get('__name__') in ('STWORK','STDWK','STEFMT','STEXACT')
                and frame.f_code.co_name!='<module>'):
            return
        names = tuple(n for n in sys.modules if n in self.sizes)
        for name in names:
            if name not in ('STCORE','STAT1'):
                module=sys.modules[name]
                self.references[id(module)]=weakref.ref(module)
        size = sum(self.sizes[n] for n in names)
        if size > self.peak_bytes:
            self.peak_bytes, self.peak_modules = size, names

    def choose(self, title, items):
        frame = sys._getframe(2)
        # Scoped walkers may wrap choose(); locate the actual calculator caller.
        while frame.f_globals.get('__name__') not in self.sizes:
            frame=frame.f_back
        site = Path(frame.f_code.co_filename).name+':'+frame.f_code.co_name
        identity = site+' | '+title
        if title=='SEARCH RESULTS': identity+=' | '+', '.join(label for key,label in items)
        entry = self.menus.setdefault(identity, {'options':{}, 'passed':[], 'site':site})
        for key, label in items:
            entry['options'][key] = label
        if self.position == len(self.path):
            if self.path:
                self.passed.add(self.last_edge)
            for key, label in items+[('0','BACK / EXIT')]:
                edge = (identity,key)
                if edge not in self.scheduled:
                    self.queue.append(self.path+[key])
                    self.scheduled.add(edge)
            # Shared formatting/confirmation menus must not hide the caller's
            # next menu. Return normally through the program so cleanup is
            # measured without exception traceback frames retaining modules.
            default='1' if title in ('RANDOM / INDEPENDENT SAMPLE',
                                    'POPULATION APPROXIMATELY NORMAL?') else '0'
            if (title.startswith('CLAIM ABOUT ') or title.endswith(' MEAN INPUT')
                    or title in ('SRS / RANDOM INDEPENDENT SAMPLE(S)?',
                                 'TWO GROUPS INDEPENDENT?', 'INDEPENDENT GROUPS (NOT PAIRED)?')
                    or 'NORMAL, NO STRONG SKEW / OUTLIERS?' in title):
                default='1'
            if title=='TABLE PAGE / FORMAT' and frame.f_locals['end']<frame.f_locals['count']:
                default='N'
            self.path.append(default)
        key = self.path[self.position]
        self.position += 1
        if key not in dict(items) and key != '0':
            raise AssertionError(('Replay menu changed', identity, key, items))
        self.last_edge = (identity,key)
        return key

    def menu(self, title, items, shortcuts=(), other_shortcuts=(), page_size=5):
        items = list(items)
        for key in shortcuts if len(shortcuts)<=3 else ():
            if key in ('C','S') and key not in dict(items):
                items.append((key,'CHANGE DATA' if key=='C' else 'SELECT MANY'))
        key = self.choose(title,items)
        # Use the production renderer and validation after choosing an edge.
        saved = c.read_choice
        c.read_choice = lambda:key
        try:
            return self.menu_impl(title,items,shortcuts,other_shortcuts,page_size)
        finally:
            c.read_choice = saved

    def pages(self, title, pages):
        items=[(token,'PAGE '+str(p+1)+' / '+str(i+1)+' '+label)
               for p,page in enumerate(pages) for i,(label,token) in enumerate(page)]
        key=self.choose(title,items)
        saved=c.read_choice
        if key=='0':
            keys=iter(['0'])
        else:
            page,index=next((p,i) for p,values in enumerate(pages)
                            for i,(label,token) in enumerate(values) if token==key)
            c._menu_pages.pop(title,None)
            keys=iter(['N']*page+[str(index+1)])
        c.read_choice=lambda:next(keys)
        try:
            return self.pages_impl(title,pages)
        finally:
            c.read_choice=saved

    def read(self, prompt=''):
        self.reads += 1
        if self.reads > 600:
            raise AssertionError(('Input did not progress',prompt))
        p=prompt.upper()
        if 'PARAMETERS ESTIMATED' in p: return '0'
        if 'NUMBER OF PAIRS' in p: return '100' if self.large else '5'
        if p.startswith('X LIST NUMBER'): return '1'
        if p.startswith('Y LIST NUMBER'): return '2'
        if p.startswith('OBSERVED COUNT '): return '20'
        if p.startswith('EXPECTED COUNT '): return '20'
        if p.startswith('PROBABILITY ') and p.endswith(': '): return '1/60' if self.large else '.5'
        if p.startswith('X') and p[1:-2].isdigit(): return p[1:-2]
        if p.startswith('Y') and p[1:-2].isdigit(): return str(2*int(p[1:-2])+int(p[1:-2])%2)
        if p == '> ': return 'N'  # Definition pages: visit every page.
        if 'ENTER=' in p or 'ENTER IF' in p: return ''
        if p=='Y/N: ': return self.replacement
        if self.small_clt and p=='SAMPLE SIZE N: ': return '2'
        if p in ('RIGHT-TAIL AREA: ','LEFT-TAIL AREA: ','AREA FROM 0 TO CUTOFF: '): return '.25'
        if 'COUNT IN GIVEN GROUP' in p: return '50'
        if p=='VALUE IN H0: ': return '.4'
        if 'SUCCESSES X' in p: return '40'
        if 'CONFIDENCE' in p: return '95%'
        if 'SEARCH TERM' in p: return self.search
        if 'EVENT (BACK' in p: return 'EVEN'
        if 'NAME' in p or 'PERSPECTIVE' in p or 'VARIABLE / UNITS' in p: return 'GROUP'
        if 'POPULATION N' in p or 'TOTAL OBJECTS' in p or 'POPULATION TOTAL' in p or 'TOTAL IN BOX' in p: return '100'
        if 'TARGET OBJECTS' in p or 'DEFECTIVE' in p or 'TARGET COUNT' in p or 'TARGET GROUP' in p: return '40'
        if 'TOTAL PEOPLE' in p or 'TOTAL TICKETS' in p or p=='TOTAL: ': return '100'
        if 'COUNT A' in p or 'COUNT B' in p or 'INCLUDING BOTH' in p: return '50'
        if 'BOTH' in p: return '20' if 'COUNT' in p or p=='BOTH: ' else '.2'
        if 'NUMBER WITH EVENT' in p: return '20'
        if 'TOTAL NUMBER SAMPLED' in p or 'TOTAL SAMPLED' in p or 'SAMPLE SIZE' in p: return '100'
        if 'MARGIN' in p or 'ALPHA' in p or 'CUTOFF (ENTER' in p: return '.05'
        if 'HOW MANY KNOWN' in p: return '2'
        if 'P(X)' in p: return '1/25' if self.large else '.5'
        if 'KNOWN P' in p: return '.5'
        if 'AREA TO LEFT' in p: return '.7'
        if 'POINT ESTIMATE' in p: return '.5'
        if 'CHANCE' in p or 'PROBABILITY' in p or 'PROPORTION' in p or 'PERCENT' in p or p.startswith('P(') or p=='SUCCESS P: ' or p=='P-VALUE: ': return '.25'
        if 'ROW COUNT' in p or 'COLUMN COUNT' in p: return '10' if self.large else '2'
        if 'NUMBER OF ROWS' in p or 'NUMBER OF OUTCOMES' in p: return '25' if self.large else '2'
        if 'NUMBER OF CATEGORIES' in p: return '60' if self.large else '2'
        if 'NUMBER OF VALUES' in p: return '100' if self.large else '5'
        if 'FIRST LOWER' in p: return '0'
        if 'CLASS WIDTH' in p: return '2'
        if 'MEASURE UNIT' in p: return '1'
        if 'NUMBER OF CLASSES' in p: return '3'
        if 'LOWER Z' in p: return '-1'
        if 'UPPER Z' in p: return '2'
        if 'LOWER' in p or p=='MIN: ' or p=='Q1: ': return '1'
        if 'UPPER' in p or p=='MAX: ' or p=='Q3: ': return '5'
        if 'SUM:' in p: return '7'
        if 'DEGREES' in p: return '9'
        if 'TRIAL' in p: return '20' if self.large else '5'
        if 'NUMBER SELECTED' in p or 'HOW MANY SELECTED' in p or 'SAMPLE N:' in p or p=='N: ': return '5'
        if 'DICE' in p and ('HOW MANY' in p or 'NUMBER OF' in p): return '2'
        if 'SIDE' in p: return '6'
        if 'LAST NUMBER' in p: return '36'
        if 'FACE' in p or 'INDEX' in p or 'ROW TO CHANGE' in p or 'OBSERVATION NUMBER' in p or 'CATEGORY NUMBER' in p: return '1'
        if 'AVERAGE' in p or 'MEAN:' in p or 'MEAN MU' in p: return '10'
        if 'STANDARD DEVIATION' in p or 'SD' in p or 'SIGMA' in p: return '2'
        if p.startswith('VALUE ') and p[6:7].isdigit(): return str(int(p.split()[1].rstrip(':')))
        return '2'

    def view(self,title,lines):
        if title=='CHECK ENTERED VALUES':
            raise AssertionError(('Unexpected input rejection',lines,self.path))
        return self.view_impl(title,lines)

    def run(self):
        c.menu=self.menu
        c.choice_pages=self.pages
        c.wait_key=lambda:'right'
        c.view=self.view
        builtins.input=self.read
        while self.queue:
            self.path=self.queue.pop(0)
            self.position=self.reads=0
            self.last_edge=None
            self.peak_bytes=0
            self.peak_modules=()
            self.references={}
            c._menu_pages.clear()
            if len(self.path)>24:
                raise AssertionError('Exploration exceeded expected menu depth')
            error=None
            with contextlib.redirect_stdout(Sink()):
                sys.setprofile(self.profile)
                try:
                    STAT1.main()
                    if self.last_edge: self.passed.add(self.last_edge)
                except Exception:
                    error=traceback.format_exc()
                finally:
                    sys.setprofile(None)
            if c.topic_modules() or c._call_depth:
                error=(error or '')+'\nModules or call depth retained: '+str(c.topic_modules())
            retained=[ref().__name__ for ref in self.references.values() if ref() is not None]
            if retained:
                error=(error or '')+'\nModule objects retained: '+str(retained)
            record={'path':self.path,'peak_loaded_source_bytes':self.peak_bytes,
                    'peak_modules':self.peak_modules,'error':error,
                    'fixture':{'large':self.large,'replacement':self.replacement,'search':self.search,
                               'small_clt':self.small_clt}}
            self.runs.append(record)
            if error: self.failures.append(record)
        for identity,entry in self.menus.items():
            entry['passed']=sorted(key for name,key in self.passed if name==identity)
        return {'menus':self.menus,'runs':self.runs,'failures':self.failures,
                'scope':'Deterministic numeric fixtures; real renderers and calculations; desktop only. Loaded source bytes are not heap bytes.'}


if __name__=='__main__':
    # OS-list transfer is simulated; all calculator arithmetic stays real.
    import types
    ti=types.ModuleType('ti_system')
    ti.recall_list=lambda number:[1,2,3,4,5] if number=='1' else [3,5,8,9,12]
    sys.modules['ti_system']=ti
    walker=Walker()
    walker.queue += [[home,'8',source,direction] for home in ('15','11') for source in ('1','2') for direction in ('1','2')]
    result=walker.run()
    walker.replacement='N'
    walker.queue=[['2','finite']]
    result=walker.run()
    for term in ('mean','median','z score','outlier','empirical rule',
                 'range rule of thumb','expected value'):
        walker.search=term
        walker.queue=[['6','7','5']]
        result=walker.run()
    walker.queue=[['4','5','1','0','E']]
    result=walker.run()
    walker.large=True
    walker.queue=[['4',key] for key in ('1','2','3','4','5')]+[['2','full']]+[
        ['4','1','0','5','4',method] for method in ('1','2','3')]+[
        ['4','1','0','6'], ['4','1','0','10','1','1']]
    result=walker.run()
    walker.small_clt=True
    walker.large=False
    walker.queue=[['9','2','2','2']]
    result=walker.run()
    result['runtime_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in sorted(ROOT.glob('ST*.py'))}
    result['uncovered']={name:sorted(set(menu['options'])-set(menu['passed']))
                         for name,menu in result['menus'].items()
                         if set(menu['options'])-set(menu['passed'])}
    result['scope']+=' ti_system.recall_list uses a five-value desktop fixture, not a physical calculator.'
    from menu_report import render
    render(result)
    destination=ROOT/'MENU_AUDIT.json'
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(len(result['menus']),'menus;',len(result['runs']),'runs;',len(result['failures']),'failures')
    for failure in result['failures']:
        print(failure['path'],failure['error'][-1300:])
    sys.exit(bool(result['failures'] or result['uncovered'] or result['unclassified_menu_sites']))
