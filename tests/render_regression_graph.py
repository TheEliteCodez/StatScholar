"""Desktop previews from native drawing calls; not calculator screenshots."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from render_hypothesis_graph import Preview,plt
import STGSCAT
import STGRT
import STREG

class RegressionPreview(Preview):
    def show_plot(self):
        self.fig.savefig(ROOT/'artifacts'/('regression_'+self.name+'.png'),facecolor='white')
        plt.close(self.fig)

if __name__=='__main__':
    points=list(zip([248,680,286,906,453,907,838,301,434],
                    [25.36,47.6,29.02,70.42,35.71,69.49,54.66,18.07,25.38]))
    result=STREG.fit(points);fit=(result['intercept'],result['slope'])
    preview=RegressionPreview('ti_plotlib');sys.modules['ti_plotlib']=preview
    for name,residual,line_only in (('scatter',False,False),('line',False,True),('residual',True,False)):
        preview.name=name;STGSCAT.show(points,'pages','dollars',fit,residual,line_only)
    for name,key in (('rejection','1'),('pvalue','2')):
        preview.name=name;STGRT.show(result['ts'],result['df'],.05,result['p'],result['tc'],key)
