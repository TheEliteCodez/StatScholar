import contextlib
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import STCORE as c

ROOT=Path(__file__).resolve().parent.parent


class MenuAuditRegressions(unittest.TestCase):
    def test_cancel_between_endpoints_returns_without_an_event(self):
        for binomial in (False,True):
            with patch.object(c,'menu',side_effect=['6','0']), \
                 patch('builtins.input',side_effect=['1','5']), \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertIsNone(c.event_input(binomial))

    def test_device_monitor_restores_hooks_and_reports_real_counter(self):
        code='''
import builtins,gc,sys
import STCORE as c
import EVOMEM
original_import=builtins.__import__
original_call=c.call
original_menu=c.menu
gc.mem_free=lambda:12345
pending=iter(['3','1','2','8','0','0','0'])
builtins.input=lambda prompt='':next(pending)
EVOMEM.main()
assert list(pending)==[]
assert builtins.__import__ is original_import
assert c.call is original_call and c.menu is original_menu
assert not c.topic_modules()
'''
        run=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,
                           capture_output=True,text=True,timeout=15)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
        self.assertIn('MIN FREE: 12345',run.stdout)
        self.assertIn('ERROR: NONE',run.stdout)

    def test_device_monitor_does_not_invent_heap_results_on_desktop(self):
        run=subprocess.run([sys.executable,'-B','EVOMEM.py'],cwd=ROOT,
                           capture_output=True,text=True,timeout=15)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('HEAP COUNTER UNAVAILABLE',run.stdout)
        self.assertNotIn('MIN FREE:',run.stdout)
