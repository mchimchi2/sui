# Original BGM (no third-party material). 72 BPM, F major, warm piano + pad, drop before the smile and resolve at 25.05s.
import numpy as np, wave
from scipy.signal import fftconvolve
SR=44100; T=27.85; N=int(SR*T)
out=np.zeros((N,2))
def hz(m): return 440*2**((m-69)/12)
def piano(m,dur=2.5,vel=0.5):
    n=int(SR*dur); t=np.arange(n)/SR; f=hz(m); s=np.zeros(n)
    for k,a in enumerate([1,0.5,0.28,0.15,0.08,0.05],1):
        fk=f*k*np.sqrt(1+0.0004*k*k); s+=a*np.sin(2*np.pi*fk*t)*np.exp(-t*(1.2+0.9*k))
    s*=np.minimum(t/0.004,1)
    return s*vel
def pad(ms,dur,vel=0.08,att=1.2,rel=1.5):
    n=int(SR*dur); t=np.arange(n)/SR; s=np.zeros(n)
    for m in ms:
        for det in (-0.07,0,0.07):
            f=hz(m+det); s+=np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t)
    env=np.minimum(t/att,1)*np.minimum((dur-t)/rel,1).clip(0,1)
    return s*env*vel/len(ms)
def add(sig,t0,pan=0.0):
    i=int(t0*SR); j=min(N,i+len(sig)); 
    if i>=N: return
    s=sig[:j-i]; out[i:j,0]+=s*(1-pan)/1; out[i:j,1]+=s*(1+pan)/1
beat=60/72; e=beat/2
chords=[[53,57,60,64],[50,53,57,60],[46,50,53,57],[48,52,55,60]]  # Fmaj7 Dm7 Bbmaj7 C
rng=np.random.default_rng(3)
t=0.0; ci=0
DROP=23.35; HIT=25.05
while t<DROP-0.01:
    c=chords[ci%4]; root=c[0]-12
    add(pad([root]+c,beat*4+1.5,0.10),t)
    add(piano(root,3.0,0.35),t,-0.2)
    pat=[c[0],c[2],c[3]+12,c[1]+12,c[3]+12,c[1]+12,c[2]+12,c[2]]
    for k,m in enumerate(pat):
        tt=t+k*e
        if tt>=DROP-0.05: break
        if t<2.2 and k<4: continue   # sparse intro
        v=(0.22 if k%2==0 else 0.15)*rng.uniform(0.85,1.1)
        add(piano(m+12 if ci>=4 and k in (2,4) else m,2.0,v),tt+rng.uniform(-0.008,0.008),0.25*(1 if k%2 else -1))
    t+=beat*4; ci+=1
# drop: single suspended note + swell into the hit
add(piano(81,1.7,0.16),DROP,0.1)
sw=pad([65,69,72,76],HIT-DROP+0.05,0.10,att=HIT-DROP,rel=0.05); add(sw,DROP)
# resolution at HIT: Fmaj9 big + bell
for m,v in [(41,0.45),(53,0.35),(57,0.3),(60,0.3),(64,0.28),(67,0.25),(72,0.25)]: add(piano(m,3.0,v),HIT)
bell_t=np.arange(int(SR*2.8))/SR
bell=sum(a*np.sin(2*np.pi*hz(84)*r*bell_t)*np.exp(-bell_t*d) for a,r,d in [(0.25,1,1.5),(0.12,2.76,3),(0.06,5.4,5)])
add(bell,HIT+0.02,0.15)
add(pad([41,53,57,60,67],T-HIT,0.12,att=0.3,rel=1.8),HIT)
# gentle echo arpeggio after hit
for k,m in enumerate([72,76,79,84]): add(piano(m,2.0,0.12),HIT+0.9+k*e,0.3*(-1)**k)
# reverb
ir_t=np.arange(int(SR*2.2))/SR; rng2=np.random.default_rng(7)
ir=np.stack([rng2.normal(0,1,len(ir_t))*np.exp(-ir_t*3.0) for _ in range(2)],1); ir[:int(0.012*SR)]=0
wet=np.stack([fftconvolve(out[:,c],ir[:,c])[:N] for c in range(2)],1)
wet/=np.abs(wet).max()+1e-9; dry=out/(np.abs(out).max()+1e-9)
mix=0.72*dry+0.38*wet
tt=np.arange(N)/SR; mix*=np.minimum(tt/0.6,1)[:,None]*np.clip((T-tt)/1.2,0,1)[:,None]
mix/=np.abs(mix).max(); mix*=0.8
w=wave.open('assets/bgm_raw.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix*32767).astype(np.int16).tobytes()); w.close(); print('ok')
