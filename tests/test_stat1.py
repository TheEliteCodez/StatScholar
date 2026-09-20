"""Desktop verification of the modular calculator runtime."""
import ast
import builtins
import contextlib
import importlib.util
import io
import itertools
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
import unittest
from unittest.mock import patch

from test_support import s
getcontext().prec=60


def R(x): return s.as_ratio(str(x))
def dist(xs,ps): return [(R(x),R(p)) for x,p in zip(xs,ps)]
def oracle(n,p,a,b):
    p=Decimal(str(p))
    return float(sum(Decimal(math.comb(n,k))*p**k*(1-p)**(n-k) for k in range(a,b+1)))


NEW_GUIDES = [('F05', 'Mean from Frequency Table', 'FREQUENCY_SESSION', 'VALUES + FREQUENCY; MEAN', 'SUM(x*f)/SUM(f)', '3,6,9,12; f=1,2,6,5: 9.2143'), ('F06', 'Median from Frequency Table', 'FREQUENCY_SESSION', 'FREQUENCY TABLE; MEDIAN', 'USE CUMULATIVE POSITIONS', 'n=20: POS 10 AND 11 BOTH 7'), ('F07', 'Mode from Frequency Table', 'FREQUENCY_SESSION', 'FREQUENCY TABLE; MODE', 'VALUE WITH GREATEST COUNT', '6 HAS f=5; 7 HAS f=6: MODE 7'), ('C05', 'List Sample Space', 'COIN_SESSION', 'DIE THEN COIN; LIST OUTCOMES', 'PAIR EACH DIE VALUE WITH H,T', '6-SIDED DIE + COIN: 12 OUTCOMES'), ('P10', 'Test Mutually Exclusive', 'SUPPLIED_SESSION', 'CAN THESE OCCUR TOGETHER?', 'EXCLUSIVE IF P(BOTH)=0', 'BOTH=.46: NOT EXCLUSIVE'), ('P11', 'Test Independence', 'SUPPLIED_SESSION', 'ARE EVENTS INDEPENDENT?', 'P(BOTH)=P(A)*P(B)', '.57*.69=.3933, NOT .46: NO'), ('P12', 'Direct Intersection Counts', 'TWO_WAY_SESSION', 'AND / BOTH FROM COUNTS', 'BOTH CELL / WHOLE TOTAL', '61/979=0.0623'), ('P13', 'Valid Probability Value', 'VALID_PROBABILITY', 'CAN THIS BE A PROBABILITY?', '0<=p<=1', '0 AND 1 VALID; 1.2 INVALID'), ('P14', 'Two-Way Table Events', 'TWO_WAY_SESSION', 'ROW/COLUMN TABLE; ONE EVENT', 'ROW OR COLUMN / GRAND TOTAL', 'MALE 36 / ALL 81 = 4/9'), ('R04', 'Probability from X/P Table', 'DISTRIBUTION_SESSION', 'TABLE ALREADY GIVES P(X)', 'ADD ONLY MATCHING ROWS', 'P(2<=X<=4)=.024+.018+.005'), ('R05', 'Missing Probability', 'MISSING_PROBABILITY', 'ONE BLANK IN P(X) COLUMN', '1-SUM(KNOWN PROBABILITIES)', '1-(.18+.13+.2+.13+.2)=.16'), ('R06', 'Unusual Event Probability', 'DISTRIBUTION_SESSION', 'IS AN EVENT UNUSUAL?', 'COMPARE EVENT P WITH CUTOFF', '.047<=.05: UNUSUAL'), ('R07', 'Sample Without Replacement', 'SAMPLE_SESSION', 'BOX; TARGET COUNT; SELECT n', 'C(K,k)*C(N-K,n-k)/C(N,n)', 'N=8 K=5 n=2: E=5/4'), ('R08', 'Expected Profit or Loss', 'PAYOFF_SESSION', 'PRIZES, COSTS, PROFIT, LOSS', 'SUM(NET PAYOFF*PROBABILITY)', 'GOLD/SILVER/BLACK: E=-1/7'), ('B11', 'Full Binomial Distribution', 'BINOMIAL_SESSION', 'LIST X AND P(X) FOR TRIALS', 'X=0..n; P=nCx*p^x*(1-p)^(n-x)', '3 FAIR FLIPS: 1,3,3,1 OVER 8'), ('B12', 'Binomial Shape and Symmetry', 'SHAPE_TASKS', 'MATCH GRAPH TO p; SYMMETRY', 'CENTER=np; SYMMETRIC IF p=.5', 'n=10,p=.35: CENTER=3.5'), ('B13', 'Binomial Usual Counts', 'BINOMIAL_SESSION', 'RANGE RULE; FIRST UNUSUAL', 'mu +/- 2*SD; INTEGER ENDPOINTS', '47,.387: FIRST HIGH=25')]

