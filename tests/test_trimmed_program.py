from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent


class TrimmedProgram(unittest.TestCase):
    def test_single_program_and_removed_files(self):
        modules = list(ROOT.glob('ST*.py'))
        # Paired-data, streaming mean and full-screen graph helpers load on demand.
        # This is an inventory budget, not a measurement of calculator heap use.
        self.assertLess(sum(p.stat().st_size for p in modules), 323000)
        self.assertLessEqual(len(modules), 118)
        self.assertFalse((ROOT / 'STCI.py').exists())
        self.assertFalse((ROOT / 'calculator').exists())
        self.assertFalse((ROOT / 'build_calculator.py').exists())
        for pattern in ('STQUIZ*.py', 'STQ[1-5].py', 'STPRE*.py', 'STPT*.py',
                        'STREF*.py', 'STNAV*.py', 'STFIND*.py', 'STGDESC*.py',
                        'STGPROB*.py', 'STGBIN*.py', 'STGCNT*.py', 'STGNEW*.py', 'STGDICE.py',
                        'STWORDS.py', 'STWPROB.py', 'STWDATA.py', 'STWIZM.py'):
            self.assertEqual(list(ROOT.glob(pattern)), [], pattern)

    def test_home_contains_calculators_without_words_quizzes_or_wizard(self):
        import STHOME
        from unittest.mock import patch
        with patch.object(STHOME.c, 'menu', return_value='0') as menu:
            STHOME.quick_main()
        items = dict(menu.call_args.args[1])
        self.assertTrue({'2', '3', '4', '5', '6', '9', '10', '11'} <= set(items))
        self.assertEqual(items['1'], 'NORMAL DISTRIBUTION')
        self.assertEqual(items['7'], 'UNIFORM DISTRIBUTION')
        self.assertEqual(items['8'], 'STUDENT t DISTRIBUTION')

    def test_remaining_home_menus_open_and_release(self):
        code = """
import builtins, STAT1, STCORE
for option in ['1','2','3','4','5','6','7','8','9','10','11']:
    pending=iter([option,'0','0'])
    builtins.input=lambda prompt='':next(pending)
    STAT1.main()
    assert list(pending)==[], option
    assert not STCORE.topic_modules(), STCORE.topic_modules()
"""
        run = subprocess.run([sys.executable, '-B', '-c', code], cwd=ROOT,
                             capture_output=True, text=True, timeout=10)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)

    def test_frequency_calculator_survived_quiz_deletion(self):
        import STPCT
        self.assertEqual(STPCT.frequency_event([((1, 1), 3), ((2, 1), 5)], '>=', (2, 1)), (5, 8))
