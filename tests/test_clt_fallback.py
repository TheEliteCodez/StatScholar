from fractions import Fraction
from itertools import product
from math import comb
import unittest
from unittest.mock import patch
import STCORE as c
import STCLT
import STCLTF as exact
from test_expansion import flow


class ExactSamplingFallback(unittest.TestCase):
    def test_small_proportion_uses_binomial_and_strict_cutoff(self):
        output,_=flow(STCLT.clt_menu,
            ['4','','.1','5','1','','2','.2','0','0'])
        self.assertIn('EXACT BINOMIAL',output)
        self.assertIn('P=0.0815',output)
        self.assertIn('X > 1',output)
        self.assertNotIn('DRAW A SYMMETRIC BELL',output)

    def test_fraction_cutoff_is_not_rounded_before_count_conversion(self):
        with patch.object(c,'results') as result,patch.object(c,'view'), \
             patch.object(c,'menu',return_value='2'), \
             patch.object(c,'read_exact',return_value=(1,3)):
            exact.proportion_fallback((1,3),3,'PASS',None)
        self.assertEqual(result.call_args.args[1][0],('P',(7,27)))

    def test_finite_sampling_switches_to_hypergeometric(self):
        output,_=flow(STCLT.clt_menu,
            ['4','','.1','5','1','20','2','2','.2','0','0'])
        self.assertIn('EXACT HYPERGEOMETRIC',output)
        self.assertIn('N=20; K=2; n=5',output)
        self.assertIn('P=0.0526',output)

    def test_failure_of_independence_does_not_silently_assume_binomial(self):
        output,_=flow(STCLT.clt_menu,
            ['4','','.1','5','2','','3','0'])
        self.assertIn('NEED THEIR JOINT DISTRIBUTION',output)
        self.assertNotIn('EXACT BINOMIAL',output)

    def test_small_normal_population_still_uses_normal_method(self):
        output,_=flow(STCLT.clt_menu,
            ['2','','9.3','2','9','1','','1','2','10','0'])
        self.assertIn('P(ABOVE)=0.146859',output)
        self.assertNotIn('SWITCH TO EXACT',output)

    def test_small_uniform_mean_uses_sum_of_uniforms(self):
        output,_=flow(STCLT.clt_menu,
            ['2','','.5','.288675','2','1','','2','1','0','1','2','.75','0','0'])
        self.assertIn('EXACT MEAN OF 2 INDEPENDENT UNIFORMS',output)
        self.assertIn('P=0.1250',output)
        self.assertIn('n=2: TRIANGLE',output)

    def test_uniform_cdf_exact_boundaries_and_symmetry(self):
        for n in (1,2,3,9,29):
            for x in (Fraction(-1),Fraction(0),Fraction(1,4),Fraction(1,2),Fraction(3,4),Fraction(1),Fraction(2)):
                actual=Fraction(*exact.uniform_cdf((x.numerator,x.denominator),(0,1),(1,1),n))
                reflected=Fraction(*exact.uniform_cdf(((1-x).numerator,(1-x).denominator),(0,1),(1,1),n))
                self.assertGreaterEqual(actual,0)
                self.assertLessEqual(actual,1)
                self.assertEqual(actual+reflected,1)
        self.assertEqual(exact.uniform_cdf((1,4),(0,1),(1,1),2),(1,8))

    def test_discrete_mean_agrees_with_enumerating_all_samples(self):
        population=[0,0,3]
        expected=Fraction(sum(sum(sample)>3 for sample in product(population,repeat=3)),27)
        with patch.object(c,'menu',side_effect=['2','2']), \
             patch.object(c,'read_exact',return_value=(1,1)), \
             patch.object(c,'view'),patch.object(c,'results') as result, \
             patch.object(c,'paged_results'), \
             patch('STCOUNT2.read_distribution',return_value=([((0,1),(2,3)),((3,1),(1,3))],False)):
            exact.mean_fallback(1,2**.5,3,'PASS',None)
        self.assertEqual(Fraction(*result.call_args.args[1][0][1]),expected)

    def test_without_replacement_mean_uses_all_population_values(self):
        output,_=flow(STCLT.clt_menu,
            ['2','','1','1','2','2','3','2','2','3','0','0','3','2','1','0','0','0'])
        self.assertIn('RANDOM WITHOUT REPLACEMENT',output)
        self.assertIn('P=0.6667',output)

    def test_only_moments_cannot_determine_small_sample_probability(self):
        output,_=flow(STCLT.clt_menu,
            ['2','','50','10','12','1','','3','3','0'])
        self.assertIn('MEAN AND SD DO NOT DETERMINE',output)
        self.assertNotIn('t PROBABILITY',output)

    def test_large_sampling_fraction_routes_even_when_count_check_passes(self):
        expected=sum(Fraction(comb(50,k)*comb(50,50-k),comb(100,50)) for k in range(26,51))
        with patch.object(c,'menu',side_effect=['2','2']), \
             patch.object(c,'read_exact',return_value=(1,2)), \
             patch.object(c,'view'),patch.object(c,'results') as result:
            exact.proportion_fallback((1,2),50,'PASS',100)
        self.assertEqual(Fraction(*result.call_args.args[1][0][1]),expected)

    def test_full_population_sample_is_point_mass_at_population_mean(self):
        output,_=flow(STCLT.clt_menu,
            ['2','','9.3','2','9','1','9','1','2','2','10','0','0'])
        self.assertIn('EXACT CENSUS MEAN',output)
        self.assertIn('P=0.0000',output)
        self.assertIn('ONE POINT AT mu',output)

    def test_confirmed_replacement_removes_finite_correction_for_normal_mean(self):
        output,_=flow(STCLT.clt_menu,
            ['2','','9.3','2','9','1','20','1','1','2','10','0'])
        self.assertIn('CONFIRMED INDEPENDENT / WITH REPLACEMENT',output)
        self.assertIn('SD OF x-bar=SE=0.6667',output)
        self.assertIn('P(ABOVE)=0.146859',output)
