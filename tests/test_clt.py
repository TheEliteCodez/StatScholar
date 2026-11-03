import unittest
from unittest.mock import patch

import STCORE as c
import STCLT as clt
import STHOME as home
from test_expansion import flow


class CentralLimitTheorem(unittest.TestCase):
    def test_washing_machine_drawing_uses_entered_numbers(self):
        output,_ = flow(clt.clt_menu,[
            '2','','9.3','2','9','1','','1','2','10','0'])
        for expected in ('HOW TO DRAW: x-bar','CENTER / MEAN: 9.3000',
                         'SD / TICK SPACING: 0.6667','+1 SD: 9.9667',
                         'MARK CUTOFF: 10.0000','SHADE RIGHT OF CUTOFF.',
                         'CENTER=0; SD=1','INDIVIDUAL SD: 2.0000',
                         'P(ABOVE)=0.146859'):
            self.assertIn(expected,output)

    def test_drawing_shades_lower_tail_and_between_bounds(self):
        for event,bounds,expected in (
                ('1',['8'],'SHADE LEFT OF CUTOFF.'),
                ('3',['8','10'],'SHADE BETWEEN THE CUTOFFS.')):
            output,_ = flow(clt.clt_menu,[
                '2','','9.3','2','9','1','','1',event]+bounds+['0'])
            self.assertIn(expected,output)

    def test_standard_normal_cdf(self):
        self.assertAlmostEqual(clt.normal_cdf(0),.5,places=7)
        self.assertAlmostEqual(clt.normal_cdf(1.96),.975,places=4)
        self.assertAlmostEqual(clt.normal_cdf(-1.96),.025,places=4)

    def test_sample_mean_distribution_and_upper_tail(self):
        output,_ = flow(clt.clt_menu,[
            '2','','100','15','36','1','','2','2','105','0'])
        self.assertIn('CLT > SAMPLE MEAN',output)
        self.assertIn('INPUT CHECK: n=36; mu=100.0000; SE=2.5000',output)
        self.assertIn('APPROXIMATELY NORMAL BY CLT',output)
        self.assertIn('SE=sigma/sqrt(n)=15.0000/sqrt(36)=2.5000',output)
        self.assertIn('z=(cutoff-mean)/SE=(105-100)/2.5=2.0000',output)
        self.assertIn('P(ABOVE)=0.022750',output)

    def test_sample_proportion_distribution_and_between_probability(self):
        output,_ = flow(clt.clt_menu,[
            '4','','0.2','100','1','','3','0.15','0.25','0'])
        self.assertIn('CLT > SAMPLE PROPORTION',output)
        self.assertIn('INPUT CHECK: n=100; p=0.2000; SE=0.0400',output)
        self.assertIn('SUCCESS / FAILURE: PASS: np=20.00 AND n(1-p)=80.00 >= 10',output)
        self.assertIn('z lower=(0.15-0.2)/0.04=-1.2500; z upper=(0.25-0.2)/0.04=1.2500',output)
        self.assertIn('P(BETWEEN)=0.788700',output)

    def test_small_n_unknown_shape_does_not_offer_normal_probability(self):
        output,_ = flow(clt.clt_menu,[
            '2','','50','10','12','1','','3','0','0'])
        self.assertIn('VERIFY: POPULATION SHAPE UNKNOWN AND n < 30',output)
        self.assertIn('NORMAL PROBABILITY NOT CALCULATED',output)
        self.assertNotIn('CLT > RESULT',output)

    def test_large_sampling_fraction_applies_finite_population_correction(self):
        output,_ = flow(clt.clt_menu,[
            '1','','50','2','10','1','100','1','0'])
        self.assertIn('5% POPULATION CONDITION: FAIL; FINITE CORRECTION APPLIED',output)
        self.assertIn('FINITE POPULATION CORRECTION APPLIED',output)
        self.assertIn('SD OF x-bar=SE=0.6030',output)

    def test_home_menu_routes_to_clt_menu(self):
        context = {
            'GUIDES':(),
            'QUESTION_INDEX':(),
            'question_lookup':lambda key:None,
            'launch_route':lambda key:None}
        with patch.object(c,'menu',side_effect=['9','0']), \
             patch.object(c,'call') as dispatch:
            home.quick_main()
        dispatch.assert_called_once_with('STCLT','clt_menu')

    def test_clt_is_a_home_menu_choice_on_second_page(self):
        context = {'GUIDES':(), 'QUESTION_INDEX':()}
        with patch.object(c,'menu',return_value='0') as menu:
            home.quick_main()
        args,kwargs = menu.call_args
        choices = args[1]
        self.assertIn(('9','CLT / SAMPLING DISTRIBUTIONS'),choices)
        self.assertEqual(kwargs.get('page_size'),6)

    def test_invalid_parameter_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            clt.mean_standard_error(-1,10)
        with self.assertRaises(ValueError):
            clt.proportion_standard_error(1.2,10)
        with self.assertRaises(ValueError):
            clt.proportion_standard_error(.5,0)


if __name__ == '__main__':
    unittest.main()


class CLTImportPath(unittest.TestCase):
    def test_home_menu_defers_workflow_imports(self):
        import subprocess, sys
        code = """
import sys, builtins
original = builtins.__import__
def guarded(name, *args, **kwargs):
    if name in ('STCLT1','STCLT2','STCLTC','STCLTR','STCI'):
        raise AssertionError('CLT menu eagerly loaded '+name)
    return original(name, *args, **kwargs)
builtins.__import__ = guarded
import STAT1, STCORE
answers = iter(['9','0','0'])
builtins.input = lambda prompt='': next(answers)
STAT1.main()
assert 'STCLT' not in sys.modules
assert 'STCLTM' not in sys.modules
"""
        run = subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
