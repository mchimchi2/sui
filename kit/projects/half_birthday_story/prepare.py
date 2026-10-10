"""input/half_birthday/ の写真・動画から assets/ を作る
- 写真: 赤ちゃんが中心に来るよう 9:16 に切り抜き、暗い室内なので少し明るく
- 動画: iPhone の HDR(HLG/Dolby Vision)を SDR に変換(HDRのままだと書き出しが遅い・色が転ぶ)"""
import os, subprocess
from PIL import Image, ImageEnhance
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.environ.get("INPUT_DIR", os.path.join(HERE,"..","..","input","half_birthday"))
A=os.path.join(HERE,"assets"); os.makedirs(A,exist_ok=True)
FOCUS={"p01":0.47,"p11":0.58}          # 赤ちゃんの横位置(写真幅に対する割合)。既定 0.5
for i in range(1,14):
    n=f"p{i:02d}"; im=Image.open(os.path.join(SRC,n+".jpg")).convert("RGB")
    w,h=im.size; cw=int(h*9/16); cx=FOCUS.get(n,0.5)*w
    x0=int(min(max(cx-cw/2,0),w-cw)); im=im.crop((x0,0,x0+cw,h)).resize((1080,1920),Image.LANCZOS)
    im=ImageEnhance.Brightness(im).enhance(1.18); im=ImageEnhance.Contrast(im).enhance(1.08); im=ImageEnhance.Color(im).enhance(1.15)
    im.save(os.path.join(A,n+".jpg"),quality=90)
TM="zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920,eq=brightness=0.04:saturation=1.15,fps=30"
subprocess.run(["ffmpeg","-v","error","-y","-i",os.path.join(SRC,"IMG_4727.mov"),"-an","-vf",TM,"-c:v","libx264","-crf","18",
    "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",os.path.join(A,"clip.mp4")],check=True)
print("✓ assets/p01..p13.jpg, clip.mp4")
