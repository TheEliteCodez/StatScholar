"""Maximum existing table/list sizes for the new chi-square/regression routes."""
import hashlib
import json
import sys
import types
from menu_walk import Walker, ROOT


def main():
    ti=types.ModuleType('ti_system')
    ti.recall_list=lambda number:list(range(1,101)) if number=='1' else [2*i+i%2 for i in range(1,101)]
    sys.modules['ti_system']=ti
    walker=Walker();walker.large=True
    walker.queue=[['15','5'],['15','6'],['15','7'],['15','8'],['11','8'],['4','8'],['5','1']]
    walker.queue += [[home,'8',source,direction] for home in ('15','11') for source in ('1','2') for direction in ('1','2')]
    choose_original=walker.choose
    parents=('STAT1','HYPOTHESIS TESTING','DATA / STATISTICS','GRAPHS / DATA SHAPE','CONFIDENCE INTERVAL / MOE')
    def choose(title,items):
        if title in parents and walker.position==len(walker.path): return '0'
        return choose_original(title,items)
    walker.choose=choose
    result=walker.run()
    result['uncovered']={name:sorted(set(menu['options'])-set(menu['passed']))
        for name,menu in result['menus'].items()
        if name.split(' | ',1)[-1] not in parents and set(menu['options'])-set(menu['passed'])}
    result['runtime_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted(ROOT.glob('ST*.py'))}
    result['scope']='60-category GOF, 10x10 independence, 100 paired values; real calculations/viewers, sys.modules and weakref cleanup. Desktop fixtures; not calculator heap proof.'
    (ROOT/'ADVANCED_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    peak=max(result['runs'],key=lambda r:r['peak_loaded_source_bytes'])
    lines=['# Chi-square and regression maximum-size replay','',result['scope'],'',
        '%d paths; %d failures; %d menus with unchecked choices.' %
        (len(result['runs']),len(result['failures']),len(result['uncovered'])),'',
        'Largest simultaneous source set: %d bytes (not heap bytes).' % peak['peak_loaded_source_bytes'],
        'Modules: '+', '.join(peak['peak_modules']),
        '', 'See ADVANCED_AUDIT.json for individual paths and current source hashes.']
    (ROOT/'ADVANCED_AUDIT.md').write_text('\n'.join(lines)+'\n')
    print(lines[4]);print(lines[6])
    for failure in result['failures']: print(failure['path'],failure['error'])
    return bool(result['failures'] or result['uncovered'])


if __name__=='__main__': sys.exit(main())
