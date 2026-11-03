import numpy as np, math, json
from scipy.optimize import brentq
g=3.71; rho=917.0; E0=9.0e9; Lf=334e3; cp=1700.0
gam=36.0; kap=0.5; FSreq=2.5; yrs=30; td=yrs*365.25*86400
Astar=3.5e-25; Tstar=263.15; Qc=6.0e4; Rg=8.314
Tin=20.0; Rins=4.0
def A(Tk): return Astar*math.exp(-Qc/Rg*(1/Tk-1/Tstar))
def kice(Tk): return 9.828*math.exp(-0.0057*Tk)
def catenary(L,h):
    a=brentq(lambda a: a*(math.cosh(L/(2*a))-1)-h, 0.5, 1e4)
    s=2*a*math.sinh(L/(2*a)); return a,s
def thermal(t,To,R=Rins):
    # iterate k at mean temp
    Ti=To; 
    for _ in range(30):
        k=kice(273.15+(Ti+To)/2); q=(Tin-To)/(R+t/k); Ti=To+q*t/k
    return q,Ti,k
AMP={"desain":15.0,"buruk":30.0}
def Aeff(To,Ti,amp=0.0):
    z=np.linspace(0,1,61); ph=np.linspace(0,2*np.pi,73)[:-1]
    vals=[A(273.15+To+amp*math.sin(p)+(Ti-To)*zz) for p in ph for zz in z]
    return float(np.mean(vals))
def Eeff(sig,Ae):
    ec=(2/9)*Ae*sig**3*td; return sig/(sig/E0+ec), ec
def FS(t,L,s,sig,To,R=Rins,amp=15.0):
    q,Ti,k=thermal(t,To,R); Ae=Aeff(To,Ti,amp); E,ec=Eeff(sig,Ae)
    qcr=gam*kap*E*t**3/12/L**3; w=rho*g*t*s/L
    return qcr/w, dict(q=q,Ti=Ti,k=k,Aeff=Ae,E=E,ec=ec)
rows=[]
for L in (16,24,32,40):
    h=0.5625*L; a,s=catenary(L,h); sig=rho*g*(a+h)
    # required t at design case To=-60
    t=brentq(lambda t: FS(t,L,s,sig,-60)[0]-FSreq, 0.05, 10)
    t_d=max(math.ceil(t*20)/20,0.6)   # round up to 5 cm; >=0.6 m for radiation shielding
    fs_d,info=FS(t_d,L,s,sig,-60)
    fs_w,infow=FS(t_d,L,s,sig,-55,amp=30.0)
    try: t_w=brentq(lambda t: FS(t,L,s,sig,-55,amp=30.0)[0]-FSreq, 0.05, 8)
    except ValueError: t_w=float('nan')
    H=rho*g*t_d*a  # thrust per m width
    R1=20+L/2; Ain=2*math.pi*R1*s
    qmelt=info['k']*(0-(-60))/t_d
    alpha=info['k']/(rho*cp); tau=t_d**2/alpha/86400
    mslice=2.5*s*t_d*rho/1000
    rows.append(dict(L=L,h=h,a=a,s=s,sig=sig/1e3,t_req=t,t=t_d,FS=fs_d,FSw=fs_w,t_w=t_w,
        q=info['q'],Ti=info['Ti'],Tiw=infow['Ti'],E=info['E']/1e9,Ew=infow['E']/1e9,ec=info['ec'],ecw=infow['ec'],
        H=H/1e3,Htie=H*2.5/1e3,R1=R1,Ain=Ain,Ploss=info['q']*Ain/1e3,qmelt=qmelt,tau=tau,mslice=mslice,
        crush=5e6/sig))
for r in rows: print({k:(round(v,4) if isinstance(v,float) else v) for k,v in r.items()})
# sensitivity: inner temp vs insulation for L=32 design t
r32=[r for r in rows if r['L']==32][0]
sens=[]
for R in (0.25,0.5,1,2,4,8):
    q,Ti,k=thermal(r32['t'],-60,R); fs,_=FS(r32['t'],32,r32['s'],r32['sig']*1e3,-60,R)
    sens.append(dict(R=R,q=q,Ti=Ti,FS=fs,P=q*r32['Ain']/1e3))
for x in sens: print({k:round(v,3) for k,v in x.items()})
print("A(-60),A(-50),A(-40),A(-20),A(-10):",[f"{A(273.15+T):.2e}" for T in (-60,-50,-40,-20,-10)])
# melt rate example: excess flux 150 W/m2
print("melt rate cm/day for 150 W/m2 excess:",150/(rho*Lf)*86400*100)
alpha=kice(213.15)/(rho*cp); sol=88775.0; yr=686.98*sol
extra=dict(alpha=alpha,d_day=math.sqrt(alpha*sol/math.pi),d_year=math.sqrt(alpha*yr/math.pi),k60=kice(213.15),A=[A(273.15+T) for T in (-60,-50,-40,-20,-10)])
print(extra)
json.dump(dict(rows=rows,sens=sens,extra=extra),open("results.json","w"),indent=1)
