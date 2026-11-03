import unittest
from test_expansion import flow
import STHOME
import STTDIST


class CriticalInputs(unittest.TestCase):
    def test_estimate_and_se_produce_margin_interval_and_work(self):
        output,_=flow(STHOME.quick_main,['13','1','95%','1','100','3','0'])
        for text in ('POINT ESTIMATE=100.000000','MARGIN OF ERROR E=5.879892',
                     'E=abs(CRITICAL)*SE','ENDS=(94.120108, 105.879892)',
                     'LEFT=(1+C)/2'):
            self.assertIn(text,output)

    def test_interval_endpoints_produce_midpoint_margin_and_se(self):
        output,_=flow(STHOME.quick_main,['13','1','95%','3','.12','.20','0'])
        for text in ('POINT ESTIMATE=0.160000','MARGIN OF ERROR E=0.040000',
                     'STANDARD ERROR=0.020409','POINT ESTIMATE=(LOW+HIGH)/2',
                     'E=(HIGH-LOW)/2'):
            self.assertIn(text,output)

    def test_given_estimate_and_margin_recover_se(self):
        output,_=flow(STHOME.quick_main,['13','1','95%','2','.6','.05','0'])
        self.assertIn('STANDARD ERROR=0.025511',output)
        self.assertIn('ENDS=(0.550000, 0.650000)',output)

    def test_one_sided_uses_bound_instead_of_two_sided_interval(self):
        output,_=flow(STHOME.quick_main,['13','5','95%','2','1','100','3','0'])
        self.assertIn('LOWER ONE-SIDED BOUND',output)
        self.assertIn('BOUND=95.065439',output)
        self.assertNotIn('ENDS=(',output)

    def test_equivalent_inputs_give_same_z_and_t(self):
        methods=[['1','95%'],['2','.05'],['3','.025'],['4','.975'],
                 ['5','.975','2'],['6','.475','2']]
        for home,expected,df in [('13','1.959964',[]),('14','2.262157',['1','9'])]:
            for method in methods:
                with self.subTest(home=home,method=method):
                    output,_=flow(STHOME.quick_main,[home]+method+df+['0','0'])
                    self.assertIn(expected,output)
                    self.assertIn('AREA TO LEFT=0.975000',output)

    def test_lower_cutoffs_are_signed_and_use_left_tail(self):
        for method in (['4','.025'],['5','97.5%','1'],['6','.475','1']):
            output,_=flow(STHOME.quick_main,['13']+method+['0','0'])
            self.assertIn('SIGNED CRITICAL CUTOFF=-1.959964',output)
            self.assertIn('AREA TO LEFT=0.025000',output)

    def test_sample_size_and_direct_df_agree(self):
        for df in (['1','9'],['2','10']):
            output,_=flow(STHOME.quick_main,['14','1','95%']+df+['0','0'])
            self.assertIn('df=9.0000',output)
            self.assertIn('CRITICAL VALUES=+/-2.262157',output)

    def test_fractional_df_is_supported(self):
        output,_=flow(STHOME.quick_main,['14','4','.5','1','8.5','0','0'])
        self.assertIn('df=8.5000',output)
        self.assertIn('SIGNED CRITICAL CUTOFF=0.000000',output)

    def test_shading_matches_requested_area(self):
        for method,shade in [(['1','95%'],'SHADE BETWEEN CUTOFFS.'),
                             (['2','.05'],'SHADE BOTH OUTSIDE TAILS.'),
                             (['3','.025'],'SHADE RIGHT OF CUTOFF.'),
                             (['4','.025'],'SHADE LEFT OF CUTOFF.'),
                             (['6','.475','1'],'SHADE BETWEEN CUTOFFS.')]:
            output,_=flow(STHOME.quick_main,['13']+method+['0','0'])
            self.assertIn(shade,output)

    def test_existing_t_distribution_menu_opens_other_input_methods(self):
        output,_=flow(STTDIST.t_menu,['4','2','5%','2','10','0','0'])
        self.assertIn('CRITICAL VALUES=+/-2.262157',output)

    def test_sample_size_df_rule_is_labeled_for_one_sample_or_pairs(self):
        output,_=flow(STHOME.quick_main,['14','1','95%','2','10','0','0'])
        self.assertIn('ONE-SAMPLE / PAIRED: ENTER n',output)

    def test_one_sided_95_percent_differs_from_two_sided(self):
        output,_=flow(STHOME.quick_main,['13','5','95%','2','0','0'])
        self.assertIn('SIGNED CRITICAL CUTOFF=1.644854',output)
        self.assertIn('ONE-SIDED alpha=0.050000',output)
