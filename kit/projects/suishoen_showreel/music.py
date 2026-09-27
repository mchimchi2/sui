import os
# Original track: 120 BPM, D minor pentatonic, koto-like plucks + taiko + bass. Accents on scene hits.
import numpy as np, wave
from scipy.signal import fftconvolve, lfilter
SR=44100; T=30.0; N=int(SR*T); B=0.5
out=np.zeros((N,2)); rng=np.random.default_rng(5)
def hz(m): return 440*2**((m-69)/12)
def put(s,t,g=1.0,pan=0.0):
    i=int(t*SR); j=min(N,i+len(s))
    if i>=N or i<0: return
    out[i:j,0]+=s[:j-i]*g*(1-pan); out[i:j,1]+=s[:j-i]*g*(1+pan)
def kick(d=0.45):
    t=np.arange(int(SR*d))/SR; f=45+110*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)
def taiko(d=0.9):
    t=np.arange(int(SR*d))/SR; f=70+50*np.exp(-t*18)
    s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*4.5)
    n=rng.normal(0,1,len(t))*np.exp(-t*25)*0.3
    return s+lfilter([0.2],[1,-0.8],n)
def hat(d=0.06):
    t=np.arange(int(SR*d))/SR; n=rng.normal(0,1,len(t)); n=np.diff(np.r_[0,n]); return n*np.exp(-t*60)*0.25
def clap():
    t=np.arange(int(SR*0.25))/SR; n=rng.normal(0,1,len(t))
    env=np.exp(-t*22)+0.6*np.exp(-np.maximum(t-0.012,0)*30)*(t>0.012)
    return lfilter([1,-1],[1,-0.3],n)*env*0.35
def koto(m,d=1.2,b=0.996):
    f=hz(m); L=int(SR/f); buf=rng.uniform(-1,1,L); n=int(SR*d); y=np.zeros(n)
    for i in range(n):
        y[i]=buf[i%L]; buf[i%L]=b*0.5*(buf[i%L]+buf[(i+1)%L])
    t=np.arange(n)/SR; return y*np.exp(-t*2.2)*0.5
kc={}
def K(m,d=1.0):
    if (m,d) not in kc: kc[(m,d)]=koto(m,d)
    return kc[(m,d)]
def bass(m,d):
    t=np.arange(int(SR*d))/SR; f=hz(m)
    s=np.sin(2*np.pi*f*t)+0.35*np.sin(2*np.pi*2*f*t)+0.12*np.sin(2*np.pi*3*f*t)
    return s*np.minimum(t/0.01,1)*np.exp(-t*1.8)*0.5
def riser(d):
    t=np.arange(int(SR*d))/SR; n=rng.normal(0,1,len(t))
    y=np.zeros_like(n); a=0.0
    for i in range(len(n)):
        c=0.02+0.5*(t[i]/d)**2; a+=c*(n[i]-a); y[i]=a
    return y*(t/d)**2*0.6
def boom():
    t=np.arange(int(SR*2.5))/SR; f=38+60*np.exp(-t*8)
    s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*1.6)
    n=lfilter([0.05],[1,-0.95],rng.normal(0,1,len(t)))*np.exp(-t*3)
    return (s+n)*0.9
def whoosh(d=0.5):
    t=np.arange(int(SR*d))/SR; n=rng.normal(0,1,len(t)); env=np.sin(np.pi*t/d)**2
    return lfilter([1,-1],[1,-0.6],n)*env*0.12
pent=[62,65,67,69,72,74,77,79,81]   # D F G A C D F G A
riff=[0,2,4,5,4,2,3,1]
roots=[38,38,34,36]  # D D Bb C
beats=int(T/B)
for b in range(beats):
    t=b*B; bar=b//4; inb=b%4
    intro = t<4.0; half = 14.5<=t<18.5; out_ = t>=27.0
    if out_: continue
    # drums
    if not intro:
        if half:
            if inb==0: put(kick(),t,0.9)
            if inb==2: put(taiko(),t,0.6,-0.2)
        else:
            put(kick(),t,0.95)
            if inb in (1,3): put(clap(),t,0.8,0.1)
            for k in range(2): put(hat(),t+k*B/2,0.5 if k else 0.3,0.3)
    else:
        if inb==0 and t>=1.0: put(taiko(),t,0.7,-0.1)
    # bass
    if not intro:
        put(bass(roots[bar%4],B*0.95),t,0.8 if not half else 0.5)
    # koto riff 8ths
    for k in range(2):
        tt=t+k*B/2; idx=riff[(b*2+k)%8]+(2 if bar%4==2 else 0)
        if intro and tt<0.9: continue
        g=0.45 if not half else 0.35
        put(K(pent[min(idx,8)],1.0),tt+rng.uniform(-0.005,0.005),g,0.35*(1 if k else -1))
# fills / accents at hits
for th in (2.5,):
    put(whoosh(0.6),th-0.45,1.0)
put(riser(1.5),2.5,0.7); put(boom(),4.0,1.0)
for th in (10.0,20.0):
    put(riser(1.0),th-1.0,0.6); put(boom(),th,0.85); put(taiko(),th,0.8)
for th in (5.6,): put(taiko(),th,0.9); put(taiko(),th+0.12,0.6)
for th in (7.0,): put(whoosh(0.5),th-0.1,1.2)
for k in range(6): put(hat(0.04),18.5+k*0.25,0.9); put(kick(0.2),18.5+k*0.25,0.6)
for th in (8.5,8.875,9.25,9.625): pass
put(riser(2.0),25.0,0.7)
put(boom(),27.0,1.1); put(taiko(),27.0,1.0)
for i,m in enumerate([74,77,81,86]): put(K(m,2.5),27.0+i*0.09,0.5,0.3*(-1)**i)
put(K(50,2.5),27.0,0.6)
# gong-ish shimmer
t=np.arange(int(SR*3))/SR; g=sum(a*np.sin(2*np.pi*hz(74)*r*t)*np.exp(-t*dd) for a,r,dd in [(0.2,1,1.2),(0.1,2.4,2),(0.05,3.9,3)])
put(g,27.0,0.6)
# reverb
ir_t=np.arange(int(SR*1.6))/SR; ir=np.stack([rng.normal(0,1,len(ir_t))*np.exp(-ir_t*4) for _ in range(2)],1); ir[:500]=0
wet=np.stack([fftconvolve(out[:,c],ir[:,c])[:N] for c in range(2)],1)
mix=out/np.abs(out).max()*0.85+wet/np.abs(wet).max()*0.25
tt=np.arange(N)/SR; mix*=np.clip((T-tt)/0.8,0,1)[:,None]
mix=np.tanh(mix*1.3); mix/=np.abs(mix).max(); mix*=0.9
os.makedirs("assets",exist_ok=True); w=wave.open("assets/music_raw.wav","wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix*32767).astype(np.int16).tobytes()); w.close(); print('ok')
