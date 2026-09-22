# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Choice-page picker, loaded only while an op page is shown.
import STCORE


def choice_pages(title, pages):
    page = min(STCORE._menu_pages.get(title, 0), len(pages)-1)
    while True:
        STCORE.heading(title)
        for i, (label, token) in enumerate(pages[page]):
            print(str(i + 1) + ' ' + label[:28])
        print(('LEFT BACK / RIGHT NEXT' if page == 0 else 'LEFT PREV / RIGHT NEXT') if STCORE.HAS_KEYS else '0 BACK ENTER NEXT - PREVIOUS')
        key = STCORE.read_choice()
        if key == '0':
            STCORE._menu_pages.pop(title, None)
            return None
        if key == 'N':
            page = (page + 1) % len(pages)
        elif key == 'P':
            if page == 0:
                STCORE._menu_pages.pop(title, None)
                return None
            page -= 1
        elif key.isdigit() and 1 <= int(key) <= len(pages[page]):
            if len(STCORE._menu_pages) > 32: STCORE._menu_pages.clear()
            STCORE._menu_pages[title] = page
            return pages[page][int(key) - 1][1]
