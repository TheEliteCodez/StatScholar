"""Fixed-heap MicroPython replay. Supply a native 32-bit interpreter executable.

Run from the project root: python tests/native_heap_walk.py <micropython.exe>
Optional --baseline points to an earlier runtime tree for identical replays.
This is not TI firmware or a measurement of the calculator's available RAM.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parent.parent


def fixture(entry):
    code=(ROOT/'tests/micropython_hypothesis.py').read_text()
    code=code.replace("c.wait_key=", "fixed_heap=gc.mem_free()+gc.mem_alloc()\nprint('MPY_HEAP',fixed_heap)\nc.wait_key=",1)
    code=code.replace("        print('MPY_BATCH_PASS'", "        assert gc.mem_free()+gc.mem_alloc()==fixed_heap\n        print('MPY_BATCH_PASS'")
    if entry:
        code=code.replace('import STAT1\n','').replace('for graphics in (False,True):','for graphics in (True,):')
        code=code.replace('        STAT1.main()',"        if 'STAT1' in globals():STAT1.main()\n        else:import STAT1")
    return code


def run(exe,tree,heap,entry):
    result=subprocess.run([str(exe),'-X','heapsize='+str(heap),'-c',fixture(entry)],
                          cwd=tree,capture_output=True,text=True,timeout=60)
    output=result.stdout+result.stderr
    markers=[line for line in output.splitlines() if line.startswith('MPY_')]
    passed=(result.returncode==0 and len([m for m in markers if m.startswith('MPY_BATCH_PASS')])==(2 if entry else 4)
            and any(m.startswith('MPY_PASS ') for m in markers))
    return dict(heap_requested_bytes=heap,entry_autorun=entry,passed=passed,exit_code=result.returncode,
                markers=markers,gc_heap_bytes=next((int(m.split()[1]) for m in markers if m.startswith('MPY_HEAP ')),None),failure_tail='' if passed else output[-1400:])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('interpreter',type=Path)
    parser.add_argument('--baseline',type=Path)
    args=parser.parse_args()
    exe=args.interpreter.resolve()
    trees=[('current',ROOT)]
    if args.baseline:trees.insert(0,('baseline',args.baseline.resolve()))
    evidence={'scope':'Native 32-bit MicroPython, fixed GC heap; 20 continuous problems or 10 autorun problems per replay, real imports/math/text, plot/key stubs. Every completed batch asserts the heap did not expand. Not TI firmware/device proof.',
              'interpreter_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'trees':{}}
    for label,tree in trees:
        rows=[]
        for entry in (False,True):
            for heap in (36000,38000,40000,42000,48000,64000):
                row=run(exe,tree,heap,entry);rows.append(row)
                print(label,heap,'autorun' if entry else 'continuous','PASS' if row['passed'] else 'FAIL',flush=True)
        evidence['trees'][label]={'runs':rows,'runtime_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(tree.glob('ST*.py'))}}
    (ROOT/'artifacts/native_heap.json').write_text(json.dumps(evidence,indent=2)+'\n')
    assert all(r['passed'] for r in evidence['trees']['current']['runs'] if r['heap_requested_bytes']>=40000)
