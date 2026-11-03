import numpy as np, math, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch, Circle
plt.rcParams["svg.fonttype"]="none"
plt.rcParams["font.family"]="Inter" if "Inter" in [f.name for f in matplotlib.font_manager.fontManager.ttflist] else "DejaVu Sans"
INK="#111111"; MUT="#6b6b6b"; ICE="#9cc6de"; ICED="#5f9bc0"; CO2="#e9e4f2"; ROD="#c4502a"; SAND="#e3cdb6"; MOD="#f2d9b8"
fig=plt.figure(figsize=(18,10.5),facecolor="white")
fig.text(0.02,0.955,"ICE AS A BUILDING MATERIAL",fontsize=26,fontweight="bold",color=INK)
fig.text(0.02,0.92,"One material, three jobs: keeping out the cold together with a CO₂ layer, stopping radiation, and carrying its own weight.",fontsize=12,color=MUT)
cols=[0.02,0.355,0.69]; W=0.29
heads=["1  INSULATION","2  RADIATION SHIELDING","3  STRUCTURAL INTEGRITY"]
for x,h in zip(cols,heads): fig.text(x,0.86,h,fontsize=15,fontweight="bold",color=INK)
# ---------- 1 insulation: layer section with temperature profile ----------
ax=fig.add_axes([cols[0],0.53,W,0.31]); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(-75,40)
layers=[(0,2.2,"#fbf3e6","living\nspace"),(2.2,2.6,MOD,""),(2.6,4.6,CO2,"metal-lined\nCO₂ cells"),(4.6,8.2,ICE,"ice"),(8.2,10,"#f6efe6","outside")]
for a,b,c,t in layers:
    ax.add_patch(Rectangle((a,-75),b-a,115,fc=c,ec="none"))
    if t: ax.text((a+b)/2,-70,t,ha="center",va="bottom",fontsize=10,color=INK)
for x in (2.6,3.1,3.6,4.1,4.6): ax.plot([x,x],[-75,40],color="#a9a2b8",lw=1.2)
ax.text(2.4,36,"module",rotation=90,fontsize=8.5,ha="center",va="top",color=MUT)
# temperature profile: 20 -> (modul) 19 -> co2 big drop to -52 -> ice to -60
px=[0,2.2,2.6,4.6,8.2,10]; py=[20,19,18.5,-52,-60,-60]
ax.plot(px,py,color=ROD,lw=2.6)
for (x,y,t,dx,ha) in ((1.1,20,"20 °C",0,"center"),(4.6,-52,"−52 °C",0.15,"left"),(9.1,-60,"−60 °C",0,"center")):
    ax.plot(x,y,"o",color=ROD,ms=5); ax.text(x+dx,y+4,t,fontsize=10.5,fontweight="bold",color=ROD,ha=ha)
ax.text(3.9,8,"temperature drops\nin the CO₂ layer",ha="center",fontsize=9,color=ROD)
ax.text(6.4,-30,"ice stays ≤ −50 °C",ha="center",fontsize=9.5,color=INK)
tx=fig.text
def block(x,y,head,body):
    fig.text(x,y,head,fontsize=12.5,fontweight="bold",va="top")
    n=body.count("\n")+1
    fig.text(x,y-0.03,body,fontsize=10.5,va="top",linespacing=1.45)
    return y-0.03-n*0.0235-0.03
y0=0.49
y0=block(cols[0],globals().get("y0",y0),"Ice is not a good insulator.","Its conductivity is ±2.9 W/m·K at −60 °C, about the same as granite.\nThe real insulator is the layer of CO₂ cells (±0.01 W/m·K). The cell\nwalls carry a metal film so heat cannot leak out as radiation.")
y0=block(cols[0],globals().get("y0",y0),"Insulation works both ways:","it keeps the habitat warm and keeps the ice cold.\nWarmer ice creeps faster (see 3). Target: R ≥ 4 m²K/W.")
y0=block(cols[0],globals().get("y0",y0),"Thermal mass:","the day–night temperature swing reaches only ±23 cm into the ice,\nso the interior does not follow the outside cycle.")
# ---------- 2 radiation ----------
bx=fig.add_axes([cols[1],0.53,W,0.31]); bx.axis("off"); bx.set_xlim(-11,11); bx.set_ylim(-2,13); bx.set_aspect("equal")
bx.add_patch(Rectangle((-11,-2),22,2,fc=SAND,ec="none"))
th=np.linspace(0,np.pi,100)
for r,c in ((8.2,ICE),(7.0,"white")):
    bx.fill_between(r*np.cos(th),0,r*np.sin(th),color=c)
