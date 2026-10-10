"""パリピ風オリジナルBGM(128BPM・numpyで自作=著作権フリー)→ assets/music.wav (-14 LUFS)
構成(拍=0.469秒/小節=1.875秒): イントロ2小節 → ビルドアップ2小節 → ドロップ4小節 → レコード停止 → 静寂1小節 → チル3小節"""
import os, subprocess, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
HERE=os.path.dirname(os.path.abspath(__file__)); SR=48000
BPM=128; B=60/BPM; BAR=4*B
SEC=dict(intro=0, build=2*BAR, drop=4*BAR, stop=8*BAR, chill=9*BAR, end=12*BAR+0.6)
N=int(SEC["end"]*SR); rng=np.random.default_rng(5)
L=np.zeros(N); R=np.zeros(N)
def add(x,t,g=1.0,pan=0.0):
    i=int(t*SR); j=min(N,i+len(x))
    if i>=N or j<=i: return
    L[i:j]+=g*(1-max(pan,0))*x[:j-i]; R[i:j]+=g*(1+min(pan,0))*x[:j-i]
def tt(d): return np.arange(int(d*SR))/SR
def lp(x,f): return sosfilt(butter(2,f,'low',fs=SR,output='sos'),x)
def hp(x,f): return sosfilt(butter(2,f,'high',fs=SR,output='sos'),x)
note=lambda n:440*2**((n-69)/12)
def saw(f,d,det=0.0):
    t=tt(d); return 2*((t*f*(1+det))%1)-1
def supersaw(f,d):
    return sum(saw(f,d,dt) for dt in (-0.012,-0.006,0,0.006,0.012))/5
def kick():
    t=tt(0.35); return np.sin(2*np.pi*(48*t+ (150/30)*(1-np.exp(-t*30))))*np.exp(-t*9)
def clap():
    t=tt(0.18); x=hp(rng.normal(0,1,len(t)),900)*np.exp(-t*22); return x
def hat(d=0.05):
    t=tt(d); return hp(rng.normal(0,1,len(t)),7000)*np.exp(-t*(60 if d<0.1 else 14))
def snare():
    t=tt(0.16); return (0.6*hp(rng.normal(0,1,len(t)),1500)+0.4*np.sin(2*np.pi*190*t))*np.exp(-t*25)
PROG=[(57,[57,60,64]),(53,[53,57,60]),(48,[48,52,55]),(55,[55,59,62])]   # Am F C G
def chord_at(bar): return PROG[bar%4]
# ---------- イントロ(こもった4つ打ち)+ビルド
intro=np.zeros(N)
for k in range(int(SEC["drop"]/B)):
    t=k*B; add(kick(),t,0.55 if t<SEC["build"] else 0.8)
    root,ch=chord_at(int(t/BAR))
    if k%2==1: add(hat(),t,0.12)
    add(lp(supersaw(note(root-12),B*0.9),900)*np.exp(-tt(B*0.9)*3),t+B/2,0.25)
# ビルド: スネアロール(だんだん細かく)+ノイズの上昇
t=SEC["build"]
while t<SEC["drop"]-0.02:
    p=(t-SEC["build"])/(SEC["drop"]-SEC["build"])
    add(snare(),t,0.25+0.45*p); t+=B/2 if p<0.5 else (B/4 if p<0.85 else B/8)
