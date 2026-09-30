import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import base64, math
from charts import *
def fb(n): return base64.b64encode(open(f'fonts/{n}.woff2','rb').read()).decode()
LOGO=open('logo_nav.b64').read(); LOGONEG=open('logo_neg.b64').read(); FAV=open('fav.b64').read()
FAVSVG=("<svg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 96 96'>"
        f"<image width='96' height='96' href='data:image/png;base64,{FAV}'/></svg>")
FAVURI='data:image/svg+xml;base64,'+base64.b64encode(FAVSVG.encode()).decode()

# ---------- HERO DRAWING (technical sheet of an S-curve) ----------
X0,X1,Y0,Y1=70,690,390,60
plan=curve(X0,X1,Y0,Y1); act=actual(X0,X1,Y0,Y1)
dayx=lambda d:X0+(X1-X0)*d/14
ticks=''.join(f'<line x1="{dayx(d):.1f}" y1="{Y0}" x2="{dayx(d):.1f}" y2="{Y0+ (9 if d%7==0 else 5)}"/>' for d in range(15))
yt=''.join(f'<line x1="{X0-(9 if p%50==0 else 5)}" y1="{Y0-(Y0-Y1)*p/100:.1f}" x2="{X0}" y2="{Y0-(Y0-Y1)*p/100:.1f}"/>' for p in range(0,101,25))
ax,ay=act[-1]
HERO_SVG=f'''<svg class="folha" viewBox="0 0 760 470" aria-hidden="true" focusable="false">
 <defs><marker id="seta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9" fill="none" stroke="currentColor" stroke-width="1.4"/></marker></defs>
 <g class="eixos">
  <path d="M{X0},{Y1-20} L{X0},{Y0} L{X1+20},{Y0}"/>
  {ticks}{yt}
  <line class="guia" x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}"/>
  <line class="guia" x1="{X1}" y1="{Y1}" x2="{X1}" y2="{Y0}"/>
 </g>
 <g class="cota">
  <line x1="{X0}" y1="{Y0+34}" x2="{X1}" y2="{Y0+34}" marker-start="url(#seta)" marker-end="url(#seta)"/>
  <line x1="{X0}" y1="{Y0+14}" x2="{X0}" y2="{Y0+42}"/><line x1="{X1}" y1="{Y0+14}" x2="{X1}" y2="{Y0+42}"/>
  <text x="{(X0+X1)/2}" y="{Y0+56}" text-anchor="middle">prazo da parada: 14 dias</text>
  <line x1="{X1+44}" y1="{Y1}" x2="{X1+44}" y2="{Y0}" marker-start="url(#seta)" marker-end="url(#seta)"/>
  <text x="{X1+56}" y="{(Y0+Y1)/2}" transform="rotate(90 {X1+56} {(Y0+Y1)/2})" text-anchor="middle">avanço físico 100%</text>
 </g>
 <path class="previsto" d="{path(plan)}"/>
 <path class="realizado" pathLength="1" d="{path(act)}"/>
 <g class="hoje">
  <line x1="{ax:.1f}" y1="{Y0}" x2="{ax:.1f}" y2="{ay-40:.1f}"/>
  <circle cx="{ax:.1f}" cy="{ay:.1f}" r="6"/>
  <text x="{ax-14:.1f}" y="{ay-26:.1f}" text-anchor="end">dia 8: 61,3% realizado</text>
  <text x="{ax-14:.1f}" y="{ay-8:.1f}" class="sub" text-anchor="end">previsto 64,0%</text>
 </g>
</svg>'''

# ---------- DASHBOARD S-curve ----------
a,b,c,d=46,540,212,18
p2=curve(a,b,c,d); r2=actual(a,b,c,d)
hx,hy=r2[-1]
grid=''.join(f'<line x1="{a}" x2="{b}" y1="{c-(c-d)*p/100:.1f}" y2="{c-(c-d)*p/100:.1f}"/><text x="{a-8}" y="{c-(c-d)*p/100+4:.1f}" text-anchor="end">{p}%</text>' for p in (0,25,50,75,100))
xl=''.join(f'<text x="{a+(b-a)*dd/14:.1f}" y="{c+18}" text-anchor="middle">D{dd}</text>' for dd in (0,2,4,6,8,10,12,14))
area=path(r2)+f' L{hx:.1f},{c} L{a},{c} Z'
DASH_CURVE=f'''<svg viewBox="0 0 560 236" role="img" aria-label="Curva S da parada: previsto 64,0% e realizado 61,3% no dia 8 de 14">
 <g class="g-grid">{grid}{xl}</g>
 <path class="g-area" d="{area}"/>
 <path class="g-prev" d="{path(p2)}"/>
 <path class="g-real" d="{path(r2)}"/>
 <line class="g-hoje" x1="{hx:.1f}" x2="{hx:.1f}" y1="{d}" y2="{c}"/>
 <circle class="g-pt" cx="{hx:.1f}" cy="{hy:.1f}" r="4.5"/>
</svg>'''

