# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Guide routing and solver dispatch; context globals live on STNAV.
import STCORE
import STNAV


def get_guide(gid, field=None):
    if gid in STNAV.NEW_ROUTES:
        module = 'STGNEW'
    elif gid[0] in 'DFSG':
        module = 'STGDESC'
    elif gid[0] == 'P':
        module = 'STGPROB'
    elif gid[0] == 'B':
        module = 'STGBIN'
    elif gid in ('C02', 'C05', 'C07'):
        module = 'STGDICE'
    else:
        module = 'STGCNT'
    return STCORE.call(module, 'get_guide', gid, field)


def show_identified(qid):
    if qid not in STNAV.GUIDES:
        STCORE.view('NOT FOUND', ['GUIDE '+qid+' NOT FOUND'])
        return
    title, solver = STNAV.GUIDES[qid]
    while True:
        key=STCORE.menu(qid+' '+title.upper(), [('1','SOLVE NOW' if solver else 'QUICK ANSWER / CLASSIFY'),('2','HOW TO RECOGNIZE'),('3','FORMULA / SYMBOLS'),('4','SOLVE BY HAND'),('5','TI-84 METHOD'),('6','EXAMPLE'),('7','COMMON MISTAKES'),('8','RELATED TYPES')],page_size=7)
        if key=='0': return
        if key=='1' and solver:
            run_solver(solver)
        else:
            field={'1':'recognize','2':'recognize','3':'values','4':'byhand','5':'ti84','6':'example','7':'mistakes','8':'related'}[key]
            STCORE.view(qid+' '+field.upper(),get_guide(qid,field))


def run_solver(name):
    if name in STNAV.NEW_ROUTES:
        STCORE.call(STNAV.NEW_ROUTES[name][1],STNAV.NEW_ROUTES[name][2])
        return
    if name=='COIN_SESSION':
        STCORE.call('STEXPER','experiment_session','coin')
        return
    for label,module,function in (
        ('BINOMIAL_CONDITIONS', 'STBEXTRA', 'binomial_conditions'),
        ('CATEGORY_SESSION', 'STPROB', 'category_session'),
        ('FREQUENCY_SESSION', 'STDESC', 'frequency_session'),
        ('SUPPLIED_SESSION', 'STPROB', 'supplied_session'),
        ('TWO_WAY_SESSION', 'STPROB', 'two_way_session'),
        ('VALID_PROBABILITY', 'STPROB', 'valid_probability'),
        ('DISTRIBUTION_SESSION', 'STCOUNT', 'distribution_session'),
        ('MISSING_PROBABILITY', 'STCOUNT', 'missing_probability'),
        ('SAMPLE_SESSION', 'STSAMPLE', 'sample_session'),
        ('PAYOFF_SESSION', 'STCOUNT', 'payoff_tasks'),
        ('BINOMIAL_SESSION', 'STBINOM', 'binomial_session'),
        ('SHAPE_SESSION', 'STBEXTRA', 'shape_session'),
        ('SHAPE_TASKS', 'STBEXTRA', 'shape_tasks'),
        ('BASIC_PROB', 'STPROB', 'solver_basic_prob'),
        ('COMPLEMENT', 'STPROB', 'solver_complement'),
        ('GENERAL_OR', 'STPROB', 'solver_general_or'),
        ('MUT_OR', 'STPROB', 'solver_mut_or'),
        ('INDEP_AND', 'STPROB', 'solver_indep_and'),
        ('GENERAL_AND', 'STPROB', 'solver_general_and'),
        ('CONDITIONAL', 'STPROB', 'solver_conditional'),
        ('REL_FREQ', 'STDESC', 'solver_rel_freq'),
        ('RANGE_IQR', 'STDESC', 'solver_range_iqr'),
        ('USUAL', 'STDESC', 'solver_usual'),
        ('ZSCORE', 'STDESC', 'solver_zscore'),
        ('OUTLIER', 'STDESC', 'solver_outlier'),
        ('AT_LEAST_ONE', 'STPROB', 'solver_at_least_one'),
        ('SAMPLE_SPACE', 'STCOUNT', 'solver_sample_space'),
        ('MULTI_DICE', 'STMDICE', 'solver_multi_dice'),
        ('DICE_SPACE', 'STMDICE', 'solver_dice_space'),
        ('NCR', 'STCOUNT', 'solver_ncr'),
        ('NPR', 'STCOUNT', 'solver_npr'),
        ('EXPECTED', 'STCOUNT', 'solver_expected'),
        ('BIN_EXACT', 'STBINOM', 'solver_bin_exact'),
        ('BIN_AT_MOST', 'STBINOM', 'solver_bin_at_most'),
        ('BIN_LESS', 'STBINOM', 'solver_bin_less'),
        ('BIN_AT_LEAST', 'STBINOM', 'solver_bin_at_least'),
        ('BIN_MORE', 'STBINOM', 'solver_bin_more'),
        ('BIN_BETWEEN', 'STBINOM', 'solver_bin_between'),
        ('BIN_MEAN_SD', 'STBINOM', 'solver_bin_mean_sd'),
    ):
        if label==name:
            STCORE.call(module,function)
            return
    raise ValueError('UNKNOWN SOLVER '+name)


def concept_session():
    STCORE.view('CONCEPTS', ['LONG-RUN RELATIVE FREQUENCY', 'ESTIMATES EVENT PROBABILITY', 'EXPECTED VALUE=LONG-RUN MEAN', 'DOLLARS ARE NOT WIN %', 'mu=MEAN; sigma=SD', 'X=COUNT OR MEASURED VALUE', 'BINOMIAL X=SUCCESS COUNT', 'ONE TRIAL: SUCCESS OR NOT', 'p=.5 BINOMIAL IS SYMMETRIC', 'OTHER p: TAILS NEED NOT MATCH'])


def launch_route(route):
    routes = {'ROULETTE': lambda: STCORE.call('STEXPER', 'experiment_session', 'roulette'), 'CARDS': lambda: STCORE.call('STEXPER', 'experiment_session', 'cards'), 'SPINNER': lambda: STCORE.call('STEXPER', 'experiment_session', 'spinner'), 'CATEGORY': STCORE.task('STPROB', 'category_session'), 'CONCEPT': concept_session, 'BINOMIAL_MODEL': STCORE.task('STBEXTRA', 'binomial_model_session'), 'SYMMETRY': STCORE.task('STBEXTRA', 'symmetry_session'), 'WIN_LOSS': STCORE.task('STCOUNT', 'win_loss_session'), 'INSURANCE': STCORE.task('STCOUNT', 'insurance_session'), 'RAFFLE': STCORE.task('STCOUNT', 'raffle_session')}
    if route in routes:
        routes[route]()
    elif route == 'B01':
        STCORE.call('STBEXTRA', 'binomial_conditions')
    elif route in STNAV.GUIDES:
        if STNAV.GUIDES[route][1]:
            run_solver(STNAV.GUIDES[route][1])
        else:
            show_identified(route)


def homework_tag(qid):
    i = int(qid[1:])
    if i <= 2:
        return 'EARLIER ' + str(i)
    if i <= 17:
        return 'CH3A ' + str(i - 2)
    if i <= 31:
        return 'CH4A ' + str(i - 17)
    return 'CH4B ' + str(i - 31)