d=SEC["drop"]-SEC["build"]; nz=rng.normal(0,1,int(d*SR)); env=np.linspace(0,1,len(nz))**2
riser=np.concatenate([hp(nz[i:i+4800],400+6000*(i/len(nz))) for i in range(0,len(nz),4800)])[:len(nz)]*env
add(riser,SEC["build"],0.35)
add(supersaw(note(81),d)*np.linspace(0,0.4,int(d*SR))*np.sin(2*np.pi*np.linspace(0,d*8,int(d*SR)))**2,SEC["build"],0.25)
# ---------- ドロップ
crash=hp(rng.normal(0,1,int(1.6*SR)),3000)*np.exp(-tt(1.6)*2.5)
add(crash,SEC["drop"],0.5); add(np.sin(2*np.pi*40*tt(1.0))*np.exp(-tt(1.0)*3),SEC["drop"],0.9)
lead=[69,72,76,72, 69,72,77,72, 67,72,76,72, 67,71,74,71]
for k in range(int((SEC["stop"]-SEC["drop"])/B)):
    t=SEC["drop"]+k*B; bar=int((t-SEC["drop"])/BAR); root,ch=chord_at(bar)
    add(kick(),t,1.0); 
    if k%2==1: add(clap(),t,0.45)
    add(hat(),t+B/2,0.18,pan=0.3); add(hat(0.03),t+B/4,0.08,pan=-0.3); add(hat(0.03),t+3*B/4,0.08,pan=-0.3)
    bass=lp(saw(note(root-24),B*0.45),500)*np.exp(-tt(B*0.45)*4); add(bass,t+B/2,0.55)
    stab=sum(lp(supersaw(note(n),B*0.4),3500) for n in ch+[ch[0]+12])/4*np.exp(-tt(B*0.4)*5)
    add(stab,t+B/2,0.42,pan=0.15); add(stab,t+B/2+0.012,0.3,pan=-0.15)
    for s in range(2):   # 8分のプラック
        n=lead[(k*2+s)%16]+ (0 if bar<2 else 12 if k%8>5 else 0)
        pl=lp(supersaw(note(n),B*0.4),5000)*np.exp(-tt(B*0.4)*9); add(pl,t+s*B/2,0.22)
# サイドチェイン風: キックのたびに全体を一瞬下げる(ドロップ区間)
duck=np.ones(N)
for k in range(int(SEC["stop"]/B)):
    i=int(k*B*SR); m=int(0.18*SR); duck[i:i+m]=np.minimum(duck[i:i+m],0.45+0.55*np.linspace(0,1,m)**0.6)
L*=duck; R*=duck
# ---------- レコード停止(テープストップ)
a=int((SEC["stop"]-0.45)*SR); b=int(SEC["stop"]*SR)
for ch in (L,R):
    seg=ch[a:b].copy(); n=len(seg); pos=np.cumsum(np.linspace(1,0.05,int(n*1.6)))[:]
    pos=pos[pos<n-1]; st=np.interp(pos,np.arange(n),seg)*np.linspace(1,0,len(pos))
    ch[a:]=0; ch[a:a+len(st)]=st
# ---------- チル(ローファイ: こもったキック+やわらかい和音)
for k in range(int((SEC["end"]-SEC["chill"])/B)):
    t=SEC["chill"]+k*B; bar=int((t-SEC["chill"])/BAR); root,ch=chord_at(bar)
    if k%2==0: add(lp(kick(),300),t,0.6)
    if k%2==1: add(lp(snare(),2500),t,0.25)
    if k%4==0:
        pad=sum(lp(supersaw(note(n),BAR),1200) for n in ch)/3*np.minimum(1,tt(BAR)*6)*np.exp(-tt(BAR)*0.8); add(pad,t,0.45)
    add(lp(hat(0.04),5000),t+B/2,0.07)
d0=int(SEC['drop']*SR); b0=int(SEC['build']*SR); L[b0:d0]*=0.78; R[b0:d0]*=0.78   # ドロップが一番大きく聞こえるように
mix=np.stack([L,R],1); mix/=np.max(np.abs(mix))*1.05
f=int(0.6*SR); mix[-f:]*=np.linspace(1,0,f)[:,None]
raw=os.path.join(HERE,"assets","music_raw.wav"); wavfile.write(raw,SR,(mix*32767).astype(np.int16))
# 全体の音量だけを -14 LUFS に合わせる(曲の抑揚=ドロップの大きさは保つ)。ピークはリミッターで抑える
import re
r=subprocess.run(["ffmpeg","-hide_banner","-i",raw,"-af","ebur128","-f","null","-"],capture_output=True,text=True)
I=float(re.findall(r"I:\s+(-?[\d.]+) LUFS",r.stderr)[-1]); gain=-14.0-I+0.6   # リミッターで削れる分を少し上乗せ
subprocess.run(["ffmpeg","-v","error","-y","-i",raw,"-af",f"volume={gain:.2f}dB,alimiter=limit=0.84:attack=3:release=60:level=disabled","-ar","48000",os.path.join(HERE,"assets","music.wav")],check=True)
os.remove(raw); print("✓ assets/music.wav", round(SEC["end"],2),"s", {k:round(v,3) for k,v in SEC.items()})
