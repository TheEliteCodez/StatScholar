# Author: TheEliteCodez
# STFIND - on-demand reference module.
import STCORE

SEARCH_METHODS = (
 ('PRACTICE TEST 1 / Q1-30','X:pretest','pretest pre test practice test 1 review paper'),
 ('FINITE SAMPLE / 5%','X:finite','finite population independence 5% sample size'),
 ('QUIZ 5 / DISTRIBUTIONS','X:quiz5','quiz 5 quiz5 credit cards girls newborn babies metra merta trains packaging rounded table'),
 ('VENN COUNTS / SURVEY','X:venn','venn compost recycle survey overlap contingency counts'),
 ('ALL SELECTED / REPLACEMENT','X:all','all three students recycle with without replacement cumbersome 5% guideline'),
 ('DICE OUTCOMES / ODD EVEN','X:dice','dice die sum odd even subset sample space matching outcomes'),
 ('QUIZ 4 EXAMPLES','X:quiz4','quiz 4 quiz4 probability'),
 ('RAW DATA SUMMARY','S13','mean median half are below shortest 25% quartile standard deviation variance raw list numbers'),
 ('Q1 / LOWEST 25%','S06','quartile shortest 25% lower fourth'),
 ('Q3 / 75%','S07','quartile upper fourth 75%'),
 ('IQR','S08','quartile interquartile middle 50% spread'),
 ('BOXPLOT','G04','quartile boxplot five number summary box whisker'),
 ('SAMPLE VARIANCE','S14','sample variance squared standard deviation'),
 ('MIDRANGE','S15','midrange average minimum maximum'),
 ('COMPARE TWO DATA SETS','S16','compare two groups lists centers spreads'),
 ('DOTPLOT','G05','dotplot dots repeated values'),
 ('HISTOGRAM / CLASSES','G06','histogram frequency bars classes'),
 ('GROUPED FREQUENCY','F08','grouped frequency class width boundaries cumulative'),
 ('Z-SCORE','S12','z score statistically high usual standard score'),
 ('USUAL RANGE','S10','usual unusual range rule statistically high'),
 ('NORMAL CURVE / AXES','G07','normal bell shaped bell curve z score label axes'),
 ('EMPIRICAL RULE','G08','normal bell shaped empirical 68 95 99.7'),
 ('RELATIVE POSITION','G09','relative position compare z scores'),
 ('AT LEAST ONE','P09','at least one complement none'),
 ('BINOMIAL AT LEAST','B05','at least one at least repeated trials'),
 ('BINOMIAL AT MOST','B03','at most no more than'),
 ('BINOMIAL EXACTLY','B02','exactly binomial trials'),
 ('WITHOUT REPLACEMENT','R07','without replacement selected defective box'),
 ('A / B / BOTH / GIVEN','P10','and or both given conditional independent mutually exclusive'),
 ('ROW / COLUMN TABLE','P14','row column two way table'),
 ('EXPECTED VALUE / MONEY','R02','expected value distribution x p(x)'),
 ('PAYOFF / MONEY','R08','money prizes cost profit loss'),
 ('CERTAIN / IMPOSSIBLE','P15','valid certain impossible probability'),
 ('SAMPLING METHODS','D05','sampling convenience systematic stratified cluster random every 10th easiest people sample every group select classrooms'),
 ('PARAMETER / STATISTIC','D04','parameter statistic population percentage'),
 ('SAMPLE / POPULATION','D03','sample population target group'),
 ('OBSERVATIONAL / EXPERIMENT','D06','observational experiment treatment assigned'),
 ('MEASUREMENT LEVELS','D07','nominal ordinal interval ratio data type measurement'),
 ('SIGNIFICANCE / ERROR','D08','significance significant error practical statistical'),
 ('LAW OF LARGE NUMBERS','D09','law large numbers relative frequency empirical probability'))

def recognition(query):
    text=' '+query.lower().replace('-',' ').strip()+' '
    if any(phrase in text for phrase in ('half below','half are below','50% below')): return 'median'
    if 'every kth' in text or 'every k th' in text: return 'sampling'
    # Specific phrases precede broad substrings (NO FEWER is not FEWER).
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
    found=[(label,gid) for label,gid,words in SEARCH_METHODS if query in (label.lower()+' '+words).replace('-',' ') or all(word in (label.lower()+' '+words) for word in query.split())]
    word=recognition(query)
    labels={'not':'NOT / COMPLEMENT','sampling':'SYSTEMATIC / EVERY kth','=':'EXACTLY / X=r','<=':'AT MOST / X<=r','>=':'AT LEAST / X>=r','<':'LESS / X<r','>':'MORE / X>r','[]':'BETWEEN / CHECK ENDPOINTS','one':'AT LEAST ONE / CONTEXT','given':'GIVEN / CONDITIONAL','and':'AND / BOTH / CONTEXT','or':'OR / OVERLAP','sample':'WITHOUT REPLACEMENT','q1':'Q1 / SHORTEST 25%','median':'MEDIAN / HALF BELOW','unusual':'UNUSUAL / CHOOSE CRITERION','empirical':'EMPIRICAL RULE / SD PERCENT'}
    if word: found.insert(0,(labels[word],'W:'+word))
    return found


