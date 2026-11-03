import os
import numpy as np, math, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from draw2d import INK,BG,ICE,ICED,RIB,RUST,SAND,MUTED
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["svg.fonttype"]="none"
from matplotlib.patches import Polygon, Circle, FancyBboxPatch
plt.rcParams["font.family"]="Inter" if "Inter" in [f.name for f in matplotlib.font_manager.fontManager.ttflist] else "DejaVu Sans"
SPAN=16.0; H=9.0; K=0.16; T=0.6
def arch(x):
    c=math.cosh(K*SPAN/2); return H*(c-np.cosh(K*x))/(c-1)
def band(x0,y0,off_out=T/2,off_in=-T/2,n=80):
    u=np.linspace(-SPAN/2,SPAN/2,n); y=arch(u); dy=np.gradient(y,u); nn=np.c_[-dy,np.ones_like(u)]/np.sqrt(1+dy**2)[:,None]
    c=np.c_[u+x0,y+y0]; return np.r_[c+off_out*nn,(c+off_in*nn)[::-1]]
# oblique "cabinet" projection: x along arch span, depth along ring (offset dx,dy per m)
OX,OY=0.55,0.32
def slice_poly(depth, lift=0.0, xoff=0.0):
    P=band(xoff,lift); return P+np.array([depth*OX,depth*OY])
fig=plt.figure(figsize=(15,13.5),facecolor=BG)
def panel(rect,title,sub):
    ax=fig.add_axes(rect); ax.set_facecolor(BG); ax.set_aspect("equal"); ax.axis("off")
    ax.text(0,1.02,title,transform=ax.transAxes,fontsize=13,fontweight="bold")
    ax.text(0,0.975,sub,transform=ax.transAxes,fontsize=9.5,color=MUTED,va="top")
    return ax
def ground(ax,x0,x1):
    ax.fill_between([x0,x1],-1.2,0,color="#e3cdb6",zorder=0); ax.plot([x0,x1],[0,0],color=INK,lw=0.8,zorder=1)
def outer(lift=0.0,n=80):
    u=np.linspace(-SPAN/2,SPAN/2,n); y=arch(u); dy=np.gradient(y,u); nn=np.c_[-dy,np.ones_like(u)]/np.sqrt(1+dy**2)[:,None]
    return np.c_[u,y+lift]+T/2*nn
def slab(ax,d,w,lift=0.0,fc=ICE,top="#c9dde9",z=2,lw=0.6):
    O=outer(lift); sh=np.array([OX,OY])
    ax.add_patch(Polygon(np.r_[O+(d+w)*sh,(O+d*sh)[::-1]],fc=top,ec=INK,lw=lw,zorder=z))
    ax.add_patch(Polygon(band(0,lift)+d*sh,fc=fc,ec=INK,lw=lw,zorder=z+0.001))
def placed(ax,nmax,w=2.5,start=1,fc=ICE):
    for k in range(nmax,start-1,-1):
        slab(ax,k*w,w,fc=fc,z=2+0.01*(nmax-k))
