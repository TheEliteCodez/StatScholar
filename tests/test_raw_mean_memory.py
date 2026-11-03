import statistics
import unittest
from unittest.mock import patch

import STCORE as c
import STCIMEAN as ci
from test_worked_substitutions import flow


class RawMeanMemory(unittest.TestCase):
    def test_interval_avoids_full_descriptive_engine(self):
        original=c.call
        def call(module,function,*args):
            self.assertNotIn(module,('STDMATH','STDMATH1','STDMATH2'))
            return original(module,function,*args)
        with patch.object(c,'call',side_effect=call):
            text=flow(ci._one_mean,['2','10','63.9','88','64.3','68.4','64.3','68.4','64.3','69','64.3','73.5','95%',''])
        self.assertIn('x-bar=68.8400',text)
        self.assertIn('STANDARD ERROR=2.3478',text)

    def test_list_import_and_large_offset_accuracy(self):
        import types
        import sys
        import STMEAN
        values=[1000000+i/10 for i in range(100)]
        fake=types.ModuleType('ti_system')
        fake.recall_list=lambda name:values if name=='6' else None
        with patch.dict(sys.modules,{'ti_system':fake}),patch('builtins.input',return_value='L6'),patch.object(c,'heading'):
            mean,sd,n=STMEAN.read_raw('MEASUREMENTS')
        self.assertEqual(n,100)
        self.assertAlmostEqual(mean,statistics.mean(values),places=7)
        self.assertAlmostEqual(sd,statistics.stdev(values),places=7)


if __name__=='__main__': unittest.main()
