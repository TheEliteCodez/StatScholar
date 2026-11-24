"""Desktop previews of the dedicated calculator chi-square renderer."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from render_hypothesis_graph import Preview,plt
import STGCHI

class ChiPreview(Preview):
    def show_plot(self):
        self.fig.savefig(ROOT/'artifacts'/('chi_'+self.name+'.png'),facecolor='white')
        plt.close(self.fig)

if __name__=='__main__':
    preview=ChiPreview('ti_plotlib');sys.modules['ti_plotlib']=preview
    for preview.name,key in (('rejection','1'),('pvalue','2')):
        STGCHI.show(10,3,.05,.01856613546,7.814727903,key)
