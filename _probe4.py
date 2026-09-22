import glob, os, types, re

def own_code(mod):
    total = 0
    for name, obj in vars(mod).items():
        if isinstance(obj, types.FunctionType) and getattr(obj, '__module__', '') == mod.__name__:
            try:
                total += len(obj.__code__.co_code)
                for k in obj.__code__.co_consts:
                    if isinstance(k, str):
                        total += len(k)
                    elif isinstance(k, tuple):
                        for kk in k:
                            if isinstance(kk, str):
                                total += len(kk)
            except Exception:
                pass
    return total

rows = []
for path in sorted(glob.glob('ST*.py')):
    name = os.path.basename(path)[:-3]
    src = len(open(path,'rb').read())
    top = []
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if line.startswith('import ') or line.startswith('from '):
            top.append(line)
        elif line.startswith('def ') or line.startswith('class '):
            break
    try:
        mod = __import__(name)
        oc = own_code(mod)
    except Exception as e:
        oc = -1
    rows.append((oc, name, src, '; '.join(top)))

for oc, name, src, top in sorted(rows, reverse=True):
    print('%-5d %-12s src=%-6d %s' % (oc, name, src, top))
