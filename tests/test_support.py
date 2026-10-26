# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

"""Desktop test adapter for the modular runtime; never transfer this file."""
import importlib
MODULE_NAMES = ('STDEFS', 'STBINFO', 'STSAMPLE', 'STFINITE', 'STZLIST', 'STPAGE', 'STEXPER', 'STEXPER1', 'STEXPER2', 'STEXPER4', 'STMDICE', 'STVENN', 'STAT1', 'STCORE', 'STDESC', 'STPROB', 'STDICE', 'STBINOM', 'STCOUNT', 'STDMATH', 'STDATA', 'STGRAPH', 'STNORM', 'STCLT', 'STDIST', 'STNDIST', 'STUNIF', 'STTDIST', 'STTPROB', 'STHIST', 'STSTUDY', 'STSTU1', 'STSTU2', 'STCOMB', 'STBMATH', 'STBEXTRA', 'STBWORD', 'STBW2', 'STBWE', 'STEFMT', 'STBHELP', 'STVIN', 'STVMENU', 'STVCP', 'STVDISP', 'STVRES', 'STHOME', 'STEXACT', 'STEVENT', 'STTASKS', 'STPROBM', 'STBINFO2', 'STBINFO5', 'STBINFO7', 'STBINFO9', 'STPROB1', 'STPROB3', 'STPROB4', 'STCOUNT2', 'STCOUNT3', 'STCOUNT4', 'STCOUNT5', 'STCOUNT6', 'STNORM1', 'STNORM2', 'STNORM3', 'STNORM4', 'STDMATH1', 'STDMATH2', 'STVENN2', 'STDATA2', 'STDATA3', 'STBINOM1', 'STBINOM2', 'STDESC1', 'STDESC2', 'STSAMP1', 'STSAMP2', 'STHIST2', 'STMDICE2', 'STDICE2', 'STSIZE', 'STZCRIT', 'STCLT1', 'STCLT2', 'STCLTC', 'STCLTM', 'STCLTR', 'STTCRIT', 'STCINUM', 'STCIIO', 'STCIPROP', 'STCIMEAN', 'STCIMOE', 'STCIMENU', 'STCI', 'STPCT', 'STSKETCH', 'STCLTF', 'STRULE', 'STHYP', 'STHYIO', 'STHYPR', 'STHYME', 'STHYRES')
MODULES = [importlib.import_module(name) for name in MODULE_NAMES]
import STCORE
STCORE.release_topics = lambda *args: None
OWNERS = {name: module for module in reversed(MODULES) for name in vars(module)}

class Runtime:
    def owner(self, name):
        if name in OWNERS:
            return OWNERS[name]
        raise AttributeError(name)

    def __getattr__(self, name):
        return getattr(self.owner(name), name)

    def __setattr__(self, name, value):
        setattr(self.owner(name), name, value)

    def __delattr__(self, name):
        delattr(self.owner(name), name)

s = Runtime()
