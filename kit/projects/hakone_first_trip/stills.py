from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
import os, glob, json
U=os.path.join(os.environ.get('INPUT_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../input')),'')
def _font(cands):
    for c in cands:
        if os.path.exists(c): return c
    raise SystemExit('日本語明朝フォントが見つかりません。FONT_JP / FONT_LT 環境変数で .ttc/.otf のパスを指定してください')
W,H=1080,1920; IW,IH=1080,1350; IY=210
JP=os.environ.get('FONT_JP') or _font(['/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc','/System/Library/Fonts/ヒラギノ明朝 ProN.ttc','/Library/Fonts/NotoSerifJP-Regular.otf'])
LT=os.environ.get('FONT_LT') or _font(['/usr/share/fonts/opentype/noto/NotoSerifCJK-Light.ttc','/System/Library/Fonts/ヒラギノ明朝 ProN.ttc','/Library/Fonts/NotoSerifJP-Light.otf'])
scenes=[
 ('IMG_4519',(381,116,1834,1932),'AUTUMN · 2026','はじめての、旅。','her first trip'),
 ('IMG_4541',(313,200,1813,2075),'DAY 1 — 10:24','ちょっとだけ、ねむい。','on the way'),
 ('IMG_4489',(300,680,1200,1805),'DAY 1 — 21:00','ふかふかの、夜。','check-in'),
 ('IMG_0652',(634,432,1834,1932),'DAY 2 — 07:30','朝ごはんは、まだ様子見。','breakfast'),
 ('IMG_4532',(175,500,1425,2062),'DAY 2 — 07:42','…気に入ったらしい。','approved'),
 ('IMG_4517',(300,20,1932,2060),'FIN.','ぜんぶ、たのしかった。','see you next trip'),
]
def fix_shadow(im):
    a=np.asarray(im).astype(np.float32)
    x0,y0,x1,y1=600,2020,1110,2480
    reg=a[y0:y1,x0:x1]
    lum=reg.mean(axis=2)
    from PIL import Image as I
    bl=np.asarray(I.fromarray(lum.astype(np.uint8)).filter(ImageFilter.GaussianBlur(40))).astype(np.float32)
    ref=np.percentile(lum,90)
    gain=np.clip(ref/np.maximum(bl,1),1,3)[...,None]
    a[y0:y1,x0:x1]=np.clip(reg*gain,0,255)
    return I.fromarray(a.astype(np.uint8))
def grade(im):
    a=np.asarray(im).astype(np.float32)/255
    a=0.04+0.94*a  # lifted blacks
    a[...,0]*=1.03; a[...,2]*=0.95
    im=Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8))
    im=ImageEnhance.Color(im).enhance(0.88)
    return im
def load(name,box):
    im=Image.open(U+name+'.jpeg') if os.path.exists(U+name+'.jpeg') else Image.open(U+name+'.JPG').convert('RGB')

    import blur; im=blur.apply(name,im)
    im=im.crop(box).resize((IW,IH),Image.LANCZOS)
    return grade(im)
def vignette(im):
    y,x=np.mgrid[0:IH,0:IW]; d=np.sqrt(((x-IW/2)/(IW/2))**2+((y-IH/2)/(IH/2))**2)
    m=np.clip(1-0.35*np.clip(d-0.5,0,1)**1.5,0,1)[...,None]
    return Image.fromarray((np.asarray(im)*m).astype(np.uint8))
def spaced(d,xy,t,f,fill,sp=6):
    tw=sum(d.textlength(c,font=f)+sp for c in t)-sp
    x=xy[0]-tw/2
    for c in t:
        d.text((x,xy[1]),c,font=f,fill=fill); x+=d.textlength(c,font=f)+sp
def frame(img,top,title,sub,alpha=1.0):
    c=Image.new('RGB',(W,H),(8,8,8)); c.paste(img,(0,IY))
    d=ImageDraw.Draw(c)
    col=lambda v:tuple(int(8+(v-8)*alpha) for _ in range(3))
    spaced(d,(W/2,120),top,ImageFont.truetype(LT,30),col(200),8)
    f=ImageFont.truetype(JP,58); tw=d.textlength(title,font=f)
    d.text(((W-tw)/2,1620),title,font=f,fill=col(240))
    spaced(d,(W/2,1725),sub,ImageFont.truetype(LT,26),col(150),5)
    return c
if __name__=='__main__':
    scenes=[(d['file'],tuple(d['crop']),d['top'],d['title'],d['sub']) for d in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'scenes.json')))]
    ims=[]
    for i,(n,b,t,ti,s) in enumerate(scenes):
        fr=frame(vignette(load(n,b)),t,ti,s); fr.save(f'still{i+1}.png'); ims.append(fr)
    rows=(len(ims)+2)//3
    sh=Image.new('RGB',(3*370+10,rows*650+10),(30,30,30))
    for i,fr in enumerate(ims):
        sh.paste(fr.resize((360,640)),(10+(i%3)*370,10+(i//3)*650))
    sh.save('sheet.png')
