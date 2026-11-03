"""Complete scoped hypothesis menu walk, with real math/viewers and cleanup."""
import hashlib
import json
from pathlib import Path
import sys
from menu_walk import Walker, ROOT


def main():
    import types
    ti=types.ModuleType('ti_system')
    ti.recall_list=lambda number:[1,2,3,4,5] if number=='1' else [3,5,8,9,12]
    sys.modules['ti_system']=ti
    walker=Walker()
    walker.queue=[['15',str(i)] for i in range(1,9)]
    walker.queue += [['15','8',source,direction] for source in ('1','2') for direction in ('1','2')]
    choosing=walker.choose
    parents=('STAT1','HYPOTHESIS TESTING')
    def choose(title,items):
        if title in parents and walker.position==len(walker.path): return '0'
        return choosing(title,items)
    walker.choose=choose
    result=walker.run()
    result['uncovered']={name:sorted(set(menu['options'])-set(menu['passed']))
                         for name,menu in result['menus'].items()
                         if name.split(' | ',1)[-1] not in parents
                         and set(menu['options'])-set(menu['passed'])}
    result['runtime_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in sorted(ROOT.glob('ST*.py'))}
    result['scope']='Home 15 only; deterministic numeric fixtures; real math, renderers and cleanup. Desktop source-byte observations are not calculator heap measurements.'
    (ROOT/'HYPOTHESIS_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    menus={name:m for name,m in result['menus'].items() if name.split(' | ',1)[-1] not in parents}
    lines=['# Hypothesis testing audit','',
           str(len(menus))+' scoped menu variants; '+str(len(result['runs']))+' paths; '+
           str(len(result['failures']))+' failures; '+str(len(result['uncovered']))+' menus with unchecked options.','',
           'All eight Home 15 routes are seeded separately, including chi-square, regression and automatic paired tests/intervals. Randomness, claim operators, expected-count modes, summary/raw mean input, normality checks, review steps, predictions and residuals are exercised. Calculators, result viewers and module cleanup run normally; menu choices and numeric entries are deterministic desktop fixtures. No remaining topic module entries or live module objects are permitted after a path returns.','',
           'Physical TI-84 heap capacity remains unverified. Full path records and runtime hashes are in HYPOTHESIS_AUDIT.json.','',
           '| Menu | Checked choices |','| --- | --- |']
    for name,menu in sorted(menus.items()):
        lines.append('| '+name.replace('|','/')+' | '+'; '.join(k+' '+v for k,v in menu['options'].items())+' |')
    (ROOT/'HYPOTHESIS_AUDIT.md').write_text('\n'.join(lines)+'\n')
    print(len(menus),'menus;',len(result['runs']),'paths;',len(result['failures']),
          'failures;',len(result['uncovered']),'menus with unchecked choices')
    for failure in result['failures']: print(failure['path'],failure['error'])
    if result['uncovered']: print(result['uncovered'])
    return bool(result['failures'] or result['uncovered'])


if __name__=='__main__': sys.exit(main())
