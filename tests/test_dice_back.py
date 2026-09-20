import contextlib
import io
import unittest
from unittest.mock import patch
import STCORE as c
import STDICE as dice
import STMDICE as multi
import STPAGE


def keys(presses):
    return [value for key in presses for value in (key,key,0)]


class DiceBack(unittest.TestCase):
    def run_keys(self,fn,presses,inputs=()):
        with patch.object(c,'HAS_KEYS',True),patch.object(c,'KEY_STYLE','scan'),patch.object(c,'_LAST_RAW',None),patch.object(c,'get_key',side_effect=keys(presses),create=True),patch('builtins.input',side_effect=inputs) as entry,contextlib.redirect_stdout(io.StringIO()) as out:
            fn()
        return out.getvalue(),entry.call_count

    def test_single_page_dice_menu_left_returns(self):
        output,count=self.run_keys(dice.dice_session,[24],['2'])
        self.assertIn('TWO DICE > QUESTION',output)
        self.assertEqual(count,1)

    def test_cancel_word_selector_does_not_ask_for_value(self):
        output,count=self.run_keys(dice.read_pair_event,[92,105,24])
        self.assertIn('DICE > WORDS',output)
        self.assertEqual(count,0)

    def test_dice_result_left_leaves_without_format_menu(self):
        # One event -> doubles -> Left from result -> Left from next menu.
        output,count=self.run_keys(dice.dice_session,[92,105,82,105,24,24],['2'])
        self.assertIn('P=0.1667',output)
        self.assertNotIn('ANSWER FORMAT',output)
        self.assertEqual(count,1)

    def test_multiple_dice_result_back_and_menu_page_back(self):
        output,count=self.run_keys(lambda:multi.solver_multi_dice(5),[26,24,92,105,24,24])
        self.assertIn('TOTAL OUTCOMES=7776',output)
        self.assertNotIn('ANSWER FORMAT',output)
        self.assertEqual(count,0)

    def test_outcome_list_next_previous_then_back(self):
        text=', '.join('('+str(a)+','+str(b)+')' for a in range(1,7) for b in range(1,7))
        output,_=self.run_keys(lambda:STPAGE.text_pages('DICE OUTCOMES',text),[26,24,24])
        self.assertIn('PAGE 2/',output)
        self.assertEqual(output.count('PAGE 1/'),2)
        self.run_keys(lambda:STPAGE.text_pages('ONE RESULT','(1,1)'),[26])

    def test_last_result_page_right_advances(self):
        output,_=self.run_keys(lambda:c.results('DICE RESULT',[('P',(1,6))]),[26,24])
        self.assertIn('ANSWER FORMAT',output)

    def test_table_page_controls_left_at_first_page_returns(self):
        output,_=self.run_keys(lambda:c.paged_results('TABLE',9,lambda i:('ROW '+str(i),i)),[45,24])
        self.assertIn('LEFT BACK',output)


if __name__=='__main__': unittest.main()
