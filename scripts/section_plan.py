import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"torus_3d.py")).read().split("# ---------- projection")[0])
xs=np.linspace(-SPAN/2,SPAN/2,400); ys=arch(xs); arc=np.sum(np.hypot(np.diff(xs),np.diff(ys)))
t=0.6; rho=917; g=3.71; w=t*rho*g  # N/m2 of shell
# simple funicular estimate: H from parabola-ish, V = half arc weight
f=H; Hthr=w*(arc/SPAN)*SPAN**2/(8*f); V=w*arc/2; N=math.hypot(Hthr,V)
print("arc",arc,"H",Hthr/1e3,"V",V/1e3,"N",N/1e3,"stress kPa",N/t/1e3)
rows=[]
for R in RINGS:
    Nt=int(round(2*np.pi*R/SW)); A=2*np.pi*R*(SPAN-2)
    tw=2*np.pi*R/Nt; tile=tw*arc*t*rho
    rows.append((R,Nt,Nt,A,tile/1000)); print(R,Nt,round(A),round(tile/1000,1))
fig,(ax,bx)=plt.subplots(2,1,figsize=(13,13),facecolor=BG,gridspec_kw=dict(height_ratios=[1,1.25]))
# ---------- SECTION ----------
ax.set_facecolor(BG); ax.set_aspect("equal"); ax.axis("off")
ax.fill_between([-104,104],-6,0,color="#e3cdb6",zorder=0); ax.plot([-104,104],[0,0],color=INK,lw=0.8)
ax.fill_between([-104,104],-6,-3.5,color="#cfe3ee",zorder=0); ax.text(-103,-4.9,"ground ice layer (±1–10 m)",fontsize=8.5,color=MUTED,va="center")
cols=[ICED,ICE,"#ffffff"]
for side in (-1,1):
    for k,R in enumerate(RINGS):
        c=side*R; x=c+xs; y=ys
        nx=-np.gradient(y); ny=np.gradient(xs); n=np.hypot(nx,ny); nx/=n; ny/=n
        outer=np.c_[x+nx*t/2*side*0+(-nx)*0, y]  # thin centreline drawing
        built = (k<2) if side<0 else (k<2)
        ec=INK if built else MUTED
        ax.add_patch(Polygon(np.r_[np.c_[x+nx*0.35,y+ny*0.35],np.c_[x-nx*0.35,y-ny*0.35][::-1]],
                     fc=ICED if built else "none",ec=ec,lw=0.8,ls="-" if built else (0,(3,2)),zorder=3))
        # inflatable liner (pressurised) inside
        if built and not (side>0 and k==1):
            th=np.linspace(0,np.pi,60); ax.add_patch(Polygon(np.c_[c+6.3*np.cos(th),0.4+6.6*np.sin(th)],fc="#f6efe6",ec="#c49a6c",lw=1,zorder=2))
    # foot blocks
    for k,R in enumerate(RINGS):
        for e in (R-SPAN/2,R+SPAN/2):
            ax.add_patch(Polygon([(side*e-1,0),(side*e+1,0),(side*e+1,-1.4),(side*e-1,-1.4)],fc="#b9a089",ec=INK,lw=0.6,zorder=4))
# floor ties in built rings (each ring now stands alone)
for c in (-RINGS[0],-RINGS[1],RINGS[0]):
    ax.plot([c-SPAN/2+1,c+SPAN/2-1],[-0.7,-0.7],color=RUST,lw=1.6,zorder=5)
