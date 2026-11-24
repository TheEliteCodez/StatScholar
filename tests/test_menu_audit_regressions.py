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
    def test_auditor_detects_code_retained_after_module_object_is_gone(self):
        code=r'''
import gc,sys,types,weakref
sys.path.insert(0,'tests')
from menu_walk import Walker
walker=Walker();walker.references={};walker.peak_bytes=0
module=types.ModuleType('STREGWK')
module_ref=weakref.ref(module)
sys.setprofile(walker.profile)
try:exec(compile('def row(): return 1\nclass Report: pass\n','STREGWK.py','exec'),module.__dict__)
finally:sys.setprofile(None)
held=module.row;del module;gc.collect()
assert module_ref() is None
assert 'STREGWK' not in sys.modules
assert {ref().__name__ for ref in walker.references.values() if ref() is not None}=={'row','Report'}
del held;gc.collect()
assert all(ref() is None for ref in walker.references.values())
print('RETAINED_CODE_DETECTED')
'''
        result=subprocess.run([sys.executable,'-B','-c',code],cwd=ROOT,capture_output=True,text=True,timeout=15)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('RETAINED_CODE_DETECTED',result.stdout)

    def test_cancel_between_endpoints_returns_without_an_event(self):
        for binomial in (False,True):
            with patch.object(c,'menu',side_effect=['6','0']), \
                 patch('builtins.input',side_effect=['1','5']), \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertIsNone(c.event_input(binomial))



