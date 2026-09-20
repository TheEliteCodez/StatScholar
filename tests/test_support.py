"""Desktop test adapter for the modular runtime; never transfer this file."""
import importlib
MODULE_NAMES = ('STBINFO','STSAMPLE','STPRE','STPRE1','STPRE2','STPRE3','STFINITE','STZLIST','STPAGE','STEXPER','STMDICE','STQUIZ5','STVENN','STQUIZ4','STQUIZ3','STQUIZ','STAT1','STCORE','STDESC','STPROB','STDICE','STBINOM','STCOUNT',
                'STGDESC','STGPROB','STGDICE','STGBIN','STGCNT','STREF','STDMATH','STDATA','STGRAPH',
                'STNORM','STHIST','STSTUDY','STFIND','STQUEST','STGNEW','STCOMB','STBMATH','STBEXTRA','STBWORD','STBHELP','STWORDS','STPWORD','STPTIDX','STPT1','STPT2','STPT3','STPT4','STQ1','STQ2','STQ3','STQ4','STQ5','STNAV','STINDEX','STVIEW')
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
