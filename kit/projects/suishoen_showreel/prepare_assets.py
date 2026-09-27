"""手元の写真・動画(input/)から assets/ を作る。
使い方: python prepare_assets.py   (INPUT_DIR で素材フォルダを変更可)"""
import os, subprocess, shutil, numpy as np
from PIL import Image, ImageEnhance
HERE=os.path.dirname(os.path.abspath(__file__))
U=os.path.join(os.environ.get("INPUT_DIR", os.path.join(HERE,"../../input")),"")
A=os.path.join(HERE,"assets"); os.makedirs(A,exist_ok=True)
def op(name):
    for ext in (".jpeg",".jpg",".JPG",".JPEG"):
        if os.path.exists(U+name+ext): return Image.open(U+name+ext).convert("RGB")
    raise SystemExit(f"素材が見つかりません: {name}")
def save(im,out,w):
    h=int(im.height*w/im.width); im=im.resize((w,h),Image.LANCZOS)
    ImageEnhance.Color(im).enhance(0.93).save(os.path.join(A,out),quality=88); print("✓",out,im.size)
# name, crop box (None=そのまま), 出力名, 幅   ※人が写り込まない位置でトリミング済み
PHOTOS=[("IMG_0616",None,"forest.jpg",1300),        # 客室からの森
        ("IMG_4492",(0,150,760,1100),"entrance.jpg",1000),  # 料亭 紅葉の玄関(人物を外す)
        ("IMG_4532",(0,0,1250,1000),"dining.jpg",1300),     # 朝食会場の窓(人物を外す)
        ("IMG_0628",(0,0,1932,880),"lounge.jpg",1400),      # ラウンジ(子どもを外す)
        ("IMG_4475",None,"room2.jpg",800),("IMG_4478",None,"room3.jpg",800),
        ("IMG_4479",None,"bath.jpg",800),("IMG_4476",(300,950,1100,1650),"tub.jpg",1100),
        ("IMG_4509",(0,400,1000,1650),"garden.jpg",1100),
        ("IMG_0638",None,"hassun.jpg",1200),
        ("IMG_0643",(150,1050,1932,2576),"sashimi.jpg",1300),   # 人物を外して皿だけ
        ("IMG_4482",None,"onsen.jpg",1000),
        ("IMG_4480",(0,430,1450,2576),"sisley.jpg",900)]
for n,b,o,w in PHOTOS:
    im=op(n); save(im.crop(b) if b else im,o,w)
# 献立: 宿泊者名を消す(周囲の紙色で塗る) → 上のお盆を外してトリミング
try:
    import cv2
    im=cv2.cvtColor(np.asarray(op("IMG_0636")),cv2.COLOR_RGB2BGR)
    m=np.zeros(im.shape[:2],np.uint8); cv2.rectangle(m,(1234,1540),(1290,1602),255,-1)
    im=cv2.inpaint(im,m,9,cv2.INPAINT_TELEA)[1360:,:]
    save(Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)),"menu.jpg",1300)
    print("  ⚠ menu.jpg: 宿泊者名が消えているか必ず目視確認")
except ImportError:
    print("opencv-python が無いので menu.jpg は作りません (pip install opencv-python)")
# フィルムグレイン
rng=np.random.default_rng(2); Image.fromarray((128+rng.normal(0,40,(480,270))).clip(0,255).astype(np.uint8)).save(os.path.join(A,"grain.png"))
# iPhone動画(HDR)→SDRに変換して切り出し。HDRのままだと書き出しが数倍遅くなる
TM="zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:-2,fps=30"
CLIPS=[("IMG_0621.mov",0,3.0,"v_room.mp4"),("IMG_0621.mov",10.0,1.5,"v_bed.mp4"),
       ("IMG_0621.mov",7.3,1.6,"v_bath.mp4"),("IMG_0656.mov",0,1.8,"v_bfast.mp4")]
for src,ss,t,out in CLIPS:
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(t),"-i",U+src,"-an","-vf",TM,"-c:v","libx264","-crf","18",
                    "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",os.path.join(A,out)],check=True); print("✓",out)
print("完了。次に: python music.py && bash build.sh")
