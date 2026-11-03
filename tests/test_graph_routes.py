import contextlib
import io
import unittest
from unittest.mock import patch
import STCORE as c
import test_graph_expansion as expansion

# Real calculator entry functions and prompts; only the text viewer/format menus are captured.
CASES=[
 ('normal-left','STNDIST','_normal_probability',(100,15),['115',''],['1']),
 ('normal-right','STNDIST','_normal_probability',(100,15),['115',''],['2']),
 ('normal-between','STNDIST','_normal_probability',(100,15),['85','115',''],['3']),
 ('normal-zero-percentile','STNDIST','_normal_percentile',(0,1),['0%'],['3']),
 ('normal-full-percentile','STNDIST','_normal_percentile',(0,1),['100%'],['3']),
 ('normal-cutoff','STNDIST','_normal_percentile',(100,15),['95%'],['3']),
 ('uniform','STUNIF','_uniform_probability',(2,12),['4','8'],['3']),
 ('uniform-cutoff','STUNIF','_uniform_percentile',(2,12),['30%'],['2']),
 ('t','STTPROB','t_probability_session',(9,'2'),['2'],[]),
 ('z-critical','STCIIO','critical_session',('z',),['95%'],['1','0']),
 ('t-critical','STCIIO','critical_session',('t',),['95%','9'],['1','1','0']),
 ('one-sided-bound','STCIIO','critical_session',('z',),['95%','100','2'],['5','1','1']),
 ('one-proportion','STCIPROP','_one_proportion',(),['60','100','95%'],[]),
 ('one-proportion-estimate','STCIPROP','_one_proportion_estimate',(),['approval','.6','100','95%'],[]),
 ('two-proportions','STCIPROP','_two_proportions',(),['60','100','50','100','95%'],[]),
 ('one-mean','STCIMEAN','_one_mean',(),['100','15','36','95%',''],['1']),
 ('two-means','STCIMEAN','_two_means',(),['100','15','36','105','18','40','95%'],['1','1']),
 ('given-margin','STCIMOE','_interval_from_estimate_and_margin',(),['.6','.05'],['1']),
 ('mean-clt','STCLT1','_sample_mean',(True,),['scores','100','15','36','','105'],['1','1','2']),
 ('proportion-clt','STCLT2','_sample_proportion',(True,),['approval','.4','100','','.5'],['1','2']),
 ('chi-goodness','STCHI','session',(),['counts','.05','4','30','10','20','20','0'],['1','1']),
 ('chi-independence','STCHI','session',(True,),['counts','.05','2','2','30','10','10','30'],['1']),
 ('raw-box','STGRAPH','boxplot_data',([(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(20,1)],),[],[]),
 ('ordinary-box','STGRAPH','boxplot_session',(),['1','2','3','4','5'],['2']),
 ('dotplot','STGRAPH','dotplot_session',([(1,1),(1,1),(2,1),(4,1)],),[],[]),
 ('histogram','STHIST2','histogram_session',(None,False,[((0,1),1),((1,1),1),((2,1),1),((3,1),1),((4,1),1)]),[],['1','0']),
 ('grouped','STHIST2','histogram_session',(None,False,[((0,1),1),((1,1),1),((2,1),1),((3,1),1),((4,1),1)]),['0','0','2'],['4','1','0']),
 ('qq','STNDIST','normal_probability_plot',([(1,1),(2,1),(3,1)],),[],['1']),
 ('category','STPROB4','category_session',(),['3','A','1','B','2','C','3'],['1','T','0']),
 ('venn-counts','STVENN2','venn_session',(),['100','60','50','30'],['1','3','0']),
 ('venn-supplied','STPROB','supplied_session',(),['.6','.5','.3'],[]),
 ('venn-conditional','STPROB1','_report',((3,5),(1,2),(3,10),[]),[],['2','2','2','1','0']),
 ('discrete-cdf','STCOUNT4','discrete_tools',(3,lambda i:[((0,1),(1,4)),((2,1),(1,2)),((5,1),(1,4))][i],'DISCRETE'),[],['2','0']),
 ('binomial-answer','STBINFO','show_answer',(4,(1,2),('>=',(2,1),0),(11,16),'BINOMIAL'),[],[]),
 ('hyper','STSAMP2','sample_tasks',(10,4,3),[],['5','0']),
 ('exact-proportion','STCLTF','proportion_fallback',((1,10),4,'PASS',None),['0'],['2']),
 ('exact-uniform-mean','STCLTF','mean_fallback',(.5,1/12**.5,2,'PASS',None),['0','1','.25','.75'],['1','3']),
 ('exact-discrete-mean','STCLTF','mean_fallback',(.5,.5,2,'PASS',None),['2','0','.5','1','.5','0','.5'],['2','3'])]

class GraphRoutes(unittest.TestCase):
    def test_real_entry_functions_build_renderable_descriptors(self):
        helper=expansion.ExpandedGraphs()
        for name,module,function,args,inputs,menus in CASES:
            with self.subTest(name=name):
                seen=[];pending=iter(inputs);choices=iter(menus)
                def capture(title,lines):
                    graph=getattr(lines,'graph',None)
                    if graph:seen.append(graph)
                def result(title,answers,steps=None,default_places=4,drawing=(),graph=None):
                    graph=graph or getattr(drawing,'graph',None)
                    if graph:seen.append(graph)
                def table(title,count,row_at,steps=None,drawing=(),graph=None):
                    graph=graph or getattr(drawing,'graph',None)
                    if graph:seen.append(graph)
                with patch.object(c,'ON_TI',False),patch.object(c,'menu',side_effect=lambda *a,**k:next(choices)),patch.object(c,'view',side_effect=capture),patch.object(c,'results',side_effect=result),patch.object(c,'paged_results',side_effect=table),patch('builtins.input',side_effect=lambda prompt='':next(pending)),contextlib.redirect_stdout(io.StringIO()):
                    c.call(module,function,*args)
                self.assertEqual(list(pending),[]);self.assertEqual(list(choices),[])
                self.assertTrue(seen,name)
                for graph in seen:
                    m,f,a=graph
                    if m in ('STGINFER','STGDIAG'):
                        for key in ('1','2'):
                            with patch.object(c,'menu',return_value=key):helper.render(m,f,*a)
                    else:helper.render(m,f,*a)

    def test_regression_scatter_fit_residual_and_inference_menu_choices(self):
        import sys,types,itertools
        plot=expansion.Plot();keys=types.ModuleType('ti_system');events=itertools.cycle((0,105,0));keys.get_key=lambda mode:next(events)
        inputs=iter(['4','1','2','2','4','3','5','4','4','x','y','.05'])
        choices=iter(['1','2','6','7','8','1','8','2','0'])
        with patch.dict(sys.modules,ti_plotlib=plot,ti_system=keys),patch.object(c,'KEY_STYLE','scan'),patch.object(c,'menu',side_effect=lambda *a,**k:next(choices)),patch.object(c,'view',return_value=None),patch('builtins.input',side_effect=lambda prompt='':next(inputs)):
            c.call('STREGIO','session')
        self.assertFalse(list(inputs));self.assertFalse(list(choices));self.assertEqual(len(plot.frames),5)

if __name__=='__main__':unittest.main()
