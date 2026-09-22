# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STREF - on-demand reference module.
import STCORE

STARTERS = [('Roll 3, 4, 5, 6 or more fair dice...', 'C07'), ('You roll two fair dice...', 'C02'), ('An experiment is rolling a fair die and then flipping a coin...', 'C01'), ('Find the probability that the sum is...', 'P01'), ('Find the probability that A OR B...', 'P04'), ('E and F are mutually exclusive events...', 'P03'), ('Find P(E|F)...', 'P07'), ('Find the probability that at least one...', 'P09'), ("Using your whole group's sample, determine what proportion...", 'F04'), ('Under what distance do the shortest 25%...', 'S06'), ('Half of students travel under what distance...', 'S02'), ('Calculate the maximum usual value...', 'S10'), ('Are any values statistically high? Find z-scores...', 'S12'), ('Does the data appear to come from a Normally distributed population? Why?', 'G02'), ('For the data shown above, find the mean...', 'S01'), ('Find the five-number summary...', 'S05'), ('Find the interquartile range...', 'S08'), ('Find the expected value of X...', 'R02'), ('Is this a valid probability distribution?', 'R01'), ('Choose r objects from n...', 'C03'), ('Arrange or rank r objects from n...', 'C04'), ('What is the probability of exactly x successes...', 'B02'), ('What is the probability of at most x successes...', 'B03'), ('What is the probability of less than x successes...', 'B04'), ('What is the probability of at least x successes...', 'B05'), ('What is the probability of more than x successes...', 'B06'), ('VALUES + FREQUENCY; MEAN', 'F05'), ('FREQUENCY TABLE; MEDIAN', 'F06'), ('FREQUENCY TABLE; MODE', 'F07'), ('DIE THEN COIN; LIST OUTCOMES', 'C05'), ('CAN THESE OCCUR TOGETHER?', 'P10'), ('ARE EVENTS INDEPENDENT?', 'P11'), ('AND / BOTH FROM COUNTS', 'P12'), ('CAN THIS BE A PROBABILITY?', 'P13'), ('ROW/COLUMN TABLE; ONE EVENT', 'P14'), ('TABLE ALREADY GIVES P(X)', 'R04'), ('ONE BLANK IN P(X) COLUMN', 'R05'), ('IS AN EVENT UNUSUAL?', 'R06'), ('BOX; TARGET COUNT; SELECT n', 'R07'), ('PRIZES, COSTS, PROFIT, LOSS', 'R08'), ('LIST X AND P(X) FOR TRIALS', 'B11'), ('MATCH GRAPH TO p; SYMMETRY', 'B12'), ('RANGE RULE; FIRST UNUSUAL', 'B13')]
def question_starters():
    return STCORE.call('STREF1', 'question_starters')


def wizard_raw_data():
    return STCORE.call('STREF1', 'wizard_raw_data')


def wizard_counting():
    return STCORE.call('STREF1', 'wizard_counting')


def wizard_formula():
    return STCORE.call('STREF1', 'wizard_formula')


def browse_matrix():
    return STCORE.call('STREF2', 'browse_matrix')


def browse_ids(title, ids):
    return STCORE.call('STREF2', 'browse_ids', title, ids)


def ti84_methods():
    return STCORE.call('STREF2', 'ti84_methods')


def open_reference(name, context, *args):
    for key,value in context.items():
        if key not in globals(): globals()[key]=value
    return globals()[name](*args)
