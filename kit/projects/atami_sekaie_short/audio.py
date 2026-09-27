"""BGM(オリジナル・128BPM)+効果音+声を1本の音にまとめる → assets/mix.wav (-14 LUFS)
声の区間はBGMを約25%に下げる(ダッキング)。すべて numpy で自作なので著作権フリー。"""
import json, os, subprocess, numpy as np
from scipy.io import wavfile
HERE=os.path.dirname(os.path.abspath(__file__)); A=os.path.join(HERE,"assets")
SR=48000; T=json.load(open(os.path.join(HERE,"timing.json"))); N=int(T["total"]*SR)
BPM=128; B=60/BPM
rng=np.random.default_rng(7)
def env(n,a=0.005,d=0.25):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def tone(f,dur,d=0.25,harm=(1,0.4,0.15)):
    t=np.arange(int(dur*SR))/SR; return sum(h*np.sin(2*np.pi*f*(k+1)*t) for k,h in enumerate(harm))*env(len(t),d=d)
def add(buf,x,t,g=1.0):
    i=int(t*SR); j=min(len(buf),i+len(x));
    if i<len(buf): buf[i:j]+=g*x[:j-i]
note=lambda n:440*2**((n-69)/12)
# ---- BGM: マリンバ風のコード分散+ベース+シェイカー(F→Dm→B♭→C)
bgm=np.zeros(N)
prog=[(65,[65,69,72,76]),(62,[62,65,69,74]),(58,[58,62,65,70]),(60,[60,64,67,72])]
beat=0; t=0
while t<T["total"]:
    root,ch=prog[(beat//8)%4]
    for s in range(2):                        # 8分音符のアルペジオ
        n=ch[(beat*2+s)%4]+12
        add(bgm,tone(note(n),0.4,d=0.12,harm=(1,0.25,0.3)),t+s*B/2,0.16)
    if beat%2==0: add(bgm,tone(note(root-24),0.5,d=0.3,harm=(1,0.5)),t,0.30)
    k=int(0.05*SR); sh=rng.normal(0,1,k)*env(k,a=0.002,d=0.02)
    add(bgm,sh,t+B/2,0.05)
    if beat%4==0:                              # やわらかいキック
        kt=np.arange(int(0.18*SR))/SR; add(bgm,np.sin(2*np.pi*(55+90*np.exp(-kt*30))*kt)*np.exp(-kt*18),t,0.35)
    beat+=1; t+=B
# ---- 声とダッキング
voice=np.zeros(N); duck=np.ones(N)
for i,l in enumerate(T["lines"]):
    sr,y=wavfile.read(os.path.join(A,"voice",f"{i:02d}.wav")); y=y.astype(float)/32768
    add(voice,y,l["start"],1.0)
    a=int((l["start"]-0.08)*SR); b=int((l["start"]+l["dur"]+0.15)*SR); duck[max(0,a):b]=0.28
k=int(0.12*SR); duck=np.convolve(duck,np.ones(k)/k,mode="same")
# ---- 効果音
sfx=np.zeros(N)
pop=lambda:tone(880,0.12,d=0.04,harm=(1,0.3))*np.linspace(1,0.6,int(0.12*SR))
def swoosh(d=0.25):
    n=int(d*SR); x=rng.normal(0,1,n); x=np.convolve(x,np.ones(30)/30,mode="same"); return x*np.sin(np.linspace(0,np.pi,n))*0.6
def impact():
    t=np.arange(int(0.5*SR))/SR; return (np.sin(2*np.pi*(45+120*np.exp(-t*25))*t)*np.exp(-t*7)+0.3*rng.normal(0,1,len(t))*np.exp(-t*30))
def bell():
    return sum(tone(note(n),1.6,d=0.7,harm=(1,0.2,0.1)) for n in (84,88,91))*0.5
def roll(d):
    n=int(d*SR); x=np.zeros(n)
    for i in range(0,n,int(0.045*SR)):
        m=int(0.04*SR); x[i:i+m]+=rng.normal(0,1,min(m,n-i))*env(min(m,n-i),a=0.001,d=0.01)*(0.3+0.7*i/n)
    return x
for l in T["lines"]:
    s=l["start"]
    add(sfx,swoosh(),s-0.2,0.25)
    if l["card"]:
        c=l["card"]["type"]
        if c=="check":
            for j in range(3): add(sfx,pop(),s+0.5+j*0.55,0.5)
        elif c=="warn": add(sfx,impact(),s+1.2,0.9)
        elif c=="stamp":
            add(sfx,roll(1.0),s-0.1,0.5); add(sfx,impact(),s+1.0,0.8); add(sfx,bell(),s+1.0,0.6)
        else: add(sfx,pop(),s+0.3,0.45)
mix=bgm*duck+voice*1.0+sfx*0.6
mix/=np.max(np.abs(mix))*1.05
fade=int(0.8*SR); mix[-fade:]*=np.linspace(1,0,fade)
raw=os.path.join(A,"mix_raw.wav"); wavfile.write(raw,SR,(mix*32767).astype(np.int16))
subprocess.run(["ffmpeg","-v","error","-y","-i",raw,"-af","loudnorm=I=-14:TP=-1.5:LRA=11","-ar","48000","-ac","2",os.path.join(A,"mix.wav")],check=True)
os.remove(raw); print("✓ assets/mix.wav", T["total"],"s")
