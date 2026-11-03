import os
import numpy as np, math, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from draw2d import INK,BG,ICE,ICED,RIB,RUST,SAND,MUTED
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["svg.fonttype"]="none"
from matplotlib.patches import Polygon, Circle, Wedge, FancyArrowPatch
plt.rcParams["font.family"]="Inter" if "Inter" in [f.name for f in matplotlib.font_manager.fontManager.ttflist] else "DejaVu Sans"
SPAN=16.0; H=9.0; K=0.16
def arch(x):  # x in [-8,8] relative to ring centerline
    c=math.cosh(K*SPAN/2); return H*(c-np.cosh(K*x))/(c-1)
GAP=12.0
RINGS=[28,28+SPAN+GAP,28+2*(SPAN+GAP)]   # 28, 56, 84 m
REACH=95
NB=12                # render subdivisions only (each slice is ONE whole arch)
SW=2.5               # whole-arch slice width at ring centreline
def ring_tiles(R,tw=SW,th0=0,th1=2*np.pi):
    N=int(round(2*np.pi*R/tw)); us=np.linspace(-SPAN/2,SPAN/2,NB+1)
    # arc-length-equal bands
    xs=np.linspace(-SPAN/2,SPAN/2,400); ys=arch(xs); s=np.r_[0,np.cumsum(np.hypot(np.diff(xs),np.diff(ys)))]
    us=np.interp(np.linspace(0,s[-1],NB+1),s,xs)
    T=[]
    for j in range(N):
        a0=2*np.pi*j/N; a1=2*np.pi*(j+1)/N
        if ((a0-th0)%(2*np.pi))+(a1-a0)>((th1-th0)%(2*np.pi) or 2*np.pi)+1e-9: continue
        for b in range(NB):
            P=[]
            for (u,a) in ((us[b],a0),(us[b],a1),(us[b+1],a1),(us[b+1],a0)):
                r=R+u; P.append((r*math.cos(a),r*math.sin(a),float(arch(u))))
            T.append((b,np.array(P)))
            # joint strip at a0 (white line between whole-arch slices)
            d=0.14
            Q=[]
            for (u,a) in ((us[b],a0-d/(R+us[b])),(us[b],a0+d/(R+us[b])),(us[b+1],a0+d/(R+us[b+1])),(us[b+1],a0-d/(R+us[b+1]))):
                r=R+u; Q.append((r*math.cos(a),r*math.sin(a),float(arch(u))+0.02))
            T.append((-1,np.array(Q)))
    return T,N
# ---------- projection ----------
AZ=math.radians(-35); EL=math.radians(28)
def proj(P):
    P=np.atleast_2d(P); x,y,z=P[:,0],P[:,1],P[:,2]
    xr=x*math.cos(AZ)-y*math.sin(AZ); yr=x*math.sin(AZ)+y*math.cos(AZ)
    return np.c_[xr, z*math.cos(EL)+yr*math.sin(EL)], yr*math.cos(EL)-z*math.sin(EL)  # depth: larger = nearer
import matplotlib.colors as mc
def BC(b):
    f=1-abs((b+0.5)/NB*2-1)   # 0 at feet, 1 at crown
    return mc.to_hex(np.array(mc.to_rgb("#7eaac4"))*(1-f)+np.array(mc.to_rgb("#d3e5ef"))*f)
