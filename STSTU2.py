# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Study menus (sampling/measurement/significance/large-numbers), loaded only when used.
import STCORE
from STSTUDY import definition_pages, definition_list, SAMPLING_DEFINITIONS, MEASUREMENT_DEFINITIONS, STUDY_DEFINITIONS, BIAS_DEFINITIONS, DEFINITIONS


def sampling_menu():
    while True:
        key=STCORE.menu('STUDY > SAMPLING',[('1','IDENTIFY SELECTION METHOD'),('2','VIEW METHODS'),('3','CHECK FRAME / SURVEY BIAS')])
        if key=='0': return
        if key=='2': definition_list('STUDY > METHODS',SAMPLING_DEFINITIONS)
        elif key=='3': definition_list('SURVEY BIAS / QUOTAS',BIAS_DEFINITIONS)
        else:
            method=STCORE.menu('HOW ARE PEOPLE SELECTED?', [('1','EVERY kth PERSON'),('2','RANDOM FROM EVERY GROUP'),('3','RANDOM WHOLE GROUPS'),('4','PEOPLE CHOOSE TO RESPOND'),('5','FILL SUBGROUP QUOTAS'),('6','EASIEST PEOPLE TO REACH'),('7','ALL SIZE-n SUBSETS EQUALLY'),('8','EACH PERSON EQUALLY'),('9','GROUPS THEN SOME MEMBERS')])
            if method=='0': continue
            if method in ('1','2','3','6','7','8'):
                definition_pages(*SAMPLING_DEFINITIONS[{'1':2,'2':4,'3':5,'6':3,'7':0,'8':1}[method]])
            elif method=='9': definition_pages(*DEFINITIONS[-1])
            else: definition_pages(*BIAS_DEFINITIONS[0 if method=='4' else 3])
            definition_pages('METHOD VERSUS BIAS','THE SELECTION METHOD AND REPRESENTATIVENESS ARE SEPARATE. EVERY TENTH LIBRARY VISITOR IS SYSTEMATIC, BUT EXCLUDES NONVISITORS. SAMPLING MENU 3 EXPLAINS SURVEY BIAS.')


def measurement_menu():
    while True:
        key=STCORE.menu('STUDY > DATA TYPE',[('1','QUALITATIVE / QUANTITATIVE'),('2','DISCRETE / CONTINUOUS'),('3','MEASUREMENT LEVELS')])
        if key=='0': return
        if key=='1': definition_pages('STUDY > DATA TYPE','QUALITATIVE: CATEGORIES OR LABELS. QUANTITATIVE: NUMERICAL COUNTS OR MEASUREMENTS. A NUMBER USED ONLY AS AN ID IS A LABEL.')
        elif key=='2': definition_pages('STUDY > DATA TYPE','DISCRETE: COUNTABLE VALUES, LIKE NUMBER OF CHILDREN. CONTINUOUS: MEASUREMENTS THROUGH AN INTERVAL, LIKE HEIGHT.')
        elif key=='3': definition_list('STUDY > MEASUREMENT',MEASUREMENT_DEFINITIONS)


def significance_menu():
    while True:
        key=STCORE.menu('STUDY > SIGNIFICANCE',[('1','STATISTICAL VS PRACTICAL'),('2','ERROR DEFINITIONS'),('3','GIVEN p-VALUE: COMPARE alpha')])
        if key=='0': return
        if key=='1': definition_pages('STUDY > INTERPRETATION','STATISTICAL: UNLIKELY UNDER THE NULL; COMPARE p-VALUE TO alpha. PRACTICAL: IS THE EFFECT LARGE ENOUGH TO MATTER IN CONTEXT? CONSIDER EFFECT SIZE, COSTS AND CONSEQUENCES. STATISTICAL SIGNIFICANCE ALONE CANNOT DECIDE PRACTICAL IMPORTANCE.')
        elif key=='2': definition_list('STUDY > ERROR',STUDY_DEFINITIONS[:2])
        elif key=='3':
            p=STCORE.read_exact('p-VALUE: '); alpha=STCORE.read_exact('alpha: ')
            STCORE.results('STUDY > SIGNIFICANCE',[('STATISTICALLY SIGNIFICANT','YES' if STCORE.compare_exact(p,alpha)<=0 else 'NO'),('PRACTICALLY SIGNIFICANT','NEED EFFECT SIZE / CONTEXT')],['COMPARE p-VALUE <= alpha'])


def large_numbers():
    definition_pages('LAW OF LARGE NUMBERS','AS THE NUMBER OF INDEPENDENT TRIALS WITH THE SAME PROBABILITY BECOMES LARGE, RELATIVE FREQUENCY TENDS TO GET CLOSER TO THE TRUE PROBABILITY. SEE RELATIVE FREQUENCY AND EMPIRICAL PROBABILITY. THIS DOES NOT MEAN A LOSING STREAK MAKES A WIN DUE.')
