# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.
# Experiment event description helper.
import STCORE


def guided_event(kind, word=None):
    key = STCORE.menu('DESCRIBE EVENT', [('1','NUMBER / RANK'),('2','ODD'),('3','EVEN'),('4','SUIT / COLOR / COIN SIDE')])
    if key == '0': return None
    if key in ('2', '3'): return 'ODD' if key == '2' else 'EVEN'
    if key == '4':
        entries = [('1','HEARTS'),('2','DIAMONDS'),('3','CLUBS'),('4','SPADES'),('5','RED'),('6','BLACK')] if kind == 'cards' else [('1','HEADS'),('2','TAILS')] if kind == 'coin' else []
        if not entries:
            STCORE.view('NUMBERED OUTCOMES', ['USE NUMBER, ODD OR EVEN']); return None
        chosen = STCORE.menu('WHICH GROUP?', entries)
        return None if chosen == '0' else entries[int(chosen)-1][1]
    if word is None:
        word = STCORE.choice_pages('NUMBER WORDING', ((('EXACTLY','='),('AT MOST','<='),('AT LEAST','>='),('LESS THAN','<'),('MORE THAN','>'),('BETWEEN','[]')),))
    if word is None: return None
    if kind == 'roulette' and word == '=':
        return input('NUMBER (0 OR 00 ALLOWED): ').strip()
    event = STCORE.call('STBWE','read_event',word)
    if event is None: return None
    op, a, b = event
    if op in ('[]','()','[)','(]'):
        return ('>=' if op[0] == '[' else '>')+STCORE.exact_text(a)+' AND '+('<=' if op[-1] == ']' else '<')+STCORE.exact_text(b)
    return op+STCORE.exact_text(a)
