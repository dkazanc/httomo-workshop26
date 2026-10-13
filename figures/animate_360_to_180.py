"""Educational parallel-beam half-acquisition animation, after Vo et al. (2021)."""
from pathlib import Path
import math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
W,H,FPS,DURATION=1280,720,24,60
BG='#191919'; FG='#f1f4f5'; MUT='#b6c0c7'; A='#56d9db'; B='#db8df2'; GOLD='#ffcf66'
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F=lambda n:ImageFont.truetype(font,n)
# Exact analytic line integrals through a synthetic collection of circular disks.
s=np.linspace(-1,1,600); th=np.arange(180)*np.pi/180
full=np.zeros((180,600))
disks=[(0,0,.88,.3),(-.38,.28,.20,.7),(.36,-.22,.27,.5),(.13,.42,.12,.9),(-.24,-.42,.13,.8)]
for x,y,r,mu in disks:
 q=s[None,:]-(x*np.cos(th)+y*np.sin(th))[:,None]
 full+=2*mu*np.sqrt(np.maximum(r*r-q*q,0))
full=np.uint8(full/full.max()*225+12)
a=full[:,270:]; b=full[:,:330][:,::-1]; bf=b[:,::-1]; raw=np.vstack([a,b])
assert np.array_equal(a[:,:60],bf[:,-60:])
# Linear-ramp blending of the common measurements.
w=np.linspace(0,1,60)[None,:]
joined=np.concatenate([bf[:,:270],np.uint8(np.rint((1-w)*bf[:,270:]+w*a[:,:60])),a[:,60:]],axis=1)
assert np.array_equal(joined,full)
def txt(d,xy,t,size=26,color=FG): d.text(xy,t,font=F(size),fill=color)
def arrow(d,p,q,c=FG):
 d.line([p,q],fill=c,width=3); ang=math.atan2(q[1]-p[1],q[0]-p[0])
 d.polygon([q,(q[0]-14*math.cos(ang-.45),q[1]-14*math.sin(ang-.45)),(q[0]-14*math.cos(ang+.45),q[1]-14*math.sin(ang+.45))],fill=c)
def panel(im,d,data,box,color,label=None):
 x,y,w,h=map(int,box); im.paste(Image.fromarray(data).convert('RGB').resize((max(w,1),h)),(x,y)); d.rectangle((x,y,x+w,y+h),outline=color,width=3)
 if label:txt(d,(x,y-38),label,24,color)
def smooth(v): v=max(0,min(1,v)); return v*v*(3-2*v)
def base(t,k,title,sub):
 im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
 txt(d,(50,27),'360° → 180°  |  Extended field of view  |  Synthetic example',18,MUT)
 txt(d,(50,70),title,36);txt(d,(50,122),sub,23,MUT)
 for j,n in enumerate(['Acquire','Split','Flip','Align + blend','Reconstruct']):
  x=50+j*242; d.rounded_rectangle((x,635,x+222,674),radius=9,fill='#343434' if j!=k else '#365052');txt(d,(x+12,643),f'{j+1}  {n}',19,FG if j==k else MUT)
 txt(d,(50,690),'Based on Vo et al. (2021), §2.1.1.1, Fig. 1  •  doi:10.1364/OE.418448',14,MUT)
 d.line((0,718,int(W*t/DURATION),718),fill=A,width=3)
 return im,d
