# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

"""Desktop test adapter for the modular runtime; never transfer this file."""
import importlib
MODULE_NAMES = ('STDEFS','STBINFO','STSAMPLE','STPRE','STPRE1','STPRE2','STPRE3','STFINITE','STZLIST','STPAGE','STEXPER','STEXPER1','STEXPER2','STMDICE','STQUIZ5','STVENN','STQUIZ4','STQUIZ3','STQUIZ','STAT1','STCORE','STDESC','STPROB','STDICE','STBINOM','STCOUNT',
                'STGDESC','STGPROB','STGDICE','STGBIN','STGCNT','STREF','STDMATH','STDATA','STGRAPH',
                'STNORM','STHIST','STSTUDY','STSTU1','STSTU2','STFIND','STQUEST','STGNEW','STCOMB','STBMATH','STBEXTRA','STBWORD','STBW2','STBWE','STEFMT','STBHELP','STWORDS','STPWORD','STPTIDX','STPT1','STPT2','STPT3','STPT4','STQ1','STQ2','STQ3','STQ4','STQ5','STNAV','STINDEX','STVIN','STVMENU','STVCP','STVDISP','STVRES','STHOME','STEXACT','STEVENT','STTASKS','STPROBM','STWIZM','STBINFO2','STBINFO3','STBINFO4','STBINFO5','STBINFO6','STBINFO7','STBINFO9','STPROB1','STPROB2','STPROB3','STPROB4','STCOUNT1','STCOUNT2','STCOUNT3','STCOUNT4','STCOUNT5','STCOUNT6','STCOUNT7','STNORM1','STNORM2','STNORM3','STNORM4','STNORM5','STNORM6','STDMATH1','STDMATH2','STDMATH3','STVENN1','STVENN2','STDATA1','STDATA2','STDATA3','STGDESC1','STGDESC2','STGDESC3','STGDESC4','STGDESC5','STGDESC6','STGDESC7','STGDESC8','STGDESC9','STGPROB1','STGPROB2','STGPROB3','STGPROB4','STGPROB5','STGBIN1','STGBIN2','STGBIN3','STGBIN4','STGBIN5','STGCNT1','STGCNT2','STGCNT3','STGCNT4','STGNEW1','STGNEW2','STGNEW3','STGNEW4','STGNEW5','STGNEW6','STBINOM1','STBINOM2','STDESC1','STDESC2','STSAMPLE1','STSAMPLE2','STHIST1','STHIST2','STMDICE1','STMDICE2','STNAV1','STNAV2','STREF1','STREF2','STFIND1','STFIND2','STDICE1','STDICE2','STEXPER3')
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
