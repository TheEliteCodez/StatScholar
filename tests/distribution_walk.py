"""Scoped real-menu replay for the distribution sections; desktop fixtures only."""
import sys
from menu_walk import Walker


def main():
    walker=Walker()
    walker.queue=[['1'],['2'],['7'],['8'],['3','14'],['4','3'],['9'],['3','4','1']]
    original_choose=walker.choose
    original_read=walker.read
    parents=('STAT1','PROB: WHAT DOES IT ASK?','GRAPHS / DATA SHAPE',
             'DATA / STATISTICS','PROB > RANDOM EXPERIMENT')
    def choose(title,items):
        if title in parents and walker.position==len(walker.path): return '0'
        return original_choose(title,items)
    def read(prompt=''):
        if prompt in ('RIGHT-TAIL AREA: ','LEFT-TAIL AREA: ','AREA FROM 0 TO CUTOFF: '): return '.25'
        return original_read(prompt)
    walker.choose=choose
    walker.read=read
    result=walker.run()
    missing={name:sorted(set(menu['options'])-set(menu['passed']))
             for name,menu in result['menus'].items()
             if name.split(' | ',1)[-1] not in parents and set(menu['options'])-set(menu['passed'])}
    print(len(result['menus']),'menus;',len(result['runs']),'runs;',
          len(result['failures']),'failures;',len(missing),'uncovered menus')
    for failure in result['failures']: print(failure['path'],failure['error'])
    if missing: print(missing)
    return bool(result['failures'] or missing)


if __name__=='__main__': sys.exit(main())
