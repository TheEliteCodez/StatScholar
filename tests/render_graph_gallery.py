"""Render the real calculator drawing calls; these are desktop previews."""
from pathlib import Path
import importlib
import sys
import types
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from render_hypothesis_graph import Preview,plt
import matplotlib.image as mpimg

class Gallery(Preview):
    def cls(self):
        if hasattr(self,'fig'):plt.close(self.fig)
        super().cls()
    def show_plot(self):
        folder=ROOT/'artifacts';folder.mkdir(exist_ok=True)
        self.fig.savefig(folder/('graph_'+self.name+'.png'),facecolor='white')
        plt.close(self.fig)

cases=[
 ('normal','STGCURV','show',('NORMAL',100,15,'2',(115,),'x')),
 ('proportion','STGCURV','show',('NORMAL',.4,(.4*.6/100)**.5,'2',(.5,),'p-hat')),
 ('uniform','STGCURV','show',('UNIFORM',2,12,'3',(4,8),'x')),
 ('chi','STGCURV','show',('CHI',0,4,'2',(9.4877,),'chi-square CV',.05,'alpha')),
 ('interval','STGINTR','show',(.6,.504,.696,.95,'p-hat')),
 ('bars','STGBARS','show',(('binomial',10,(1,2)),('>=',(7,1),0),'BINOMIAL')),
 ('cdf','STGBARS','show',(('rows',[((0,1),(1,4)),((2,1),(1,2)),((5,1),(1,4))]),None,'DISCRETE',True)),
 ('box','STGBOX','show',((((1,2,3,4,20,1,5),(20,)),),)),
 ('scatter','STGSCAT','show',([(1,2),(2,4),(3,5)],'x','y',(.6666667,1.5))),
 ('venn','STGDIAG','venn',(100,60,50,30,'6')),
 ('dice','STGDIAG','dice',(('sum','=',7),)),
 ('umean','STGUMEA','show',(0,1,2,('[]',(1,4),(3,4)),.75))]
if __name__=='__main__':
    preview=Gallery('ti_plotlib');sys.modules['ti_plotlib']=preview
    for name,module,function,args in cases:
        preview.name=name
        getattr(importlib.import_module(module),function)(*args)
    fig,axes=plt.subplots(4,3,figsize=(12,10))
    for ax,(name,*rest) in zip(axes.flat,cases):
        ax.imshow(mpimg.imread(ROOT/'artifacts'/('graph_'+name+'.png')));ax.set_axis_off();ax.set_title(name)
    fig.tight_layout();fig.savefig(ROOT/'artifacts'/'graph_gallery.png',dpi=150)
