# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Optional on-calculator compatibility probe. Run separately from STAT1.
# No files are written. Press ENTER between sections; record the results.
import sys
import gc
try:
    import ti_system as ti
except ImportError:
    ti = None


def heap(label):
    gc.collect()
    print(label)
    free = getattr(gc, "mem_free", None)
    print("FREE BYTES: " + str(free()) if free else "mem_free unavailable")


def list_probe(size):
    values = None
    try:
        values = [0] * size
        print("LIST " + str(size) + ": OK " + str(len(values)))
    except Exception as exc:
        print("LIST " + str(size) + ": " + type(exc).__name__)
    finally:
        values = None
        gc.collect()


def module_probe():
    modules = getattr(sys, "modules", None)
    if modules is None:
        print("sys.modules unavailable")
        return
    first = second = None
    had_core = "STCORE" in modules
    try:
        first = __import__("STGDICE")
        del modules["STGDICE"]
        print("CACHE DELETE: " + str("STGDICE" not in modules))
        second = __import__("STGDICE")
        print("FRESH REIMPORT: " + str(first is not second))
    except Exception as exc:
        print("MODULE TEST: " + type(exc).__name__)
        print(str(exc))
    finally:
        first = second = None
        # Only entries introduced or exercised by this probe are removed.
        try:
            if "STGDICE" in modules:
                del modules["STGDICE"]
            if not had_core and "STCORE" in modules:
                del modules["STCORE"]
        except Exception as exc:
            print("CACHE CLEANUP: " + type(exc).__name__)
        gc.collect()


def expansion_probe():
    # Keep the real home module resident while measuring new helper imports.
    import STCORE
    saved_keys=STCORE.ON_TI
    STCORE.ON_TI=False
    try:
        import STAT1
    finally:
        STCORE.ON_TI=saved_keys
    heap('HOME RESIDENT')
    for size in (25,50,100):
        try:
            STCORE.call('STDMATH','probe_summary',size)
            heap('AFTER RAW '+str(size))
        except Exception as exc:
            print('RAW '+str(size)+': '+type(exc).__name__)
            print(str(exc))
            break
    try:
        answer=STCORE.call('STNORM','z_value',(44,1),(40,1),(4,1))
        print('NORMAL z=1: '+str(answer==(1,1)))
    except Exception as exc:
        print('NORMAL: '+type(exc).__name__)
        print(str(exc))
    heap('AFTER NORMAL')


def main():
    print("EVO COMPATIBILITY PROBE")
    print("Run in a fresh Python session")
    heap("START / GC OK")
    list_probe(100)
    list_probe(101)
    input("ENTER FOR MODULE TEST: ")
    print("Needs project STGDICE, STCORE")
    module_probe()
    heap("AFTER MODULE TEST")
    input("ENTER FOR KEY TEST: ")
    if ti is None:
        print("ti_system unavailable")
    else:
        get = getattr(ti, "get_key", None)
        wait = getattr(ti, "wait_key", None)
        print("get_key: " + str(get is not None))
        print("wait_key: " + str(wait is not None))
        if get:
            import STCORE
            print('READER: get_key(0)')
            for label in ("UP", "DOWN", "LEFT", "RIGHT", "1", "2", "3", "0", "ENTER", "CLEAR"):
                print("PRESS " + label)
                raw = STCORE.read_raw_key()
                print(label + " = " + repr(raw))
        else:
            print("Native input: no get_key")
    if input("RAW/NORMAL MEMORY TEST? Y/N: ").strip().upper()=="Y":
        expansion_probe()
    heap("END")
    print("Record or photograph results")


if __name__ == "__main__" or ti is not None:
    main()