xf=-RINGS[1]
ax.text(xf,-1.6,"basalt floor ties resist\nthe thrust of both arch feet",ha="center",va="top",fontsize=8.5,color=RUST)
# corridor across the gap (left, ring1<->ring2)
x0=-(RINGS[0]+SPAN/2)+0.5; x1=-(RINGS[1]-SPAN/2)-0.5
ax.add_patch(Polygon([(x0,0),(x0,3.2),(x1,3.2),(x1,0)],fc="#b3bec4",ec="#7d8a90",lw=0.8,zorder=4))
ax.annotate("",xy=(-(RINGS[0]+SPAN/2),7.5),xytext=(-(RINGS[1]-SPAN/2),7.5),arrowprops=dict(arrowstyle="<->",color=INK,lw=0.8))
ax.text(-(RINGS[0]+SPAN/2+GAP/2),8.2,"12 m gap\n+ corridor",ha="center",fontsize=8.5)
# robotic pumping tower
WATER="#2f6a8f"; mh=30
for dx in (-1.0,1.0): ax.plot([dx,dx*0.6],[-1,mh+8],color=INK,lw=1.4,zorder=5)
for z in np.arange(0,mh+6,3): ax.plot([-1+0.4*z/(mh+8),1-0.4*(z+3)/(mh+8)],[z,z+3],color=INK,lw=0.5,zorder=5)
ax.plot([0,0],[-4.5,mh],color=WATER,lw=2.2,zorder=5.1)
ax.plot([-10,0,REACH],[mh,mh,mh-2],color=WATER,lw=3,zorder=5.2,solid_capstyle="round")
for fr in (0.35,0.7,1.0): ax.plot([0,REACH*fr],[mh+8,mh-2*fr],color=INK,lw=0.7)
ax.plot([0,-10],[mh+8,mh],color=INK,lw=0.7)
# buffer tank (buried) + pipe from Rodwell
ax.add_patch(Polygon([(-4,-5.6),(4,-5.6),(4,-3.4),(-4,-3.4)],fc="#cfe3ee",ec=INK,lw=0.6,zorder=5))
ax.plot([-4,-36],[-5.2,-5.2],color=WATER,lw=1.4,ls=(0,(4,2)),zorder=5)
ax.text(-25,-7.3,"pipe from Rodwell wells",ha="center",fontsize=8.5,color=WATER)
ax.text(5,-5.4,"buffer tank",fontsize=8.5,color=WATER,va="center")
# robot carriage + hose to formwork crown
cx_=RINGS[1]+1; ax.add_patch(Polygon([(cx_-1.2,mh-1.6),(cx_+1.2,mh-1.6),(cx_+1.2,mh-0.2),(cx_-1.2,mh-0.2)],fc=INK,zorder=6))
hz=np.linspace(0,1,30); ax.plot(cx_+1.5*np.sin(np.pi*hz)-1*hz,(mh-1.6)*(1-hz)+(H+0.8)*hz,color=WATER,lw=1.4,zorder=6)
ax.text(RINGS[1]+3,18,"boom robot:\nwater hose to ports",fontsize=8.5,va="center")
uu=np.linspace(-SPAN/2,SPAN/2,80); yy=arch(uu); dyy=np.gradient(yy,uu); nn=np.c_[-dyy,np.ones_like(uu)]/np.sqrt(1+dyy**2)[:,None]
cc=np.c_[RINGS[1]+uu,yy]
ax.add_patch(Polygon(np.r_[cc-0.35*nn,(cc-1.1*nn)[::-1]],fc="#f3d9c4",ec=RUST,lw=1,zorder=3.5))
ax.add_patch(Polygon(np.r_[cc+0.35*nn,(cc+0.7*nn)[::-1]],fc="#d9d2c8",ec=INK,lw=0.6,zorder=3.6))
for xw in (RINGS[1]-SPAN/2-0.8,RINGS[1]+SPAN/2+0.8): ax.add_patch(Circle((xw,0.35),0.35,fc=INK,zorder=6))
ax.text(RINGS[1],-1.9,"being cast: travelling formwork\n+ outer clamp, wheels + compass cables",ha="center",va="top",fontsize=8.5,color=RUST)
ax.annotate("",xy=(REACH,mh+3),xytext=(0,mh+3),arrowprops=dict(arrowstyle="<->",color=INK,lw=0.8)); ax.text(REACH/2,mh+4,"pipe boom ±95 m",ha="center",fontsize=9)
ax.text(1.5,mh+9,"central pumping tower",fontsize=9.5,fontweight="bold")
for k,R in enumerate(RINGS):
    ax.text(R,10.8 if k==0 else 10.3,f"Ring {k+1}",ha="center",fontsize=9.5,fontweight="bold",color=INK if k<2 else MUTED)
    ax.text(-R,10.3,f"Ring {k+1}",ha="center",fontsize=9.5,fontweight="bold",color=INK if k<2 else MUTED)
ax.text(-RINGS[0],2.2,"pressurized\nmodule",ha="center",fontsize=8,color="#8a6a48",zorder=5)

