# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Compatibility shim for tests; the device loads STVIN/STVMENU/STVDISP/STVRES directly.
from STVIN import read_raw_key, normalize_key, wait_key, read_choice
from STCORE import _menu_pages
from STVMENU import menu
from STVCP import choice_pages
from STVDISP import view
from STVRES import results, paged_results
