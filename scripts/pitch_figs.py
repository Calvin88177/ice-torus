import os
import numpy as np, math, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from draw2d import INK,BG,ICE,ICED,RUST,MUTED
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle, FancyBboxPatch, Ellipse, FancyArrowPatch, Wedge
plt.rcParams["font.family"]="Inter" if "Inter" in [f.name for f in matplotlib.font_manager.fontManager.ttflist] else "DejaVu Sans"
FIB="#2b2b2b"; WATER="#2f6a8f"; OK="#3c8d5a"; BAD="#c4502a"
rho=917; g=9.81
# ===================== FIGURE 1: prestressed ice =====================
fig=plt.figure(figsize=(15,10.5),facecolor=BG)
fig.text(0.04,0.95,"Prestressed ice: how ice can hold a spinning station together",fontsize=18,fontweight="bold")
fig.text(0.04,0.915,"Fibre hoops carry the spin load; the ice carries the mass, shape and shielding. The same trick as prestressed concrete.",fontsize=11,color=MUTED)
# --- A: stress vs radius ---
ax=fig.add_axes([0.06,0.50,0.40,0.36]); ax.set_facecolor(BG)
R=np.linspace(10,1000,300)
for gg,lab,ls in ((1.0,"1 g",'-'),(0.38,"Mars gravity (0.38 g)",'--'),(0.165,"Moon gravity (0.16 g)",':')):
    ax.plot(R,rho*g*gg*R/1e6,color=INK,lw=1.8,ls=ls,label=lab)
ax.axhspan(0,1.0,color=OK,alpha=0.12); ax.axhline(1.0,color=OK,lw=1.2)
ax.text(990,0.55,"plain ice cracks at ≈1 MPa in tension",ha="right",va="bottom",fontsize=9.5,color=OK)
for Rr,lab in ((56,"56 m"),(224,"224 m"),(830,"Stanford torus\n830 m")):
    s=rho*g*Rr/1e6; ax.plot(Rr,s,"o",color=BAD,ms=7,zorder=5)
    ax.annotate(f"{lab}: {s:.1f} MPa",xy=(Rr,s),xytext=((Rr+30,s-0.15) if Rr>100 and Rr<800 else ((Rr+15,s+0.9) if Rr<100 else (Rr+30,s-1.7))),fontsize=9.5,color=BAD)
ax.set_xlabel("ring radius R (m)"); ax.set_ylabel("hoop stress from spin, σ = ρ·g·R (MPa)")
ax.set_xlim(0,1000); ax.set_ylim(0,9); ax.legend(frameon=False,fontsize=9.5,loc="upper left")
for sp in ("top","right"): ax.spines[sp].set_visible(False)
ax.set_title("A · Why plain ice fails",loc="left",fontsize=13,fontweight="bold",pad=12)
# --- B: section of ring tube with fibres in sleeves ---
bx=fig.add_axes([0.53,0.50,0.43,0.36]); bx.set_aspect("equal"); bx.axis("off")
bx.set_title("B · What the ring is made of (section through the tube)",loc="left",fontsize=13,fontweight="bold",pad=12)
bx.add_patch(Circle((0,0),4.0,fc=ICE,ec=INK,lw=1.2))
bx.add_patch(Circle((0,0),2.6,fc="#fbf3e6",ec=INK,lw=1.0))
bx.add_patch(Circle((0,0),2.45,fc="none",ec=WATER,lw=2.2))
th=np.linspace(0,2*np.pi,28,endpoint=False)
for a in th:
    for r in (3.0,3.6):
        p=(r*math.cos(a+ (0.11 if r>3.3 else 0)),r*math.sin(a+(0.11 if r>3.3 else 0)))
        bx.add_patch(Circle(p,0.11,fc="white",ec=FIB,lw=0.8)); bx.add_patch(Circle(p,0.05,fc=FIB))
bx.add_patch(Circle((0,0),4.15,fc="none",ec="#b9a089",lw=2.5))
bx.text(0,0.2,"habitat\n(pressurised)",ha="center",va="center",fontsize=10)
def L(xy,t,xt):
    bx.annotate(t,xy=xy,xytext=xt,fontsize=10,va="center",arrowprops=dict(arrowstyle="-",lw=0.7,color=INK))
