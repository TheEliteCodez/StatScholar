import types
import unittest
from unittest.mock import patch,Mock
import STCORE as c
import STDMATH1
import STDATA2
from test_expansion import flow


class CalculatorLists(unittest.TestCase):
    def test_l1_uses_builtin_number_and_keeps_original_order(self):
        original=[3.5,-1,3.5,0]
        recall=Mock(return_value=original)
        with patch.dict('sys.modules',{'ti_system':types.SimpleNamespace(recall_list=recall)}):
            with patch('builtins.input',return_value='L1'):
                values=STDMATH1.read_raw()
        recall.assert_called_once_with('1')
        self.assertEqual(values,[(-1,1),(0,1),(7,2),(7,2)])
        self.assertEqual(original,[3.5,-1,3.5,0])

    def test_import_flows_through_real_summary(self):
        with patch.dict('sys.modules',{'ti_system':types.SimpleNamespace(recall_list=lambda name:list(range(10)))}):
            output,_=flow(STDATA2.raw_session,['L1','0','0'])
        self.assertIn('MEAN=4.5000',output)
        self.assertIn('POPULATION SD=2.8723',output)
        self.assertIn('POPULATION VARIANCE=8.2500',output)

    def test_load_l1_replaces_current_session_data(self):
        with patch.dict('sys.modules',{'ti_system':types.SimpleNamespace(recall_list=lambda name:[2,4,6])}):
            output,_=flow(lambda:STDATA2.raw_session([(99,1)]),['0','11','0','0'])
        self.assertIn('MEAN=99.0000',output)
        self.assertIn('MEAN=4.0000',output)

    def test_current_l1_list_reused_for_mean_interval(self):
        recall=Mock(return_value=[2,4,6,8,10])
        with patch.dict('sys.modules',{'ti_system':types.SimpleNamespace(recall_list=recall)}):
            output,prompts=flow(STDATA2.raw_session,['L1','0','8','2','12','95%','','0'])
        recall.assert_called_once_with('1')
        self.assertIn('ONE-MEAN t INTERVAL',output)
        self.assertIn('x-bar=6.0000; s=3.1623; n=5',output)
        self.assertIn('DF=4.00',output)
        self.assertIn('t*=2.7764',output)
        self.assertIn('HOW TO DRAW: CONFIDENCE INTERVAL',output)
        self.assertEqual(sum('NUMBER OF VALUES' in p for p in prompts),1)

    def test_other_builtin_lists_and_manual_entry(self):
        recall=Mock(return_value=[1e-5])
        with patch.dict('sys.modules',{'ti_system':types.SimpleNamespace(recall_list=recall)}),patch('builtins.input',return_value='l2'):
            self.assertEqual(STDMATH1.read_raw(),[(1,100000)])
        recall.assert_called_once_with('2')
        with patch('builtins.input',side_effect=['3','3','1','2']):
            self.assertEqual(STDMATH1.read_raw(),[(1,1),(2,1),(3,1)])

    def test_empty_list_and_missing_bridge_do_not_create_data(self):
        with patch.dict('sys.modules',{'ti_system':types.SimpleNamespace(recall_list=lambda name:[])}):
            with self.assertRaises(ValueError): STDMATH1.read_os_list()
        with patch.dict('sys.modules',{'ti_system':types.SimpleNamespace()}):
            with self.assertRaisesRegex(ValueError,'recall_list'): STDMATH1.read_os_list()
