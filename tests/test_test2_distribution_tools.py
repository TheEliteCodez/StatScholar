import unittest
from unittest.mock import patch

import STCI as ci
import STCORE as c
import STDIST as distributions
import STCLT as clt
import STTASKS as tasks
import STSTUDY as study
import STSTU2 as concepts
from test_expansion import flow


class TestTwoDistributionTools(unittest.TestCase):
    def test_normal_individual_tail_and_expected_count(self):
        output, _ = flow(distributions.normal_menu, ['1', '9.3', '2', '2', '10', '100', '0'])
        self.assertIn('P(X > 10.0000)', output)
        self.assertIn('PROBABILITY=0.363169', output)
        self.assertIn('EXPECTED NUMBER=36.3169', output)

    def test_expected_count_for_washing_machine_lifetime_question(self):
        output, _ = flow(distributions.normal_menu, ['1', '9.3', '2', '2', '5', '100', '0'])
        self.assertIn('P(X > 5.0000)', output)
        self.assertIn('EXPECTED NUMBER=98.4222', output)

    def test_lumber_piece_tail_probability(self):
        output, _ = flow(distributions.normal_menu, ['1', '4', '.05', '2', '4.08', '', '0'])
        self.assertIn('P(X > 4.0800)', output)
        self.assertIn('PROBABILITY=0.054799', output)

    def test_pencil_diameter_tail_returns_expected_count(self):
        output, _ = flow(distributions.normal_menu, ['1', '.30', '.01', '1', '.293', '450', '0'])
        self.assertIn('P(X < 0.2930)', output)
        self.assertIn('EXPECTED COUNT=N*P', output)
        self.assertIn('EXPECTED NUMBER=108.8836', output)

    def test_normal_extreme_upper_tail_retains_precision(self):
        probability=clt.normal_sf(6.4)
        self.assertGreater(probability,0)
        output, _ = flow(clt.clt_menu, [
            '2', 'lumber width', '4', '.05', '16', '1', '', '1',
            '2', '4.08', '0'])
        self.assertIn('z=(cutoff-mean)/SE=6.4000', output)
        self.assertIn('P(ABOVE)=%.6e' % probability, output)

    def test_normal_cutoff_from_left_tail_percentile(self):
        output, _ = flow(distributions.normal_menu, ['2', '200', '50', '3', '70%', '0'])
        self.assertIn('AREA TO LEFT=0.7000 (70.00%)', output)
        self.assertIn('z CUTOFF=0.5244', output)
        self.assertIn('VALUE CUTOFF x=226.2200', output)

    def test_uniform_mean_sd_and_between_probability(self):
        output, _ = flow(distributions.uniform_menu, ['3', '0', '20', '0'])
        self.assertIn('MEAN=(a+b)/2=10.0000', output)
        self.assertIn('SD=(b-a)/sqrt(12)=5.7735', output)
        output, _ = flow(distributions.uniform_menu, ['1', '0', '20', '3', '2.8', '6.4', '0'])
        self.assertIn('P(2.8000 < X < 6.4000)', output)
        self.assertIn('PROBABILITY=0.180000', output)

    def test_uniform_upper_tail_and_percentile_cutoff(self):
        output, _ = flow(distributions.uniform_menu, ['1', '0', '20', '2', '9', '0'])
        self.assertIn('PROBABILITY=0.550000', output)
        output, _ = flow(distributions.uniform_menu, ['2', '0', '20', '3', '70%', '0'])
        self.assertIn('VALUE CUTOFF x=14.0000', output)

    def test_t_critical_probability_and_percentile(self):
        self.assertAlmostEqual(ci.t_critical(.99, 6), 3.7074280213, places=7)
        self.assertAlmostEqual(ci.t_cdf(2.1314495456, 15), .975, places=7)
        self.assertAlmostEqual(ci.t_quantile(.05, 15), -1.7530503557, places=7)
        output, _ = flow(distributions.t_menu, [
            '2', '15', '1', '2.1314495456', '0'])
        self.assertIn('P(T < 2.1314)', output)
        self.assertIn('PROBABILITY=0.9750000', output)

    def test_t_critical_menu_and_two_tail_cutoffs(self):
        output, _ = flow(distributions.t_menu, ['1', '99%', '6', '0', '0'])
        self.assertIn('CRITICAL VALUES=+/-3.707428', output)
        output, _ = flow(distributions.t_menu, [
            '3', '15', '3', '5%', '0'])
        self.assertIn('t CUTOFF=-1.753050', output)
        output, _ = flow(distributions.t_menu, [
            '2', '15', '3', '-2.1314495456', '2.1314495456', '0'])
        self.assertIn('P(-2.1314 < T < 2.1314)', output)
        self.assertIn('PROBABILITY=0.9500000', output)

    def test_practice_test2_sample_mean_probabilities(self):
        cases=[
            (['2','washer life','9.3','2','9','1','','1','2','10','0'],
             'P(ABOVE)=0.146859'),
            (['2','loan score','200','50','40','1','','3','2','215','0'],
             'P(ABOVE)=0.028890'),
            (['2','uniform sample','0.5','0.289','50','1','','3','1','0.3','0'],
             'P(BELOW)=%.6e' % clt.normal_cdf(
                 (0.3-0.5)/clt.mean_standard_error(.289,50))),
            (['2','normal SAT score','430','120','15','1','','1','2','500','0'],
             'P(ABOVE)=0.011934'),
            (['4','odd proportion','0.5','800','1','','1','.49','0'],
             'P(BELOW)=0.285'),
            (['2','random digit mean','4.5','2.872281323','800','1','','3','2','4.6','0'],
             'P(ABOVE)=0.162'),
        ]
        for inputs, expected in cases:
            with self.subTest(inputs=inputs):
                output, _ = flow(clt.clt_menu, inputs)
                self.assertIn(expected, output)

    def test_clt_refuses_small_uniform_sample_approximation(self):
        output, _ = flow(clt.clt_menu, [
            '2','uniform generator','0.5','0.289','15','1','','2','0','0'])
        self.assertIn('FAIL: NONNORMAL POPULATION AND n < 30', output)
        self.assertIn('NORMAL PROBABILITY NOT CALCULATED', output)

    def test_confidence_tools_accept_decimal_proportion_and_center_moe(self):
        output, _ = flow(ci.confidence_menu, [
            '10', 'voter registration', '.67', '168', '95%', '0'])
        self.assertIn('INPUT CHECK: p-hat=0.6700; n=168 TOTAL', output)
        self.assertIn('MARGIN OF ERROR=0.0711', output)
        self.assertIn('INTERVAL=(0.5989, 0.7411)', output)
        output, _ = flow(ci.confidence_menu, [
            '11', '1', '.60', '.046', '0'])
        self.assertIn('INTERVAL=(0.5540, 0.6460)', output)
        output, _ = flow(ci.confidence_menu, [
            '11','1','.02','.05','0'])
        self.assertIn('EXTEND OUTSIDE [0,1]; NOT CLAMPED.', output)

    def test_interval_from_estimate_rejects_negative_margin(self):
        with self.assertRaisesRegex(ValueError, 'MARGIN OF ERROR MUST NOT BE NEGATIVE'):
            flow(ci.confidence_menu, ['11', '1', '.60', '-.01', '0'])

    def test_confidence_mean_summary_checks_optional_reference(self):
        output, _ = flow(ci.confidence_menu, [
            '3', '1', '218', '11', '40', '95%', '220', '0'])
        self.assertIn('ONE-MEAN CLAIM CHECK', output)
        self.assertIn('REFERENCE IS INSIDE THE CI.', output)
        self.assertIn('INTERVAL INCLUSION DOES NOT PROVE THE CLAIM TRUE.', output)
        output, _ = flow(ci.confidence_menu, [
            '3', '1', '218', '11', '40', '95%', '230', '0'])
        self.assertIn('REFERENCE IS OUTSIDE THE CI.', output)

    def test_mean_ci_can_compare_original_data_with_verified_omission(self):
        output, _ = flow(ci.confidence_menu, [
            '13', 'sample measurement', '5', '1', '2', '3', '4', '100',
            '95%', '100', '0'])
        self.assertIn('WITH ALL DATA: n=5; x-bar=22.0000', output)
        self.assertIn('OMITTED ONE RECORDED VALUE: 100', output)
        self.assertIn('WITHOUT THAT VALUE: n=4; x-bar=2.5000', output)
        self.assertIn('VERIFY THE VALUE IS A REAL OUTLIER', output)

    def test_practice_test2_proportion_interval_uses_exact_success_count(self):
        output, _ = flow(ci.confidence_menu, [
            '1', '594', '1100', '95%', '0'])
        self.assertIn('INPUT CHECK: x=594 WITH EVENT; n=1100 TOTAL', output)
        self.assertIn('p-hat=0.5400', output)
        self.assertIn('INTERVAL=(0.5105, 0.5695)', output)

    def test_proportion_margin_error_can_use_decimal_estimate(self):
        output, _ = flow(ci.zstar_menu, [
            '3', '3', '95%', '.67', '168', '0'])
        self.assertIn('p-hat=0.6700', output)
        self.assertIn('MARGIN OF ERROR=0.0711', output)

    def test_z_critical_value_from_upper_tail_area(self):
        output, _ = flow(ci.zstar_menu, ['5', '.005', '0'])
        self.assertIn('z*=2.575829', output)

    def test_confidence_menu_opens_student_t_distribution_tools(self):
        with patch.object(c,'call') as dispatch, \
                patch.object(c,'menu',side_effect=['9','0']):
            ci.confidence_menu()
        dispatch.assert_called_once_with('STDIST','t_menu')

    def test_qq_plot_values_offer_multiple_position_conventions(self):
        values=[c.as_ratio('1'),c.as_ratio('2'),c.as_ratio('3')]
        output, _ = flow(
            lambda:distributions.normal_probability_plot(values), ['2', '1'])
        self.assertIn('QQ PLOT > HAZEN ORDERED PAIRS', output)
        self.assertIn('normal z=-0.9674', output)
        self.assertIn('normal z=0.0000', output)
        self.assertNotIn('NORMALITY=PASS', output)

    def test_test2_concepts_include_estimator_bias_and_t_assumptions(self):
        with patch.object(concepts, 'definition_pages') as show, \
                patch.object(c, 'menu', side_effect=['5', '8', '0']):
            concepts.test2_concepts()
        self.assertIn('SAMPLE SD s IS BIASED FOR sigma', show.call_args_list[0].args[1])
        self.assertIn('APPROXIMATELY NORMAL', show.call_args_list[1].args[1])

    def test_test2_concept_explains_sample_statistic_and_count(self):
        with patch.object(concepts, 'definition_pages') as show, \
                patch.object(c, 'menu', side_effect=['3', '0']):
            concepts.test2_concepts()
        self.assertIn('SAMPLE STATISTIC', show.call_args.args[1])
        self.assertIn('0.54*1100=594', show.call_args.args[1])

    def test_home_routes_to_normal_and_uniform_tools(self):
        import STHOME
        for key,module,func in [('1','STNDIST','normal_menu'),('7','STUNIF','uniform_menu')]:
            with patch.object(c,'menu',side_effect=[key,'0']), patch.object(c,'call') as dispatch:
                STHOME.quick_main()
            dispatch.assert_called_once_with(module,func)

    def test_study_menu_routes_to_test2_concepts(self):
            with patch.object(c, 'menu', side_effect=['9', '0']), \
                    patch.object(c, 'call') as dispatch:
                study.study_menu()
            dispatch.assert_called_once_with('STSTU2','test2_concepts')


if __name__ == '__main__':
    unittest.main()
