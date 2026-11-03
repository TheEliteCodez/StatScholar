"""Render the desktop menu walk evidence; not part of the calculator program."""
import ast
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent

DORMANT={
    'STBEXTRA.py:shape_tasks':'Older shape menu; no current Home route calls it.',
    'STBINOM2.py:binomial_session':'Older binomial menu; Home and table tools use STBWORD.',
    'STCOUNT6.py:money_session':'Older money menu; Home uses STPROBM.money_tasks.',
    'STDESC1.py:solver_range_iqr':'Older standalone range/IQR menu; summaries provide these values.',
    'STMDICE2.py:word_event':'Its selector needs a nondefault word argument; current Home routes do not pass one. The sum-only branch is exercised.',
}
for name in ('_check_assumption','_read_mean_group','choose_confidence_method',
             '_interpret_given_interval','zstar_menu','confidence_menu'):
    DORMANT['STCI.py:'+name]='Legacy CI bundle; current Home CI menu uses STCIMENU and smaller helpers.'


FOCUSED={
    'STGDIAG.py:venn':'Active optional graph selector; choices 1-7 rendered in test_graph_expansion.py, and event/conditional routes in test_graph_routes.py.',
    'STGINFER.py:chi':'Active optional graph selector; rejection and p-value choices rendered from both real chi-square input routes in test_graph_routes.py.',
}


def render(result):
    seen={m['site'] for m in result['menus'].values()}
    unobserved={}
    for path in ROOT.glob('ST*.py'):
        for function in ast.parse(path.read_text()).body:
            if not isinstance(function,ast.FunctionDef): continue
            calls=[n for n in ast.walk(function) if isinstance(n,ast.Call)
                   and isinstance(n.func,ast.Attribute) and n.func.attr in ('menu','choice_pages')]
            site=path.name+':'+function.name
            if calls and site not in seen:
                unobserved[site]=DORMANT.get(site,FOCUSED.get(site,'UNCLASSIFIED: further checking required.'))
    result['menu_sites_outside_observed_walk']=unobserved
    result['unclassified_menu_sites']=[name for name in unobserved if name not in DORMANT and name not in FOCUSED]
    choices=sum(len(m['options']) for m in result['menus'].values())
    peak=max(result['runs'],key=lambda r:r['peak_loaded_source_bytes'])
    lines=[
        '# Systematic menu audit', '',
        'Current working-tree source; exact runtime SHA-256 hashes and individual paths are in [MENU_AUDIT.json](MENU_AUDIT.json).', '',
        '| Check | Result |','| --- | --- |',
        '| Discovered menu variants | '+str(len(result['menus']))+' |',
        '| Displayed choices exercised | '+str(choices)+'; Back/Exit also exercised |',
        '| Completed replay paths | '+str(len(result['runs']))+' |',
        '| Exceptions / cleanup failures | '+str(len(result['failures']))+' |',
        '| Unchecked choices in discovered menus | '+str(len(result['uncovered']))+' |',
        '| Unclassified menu-bearing functions | '+str(len(result['unclassified_menu_sites']))+' |',
        '| Physical calculator heap | NOT VERIFIED |', '',
        'Run `python -B tests/menu_walk.py` separately from the shared test adapter. The walk uses production menus, result formatting and viewers, deterministic numeric input, and real module cleanup. It explores every choice in each discovered menu variant, including follow-up formatting/method menus. On each path it checks both sys.modules and weak references to loaded topic module objects after returning normally. It does not stub the calculators or disable cleanup.', '',
        'Fixtures cover normal inputs, replacement/no-replacement, seven definition searches, selecting a category before comparing its expected probability, 100 raw values, 25 frequency/probability rows, 10-by-10 tables, 60 categories, 20-trial binomial tables, and full 100-row normal-quantile/observation tables. Existing numerical-oracle, repeat-workflow and physical-key simulation tests remain separate. This is menu-edge coverage for these fixtures, not proof for every possible input or combination of prior selections.', '',
        'Fixed during this audit: choosing 0 in the general between-event endpoint menu now returns without creating an event. A regression check covers both ordinary and binomial event selectors.', '',
        '## Memory evidence and its limit', '',
        'The largest observed set of simultaneously loaded runtime sources totaled **'+format(peak['peak_loaded_source_bytes'],',')+' source bytes**. These are file bytes, not bytecode, compiler workspace, object allocations or measured heap usage. No source-byte threshold was used to declare a calculator-memory pass.', '',
        'Modules at that checkpoint: '+', '.join('`'+n+'`' for n in peak['peak_modules'])+'.', '',
        'The current runtime still accepts numeric sizes/precision whose exact arithmetic or output can grow with the input. The existing row limits bound stored tables, but do not establish an upper bound for every large integer, fraction, exponent or output precision. No new input limits were added.', '',
        '## Checked menu matrix', '',
        'Each row lists the selected keys for one observed menu variant. Dynamic names/data and prior choices can produce additional variants. Option numbers on the binomial question pages restart; that row records the internal wording tokens and labels.', '',
        '| Menu / source function | Checked options |',
        '| --- | --- |',
    ]
    for identity,menu in sorted(result['menus'].items()):
        title=identity.split(' | ',1)[1].replace('|','/')
        options='; '.join(str(key)+' '+label.replace('|','/') for key,label in menu['options'].items())
        lines.append('| '+title+' (`'+menu['site']+'`) | '+options+' |')
    lines += ['', '## Menu code outside the observed text-menu walk', '',
              'These source functions were reviewed separately from the exposed menu tree. These include retained compatibility/legacy paths and active optional graph selectors. Active graph selectors are tested separately by the named renderer/route suites; they are not classified as dormant.', '',
              '| Source function | Scope |','| --- | --- |']
    lines += ['| `'+name+'` | '+reason+' |' for name,reason in sorted(unobserved.items())]
    (ROOT/'MENU_AUDIT.md').write_text('\n'.join(lines)+'\n')