# ---------- Pareto ----------
par=[('Selo mecânico',31),('Rolamento',22),('Desalinhamento',14),('Correia',9),('Instrumentação',7),('Outros',5)]
tot=sum(v for _,v in par); bw=62; gx=40; H=170; top=16
bars='';cum=0;cpts=[]
for i,(n,v) in enumerate(par):
    x=gx+i*(bw+14); h=v/31*H*0.95; y=top+H-h
    cls='g-bar hot' if i<2 else 'g-bar'
    bars+=f'<rect class="{cls}" x="{x}" y="{y:.1f}" width="{bw}" height="{h:.1f}"/><text class="g-v" x="{x+bw/2}" y="{y-6:.1f}" text-anchor="middle">{v}</text><text class="g-l" x="{x+bw/2}" y="{top+H+16}" text-anchor="middle">{n.split()[0]}</text>'
    cum+=v; cpts.append((x+bw/2, top+H-(cum/tot)*H))
PARETO=f'''<svg viewBox="0 0 500 212" role="img" aria-label="Pareto de falhas de bombas centrífugas: selo mecânico e rolamento somam 60% das ocorrências">
 <line class="g-base" x1="30" x2="490" y1="{top+H}" y2="{top+H}"/>
 {bars}
 <path class="g-cum" d="{path(cpts)}"/>
 {''.join(f'<circle class="g-cumpt" cx="{x:.1f}" cy="{y:.1f}" r="3"/>' for x,y in cpts)}
</svg>'''

# ---------- MTBF sparkline ----------
mt=[212,198,230,241,236,268,281,295,322]
mx=lambda i:10+i*30; my=lambda v:78-(v-180)/160*66
MTBF=f'<svg viewBox="0 0 260 90" role="img" aria-label="MTBF subindo de 212 para 322 horas em 9 meses"><path class="g-mtbf" d="{path([(mx(i),my(v)) for i,v in enumerate(mt)])}"/><circle class="g-pt" cx="{mx(8)}" cy="{my(322):.1f}" r="4"/></svg>'

# ---------- Gantt ----------
gantt=[('Liberação e bloqueios (LOTO)',0,1,0,1,'ok',''),
       ('Montagem de andaimes',0.5,2.5,0.5,2.8,'ok',''),
       ('Troca de tubos: banco gerador',2,9,2.4,None,'crit','folga −6 h'),
       ('Refratário da fornalha',3,10,3.2,None,'aten','folga 4 h'),
       ('Revisão ventilador de tiragem',4,7,4,7,'ok',''),
       ('Inspeção NR-13 e teste hidrostático',9,12,None,None,'plan',''),
       ('Partida assistida',12,14,None,None,'plan','')]
G=''
for n,ps,pe,rs,re_,st,note in gantt:
    pl=f'<span class="gb-prev" style="left:{ps/14*100:.2f}%;width:{(pe-ps)/14*100:.2f}%"></span>'
    rl=''
    if rs is not None:
        end=re_ if re_ is not None else 8
        rl=f'<span class="gb-real {st}" style="left:{rs/14*100:.2f}%;width:{(end-rs)/14*100:.2f}%"></span>'
    nt=f'<em class="{st}">{note}</em>' if note else ''
    G+=f'<li><span class="gn">{n}{nt}</span><span class="gt">{pl}{rl}</span></li>'

PAGE=open('template.html').read()
for k,v in dict(FONT_R=fb('Barlow-Regular'),FONT_M=fb('Barlow-Medium'),FONT_SB=fb('Barlow-SemiBold'),
                FONT_CSB=fb('BarlowSemiCondensed-SemiBold'),FONT_CB=fb('BarlowSemiCondensed-Bold'),
                LOGO=LOGO,LOGONEG=LOGONEG,FAVURI=FAVURI,HERO_SVG=HERO_SVG,DASH_CURVE=DASH_CURVE,
                PARETO=PARETO,MTBF=MTBF,GANTT=G,HOJE=f'{8/14*100:.2f}').items():
    PAGE=PAGE.replace('{{'+k+'}}',v)
assert '{{' not in PAGE, PAGE[PAGE.find('{{'):PAGE.find('{{')+40]
open('../site/index.html','w').write(PAGE)
print('ok', len(PAGE)//1024,'KB')
