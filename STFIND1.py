# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Word recognition and method search; context globals live on STFIND.
import STCORE
import STFIND


def recognition(query):
    text=' '+query.lower().replace('-',' ').strip()+' '
    if any(phrase in text for phrase in ('half below','half are below','50% below')): return 'median'
    if 'every kth' in text or 'every k th' in text: return 'sampling'
    groups=(('one',('at least one',)),('<=',('at most','no more than','or fewer','or less','not more than')),
            ('>=',('at least','or more','no fewer than')),('<',('less than','fewer than','below')),
            ('>',('more than','greater than','over')),('[]',('between','through')),('=',('exactly','p(x=','equal to')),
            ('given',('given',)),('sample',('without replacement',)),('q1',('shortest 25%','lowest 25%')),
            ('median',('half below','half are below','50% below')),('unusual',('unusual','usual','statistically high','statistically low')),
            ('not',('not','none','complement','does not')),('and',('both','and')),('or',('or',)))
    if 'standard deviations' in text and ('two' in text or '2' in text): return 'empirical'
    for token,phrases in groups:
        if any((' '+phrase+' ') in text or phrase=='p(x=' and phrase in text for phrase in phrases): return token
    return None


def search_methods(query):
    query=' '.join(query.lower().replace('-',' ').split())
    if query.startswith('every ') and any(c.isdigit() for c in query): query='systematic'
    aliases={'happen to be there':'convenience','easiest':'convenience','convenient':'convenience','sample from every group':'stratified','select entire groups':'cluster','observed':'observational','surveyed without intervention':'observational'}
    query=aliases.get(query,query)
    found=[(label,gid) for label,gid,words in STFIND.SEARCH_METHODS if query in (label.lower()+' '+words).replace('-',' ') or all(word in (label.lower()+' '+words) for word in query.split())]
    word=recognition(query)
    labels={'not':'NOT / COMPLEMENT','sampling':'SYSTEMATIC / EVERY kth','=':'EXACTLY / X=r','<=':'AT MOST / X<=r','>=':'AT LEAST / X>=r','<':'LESS / X<r','>':'MORE / X>r','[]':'BETWEEN / CHECK ENDPOINTS','one':'AT LEAST ONE / CONTEXT','given':'GIVEN / CONDITIONAL','and':'AND / BOTH / CONTEXT','or':'OR / OVERLAP','sample':'WITHOUT REPLACEMENT','q1':'Q1 / SHORTEST 25%','median':'MEDIAN / HALF BELOW','unusual':'UNUSUAL / CHOOSE CRITERION','empirical':'EMPIRICAL RULE / SD PERCENT'}
    if word: found.insert(0,(labels[word],'W:'+word))
    return found


def search_words():
    query=input('QUESTION WORDS: ').strip()
    if not query: return
    matches=search_methods(query)
    known={gid for label,gid in matches}
    for gid in STFIND.GUIDES:
        if gid not in known and query.lower() in STFIND.GUIDES[gid][0].lower():
            matches.append((STFIND.GUIDES[gid][0].upper(),gid))
    for qid,title in STCORE.call('STQUEST','search_questions',query):
        matches.append((qid+' '+title,qid))
    for qid,title in STCORE.call('STPRE','search',query):
        matches.append((title,qid))
    if not matches:
        STCORE.view('FIND > NO MATCH',['TRY WHAT DOES IT LOOK LIKE','OR WHAT DOES IT ASK.'])
        return
    while True:
        key=STCORE.menu('FIND > METHODS FIRST',[(str(i+1),label) for i,(label,gid) in enumerate(matches)])
        if key=='0': return
        gid=matches[int(key)-1][1]
        if gid.startswith('PR:'):
            STCORE.call('STPRE','pretest_menu',int(gid[3:]))
        elif gid.startswith('X:'):
            STCORE.call(*{'X:venn':('STVENN','venn_session'),'X:all':('STVENN','selection_session'),'X:dice':('STDICE','dice_session'),'X:quiz4':('STQUIZ4','quiz_menu'),'X:quiz5':('STQUIZ5','quiz_menu'),'X:pretest':('STPRE','pretest_menu'),'X:finite':('STFINITE','finite_check')}[gid])
        elif gid.startswith('Q') or gid.startswith('PT'): STFIND.question_lookup(gid)
        elif gid.startswith('W:'):
            if gid=='W:empirical': STCORE.call('STNORM','empirical_session')
            else: STCORE.call('STWORDS','word_route',gid[2:],{'experiment_tasks':STFIND.experiment_tasks,'find_tasks':STFIND.find_tasks})
        elif gid in ('S06','S07','S08'): STCORE.call('STDATA','raw_session')
        elif gid=='D04': STCORE.call('STSTUDY','parameter_classifier')
        elif gid=='D03': STCORE.call('STSTUDY','population_classifier')
        else: STFIND.launch_route(gid)
