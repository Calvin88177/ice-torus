import os
import numpy as np, math, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from draw2d import INK,BG,ICE,ICED,RUST,MUTED
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Wedge, FancyBboxPatch
plt.rcParams["font.family"]="Inter" if "Inter" in [f.name for f in matplotlib.font_manager.fontManager.ttflist] else "DejaVu Sans"
FORM="#f3d9c4"; GROUND="#e3cdb6"; TRACK="#cdb397"
SPAN=16; K=0.16; H=9
def arch(x):
    c=math.cosh(K*SPAN/2); return H*(c-np.cosh(K*x))/(c-1)
fig=plt.figure(figsize=(15,10.5),facecolor=BG)
# ---------- plan ----------
ax=fig.add_axes([0.02,0.04,0.52,0.86]); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(Circle((0,0),46,fc=GROUND,ec="none"))
R=28; ri,ro=R-SPAN/2,R+SPAN/2
# compacted tracks under the feet
for rr in (ri,ro):
    ax.add_patch(Wedge((0,0),rr+1.3,0,360,width=2.6,fc=TRACK,ec="none"))
# built arches (sector 40..330 deg)
N=70; d=360/N
for j in range(N):
    a0=j*d
    if 40<=a0<330:
        ax.add_patch(Wedge((0,0),ro,a0,a0+d,width=SPAN,fc=ICE,ec="#ffffff",lw=0.6))
# formwork at angle 25..30 (open side toward 40? builds clockwise: front at 40 going down)
af=40-d; a0,a1=af,af+d
ax.add_patch(Wedge((0,0),ro+0.3,a0,a1,width=SPAN+0.6,fc=FORM,ec=RUST,lw=1.4))
am=math.radians((a0+a1)/2); u=np.array([math.cos(am),math.sin(am)])
pin=u*ri; pout=u*ro
for p in (pin,pout): ax.add_patch(Circle(p,1.1,fc=INK,zorder=6))
# collar & tethers
ax.add_patch(Circle((0,0),2.2,fc="#555",ec=INK,zorder=7)); ax.add_patch(Circle((0,0),3.4,fc="none",ec=RUST,lw=1.6,zorder=7))
nrm=np.array([-u[1],u[0]])
ax.plot([nrm[0]*0.7,pin[0]+nrm[0]*0.7],[nrm[1]*0.7,pin[1]+nrm[1]*0.7],color=RUST,lw=1.6,zorder=5)
ax.plot([-nrm[0]*0.7,pout[0]-nrm[0]*0.7],[-nrm[1]*0.7,pout[1]-nrm[1]*0.7],color=RUST,lw=1.6,zorder=5)
# dashed future path
ang=np.radians(np.linspace(af-40,af,40))
for rr in (ri,ro): ax.plot(rr*np.cos(ang),rr*np.sin(ang),color=RUST,lw=1,ls=(0,(3,3)))
ax.annotate("",xy=(ro*math.cos(math.radians(af-22)),ro*math.sin(math.radians(af-22))),xytext=(ro*math.cos(math.radians(af-12)),ro*math.sin(math.radians(af-12))),arrowprops=dict(arrowstyle="-|>",color=RUST,lw=1.4))
def L(xy,t,xt,ha="left"):
    ax.annotate(t,xy=xy,xytext=xt,fontsize=10.5,ha=ha,va="center",arrowprops=dict(arrowstyle="-",lw=0.7,color=INK),bbox=dict(fc=BG,ec="none",pad=1.5),zorder=10)
