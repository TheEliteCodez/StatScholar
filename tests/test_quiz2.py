# Author: Gregory King
"""Quiz 2 calculations, reusable rows, menu access and numeric paging."""
import contextlib
import io
import unittest
from unittest.mock import patch
from test_expansion import flow
import STAT1
import STQUIZ as q
import STSTUDY as study
import STCORE as c


class Quiz2(unittest.TestCase):
    def test_percent_home_and_changed_numbers(self):
        for total,percent,answer in [('75','45%','33.7500'),('120','.25','30.0000')]:
            out,_=flow(STAT1.main,['4','7',total,percent,'0','0'])
            self.assertIn('ANSWER='+answer,out)

    def test_hurricane_table_and_events(self):
        rows=[((i+1,1),f) for i,f in enumerate([109,72,71,18,3])]
        lines=list(q.frequency_lines(list(reversed(rows))))
        self.assertIn('RELATIVE=0.0659',lines)
        self.assertIn('CUM REL=0.9231',lines)
        self.assertEqual(lines[-2:],['CUM COUNT=273','CUM REL=1.0000'])
        self.assertEqual(q.frequency_event(rows,'>=',(3,1)),(92,273))
        self.assertEqual(q.frequency_event(rows,'>',(3,1)),(1,13))
        out,prompts=flow(lambda:q.frequency_tools(rows),['4','3','1','3','2','1','0'])
        self.assertIn('PROPORTION=0.3370',out)
        self.assertIn('PROPORTION=0.6630',out)
        self.assertNotIn('NUMBER OF ROWS: ',prompts)

    def test_exact_order_and_duplicate_values(self):
        rows=[((3,2),2),((1,1),1),((3,2),3)]
        self.assertEqual(list(q.frequency_lines(rows))[-4:],['VALUE=1.5 COUNT=5','RELATIVE=0.8333','CUM COUNT=6','CUM REL=1.0000'])
        self.assertEqual(q.frequency_event(rows,'<',(3,2)),(1,6))

    def test_quiz_home_and_numeric_pages(self):
        # Numeric option selection and definition paging need no arrow keys.
        outputs=io.StringIO()
        with patch('builtins.input',side_effect=['6','9','7','1','2','0','0','0','0']),contextlib.redirect_stdout(outputs):
            STAT1.main()
        text=outputs.getvalue()
        self.assertIn('QZ207',text)
        self.assertIn('PAGE 2/',text)
        self.assertIn('ENTER/1 NEXT',text)

    def test_bias_definitions_are_searchable(self):
        with patch.object(study,'definition_list') as show:
            flow(study.definitions_menu,['5','quota','0'])
        self.assertEqual(show.call_args[0][1][0][0],'quota sampling')

    def test_frequency_home_reuses_rows_and_numeric_table_pages(self):
        inputs=['4','2','5','1','109','2','72','3','71','4','18','5','3',
                '1','4','1','1','2','0','4','3','1','0','0','0']
        out,prompts=flow(STAT1.main,inputs)
        self.assertEqual(prompts.count('NUMBER OF ROWS: '),1)
        self.assertIn('PAGE 2/',out)
        self.assertIn('PROPORTION=0.3370',out)


if __name__=='__main__': unittest.main()