L((3.0*math.cos(0.25),3.0*math.sin(0.25)),"carbon-fibre tendons\nin sleeves, running\naround the ring\n(≈0.2% of section)",(5.0,2.0))
L((3.8*math.cos(-0.5),3.8*math.sin(-0.5)),"ice shield (radiation + mass)",(5.0,-1.2))
L((2.45*math.cos(2.3),2.45*math.sin(2.3)),"pressure liner (fibre) holds the air",(-9.5,3.6))
L((4.15*math.cos(-2.2),4.15*math.sin(-2.2)),"sealed bag + sunshade\n(stops sublimation)",(-9.5,-3.4))
bx.set_xlim(-9.6,11.5); bx.set_ylim(-4.8,4.8)
# --- C: stress states ---
cx=fig.add_axes([0.06,0.08,0.40,0.32]); cx.set_facecolor(BG)
cx.set_title("C · Stress in the ice through the life of the ring (224 m, 1 g)",loc="left",fontsize=13,fontweight="bold",pad=12)
stages=["1 · ice frozen,\nfibres slack","2 · fibres tensioned\n(post-tensioning)","3 · spun up\nto 1 g"]
ice=[0,-2.0,0.0]; fib=[0,1.0,1.0]
x=np.arange(3)
cx.bar(x-0.18,ice,0.34,color=ICED,label="stress in ice (MPa)")
cx.axhline(0,color=INK,lw=0.8); cx.axhline(1.0,color=OK,lw=1,ls="--"); cx.axhline(-1.0,color=OK,lw=0)
cx.text(-0.45,1.05,"ice tension limit",fontsize=9,color=OK,ha="left",va="bottom")
for xi,v in zip(x,ice):
    cx.text(xi-0.18,v-0.12 if v<0 else v+0.08,f"{v:+.1f}" if v else "0",ha="center",va="top" if v<0 else "bottom",fontsize=10,fontweight="bold")
cx2=cx.twinx(); cx2.bar(x+0.18,fib,0.34,color=FIB,label="stress in fibre (GPa)"); cx2.set_ylim(-2.4,1.8); cx2.set_ylabel("fibre (GPa)")
for xi,v in zip(x,fib): cx2.text(xi+0.18,v+0.04,f"{v:.1f}",ha="center",va="bottom",fontsize=10)
cx.set_ylim(-2.4,1.8); cx.set_ylabel("ice (MPa; negative = squeezed)")
cx.set_xticks(x); cx.set_xticklabels(stages,fontsize=9.5)
for a in (cx,cx2):
    a.spines["top"].set_visible(False)
h1,l1=cx.get_legend_handles_labels(); h2,l2=cx2.get_legend_handles_labels(); cx.legend(h1+h2,l1+l2,frameon=False,fontsize=9,loc="lower left")
fig.text(0.06,0.015,"At full spin the pre-squeeze is used up exactly: the ice sits at zero stress and never goes into tension.",fontsize=9.5,color=MUTED)
# --- D: table ---
dx=fig.add_axes([0.53,0.08,0.43,0.32]); dx.axis("off"); dx.set_xlim(0,1); dx.set_ylim(0,1)
dx.text(0,1.02,"D · How much fibre and squeeze each ring needs (1 g)",fontsize=13,fontweight="bold",va="bottom")
hdr=["Ring radius","Spin","Fibre share","Fibre per m²","Pre-squeeze on ice"]
X=[0,0.2,0.36,0.56,0.76]
rows=[["56 m","4 rpm","0.05%","4–5 kg","0.5 MPa"],["224 m","2 rpm","0.2–0.25%","18–22 kg","1.9–2.3 MPa"],["830 m (Stanford)","1 rpm","0.75–0.9%","66–81 kg","6.4–7.5 MPa ⚠"]]
for xx,h in zip(X,hdr): dx.text(xx,0.88,h,fontsize=10,fontweight="bold",color=MUTED)
dx.plot([0,1],[0.84,0.84],color=INK,lw=0.6)
for i,r in enumerate(rows):
    y=0.74-i*0.12
    for xx,v in zip(X,r): dx.text(xx,y,v,fontsize=11,va="center",fontweight="bold" if i==1 else "normal")