# ---------- Opsi 1: precast whole arch ----------
ax=panel([0.03,0.47,0.46,0.47],"Option 1 · Precast whole arch, lifted by crane","One arch = one piece (1.25–2.5 m wide), set side by side around the ring.")
ground(ax,-12,22)
placed(ax,5)
# hanging slice at depth 0 lifted 6 m
lift=5.0; slab(ax,0,2.5,lift=lift,fc=ICED,top="#a9c6d6",z=6,lw=0.9)
# spreader truss following arch
u=np.linspace(-6.5,6.5,6); yy=arch(u)+lift+T/2
sp_y=lift+H+3.2
ax.plot([-7,7],[sp_y,sp_y],color=INK,lw=2.4,zorder=7)
for a,b in zip(u,yy): ax.plot([a,a],[sp_y,b],color=INK,lw=0.7,zorder=7)
ax.plot([-7,0,7],[sp_y,sp_y+3.5,sp_y],color=INK,lw=0.8,zorder=7); ax.plot([0,0],[sp_y+3.5,sp_y+8],color=INK,lw=0.9,zorder=7)
ax.add_patch(Polygon([(-0.5,sp_y+8),(0.5,sp_y+8),(0.3,sp_y+7.2),(-0.3,sp_y+7.2)],fc=INK,zorder=8))
ax.text(8.6,sp_y+1,"spreader beam: 6 lift points\n→ bending stress while lifting\n±70–150 kPa (safe, but needs\nbasalt fibres in the ice)",fontsize=9,va="center")
ax.annotate("arches already standing\n(stable at once, just\nlocked to the previous arch)",xy=(14.5,6.5),xytext=(15.5,1.0),fontsize=9,arrowprops=dict(arrowstyle="-",lw=0.6))
ax.text(-11.8,25.5,"35 t (2.5 m wide)\n17 t (1.25 m wide)",fontsize=10,fontweight="bold",color=RUST)
# casting on its side inset
iy=-4.0
ax.text(-11.5,iy,"Cast lying on its side in a factory (mould = flat floor + two curved walls), then tilted up.",fontsize=9)
u=np.linspace(-SPAN/2,SPAN/2,80); cp=np.c_[u*0.7-3,iy-5.2+arch(u)*0.42]
ax.fill_between(cp[:,0],cp[:,1],cp[:,1]+0.45,color=ICED,zorder=3); ax.plot(cp[:,0],cp[:,1],color=INK,lw=2.2,zorder=4); ax.plot(cp[:,0],cp[:,1]+0.45,color=INK,lw=2.2,zorder=4)
ax.plot([-11,6],[iy-5.25,iy-5.25],color=MUTED,lw=0.8); ax.text(7,iy-3.4,"mould, top view:\narch width (2.5 m)\n= mould depth",fontsize=8.5,color=MUTED)
ax.set_xlim(-12,26); ax.set_ylim(-10.5,30)
# ---------- Opsi 2: cast in place ----------
bx=panel([0.52,0.47,0.46,0.47],"Option 2 · Arch cast in place","A one-arch bag sits on travelling formwork, is filled and frozen, then the formwork moves on.")
ground(bx,-12,22)
placed(bx,5)
# formwork at depth 0: centering below and outer shutter
Pin=band(0,0,off_out=-T/2,off_in=-T/2-0.9); bx.add_patch(Polygon(Pin,fc="#f3d9c4",ec=RUST,lw=1.2,zorder=5))
Pout=band(0,0,off_out=T/2+0.35,off_in=T/2); bx.add_patch(Polygon(Pout,fc="#d9d2c8",ec=INK,lw=0.8,zorder=6))
Pice=band(0,0); bx.add_patch(Polygon(Pice,fc=ICED,ec=INK,lw=0.9,zorder=5.5))
# wheels / rail
for x in (-7.5,-4,4,7.5): bx.add_patch(Circle((x,-0.2),0.35,fc=INK,zorder=7))
bx.plot([-9,9],[-0.55,-0.55],color=INK,lw=1.2,zorder=6)
# crane hook bringing bucket
bx.plot([2.5,2.5],[26.5,19],color=INK,lw=0.8); bx.add_patch(Polygon([(1.6,19),(3.4,19),(3.1,17.5),(1.9,17.5)],fc="#b9a089",ec=INK,lw=0.8,zorder=8))
bx.text(4.0,18.3,"the central tower only pumps\nwater through its boom\n(no heavy lifts)",fontsize=9,va="center")
bx.text(-0.3,3.2,"lower arch\nformwork\n(inflatable/frame)",ha="center",fontsize=8.5,color=RUST,zorder=9,bbox=dict(fc=BG,ec="none",pad=1.5))
bx.annotate("outer clamp (holds the shape\nwhile freezing → shape locked\non both sides)",xy=(-4.6,arch(np.array([-4.6]))[0]+0.75),xytext=(-11.5,16),fontsize=9,arrowprops=dict(arrowstyle="-",lw=0.6))
bx.annotate("wheels on a circular track:\nformwork advances one arch width\nafter each freeze",xy=(7.5,-0.2),xytext=(10.5,-4.5),fontsize=9,arrowprops=dict(arrowstyle="-",lw=0.6))
bx.text(-11.5,-4.2,"The new arch freezes against\nthe previous one → the joint\nfuses (monolithic).",fontsize=9,color=INK)
bx.set_xlim(-12,26); bx.set_ylim(-10.5,30)
# ---------- table ----------
e=fig.add_axes([0.03,0.03,0.95,0.38]); e.axis("off"); e.set_xlim(0,1); e.set_ylim(0,1)
e.text(0,0.98,"Comparison for 3 rings",fontsize=13,fontweight="bold",va="top")
cols=["","Tiles (8 per arch)","Precast arch 2.5 m","Precast arch 1.25 m","Cast-in-place arch 2.5 m"]
X=[0,0.2,0.4,0.6,0.8]
rows=[("Number of pieces","3,376","422","844","422 (no lifting)"),
("Heaviest lift","5.5 t","35 t","17 t","none (water pumped)"),
("Crane moment at ring 3","±2 MN·m","±11 MN·m","±5.4 MN·m","no crane needed"),
("Mould type","4 profiles + hinged walls","1 full-arch mould","1 full-arch mould","travelling formwork (several sets)"),
("Arch formwork during erection","needed","not needed","not needed","yes (formwork = mould)"),
("Joints in ring 1","±3,000 m","±1,780 m","±3,580 m","±1,780 m, fused"),
("Main risk","many joints","cracking when lifted & tilted;\nvery large crane","cracking when lifted","on-site freezing rate\nsets the schedule")]
y0=0.84
for xx,c in zip(X,cols): e.text(xx,y0,c,fontsize=10,fontweight="bold",color=MUTED)
e.plot([0,1],[y0-0.03,y0-0.03],color=INK,lw=0.6)
for k,r in enumerate(rows):
    yy=y0-0.09-k*0.105
    for j,(xx,v) in enumerate(zip(X,r)): e.text(xx,yy,v,fontsize=10,va="center",fontweight="bold" if j==0 else "normal")
e.add_patch(FancyBboxPatch((0.79,0.03),0.205,0.85,boxstyle="round,pad=0.004",fc="none",ec=RUST,lw=1.4))
fig.savefig("T4_arch_options.png",dpi=120,facecolor=BG); fig.savefig("T4_arch_options.svg",dpi=72,facecolor=BG)
