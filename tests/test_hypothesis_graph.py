import math
from pathlib import Path
import subprocess
import sys
import types
import unittest
from unittest.mock import patch

import STCORE as c
import STHYRES as output
import STHTPLOT as graph
import STGPEN as pen
import STHTLAB as labeler
import STGINK as glyphs


class Plot(types.ModuleType):
    def __init__(self):
        super().__init__('ti_plotlib')
        self.frames=[]

    def cls(self):
        self.lines=[];self.text=[];self.fills=[];self.penmode=None

    def window(self,*limits): self.limits=limits
    def pen(self,*args): self.penmode=args
    def color(self,*rgb): self.rgb=rgb
    def line(self,*points):
        self.lines.append((self.rgb,points))
        if self.penmode and self.penmode[0]=='medium' and self.rgb!=(255,255,255): self.fills.append((self.rgb,points))
    def text_at(self,*args): self.text.append(args)
    def show_plot(self): self.frames.append((self.limits,self.lines,self.text))


class HypothesisGraph(unittest.TestCase):
    def setUp(self):
        # Keep patched renderer owners stable for semantic drawing assertions.
        # Fresh-process tests separately exercise real stage unloading.
        self.enterContext(patch.object(c,'release_topics',lambda *args:None))

    def setup_values(self,alternative='>',degrees=None):
        setup={'alternative':alternative,'alpha':.05,'parameter':'p' if degrees is None else 'mu',
               'null':.5 if degrees is None else 65,'context':'scores','claim':alternative,'random':'PASS'}
        result={'ts':2,'df':degrees,'estimate':.6 if degrees is None else 68.84,
                'se':.05 if degrees is None else 1.92,'name':'TEST','checks':[],'inputs':[],'formula':'test','command':'test'}
        return setup,result

    def test_normal_and_t_curves_use_correct_relative_density(self):
        self.assertEqual(graph.height(0,None),1)
        self.assertEqual(graph.height(0,9),1)
        self.assertAlmostEqual(graph.height(2,None),math.exp(-2))
        self.assertAlmostEqual(graph.height(2,9),(1+4/9)**-5)

    def test_both_screens_show_rejection_first_and_stop_when_back_is_pressed(self):
        setup,result=self.setup_values()
        with patch.object(graph,'show',side_effect=['next','next']) as show:
            self.assertEqual(graph.screens(setup,result,.02,(1.645,)),'next')
        self.assertEqual([call.args[-1] for call in show.call_args_list],['alpha','p'])
        with patch.object(graph,'show',return_value='back') as show:
            self.assertEqual(graph.screens(setup,result,.02,(1.645,)),'back')
        self.assertEqual(show.call_count,1)

    def test_direct_label_boxes_do_not_overlap_for_close_negative_and_two_tailed_marks(self):
        for alt,statistic in [('>',1.6356),('<',-2.1),('!=',2.3),('!=',0)]:
            setup,result=self.setup_values(alt,9);result['ts']=statistic
            p,cv,reject=output.inference(statistic,.05,alt,9)
            for region in ('p','alpha'):
                plt=Plot()
                with patch.dict(sys.modules,ti_plotlib=plt,STHTLAB=labeler,STGPEN=pen,STGINK=glyphs),patch.object(labeler,'tag',wraps=labeler.tag) as tags:
                    graph.show(setup,result,p,cv,region)
                boxes=tags.call_args_list[0].args[-1]
                for i,(left,right,top,bottom) in enumerate(boxes):
                    self.assertTrue(0<=left<right<=319 and 35<=top<bottom<100)
                    for a,b,c,d in boxes[i+1:]:
                        self.assertTrue(right+2<a or left>b+2 or bottom+2<c or top>d+2)
                if alt=='!=':
                    areas=[call.args[2] for call in tags.call_args_list if call.args[1].startswith('p/2' if region=='p' else 'alpha/2')]
                    self.assertEqual(len(areas),2)
                    self.assertLess(areas[0],159.5)
                    self.assertGreater(areas[1],159.5)

    def test_pvalue_tail_shading_and_numeric_labels(self):
        for alt in ('<','>','!='):
            for df in (None,9):
                setup,result=self.setup_values(alt,df)
                p,cv,reject=output.inference(2,.05,alt,df)
                plt=Plot()
                with patch.dict(sys.modules,ti_plotlib=plt,STHTLAB=labeler,STGPEN=pen,STGINK=glyphs),patch.object(glyphs,'ink',wraps=glyphs.ink) as shared_ink,patch.object(labeler,'ink',wraps=labeler.ink) as ink,patch.object(labeler,'tag',wraps=labeler.tag) as tags:
                    self.assertTrue(graph.show(setup,result,p,cv))
                extent=max(3.5,2.7,max(abs(v) for v in cv)+.7)
                blue=[points for rgb,points in plt.fills if rgb==pen.BLUE]
                self.assertTrue(blue)
                for points in blue:
                    score=(points[0]-8)*2*extent/303-extent
                    self.assertTrue(graph.shaded(score+(-1e-10 if alt=='<' else 1e-10 if alt=='>' else 0),2-1e-9 if alt=='!=' else 2,alt))
                labels=[call.args[1] for call in ink.call_args_list+shared_ink.call_args_list]
                self.assertIn('TS=2',labels)
                self.assertIn('H0=%.5g' % setup['null'],labels)
                self.assertIn('%.5g' % result['estimate'],labels)
                self.assertIn(('p/2' if alt=='!=' else 'p')+'=%.4g' % (p/2 if alt=='!=' else p),labels)
                for value in cv:
                    self.assertIn('CV=%.4g' % value,labels)
                    tag=next(call for call in tags.call_args_list if call.args[1]=='CV=%.4g' % value)
                    self.assertAlmostEqual(tag.args[2],pen.position(value,extent))
                native=' '.join(args[1] for args in plt.text)
                self.assertIn('p-VALUE REGION',native)
                self.assertIn('p-VALUE=%.6g' % p,native)
                self.assertIn('LEFT/CLEAR:BACK ENTER:NEXT',native)
                if df is not None:self.assertIn('df=9',native)

    def test_rejection_shading_uses_critical_values_instead_of_test_statistic(self):
        for alt in ('<','>','!='):
            setup,result=self.setup_values(alt,9);result['ts']=.3
            p,cv,reject=output.inference(.3,.05,alt,9);plt=Plot()
            with patch.dict(sys.modules,ti_plotlib=plt,STHTLAB=labeler,STGPEN=pen,STGINK=glyphs),patch.object(glyphs,'ink',wraps=glyphs.ink) as shared_ink,patch.object(labeler,'ink',wraps=labeler.ink) as ink:
                graph.show(setup,result,p,cv,'alpha')
            extent=max(3.5,max(abs(v) for v in cv)+.7)
            boundary=cv[0] if alt=='<' else cv[-1]
            self.assertTrue(plt.fills)
            for rgb,points in plt.fills:
                self.assertEqual(rgb,pen.RED)
                score=(points[0]-8)*2*extent/303-extent
                self.assertTrue(graph.shaded(score+(-1e-9 if alt=='<' else 1e-9 if alt=='>' else 0),boundary-1e-9 if alt=='!=' else boundary,alt))
            labels=[call.args[1] for call in ink.call_args_list+shared_ink.call_args_list]
            self.assertIn(('alpha/2' if alt=='!=' else 'alpha')+'=%.4g' % (.025 if alt=='!=' else .05),labels)
            self.assertIn('FAIL TO REJECT H0',' '.join(args[1] for args in plt.text))

    def test_original_axis_matches_center_estimate_and_critical_cutoffs(self):
        for parameter,null,se,ts,symbol in [('mu',65,2.3477744,1.6355916,'x-bar'),('p',.5,.05,2,'p-hat'),('mu1-mu2',4,1.5,-2,'x1bar-x2bar'),('p1-p2',0,.04,2,'p1hat-p2hat'),('mu_d',2,.5,-1,'d-bar')]:
            setup={'parameter':parameter,'null':null,'alpha':.05,'alternative':'>'}
            result={'ts':ts,'df':9 if parameter.startswith('mu') else None,'se':se,'estimate':null+ts*se}
            cv=(1.833113,);plt=Plot()
            self.assertAlmostEqual(labeler.original(setup,result,ts),result['estimate'])
            with patch.dict(sys.modules,ti_plotlib=plt,STHTLAB=labeler,STGPEN=pen,STGINK=glyphs),patch.object(glyphs,'ink',wraps=glyphs.ink) as shared_ink,patch.object(labeler,'ink',wraps=labeler.ink) as ink:
                graph.show(setup,result,.068177,cv)
            extent=max(3.5,abs(ts)+.7,cv[0]+.7)
            labels=[call.args[1] for call in ink.call_args_list+shared_ink.call_args_list]
            self.assertIn(symbol,labels)
            self.assertIn('H0=%.5g' % null,labels)
            self.assertIn('%.5g' % (null+cv[0]*se),labels)
            original_mark=next(call for call in ink.call_args_list if call.args[1]=='%.5g' % result['estimate'] and call.args[3]==149)
            self.assertAlmostEqual(original_mark.args[2]+3*len(original_mark.args[1]),pen.position(ts,extent))
            self.assertIn((pen.BLACK,(8,77,311,77)),plt.lines)
            self.assertIn((pen.BLACK,(8,109,311,109)),plt.lines)

    def test_graph_keys_bypass_native_pause_and_consume_key_release(self):
        for raw,expected in [(45,'back'),(24,'back'),(102,'back'),
                             ('clear','back'),(105,'next'),(26,'next')]:
            plt=Plot()
            events=iter([105,105,0,25,0,raw,raw,0])
            keys=types.ModuleType('ti_system')
            keys.get_key=lambda mode:next(events)
            with patch.dict(sys.modules,ti_system=keys),patch.object(c,'KEY_STYLE','scan'), \
                 patch.object(plt,'show_plot',side_effect=AssertionError('Do not enter native graph pause')):
                self.assertEqual(pen.wait(plt),expected)
            self.assertEqual(list(events),[])
            self.assertIsNone(c._LAST_RAW)

    def test_wait_key_devices_can_go_back_or_continue(self):
        for raw,expected in [(9,'back'),(2,'back'),(142,'back'),(5,'next'),(1,'next')]:
            plt=Plot()
            keys=types.ModuleType('ti_system')
            events=iter([4,raw])
            keys.wait_key=lambda:next(events)
            with patch.dict(sys.modules,ti_system=keys),patch.object(c,'KEY_STYLE','ce'), \
                 patch.object(plt,'show_plot',side_effect=AssertionError('Do not enter native graph pause')):
                self.assertEqual(pen.wait(plt),expected)
            self.assertEqual(list(events),[])

    def test_graph_step_and_both_review_graph_options(self):
        setup,result=self.setup_values()
        plt=Plot()
        with patch.dict(sys.modules,ti_plotlib=plt,STHTLAB=labeler,STGPEN=pen,STGINK=glyphs),patch.object(c,'ON_TI',True), \
             patch.object(c,'view',return_value=None) as view, \
             patch.object(c,'menu',side_effect=['11','12','0']):
            output.show(setup,result)
        self.assertEqual(len(plt.frames),4)
        titles=[call.args[0] for call in view.call_args_list]
        self.assertNotIn('HT 6: DRAW SAMPLING DISTRIBUTION',titles)
        self.assertIn('HT 9: FINAL CONCLUSION',titles)

    def test_no_graphics_module_returns_to_text_instructions(self):
        setup,result=self.setup_values()
        with patch.dict(sys.modules,ti_plotlib=None):
            self.assertFalse(graph.show(setup,result,.02,(1.645,)))

    def test_fresh_home_graph_path_releases_plot_module(self):
        code="""
import builtins,sys,types
import STAT1,STCORE as c
plot=types.ModuleType('ti_plotlib')
frames=[]
plot.cls=lambda:None
plot.window=plot.pen=plot.color=plot.line=plot.text_at=lambda *args:None
plot.show_plot=lambda:frames.append(True)
sys.modules['ti_plotlib']=plot
c.ON_TI=True
c.view=lambda title,lines:None
answers=iter(['15','1','approval','1','2','.5','.05','60','100','','0','0','0'])
builtins.input=lambda prompt='':next(answers)
STAT1.main()
assert not list(answers)
assert frames==[True,True],frames
assert 'STHTPLOT' not in sys.modules
assert not c.topic_modules(),c.topic_modules()
"""
        run=subprocess.run([sys.executable,'-B','-c',code],
                           cwd=Path(__file__).resolve().parent.parent,
                           capture_output=True,text=True,timeout=15)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)

    def test_fresh_home_back_returns_to_review_and_enter_continues_to_conclusion(self):
        code="""
import builtins,sys,types
import STAT1,STCORE as c
plot=types.ModuleType('ti_plotlib')
plot.cls=lambda:None
plot.window=plot.pen=plot.color=plot.line=plot.text_at=lambda *args:None
def blocked():raise AssertionError('Native pause would trap graph navigation')
plot.show_plot=blocked
sys.modules['ti_plotlib']=plot
keys=types.ModuleType('ti_system');sys.modules['ti_system']=keys
c.ON_TI=True;c.KEY_STYLE='scan'
for close in (45,105):
 events=iter([0,close,close,0]*(2 if close==105 else 1));keys.get_key=lambda mode:next(events)
 titles=[];c.view=lambda title,lines:titles.append(title)
 answers=iter(['15','1','approval','1','2','.5','.05','60','100','','0','0','0'])
 builtins.input=lambda prompt='':next(answers)
 STAT1.main()
 assert not list(answers) and not list(events)
 assert ('HT 9: FINAL CONCLUSION' in titles)==(close==105),titles
 assert not c.topic_modules(),c.topic_modules()
"""
        run=subprocess.run([sys.executable,'-B','-c',code],
                           cwd=Path(__file__).resolve().parent.parent,
                           capture_output=True,text=True,timeout=15)
        self.assertEqual(run.returncode,0,run.stdout+run.stderr)
