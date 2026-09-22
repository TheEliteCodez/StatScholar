# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-21
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Answer tables, loaded only while a result is displayed.
# Formatting is inlined so displaying a result never imports STEFMT.
import STCORE as c


def _answer_text(value, style="D", places=4):
    if isinstance(value, str):
        return value
    if isinstance(value, tuple):
        if style == "F":
            return str(value[0]) + "/" + str(value[1])
        a, b = value
        if style == "P":
            a = a * 100
        scaled, rem = divmod(abs(a)*10**places, b)
        if rem*2 >= b:
            scaled += 1
        sign = "-" if a < 0 and scaled else ""
        digits = str(scaled)
        while len(digits) <= places:
            digits = "0" + digits
        if places:
            return sign + digits[:-places] + "." + digits[-places:] + ("%" if style == "P" else "")
        return sign + digits + ("%" if style == "P" else "")
    if style == "F":
        try:
            if abs(value - int(value)) < 0.0000000001:
                return str(int(value))
        except:
            pass
        return str(round(value, 10)) + " (APPROX)"
    if style == "P":
        value = value * 100
    return ("%.*f" % (places, value)) + ("%" if style == "P" else "")


def results(title, answers, steps=None, default_places=4):
    style, places = ('D', default_places)
    while True:
        lines = []
        for label, value in answers:
            lines.append(label + '=' + _answer_text(value, style, places))
        if c.view(title, lines) in ('back', 'exit'): return
        key = c.menu('ANSWER FORMAT', [('1', 'DONE / NEXT PART'), ('2', 'DECIMAL PLACES'), ('3', 'REDUCED FRACTIONS'), ('4', 'PERCENT PLACES'), ('5', 'SHOW METHOD')])
        if key in ('0', '1'):
            return
        if key == '5':
            c.view('WORK / FORMULA', steps or ['NO ADDITIONAL METHOD'])
            continue
        if key == '3':
            style = 'F'
        else:
            style = 'P' if key == '4' else 'D'
            places = max(0, c.read_int('DECIMAL PLACES: '))


def paged_results(title, count, row_at, steps=None):
    if count <= c.VIEW_LINES:
        c.results(title, [row_at(i) for i in range(count)], steps)
        return
    start = 0
    style, places = ('D', 4)
    while True:
        end = min(count, start + c.VIEW_LINES)
        lines = []
        for i in range(start, end):
            label, value = row_at(i)
            lines.append(label + '=' + _answer_text(value, style, places))
        navigation = c.view(title, ['ROWS ' + str(start + 1) + '..' + str(end) + '/' + str(count)] + lines)
        if navigation == 'exit': return
        if navigation == 'back':
            if start == 0: return
            start = max(0, start - c.VIEW_LINES)
            continue
        key = c.menu('TABLE PAGE / FORMAT', [('N', 'NEXT ROWS'), ('P', 'PREVIOUS ROWS' if start else 'BACK'), ('2', 'DECIMAL PLACES'), ('3', 'REDUCED FRACTIONS'), ('4', 'PERCENT PLACES'), ('5', 'SHOW METHOD')], page_size=6)
        if key == '5':
            c.view('WORK / FORMULA', steps or ['NO ADDITIONAL METHOD'])
            continue
        if key == '0':
            return
        if key == 'N':
            if end < count:
                start = end
        elif key == 'P':
            if start == 0: return
            start = max(0, start - c.VIEW_LINES)
        elif key == '3':
            style = 'F'
        else:
            style = 'P' if key == '4' else 'D'
            places = max(0, c.read_int('DECIMAL PLACES: '))
