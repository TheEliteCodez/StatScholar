# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Question lookup; context globals live on STNAV.
import STCORE
import STNAV


def question_lookup(qid=None):
    if qid is None:
        text = input('Q ID / CH4B 8 / WORDS: ').strip().upper()
        if text in STNAV.QUESTION_INDEX or (text.startswith('PT') and text[2:].isdigit() and 1<=int(text[2:])<=24):
            qid = text
        elif text in [STCORE.call('STNAV','homework_tag',q) for q in STNAV.QUESTION_INDEX]:
            qid = [q for q in STNAV.QUESTION_INDEX if STCORE.call('STNAV','homework_tag',q) == text][0]
        else:
            matches = STCORE.call('STQUEST','search_questions',text)
            if not matches:
                STCORE.view('SEARCH', ['NO MATCH; TRY FEWER WORDS'])
                return
            qid = STCORE.menu('MATCHING QUESTIONS', matches)
    if qid not in STNAV.QUESTION_INDEX and not (qid and qid.startswith('PT') and qid[2:].isdigit() and 1<=int(qid[2:])<=24):
        return
    record, method = STCORE.call('STQUEST','get_question',qid)
    q, title, route, example = record
    while True:
        key = STCORE.menu(q + ' ' + title, [('1', 'SOLVE WITH YOUR NUMBERS'), ('2', 'WORKED HOMEWORK ANSWER'), ('3', 'METHOD GUIDE'),('4','SOURCE / WORDS / COMMAND')])
        if key == '0':
            return
        if key == '1':
            if qid.startswith('PT') and route in ('D03','D04'):
                STCORE.call('STSTUDY','parameter_classifier' if route=='D04' else 'population_classifier')
            elif qid.startswith('PT') and route=='C07':
                STCORE.call('STDICE','dice_session')
            elif qid.startswith('PT') and route in ('B02','B03','B04','B05','B06'):
                STCORE.call('STBWORD','wording_session',{'B02':'=','B03':'<=','B04':'<','B05':'>=','B06':'>'}[route])
            else: STCORE.call('STNAV','launch_route',route)
        elif key == '2':
            STCORE.view(q + ' EXAMPLE', [example, 'USE YOUR OWN NUMBERS TO SOLVE'])
        elif key == '3':
            STCORE.call('STNAV','show_identified',method)
        elif key == '4':
            record=STCORE.call('STQUEST','get_record',qid)
            STCORE.view(qid+' SOURCE',[field.upper()+': '+str(record[field]) for field in ('description','words','methods','parameters','event','command','answer','mistake','completeness')])
