# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# STFIND - on-demand reference module.
import STCORE

SEARCH_METHODS = (
 ('PRACTICE TEST 1 / Q1-30','X:pretest','pretest pre test practice test 1 review paper'),
 ('FINITE SAMPLE / 5%','X:finite','finite population independence 5% sample size'),
 ('QUIZ 5 / DISTRIBUTIONS','X:quiz5','quiz 5 quiz5 credit cards girls newborn babies metra merta trains packaging rounded table'),
 ('VENN COUNTS / SURVEY','X:venn','venn compost recycle survey overlap contingency counts'),
 ('ALL SELECTED / REPLACEMENT','X:all','all three students recycle with without replacement cumbersome 5% guideline'),
 ('DICE OUTCOMES / ODD EVEN','X:dice','dice die sum odd even subset sample space matching outcomes'),
 ('QUIZ 4 EXAMPLES','X:quiz4','quiz 4 quiz4 probability'),
 ('RAW DATA SUMMARY','S13','mean median half are below shortest 25% quartile standard deviation variance raw list numbers'),
 ('Q1 / LOWEST 25%','S06','quartile shortest 25% lower fourth'),
 ('Q3 / 75%','S07','quartile upper fourth 75%'),
 ('IQR','S08','quartile interquartile middle 50% spread'),
 ('BOXPLOT','G04','quartile boxplot five number summary box whisker'),
 ('SAMPLE VARIANCE','S14','sample variance squared standard deviation'),
 ('MIDRANGE','S15','midrange average minimum maximum'),
 ('COMPARE TWO DATA SETS','S16','compare two groups lists centers spreads'),
 ('DOTPLOT','G05','dotplot dots repeated values'),
 ('HISTOGRAM / CLASSES','G06','histogram frequency bars classes'),
 ('GROUPED FREQUENCY','F08','grouped frequency class width boundaries cumulative'),
 ('Z-SCORE','S12','z score statistically high usual standard score'),
 ('USUAL RANGE','S10','usual unusual range rule statistically high'),
 ('NORMAL CURVE / AXES','G07','normal bell shaped bell curve z score label axes'),
 ('EMPIRICAL RULE','G08','normal bell shaped empirical 68 95 99.7'),
 ('RELATIVE POSITION','G09','relative position compare z scores'),
 ('AT LEAST ONE','P09','at least one complement none'),
 ('BINOMIAL AT LEAST','B05','at least one at least repeated trials'),
 ('BINOMIAL AT MOST','B03','at most no more than'),
 ('BINOMIAL EXACTLY','B02','exactly binomial trials'),
 ('WITHOUT REPLACEMENT','R07','without replacement selected defective box'),
 ('A / B / BOTH / GIVEN','P10','and or both given conditional independent mutually exclusive'),
 ('ROW / COLUMN TABLE','P14','row column two way table'),
 ('EXPECTED VALUE / MONEY','R02','expected value distribution x p(x)'),
 ('PAYOFF / MONEY','R08','money prizes cost profit loss'),
 ('CERTAIN / IMPOSSIBLE','P15','valid certain impossible probability'),
 ('SAMPLING METHODS','D05','sampling convenience systematic stratified cluster random every 10th easiest people sample every group select classrooms'),
 ('PARAMETER / STATISTIC','D04','parameter statistic population percentage'),
 ('SAMPLE / POPULATION','D03','sample population target group'),
 ('OBSERVATIONAL / EXPERIMENT','D06','observational experiment treatment assigned'),
 ('MEASUREMENT LEVELS','D07','nominal ordinal interval ratio data type measurement'),
 ('SIGNIFICANCE / ERROR','D08','significance significant error practical statistical'),
 ('LAW OF LARGE NUMBERS','D09','law large numbers relative frequency empirical probability'))
def recognition(query):
    return STCORE.call('STFIND1', 'recognition', query)


def search_methods(query):
    return STCORE.call('STFIND1', 'search_methods', query)


def search_words():
    return STCORE.call('STFIND1', 'search_words')


def find_menu():
    return STCORE.call('STFIND2', 'find_menu')


def looks_finder():
    return STCORE.call('STFIND2', 'looks_finder')


def asks_finder():
    return STCORE.call('STFIND2', 'asks_finder')


def open_reference(name, context, *args):
    for key,value in context.items():
        if key not in globals(): globals()[key]=value
    return globals()[name](*args)
