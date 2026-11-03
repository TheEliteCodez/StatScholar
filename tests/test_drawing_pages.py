import unittest
from unittest.mock import patch
import STCORE as c
import STNDIST
import STUNIF
import STTPROB
import STCIIO
import STBINOM2
import STVRES
import STHOME
from test_expansion import flow


class DrawingPages(unittest.TestCase):
    def test_bus_cutoff_uses_question_wording_and_matching_shading(self):
        for wording,cutoff,shade in [('1','6.0000','LEFT'),('2','14.0000','RIGHT')]:
            output,_=flow(STUNIF.uniform_menu,['2', '0', '20', wording, '30%', '0'])
            self.assertIn('VALUE CUTOFF x='+cutoff,output)
            self.assertIn('SHADE '+shade+' OF CUTOFF.',output)
        self.assertIn('LEFT=1-0.300000=0.700000',output)

    def test_normal_at_least_converts_right_tail_area(self):
        output,_=flow(STNDIST.normal_menu,['2', '0', '1', '2', '5%', '0'])
        self.assertIn('VALUE CUTOFF x=1.6449',output)
        self.assertIn('SHADE RIGHT OF CUTOFF.',output)

    def test_percentile_answer_has_own_short_screen_before_drawing(self):
        cases=[(lambda:STNDIST._normal_percentile(100,15),'VALUE CUTOFF x=124.6728'),
               (lambda:STUNIF._uniform_percentile(0,20),'VALUE CUTOFF x=19.0000')]
        for calculate,answer in cases:
            with patch('builtins.input',side_effect=['3','95%']),patch.object(c,'view') as view:
                calculate()
            first=view.call_args_list[0].args
            self.assertIn('ANSWER',first[0])
            self.assertEqual(first[1][0],answer)
            self.assertLessEqual(len(list(c.wrapped_lines(first[1]))),c.VIEW_LINES)
            self.assertNotIn('HOW TO DRAW',' '.join(first[1]))
            self.assertEqual(view.call_args_list[1].args[1][0],answer)

    def test_back_from_percentile_answer_does_not_open_drawing(self):
        with patch('builtins.input',side_effect=['3','95%']),patch.object(c,'view',return_value='exit') as view:
            STNDIST._normal_percentile(100,15)
        self.assertEqual(view.call_count,1)

    def test_sample_mean_z_uses_population_sd_and_sample_size(self):
        for cutoff,expected in [('4.08','6.4000'),('3.92','-6.4000')]:
            output,prompts=flow(STHOME.quick_main,
                ['12','2',cutoff,'4','.05','16','0','0'])
            for text in ('SAMPLE-MEAN Z-SCORE','z='+expected,
                         'STANDARD ERROR SE=0.0125',
                         'SE=sigma/sqrt(n)=0.050000/sqrt(16)=0.012500',
                         'z=(x-bar-mu)/(sigma/sqrt(n))'):
                self.assertIn(text,output)
            self.assertIn('POPULATION SD sigma: ',prompts)
            self.assertIn('SAMPLE SIZE n: ',prompts)

    def test_home_zscore_calculator_and_work(self):
        for x,expected in (('10','0.3500'),('8','-0.6500'),('9.3','0.0000')):
            output,_=flow(STHOME.quick_main,['12','1',x,'9.3','2','0','0'])
            self.assertIn('Z-SCORE CALCULATOR',output)
            self.assertIn('z='+expected,output)
            self.assertIn('z=(x-MEAN)/SD',output)
            self.assertIn('HOW TO DRAW: x / z AXES',output)

    def test_normal_probability_and_percentile_use_entered_cutoffs(self):
        output,_=flow(STNDIST.normal_menu,
                      ['1', '9.3', '2', '2', '10', '', '2', '3', '50%', '0'])
        for text in ('HOW TO DRAW: NORMAL','CENTER=9.3000; SD=2.0000',
                     'MARK CUTOFF: 10.0','SHADE RIGHT OF CUTOFF.',
                     'MARK CUTOFF: 9.3','SHADE LEFT OF CUTOFF.'):
            self.assertIn(text,output)

    def test_uniform_rectangle_and_between_shading(self):
        output,_=flow(STUNIF.uniform_menu,
                      ['1', '2', '12', '3', '4', '8', '0'])
        for text in ('RECTANGLE FROM 2.0000 TO 12.0000','HEIGHT=0.1000',
                     'MARK CUTOFF: 4.0','MARK CUTOFF: 8.0',
                     'SHADE BETWEEN CUTOFFS.'):
            self.assertIn(text,output)
        self.assertNotIn('NORMAL BELL',output)

    def test_t_curve_labels_df_without_claiming_unit_sd(self):
        output,_=flow(lambda:STTPROB.t_probability_session(5,'1'),['-2'])
        self.assertIn('df=5.0000',output)
        self.assertIn('SHADE LEFT OF CUTOFF.',output)
        self.assertNotIn('SD=1',output)

    def test_confidence_interval_has_number_line_and_critical_curve(self):
        with patch.object(c,'view') as view:
            STCIIO._show_result('CI',10,1,2,(8,12),.95,df=9)
        lines=view.call_args.args[1]
        for text in ('LEFT END=8.0000','CENTER ESTIMATE=10.0000',
                     'RIGHT END=12.0000','CRITICAL-VALUE CURVE: t',
                     'EACH OUTSIDE TAIL=0.0250'):
            self.assertIn(text,lines)

    def test_discrete_open_and_closed_endpoints_remain_explicit(self):
        output,_=flow(lambda:STBINOM2.binomial_session(8,(1,2)),
                      ['1','6','2','5','2','0','0'])
        self.assertIn('HOW TO DRAW: PROBABILITY BARS',output)
        self.assertIn('SHADE ONLY BARS MATCHING:',output)
        self.assertIn('(2, 5)',output)
        self.assertIn('PARENTHESES EXCLUDE ENDPOINTS.',output)

    def test_final_table_page_includes_drawing_and_back_navigation(self):
        views=[]
        def view(title,lines):
            views.append(lines)
        with patch.object(c,'view',side_effect=view), \
             patch.object(c,'menu',side_effect=['N','P','0']):
            STVRES.paged_results('TABLE',9,lambda i:(str(i),i),
                                 drawing=['HOW TO DRAW: TEST'])
        self.assertNotIn('HOW TO DRAW: TEST',views[0])
        self.assertIn('HOW TO DRAW: TEST',views[1])
        self.assertNotIn('HOW TO DRAW: TEST',views[2])
