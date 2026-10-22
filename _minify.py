import glob, re

HEADER = (
    "# StatScholar - TI-84 Python Statistics Tutor",
    "# Author: Gregory King",
    None,  # Date line (any)
    "# Copyright (c) 2026 Gregory King",
    "# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0",
    "#",
    "# License terms: see LICENSE or STAT1.py.",
)

DATE_RE = re.compile(r"^# Date: 2026-09-\d\d$")

def strip_header(lines):
    # Remove a leading license header block if present.
    if len(lines) < 7:
        return lines
    for i, pat in enumerate(HEADER):
        ln = lines[i]
        if pat is None:
            if not DATE_RE.match(ln):
                return lines
        else:
            if ln != pat:
                return lines
    return lines[7:]

def process(path, keep_header):
    with open(path, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8")
    lines = text.split("\n")
    # drop trailing CR from each line
    lines = [ln.rstrip("\r") for ln in lines]
    if not keep_header:
        lines = strip_header(lines)
    out = []
    for ln in lines:
        stripped = ln.strip()
        if stripped == "":
            continue
        if stripped.startswith("#"):
            continue
        out.append(ln.rstrip())
    # drop trailing empty entries
    while out and out[-1] == "":
        out.pop()
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")

def main():
    files = sorted(glob.glob("ST*.py"))
    for f in files:
        process(f, keep_header=(f == "STAT1.py"))
    print("minified", len(files), "files")

if __name__ == "__main__":
    main()
