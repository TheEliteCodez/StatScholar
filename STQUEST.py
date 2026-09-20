# Author: TheEliteCodez
# STQUEST - homework examples, loaded only for lookup.
QUESTION_DATA = [('Q001', 'DELIVERIES: FREQUENCY MEAN', 'F05', '129/14=9.2143; n=14'), ('Q002', 'RAIN: MEDIAN AND MODE', 'F06', 'n=20; positions 10,11=7; mode=7'), ('Q003', 'ROULETTE 0 AND 00', 'ROULETTE', '38 spaces; single=1/38; odd=9/19'), ('Q004', 'DIE THEN COIN', 'C05', '12 outcomes; H=1/2; 6=1/6; 3 OR H=7/12; 6T=1/12'), ('Q005', 'SCRATCHED LENSES', 'CATEGORY', '5840/12712=730/1589=0.459 (3 places)'), ('Q006', 'LONG-RUN PROPORTION', 'CONCEPT', 'Relative frequency estimates event probability'), ('Q007', 'VALID PROBABILITY?', 'P13', 'Missing value; valid iff 0<=p<=1'), ('Q008', '52-CARD DECK', 'CARDS', '4S=.0192; S OR D=.5000; ace or 2=.1538'), ('Q009', 'GRADE TABLE: MALE', 'P14', '36/81=.4444'), ('Q010', 'BOTH INTOXICATED', 'P12', '61/979=.0623; whole total, not given group'), ('Q011', 'GREEN PEAS', 'CATEGORY', '465/609=76.35%; comparison target missing'), ('Q012', 'SPINNER EVEN', 'SPINNER', '6/12=.5000 IF equal sectors 1..12'), ('Q013', 'SURVEY NOT BELIEVING', 'CATEGORY', '448/678=.6608'), ('Q014', 'GRADES NOT B', 'P14', '41/62=.6613'), ('Q015', 'MEDIUM CONCERN', 'P14', '21/65=.3231'), ('Q016', 'DOG / CAT / BOTH', 'P10', '.6000,.4300,.8000,.6825 (dog GIVEN cat)'), ('Q017', 'COMPOST / RECYCLE', 'P11', '.5700,.4600,.8000,.6667; exclusive NO; independent NO'), ('Q018', 'ONE MISSING P(X)', 'R05', '1-.84=.16'), ('Q019', 'COMPLETE P COLUMN', 'R05', '1-(.1+.2+.2)=.5'), ('Q020', 'JURY EXACTLY / FEW', 'R04', 'Exactly 5=.0004; <=5 approx .0004; unusual YES at .05. 0+ is rounded.'), ('Q021', 'SCORE EXPECTED VALUE', 'R02', 'SUM(score*probability)=6.37'), ('Q022', 'WEBCAM DEFECT TABLE', 'R04', '.904; 1-.904=.096; 2..4=.047; exactly 1=.047 unusual at .05'), ('Q023', 'RAFFLE EV IS WIN %?', 'CONCEPT', 'FALSE: dollars are not a probability'), ('Q024', 'GAME EV IS WIN %?', 'CONCEPT', 'FALSE: long-run average dollars per play'), ('Q025', '8 CAMERAS 5 DEFECTIVE', 'R07', 'P(0..2)=3/28,15/28,5/14; E=5/4'), ('Q026', '6 CAMERAS 4 DEFECTIVE', 'R07', '.0667,.5333,.4000; E=1.3333'), ('Q027', '17 PENS 5 DEFECTIVE', 'R07', '11/34,33/68,3/17,1/68; E=15/17'), ('Q028', 'FOUR SUIT GUESSES', 'WIN_LOSS', 'P(win)=1/256; E=-1.93359375; SD=17.0291422'), ('Q029', 'MARBLE PRIZES AND COST', 'R08', 'NET outcomes 5,1,-1; P=3/42,9/42,30/42; E=-1/7'), ('Q030', 'INSURER EXPECTATION', 'INSURANCE', '259-206000*(1-.999363)=127.78'), ('Q031', 'RAFFLE BUYER / PTO', 'RAFFLE', '-1.67; eight=-13.33; PTO one=1.67; all=400'), ('Q032', 'REPLACED CARDS BINOMIAL?', 'B01', 'TRUE; n=15 p=13/52; independent draws'), ('Q033', 'BINOMIAL TAIL SYMMETRY?', 'SYMMETRY', 'FALSE generally; matching opposite tails requires p=.5'), ('Q034', 'CHICKENPOX 123 ADULTS', 'B13', 'mu=110.7000; SD=3.3272; 100 unusually low; P(100)=.0013'), ('Q035', 'THREE FLIPS COUNT HEADS', 'B11', '1/8,3/8,3/8,1/8; symmetric; mu=1.500 heads; sigma=.866; P(<=2)=7/8'), ('Q036', 'DEPENDENT FLIGHT DELAYS', 'B01', 'NOT BINOMIAL: flights explicitly dependent'), ('Q037', '8 CAMERAS 3 DEFECTIVE', 'R07', '5/14,15/28,3/28; E=3/4'), ('Q038', '26 FLU CALLERS', 'BINOMIAL_MODEL', 'Binomial(26,.16), assuming independence; second part missing'), ('Q039', '18 PEOPLE ELECTRICITY', 'B02', 'Binomial(18,.08); .1196,.8298,.1702,.4260'), ('Q040', 'BLOOD TYPE STANDARD DEV', 'B09', 'SQRT(19*.108*.892)=1.3529168489'), ('Q041', 'BLOOD TYPE EXPECTATION', 'B08', '23*.099=2.277'), ('Q042', 'MATCH THREE HISTOGRAMS', 'B12', 'n=10; top-to-bottom p=.35,.25,.20; centers=3.5,2.5,2'), ('Q043', '39 STUDENTS MATH CLASS', 'B02', 'p=.63; .1281,.6158,.7560,.7122'), ('Q044', '50 EAGLES SURVIVE', 'B02', 'p=.75; .0985,.9084,.3816,.7287'), ('Q045', 'ACCEPT SHIPMENT', 'B03', 'Binomial approximation: n=23,p=.05; P(<=1)=.6794'), ('Q046', 'TORNADOES IN 11 YEARS', 'B04', 'n=11,p=.04; P(<4)=P(<=3)=.9993265560'), ('Q047', '47 DAYS FORGET LUNCH', 'B13', 'mu=18.189; SD=3.33914016; first high=25; P(>=25)=.03071365753; part a labels missing'), ('Q048', '148 BUILDING SUPPORTERS', 'B02', 'n=148,p=.25; .0499,.1478,.8023,.0552,.2504,.8047'), ('Q049', 'ON-TIME BUSES', 'B13', 'n MISSING; p=.64; mu=.64n; SD=.48sqrt(n); integer range then exact tails')]
QUESTION_INDEX = {q[0]: q for q in QUESTION_DATA}
SPECIAL_METHODS = {'ROULETTE': 'P01', 'CARDS': 'P01', 'SPINNER': 'P01', 'CATEGORY': 'F02', 'CONCEPT': 'R02', 'WIN_LOSS': 'R08', 'INSURANCE': 'R08', 'RAFFLE': 'R08', 'BINOMIAL_MODEL': 'B01', 'SYMMETRY': 'B12'}
QUESTION_METHODS = {qid: SPECIAL_METHODS.get(route,route) for qid, title, route, example in QUESTION_DATA}
QUESTION_METHODS['Q006'] = 'F02'
QUESTION_METHODS['Q013'] = 'P02'