def frame(t):
 k=min(4,int(t//12)); u=(t%12)/12
 titles=['1. Collect complementary views over 360°','2. Split the sinogram into two angular halves','3. Flip the second half left to right','4. Align the overlap, then blend','5. Reconstruct from a wider 180° sinogram']
 subs=['An offset rotation axis lets the detector see different parts of a large sample.', 'A sinogram stacks one detector row across all projection angles.', 'Pair each view at θ with the view at θ + 180°.', 'Match the shared sample features; the overlap can be on either side.', 'Repeat for every detector row to reconstruct the full volume.']
 im,d=base(t,k,titles[k],subs[k])
 if k==0:
  cx,cy,r=325,345,155
  d.rectangle((cx-17,193,cx+173,536),fill='#233d3e')
  for x in range(cx-10,cx+170,31):arrow(d,(x,178),(x,211),A)
  ang=u*2*math.pi
  for x,y,rad,mu in disks:
   xx=cx+r*(x*math.cos(ang)-y*math.sin(ang)); yy=cy+r*(x*math.sin(ang)+y*math.cos(ang))
   rr=r*rad;d.ellipse((xx-rr,yy-rr,xx+rr,yy+rr),outline=FG if rad>.8 else GOLD,width=3)
  d.line((cx,205,cx,516),fill=GOLD,width=2);d.ellipse((cx-5,cy-5,cx+5,cy+5),fill=GOLD)
  d.line((cx-17,535,cx+173,535),fill=A,width=8)
  txt(d,(cx-10,550),'Detector',23,A);txt(d,(64,540),'Rotation axis',21,GOLD)
  arrow(d,(218,546),(cx,507),GOLD)
  txt(d,(625,215),f'Rotation: {int(u*360):03d}°',36,A)
  for j,line in enumerate(['The sample is wider than one view.','The axis is near a detector edge.','After 180°, the opposite side is seen.','A shared strip provides overlap.']):txt(d,(625,295+j*54),line,24)
  txt(d,(65,591),'Parallel-beam geometry • schematic top view',19,MUT)
 elif k==1:
  panel(im,d,raw,(130,195,300,350),FG,'Recorded 360° sinogram')
  d.line((130,370,430,370),fill=GOLD,width=3)
  txt(d,(66,195),'0°',22);txt(d,(48,353),'180°',22);txt(d,(48,520),'360°',22)
  panel(im,d,a,(690,208,330,145),A,'A: 0° to <180°')
  panel(im,d,b,(690,418,330,145),B,'B: 180° to <360°')
  arrow(d,(457,282),(655,282),A);arrow(d,(457,460),(655,490),B)
  txt(d,(140,578),'Detector position →',22,MUT)
  txt(d,(1044,265),'N rows',21,A);txt(d,(1044,473),'N rows',21,B)
 elif k==2:
  panel(im,d,a,(100,245,430,235),A,'A stays unchanged')
  v=smooth((u-.15)/.55);scale=abs(math.cos(v*math.pi));width=max(2,int(430*scale))
  panel(im,d,b if v<.5 else bf,(745+(430-width)/2,245,width,235),B,'')
  txt(d,(745,207),'B: horizontal flip',24,B)
  arrow(d,(773,513),(1141,513),B);arrow(d,(1141,526),(773,526),B)
  txt(d,(100,548),'Keep the angular row order.',25,GOLD)
  txt(d,(100,587),'Opposite views contain the same ray integrals, with reversed detector coordinates.',23)
 elif k==3:
  # B-flipped goes on the left for this particular offset direction.
  v=smooth((u-.05)/.5); xB=90+140*v; xA=790-290*v
  panel(im,d,bf,(xB,255,330,215),B,'Flipped B')
  panel(im,d,a,(xA,255,330,215),A,'A')
  if v>.98:
   d.rectangle((500,255,560,470),outline=GOLD,width=4)
   txt(d,(465,485),'Overlap O',24,GOLD)
   if u>.66:
    # Display the complementary linear weights below the overlap.
    arrow(d,(850,278),(1040,278),GOLD)
    txt(d,(875,321),'Blend weights',21,GOLD)
    d.line((884,441,1054,371),fill=A,width=4);d.line((884,371,1054,441),fill=B,width=4)
    txt(d,(880,464),'wA + wB = 1',21)
  txt(d,(100,552),'Find the correct side and overlap width from matching structure.',25)
  txt(d,(100,588),'A linear ramp combines the shared pixels without a hard seam.',24,MUT)
 else:
  panel(im,d,joined,(135,222,780,285),FG,'Stitched data: 0° to <180°')
  # Colour underlines identify the contributing halves, with shared gold area.
  d.line((135,517,486,517),fill=B,width=5);d.line((486,517,564,517),fill=GOLD,width=5);d.line((564,517,915,517),fill=A,width=5)
  txt(d,(959,276),'Width:',24,MUT);txt(d,(959,318),'2W − O',32,GOLD)
  txt(d,(959,385),'N angles',27,A)
  txt(d,(952,440),'W: input width',19,MUT)
  txt(d,(952,470),'O: overlap width',19,MUT)
  txt(d,(135,548),'2N × W  →  N × (2W − O)',30)
  txt(d,(135,591),'Half the angular rows • wider detector coverage • standard 180° reconstruction',23,MUT)
 return im
out=ROOT/'videos'/'360-to-180-tomography.mp4'
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
for i in range(FPS*DURATION):
 im=frame(i/FPS)
 if i in [144,432,720,1080,1368]: im.save(ROOT/'videos'/f'check-{i}.png')
 p.stdin.write(im.tobytes())
p.stdin.close(); assert p.wait()==0
frame(56).save(ROOT/'videos'/'360-to-180-poster.png')
print(out)
