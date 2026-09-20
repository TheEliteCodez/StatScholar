# Author: TheEliteCodez
import contextlib
import io
import subprocess
import sys
import unittest
from unittest.mock import patch
import STCORE as c
import STPAGE


class Navigation(unittest.TestCase):
    def test_evo_prefers_polling_when_both_apis_exist(self):
        code="""
import builtins,sys,types
ti=types.ModuleType('ti_system')
def blocked(): raise AssertionError('Do not call wait_key')
ti.wait_key=blocked
# Home next/previous, Binomial, Exactly, answer back, exit topic and home.
presses=[26,24,93,105,92,105,45,102,105,102,105]
events=iter(value for key in presses for value in (key,key,0))
def get_key(mode):
 assert mode==0
 return next(events)
ti.get_key=get_key
sys.modules['ti_system']=ti
answers=iter(['10','.05','1'])
builtins.input=lambda prompt='':next(answers)
import STAT1,STCORE
assert STCORE.KEY_STYLE=='scan' and STCORE.HAS_KEYS
assert list(answers)==[]
assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
"""
        result=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('7 PRACTICE TEST 1',result.stdout)
        self.assertIn('ANSWER=0.3151',result.stdout)

    def test_scan_release_repeated_digit_and_arrow_pages(self):
        with patch.object(c,'HAS_KEYS',True),patch.object(c,'KEY_STYLE','scan'),patch.object(c,'_LAST_RAW',None),patch.object(c,'get_key',side_effect=[92,92,0,92,0,105],create=True) as reader,contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(c.read_choice(),'11')
            self.assertTrue(all(call.args==(0,) for call in reader.call_args_list))
        with patch.object(c,'HAS_KEYS',True),patch.object(c,'KEY_STYLE','scan'),patch.object(c,'_LAST_RAW',None),patch.object(c,'get_key',side_effect=[26,26,0,24,24,0,45],create=True),contextlib.redirect_stdout(io.StringIO()) as output:
            c.view('ARROWS',[str(i) for i in range(20)])
        self.assertIn('8-14/20',output.getvalue())
        self.assertEqual(output.getvalue().count('1-7/20'),2)

    def test_wait_key_only_device_keeps_native_input(self):
        code="""
import builtins,sys,types
ti=types.ModuleType('ti_system')
def blocked(*args): raise AssertionError('Raw-key API must not run')
ti.wait_key=blocked
sys.modules['ti_system']=ti
answers=iter(['2','1','10','.05','1','0','0','0'])
builtins.input=lambda prompt='':next(answers)
import STAT1,STCORE
assert STCORE.ON_TI and not STCORE.HAS_KEYS
assert list(answers)==[]
assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
"""
        result=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('ANSWER=0.3151',result.stdout)

    def test_native_paging_without_letter_commands(self):
        with patch.object(c,'HAS_KEYS',False),patch('builtins.input',side_effect=['','-','7']),contextlib.redirect_stdout(io.StringIO()) as output:
            selected=c.menu('ITEMS',[(str(i),'ITEM '+str(i)) for i in range(1,8)])
        self.assertEqual(selected,'7')
        self.assertIn('6 ITEM 6',output.getvalue())
        with patch.object(c,'HAS_KEYS',False),patch('builtins.input',side_effect=['','-','0']),contextlib.redirect_stdout(io.StringIO()) as output:
            c.view('PAGES',[str(i) for i in range(20)])
        self.assertIn('8-14/20',output.getvalue())
        self.assertEqual(output.getvalue().count('1-7/20'),2)

    def test_alpha_locked_digits_and_shifted_arrows(self):
        # TI's green (ALPHA) keypad codes, including theta on the 3 key.
        codes=(153,178,179,204,173,174,175,168,169,170)
        for digit,code in enumerate(codes):
            with patch.object(c,'HAS_KEYS',True),patch.object(c,'KEY_STYLE','ce'),patch.object(c,'ti_wait_key',side_effect=[code,5],create=True),patch('builtins.input',side_effect=AssertionError('Numeric menu must not use text entry')),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(c.read_choice(),str(digit))
        with patch.object(c,'HAS_KEYS',True),patch.object(c,'KEY_STYLE','ce'),patch.object(c,'ti_wait_key',side_effect=[15,14,178,179,10,204,5],create=True),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(c.menu('ITEMS',[(str(i),'ITEM') for i in range(1,15)]),'13')

    def test_explicit_id_entry_preserves_letters(self):
        with patch.object(c,'HAS_KEYS',True),patch.object(c,'KEY_STYLE','ce'),patch.object(c,'ti_wait_key',return_value=5,create=True),patch('builtins.input',return_value='Q001'):
            self.assertEqual(c.read_choice(),'Q001')

    def test_ce_menu_arrows_and_multidigit_selection(self):
        # Right, left, right, 1, 2, ENTER selects option 12 on page 3.
        with patch.object(c,'HAS_KEYS',True),patch.object(c,'KEY_STYLE','ce'),patch.object(c,'ti_wait_key',side_effect=[1,2,1,243,244,13],create=True),patch('builtins.input',side_effect=AssertionError('No text input for arrows or digits')),contextlib.redirect_stdout(io.StringIO()) as out:
            key=c.menu('CHOICES',[(str(i),'ITEM '+str(i)) for i in range(1,14)])
        self.assertEqual(key,'12')
        self.assertGreaterEqual(out.getvalue().count('1 ITEM 1'),2)
        self.assertIn('6 ITEM 6',out.getvalue())

    def test_choice_pages_and_text_pages(self):
        with patch.object(c,'HAS_KEYS',True),patch.object(c,'KEY_STYLE','ce'),patch.object(c,'ti_wait_key',side_effect=[1,2,1,243,13],create=True),contextlib.redirect_stdout(io.StringIO()):
            selected=c.choice_pages('WORDS',((('FIRST','a'),),(('SECOND','b'),)))
        self.assertEqual(selected,'b')
        with patch.object(c,'HAS_KEYS',True),patch.object(c,'KEY_STYLE','ce'),patch.object(c,'ti_wait_key',side_effect=[1,2,9],create=True),patch('builtins.input',side_effect=AssertionError('Use arrows')),contextlib.redirect_stdout(io.StringIO()) as out:
            STPAGE.text_pages('PAGES','example text '*40)
        self.assertIn('PAGE 2/',out.getvalue())
        self.assertEqual(out.getvalue().count('PAGE 1/'),2)

    def test_startup_and_binomial_do_not_load_reference_index(self):
        code="""
import builtins,contextlib,io,sys
import STAT1,STCORE
assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
STCORE.view=lambda *args:None
for repeat in range(3):
 answers=iter(['2','1','10','.05','1','0','0'])
 def read(prompt=''):
  assert 'STINDEX' not in sys.modules and 'STNAV' not in sys.modules
  return next(answers)
 builtins.input=read
 with contextlib.redirect_stdout(io.StringIO()): STAT1.main()
 assert list(answers)==[]
 assert not set(STCORE.TOPIC_MODULES).intersection(sys.modules)
"""
        result=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)


if __name__=='__main__': unittest.main()
