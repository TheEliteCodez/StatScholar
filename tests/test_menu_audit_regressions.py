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



