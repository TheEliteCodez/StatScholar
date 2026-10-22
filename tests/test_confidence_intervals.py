import unittest
from unittest.mock import patch

import STCORE as c
import STCI as ci
from test_expansion import flow


class ConfidenceIntervals(unittest.TestCase):
    def test_critical_values(self):
        self.assertAlmostEqual(ci.z_critical(.95),1.9599639845,places=7)
        self.assertAlmostEqual(ci.t_critical(.95,9),2.2621571628,places=7)
        self.assertAlmostEqual(ci.t_critical(.95,1),12.7062047364,places=7)

    def test_proportion_intervals(self):
        estimate,se,critical,interval = ci.one_proportion(50,100,.95)
        self.assertEqual((estimate,se),(0.5,0.05))
        self.assertAlmostEqual(interval[0],.4020018,places=6)
        self.assertAlmostEqual(interval[1],.5979982,places=6)
        difference,se,critical,interval = ci.two_proportions(60,100,50,100,.95)
        self.assertAlmostEqual(difference,.1)
        self.assertAlmostEqual(se,.07,places=8)
        self.assertAlmostEqual(interval[0],-.0371975,places=6)
        self.assertAlmostEqual(interval[1],.2371975,places=6)
        estimate,se,critical,margin = ci.proportion_margin_error(50,100,.95)
        self.assertEqual(estimate,.5)
        self.assertAlmostEqual(margin,.0979982,places=6)

    def test_panic_proportion_checks_and_example(self):
        result = ci.panic_proportion(382,1880,.96)
        self.assertTrue(result['success_ok'])
        self.assertTrue(result['failure_ok'])
        self.assertTrue(result['independence_ok'])
        self.assertEqual(result['failures'],1498)
        self.assertAlmostEqual(result['estimate'],382/1880)
        self.assertAlmostEqual(result['interval'][0],.18414,places=4)
        self.assertAlmostEqual(result['interval'][1],.22224,places=4)
        output,prompts = flow(ci.confidence_menu,[
            '6','identity theft complaints in this state','382','1880','96%','','1','73%','0'])
        self.assertIn('p-hat = 191/940 = 0.2032',output)
        self.assertIn('FAILURE: 1498 >= 10: PASS',output)
        self.assertIn('96.0% CI = (0.184, 0.222)',output)
        self.assertIn('RANDOM SAMPLE: PASS',output)
        self.assertIn('MOE=2.0537*sqrt(0.2032*0.7968/1880)=0.0191',output)
        self.assertIn('CLAIM 0.730 IS OUTSIDE THE INTERVAL.',output)
        self.assertIn('POPULATION SIZE N (ENTER=1000000): ',prompts)

    def test_panic_mean_raw_data_solves_frog_worksheet(self):
        frogs = [138,125,128,119,133,125,119,117,78,93,98,113,91,119,107,89,105,107,88,143]
        inputs = ['7','frog weight in this region','20']+[str(v) for v in frogs]+['96%','118','5','1','1','0']
        output,prompts = flow(ci.confidence_menu,inputs)
        self.assertIn('ONE-SAMPLE STUDENT t INTERVAL; df=19',output)
        self.assertIn('x-bar=111.7500; SE=4.0399',output)
        self.assertIn('t*=2.2047; MOE=t*s/sqrt(n)=8.9067',output)
        self.assertIn('MOE=2.2047*18.0668/sqrt(20)=8.9067',output)
        self.assertIn('TAIL AREAS=0.020 EACH; t=+/-2.2047',output)
        self.assertIn('CI=(102.843, 120.657)',output)
        self.assertIn('REFERENCE MEAN 118.000 IS INSIDE THE CI.',output)
        self.assertIn('ROUND UP TO 56',output)
        self.assertIn('z*=2.0537; SUBSTITUTE: (z* 18.0668 / 5.0000)^2',output)
        self.assertIn('NO EVIDENCE OF A DIFFERENCE FROM THE REFERENCE MEAN AT 96.0%.',output)
        self.assertIn('SORTED DATA: 78,88,89,91,93,98',output)
        self.assertIn('VALUE 20: ',prompts)

    def test_panic_proportion_quiz8_inputs_and_98_percent_outputs(self):
        output,_ = flow(ci.confidence_menu,[
            '6','registration among this professor students','30','50','98%','7000','1','.73','0'])
        self.assertIn('SAMPLE: 50 OBSERVATIONS',output)
        self.assertIn('SUCCESS: 30 >= 10: PASS',output)
        self.assertIn('FAILURE: 20 >= 10: PASS',output)
        self.assertIn('INDEPENDENCE: n/N <= 0.05: PASS',output)
        self.assertIn('alpha=0.0200; z*=2.3263',output)
        self.assertIn('MOE=2.3263*sqrt(0.6000*0.4000/50)=0.1612',output)
        self.assertIn('98.0% CI = (0.439, 0.761)',output)
        self.assertIn('CLAIM 0.730 IS INSIDE THE INTERVAL.',output)

    def test_method_selector_routes_by_response_and_sample_count(self):
        with patch.object(ci,'panic_one_proportion') as solver, \
             patch.object(c,'menu',side_effect=['1','1','1']):
            ci.choose_confidence_method()
        solver.assert_called_once_with()
        with patch.object(ci,'panic_two_proportions') as solver, \
             patch.object(c,'menu',side_effect=['1','1','2']):
            ci.choose_confidence_method()
        solver.assert_called_once_with()
        with patch.object(ci,'panic_one_mean') as solver, \
             patch.object(c,'menu',side_effect=['1','2','1']):
            ci.choose_confidence_method()
        solver.assert_called_once_with()
        with patch.object(ci,'panic_two_means') as solver, \
             patch.object(c,'menu',side_effect=['1','2','2']):
            ci.choose_confidence_method()
        solver.assert_called_once_with()

    def test_guided_given_interval_interpretation(self):
        output,_ = flow(ci.choose_confidence_method,[
            '2','2','mean height of basketball players','70','75','95%'])
        self.assertIn('POINT ESTIMATE / CENTER=72.5000',output)
        self.assertIn('MARGIN OF ERROR=2.5000',output)
        self.assertIn('95.0% CONFIDENT THE mean height of basketball players IS BETWEEN 70.0000 AND 75.0000.',output)

    def test_guided_margin_error_and_sample_size_route_to_existing_tools(self):
        with patch.object(ci,'_margin_error') as solver, \
             patch.object(c,'menu',return_value='3'):
            ci.choose_confidence_method()
        solver.assert_called_once_with()
        with patch.object(ci,'_required_sample_size') as solver, \
             patch.object(c,'menu',return_value='4'):
            ci.choose_confidence_method()
        solver.assert_called_once_with()

    def test_confidence_menu_opens_guided_solver(self):
        with patch.object(ci,'choose_confidence_method') as solver:
            flow(ci.confidence_menu,['8','0'])
        solver.assert_called_once_with()

    def test_guided_two_proportion_panic_outputs_full_solution(self):
        output,_ = flow(ci.choose_confidence_method,[
            '1','1','2','registration rate, group 1 minus group 2',
            '60','100','10000','50','100','10000','95%','1'])
        self.assertIn('PANIC: TWO PROPORTIONS',output)
        self.assertIn('INPUT CHECK: GROUP 1 60/100; GROUP 2 50/100',output)
        self.assertIn('INTERVAL DIRECTION: p1 - p2',output)
        self.assertIn('INDEPENDENT RANDOM SAMPLES: PASS',output)
        self.assertIn('SUCCESS/FAILURE COUNTS EACH >= 10: PASS',output)
        self.assertIn('TWO-PROPORTION z INTERVAL',output)
        self.assertIn('CI=(-0.037, 0.237)',output)

    def test_guided_two_mean_panic_outputs_assumptions_and_interval(self):
        output,_ = flow(ci.choose_confidence_method,[
            '1','2','2','mean in group 1 minus group 2',
            '1','10','2','25','1','8','3','30','95%','1','1','1'])
        self.assertIn('PANIC: TWO MEANS',output)
        self.assertIn('GROUP 1 x-bar=10.0000, s=2.0000, n=25',output)
        self.assertIn('INTERVAL DIRECTION: GROUP 1 - GROUP 2',output)
        self.assertIn('RANDOM SAMPLES: PASS; INDEPENDENT GROUPS: PASS',output)
        self.assertIn('TWO-INDEPENDENT-SAMPLE t INTERVAL (WELCH)',output)
        self.assertIn('CI=(0.638, 3.362)',output)

    def test_mean_intervals(self):
        estimate,se,critical,interval = ci.one_mean(10,2,25,.95)
        self.assertEqual(estimate,10)
        self.assertAlmostEqual(critical,2.06389855,places=6)
        self.assertAlmostEqual(interval[0],9.17444058,places=6)
        difference,se,critical,degrees,interval = ci.two_means(10,2,25,8,3,30,.95)
        self.assertAlmostEqual(difference,2)
        self.assertAlmostEqual(degrees,50.7420066,places=5)
        self.assertAlmostEqual(interval[0],.63822236,places=6)
        self.assertAlmostEqual(interval[1],3.36177764,places=6)
        se,critical,margin = ci.mean_margin_error(10,100,.95)
        self.assertEqual(se,1)
        self.assertAlmostEqual(margin,1.9599639845,places=7)

    def test_zstar_reverse_and_sample_size(self):
        self.assertAlmostEqual(ci.confidence_from_z(1.9599639845),.95,places=6)
        self.assertAlmostEqual(ci.proportion_sample_size(.5,.05,.95),384.145882,places=4)
        self.assertEqual(int(ci.math.ceil(ci.proportion_sample_size(.5,.05,.95))),385)
        self.assertAlmostEqual(ci.mean_sample_size(10,2,.95),96.036,places=2)

    def test_invalid_inputs_are_reported(self):
        with self.assertRaises(ValueError):
            ci.one_proportion(11,10,.95)
        with self.assertRaises(ValueError):
            ci.one_mean(5,1,1,.95)
        with self.assertRaises(ValueError):
            ci.z_critical(1)

    def test_confidence_interval_menu_calculates_from_counts(self):
        output,prompts = flow(ci.confidence_menu,['1','60','100','95%','0'])
        self.assertIn('ONE-PROPORTION z INTERVAL',output)
        self.assertIn('INTERVAL=(0.5040, 0.6960)',output)
        self.assertIn('INPUT CHECK: x=60 WITH EVENT; n=100 TOTAL',output)
        self.assertIn('NUMBER WITH EVENT (successes x): ',prompts)
        self.assertIn('TOTAL NUMBER SAMPLED (n): ',prompts)
        self.assertIn('CONFIDENCE LEVEL (E.G. 95%): ',prompts)


    def test_zstar_menu_calculates_lookup_and_required_n(self):
        output,_ = flow(ci.zstar_menu,['1','95%','0'])
        self.assertIn('z*=1.9600',output)
        output,_ = flow(ci.zstar_menu,['2','1.96','0'])
        self.assertIn('CONFIDENCE=95.00%',output)
        output,_ = flow(ci.zstar_menu,['4','1','95%','.5','.05','0'])
        self.assertIn('ROUND UP: n=385',output)
        self.assertIn('SUBSTITUTE: (1.9600^2*0.5000*0.5000)/0.0500^2',output)
        output,_ = flow(ci.zstar_menu,['4','2','98%','10','5','0'])
        self.assertIn('ROUND UP: n=22',output)
        output,_ = flow(ci.zstar_menu,['4','1','98%','.73','.05','0'])
        self.assertIn('ROUND UP: n=427',output)
        self.assertIn('CHECK AT n: APPROX E=0.0500',output)