def homework_tag(qid):
    i = int(qid[1:])
    if i <= 2:
        return 'EARLIER ' + str(i)
    if i <= 17:
        return 'CH3A ' + str(i - 2)
    if i <= 31:
        return 'CH4A ' + str(i - 17)
    return 'CH4B ' + str(i - 31)


def get_question(qid):
    if qid.startswith('PT'):
        record=get_record(qid)
        return (qid,record['title'],record['methods'][0],record['answer']),record['methods'][0]
    return QUESTION_INDEX[qid], QUESTION_METHODS[qid]


def search_questions(text):
    text=text.upper()
    words=text.split()
    matches=[(q[0],q[1]) for q in QUESTION_DATA if all(word in (q[0]+' '+homework_tag(q[0])+' '+q[1]+' '+q[3]).upper() for word in words)]
    if 'WITHOUT REPLACEMENT' in text:
        matches=[(q[0],q[1]) for q in QUESTION_DATA if q[2]=='R07']
    import STCORE
    return matches+STCORE.call('STPTIDX','search',text)



def get_record(qid):
    import STCORE
    if qid.startswith('PT'):
        bank='STPT'+str((int(qid[2:])-1)//6+1)
    else:
        bank='STQ'+str((int(qid[1:])-1)//10+1)
    return STCORE.call(bank,'get_record',qid)