def draw3d():
    fig,ax=plt.subplots(figsize=(13,9),facecolor=BG); ax.set_facecolor(BG); ax.set_aspect("equal"); ax.axis("off")
    polys=[]
    # ground disc
    th=np.linspace(0,2*np.pi,200)
    g,_=proj(np.c_[102*np.cos(th),102*np.sin(th),0*th]); ax.add_patch(Polygon(g,fc="#e3cdb6",ec="none",zorder=0))
    # ring 1 complete
    T,_=ring_tiles(RINGS[0])
    for b,P in T: polys.append((P,"#ffffff" if b<0 else BC(b),"#ffffff" if b<0 else BC(b),0.3))
    # ring 2 partial (built sector), front at angle th_f
    thf=math.radians(20)
    T2,_=ring_tiles(RINGS[1],th0=thf+math.radians(70),th1=thf)
    for b,P in T2: polys.append((P,"#ffffff" if b<0 else BC(b),"#ffffff" if b<0 else BC(b),0.3))
    # foundation footprint ring 2 rest & ring 3 (dashed)
    for R in RINGS[1:]:
        for rr in (R-SPAN/2,R+SPAN/2):
            g,_=proj(np.c_[rr*np.cos(th),rr*np.sin(th),0*th]); ax.plot(g[:,0],g[:,1],color=MUTED,lw=0.9,ls=(0,(4,3)),zorder=1)
    for i in range(6):
        a=math.radians(60*i+30); u=np.array([math.cos(a),math.sin(a),0]); n=np.array([-u[1],u[0],0])
        r0=RINGS[0]+SPAN/2-1; r1=RINGS[1]-SPAN/2+1; hw=2.0; hz=np.array([0,0,3.2])
        A=u*r0+n*hw; B=u*r1+n*hw; C=u*r1-n*hw; D=u*r0-n*hw
        polys.append((np.array([A+hz,B+hz,C+hz,D+hz]),"#c7ced2","#7d8a90",0.6))
        polys.append((np.array([A,B,B+hz,A+hz]),"#b3bec4","#7d8a90",0.6))
        polys.append((np.array([D,C,C+hz,D+hz]),"#b3bec4","#7d8a90",0.6))
    # depth sort
    polys.sort(key=lambda t: -(proj(t[0])[1].mean()-(0.05 if t[1]=="#ffffff" and t[2]=="#ffffff" else 0)))
    for P,fc,ec,lw in polys:
        g,d=proj(P); ax.add_patch(Polygon(g,fc=fc,ec=ec,lw=lw,zorder=10 if d.mean()<-RINGS[0]*0.35 else 2))
    # rotating arch formwork at front (inflatable centering), drawn as outline arch
    xs=np.linspace(-SPAN/2,SPAN/2,60); R=RINGS[1]
    a0=thf; a1=thf+SW/R
    for a in (a0,a1):
        P=np.c_[(R+xs)*math.cos(a),(R+xs)*math.sin(a),arch(xs)+0.4]
        g,_=proj(P); ax.plot(g[:,0],g[:,1],color=RUST,lw=2.4,zorder=6)
    for u in np.linspace(-SPAN/2,SPAN/2,9):
        P=np.array([[(R+u)*math.cos(a0),(R+u)*math.sin(a0),arch(u)+0.4],[(R+u)*math.cos(a1),(R+u)*math.sin(a1),arch(u)+0.4]])
        g,_=proj(P); ax.plot(g[:,0],g[:,1],color=RUST,lw=1.0,zorder=6)
    # circular rails at both feet of ring 2 (dash where not yet built)
    th=np.linspace(0,2*np.pi,300)
    for rr in (R-SPAN/2-0.8,R+SPAN/2+0.8):
        g,_=proj(np.c_[rr*np.cos(th),rr*np.sin(th),0*th]); ax.plot(g[:,0],g[:,1],color=RUST,lw=0.7,alpha=0.6,zorder=1.5)
    # radial guide arm from crane base to formwork
    a=thf+math.radians(2); R=RINGS[1]
    g,_=proj(np.array([[0,0,0.5],[(R+SPAN/2)*math.cos(a),(R+SPAN/2)*math.sin(a),0.5]]))
    ax.plot(g[:,0],g[:,1],color=INK,lw=1.2,ls=(0,(2,2)),zorder=6)
    # central robotic pumping tower
    WATER="#2f6a8f"; mh=30
    for dx in (-0.9,0.9):
        g,_=proj(np.array([[dx,0,0],[dx*0.6,0,mh+8]])); ax.plot(g[:,0],g[:,1],color=INK,lw=1.6,zorder=8)
    for z in np.arange(2,mh+6,4):
        g,_=proj(np.array([[-0.9+0.3*z/(mh+8),0,z],[0.9-0.3*(z+4)/(mh+8),0,z+4]])); ax.plot(g[:,0],g[:,1],color=INK,lw=0.6,zorder=8)
    g,_=proj(np.array([[0,0,0],[0,0,mh]])); ax.plot(g[:,0],g[:,1],color=WATER,lw=2.2,zorder=8.1)
    # buffer tank at base + buried pipeline from Rodwell field
    tb,_=proj(np.array([[3.5,3.5,0]])); ax.add_patch(Polygon(tb+np.array([[-3,0],[3,0],[3,4],[-3,4]]),fc="#cfe3ee",ec=INK,lw=0.8,zorder=8.2))
    ap=math.radians(210); pl=np.array([[3.5,3.5,-0.3],[100*math.cos(ap),100*math.sin(ap),-0.3]])
    g,_=proj(pl); ax.plot(g[:,0],g[:,1],color=WATER,lw=1.6,ls=(0,(4,2)),zorder=1.6)
    aj=thf+math.radians(2); L=REACH
    head=np.array([0,0,mh]); tip=np.array([L*math.cos(aj),L*math.sin(aj),mh-2])
    back=np.array([-10*math.cos(aj),-10*math.sin(aj),mh])
    g,_=proj(np.array([back,head,tip])); ax.plot(g[:,0],g[:,1],color=WATER,lw=3.2,zorder=8.3,solid_capstyle="round")
    for fr in (0.35,0.7,1.0):
        q=head+(tip-head)*fr; g,_=proj(np.array([[0,0,mh+8],q])); ax.plot(g[:,0],g[:,1],color=INK,lw=0.7,zorder=8)
    g,_=proj(np.array([[0,0,mh+8],back])); ax.plot(g[:,0],g[:,1],color=INK,lw=0.7,zorder=8)
    # robotic carriage on boom + hose down to the formwork crown
    rt=RINGS[1]; car=np.array([rt*math.cos(aj),rt*math.sin(aj),mh-2*rt/L]); hk=np.array([rt*math.cos(aj),rt*math.sin(aj),9.8])
    cp,_=proj(car[None]); ax.add_patch(Polygon(cp+np.array([[-1.4,-0.8],[1.4,-0.8],[1.4,0.9],[-1.4,0.9]]),fc=INK,zorder=9))
    hz=np.linspace(0,1,30); hose=car[None,:]*(1-hz[:,None])+hk[None,:]*hz[:,None]; hose[:,0]+=2.0*np.sin(np.pi*hz)
    g,_=proj(hose); ax.plot(g[:,0],g[:,1],color=WATER,lw=1.6,zorder=8.4)
    # sweep arrow of boom
    ang=np.linspace(aj-0.5,aj+0.5,40); P=np.c_[66*np.cos(ang),66*np.sin(ang),mh+0*ang]
    g,_=proj(P); ax.annotate("",xy=g[-1],xytext=g[-2],arrowprops=dict(arrowstyle="-|>",color=RUST,lw=1.4),zorder=9)
    ax.plot(g[:,0],g[:,1],color=RUST,lw=1.4,zorder=9)
    # labels
    def lab(p3,txt,dx,dy,ha="left"):
        p,_=proj(np.array(p3)[None]); p=p[0]
        ax.annotate(txt,xy=p,xytext=(p[0]+dx,p[1]+dy),fontsize=10,ha=ha,va="center",
            arrowprops=dict(arrowstyle="-",color=INK,lw=0.7),bbox=dict(fc=BG,ec="none",pad=1.5),zorder=12)
    lab((0,0,mh+8),"Robotic water-pumping tower (mast = riser pipe, pipe boom rotates 360°)",0,9,"center")
    lab(tip,"Pipe boom ±95 m\n(reaches ring 3)",6,6)
    lab(car,"boom robot: water hose\nto formwork ports",10,-8)
    lab(tuple(tb[0]*0)+(0,) if False else (3.5,3.5,2),"buffer tank\n+ pump",28,-24)
    p=pl[0]+(pl[1]-pl[0])*0.55; lab(tuple(p),"buried pipe from Rodwell wells",-10,-14,"right")
    a=math.radians(165); lab(((RINGS[0]-3)*math.cos(a),(RINGS[0]-3)*math.sin(a),7),"Ring 1 — complete: 70 whole arches\n(16 m span, 9 m high, 2.5 m wide)",-62,2,"right")
    a=math.radians(175); lab(((RINGS[1]+6)*math.cos(a),(RINGS[1]+6)*math.sin(a),5),"Ring 2 — under construction,\nadvancing with the boom",-12,14,"right")
    a=thf; lab(((RINGS[1]+SPAN/2)*math.cos(a),(RINGS[1]+SPAN/2)*math.sin(a),1),"Travelling formwork (wheels + compass cables):\ncast one whole arch → freeze → advance 2.5 m",14,-12)
    a=math.radians(215); lab(((RINGS[0]+SPAN/2+GAP/2)*math.cos(a),(RINGS[0]+SPAN/2+GAP/2)*math.sin(a),0),"12 m gap: rover service road,\ncrossed by radial corridors",-35,-38,"right")
    a=math.radians(-20); lab(((RINGS[2]+SPAN/2)*math.cos(a),(RINGS[2]+SPAN/2)*math.sin(a),0),"Planned ring 3",12,-6)
    p,_=proj(np.array([[0,0,0]])); ax.text(p[0,0]-1.5,p[0,1]+3,"central\ncourtyard\nØ40 m",fontsize=8.5,color=INK,ha="right",va="center",zorder=12)
    ax.set_xlim(-135,128); ax.set_ylim(-78,88)
    ax.text(-134,86,"Concentric torus habitat with a central pumping tower",fontsize=15,fontweight="bold",va="top")
    ax.text(-134,79,"The central tower pumps water to the formwork; the boom rotates so each ring is cast arch by arch.",fontsize=10.5,color=MUTED,va="top")
    fig.savefig("T1_torus_3d.png",dpi=140,bbox_inches="tight",facecolor=BG); fig.savefig("T1_torus_3d.svg",dpi=72,bbox_inches="tight",facecolor=BG)
draw3d()
