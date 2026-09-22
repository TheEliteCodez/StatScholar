# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Study classifiers (population/parameter/experiment), loaded only when used.
import STCORE
from STSTUDY import definition_pages, study_yesno


def population_classifier():
    definition_pages('STUDY > POPULATION / SAMPLE','POPULATION: ENTIRE GROUP THE STUDY WANTS TO DESCRIBE. SAMPLE: SUBSET ACTUALLY OBSERVED. IDENTIFY THE TARGET GROUP FROM THE QUESTION; DO NOT ASSUME AN UNSTATED POPULATION.')
    key=STCORE.menu('STUDY > GROUP DESCRIBED',[('1','ENTIRE TARGET GROUP'),('2','SUBSET ACTUALLY OBSERVED'),('3','TARGET NOT STATED')])
    if key!='0': definition_pages('STUDY > ANSWER',{'1':'POPULATION','2':'SAMPLE','3':'NEED THE GROUP THE STUDY WANTS TO DESCRIBE BEFORE IDENTIFYING THE POPULATION.'}[key])


def parameter_classifier():
    entire=study_yesno('BASED ON ENTIRE POPULATION?')
    if entire is None: return
    definition_pages('STUDY > '+('PARAMETER' if entire else 'STATISTIC'),'PARAMETER DESCRIBES POPULATION. STATISTIC DESCRIBES SAMPLE. THIS APPLIES TO MEANS, SDs, COUNTS AND PERCENTAGES. PERCENTAGE ALONE DOES NOT DECIDE.')


def experiment_classifier():
    yes=study_yesno('RESEARCHERS IMPOSE TREATMENT?')
    if yes is None: return
    definition_pages('STUDY > '+('EXPERIMENT' if yes else 'OBSERVATIONAL'),'ASSIGNED OR IMPOSED TREATMENT MEANS EXPERIMENT. MERELY OBSERVING, MEASURING OR SURVEYING IS AN OBSERVATIONAL STUDY.')
