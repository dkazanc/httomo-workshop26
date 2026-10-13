"""Scientific schematic of the radial lookup implemented in alignment.py."""
from pathlib import Path
from math import hypot
from html import escape
out=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="470" viewBox="0 0 1100 470">', '<rect width="1100" height="470" fill="#191919"/>']
def text(x,y,label,size=23,color='#eeeeee'):
 out.append(f'<text x="{x}" y="{y}" text-anchor="middle" fill="{color}" font-family="Arial,sans-serif" font-size="{size}">{escape(label)}</text>')
b2=0.2/150**2
for cx,title,warped,color in [(260,'Corrected output grid',False,'#65cbd5'),(840,'Sample locations in the input',True,'#f2c879')]:
 text(cx,37,title,27)
 for fixed in range(-120,121,40):
  for swap in (False,True):
   pts=[]
   for t in range(-120,121,3):
    x,y=(fixed,t) if swap else (t,fixed)
    q=1+b2*(x*x+y*y) if warped else 1
    pts.append(f'{cx+x*q:.2f},{225+y*q:.2f}')
   out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2"/>')
 out.append(f'<circle cx="{cx}" cy="225" r="6" fill="#ffffff"/>')
 text(cx,415,'White dot: distortion centre',21)
out.append('<path d="M450 225 H630 M615 215 L630 225 L615 235" stroke="#eeeeee" stroke-width="3" fill="none"/>')
text(540,180,'Radial lookup',22)
text(550,456,'Illustrative model: q(r) = 1 + 0.2(r / 150)²; coordinates in pixels. Not a calibration.',21)
out.append('</svg>')
Path('images/distortion-coefficient-map.svg').write_text('\n'.join(out))
