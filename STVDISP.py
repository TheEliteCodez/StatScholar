# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Scrolling text viewer, loaded only while a screen is displayed.
import STCORE as c


def view(title, lines):
    if len(lines) == 0:
        lines = ('NO CONTENT',)
    count = sum((1 for line in c.wrapped_lines(lines)))
    top = 0
    max_top = max(0, count - c.VIEW_LINES)
    while True:
        c.cls()
        end = min(count, top + c.VIEW_LINES)
        print(title[:30])
        print(str(top + 1) + '-' + str(end) + '/' + str(count))
        for i, line in enumerate(c.wrapped_lines(lines)):
            if i >= end:
                break
            if i >= top:
                print(line)
        if c.HAS_KEYS:
            print('UP/DN SCROLL RIGHT NEXT')
            print('LEFT BACK  CLEAR BACK' if top == 0 else 'LEFT PREV  CLEAR BACK')
        else:
            print('ENTER NEXT  - PREV  0 BACK')
        k = c.wait_key()
        if k in ('up', 'u'):
            if top > 0:
                top -= 1
        elif k == 'left':
            if top == 0: return 'back'
            top = max(0, top - c.VIEW_LINES)
        elif k == 'right':
            if top == max_top: return
            top = min(max_top, top + c.VIEW_LINES)
        elif k in ('down', 'd', 'enter'):
            if top < max_top:
                top += 1
            elif k == 'enter': return
        elif k in ('b', 'esc'):
            return 'exit'
