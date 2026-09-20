import contextlib
import io
import unittest
from unittest.mock import patch
from test_expansion import flow,raw
import STAT1 as app
import STCORE as c
import STNORM as normal
import STDMATH as data


class Quiz3(unittest.TestCase):
    def test_bear_boundaries_and_zero_spread(self):
        for x,strict,inclusive in [(35,'UNUSUALLY LOW','UNUSUALLY LOW'),(36,'NOT UNUSUAL','UNUSUALLY LOW'),(37,'NOT UNUSUAL','NOT UNUSUAL'),(48,'NOT UNUSUAL','UNUSUALLY HIGH'),(49,'UNUSUALLY HIGH','UNUSUALLY HIGH')]:
            self.assertEqual(normal.usual_classification((x,1),(42,1),(9,1)),strict)
            self.assertEqual(normal.usual_classification((x,1),(42,1),(9,1),True),inclusive)
        self.assertEqual(normal.usual_classification((4,1),(4,1),(0,1),True),'BOTH LOW AND HIGH')
        # Exact boundary with non-integer SD: no rounded-sqrt comparison.
        self.assertEqual(normal.usual_classification((1,1),(0,1),(1,4),True),'UNUSUALLY HIGH')

    def test_normal_rule_menu_and_reuse(self):
        out,prompts=flow(app.main,['5','1','7','2','5','42','3','1','36','1','7','1','5','1','36','1','0','0'])
        self.assertIn('UNUSUALLY LOW',out)
        self.assertIn('NOT UNUSUAL',out)
        self.assertEqual(prompts.count('MEAN: '),1)

    def test_urban_rural_real_compare_workflow(self):
        urban=['24','23.5','25','27','39','22.5','28','24']
        rural=['18','20','24','24','20','21','22','20']
        # Four original summary result screens, then the new compare option.
        out,prompts=flow(app.main,['4','6','8']+urban+['8']+rural+['1']*4+['6','1','1','1']+['1']*4+['0','0'])
        for value in ['15.9781','37.2719','16.9247','25.3253','39=UNUSUALLY HIGH','UNUSUAL OBSERVATIONS=NONE']:
            self.assertIn(value,out)
        self.assertEqual(prompts.count('NUMBER OF VALUES (1..100): '),2)

    def test_plant_axes_no_reentry(self):
        out,prompts=flow(app.main,['5','7','24.6','21','9','6.4','4.7','1.2','1','1','1','1','0','0'])
        for text in ['z A=0.4000','z B=1.4167','HIGHER RELATIVE=B','z=-3 x=-6.0000','z=3 x=8.3000']:
            self.assertIn(text,out)
        self.assertEqual(prompts.count('x: '),2)
        self.assertEqual(prompts.count('MEAN: '),2)

    def test_quiz_guide_numeric_paging(self):
        stream=io.StringIO()
        with patch('builtins.input',side_effect=['6','10','1','1','2','0','5','1','0','0','0','0']),contextlib.redirect_stdout(stream):
            app.main()
        self.assertIn('GRAPH IMAGE MISSING',stream.getvalue())
        self.assertIn('PAGE 2/',stream.getvalue())


if __name__=='__main__': unittest.main()