bx.add_patch(Rectangle((-4,0),8,2.2,fc=MOD,ec="none")); bx.text(0,1.0,"habitat",ha="center",fontsize=9)
import random
random.seed(3)
for i,(x0,ang,stop) in enumerate([(-6.5,-60,True),(-4,-80,True),(2,-95,True),(7,-115,True),(10.5,-125,False)]):
    a=math.radians(ang); L=6.0
    sx,sy=x0,12.5; ex,ey=sx+L*math.cos(a)*1.0,sy+L*math.sin(a)
    col="#7a57b8"
    bx.add_patch(FancyArrowPatch((sx,sy),(ex,ey),arrowstyle="-|>",mutation_scale=12,color=col,lw=1.4))
bx.text(-10.8,12.3,"cosmic rays +\nsolar particles",fontsize=9,color="#7a57b8",va="top")
bx.text(0,9.1,"ice 55–115 g/cm²",ha="center",fontsize=10,fontweight="bold",color=INK)
bx.text(8.6,1.0,"the ground blocks\nhalf the sky\n(from below)",fontsize=8.5,color=MUT,ha="left")
y1=block(cols[1],globals().get("y1",0.49),"Water is an excellent shield.","Ice is rich in hydrogen. Light hydrogen nuclei slow particles down\nwithout shattering them into many secondary particles, unlike\nmetals or heavy rock.")
y1=block(cols[1],globals().get("y1",0.49),"Dose on the Martian surface: ±0.64 mSv/day","(±230 mSv/year, measured by the Curiosity rover). A 0.6 m ice shell\n= ±55 g/cm², plus ±20 g/cm² of atmosphere. Most solar particle\nstorms are stopped; galactic cosmic rays are reduced gradually.")
y1=block(cols[1],globals().get("y1",0.49),"Still lets light in:","clear ice transmits daylight. Freezing from the bottom up\npushes bubbles out, so the ice does not turn cloudy.")
# ---------- 3 structure ----------
cx=fig.add_axes([cols[2],0.53,W,0.31]); cx.axis("off"); cx.set_xlim(-11,11); cx.set_ylim(-2,13); cx.set_aspect("equal")
cx.add_patch(Rectangle((-11,-2),22,2,fc=SAND,ec="none"))
a=4.56*1.0; L=16; h=9
xs=np.linspace(-8,8,120); ys=h-a*(np.cosh(xs/a)-1)
dy=np.gradient(ys,xs); nn=np.c_[-dy,np.ones_like(xs)]/np.sqrt(1+dy**2)[:,None]
P=np.c_[xs,ys]; cx.add_patch(Polygon(np.r_[P+0.35*nn,(P-0.35*nn)[::-1]],fc=ICE,ec=INK,lw=1))
for u in (-6.5,-3.5,3.5,6.5):
    i=np.argmin(abs(xs-u)); t=np.array([1,dy[i]])/math.hypot(1,dy[i]); p=P[i]+0.9*nn[i]
    for sgn in (1,-1):
        cx.add_patch(FancyArrowPatch(p+sgn*t*1.6,p+sgn*t*0.35,arrowstyle="-|>",mutation_scale=11,color=ROD,lw=1.3))
cx.text(0,10.6,"the arch is only squeezed,\nnever pulled",ha="center",fontsize=10,color=ROD,fontweight="bold")
cx.add_patch(FancyArrowPatch((-8,-0.6),(8,-0.6),arrowstyle="<->",mutation_scale=10,color=INK,lw=1))
cx.text(0,-1.6,"floor ties resist the thrust at the feet",ha="center",fontsize=8.5,color=MUT)
y2=block(cols[2],globals().get("y2",0.49),"Strong in compression, weak in tension.","Cold ice crushes above ±5 MPa in compression but cracks at ±1 MPa\nin tension. A catenary shape keeps the arch in compression only:\n46 kPa (16 m span) to 92 kPa (32 m), over 50× below crushing.")
y2=block(cols[2],globals().get("y2",0.49),"The real limit: creep.","Ice under load for years flows slowly, like a glacier. Every\n20 °C warmer makes creep 10–20× faster. So the ice is kept\n≤ −50 °C, and larger spans need thicker ice.")
y2=block(cols[2],globals().get("y2",0.49),"Shell thickness:","0.6 m for 16–24 m spans · 1.25 m for a 32 m span\n(buckling safety factor ≥ 2.5 after 30 years).")
fig.text(0.02,0.12,"Sources: Hassler et al. 2014 (Science, Curiosity RAD); Cuffey & Paterson 2010 (ice creep); Petrenko & Whitworth 1999 (ice properties); team calculations (structural integrity appendix).",fontsize=8.5,color=MUT)
for f in ("png","svg"): fig.savefig(f"ice_properties.{f}",dpi=220,facecolor="white",bbox_inches="tight",pad_inches=0.3)
