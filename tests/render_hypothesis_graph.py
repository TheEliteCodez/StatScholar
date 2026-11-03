"""Desktop previews from the calculator's drawing calls; not device screenshots."""
from pathlib import Path
import sys
import types

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import STHTPLOT
import STHYRES


class Preview(types.ModuleType):
    def cls(self):
        self.layer=4
        self.fig=plt.figure(figsize=(3.2,2.1),dpi=200)
        self.ax=self.fig.add_axes([0,0,1,1]);self.ax.set_axis_off()

    def window(self,a,b,c,d):
        self.ax.set_xlim(a,b);self.ax.set_ylim(c,d)

    def pen(self,size,style): self.width=1.4 if size=='medium' else .72
    def color(self,*rgb): self.rgb=tuple(value/255 for value in rgb)

    def line(self,x,y,a,b):
        self.ax.plot([x,a],[y,b],color=self.rgb,linewidth=self.width,solid_capstyle='round')

    def text_at(self,row,text,align,clear=1):
        self.layer+=2
        if clear:
            self.ax.add_patch(plt.Rectangle((0,1-row/12),1,1/12,
                transform=self.ax.transAxes,color='white',zorder=self.layer))
        self.ax.text({'left':.01,'center':.5,'right':.99}[align],1-(row-.5)/12,
            text,ha=align,va='center',color=self.rgb,fontsize=7.2,
            fontfamily='DejaVu Sans Mono',transform=self.ax.transAxes,zorder=self.layer+1)

    def show_plot(self):
        folder=ROOT/'artifacts';folder.mkdir(exist_ok=True)
        self.fig.savefig(folder/('hypothesis_'+self.name+'_graph.png'),facecolor='white')
        plt.close(self.fig)


if __name__=='__main__':
    preview=Preview('ti_plotlib');sys.modules['ti_plotlib']=preview
    setup={'parameter':'mu','null':98.8,'alpha':.05,'alternative':'>'}
    result={'ts':3.122,'df':154,'se':.1/3.122,'estimate':98.9}
    probability,critical,_=STHYRES.inference(result['ts'],setup['alpha'],'>',154)
    for preview.name,region in [('rejection','alpha'),('pvalue','p')]:
        STHTPLOT.show(setup,result,probability,critical,region)
