"""HyperFrames版(hyperframes_index.html)用の素材を作る: assets/s00..s16.jpg, grain.png, bgm.wav"""
import os, json, subprocess, numpy as np
from PIL import Image
import stills as S, blur
HERE=os.path.dirname(os.path.abspath(__file__)); A=os.path.join(HERE,"assets"); os.makedirs(A,exist_ok=True)
for i,d in enumerate(json.load(open(os.path.join(HERE,"scenes.json")))):
    im=Image.open(S.U+d["file"]+".jpeg").convert("RGB"); im=blur.apply(d["file"],im)   # 大人の顔ぼかし
    S.grade(im.crop(tuple(d["crop"])).resize((1404,1755),Image.LANCZOS)).save(os.path.join(A,f"s{i:02d}.jpg"),quality=90)
rng=np.random.default_rng(2); Image.fromarray((128+rng.normal(0,40,(480,270))).clip(0,255).astype(np.uint8)).save(os.path.join(A,"grain.png"))
os.chdir(HERE); subprocess.run(["python3","make_bgm.py"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","assets/bgm_raw.wav","-af","loudnorm=I=-14:TP=-1.5","-ar","44100","assets/bgm.wav"],check=True)
print("完了")