class Arithmetic(unittest.TestCase):
    def test_frequency_original_and_variants(self):
        out=s.frequency_stats([(R(x),f) for x,f in [(3,1),(6,2),(9,6),(12,5)]])
        self.assertEqual(out[:3],(14,(129,1),(129,14)))
        self.assertEqual(s.fixed(out[2],4),'9.2143')
        out=s.frequency_stats([(R(x),f) for x,f in [(6,5),(7,6),(8,3),(9,4),(10,2)]])
        self.assertEqual((out[0],out[3],out[4],out[5]),(20,(7,1),'7',[10,11]))
        out=s.frequency_stats([(R(x),f) for x,f in [(9,2),(2,1),(5,3)]])
        self.assertEqual((out[2],out[3],out[4]),((35,6),(5,1),'5'))
        self.assertEqual(s.frequency_stats([(R(1),1),(R(3),1)])[3],(2,1))
        self.assertEqual(s.frequency_stats([(R(3),2),(R(1),1)])[3],(3,1))
        for rows,mode in [([(1,2),(2,2),(3,1)],'1,2'), ([(1,2),(2,2),(3,2),(4,1)],'DNE'),
                          ([(1,1),(2,1)],'DNE'), ([(2,1)],'2'), ([(1,1),(1,2),(2,2),(99,0)],'1')]:
            self.assertEqual(s.frequency_stats([(R(x),f) for x,f in rows])[4],mode)

    def test_counts_and_supplied_originals(self):
        for a,b,expected in [(5840,12712,'0.459'),(36,81,'0.4444'),(61,979,'0.0623'),
                              (448,678,'0.6608'),(41,62,'0.6613'),(21,65,'0.3231')]:
            self.assertEqual(s.fixed(s.ratio(a,b),3 if a==5840 else 4),expected)
        self.assertEqual(s.answer_text(s.ratio(465,609),'P',2),'76.35%')
        self.assertEqual(s.two_way_values([[11,15,10],[20,18,7]],0,0),(81,36,31,11))
        self.assertEqual(s.two_way_values([[61,73],[238,607]],0,0),(979,134,299,61))
        self.assertEqual(s.two_way_values([[2,3],[4,1]],0,0),(10,5,6,2))
        for a,b,both,want in [('.6','.63','.43','0.6825'),('.57','.69','.46','0.6667')]:
            self.assertEqual(s.fixed(s.rdiv(R(both),R(b)),4),want)
            self.assertEqual(s.radd(s.radd(R(a),R(b)),s.rmul(R(both),(-1,1))),R('.8'))
            self.assertNotEqual(s.rmul(R(a),R(b)),R(both))
        self.assertEqual(s.rmul(R('.5'),R('.4')),R('.2'))

    def test_known_experiments(self):
        roulette=[(str(k),k) for k in range(1,37)]+[('0',0),('00',0)]
        cards=[(str(k)+suit,k) for suit in 'SDCH' for k in range(1,14)]
        coin=[(str(k)+side,k) for k in range(1,7) for side in 'HT']
        for space,kind,query,count in [(roulette,'roulette','1',1),(roulette,'roulette','ODD',18),
                (roulette,'roulette','00',1),(roulette,'roulette','0',1),(roulette,'roulette','17',1),
                (cards,'cards','4S',1),(cards,'cards','S OR D',26),(cards,'cards','<3',8),
                (coin,'coin','H',6),(coin,'coin','6',2),(coin,'coin','3 OR H',7),
                (coin,'coin','6 AND T',1),(coin,'coin','2 OR T',7)]:
            self.assertEqual(len(s.experiment_indices(space,kind,query)),count)
        self.assertEqual(len(coin),12)
        self.assertEqual(len(s.experiment_indices([(str(k),k) for k in range(1,13)],'spinner','EVEN')),6)

    def test_distribution_tables(self):
        self.assertEqual(s.radd((1,1),s.rmul(s.rsum([R(x) for x in ['.18','.13','.2','.13','.2']]),(-1,1))),R('.16'))
        self.assertEqual(s.radd((1,1),s.rmul(s.rsum([R(x) for x in ['.1','.2','.2']]),(-1,1))),R('.5'))
        self.assertEqual(s.distribution_moments(dist([1,2,6,8,9,12,13],['.32','.01','.08','.35','.05','.17','.02']))[0],R('6.37'))
        rows=dist(range(6),['.904','.047','.024','.018','.005','.002'])
        for ev,want in [(('=',0,0),'.904'),(('>=',1,0),'.096'),(('[]',2,4),'.047'),(('=',1,0),'.047')]:
            self.assertEqual(s.table_probability(rows,ev),R(want))
        rows=dist(range(4),['.1','.2','.3','.4'])
        for ev,want in [(('<',2,0),'.3'),(('<=',2,0),'.6'),(('>=',2,0),'.7'),(('[]',1,2),'.5'),(('()',0,3),'.5'),(('[)',1,3),'.5'),(('(]',1,3),'.7')]:
            self.assertEqual(s.table_probability(rows,ev),R(want))

    def test_without_replacement(self):
        for N,K,n,ps,mean in [(8,5,2,['3/28','15/28','5/14'],'5/4'),
                              (6,4,2,['1/15','8/15','2/5'],'4/3'),
                              (17,5,3,['11/34','33/68','3/17','1/68'],'15/17'),
                              (8,3,2,['5/14','15/28','3/28'],'3/4'),
                              (10,4,3,['1/6','1/2','3/10','1/30'],'6/5'),
                              (5,4,3,['3/5','2/5'],'12/5')]:
            rows=s.hyper_distribution(N,K,n)
            self.assertEqual([p for x,p in rows],[R(p) for p in ps])
            self.assertEqual(s.rsum([p for x,p in rows]),(1,1))
            self.assertEqual(s.distribution_moments(rows)[0],R(mean))
            counts={}
            for draw in itertools.combinations(range(N),n):
                k=sum(x<K for x in draw);counts[k]=counts.get(k,0)+1
            self.assertEqual([p for x,p in rows],[s.ratio(counts[x[0]],math.comb(N,n)) for x,p in rows])

    def test_payoffs_precision(self):
        mean,var,sd=s.distribution_moments(dist([-3,270],['255/256','1/256']))
        self.assertEqual(mean,R('-1.93359375'));self.assertAlmostEqual(sd,17.029142196833078)
        self.assertEqual(s.fixed(R('1/256'),6),'0.003906')
        self.assertEqual(s.distribution_moments(dist([5,1,-1],['3/42','9/42','30/42']))[0],R('-1/7'))
        self.assertEqual(s.fixed(s.radd(R(259),s.rmul(R(-206000),R('.000637'))),2),'127.78')
        self.assertEqual(s.fixed(s.rmul(R('-5/3'),R(8)),2),'-13.33')
        self.assertEqual(s.rmul(R('5/3'),R(240)),R(400))
        mean,var,sd=s.distribution_moments(dist([-2,8],['.75','.25']))
        self.assertEqual((mean,var),(R('.5'),R('18.75')))
        self.assertAlmostEqual(sd,math.sqrt(18.75))
        self.assertEqual(s.fixed(R('2.5'),4),'2.5000')
        self.assertEqual(s.fixed(R('-1.005'),2),'-1.01')
        self.assertEqual(s.answer_text(R('7/20'),'P',2),'35.00%')

    def test_binomial_all_assignment_probabilities(self):
        fixtures=[(12,.86,[(5,5),(0,5)],['0.0004','0.0004']),
                  (123,.9,[(100,100)],['0.0013']),
                  (18,.08,[(3,3),(0,2),(3,18),(2,5)],['0.1196','0.8298','0.1702','0.4260']),
                  (39,.63,[(24,24),(0,25),(23,39),(19,26)],['0.1281','0.6158','0.7560','0.7122']),
                  (50,.75,[(40,40),(0,41),(39,50),(36,43)],['0.0985','0.9084','0.3816','0.7287']),
                  (23,.05,[(0,1)],['0.6794']),(11,.04,[(0,3)],['0.9993']),
                  (47,.387,[(25,47)],['0.0307']),
                  (148,.25,[(32,32),(0,31),(33,148),(41,41),(41,148),(0,41)],
                            ['0.0499','0.1478','0.8023','0.0552','0.2504','0.8047'])]
        for n,p,intervals,answers in fixtures:
            for (a,b),want in zip(intervals,answers):
                exact=s.binomial_exact_event(n,R(p),('[]',a,b))
                actual=s.number(exact)
                self.assertAlmostEqual(actual,oracle(n,p,a,b),places=12)
                self.assertEqual(s.fixed(actual,4),want)
        self.assertEqual([s.number(s.binomial_exact_ratio(3,R(.5),k)) for k in range(4)],[.125,.375,.375,.125])
        self.assertAlmostEqual(math.sqrt(19*.108*.892),1.352916848886139)
        self.assertEqual(s.fixed(23*.099,3),'2.277')

    def test_ranges_shapes_and_boundaries(self):
        mu,sd,lo,hi,L,U,first=s.usual_counts(47,.387)
        self.assertAlmostEqual(mu,18.189);self.assertEqual((L,U,first),(12,24,25))
        self.assertIsNone(s.usual_counts(4,.5)[-1])
        self.assertEqual(s.usual_counts(10,.5)[4:],(2,8,9))
        v=[s.number(s.binomial_exact_ratio(10,R(.5),k)) for k in range(11)]
        self.assertAlmostEqual(sum(v[2:9]),1002/1024)
        self.assertAlmostEqual(sum(v[:2]),11/1024)
        for ev,want in [(('<',2,0),5/16),(('<=',2,0),11/16),(('>',2,0),5/16),(('>=',2,0),11/16),(('[]',1,3),7/8), (('<',0,0),0),(('>=',0,0),1),(('<=',99,0),1),(('>',99,0),0)]:
            self.assertAlmostEqual(s.number(s.binomial_exact_event(4,R(.5),ev)),want)
        self.assertEqual([s.number(s.binomial_exact_ratio(4,R(0),k)) for k in range(5)],[1,0,0,0,0])
        self.assertEqual([s.number(s.binomial_exact_ratio(4,R(1),k)) for k in range(5)],[0,0,0,0,1])
        self.assertEqual([s.binomial_shape(p) for p in [.2,.5,.8]],['RIGHT SKEW','SYMMETRIC','LEFT SKEW'])
        for k in range(11):self.assertEqual(s.binomial_exact_ratio(10,R(.2),k),s.binomial_exact_ratio(10,R(.8),10-k))
        self.assertEqual(s.binomial_exact_event(1000,R(.5),('>=',0,0)),(1,1))

    def test_dice(self):
        for n in range(1,5):
            outcomes=list(itertools.product(range(1,7),repeat=n))
            for cutoff in range(6*n+2):
                for code,op in [('2','='),('3','<='),('4','>=')]:
                    self.assertEqual(s.dice_event_count(n,code,cutoff),sum(s.event_match(sum(x),op,cutoff) for x in outcomes))
            for r in range(n+2):self.assertEqual(s.dice_event_count(n,'6',r),sum(x.count(3)==r for x in outcomes))
        self.assertEqual(s.dice_event_count(5,'5'),4651)
        self.assertEqual(s.dice_event_count(5,'2',18),780)
        self.assertEqual(s.dice_event_count(6,'4',20),29715)