L((0,0),"slewing ring at the tower base\n(cables rotate along, never wrap)",(-44,-30))
L(pin*0.55,"short cable = inner-foot radius (20 m)",(10,-38))
L((pin+pout)/2-nrm*0.7,"long cable = outer-foot\nradius (36 m)",(24,48))
L(pout,"outer wheel",(44,20))
L(pin,"inner wheel",(8,-26))
L((0.5*(ri+ro)*math.cos(math.radians(200)),0.5*(ri+ro)*math.sin(math.radians(200))),"arches already frozen",(-44,40))
L((ri*math.cos(math.radians(-15)),ri*math.sin(math.radians(-15))),"compacted regolith track\n(instead of rails)",(26,-48))
L((ro*math.cos(math.radians(af-28)),ro*math.sin(math.radians(af-28))),"direction of travel",(48,-6))
ax.text(-46,56,"Plan view: the formwork is guided by two cables",fontsize=13.5,fontweight="bold")
ax.text(-46,51.5,"The robot only keeps the cables taut; the radius locks itself.",fontsize=10,color=MUTED)
ax.set_xlim(-48,62); ax.set_ylim(-54,58)
# ---------- why radial (small) ----------
bx=fig.add_axes([0.57,0.55,0.41,0.36]); bx.set_aspect("equal"); bx.axis("off")
bx.text(0,15.5,"Why two cables are enough",fontsize=13.5,fontweight="bold")
bx.text(0,13.6,"The formwork frame between inner and outer wheels is 16 m long,\nexactly the difference of the two cables (36 − 20 m). The three points\ncan only be collinear: the formwork always faces the centre.",fontsize=10,va="top")
o=np.array([2,1]); bx.add_patch(Circle(o,0.5,fc="#555"))
pi=o+np.array([20,0])*0.6; po=o+np.array([36,0])*0.6
bx.plot([o[0],po[0]],[o[1]+0.0,po[1]],color=RUST,lw=1.4); bx.plot([o[0],pi[0]],[o[1]+0.5,pi[1]+0.5],color=RUST,lw=1.4)
bx.add_patch(Polygon([(pi[0],pi[1]-0.6),(po[0],po[1]-0.6),(po[0],po[1]+0.9),(pi[0],pi[1]+0.9)],fc=FORM,ec=RUST))
for p in (pi,po): bx.add_patch(Circle(p,0.45,fc=INK,zorder=5))
bx.text((o[0]+pi[0])/2,o[1]+1.4,"20 m",ha="center",fontsize=9.5); bx.text((pi[0]+po[0])/2,o[1]+1.6,"16 m frame",ha="center",fontsize=9.5)
bx.text(o[0],o[1]-1.6,"mast",ha="center",fontsize=9.5)
bx.set_xlim(0,26); bx.set_ylim(-1.5,16.5)
# ---------- ring 2: cable over ring 1 ----------
cx=fig.add_axes([0.57,0.05,0.41,0.45]); cx.set_aspect("equal"); cx.axis("off")
cx.text(-2,40,"For rings 2 and 3",fontsize=13.5,fontweight="bold")
cx.text(-2,37.5,"A straight cable from the mast base would hit ring 1. Two options:",fontsize=10,va="top")
cx.fill_between([-2,70],-1.5,0,color=GROUND); cx.plot([-2,70],[0,0],color=INK,lw=0.8)
cx.plot([0,0],[0,30],color=INK,lw=3)
u=np.linspace(-8,8,60)
cx.fill_between(28+u,0,arch(u),color=ICE); cx.plot(28+u,arch(u),color=INK,lw=1.2)
cx.fill_between(56+u,0,arch(u)-0.6,color=FORM,alpha=0.9); cx.plot(56+u,arch(u),color=MUTED,lw=1.2,ls=(0,(3,2)))
for x in (48,64): cx.add_patch(Circle((x,0.5),0.6,fc=INK))
cx.plot([0,48],[24,0.6],color=RUST,lw=1.3); cx.plot([0,64],[24,0.6],color=RUST,lw=1.3)
cx.plot([0,56],[28,10.2],color="#2f6a8f",lw=1.2,ls=(0,(1.5,2))); cx.add_patch(Circle((56,10.2),0.6,fc="#2f6a8f"))
cx.text(28,4.5,"ring 1",ha="center",fontsize=9.5,fontweight="bold")
cx.text(56,4.5,"ring 2",ha="center",fontsize=9.5,color=MUTED,fontweight="bold")
cx.text(-2,-4,"A · cable from a high point on the mast (±24 m), passing over ring 1",fontsize=9.8,color=RUST,va="top")
cx.text(-2,-7,"B · no cable: a laser on the mast measures the distance to a reflector",fontsize=9.8,color="#2f6a8f",va="top")
cx.text(-2,-9.6,"     on the formwork (a 'virtual' cable; the robot steers to keep it constant)",fontsize=9.8,color="#2f6a8f",va="top")
cx.set_xlim(-3,70); cx.set_ylim(-12,42)
fig.savefig("T6_compass_cables.png",dpi=120,facecolor=BG)
