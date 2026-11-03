import os
import sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from draw2d import INK,BG,ICE,RUST,MUTED
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
plt.rcParams["font.family"]="Inter" if "Inter" in [f.name for f in matplotlib.font_manager.fontManager.ttflist] else "DejaVu Sans"
FORM="#f3d9c4"; CLAMP="#b9b2a8"; RAIL="#3a3a3a"; GROUND="#e9dccb"
W=2.5
fig,axs2=plt.subplots(2,2,figsize=(15,15.5),facecolor=BG); axs=axs2.flatten()
steps=[("1 · Cast and freeze","Centering (below) and clamp panel (above) at slot N.\nRails: segment A underneath, B ahead, C behind.",dict(frozen=2,cent=0,panel=True,rails={"C":-1,"A":0,"B":1},lift=None)),
("2 · Clamp panel lifted by the boom robot","Arch N is frozen. The panel sits on top of the arch, so it can\nbe lifted and taken to another formwork that is starting a cast.",dict(frozen=3,cent=0,panel=False,rails={"C":-1,"A":0,"B":1},lift="panel")),
("3 · Centering drops 10 cm and rolls forward","The centering leaves from under arch N to the open side,\nrolling on segment B to slot N+1.",dict(frozen=3,cent=1,panel=False,rails={"C":-1,"A":0,"B":1},lift=None,move=True)),
("4 · Leapfrog rails","Segment C (rearmost, no longer used) is moved by a\nrover to slot N+2. The panel goes back on; the cycle repeats.",dict(frozen=3,cent=1,panel=True,rails={"A":0,"B":1,"C":2},lift="rail"))]
for ax,(t,sub,st) in zip(axs,steps):
    ax.set_facecolor(BG); ax.set_aspect("equal"); ax.axis("off")
    x0=-3*W
    ax.add_patch(Rectangle((x0-1,-3),8*W+2,22,fc=GROUND,ec="none",zorder=0))
    # slots N-3..N+2 (index k: -3..2)
    for k in range(-3,3):
        x=k*W
        if k<0 or (k==0 and st["frozen"]>=3):
            ax.add_patch(Rectangle((x,0),W,16,fc=ICE,ec="#ffffff",lw=1.2,zorder=1))
        else:
            ax.add_patch(Rectangle((x,0),W,16,fc="none",ec=MUTED,lw=0.8,ls=(0,(3,2)),zorder=1))
        lab="N" if k==0 else (f"N{k:+d}")
        ax.text(x+W/2,-2.4,lab,ha="center",fontsize=8.5,color=MUTED)
    # rails
    for name,k in st["rails"].items():
        x=k*W
        for y in (-0.9,16.4):
            ax.add_patch(Rectangle((x+0.08,y),W-0.16,0.5,fc=RAIL,zorder=3))
        ax.text(x+W/2,17.6,name,ha="center",fontsize=11,fontweight="bold",color=RAIL)
    # centering
    c=st["cent"]*W
    ax.add_patch(Rectangle((c+0.15,0.6),W-0.3,14.8,fc=FORM,ec=RUST,lw=1.4,zorder=4,alpha=0.95))
    ax.text(c+W/2,8,"centering",rotation=90,ha="center",va="center",fontsize=9.5,color=RUST,zorder=5)
    if st.get("move"):
        ax.add_patch(FancyArrowPatch((c-W+0.4,8),(c+0.2,8),arrowstyle="-|>",mutation_scale=16,color=RUST,lw=1.6,zorder=6))
    if st["panel"]:
        ax.add_patch(Rectangle((c+0.05,0.3),W-0.1,15.4,fc=CLAMP,ec=INK,lw=1,hatch="///",alpha=0.55,zorder=5))
        ax.text(c+W+0.3,13.5,"clamp panel\n(on top of arch)",fontsize=9.5,va="center")
    if st["lift"]=="panel":
        ax.add_patch(Rectangle((c+3*W+0.4,6),W-0.1,7,fc=CLAMP,ec=INK,lw=1,hatch="///",alpha=0.55,zorder=5))
        ax.add_patch(FancyArrowPatch((c+W*0.6,10),(c+3*W+0.3,10),connectionstyle="arc3,rad=-0.35",arrowstyle="-|>",mutation_scale=16,color=INK,lw=1.3,zorder=6))
        ax.text(c+4*W+0.8,9.5,"boom robot → to\nanother formwork",fontsize=9.5,va="center")
    if st["lift"]=="rail":
        ax.add_patch(FancyArrowPatch((-W+W/2,18.6),(2*W+W/2,18.6),connectionstyle="arc3,rad=-0.25",arrowstyle="-|>",mutation_scale=16,color=INK,lw=1.3,zorder=6))
        ax.add_patch(Rectangle((-W+0.08,16.4),W-0.16,0.5,fc="none",ec=RAIL,ls=(0,(2,1.5)),zorder=3))
        ax.add_patch(Rectangle((-W+0.08,-0.9),W-0.16,0.5,fc="none",ec=RAIL,ls=(0,(2,1.5)),zorder=3))
        ax.text(0.5*W,21.0,"rover moves C",fontsize=9.5,ha="center")
    ax.text(x0-1,28.5,t,fontsize=13,fontweight="bold")
    ax.text(x0-1,26.6,sub,fontsize=10,color=MUTED,va="top")
    ax.text(3*W+0.3,0.3,"inner foot",fontsize=8.5,color=MUTED); ax.text(3*W+0.3,15.2,"outer foot",fontsize=8.5,color=MUTED)
    ax.annotate("",xy=(3*W+3.6,-1.8),xytext=(3*W+0.4,-1.8),arrowprops=dict(arrowstyle="-|>",color=MUTED))
    ax.text(3*W+0.4,-3.2,"direction of travel",fontsize=8.5,color=MUTED)
    ax.set_xlim(x0-1.5,3*W+13); ax.set_ylim(-4,30)
fig.suptitle("Plan view of one formwork, unrolled straight (arch = strip 2.5 m × 16 m)",x=0.07,ha="left",y=0.995,fontsize=14,fontweight="bold")
fig.tight_layout(rect=(0,0,1,0.985)); fig.savefig("T7_leapfrog_rails.png",dpi=115,facecolor=BG)
