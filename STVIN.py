# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Keyboard input primitives, loaded only while a menu or pager is active.
import STCORE


def read_raw_key():
    if STCORE.KEY_STYLE == 'ce':
        return STCORE.ti_wait_key()
    # Poll the physical keys; do not infer CE codes from wait_key's presence.
    # One event per press, including when a key remains held across screens.
    while True:
        raw = STCORE.get_key(0)
        if raw in (0, None, ''):
            STCORE._LAST_RAW = None
        elif raw != STCORE._LAST_RAW:
            STCORE._LAST_RAW = raw
            return raw


def normalize_key(key):
    # TI get_key scan codes and CE wait_key codes use different layouts.
    # String-valued readers and desktop U/D/B input remain supported.
    if isinstance(key, str):
        return key.strip().lower()
    if STCORE.KEY_STYLE == "ce":
        return {3:"up",4:"down",2:"left",14:"left",1:"right",15:"right",5:"enter",13:"enter",9:"esc",10:"delete",11:"delete"}.get(key, "")
    return {25:"up",34:"down",24:"left",26:"right",105:"enter",45:"esc",23:"delete"}.get(key, "")


def wait_key():
    if STCORE.HAS_KEYS:
        while True:
            raw = read_raw_key()
            key = normalize_key(raw)
            if key in ("up","down","left","right","enter","esc","u","d","b"):
                return key
    key = input("ENTER NEXT, - PREV, 0 BACK: ").strip().lower()
    return {"":"right","-":"left","0":"esc"}.get(key, normalize_key(key))


def read_choice():
    if not STCORE.HAS_KEYS:
        key = input('> ').strip().upper()
        return {'':'N','-':'P'}.get(key, key)
    text = ''
    while True:
        raw = read_raw_key()
        key = normalize_key(raw)
        if key == 'left': return 'P'
        if key == 'right': return 'N'
        if key == 'esc': return '0'
        if key == 'delete':
            text = text[:-1]
            print('CHOICE: ' + text)
            continue
        if key == 'enter':
            return text or input('CHOICE / ID: ').strip().upper()
        char = ''
        if isinstance(raw, str) and len(raw) == 1:
            char = raw.upper()
        elif STCORE.KEY_STYLE == 'ce':
            if 142 <= raw <= 151: char = str(raw-142)
            elif 243 <= raw <= 251: char = str(raw-242)
            elif raw == 62: char = '0'
            # Menu digits mean physical number keys even in ALPHA lock.
            # Letter IDs remain available via empty ENTER -> text entry.
            elif raw in (178,179,204,173,174,175,168,169,170,153):
                char = str((178,179,204,173,174,175,168,169,170,153).index(raw)+1)[-1]
            elif 154 <= raw <= 179: char = chr(65+raw-154)
        else:
            char = {102:'0',92:'1',93:'2',94:'3',82:'4',83:'5',84:'6',72:'7',73:'8',74:'9'}.get(raw, '')
        if char:
            text += char
            print('> ' + text)
