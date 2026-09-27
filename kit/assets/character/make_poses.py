"""ちび審査員の表情差分と切り抜きを作る(元絵: chibi_serious.png)
出力 poses/{serious,smile,shock}_{0,1,2}.png  … 0=口閉じ 1=半開き 2=開き。背景(赤丸・クリーム)は透過。
元絵を差し替えたら下の座標(BROW/EYE/MOUTH)を要調整。"""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,"poses"); os.makedirs(OUT,exist_ok=True)
src=Image.open(os.path.join(HERE,"chibi_serious.png")).convert("RGB"); A=np.asarray(src).astype(int)
SKIN=(253,231,206); INK=(64,44,42); LINE=(74,52,44); INSIDE=(140,52,56); TONGUE=(236,128,122); WHITE=(255,250,242)
EYES=[(385,515,556,664),(704,504,876,662)]; BROWS=[(450,462,582,522),(676,460,800,522)]
LASH=[(386,528,416,556),(526,530,552,556),(838,512,874,544)]
MOUTH=(594,645,658,695); CX,CY=626,666

# --- 背景の切り抜き: 赤丸+クリームのうち、外周につながる領域と赤い小領域を透過
red=(abs(A[...,0]-224)<40)&(abs(A[...,1]-103)<45)&(abs(A[...,2]-74)<45)
cream=(A[...,0]>240)&(A[...,1]>235)&(A[...,2]>215)&(A[...,2]<240)
lab,n=ndimage.label(red|cream)
border=set(np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]))-{0}
bg=np.isin(lab,list(border))
redlab,_=ndimage.label(red); sizes=ndimage.sum(red,redlab,range(1,redlab.max()+1))
bg|=np.isin(redlab,[i+1 for i,s in enumerate(sizes) if s>150])
alpha=Image.fromarray(((~bg)*255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))

def base_erase(eyes=True,brows=True):
    im=src.copy(); d=ImageDraw.Draw(im)
    if brows:
        for b in BROWS: d.rectangle(b,fill=SKIN)
    if eyes:
        for e in EYES: d.ellipse(e,fill=SKIN)
        for e in LASH: d.ellipse(e,fill=SKIN)   # まつ毛の先の消し残し
    d.ellipse(MOUTH,fill=SKIN)
    # ほっぺ(ピンク)は元絵から戻す
    a=np.asarray(im).copy(); pink=(A[...,1]<222)&(A[...,0]>235)&(A.sum(2)>560)
    zone=np.zeros(pink.shape,bool); zone[630:760,330:930]=True
    a[pink&zone]=A[pink&zone]
    return Image.fromarray(a.astype(np.uint8))

def mouth_open(d,w,h,cy=CY):
    d.ellipse((CX-w,cy-h+2,CX+w,cy+h+2),fill=INSIDE,outline=LINE,width=4)
    if h>10: d.chord((CX-w+6,cy+2,CX+w-6,cy+h+1),0,180,fill=TONGUE)

def serious(k):
    if k==0: return src.copy()
    im=base_erase(eyes=False,brows=False); d=ImageDraw.Draw(im); mouth_open(d,*[(15,9),(20,17)][k-1]); return im

def smile(k):
    im=base_erase(); d=ImageDraw.Draw(im)
    for (x0,y0,x1,y1) in EYES:   # にっこり閉じ目 ∩
        cx=(x0+x1)//2; d.arc((cx-52,590,cx+52,680),200,340,fill=INK,width=16)
    for (x0,y0,x1,y1) in BROWS:  # ゆるい眉
        d.arc((x0+10,y0+8,x1-10,y1+40),210,330,fill=INK,width=12)
    if k==0: d.arc((CX-34,625,CX+34,690),20,160,fill=LINE,width=8)
    else:
        h=[22,32][k-1]; d.chord((CX-38,CY-12,CX+38,CY-12+2*h),0,180,fill=INSIDE,outline=LINE,width=4)
        d.chord((CX-22,CY-12+h,CX+22,CY-12+2*h-4),0,180,fill=TONGUE)
    return im

def shock(k):
    im=base_erase(); d=ImageDraw.Draw(im)
    for (x0,y0,x1,y1) in EYES:   # まんまる目+キラキラ
        cx=(x0+x1)//2; cy=600
        d.ellipse((cx-62,cy-66,cx+62,cy+66),fill=WHITE,outline=INK,width=8)
        d.ellipse((cx-40,cy-40,cx+40,cy+44),fill=INK)
        d.ellipse((cx-24,cy-30,cx+2,cy-4),fill="white"); d.ellipse((cx+10,cy+10,cx+22,cy+22),fill="white")
    for (x0,y0,x1,y1) in BROWS:  # 上がった眉
        d.arc((x0+5,y0-18,x1-5,y1+10),200,340,fill=INK,width=12)
    w,h=[(10,12),(13,17),(17,24)][k]; mouth_open(d,w,h,CY+4)
    return im

for name,f in (("serious",serious),("smile",smile),("shock",shock)):
    for k in range(3):
        im=f(k).convert("RGBA"); im.putalpha(alpha); im.save(os.path.join(OUT,f"{name}_{k}.png"))
print("✓ poses/*.png")
