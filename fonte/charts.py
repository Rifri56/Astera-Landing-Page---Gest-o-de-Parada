import math
def logi(t,k=0.55,m=7,T=14):
    f=lambda x:1/(1+math.exp(-k*(x-m)))
    return (f(t)-f(0))/(f(T)-f(0))
def path(pts): return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)
def curve(x0,x1,y0,y1,tmax=14,tend=14,scale=1.0,n=120):
    pts=[]
    for i in range(n+1):
        t=tend*i/n; v=logi(t)*scale if t>0 else 0
        pts.append((x0+(x1-x0)*t/tmax, y0-(y0-y1)*v))
    return pts
def actual(x0,x1,y0,y1,tend=8):
    # realized: slightly lagging, bumpy
    fac=[1,0.98,0.97,0.96,0.965,0.955,0.95,0.955,0.958]
    pts=[]
    for d in range(tend+1):
        v=logi(d)*fac[d]
        pts.append((x0+(x1-x0)*d/14, y0-(y0-y1)*v))
    return pts