dx.plot([0,1],[0.38,0.38],color="#e2d8cc",lw=0.6)
dx.text(0,0.32,"Assumes 4.5 t/m² of ice shielding, carbon fibre at 1 GPa long-term, and up to 1 t/m² of contents.\nFibre mass is under 0.5% of the ice for a 224 m ring. The Stanford size needs ≈7 MPa of\nsqueeze, near what cold ice can take: a research question.",fontsize=9.5,va="top",linespacing=1.5)
dx.text(0,-0.08,"Key problem to solve on the bench: ice shrinks ≈0.5% when cooled to 150 K, so fibres run in\nsleeves and are tensioned only after the ice is cold.",fontsize=9.5,va="bottom",color=BAD,linespacing=1.5)
fig.savefig("Y1_prestressed_ice.png",dpi=130,facecolor=BG)

# ===================== FIGURE 2: IceRing-1 =====================
fig=plt.figure(figsize=(15,10),facecolor=BG)
fig.text(0.04,0.95,"IceRing-1: first in-orbit test of prestressed ice",fontsize=18,fontweight="bold")
fig.text(0.04,0.915,"A small satellite freezes water into two ice rings and spins them in opposite directions until the ice carries the same stress as a 224 m station.",fontsize=11,color=MUTED)
ax=fig.add_axes([0.03,0.30,0.55,0.58]); ax.set_aspect("equal"); ax.axis("off")
# sunshade
ax.add_patch(Polygon([(-7.5,5.3),(7.5,5.3),(6.5,6.0),(-6.5,6.0)],fc="#e8d9a8",ec=INK,lw=0.8))
for xx in np.linspace(-6.8,6.8,9): ax.plot([xx,xx*0.9],[5.3,6.0],color="#bda766",lw=0.6)
ax.text(0,6.5,"multilayer sunshade (keeps ice below ≈150 K)",ha="center",fontsize=10)
ax.add_patch(FancyArrowPatch((8.5,8.2),(6.0,6.3),arrowstyle="-|>",mutation_scale=14,color="#d9a400",lw=1.5))
ax.text(8.6,8.3,"Sun",fontsize=10,color="#b88a00")
# bus
ax.add_patch(Rectangle((-1.3,-1.2),2.6,2.4,fc="#d9d2c8",ec=INK,lw=1)); ax.text(0,0,"bus\n+ water\ntank",ha="center",va="center",fontsize=9)
ax.plot([0,0],[1.2,5.3],color=INK,lw=1.2)
for side in (-1,1):
    ax.add_patch(Rectangle((side*1.3+(0 if side>0 else -3.2),-0.25),3.2,0.5,fc="#3d5a80",ec=INK,lw=0.6))
# two counter-rotating rings (perspective ellipses)
for (cy,rot,col,lab) in ((2.6,1,ICED,"ring A"),(-2.6,-1,ICE,"ring B")):
    for r,lw in ((5.0,9),):
        e=Ellipse((0,cy),2*r,2*r*0.32,fc="none",ec=col,lw=lw,zorder=2)
        ax.add_patch(e)
    ax.add_patch(Ellipse((0,cy),10,3.2,fc="none",ec=FIB,lw=0.8,ls=(0,(2,2)),zorder=3))
    ang=np.linspace(0.25,0.9,20)*rot; xs=5.6*np.cos(ang*np.pi); ys=cy+5.6*0.32*np.sin(ang*np.pi)
    ax.annotate("",xy=(xs[-1],ys[-1]),xytext=(xs[-2],ys[-2]),arrowprops=dict(arrowstyle="-|>",color=RUST,lw=1.5))
    ax.plot(xs,ys,color=RUST,lw=1.5)
    ax.text(-6.3,cy,lab,ha="right",va="center",fontsize=10.5,fontweight="bold")
    ax.plot([0,0],[cy-0.2,cy+0.2],color=INK)
