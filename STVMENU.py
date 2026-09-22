# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Menu and choice-page renderers, loaded only while a menu is active.
import STCORE


def menu(title, items, shortcuts=(), other_shortcuts=(), page_size=5):
    items = list(items)
    for shortcut in shortcuts if len(shortcuts) <= 3 else ():
        if shortcut in ('C', 'S') and not any(k == shortcut for k, label in items):
            items.append((shortcut, 'CHANGE DATA' if shortcut == 'C' else 'SELECT MANY'))
    number = max([int(k) for k, label in items if k.isdigit()] + [0]) + 1
    aliases = {}
    shown_items = []
    for key, label in items:
        shown = key
        if not key.isdigit() and key not in ('N', 'P'):
            shown = str(number); number += 1; aliases[shown] = key
        shown_items.append((shown, label))
    page = min(STCORE._menu_pages.get(title, 0), (len(items)-1)//page_size)
    while True:
        STCORE.heading(title)
        for key, label in shown_items[page * page_size:(page + 1) * page_size]:
            shown = {'N':'RIGHT','P':'LEFT'}.get(key, key) if STCORE.HAS_KEYS else {'N':'ENTER','P':'-'}.get(key, key)
            print(shown + ' ' + label)
        print((('0 EXIT  ENTER: TYPE ID' if STCORE.HAS_KEYS else '0 EXIT / TYPE GUIDE OR Q ID') if title in ('STAT1', 'STAT1 QUICK SOLVE') else ('LEFT / 0 BACK' if STCORE.HAS_KEYS and page == 0 else '0 BACK')) + (((' RIGHT NEXT' if page == 0 else ' RIGHT NEXT LEFT PREV') if STCORE.HAS_KEYS else ' ENTER NEXT - PREV') if len(items) > page_size else ''))
        key = STCORE.read_choice()
        if key == '0':
            STCORE._menu_pages.pop(title, None)
            return key
        if key in ('N', 'P') and any(key == item[0] for item in items):
            return key
        if key == 'N' and len(items) > page_size:
            page = (page + 1) % ((len(items) + page_size - 1) // page_size)
        elif key == 'P':
            if page == 0:
                STCORE._menu_pages.pop(title, None)
                return '0'
            page -= 1
        elif key in aliases or any((key == item[0] for item in items)):
            if len(STCORE._menu_pages) > 32: STCORE._menu_pages.clear()
            selected = aliases.get(key, key)
            STCORE._menu_pages[title] = next(i//page_size for i, item in enumerate(items) if item[0] == selected)
            return selected
        elif key in shortcuts or key in other_shortcuts or (title == 'STAT1' and key.startswith('PT') and key[2:].isdigit() and (1 <= int(key[2:]) <= 24)):
            return key
