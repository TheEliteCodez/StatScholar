import contextlib
import io
import unittest
import sys
from unittest.mock import patch
import STCORE as c
import STGSCAT as graph
import STREGTXT as text_graph
import test_graph_expansion as expansion


class RegressionLineGraph(unittest.TestCase):
    def test_line_equation_and_plotted_endpoints_for_both_graph_modes(self):
        for points,fit in [([(1,0),(2,2),(3,1),(4,6)],(-3,2)),
            ([(1,11),(2,7),(3,8),(4,3)],(12,-2)),
            ([(1,5),(2,5),(3,5)],(5,0)),
            ([(2008,2),(2010,3),(2012,5)],(-2006,1))]:
            for line_only in (False,True):
                with patch.dict(sys.modules,STGSCAT=graph),patch.object(graph,'axis_number',wraps=graph.axis_number) as ticks:
                    plot=expansion.ExpandedGraphs().render('STGSCAT','show',points,'year','sales',fit,False,line_only)
                lines,labels=plot.frames[0]
                red=[coords for color,coords in lines if color==(210,45,45)]
                self.assertEqual(len(red),1)
                self.assertEqual(sum(color==(0,100,210) for color,coords in lines),0 if line_only else 2*len(points))
                xs=[call.args[1:] for call in ticks.call_args_list if len(call.args)==4]
                ys=[call.args[1:] for call in ticks.call_args_list if len(call.args)==5]
                xv,xp,_=xs[0];xv2,xp2,_=xs[-1]
                yv,_,yp,_=ys[0];yv2,_,yp2,_=ys[-1]
                for px,py in (red[0][:2],red[0][2:]):
                    x=xv+(px-xp)*(xv2-xv)/(xp2-xp)
                    y=yv+(py-yp)*(yv2-yv)/(yp2-yp)
                    self.assertAlmostEqual(y,fit[0]+fit[1]*x,places=9)
                    self.assertTrue(60-1e-8<=px<=306+1e-8 and 61-1e-8<=py<=149+1e-8)
                equation='yhat=%.6g*x %s %.6g' % (fit[1],'-' if fit[0]<0 else '+',abs(fit[0]))
                self.assertIn((3,equation,'center'),labels)
                self.assertIn((2,'y: sales','left'),labels)
                self.assertIn((11,'x: year','center'),labels)

    def test_scatter_only_and_residual_graphs_do_not_show_a_regression_equation(self):
        for fit,residual in ((None,False),((2,.7),True)):
            plot=expansion.ExpandedGraphs().render('STGSCAT','show',[(1,2),(2,4),(3,5)],'x','y',fit,residual)
            self.assertFalse(any(row==3 for row,text,align in plot.frames[0][1]))

    def test_text_fallback_supplies_equation_and_two_points_on_the_line(self):
        pages=[]
        with patch.object(c,'view',side_effect=lambda title,rows:pages.append((title,list(rows)))):
            text_graph.show([(1,0),(2,2),(4,6)],'year','sales',(-3,2),False,True)
        title,rows=pages[0]
        self.assertEqual(title,'REGRESSION LINE')
        self.assertIn('yhat=2*x - 3',rows)
        self.assertIn('(1, -1)',rows)
        self.assertIn('(4, 5)',rows)
        self.assertFalse(any(row.startswith('SCATTERPLOT') for row in rows))

    def test_menu_routes_all_four_graph_modes(self):
        calls=[]
        def dispatch(module,function,*args):
            if module=='STREGIN':return [(1,2),(2,4),(3,5)],'x','y',.05
            if module=='STREG':return {'intercept':1,'slope':2,'r':None}
            if module=='STGSCAT':calls.append(args);return True
        with patch.object(c,'call',side_effect=dispatch),patch.object(c,'menu',side_effect=['2','6','7','11','0']):
            import STREGIO
            STREGIO.session()
        self.assertEqual([(a[3],a[4],a[5]) for a in calls],
                         [((1,2),False,False),((1,2),False,True),((1,2),True,False),(None,False,False)])
