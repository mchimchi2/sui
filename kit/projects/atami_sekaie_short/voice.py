"""台詞の声を作る: script.json → assets/voice/NN.wav + timing.json
OpenJTalk(ローカル・無料)で読み上げ → rubberband で声を高くして赤ちゃんっぽくする。
口パク用に 1/30秒ごとの音量から口の開き(0/1/2)も計算して timing.json に入れる。
※本番で ElevenLabs 等に替える場合は、この段だけ差し替えれば後段はそのまま使える。"""
import json, os, subprocess, numpy as np, pyopenjtalk
from scipy.io import wavfile
HERE=os.path.dirname(os.path.abspath(__file__)); V=os.path.join(HERE,"assets","voice"); os.makedirs(V,exist_ok=True)
PITCH=1.38; TEMPO=1.16; GAP=0.22; LEAD=0.6; FPS=30
lines=json.load(open(os.path.join(HERE,"script.json")))
t=LEAD; out=[]
for i,l in enumerate(lines):
    x,sr=pyopenjtalk.tts(l["voice"], speed=1.0, half_tone=0.0)
    raw=os.path.join(V,f"{i:02d}_raw.wav"); wavfile.write(raw,sr,x.astype(np.int16))
    dst=os.path.join(V,f"{i:02d}.wav")
    subprocess.run(["ffmpeg","-v","error","-y","-i",raw,"-af",
        f"rubberband=pitch={PITCH}:tempo={TEMPO}:formant=preserved,silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
        "afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse,aresample=48000",dst],check=True)
    os.remove(raw)
    sr,y=wavfile.read(dst); y=y.astype(float)/32768; dur=len(y)/sr
    # 口パク: 1フレームごとのRMS → 0/1/2
    hop=sr//FPS; rms=np.array([np.sqrt(np.mean(y[k:k+hop]**2)) for k in range(0,len(y),hop)])
    ref=np.percentile(rms[rms>0],90) if (rms>0).any() else 1
    mouth=[0 if r<ref*0.18 else (1 if r<ref*0.55 else 2) for r in rms]
    out.append({**l,"start":round(t,3),"dur":round(dur,3),"mouth":mouth})
    print(f"{l['id']:6s} {t:6.2f}s +{dur:.2f}s")
    t+=dur+GAP+(0.5 if l["id"] in ("judge",) else 0)
total=round(t+1.2,2)
json.dump({"total":total,"lines":out},open(os.path.join(HERE,"timing.json"),"w"),ensure_ascii=False)
print("total",total)