def search_words():
    query=input('QUESTION WORDS: ').strip()
    if not query: return
    matches=search_methods(query)
    known={gid for label,gid in matches}
    for gid in GUIDES:
        if gid not in known and query.lower() in GUIDES[gid][0].lower():
            matches.append((GUIDES[gid][0].upper(),gid))
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
        elif gid.startswith('Q') or gid.startswith('PT'): question_lookup(gid)
        elif gid.startswith('W:'):
            if gid=='W:empirical': STCORE.call('STNORM','empirical_session')
            else: STCORE.call('STWORDS','word_route',gid[2:],{'experiment_tasks':experiment_tasks,'find_tasks':find_tasks})
        elif gid in ('S06','S07','S08'): STCORE.call('STDATA','raw_session')
        elif gid=='D04': STCORE.call('STSTUDY','parameter_classifier')
        elif gid=='D03': STCORE.call('STSTUDY','population_classifier')
        else: launch_route(gid)

def find_menu():
    while True:
        key=STCORE.menu('FIND A QUESTION',[('1','SEARCH WORDS'),('2','WHAT DOES IT LOOK LIKE?'),('3','WHAT DOES IT ASK?'),('4','HOMEWORK / PRACTICE ID'),('5','GUIDE ID'),('6','TI-84 / FORMULA REFERENCE'),('7','QUESTION STARTERS')])
        if key=='0': return
        if key=='1': search_words()
        elif key=='2': looks_finder()
        elif key=='3': asks_finder()
        elif key=='4': question_lookup()
        elif key=='5':
            gid=input('GUIDE ID (ENTER=BROWSE): ').strip().upper()
            if gid in GUIDES: show_identified(gid)
            else: browse_matrix()
        elif key=='6':
            c=STCORE.menu('FIND > REFERENCE',[('1','TI-84 METHODS'),('2','FORMULA WIZARD'),('3','COUNT / CHOOSE / ARRANGE')])
            if c=='1': ti84_methods()
            elif c=='2': wizard_formula()
            elif c=='3': wizard_counting()
        elif key=='7': question_starters()

def looks_finder():
    key=STCORE.menu('FIND > WHAT DO YOU SEE?',[('1','LIST OF NUMBERS'),('2','VALUE + FREQUENCY'),('3','ROW / COLUMN TABLE'),('4','X + P(X)'),('5','BELL CURVE'),('6','GRAPH'),('7','STORY / WORD PROBLEM')])
    if key=='1':
        c=STCORE.menu('FIND > LIST OF NUMBERS',[('1','FIND STATISTICS'),('2','FIND OUTLIERS'),('3','MAKE GRAPH'),('4','COMPARE TWO LISTS'),('5','NORMAL / Z')])
        if c=='3': graph_tasks()
        elif c!='0': STCORE.call(*{'1':('STDATA','raw_session'),'2':('STGRAPH','raw_outliers'),'4':('STDATA','compare_session'),'5':('STNORM','normal_session')}[c])
    elif key=='2': STCORE.call('STDESC','frequency_session')
    elif key=='3': STCORE.call('STPROB','two_way_session')
    elif key=='4': STCORE.call('STCOUNT','distribution_session')
    elif key=='5': STCORE.call('STNORM','normal_session')
    elif key=='6': graph_tasks()
    elif key=='7': asks_finder()

def asks_finder():
    key=STCORE.menu('FIND > WHAT DOES IT ASK?',[('1','MEAN / MEDIAN / SD'),('2','PROBABILITY'),('3','EXACTLY / AT MOST / AT LEAST'),('4','GRAPH / SHAPE'),('5','SAMPLE / STUDY TYPE'),('6','UNUSUAL / Z-SCORE'),('7','EXPECTED VALUE / MONEY')])
    if key=='1': data_tasks()
    elif key=='2': probability_tasks()
    elif key=='3': trial_tasks()
    elif key=='4': graph_tasks()
    elif key=='5': study_tasks()
    elif key=='6': STCORE.call('STNORM','normal_session')
    elif key=='7': STCORE.call('STCOUNT','payoff_tasks')


def open_reference(name, context, *args):
    for key,value in context.items():
        if key not in globals(): globals()[key]=value
    return globals()[name](*args)