# dosimeters
for p in ((4.7,2.9),(-4.7,-2.3)): ax.add_patch(Circle(p,0.22,fc="#7a57b8",ec="white",lw=1,zorder=6))
ax.add_patch(Circle((2.4,-4.4),0.22,fc="#7a57b8",ec="white",lw=1,zorder=6))
def L(xy,t,xt,ha="left"):
    ax.annotate(t,xy=xy,xytext=xt,fontsize=10,va="center",ha=ha,arrowprops=dict(arrowstyle="-",lw=0.7,color=INK),bbox=dict(fc=BG,ec="none",pad=1.2),zorder=10)
L((5.0,2.6),"ice ring, Ø 1 m, ≈15 kg each,\nfrozen in a bag-mould in orbit",(7.2,3.8))
L((5.0,-2.6),"carbon-fibre hoops, tensioned\nafter freezing (post-tensioning)",(7.2,-1.6))
L((2.4,-4.4),"dosimeters: behind the ice\nvs. outside → shielding data",(7.2,-4.6))
L((-3.5,-3.9),"rings spin in opposite\ndirections → no net spin\non the satellite",(-7.5,-6.6),"left")
ax.set_xlim(-9,14); ax.set_ylim(-7.6,9)
# right: numbers
nx=fig.add_axes([0.62,0.30,0.35,0.58]); nx.axis("off"); nx.set_xlim(0,1); nx.set_ylim(0,1)
nx.text(0,0.98,"Key numbers",fontsize=13,fontweight="bold",va="top")
rows=[("Water","≈30 kg (two rings)"),("Ring size","Ø 1 m, tube ≈10 × 10 cm"),("Spin rate","≈890 rpm (rim ≈47 m/s)"),
("Hoop stress in ice","≈2 MPa = a 224 m station at 1 g"),("Fibre share","≈0.2% of section"),("Stored energy","≈33 kJ per ring"),
("Angular momentum","≈700 N·m·s per ring,\ncancelled by the twin ring"),("Satellite mass","≈100–300 kg (estimate)"),("Launch","rideshare to low Earth orbit")]
for i,(a,b) in enumerate(rows):
    y=0.90-i*0.092
    nx.text(0,y,a,fontsize=10,color=MUTED,va="top"); nx.text(0.4,y,b,fontsize=10.5,va="top",fontweight="bold")
nx.text(0,-0.06,"Small ring + high spin = same stress as a large ring + slow spin,\nbecause hoop stress σ = ρ·ω²·R² depends on rim speed.",fontsize=9.5,color=MUTED,va="bottom",linespacing=1.5)
# bottom: sequence
sx=fig.add_axes([0.03,0.03,0.94,0.22]); sx.axis("off"); sx.set_xlim(0,6); sx.set_ylim(0,1)
sx.text(0,0.98,"Mission sequence",fontsize=13,fontweight="bold",va="top")
steps=[("1 · Launch dry","bags and fibres folded;\nwater in a tank"),("2 · Fill","pump water into the\nring moulds"),("3 · Freeze","radiate heat to space\nin shade; seal the bags"),
("4 · Tension","tighten the fibre hoops;\nice is pre-squeezed"),("5 · Spin up","counter-rotate to ≈2 MPa;\nhold for months"),("6 · Measure","strain, cracks, creep,\nsublimation, radiation dose")]
for i,(a,b) in enumerate(steps):
    x=i+0.05
    sx.add_patch(FancyBboxPatch((x,0.08),0.85,0.68,boxstyle="round,pad=0.01,rounding_size=0.04",fc="#fbf8f3",ec="#d8cdbf"))
    sx.text(x+0.05,0.66,a,fontsize=11,fontweight="bold",va="top"); sx.text(x+0.05,0.44,b,fontsize=9.5,va="top",linespacing=1.4)
    if i<5: sx.annotate("",xy=(x+0.97,0.42),xytext=(x+0.87,0.42),arrowprops=dict(arrowstyle="-|>",color=MUTED))
fig.savefig("Y2_icering1.png",dpi=130,facecolor=BG)
