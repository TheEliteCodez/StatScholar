import STCORE
from STBINFO2 import page

def report_pages(n, p, event=None, answer=None, threshold=(1, 20), cache=None):
    cache = {} if cache is None else cache
    target = 0
    while True:
        pg = page(n, p, event, answer, threshold, cache, target)
        if pg is None:
            return
        yield pg
        target += 1

def append_page(lines, page):
    count = sum(1 for line in STCORE.wrapped_lines(page))
    lines.extend(page)
    lines.extend([''] * ((-count) % STCORE.VIEW_LINES))

def followup(n, p, event, answer, threshold=(1, 20)):
    lines = []
    for pg in report_pages(n, p, event, answer, threshold):
        append_page(lines, pg)
    return lines
