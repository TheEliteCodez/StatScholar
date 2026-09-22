# StatScholar - TI-84 Python Statistics Tutor
# Author: Gregory King
# Date: 2026-09-20
# Copyright (c) 2026 Gregory King
# SPDX-License-Identifier: LicenseRef-StatScholar-Free-Use-No-Sale-1.0
#
# License terms: see LICENSE or STAT1.py.

# Quiz 2 examples and small table tools, loaded only on selection.
import STCORE as c

EXAMPLES = (
 ('SOLAR PANELS / PERCENT', '75 PANELS, 45% SHADED. PERCENT OF TOTAL: 75*.45=33.75. APPROXIMATELY 34 WHOLE PANELS. AN EXACT 45% IS INCONSISTENT WITH AN INTEGER COUNT; THE PERCENT MUST BE APPROXIMATE.'),
 ('PARK / EVERY EIGHTH HOUSE', 'RANDOM FIRST HOUSE, THEN EVERY EIGHTH: SYSTEMATIC SAMPLING. NEARBY HOUSEHOLDS MAY NOT REPRESENT ALL PARK USERS; FARTHER-AWAY USERS ARE EXCLUDED AND SOME NEIGHBORS NEVER USE THE PARK. ALSO SPECIFY WHICH RESIDENT TO INTERVIEW. METHOD ALONE DOES NOT ESTABLISH REPRESENTATIVENESS.'),
 ('LIBRARY / EVERY TENTH', 'SURVEY 50 STUDENTS, EVERY TENTH LEAVING THE LIBRARY: SYSTEMATIC. USE A RANDOM START. COVERAGE EXCLUDES STUDENTS NOT USING THAT LIBRARY AT THOSE TIMES. THE SAMPLE MAY REPRESENT THOSE LEAVING DURING THE SAMPLED TIMES, NOT ALL SRJC STUDENTS.'),
 ('RADIO / CALL-IN SURVEY', '1200 LISTENERS CALL ABOUT PAYING MORE FOR CLEAN ENERGY. VOLUNTARY RESPONSE: PEOPLE CHOOSE TO PARTICIPATE, OFTEN THOSE WITH STRONG OPINIONS. LISTENERS MAY NOT REPRESENT ALL PEOPLE. A LARGE RESPONSE COUNT DOES NOT REMOVE BIAS.'),
 ('COLLEGE / ALL US ADULTS', '520 RANDOM COLLEGE MEMBERS USED TO CLAIM 38% OF ALL US ADULTS VISIT A DOCTOR. WRONG SAMPLING FRAME: COLLEGE MEMBERS DO NOT REPRESENT ALL US ADULTS. RANDOM SELECTION WITHIN A COLLEGE DOES NOT FIX UNDERCOVERAGE OF OTHER ADULTS.'),
 ('HURRICANES / FREQUENCIES', 'CATEGORIES 1..5 HAVE COUNTS 109,72,71,18,3; TOTAL 273. RELATIVE f=f/273. CATEGORY 4: 18/273=.0659. CUMULATIVE THROUGH 3: 252/273=.9231. AT LEAST 3 INCLUDES 3,4,5: 92/273=.3370. THE PRINTED CUMULATIVE COLUMN IS RELATIVE FREQUENCY, ENDING AT 1; CUMULATIVE COUNTS END AT 273.'),
 ('1936 POLL / QUOTA / BIAS', 'LISTS OF SUBSCRIBERS, CAR OWNERS, PHONE USERS AND CLUB MEMBERS COULD OVERREPRESENT AFFLUENT VOTERS DURING THE DEPRESSION. COVERAGE BIAS. 2.3 MILLION OF 10 MILLION REPLIED: 23%. NONRESPONSE CAN BIAS RESULTS IF RESPONDENTS DIFFER FROM NONRESPONDENTS; LOW RESPONSE ALONE DOES NOT MEASURE THE BIAS. THESE ARE NONSAMPLING ERRORS. QUOTA SAMPLING FILLS SPECIFIED SUBGROUP COUNTS. STRATIFIED IS THE LIKELY CLASSROOM COMPARISON, BUT STRATIFIED RANDOM SAMPLING REQUIRES RANDOM SELECTION WITHIN EACH GROUP; QUOTAS ALONE DO NOT.'))