ax.text(-103,mh+12,"Section through the pumping tower",fontsize=13,fontweight="bold")
ax.text(-103,mh+11,"Left: rings 1–2 complete.  Right: ring 2 being cast.\nDashed = planned.",fontsize=9.5,color=MUTED,va="top")
ax.set_xlim(-104,104); ax.set_ylim(-9.5,mh+14)
# scale
ax.plot([75,95],[-8.6,-8.6],color=INK,lw=2); ax.text(85,-8.2,"20 m",ha="center",fontsize=8.5)
# ---------- PLAN ----------
bx.set_facecolor(BG); bx.set_aspect("equal"); bx.axis("off")
bx.add_patch(Circle((0,0),104,fc="#e3cdb6",ec="none",zorder=0))
PH=["#2f6a8f","#5f9bc0","#9cc6de"]
for k,R in enumerate(RINGS):
    Nt=int(round(2*np.pi*R/SW)); r0=R-SPAN/2; r1=R+SPAN/2
    for j in range(Nt):
        a=np.linspace(2*np.pi*j/Nt,2*np.pi*(j+1)/Nt,4)
        Q=np.r_[np.c_[r0*np.cos(a),r0*np.sin(a)],np.c_[r1*np.cos(a[::-1]),r1*np.sin(a[::-1])]]
        bx.add_patch(Polygon(Q,fc=PH[k],ec="#ffffff",lw=0.5,alpha=1 if k<2 else 0.45,zorder=2))
    # radial gates at shared foot (between ring k and k+1)
for k in range(2):
    e0=RINGS[k]+SPAN/2-1; e1=RINGS[k+1]-SPAN/2+1
    for i in range(6):
        a=math.radians(60*i+(0 if k==0 else 30)); u=np.array([math.cos(a),math.sin(a)]); nn=np.array([-u[1],u[0]])
        p0=u*e0; p1=u*e1
        bx.add_patch(Polygon([p0+nn*1.6,p1+nn*1.6,p1-nn*1.6,p0-nn*1.6],fc="#b3bec4" if k==0 else "none",ec="#7d8a90",lw=0.7,ls="-" if k==0 else (0,(3,2)),zorder=4))
# inner gates to courtyard (4)
for i in range(4):
    a=math.radians(90*i+45); u=np.array([math.cos(a),math.sin(a)]); nn=np.array([-u[1],u[0]]); e=RINGS[0]-SPAN/2
    p0=u*(e-2.5); p1=u*(e+2.2); bx.add_patch(Polygon([p0+nn*1.6,p1+nn*1.6,p1-nn*1.6,p0-nn*1.6],fc="#f3d9c4",ec=INK,lw=0.6,zorder=4))
bx.add_patch(Circle((0,0),2.5,fc=INK,zorder=5))
bx.add_patch(Circle((0,0),REACH,fc="none",ec=RUST,lw=1,ls=(0,(5,4)),zorder=5))
bx.text(0,REACH+1.5,"boom reach limit (r = 95 m)",ha="center",fontsize=9,color=RUST)
bx.text(0,-6,"tower",ha="center",fontsize=9,fontweight="bold")
for k,(R,Nt,ntile,A,m) in enumerate(rows):
    a=math.radians(-35); p=np.array([math.cos(a),math.sin(a)])*R
    bx.annotate(f"Ring {k+1}: R = {R:.0f} m · {ntile} whole arches · ±{A:,.0f} m² floor",xy=p,xytext=(108,-25-k*13),fontsize=9.5,va="center",
        arrowprops=dict(arrowstyle="-",color=INK,lw=0.6),zorder=7)
bx.annotate("radial corridors cross the 12 m gap\n(6 per gap)",xy=np.array([1,0])*(RINGS[0]+SPAN/2+GAP/2),xytext=(108,30),fontsize=9.5,va="center",arrowprops=dict(arrowstyle="-",color=INK,lw=0.6),zorder=7)
bx.text(-106,110,"Plan: growing outward, ring by ring",fontsize=13,fontweight="bold")
bx.text(-106,103,"Each ring = a row of whole 2.5 m-wide arches, cast in place with travelling formwork.  Each new ring adds more floor area.",fontsize=9.5,color=MUTED)
bx.plot([-100,-80],[-104,-104],color=INK,lw=2); bx.text(-90,-101.5,"20 m",ha="center",fontsize=8.5)
bx.set_xlim(-108,200); bx.set_ylim(-108,112)
fig.tight_layout(); fig.savefig("T2_section_plan.png",dpi=130,bbox_inches="tight",facecolor=BG); fig.savefig("T2_section_plan.svg",dpi=72,bbox_inches="tight",facecolor=BG)
