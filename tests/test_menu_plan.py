# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.


import contextlib
from fractions import Fraction
import io
import statistics
import tracemalloc
import unittest
from unittest.mock import patch
from test_expansion import flow, raw
import STAT1 as app
import STCORE as c
import STVIEW as view
import STDMATH as dm
import STBINFO as info
import STBWORD as bw
import STNORM as normal
import STVENN as venn
import STPRE as pre
import STSTUDY as study
import STMDICE as dice


class MenuPlan(unittest.TestCase):
    def setUp(self): c._menu_pages.clear()

    def test_weighted_statistics_match_independent_expanded_oracle(self):
        for numbers in ([1,2],[1,1,2,4,9],[0,0,0,1,1,7],[2,2,2],[1,1,2,2,3,3,4]):
            stats=dm.weighted_stats(dm.value_counts(raw(numbers)))
            self.assertEqual(Fraction(*stats['MEAN']),Fraction(sum(numbers),len(numbers)))
            self.assertAlmostEqual(float(Fraction(*stats['SAMPLE VARIANCE s^2'])),statistics.variance(numbers))
            self.assertAlmostEqual(float(Fraction(*stats['POPULATION VARIANCE'])),statistics.pvariance(numbers))
            xs=sorted(numbers);n=len(xs)
            self.assertEqual(float(Fraction(*stats['Q1'])),statistics.median(xs[:n//2]))
            self.assertEqual(float(Fraction(*stats['Q3'])),statistics.median(xs[(n+1)//2:]))
        self.assertEqual(stats['MODE'],'DNE')

    def test_large_frequencies_do_not_expand_observations(self):
        tracemalloc.start()
        stats=dm.weighted_stats([((1,1),1000000),((3,1),1000000)])
        _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
        self.assertEqual(stats['n'],2000000)
        self.assertEqual(stats['MEAN'],(2,1))
        self.assertLess(peak,100000)

    def test_numeric_alias_and_page_retention(self):
        items=[('1','ONE'),('2','TWO'),('H','HELP')]
        with patch.object(c,'read_choice',return_value='3'),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(view.menu('NUMERIC',items),'H')
        items=[(str(i),'ITEM '+str(i)) for i in range(1,9)]
        with patch.object(c,'read_choice',side_effect=['7','0']),contextlib.redirect_stdout(io.StringIO()) as screen:
            self.assertEqual(view.menu('RETAIN',items),'7')
            self.assertEqual(view.menu('RETAIN',items),'0')
        self.assertIn('6 ITEM 6',screen.getvalue())
        self.assertNotIn('RETAIN',c._menu_pages)

    def test_first_answer_does_not_calculate_statistics(self):
        with patch.object(info,'binomial_quartiles',side_effect=AssertionError('too early')),patch.object(c,'view',return_value='exit'):
            info.show_answer(700,(17,25),('>=',521,0),(1,10000),'ANSWER',['P=.0001'])

    def test_quartiles_cached_across_answer_revisits(self):
        cache={}
        with patch.object(info,'binomial_quartiles',wraps=info.binomial_quartiles) as calculate:
            for _ in range(2): list(info.report_pages(10,(1,20),('=',1,0),(3,10),(1,100),cache))
        self.assertEqual(calculate.call_count,1)

    def test_binomial_format_and_threshold_persist(self):
        out,prompts=flow(lambda:bw.wording_session('='),['4','.5','0','6','.1','1','5','3','2','1','1','0','0'])
        self.assertIn('PROBABILITY CUTOFF=0.1',out)
        self.assertIn('EVENT UNUSUAL=YES',out)
        self.assertGreaterEqual(out.count('ANSWER=6.25%'),2)
        self.assertEqual(prompts.count('TRIALS n: '),1)

    def test_none_presets_zero(self):
        out,prompts=flow(lambda:bw.wording_session('none'),['4','.5','0'])
        self.assertIn('ANSWER=0.0625',out)
        self.assertFalse(any('CUTOFF' in p for p in prompts))

    def test_box_from_probability_home(self):
        out,prompts=flow(app.main,['3','14','1','8','5','2','1','2','1','0','0','0'])
        self.assertIn('E(X)=1.2500',out)
        self.assertIn('mu=1.2500',out)
        self.assertEqual(prompts.count('TOTAL OBJECTS IN BOX: '),1)

    def test_replacement_can_exceed_population(self):
        out,_=flow(venn.selection_session,['2','1','5','1','0'])
        self.assertIn('WITH REPLACEMENT=0.0313',out)
        self.assertIn('NOT APPLICABLE',out)

    def test_frequency_complete_report_and_population_choice(self):
        out,prompts=flow(app.main,['4','2','2','1','2','3','2','1','8','2','1','0','0','0'])
        for value in ('Q1=1.0000','Q3=3.0000','LOWER FENCE=-2.0000','UPPER FENCE=6.0000','POPULATION VARIANCE=1.0000'):
            self.assertIn(value,out)
        self.assertEqual(prompts.count('NUMBER OF ROWS: '),1)

    def test_guided_cards_suit(self):
        out,_=flow(app.main,['3','4','4','1','4','1','1','0','0','0','0'])
        self.assertIn('P(EVENT)=0.2500',out)

    def test_dice_strict_and_between_sum_against_enumeration(self):
        from itertools import product
        for op,inputs,test in [('[]',['7','10','1'],lambda s:7<=s<=10),('<',['8'],lambda s:s<8),('>',['12'],lambda s:s>12)]:
            with patch.object(c,'results') as output:
                flow(lambda:dice.word_event(3,op,True),inputs)
            answers=dict(output.call_args.args[1])
            wanted=Fraction(sum(test(sum(p)) for p in product(range(1,7),repeat=3)),216)
            self.assertEqual(Fraction(*answers['P']),wanted)

    def test_zero_sd_and_combined_observation(self):
        out,_=flow(lambda:normal.normal_session((42,1),(3,1),'1'),['37','1','0'])
        for value in ('z=-1.6667','MIN USUAL=36.0000','MAX USUAL=48.0000','NOT UNUSUAL'):
            self.assertIn(value,out)
        out,_=flow(lambda:normal.normal_session((4,1),(0,1),'1'),['4','1','0'])
        self.assertIn('DNE (SD=0)',out)

    def test_empirical_explicit_parameters_and_segment(self):
        out,_=flow(normal.empirical_session,['8','100','10','9','1','2','1','0'])
        self.assertIn('APPROX PERCENT=13.5000',out)
        self.assertIn('LOW x=110.0000',out)
        self.assertIn('HIGH x=120.0000',out)

    def test_sampling_procedure_is_separate_from_bias(self):
        out,_=flow(study.sampling_menu,['1','1','0','0','0'])
        self.assertIn('SYSTEMATIC',out)
        self.assertIn('EXCLUDES NONVISITORS',out)
        self.assertEqual(study.normalized_term('z-score'),'z score')
        self.assertEqual(study.normalized_term('stratified sampling'),'stratified sample')

    def test_targeted_practice_routes_and_next_question(self):
        self.assertEqual(pre.get_record(11)[2],'one')
        self.assertEqual(pre.ROUTES['one'],('STBWORD','wording_session','one'))
        self.assertEqual(pre.get_record(24)[2],'observations')
        out,_=flow(lambda:pre.pretest_menu(23),['91','0','0'])
        self.assertIn('PRETEST Q24',out)
        self.assertIn('21 Sports poll',out)

    def test_clear_exits_result_without_format_menu(self):
        with patch.object(c,'view',return_value='exit'), patch.object(c,'menu') as menu:
            view.results('RESULT',[('P',(1,2))])
            view.paged_results('TABLE',20,lambda i:(str(i),i))
        menu.assert_not_called()

    def test_dice_or_word_opens_combined_event_directly(self):
        import STPWORD
        out,prompts=flow(lambda:STPWORD.probability_words('or'),
                         ['4','2','1','1','3','1','1','7','1','0'])
        self.assertIn('P=0.2222',out)
        self.assertIn('SUCCESSFUL=8',out)
        self.assertNotIn('TWO DICE > QUESTION',out)

    def test_edit_raw_recomputes_saved_summary(self):
        import STDATA
        out,_=flow(lambda:STDATA.raw_session(raw([1,2,3])),
                   ['1','9','1','2','8','1','1','1','0'])
        self.assertIn('MEAN=4.0000',out)
        self.assertIn('MAX=8.0000',out)

    def test_frequency_between_endpoint_choices(self):
        import STQUIZ
        rows=[((1,1),2),((2,1),3),((3,1),5)]
        for endpoint,wanted in [('1','1.0000'),('2','0.3000'),('3','0.5000'),('4','0.8000')]:
            out,_=flow(lambda:STQUIZ.frequency_tools(rows),['7','1','3',endpoint,'1','0'])
            self.assertIn('PROPORTION='+wanted,out)

    def test_graph_guide_describes_actual_output(self):
        import STGDESC
        guide=STGDESC.get_guide('G02')
        self.assertIn('STAT1 GIVES PLOT VALUES',str(guide))
        self.assertNotIn('CALCULATOR SHOWS GRAPH',str(guide))

if __name__=='__main__': unittest.main()
