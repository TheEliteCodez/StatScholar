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
    context = {'GUIDES': GUIDES, 'show_identified': show_identified, 'table_tasks': table_tasks, 'experiment_tasks': experiment_tasks, 'probability_tasks': probability_tasks, 'trial_tasks': trial_tasks, 'data_tasks': data_tasks, 'graph_tasks': graph_tasks, 'study_tasks': study_tasks, 'find_tasks': find_tasks, 'launch_route': launch_route, 'question_lookup': question_lookup, 'homework_tag': homework_tag, 'browse_matrix':browse_matrix, 'ti84_methods':ti84_methods, 'wizard_formula':wizard_formula, 'wizard_counting':wizard_counting, 'question_starters':question_starters}
    module='STSTUDY' if name in ('study_menu','definitions_menu') else 'STFIND' if name=='find_menu' else 'STREF'
    return STCORE.call(module, 'open_reference', name, context, *args)
class KeySet:
    # One delimited string instead of a tuple of strings keeps the startup heap small.
    def __init__(self, group, ids):
        self.group = group
        self.ids = ',' + ids.strip(',') + ','
    def __contains__(self, key): return (',' + key + ',') in self.ids
    def __iter__(self): return iter(self.ids[1:-1].split(','))
    def __len__(self): return self.ids.count(',') - 1
    def __getitem__(self, key): return STCORE.call('STINDEX', 'lookup', self.group, key)


class QSet:
    # Q001..Q049 are regular, so no storage is needed at all.
    def __contains__(self, key):
        return isinstance(key, str) and len(key) == 4 and key[0] == 'Q' and key[1:].isdigit() and 1 <= int(key[1:]) <= 49
    def __iter__(self):
        for i in range(1, 50):
            yield 'Q%03d' % i
    def __len__(self): return 49


GUIDES=KeySet("GUIDES",'D01,D02,D03,D04,F01,F02,F03,F04,S01,S02,S03,S04,S05,S06,S07,S08,S09,S10,S11,S12,G01,G02,G03,P01,P02,P03,P04,P05,P06,P07,P08,P09,C02,C07,B01,B02,B03,B04,B05,B06,B07,B08,B09,B10,C01,C03,C04,R01,R02,R03,F05,F06,F07,C05,P10,P11,P12,P13,P14,R04,R05,R06,R07,R08,B11,B12,B13,S13,S14,S15,S16,G04,G05,G06,G07,G08,G09,F08,D05,D06,D07,D08,D09,P15')
NEW_ROUTES=KeySet("NEW_ROUTES",'S13,S14,S15,S16,G04,G05,G06,G07,G08,G09,F08,D05,D06,D07,D08,D09,P15')


def get_guide(*args):
    return STCORE.call('STNAV','open_navigation','get_guide',globals(),*args)

def show_identified(*args):
    return STCORE.call('STNAV','open_navigation','show_identified',globals(),*args)


def question_starters(*args):
    return reference_call('question_starters', *args)

def wizard_raw_data(*args):
    return reference_call('wizard_raw_data', *args)

def wizard_counting(*args):
    return reference_call('wizard_counting', *args)

def wizard_formula(*args):
    return reference_call('wizard_formula', *args)

def question_wizard():
    return STCORE.call('STWIZM','question_wizard',globals())

def browse_matrix(*args):
    return reference_call('browse_matrix', *args)

def browse_ids(*args):
    return reference_call('browse_ids', *args)

def definitions_menu(*args):
    return reference_call('definitions_menu', *args)

def ti84_methods(*args):
    return reference_call('ti84_methods', *args)


def main():
    quick_main()
QUESTION_INDEX = QSet()


def launch_route(*args):
    return STCORE.call('STNAV','open_navigation','launch_route',globals(),*args)

def homework_tag(*args):
    return STCORE.call('STNAV','open_navigation','homework_tag',globals(),*args)

def question_lookup(*args):
    return STCORE.call('STNAV','open_navigation','question_lookup',globals(),*args)

def data_tasks():
    return STCORE.call('STTASKS','data_tasks',globals())


def table_tasks():
    return STCORE.call('STTASKS','table_tasks',globals())


def graph_tasks():
    return STCORE.call('STTASKS','graph_tasks',globals())


def experiment_tasks(word=None):
    return STCORE.call('STTASKS','experiment_tasks',globals(),word)


def probability_tasks():
    return STCORE.call('STPROBM','probability_tasks',globals())


def money_tasks():
    return STCORE.call('STPROBM','money_tasks',globals())


def trial_tasks():
    return STCORE.call('STHOME','trial_tasks',globals())


def words_tasks():
    return STCORE.call('STHOME','words_tasks',globals())


def study_tasks():
    return STCORE.call('STHOME','study_tasks',globals())


def find_tasks():
    return STCORE.call('STHOME','find_tasks',globals())


def quick_main():
    return STCORE.call('STHOME','quick_main',globals())

if __name__ == '__main__' or STCORE.ON_TI:
    main()
