# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# StatScholar Free Use / No Sale License, Version 1.0
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
#
# 1. Scope
# "Software" means the StatScholar code and accompanying material that Gregory
# King has the right to license. "Derived Product" means a modification, port,
# translation, or other derivative of the Software, or a product that incorporates
# any portion of it. Independently written software is not a Derived Product
# merely because it uses the same mathematical concepts or algorithms.
#
# 2. Permitted use
# Subject to these terms, you may use, copy, study, and modify the Software for
# personal, educational, and internal business purposes without a license fee.
# You may distribute the Software and Derived Products free of charge, provided
# recipients receive this license and all existing copyright and author notices.
# Your modifications must be identified as yours. These terms must continue to
# apply to the Software and Derived Products you distribute; you may not grant
# recipients permission to sell them.
#
# 3. No sale or paid commercialization
# Without prior written permission from Gregory King, you may not sell, resell,
# rent, license for a fee, or charge for access to the Software or any Derived
# Product. You may not include either in a paid product, bundle, subscription,
# or hosted service, even if the Software is described as a free component.
# You may not require a purchase, payment, or donation to obtain or use either.
# These restrictions apply to original and modified versions, in source or
# compiled form, and cannot be avoided by renaming or repackaging them.
#
# 4. Internal business use and results
# Businesses may use the Software internally without payment. Merely using it
# as an internal tool does not make unrelated goods or services Derived Products.
# Ordinary numerical results produced by running the Software are not licensed
# code and are not subject to the no-sale restriction. This does not permit
# selling access to the Software's functionality or a product built from its code.
#
# 5. Rights retained
# Ownership remains with the respective copyright holders. No rights are granted
# except those stated here; rights that cannot legally be restricted are unaffected.
# This license grants no rights to third-party material beyond those Gregory King
# is entitled to grant. Gregory King may separately authorize uses prohibited here.
# Permission under this license ends if you violate its terms.
#
# 6. No warranty or liability
# To the extent permitted by law, the Software is provided "AS IS", without
# warranties of any kind, including merchantability, fitness for a particular
# purpose, and noninfringement. The copyright holders shall not be liable for
# claims, damages, or other liability arising from the Software or its use.

# STAT1 - home menu and question lookup; topics load only on selection.
import STCORE

def reference_call(name, *args):
    context = {'GUIDES': GUIDES, 'show_identified': show_identified, 'table_tasks': table_tasks, 'experiment_tasks': experiment_tasks, 'probability_tasks': probability_tasks, 'trial_tasks': trial_tasks, 'reference_tasks': reference_tasks, 'data_tasks': data_tasks, 'graph_tasks': graph_tasks, 'study_tasks': study_tasks, 'find_tasks': find_tasks, 'launch_route': launch_route, 'question_lookup': question_lookup, 'homework_tag': homework_tag, 'browse_matrix':browse_matrix, 'ti84_methods':ti84_methods, 'wizard_formula':wizard_formula, 'wizard_counting':wizard_counting, 'question_starters':question_starters}
    module='STSTUDY' if name in ('study_menu','definitions_menu') else 'STFIND' if name=='find_menu' else 'STREF'
    return STCORE.call(module, 'open_reference', name, context, *args)
class LazyIndex:
    def __init__(self,group,keys):
        self.group=group
        self.keys=keys
    def __contains__(self,key): return key in self.keys
    def __iter__(self): return iter(self.keys)
    def __len__(self): return len(self.keys)
    def __getitem__(self,key): return STCORE.call('STINDEX','lookup',self.group,key)

GUIDES=LazyIndex("GUIDES",('D01', 'D02', 'D03', 'D04', 'F01', 'F02', 'F03', 'F04', 'S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S11', 'S12', 'G01', 'G02', 'G03', 'P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'C02', 'C07', 'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'C01', 'C03', 'C04', 'R01', 'R02', 'R03', 'F05', 'F06', 'F07', 'C05', 'P10', 'P11', 'P12', 'P13', 'P14', 'R04', 'R05', 'R06', 'R07', 'R08', 'B11', 'B12', 'B13', 'S13', 'S14', 'S15', 'S16', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'F08', 'D05', 'D06', 'D07', 'D08', 'D09', 'P15'))
NEW_ROUTES=LazyIndex("NEW_ROUTES",('S13', 'S14', 'S15', 'S16', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'F08', 'D05', 'D06', 'D07', 'D08', 'D09', 'P15'))