class Workflow(unittest.TestCase):
    def run_flow(self,fun,answers):
        pending=iter(answers);outputs=[];prompts=[]
        def read(prompt=''):
            prompts.append(prompt)
            try:return next(pending)
            except StopIteration:raise AssertionError('Unexpected prompt: '+prompt)
        with patch.object(builtins,'input',read),patch.object(s,'view',lambda title,lines:outputs.append((title,lines))),contextlib.redirect_stdout(io.StringIO()):
            fun()
        self.assertEqual(list(pending),[],'Unused scripted inputs')
        return outputs,prompts

    def test_frequency_home_and_format_reuse(self):
        output,prompts=self.run_flow(s.main,['4','2','4','3','1','6','2','9','6','12','5','2','4','3','1','0','0'])
        text=str(output);self.assertIn('MEAN=9.2143',text);self.assertIn('MEAN=129/14',text)
        self.assertEqual(prompts.count('NUMBER OF ROWS: '),1)
        self.assertEqual(prompts[:3],['> ','> ','NUMBER OF ROWS: '])

    def test_two_way_multiple_queries(self):
        output,prompts=self.run_flow(s.two_way_session,['2','2','M','F','A','B','2','3','4','1','1','1','1','2','2','1','0'])
        self.assertEqual(prompts.count('ROW COUNT (NO TOTAL): '),1)
        self.assertIn('P(BOTH)=0.2000',str(output));self.assertIn('ROW GIVEN COLUMN=0.3333',str(output))

    def test_probability_table_reuse(self):
        answers=['4','0','.1','1','.2','2','.3','3','.4', '1','3','2','1', '1','6','1','2','1','1', '2','1','0']
        output,prompts=self.run_flow(s.distribution_session,answers)
        self.assertIn('P=0.3000',str(output));self.assertIn('P=0.5000',str(output));self.assertIn('mu=2.0000',str(output))
        self.assertEqual(prompts.count('NUMBER OF ROWS: '),1)

    def test_binomial_reuse_and_strict_words(self):
        answers=['18','8%', '1','1','3','1','1','3','3','1','1','4','3','1', '1','6','2','5','1','1','0']
        output,prompts=self.run_flow(s.binomial_session,answers)
        for expected in ['0.1196','0.8298','0.1702','0.4260']:self.assertIn(expected,str(output))
        self.assertEqual(prompts.count('HOW MANY TRIALS n: '),1)

    def test_range_workflow(self):
        output,prompts=self.run_flow(s.binomial_session,['47','.387','4','1','','0'])
        self.assertIn('FIRST UNUSUALLY HIGH=25',str(output));self.assertIn('P(X>=FIRST HIGH)=0.0307',str(output))

    def test_rounded_table_not_exact(self):
        output,_=self.run_flow(s.distribution_session,['2','0','0+','1','.9999','1','2','1','5','1','0'])
        self.assertIn('P APPROX',str(output));self.assertIn('EXACT ANSWER UNAVAILABLE',str(output))

    def test_experiment_sessions(self):
        output,_=self.run_flow(lambda:s.experiment_session('roulette'),['2','36','ODD','3','1','BACK'])
        self.assertIn('9/19',str(output))
        output,_=self.run_flow(lambda:s.experiment_session('coin'),['6','LIST','3 OR H','1','6 AND T','1','BACK'])
        self.assertIn('TOTAL=12',str(output));self.assertIn('P(EVENT)=0.5833',str(output));self.assertIn('P(EVENT)=0.0833',str(output))
        output,_=self.run_flow(lambda:s.experiment_session('cards'),['<3','1','BACK'])
        self.assertIn('0.1538',str(output))
        output,_=self.run_flow(lambda:s.experiment_session('spinner'),['2','1','1','2','3','EVEN','1','BACK'])
        self.assertIn('P(EVENT)=0.7500',str(output))

    def test_money_sessions(self):
        output,_=self.run_flow(s.insurance_session,['1','.999363','259','206000','1'])
        self.assertIn('127.78',str(output))
        output,_=self.run_flow(s.raffle_session,['240','2','80','8','1'])
        for x in ['-1.67','-13.33','1.67','400.00']:self.assertIn(x,str(output))
        output,_=self.run_flow(s.payoff_session,['PLAYER','1','3','6','3/42','2','9/42','0','30/42','1','0'])
        self.assertIn('EXPECTED PROFIT=-0.14',str(output))
        output,_=self.run_flow(s.win_loss_session,['1/4','4','270','3','2','6','1','0'])
        self.assertIn('P(WIN)=0.003906',str(output));self.assertIn('SD=17.029142',str(output))

    def test_simple_sessions(self):
        output,_=self.run_flow(s.supplied_session,['57%','69%','46%','1'])
        self.assertIn('INDEPENDENT=NO',str(output));self.assertIn('MUTUALLY EXCLUSIVE=NO',str(output))
        output,_=self.run_flow(s.valid_probability,['100%','1']);self.assertIn('YES',str(output))
        output,_=self.run_flow(s.missing_probability,['3','.1','.2','.2','1']);self.assertIn('MISSING P=0.5000',str(output))
        output,_=self.run_flow(s.category_session,['2','TARGET','7','OTHER','13','1','4','2','1','0']);self.assertIn('35.00%',str(output))
        output,_=self.run_flow(s.sample_session,['8','5','2','3','1','0']);self.assertIn('3/28',str(output))
        output,_=self.run_flow(lambda:s.unusual_result(R('.047')),['','1']);self.assertIn('UNUSUAL=YES',str(output))

    def test_dice_reuse(self):
        output,prompts=self.run_flow(s.solver_multi_dice,['5','5','3','1','6','3','2','1','0'])
        self.assertIn('SUCCESSFUL=4651',str(output));self.assertIn('SUCCESSFUL=1250',str(output))
        self.assertEqual(prompts.count('HOW MANY FAIR 6-SIDED DICE: '),1)

    def test_every_question_and_guide_route(self):
        self.assertEqual(len(s.QUESTION_INDEX),49)
        special={'ROULETTE','CARDS','SPINNER','CATEGORY','CONCEPT','WIN_LOSS','INSURANCE','RAFFLE','BINOMIAL_MODEL','SYMMETRY'}
        for q in s.QUESTION_DATA:
            self.assertTrue(q[2] in s.GUIDES or q[2] in special)
            output,_=self.run_flow(lambda:s.question_lookup(q[0]),['2','0'])
            self.assertTrue(output)
        for gid,title,solver,cue,method,example in NEW_GUIDES:
            self.assertEqual(s.GUIDES[gid][1],solver)
        output,_=self.run_flow(s.main,['Q003','2','0','0']);self.assertIn('1/38',str(output))
        output,_=self.run_flow(s.question_lookup,['RAIN','Q002','2','0']);self.assertIn('mode=7',str(output))

    def test_additional_original_and_changed_workflows(self):
        # All original binomial multi-part probability questions through event menus.
        fixtures=[(123,'.9',[('1','100')],['0.0013']),
                  (39,'.63',[('1','24'),('2','25'),('4','23'),('6','19','26','1')],['0.1281','0.6158','0.7560','0.7122']),
                  (50,'.75',[('1','40'),('2','41'),('4','39'),('6','36','43','1')],['0.0985','0.9084','0.3816','0.7287']),
                  (23,'.05',[('2','1')],['0.6794']), (11,'.04',[('3','4')],['0.9993']),
                  (148,'.25',[('1','32'),('3','32'),('5','32'),('1','41'),('4','41'),('2','41')],
                    ['0.0499','0.1478','0.8023','0.0552','0.2504','0.8047'])]
        for n,p,events,expected in fixtures:
            answers=[str(n),p]
            for event in events: answers += ['1']+list(event)+['1']
            answers += ['0']
            output,_=self.run_flow(s.binomial_session,answers)
            for value in expected:self.assertIn(value,str(output))
        for total,targets,n in [(8,5,2),(6,4,2),(17,5,3),(8,3,2),(10,4,3),(5,4,3)]:
            output,_=self.run_flow(s.sample_session,[str(total),str(targets),str(n),'3','1','0'])
            for x,p in s.hyper_distribution(total,targets,n):self.assertIn(s.answer_text(p,'F'),str(output))
        output,_=self.run_flow(s.frequency_session,['5','6','5','7','6','8','3','9','4','10','2','1'])
        self.assertIn('MEDIAN=7.0000',str(output));self.assertIn('MODE=7',str(output))
        output,_=self.run_flow(s.distribution_session,['3','0','.25','1','?','2','.25','1','2','1','0'])
        self.assertIn('MISSING P=0.5000',str(output));self.assertIn('mu=1.0000',str(output))
        output,_=self.run_flow(s.binomial_session,['3','.5','3','3','1','2','2','3','1','0'])
        self.assertIn('P(0)=1/8',str(output));self.assertIn('sigma=0.866',str(output))
        output,_=self.run_flow(s.payoff_session,['PLAYER','1','3','6','3','2','9','0','30','1','0'])
        self.assertIn('EXPECTED PROFIT=-0.14',str(output))
        for cutoff,want in [('.05','YES'),('.01','NO')]:
            output,_=self.run_flow(lambda:s.unusual_result(R('.04')),[cutoff,'1'])
            self.assertIn('UNUSUAL='+want,str(output))
        output,_=self.run_flow(s.binomial_conditions,['Y','Y','Y','N','1']);self.assertIn('BINOMIAL=NO',str(output))
        output,_=self.run_flow(s.binomial_conditions,['Y','Y','Y','Y','1']);self.assertIn('BINOMIAL=YES',str(output))
        output,_=self.run_flow(s.category_session,['2','GREEN','465','YELLOW','144','1','1','E','.75','1','0'])
        self.assertIn('DIFFERENCE (PERCENT POINTS)=1.3547',str(output))
        output,_=self.run_flow(s.raffle_session,['100','3','50','4','1'])
        self.assertIn('BUYER ALL BOUGHT=-10.00',str(output));self.assertIn('ORGANIZER ALL SOLD=250.00',str(output))
        output,_=self.run_flow(s.insurance_session,['1','.99','100','5000','1']);self.assertIn('50.00',str(output))

    def test_remaining_original_workflows_and_legacy_routes(self):
        output,_=self.run_flow(s.distribution_session,['7','1','.32','2','.01','6','.08','8','.35','9','.05','12','.17','13','.02','2','1','0'])
        self.assertIn('mu=6.3700',str(output))
        output,_=self.run_flow(s.distribution_session,['6','0','.904','1','.047','2','.024','3','.018','4','.005','5','.002',
                      '1','1','0','1','3','1','1','6','2','4','1','1','4','1','1','','1','0'])
        for text in ['P=0.9040','P=0.0960','P=0.0470','UNUSUAL=YES']:self.assertIn(text,str(output))
        output,_=self.run_flow(s.binomial_session,['12','.86','1','1','5','1','1','2','5','1','6','2','5','','1','0'])
        self.assertIn('P=0.0004',str(output));self.assertIn('UNUSUAL=YES',str(output))
        output,_=self.run_flow(s.supplied_session,['.6','.63','.43','1'])
        for value in ['0.6000','0.4300','0.8000','0.6825']:self.assertIn(value,str(output))
        for a,b,both,expected in [('.3','.4','0','MUTUALLY EXCLUSIVE=YES'),('.5','.4','.2','INDEPENDENT=YES')]:
            output,_=self.run_flow(s.supplied_session,[a,b,both,'1']);self.assertIn(expected,str(output))
        for p,want in [('0','YES'),('1','YES'),('-1/2','NO'),('101%','NO')]:
            output,_=self.run_flow(s.valid_probability,[p,'1']);self.assertIn('CAN BE PROBABILITY='+want,str(output))
        for rows,col in [([[6,9,14],[16,12,5]],'2'),([[14,11,12],[2,10,16]],'2')]:
            output,_=self.run_flow(s.two_way_session,['2','3','MALE','FEMALE','A','B','C']+[str(x) for row in rows for x in row]+['1',col,'1','0'])
            self.assertIn('0.6613' if rows[0][0]==6 else '0.3231',str(output))
        output,_=self.run_flow(s.question_lookup,['CH4B 8','2','0']);self.assertIn('.1196',str(output))
        with patch.object(s,'raw_session') as called:
            self.run_flow(s.wizard_raw_data,[]);called.assert_called_once_with()
        output,_=self.run_flow(s.frequency_session,['2','1','2','3','2','5','1'])
        self.assertIn('CUMULATIVE f=4',str(output));self.assertIn('RELATIVE f=0.5000',str(output))

    def test_entry_speed_all_families(self):
        cases=[(['4','1'],'raw_session'),(['4','2'],'frequency_data_session'),(['4','5'],'category_session'),(['4','4'],'two_way_session'),
               (['4','3'],'distribution_session'),(['3','9'],'missing_probability'),(['2'],'wording_session'),
               (['3','2'],'supplied_session'),(['3','7'],'valid_probability'),(['3','6','2'],'payoff_tasks'),
               (['3','6','3'],'insurance_session'),(['3','6','4'],'raffle_session'),(['3','4','1'],'dice_session')]
        for selections,job in cases:
            with patch.object(s,job) as called:
                self.run_flow(s.main,selections+['0']);called.assert_called_once()
            self.assertLessEqual(len(selections),3)
        for key,kind in [('2','coin'),('5','roulette'),('4','cards'),('6','spinner')]:
            with patch.object(s,'experiment_session') as called:
                self.run_flow(s.main,['3','4',key,'0']);called.assert_called_once_with(kind)

    def test_module_sizes_and_wrapping(self):
        from test_support import MODULE_NAMES
        for module in MODULE_NAMES:
            path=Path(__file__).resolve().parent.parent.joinpath(module+'.py')
            self.assertLess(path.stat().st_size,64000,module)
            names=[n.name for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef)]
            self.assertEqual(len(names),len(set(names)),module)
        with patch.object(s,'wait_key',return_value='b'),contextlib.redirect_stdout(io.StringIO()) as out:
            s.view('SHORT',['x'*95,'mean from a very long explanatory sentence with many words'])
        body=out.getvalue().splitlines()
        self.assertTrue(any(line=='x'*30 for line in body))
        self.assertTrue(all(len(line)<=30 for line in body if line))


if __name__=='__main__':unittest.main(verbosity=2)
