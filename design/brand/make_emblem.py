import math
INK="#141414"; GREEN="#2F6B5E"
def arcpath(cx,cy,r,a0,a1):
    # angles in degrees, math convention, draw from a0 to a1 counterclockwise visually (large arc)
    p0=(cx+r*math.cos(math.radians(a0)), cy-r*math.sin(math.radians(a0)))
    p1=(cx+r*math.cos(math.radians(a1)), cy-r*math.sin(math.radians(a1)))
    large=1 if (a1-a0)%360>180 else 0
    return f'M{p0[0]:.2f} {p0[1]:.2f} A{r} {r} 0 {large} 0 {p1[0]:.2f} {p1[1]:.2f}'
def dots(cx,cy,r,a0,a1,step,rad,ink):
    n=max(2,round(math.radians(a1-a0)*r/step))
    out=[]
    for k in range(n+1):
        a=math.radians(a0+(a1-a0)*k/n)
        out.append(f'<circle cx="{cx+r*math.cos(a):.2f}" cy="{cy-r*math.sin(a):.2f}" r="{rad}" fill="{ink}"/>')
    return "".join(out)
def mark(rings, cx=36, cy=38, open_=110, sw=2.8, dr=1.55, step=4.4, ink=INK, accent=GREEN, center=3.8):
    a0=-90+open_/2; a1=270-open_/2
    s=[]
    for r,kind in rings:
        if kind=="s": s.append(f'<path d="{arcpath(cx,cy,r,a0,a1)}" fill="none" stroke="{ink}" stroke-width="{sw}" stroke-linecap="round"/>')
        else: s.append(dots(cx,cy,r,a0,a1,step,dr,ink))
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{center}" fill="{accent}"/>')
    return "".join(s)
full=[(10,"d"),(15.5,"s"),(21,"d"),(26.5,"s"),(32,"d")]
small=[(12,"s"),(19,"d"),(26,"s")]
C=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72">{mark(full)}</svg>'
Cs=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72">{mark(small,sw=4.2,dr=2.3,step=6.5,center=5)}</svg>'
Ci=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72"><rect width="72" height="72" rx="16" fill="{GREEN}"/>{mark(small,cy=40,sw=4.2,dr=2.3,step=6.5,center=5,ink="#FFFFFF",accent="#FFFFFF")}</svg>'
Cd=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72"><rect width="72" height="72" fill="#141414"/>{mark(full,ink="#FFFFFF",accent="#6FB7A3")}</svg>'
for n,v in dict(C=C,Cs=Cs,Ci=Ci,Cd=Cd).items(): open(n+".svg","w").write(v)
html='<html><head><link href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Display&display=swap" rel="stylesheet"></head><body style="margin:0;background:#fff;padding:30px;font-family:serif">'
html+='<div style="display:flex;gap:40px;align-items:center">'+''.join(f'<div style="display:flex;flex-direction:column;gap:14px;align-items:center"><img src="{f}" width="200"><img src="{f}" width="48"><img src="{f}" width="20"></div>' for f in ["C.svg","Cs.svg","Ci.svg","Cd.svg"])+'</div>'
html+='<div style="display:flex;align-items:center;gap:18px;margin-top:30px;font-family:\'Libre Caslon Display\';font-size:64px">Congress<img src="C.svg" width="60">Terminal</div></body></html>'
open("sheet2.html","w").write(html)