def quiz_menu():
    while True:
        key=c.menu('QUIZ 2 / WORKED EXAMPLES',[(str(i+1),title) for i,(title,body) in enumerate(EXAMPLES)])
        if key=='0': return
        i=int(key)-1
        c.call('STSTUDY','definition_pages','QZ20'+key,EXAMPLES[i][1])
        if i in (0,5):
            action=c.menu('SOLVE WITH YOUR NUMBERS',[('1','OPEN SOLVER')])
            if action=='1':
                if i==0: percent_session()
                else: frequency_tools()


def percent_session():
    total=c.read_exact('TOTAL: ')
    rate=c.read_exact('PERCENT (45% OR .45): ')
    answer=c.rmul(total,rate)
    c.results('PERCENT OF TOTAL',[('ANSWER',answer)],['TOTAL * PERCENT/100','ENTER 45% OR .45, NOT 45','FOR WHOLE ITEMS, ROUND ONLY IF THE QUESTION ALLOWS AN APPROXIMATION.','NEAREST WHOLE: '+c.fixed(answer,0)])


def frequency_lines(rows):
    total=sum(f for x,f in rows)
    if total<=0: raise ValueError('NEED POSITIVE TOTAL FREQUENCY')
    cumulative=0
    for x in c.exact_sorted(set(x for x,f in rows)):
        f=sum(f for value,f in rows if c.compare_exact(value,x)==0)
        cumulative+=f
        yield 'VALUE='+c.exact_text(x)+' COUNT='+str(f)
        yield 'RELATIVE='+c.fixed(c.ratio(f,total),4)
        yield 'CUM COUNT='+str(cumulative)
        yield 'CUM REL='+c.fixed(c.ratio(cumulative,total),4)


def frequency_event(rows,op,cutoff):
    total=sum(f for x,f in rows)
    selected=0
    for x,f in rows:
        comparison=c.compare_exact(x,cutoff)
        if {'=':comparison==0,'<=':comparison<=0,'>=':comparison>=0,'<':comparison<0,'>':comparison>0}[op]: selected+=f
    return c.ratio(selected,total)


def frequency_tools(rows=None):
    if rows is None: rows=c.call('STDMATH','read_frequency_rows')
    while True:
        key=c.menu('FREQUENCY TABLE',[('1','RELATIVE / CUMULATIVE'),('2','EXACTLY'),('3','AT MOST'),('4','AT LEAST'),('5','LESS THAN'),('6','MORE THAN'),('7','BETWEEN')])
        if key=='0': return
        if key=='1': c.call('STSTUDY','definition_pages','TABLE / IN VALUE ORDER','; '.join(frequency_lines(rows)))
        elif key=='7':
            event=c.call('STBWE','read_event','[]')
            if event:
                total=sum(f for x,f in rows)
                matching=sum(f for x,f in rows if c.event_match(x,*event))
                c.results('FREQUENCY BETWEEN',[('PROPORTION',c.ratio(matching,total))],['MATCHING COUNTS / TOTAL'])
        else:
            op={'2':'=','3':'<=','4':'>=','5':'<','6':'>'}[key]
            cutoff=c.read_exact('CATEGORY / VALUE CUTOFF: ')
            c.results('FREQUENCY > X'+op+c.exact_text(cutoff),[('PROPORTION',frequency_event(rows,op,cutoff))],['SUM MATCHING COUNTS / TOTAL','USE COUNTS BEFORE ROUNDING','ORDERED CATEGORIES OR NUMERIC VALUES'])
