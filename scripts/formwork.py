import os
import numpy as np, math, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from draw2d import INK,BG,ICE,ICED,RIB,RUST,SAND,MUTED
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, FancyBboxPatch, Rectangle
plt.rcParams["font.family"]="Inter" if "Inter" in [f.name for f in matplotlib.font_manager.fontManager.ttflist] else "DejaVu Sans"
SPAN=16.0; H=9.0; K=0.16; T=0.6; W=2.5
FORM="#f3d9c4"; STEEL="#8c8f93"; CLAMP="#d9d2c8"
def arch(x):
    c=math.cosh(K*SPAN/2); return H*(c-np.cosh(K*x))/(c-1)
def curve(off,n=90,u0=-SPAN/2,u1=SPAN/2):
    u=np.linspace(u0,u1,n); y=arch(u); dy=np.gradient(y,u); nn=np.c_[-dy,np.ones_like(u)]/np.sqrt(1+dy**2)[:,None]
    return np.c_[u,y]+off*nn, nn
OX,OY=0.62,0.36
sh=lambda d: np.array([d*OX,d*OY])
def band(o_out,o_in,d=0.0):
    a,_=curve(o_out); b,_=curve(o_in); return np.r_[a,b[::-1]]+sh(d)
def slab(ax,d0,d1,o_out,o_in,fc,top,z,lw=0.6,ec=INK):
    a,_=curve(o_out)
    ax.add_patch(Polygon(np.r_[a+sh(d1),(a+sh(d0))[::-1]],fc=top,ec=ec,lw=lw,zorder=z))
    ax.add_patch(Polygon(band(o_out,o_in,d0),fc=fc,ec=ec,lw=lw,zorder=z+0.01))
fig=plt.figure(figsize=(15,17),facecolor=BG)
# ================= A: perspective of the travelling formwork =================
ax=fig.add_axes([0.02,0.47,0.96,0.5]); ax.set_facecolor(BG); ax.set_aspect("equal"); ax.axis("off")
ax.text(-13.5,21.6,"Travelling formwork for one whole arch",fontsize=16,fontweight="bold")
ax.text(-13.5,20.6,"One unit = lower arch frame + outer clamp + end bulkhead, on wheels. Filled with plain water from the pumping-tower boom. Working width 2.5 m.",fontsize=10.5,color=MUTED)
ax.fill_between([-14,30],-1.6,0,color="#e3cdb6",zorder=0); ax.plot([-14,30],[0,0],color=INK,lw=0.8,zorder=0.5)
# rails (two, along ring direction = depth axis)
for x in (-SPAN/2-0.9,SPAN/2+0.9):
    p0=np.array([x,0])+sh(-0.6); p1=np.array([x,0])+sh(18)
    ax.plot([p0[0],p1[0]],[p0[1]-0.15,p1[1]-0.15],color=RUST,lw=2.2,zorder=0.8)
# finished arches behind (depth 2.5..12.5)
for k in range(5,0,-1):
    slab(ax,k*W,(k+1)*W,T/2,-T/2,ICE,"#c9dde9",1+0.01*(5-k))
# the new arch being cast at depth 0..2.5 : centering below, bag, clamp above
# centering truss: two arch ribs (at depth 0.2 and 2.3) + cross bracing + skin
for dd in (2.3,0.2):
    a,_=curve(-T/2-0.05); b,_=curve(-T/2-1.0)
    ax.add_patch(Polygon(np.r_[a,b[::-1]]+sh(dd),fc=FORM,ec=RUST,lw=1.0,zorder=3 if dd>1 else 6))
    # truss diagonals
    n=len(a)
    for i in range(0,n-6,6):
        p=a[i]+sh(dd); q=b[i+6]+sh(dd); ax.plot([p[0],q[0]],[p[1],q[1]],color=RUST,lw=0.6,zorder=3.1 if dd>1 else 6.1)
        p=b[i]+sh(dd); q=a[i+6]+sh(dd); ax.plot([p[0],q[0]],[p[1],q[1]],color=RUST,lw=0.6,zorder=3.1 if dd>1 else 6.1)
