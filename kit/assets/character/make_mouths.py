"""ちび審査員の口パク用差分を作る: chibi_serious.png → mouth_0(閉)/mouth_1(半開)/mouth_2(開).png
元画像の口(へ の字)を肌色で消して、開いた口を描き直す。キャラ画像を差し替えたら MOUTH の座標を要調整。"""
from PIL import Image, ImageDraw
import os
HERE=os.path.dirname(os.path.abspath(__file__))
src=Image.open(os.path.join(HERE,"chibi_serious.png")).convert("RGBA")
SKIN=(253,231,206,255); LINE=(74,52,44,255); INSIDE=(140,52,56,255); TONGUE=(236,128,122,255)
MOUTH=(594,645,658,695)   # 消す範囲 (x0,y0,x1,y1)
cx,cy=626,666
src.save(os.path.join(HERE,"mouth_0.png"))
for k,(w,h) in {1:(15,9),2:(20,17)}.items():
    im=src.copy(); d=ImageDraw.Draw(im)
    d.ellipse(MOUTH,fill=SKIN)
    box=(cx-w,cy-h+2,cx+w,cy+h+2)
    d.ellipse(box,fill=INSIDE,outline=LINE,width=4)
    d.chord((cx-w+6,cy+2,cx+w-6,cy+h+2-1),0,180,fill=TONGUE)
    im.save(os.path.join(HERE,f"mouth_{k}.png"))
print("✓ mouth_0..2.png")