def get_guide(*args):
    return STCORE.call('STNAV','open_navigation','get_guide',globals(),*args)

def show_identified(*args):
    return STCORE.call('STNAV','open_navigation','show_identified',globals(),*args)


def question_starters(*args):
    return reference_call('question_starters', *args)

def wizard_chart_table(*args):
    return reference_call('wizard_chart_table', *args)

def wizard_raw_data(*args):
    return reference_call('wizard_raw_data', *args)

def wizard_dice_random(*args):
    return reference_call('wizard_dice_random', *args)

def wizard_probability_words(*args):
    return reference_call('wizard_probability_words', *args)

def wizard_binomial(*args):
    return reference_call('wizard_binomial', *args)

def wizard_counting(*args):
    return reference_call('wizard_counting', *args)

def wizard_formula(*args):
    return reference_call('wizard_formula', *args)

def question_wizard():
    return quick_main()

def browse_matrix(*args):
    return reference_call('browse_matrix', *args)

def browse_ids(*args):
    return reference_call('browse_ids', *args)

def definitions_menu(*args):
    return reference_call('definitions_menu', *args)

def ti84_methods(*args):
    return reference_call('ti84_methods', *args)

def run_solver(*args):
    return STCORE.call('STNAV','open_navigation','run_solver',globals(),*args)


def main():
    quick_main()
QUESTION_INDEX = tuple('Q'+('00'+str(i))[-3:] for i in range(1,50))


def concept_session(*args):
    return STCORE.call('STNAV','open_navigation','concept_session',globals(),*args)

def launch_route(*args):
    return STCORE.call('STNAV','open_navigation','launch_route',globals(),*args)

def homework_tag(*args):
    return STCORE.call('STNAV','open_navigation','homework_tag',globals(),*args)

def question_lookup(*args):
    return STCORE.call('STNAV','open_navigation','question_lookup',globals(),*args)

def data_tasks():
    while True:
        key=STCORE.menu('DATA / STATISTICS',[('1','RAW LIST OF NUMBERS'),('2','VALUE + FREQUENCY'),('3','X + P(X)'),('4','ROW / COLUMN TABLE'),('5','CATEGORY COUNTS'),('6','COMPARE TWO DATA SETS'),('7','PERCENT OF TOTAL')],page_size=7)
        if key=='0': return
        routes={'1':('STDATA','raw_session'),'2':('STDATA','frequency_data_session'),'3':('STCOUNT','distribution_session'),'4':('STPROB','two_way_session'),'5':('STPROB','category_session'),'6':('STDATA','compare_session'),'7':('STQUIZ','percent_session')}
        if key in routes: STCORE.call(*routes[key])


def table_tasks():
    data_tasks()


def graph_tasks():
    while True:
        key=STCORE.menu('GRAPHS / NORMAL',[('1','Z / USUAL / EMPIRICAL RULE'),('2','BOXPLOT'),('3','DOTPLOT'),('4','HISTOGRAM'),('5','INTERPRET SHAPE / NORMALITY'),('6','OUTLIERS'),('7','COMPARE RELATIVE POSITION')])
        if key=='0': return
        if key=='5': STCORE.call('STGRAPH','shape_guide')
        elif key=='6':
            choice=STCORE.menu('GRAPH > OUTLIERS',[('1','FROM RAW DATA'),('2','GIVEN Q1 AND Q3')])
            if choice=='1': STCORE.call('STGRAPH','raw_outliers')
            elif choice=='2': STCORE.call('STDESC','solver_outlier')
        elif key!='0': STCORE.call(*{'1':('STNORM','normal_session'),'2':('STGRAPH','boxplot_session'),'3':('STGRAPH','dotplot_session'),'4':('STHIST','histogram_session'),'7':('STNORM','relative_session')}[key])


def experiment_tasks(word=None):
    while True:
        key=STCORE.menu('PROB > RANDOM EXPERIMENT',[('1','ONE / MULTIPLE DICE'),('2','DIE + COIN'),('3','COIN FLIPS'),('4','52 CARDS'),('5','ROULETTE'),('6','SPINNER')],page_size=6)
        if key=='0': return
        if key=='1': STCORE.call('STDICE','dice_session',word)
        elif key=='3': STCORE.call('STBWORD','wording_session',word,None,(1,2))
        elif key!='0': STCORE.call('STEXPER','experiment_session',{'2':'coin','4':'cards','5':'roulette','6':'spinner'}[key],word)
        word=None