# bag/ice being cast (front face visible) -- partially filled: lower part dark, top light
slab(ax,0.0,2.5,T/2,-T/2,"#9cc6de","#bcd7e6",4)
# fill level marker
# outer clamp: 4 hinged panels per side drawn as segments on top
segs=np.linspace(-SPAN/2,SPAN/2,7)
for i in range(6):
    a,_=curve(T/2+0.02,n=20,u0=segs[i]+0.08,u1=segs[i+1]-0.08); b,_=curve(T/2+0.35,n=20,u0=segs[i]+0.08,u1=segs[i+1]-0.08)
    ax.add_patch(Polygon(np.r_[b+sh(2.5),(b+sh(0))[::-1]],fc=CLAMP,ec=INK,lw=0.7,zorder=5))
    ax.add_patch(Polygon(np.r_[a,b[::-1]],fc="#c2b9ad",ec=INK,lw=0.7,zorder=5.1))
    # radiator fins on clamp
    for f in np.linspace(0.25,2.25,(9,6,3,3,6,9)[i]):
        m=(b[len(b)//2])+sh(f); nn=curve(0,n=3,u0=(segs[i]+segs[i+1])/2-0.01,u1=(segs[i]+segs[i+1])/2+0.01)[1][1]
        ax.plot([m[0],m[0]+nn[0]*0.45],[m[1],m[1]+nn[1]*0.45],color="#6f6a63",lw=0.8,zorder=5.2)
# hinges
for u in segs[1:-1]:
    p,_=curve(T/2+0.35,n=2,u0=u,u1=u+1e-3); ax.add_patch(Circle(p[0]+sh(0),0.13,fc="#fff",ec=INK,lw=0.8,zorder=6))
# end bulkhead (front face, at depth 0) outline in red dashed to show the plate
ax.add_patch(Polygon(band(T/2+0.05,-T/2-0.05,0),fc="none",ec=INK,lw=2.0,zorder=6.5))
# bogies
for x in (-SPAN/2-0.9,SPAN/2+0.9):
    for dd in (0.4,2.1):
        c=np.array([x,0.35])+sh(dd); ax.add_patch(Circle(c,0.38,fc=INK,zorder=7 if dd<1 else 2.5))
    p=np.array([x,0.8])+sh(0.2); q=np.array([x,0.8])+sh(2.3); ax.plot([p[0],q[0]],[p[1],q[1]],color=INK,lw=3,zorder=6.8)
# jacks at feet (lowering)
for x in (-SPAN/2+0.2,SPAN/2-0.2):
    p=np.array([x,0.8])+sh(0.2); ax.add_patch(Rectangle((p[0]-0.25,p[1]),0.5,0.9,fc=STEEL,ec=INK,lw=0.6,zorder=7))
# fill ports & vent at crown + crane hose
crown,_=curve(T/2+0.35,n=2,u0=0,u1=1e-3); cp=crown[0]+sh(1.25)
WATER="#2f6a8f"
ax.plot([cp[0],cp[0]],[cp[1]+0.45,cp[1]+7.5],color=WATER,lw=2.2,zorder=8)
ax.add_patch(Rectangle((cp[0]-0.45,cp[1]+0.2),0.9,0.5,fc=WATER,ec=INK,lw=0.6,zorder=8.5))
for side in (-1,1):
    fl,_=curve(T/2+0.6,n=60,u0=0,u1=side*7.3) if side>0 else curve(T/2+0.6,n=60,u0=-7.3,u1=0)
    fl=fl+sh(1.25); ax.plot(fl[:,0],fl[:,1],color=WATER,lw=1.6,zorder=8.2)
    p,_=curve(T/2+0.35,n=2,u0=side*7.3,u1=side*7.3+1e-3); p=p[0]+sh(1.25); ax.add_patch(Circle(p,0.22,fc=WATER,ec=INK,lw=1,zorder=8.6))
vp=cp+sh(0.9)+np.array([0,0.1]); ax.add_patch(Circle(vp,0.22,fc="#fff",ec=RUST,lw=1.6,zorder=8.6))
ax.plot([vp[0],vp[0]],[vp[1]+0.2,vp[1]+1.2],color=RUST,lw=1.2,zorder=8.6)
# ---- labels ----
def L(xy,txt,xt,ha="left",c=INK):
    ax.annotate(txt,xy=xy,xytext=xt,fontsize=10,ha=ha,va="center",color=c,arrowprops=dict(arrowstyle="-",color=INK,lw=0.6),zorder=12,bbox=dict(fc=BG,ec="none",pad=1.2))
p,_=curve(-T/2-0.6,n=2,u0=-7.3,u1=-7.3+1e-3); L(p[0]+sh(0.2),"① Centering: aluminium frame,\nHDPE skin + heating film\nfor release; drops 10 cm\nwhen struck",(-13.5,10.0))
p,_=curve(T/2+0.2,n=2,u0=-4.2,u1=-4.2+1e-3); L(p[0]+sh(0.6),"② Outer clamp: 6 hinged panels, 0.6 m gap.\nRadiator fins denser at the feet →\nwater freezes from the bottom up",(-13.5,15.5))
L(np.array([7.3,2.6]),"③ End bulkhead (open side).\nThe other side = face of the previous arch",(10.5,4.6))
L(np.array([-SPAN/2-0.9,0.35])+sh(0.4),"④ Wheels on leapfrog rails / compacted track (guided by compass cables)",(-13.5,-0.9))
L(np.array([SPAN/2-0.2,1.3])+sh(0.2),"⑤ Lowering jacks (mould release)",(12.5,-0.9))
L(cp+np.array([0,6.5]),"⑥ Hose from the pumping-tower boom → manifold\nat the crown → two hoses down to the feet",(5.5,19.3))
p,_=curve(T/2+0.35,n=2,u0=7.3,u1=7.3+1e-3); L(p[0]+sh(1.25),"⑦ Fill ports at left & right feet: water enters\ntogether, rises evenly, arch stays balanced",(14.5,11.2))
L(vp+np.array([0,1.2]),"⑧ Heated vent + pressure valve:\nreleases air, then excess water as it expands",(14.5,14.8))
L(np.array([21.5,9.0]),"arches already frozen\n(self-standing, they become\nthe side wall of the next mould)",(23.0,16.0))
ax.set_xlim(-14,31); ax.set_ylim(-2.2,22.4)
# ================= B: layer detail =================
bx=fig.add_axes([0.03,0.23,0.42,0.22]); bx.set_facecolor(BG); bx.set_aspect("equal"); bx.axis("off")
bx.text(0,4.35,"Layer detail (section through shell thickness)",fontsize=13,fontweight="bold")
# layers horizontal: bottom centering, skin, bag, clamp, fins
bx.add_patch(Rectangle((0,0),9,0.9,fc=FORM,ec=RUST,lw=0.8)); bx.text(9.2,0.45,"centering frame (aluminium)",va="center",fontsize=9)
bx.add_patch(Rectangle((0,0.9),9,0.12,fc="#fff",ec=INK,lw=0.6)); bx.text(9.2,0.98,"HDPE skin + release heating film",va="center",fontsize=9)
bx.add_patch(Rectangle((0,1.02),9,1.5,fc="#9cc6de",ec=INK,lw=0.8)); bx.text(9.2,1.77,"drop-stitch bag filled with water\n→ freezes into 0.6 m of ice",va="center",fontsize=9)
for x in np.linspace(0.4,8.6,12): bx.plot([x,x],[1.06,2.48],color="#6f94ab",lw=0.6)
bx.add_patch(Rectangle((0,2.52),9,0.3,fc=CLAMP,ec=INK,lw=0.8)); bx.text(9.2,2.67,"clamp panel (thin steel)",va="center",fontsize=9)
for x in np.linspace(0.3,8.7,15): bx.add_patch(Rectangle((x-0.05,2.82),0.1,0.7,fc="#6f6a63"))
bx.text(9.2,3.2,"radiator fins → heat rejected to the Martian sky",va="center",fontsize=9)
for x in (0.6,4.5,8.4):
    bx.plot([x,x],[0.9,2.82],color=INK,lw=1.4); bx.add_patch(Circle((x,2.95),0.09,fc=INK))
bx.text(0,-0.45,"Thickness-setting bolts (0.6 m) pass through the bag; holes are sealed with ice after removal.",fontsize=9,color=MUTED)
bx.set_xlim(-0.2,16.5); bx.set_ylim(-0.8,4.6)
# ================= C: numbers =================
cx=fig.add_axes([0.5,0.23,0.48,0.22]); cx.axis("off"); cx.set_xlim(0,1); cx.set_ylim(0,1)
cx.text(0,0.97,"Estimated freezing time (rough calculation)",fontsize=13,fontweight="bold",va="top")
lines=[("Water per arch","±35 t, from Rodwell wells"),
       ("Heat to reject per arch","±11.7 GJ (35 t × latent heat)"),
       ("Heat rejection (radiation, both faces, fins)","±15–25 kW"),
       ("Freezing time → cycle per set","±5–8 days → ±8 days"),
       ("Formwork sets · water demand","6 sets · ±25 t water/day"),
       ("Ring 1 · 2 · 3","±3 · 6.5 · 9.5 months of casting"),
       ("Faster?","add formwork sets + Rodwell wells")]
for i,(a,b) in enumerate(lines):
    y=0.8-i*0.105; cx.text(0,y,a,fontsize=10,va="center"); cx.text(0.56,y,b,fontsize=10,va="center",fontweight="bold")
    cx.plot([0,1],[y-0.05,y-0.05],color="#e2d8cc",lw=0.6)
cx.text(0,0.0,"Assumptions: outside ±−60 °C; water expands ±9% on freezing. To be checked with thermal simulation.",fontsize=8.8,color=MUTED)
# ================= D: cycle =================
dx_=fig.add_axes([0.02,0.015,0.96,0.2]); d=dx_; d.set_facecolor(BG); d.set_aspect("equal"); d.axis("off")
d.text(0,13.6,"One-arch cycle",fontsize=13,fontweight="bold")
steps=["1 · Place empty bag\non the centering","2 · Close clamp\n& end bulkhead","3 · Pump water from tower\nto foot ports (±2–3 h)","4 · Freeze bottom-up\n(±5–8 days)","5 · Release: warm the skin,\nlower the centering,\nopen the clamp","6 · Advance 2.5 m\n→ repeat"]
sc=0.42
for i,stp in enumerate(steps):
    ox=i*23.0+8
    u=np.linspace(-SPAN/2,SPAN/2,60)
    def C(off): 
        c,_=curve(off); return c*sc+np.array([ox,1.5])
    d.plot([ox-8*sc-1,ox+8*sc+1],[1.5,1.5],color=INK,lw=0.6)
    lowered = 0.0
    if i==4: lowered=-0.5
    # centering (present in steps 0-4)
    if i<=4:
        a=C(-T/2-0.05); b=C(-T/2-1.0); off=np.array([0,lowered])
        d.add_patch(Polygon(np.r_[a,b[::-1]]+off,fc=FORM,ec=RUST,lw=0.8))
    # bag state
    if i==0:
        a=C(T/2); b=C(-T/2); d.add_patch(Polygon(np.r_[a,b[::-1]],fc="none",ec="#6f94ab",lw=1,ls=(0,(2,1.5))))
    elif i==1:
        a=C(T/2); b=C(-T/2); d.add_patch(Polygon(np.r_[a,b[::-1]],fc="none",ec="#6f94ab",lw=1,ls=(0,(2,1.5))))
    elif i==2:
        a=C(T/2); b=C(-T/2); d.add_patch(Polygon(np.r_[a,b[::-1]],fc="none",ec="#6f94ab",lw=1))
        for side in (-1,1):
            uu=np.linspace(side*SPAN/2,side*3.5,30); y=arch(uu); dy=np.gradient(y,uu); nn=np.c_[-dy,np.ones_like(uu)]/np.sqrt(1+dy**2)[:,None]
            cc=np.c_[uu,y]; P=np.r_[cc+T/2*nn,(cc-T/2*nn)[::-1]]*sc+np.array([ox,1.5]); d.add_patch(Polygon(P,fc="#9cc6de",ec="none"))
    else:
        a=C(T/2); b=C(-T/2); d.add_patch(Polygon(np.r_[a,b[::-1]],fc="#9cc6de" if i==3 else ICED,ec=INK,lw=0.8))
        if i==3:
            for side in (-1,1):
                uu=np.linspace(side*SPAN/2,side*4.0,30); y=arch(uu); dy=np.gradient(y,uu); nn=np.c_[-dy,np.ones_like(uu)]/np.sqrt(1+dy**2)[:,None]
                cc=np.c_[uu,y]; P=np.r_[cc+T/2*nn,(cc-T/2*nn)[::-1]]*sc+np.array([ox,1.5]); d.add_patch(Polygon(P,fc=ICED,ec="none",zorder=3))
    # clamp
    if i in (1,2,3):
        a=C(T/2+0.05); b=C(T/2+0.45); d.add_patch(Polygon(np.r_[a,b[::-1]],fc=CLAMP,ec=INK,lw=0.6))
    if i==4:
        for side in (-1,1):
            p=np.array([ox+side*6.5*sc,1.5+5.2*sc]); d.annotate("",xy=p+np.array([side*1.6,1.4]),xytext=p,arrowprops=dict(arrowstyle="-|>",color=RUST,lw=1))
        d.annotate("",xy=(ox,1.5+1.6),xytext=(ox,1.5+3.0),arrowprops=dict(arrowstyle="-|>",color=RUST,lw=1))
    if i==2:
        for side in (-1,1):
            p=np.array([ox+side*7.2*sc,1.5+1.2]); d.annotate("",xy=p,xytext=p+np.array([side*1.8,0.4]),arrowprops=dict(arrowstyle="-|>",color="#2f6a8f",lw=1.2))
    if i==3:
        for side in (-1,1):
            p=np.array([ox+side*4.4,2.6]); d.annotate("",xy=p+np.array([-side*0.9,2.0]),xytext=p,arrowprops=dict(arrowstyle="-|>",color=INK,lw=1))
        d.annotate("",xy=(ox,1.5+9*sc+2.4),xytext=(ox,1.5+9*sc+0.5),arrowprops=dict(arrowstyle="-|>",color=RUST,lw=1))
    if i==5:
        d.annotate("",xy=(ox+5.5,0.6),xytext=(ox-5.5,0.6),arrowprops=dict(arrowstyle="-|>",color=RUST,lw=1.5))
        a=C(-T/2-0.05); b=C(-T/2-1.0); d.add_patch(Polygon(np.r_[a,b[::-1]]+np.array([2.2,0.9]),fc=FORM,ec=RUST,lw=0.8,alpha=0.9))
    d.text(ox,-1.6,stp,ha="center",va="top",fontsize=9.5)
    if i<5: d.annotate("",xy=(ox+12.2,4.5),xytext=(ox+10.2,4.5),arrowprops=dict(arrowstyle="-|>",color=MUTED,lw=1))
d.set_xlim(-1,140); d.set_ylim(-7.5,14.5)
fig.savefig("T5_travelling_formwork.png",dpi=120,facecolor=BG)
