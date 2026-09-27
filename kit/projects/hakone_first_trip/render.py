import numpy as np, pickle, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import stills as S, blur
import os, json
U=S.U
W,H,IW,IH,IY=1080,1920,1080,1350,210
FPS=30; OS=1.3
scenes=[(d['file'],tuple(d['crop']),d['top'],d['title'],d['sub']) for d in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'scenes.json')))]
n=len(scenes)
dur=[1.45]*n
dur[0]=2.2; dur[9]=1.6; dur[10]=1.9; dur[12]=1.7; dur[15]=1.7; dur[16]=2.8
XF=0.3
hard={15}  # cut between 15->16 (serious -> grin)
starts=np.cumsum([0]+dur[:-1]); TOTAL=starts[-1]+dur[-1]
# camera moves: (z0,z1,px0,px1,py0,py1)
moves=[]
for i in range(n):
    if i%2==0: moves.append((1.0,1.09,0,0.01,0,-0.01))
    else: moves.append((1.1,1.02,0.015,-0.01,0.01,0))
moves[0]=(1.0,1.12,0,0,0,-0.02)
moves[16]=None
JP=S.JP; LT=S.LT
fT=ImageFont.truetype(JP,58); fL=ImageFont.truetype(LT,30); fS=ImageFont.truetype(LT,26)
# sources
srcs=[]
for (name,box,*_) in scenes:
    im=Image.open(U+name+'.jpeg').convert('RGB'); im=blur.apply(name,im)
    im=im.crop(box).resize((int(IW*OS),int(IH*OS)),Image.LANCZOS)
    srcs.append(S.grade(im))
y,x=np.mgrid[0:IH,0:IW]; d=np.sqrt(((x-IW/2)/(IW/2))**2+((y-IH/2)/(IH/2))**2)
VIG=np.clip(1-0.38*np.clip(d-0.45,0,1)**1.5,0,1)[...,None].astype(np.float32)
rng=np.random.default_rng(1); GR=[rng.normal(0,3.2,(H,W,1)).astype(np.float32) for _ in range(6)]
def ease(t): t=min(max(t,0),1); return 1-(1-t)**3
def soft(t): t=min(max(t,0),1); return t*t*(3-2*t)
def cam(i,lt):
    D=dur[i]; u=lt/D
    if moves[i] is None:  # punch-in then drift
        z=1.13-0.10*ease(lt/0.45)+0.03*soft((lt-0.45)/(D-0.45)); px=py=0
    else:
        z0,z1,a0,a1,b0,b1=moves[i]; p=0.75*u+0.25*soft(u)
        z=z0+(z1-z0)*p; px=a0+(a1-a0)*p; py=b0+(b1-b0)*p
    z=max(z,1.0); SW,SH=srcs[i].size; vw,vh=SW/z,SH/z
    cx=SW/2+px*SW; cy=SH/2+py*SH
    cx=min(max(cx,vw/2),SW-vw/2); cy=min(max(cy,vh/2),SH-vh/2)
    return (cx-vw/2,cy-vh/2,cx+vw/2,cy+vh/2)
def spaced(dr,cx,y,t,f,fill,sp):
    tw=sum(dr.textlength(c,font=f)+sp for c in t)-sp; xx=cx-tw/2
    for c in t: dr.text((xx,y),c,font=f,fill=fill); xx+=dr.textlength(c,font=f)+sp
def scene_frame(i,lt):
    img=srcs[i].resize((IW,IH),Image.BILINEAR,box=cam(i,lt))
    a=np.asarray(img).astype(np.float32)*VIG
    can=np.full((H,W,3),8,np.float32); can[IY:IY+IH]=a
    c=Image.fromarray(can.astype(np.uint8)); dr=ImageDraw.Draw(c)
    _,_,top,title,sub=scenes[i]
    d0=0.05 if i!=16 else 0.35
    aL=ease((lt-d0)/0.5); aT=ease((lt-d0-0.15)/0.55); aS=ease((lt-d0-0.35)/0.6)
    g=lambda v,al:(int(8+(v-8)*al),)*3
    if aL>0: spaced(dr,W/2,120,top,fL,g(200,aL),8+10*(1-aL))
    if aT>0:
        tw=dr.textlength(title,font=fT); dr.text(((W-tw)/2,1620+22*(1-aT)),title,font=fT,fill=g(240,aT))
    if aS>0: spaced(dr,W/2,1725,sub,fS,g(150,aS),5+6*(1-aS))
    return np.asarray(c).astype(np.float32)
import sys
# 使い方: python render.py [開始フレーム 終了フレーム 出力.mp4]  引数なしなら全編を out.mp4 に書き出す
F0,F1,OUT=(int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]) if len(sys.argv)>3 else (0,10**9,'out_noaudio.mp4')
cmd=['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
     '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',OUT]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
NF=int(TOTAL*FPS)
for f in range(F0,min(F1,NF)):
    t=f/FPS
    i=int(np.searchsorted(starts,t,side='right')-1)
    fr=scene_frame(i,t-starts[i])
    # crossfade into next
    if i+1<n and i not in hard:
        tn=starts[i+1]-t
        if tn<XF:
            k=soft(1-tn/XF); fr=fr*(1-k)+scene_frame(i+1,t-starts[i+1])*k
    fr=fr+GR[f%6]
    if t<0.5: fr=8+(fr-8)*soft(t/0.5)*1 if False else fr*soft(t/0.5)
    if TOTAL-t<0.6: fr=fr*soft((TOTAL-t)/0.6)
    p.stdin.write(np.clip(fr,0,255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait(); print('done',TOTAL,NF)