if __name__ == '__main__':
    unittest.main()


class EasySampleSize(unittest.TestCase):
    def test_home_unknown_proportion_rounds_up(self):
        import STAT1
        output,_ = flow(STAT1.main,['10','1','95%','','5%','0'])
        self.assertIn('ROUND UP: n=385',output)
        self.assertIn('UNROUNDED n=384.1459',output)

    def test_changed_estimate_and_mean(self):
        output,_ = flow(ci._required_sample_size,['1','95%','20%','4%'])
        self.assertIn('ROUND UP: n=385',output)
        output,_ = flow(ci._required_sample_size,['2','95%','10','2'])
        self.assertIn('ROUND UP: n=97',output)
        self.assertIn('n IS APPROXIMATE',output)

    def test_zero_variation_still_requests_one_observation(self):
        output,_ = flow(ci._required_sample_size,['2','95%','0','2'])
        self.assertIn('ROUND UP: n=1',output)


class SampleSizeMemoryPath(unittest.TestCase):
    def test_home_sample_size_does_not_import_confidence_module(self):
        import subprocess, sys
        code = """
import builtins, sys
original = builtins.__import__
def guarded(name, *args, **kwargs):
    if name == 'STCI':
        raise AssertionError('Sample size must not load STCI')
    return original(name, *args, **kwargs)
builtins.__import__ = guarded
import STAT1, STCORE
answers = iter(['10','1','95%','','5%','0'])
builtins.input = lambda prompt='': next(answers)
results = []
STCORE.view = lambda title, lines: results.extend(lines)
STAT1.main()
assert 'ROUND UP: n=385' in results, results
assert 'STCI' not in sys.modules
assert 'STSIZE' not in sys.modules
assert 'STZCRIT' not in sys.modules
"""
        run = subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)


class DirectConfidenceMenu(unittest.TestCase):
    def test_home_interval_and_margin_without_monolith(self):
        import subprocess, sys
        code = """
import builtins, sys
original = builtins.__import__
def guarded(name, *args, **kwargs):
    if name == 'STCI':
        raise AssertionError('Home CI menu must not load STCI')
    return original(name, *args, **kwargs)
builtins.__import__ = guarded
import STAT1, STCORE
answers = iter(['11','1','60','100','95%','6','1','95%','60','100','0','0'])
builtins.input = lambda prompt='': next(answers)
lines = []
STCORE.view = lambda title, values: lines.extend(values)
STAT1.main()
assert 'INTERVAL=(0.5040, 0.6960)' in lines, lines
assert 'MARGIN OF ERROR=0.0960' in lines, lines
assert 'STCI' not in sys.modules
assert 'STCIMENU' not in sys.modules
"""
        run = subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