def probability_tasks():
    while True:
        key=STCORE.menu('PROB: WHAT DOES IT ASK?',[
            ('H','HELP ME CHOOSE A SOLVER'),
            ('1','HOW MANY OUT OF THE TOTAL?'),
            ('2','GIVEN P(A), P(B), P(BOTH)'),
            ('3','AT LEAST ONE OCCURS'),
            ('4','ROLL DICE / FLIP / DRAW CARD'),
            ('5','TABLE OF x AND ITS CHANCE'),
            ('6','AVERAGE WIN / LOSS / PAYOUT'),
            ('7','IS THIS PROBABILITY VALID?'),
            ('8','COUNTS IN ROWS AND COLUMNS'),
            ('9','FILL IN A MISSING CHANCE'),
            ('10','TOTAL, GROUP A, B AND BOTH'),
            ('11','ALL SELECTED ARE IN A GROUP'),
            ('12','QUIZ 4: DICE / SURVEY'),
            ('13','QUIZ 5: TABLE / BINOMIAL'),('14','DEFECTIVE ITEMS / BOX')])
        if key=='0': return
        if key=='H':
            STCORE.call('STPWORD','choose_probability',{'experiment_tasks':experiment_tasks,'find_tasks':find_tasks,'money_tasks':money_tasks})
            continue
        if key=='3': STCORE.call('STWORDS','word_route','one',{'experiment_tasks':experiment_tasks,'find_tasks':find_tasks,'money_tasks':money_tasks})
        elif key=='4': experiment_tasks()
        elif key=='6': money_tasks()
        elif key=='14': STCORE.call('STSAMPLE','box_session')
        elif key!='0':
            routes={'1':('STPROB','solver_basic_prob'),'2':('STPROB','supplied_session'),'3':('STPROB','solver_at_least_one'),'5':('STCOUNT','distribution_session'),'7':('STPROB','valid_probability'),'8':('STPROB','two_way_session'),'9':('STCOUNT','missing_probability'),'10':('STVENN','venn_session'),'11':('STVENN','selection_question'),'12':('STQUIZ4','quiz_menu'),'13':('STQUIZ5','quiz_menu')}
            STCORE.call(*routes[key])


def money_tasks():
    while True:
        key=STCORE.menu('PROB > EXPECTED / MONEY',[('1','X + P(X): EXPECTED VALUE'),('2','PRIZES / PAYOFFS'),('3','INSURER PROFIT'),('4','RAFFLE'),('5','COUNT / CHOOSE / ARRANGE')])
        if key=='0': return
        if key=='5': reference_call('wizard_counting')
        elif key!='0': STCORE.call('STCOUNT',{'1':'distribution_session','2':'payoff_tasks','3':'insurance_session','4':'raffle_session'}[key])


def trial_tasks():
    STCORE.call('STBWORD','wording_session')


def words_tasks():
    STCORE.call('STWORDS','words_menu',{'experiment_tasks':experiment_tasks,'find_tasks':find_tasks,'money_tasks':money_tasks})


def study_tasks():
    reference_call('study_menu')


def find_tasks():
    reference_call('find_menu')


def reference_tasks():
    find_tasks()


def range_rule_tasks():
    key=STCORE.menu('RANGE RULE OF THUMB',[('1','GIVEN MEAN AND SD'),('2','GIVEN n AND p / PERCENT')])
    if key=='1': STCORE.call('STDESC','solver_usual')
    elif key=='2': STCORE.call('STBINOM','binomial_session',None,None,'4')


def quick_main():
    while True:
        key=STCORE.menu('STAT1',[('1','QUESTION WORDS / HELP'),('2','BINOMIAL'),('3','PROBABILITY'),('4','DATA / STATS'),('5','NORMAL / Z / GRAPHS'),('6','STUDY / CONCEPTS'),('7','PRACTICE TEST 1 / Q1-30')],GUIDES,QUESTION_INDEX,page_size=6)
        if key=='0': return
        try:
            if key=='7':
                STCORE.call('STPRE','pretest_menu')
            elif key in QUESTION_INDEX or key.startswith('PT'): question_lookup(key)
            elif key in GUIDES: launch_route(key)
            else: {'1':words_tasks,'2':trial_tasks,'3':probability_tasks,'4':data_tasks,'5':graph_tasks,'6':study_tasks}[key]()
        except (ValueError,ZeroDivisionError,IndexError) as exc:
            STCORE.view('CHECK ENTERED VALUES',[str(exc)])

if __name__ == '__main__' or STCORE.ON_TI:
    main()
