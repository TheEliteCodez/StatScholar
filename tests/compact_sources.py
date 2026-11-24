"""Compact root source whitespace while proving AST and string equivalence.

Run only when intentionally updating the calculator source files in place.
License comments, other comments, blank lines, and string contents are kept.
"""
import ast
import hashlib
import io
import json
from pathlib import Path
import tokenize

ROOT=Path(__file__).resolve().parent.parent


def compact(source):
    tokens=list(tokenize.generate_tokens(io.StringIO(source).readline))
    protected=set()
    for token in tokens:
        if token.type==tokenize.STRING and token.end[0]>token.start[0]:
            protected.update(range(token.start[0]+1,token.end[0]+1))
    widths=[len(t.string) for t in tokens if t.type==tokenize.INDENT]
    if not widths or min(widths)<4:return source
    lines=[]
    for number,line in enumerate(source.splitlines(keepends=True),1):
        if number not in protected:
            width=len(line)-len(line.lstrip(' '))
            line=' '*(width//2)+line[width:]
        lines.append(line)
    result=''.join(lines)
    assert ast.dump(ast.parse(result))==ast.dump(ast.parse(source))
    return result


if __name__=='__main__':
    pending=[];records=[]
    for path in sorted(ROOT.glob('ST*.py')):
        before=path.read_bytes();source=path.read_text(encoding='utf-8')
        after=compact(source).encode('utf-8')
        assert ast.dump(ast.parse(after))==ast.dump(ast.parse(before)),path.name
        pending.append((path,after))
        records.append(dict(file=path.name,before_bytes=len(before),after_bytes=len(after),
                            before_sha256=hashlib.sha256(before).hexdigest(),
                            after_sha256=hashlib.sha256(after).hexdigest(),ast_identical=True))
    for path,data in pending:path.write_bytes(data)
    result=dict(scope='Whitespace and line-ending compaction only; every file has identical parsed AST, including string constants. No heap savings inferred from disk-byte savings.',
                before_bytes=sum(r['before_bytes'] for r in records),
                after_bytes=sum(r['after_bytes'] for r in records),files=records)
    (ROOT/'artifacts/source_compaction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['before_bytes'], '->',result['after_bytes'],'source bytes; all ASTs identical')
