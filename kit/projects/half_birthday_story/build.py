"""ハーフバースデーのストーリー動画(1080×1920・約23秒)の index.html を作る。拍は music.py と同じ 128BPM。"""
import os
HERE=os.path.dirname(os.path.abspath(__file__))
B=60/128; BAR=4*B; DROP=4*BAR; STOP=8*BAR; CHILL=9*BAR; END_CARD=10*BAR; TOTAL=round(12*BAR+0.6,3)
f=lambda x:f"{x:.3f}"
b=[]; j=[]
# ---------- 映像の層
b.append(f'<video id="vid" class="clip" src="assets/clip.mp4" data-start="0" data-duration="{f(DROP+0.05)}" data-media-start="0" data-track-index="0" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover"></video>')
# ドロップの写真(拍数)とテロップ
CUTS=[("p01",2,"drop"),("p02",2,"VIBES ↑↑"),("p03",1,None),("p04",2,"サングラス<br>似合いすぎ😎"),("p05",2,"…ずれてますけど"),
      ("p06",1,"上げてこ↑↑"),("p07",1,"上げてこ↑↑"),("p09",1,None),("p10",1,None),("p08",1,None),("p12",2,"フロア<br>最高潮🔥")]
assert sum(c[1] for c in CUTS)==16
SHOTS=[]; t=DROP
for n,beats,cap in CUTS: SHOTS.append((n,t,beats*B,cap)); t+=beats*B
SHOTS+= [("p11",STOP,CHILL-STOP,None),("p13",CHILL,END_CARD-CHILL,None),("p08",END_CARD,TOTAL-END_CARD,None)]
for k,(n,t0,d,cap) in enumerate(SHOTS):
    b.append(f'<div id="s{k}" class="shot" style="opacity:0"><div id="s{k}i" class="ph" style="background-image:url(assets/{n}.jpg)"></div></div>')
    j.append(f'tl.set("#s{k}",{{opacity:1}},{f(t0)});')
    if k+1<len(SHOTS): j.append(f'tl.set("#s{k}",{{opacity:0}},{f(t0+d)});')
    if t0<STOP:   # ドロップ: カットごとに寄りから戻す(転換効果は使わない)
        org=["50% 62%","45% 60%","55% 64%"][k%3]
        j.append(f'tl.fromTo("#s{k}i",{{scale:1.16,transformOrigin:"{org}"}},{{scale:1.0,duration:0.32,ease:"power3.out"}},{f(t0)});')
    else:         # 後半: ゆっくり寄る
        j.append(f'tl.fromTo("#s{k}i",{{scale:1.0,transformOrigin:"50% 62%"}},{{scale:1.08,duration:{f(d)},ease:"none"}},{f(t0)});')
# ---------- クラブ照明(回る光線+拍ごとのネオン明滅)
b.append('<div id="beams" class="abs" style="left:-660px;top:-1100px;width:2400px;height:2400px;border-radius:50%;mix-blend-mode:screen;opacity:0.55;'
         'background:repeating-conic-gradient(from 0deg, rgba(255,60,170,0.0) 0deg 10deg, rgba(255,60,170,0.35) 12deg 14deg, rgba(0,0,0,0) 16deg 30deg, rgba(60,220,255,0.3) 32deg 34deg, rgba(0,0,0,0) 36deg 45deg)"></div>')
b.append('<div id="tintA" class="abs tint" style="background:radial-gradient(circle at 50% 30%,rgba(255,40,160,0.55),rgba(255,40,160,0) 70%)"></div>')
b.append('<div id="tintB" class="abs tint" style="background:radial-gradient(circle at 50% 30%,rgba(40,200,255,0.5),rgba(40,200,255,0) 70%)"></div>')
b.append('<div class="abs" style="inset:0;background:linear-gradient(to bottom,rgba(0,0,0,0.45) 0%,rgba(0,0,0,0) 28%,rgba(0,0,0,0) 70%,rgba(0,0,0,0.35) 100%)"></div>')
j.append(f'tl.fromTo("#beams",{{rotation:0}},{{rotation:120,duration:{f(STOP)},ease:"none"}},0);')
j.append(f'tl.set("#beams",{{opacity:0}},{f(STOP)});')   # 泣いた瞬間に照明オフ
j.append(f'tl.set("#beams",{{opacity:0.25}},{f(CHILL)});tl.to("#beams",{{rotation:150,duration:{f(TOTAL-CHILL)},ease:"none"}},{f(CHILL)});')
for k in range(int(STOP/B)):
    t=k*B
    if t<BAR*2 and k%2: continue                 # イントロは控えめ
    tid="#tintA" if k%2==0 else "#tintB"; pk=0.75 if t>=DROP else 0.4
    j.append(f'tl.set("{tid}",{{opacity:{pk}}},{f(t)});tl.to("{tid}",{{opacity:0,duration:{f(B*0.8)},ease:"power2.out"}},{f(t+0.001)});')
# ドロップの瞬間だけピンクの閃光(1回だけ・強すぎない)
b.append('<div id="flash" class="abs" style="inset:0;background:#ffd6f0;opacity:0;z-index:40"></div>')
j.append(f'tl.set("#flash",{{opacity:0.7}},{f(DROP)});tl.to("#flash",{{opacity:0,duration:0.35,ease:"power2.out"}},{f(DROP+0.001)});')
# ---------- テロップ
def text(tid,html,t0,t1,cls="neon",top=360,anim="pop"):
    b.append(f'<div id="{tid}" class="abs txt {cls}" style="top:{top}px;opacity:0">{html}</div>')
    if anim=="pop": j.append(f'tl.fromTo("#{tid}",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:0.18,ease:"power4.out"}},{f(t0)});')
    else: j.append(f'tl.fromTo("#{tid}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.3,ease:"power3.out"}},{f(t0)});')
    j.append(f'tl.set("#{tid}",{{opacity:0}},{f(t1)});')
b.append('<div id="tag" class="abs tag">HALF BIRTHDAY PARTY 🪩</div>')
j.append(f'tl.set("#tag",{{opacity:0}},{f(STOP)});tl.set("#tag",{{opacity:1}},{f(END_CARD)});')
text("t1a",'<div class="s">シャンパンタワー…</div>',0.15,2*B*2)
text("t1b",'<div class="s">じゃなくて</div><div class="l">ミルク缶タワー🍼</div>',2*B,BAR)
text("t2",'<div class="s">生後6ヶ月</div><div class="l">クラブデビュー🪩</div>',BAR,2*BAR)
text("t3",'<div class="s">本日の主役、</div><div class="l">入場です👑</div>',2*BAR,DROP-3*B)
for i,c in enumerate("321"):
    text(f"cd{i}",f'<div class="cd">{c}</div>',DROP-3*B+i*B,DROP-3*B+(i+1)*B,top=430)
text("hb",'<div class="hb">HAPPY<br>HALF<br>BIRTHDAY</div>',DROP,DROP+2*B,top=330)
for k,(n,t0,d,cap) in enumerate(SHOTS):
    if cap and cap!="drop" and t0<STOP:
        if k>0 and SHOTS[k-1][3]==cap: continue
        d2=d+(SHOTS[k+1][2] if k+1<len(SHOTS) and SHOTS[k+1][3]==cap else 0)
        text(f"c{k}",f'<div class="l">{cap}</div>',t0,t0+d2)
text("cry1",'<div class="s">…からの</div>',STOP+0.05,CHILL,cls="plain",anim="up")
text("cry2",'<div class="xl">ギャン泣き😭</div>',STOP+0.6,CHILL,cls="plain",top=470)
text("cry3",'<div class="s">パリピ、限界でした</div>',STOP+1.1,CHILL,cls="plain",top=700,anim="up")
for k in range(6):
    a=18*(1-k/6)*(1 if k%2 else -1); j.append(f'tl.to("#shake",{{x:{a:.1f},duration:0.04}},{f(STOP+0.6+k*0.045)});')
j.append(f'tl.to("#shake",{{x:0,duration:0.04}},{f(STOP+0.6+6*0.045)});')
text("bye",'<div class="s">今日はもう、</div><div class="l">帰りまーす👋</div>',CHILL+0.2,END_CARD,cls="plain",anim="up")
text("end1",'<div class="hb2">HAPPY HALF<br>BIRTHDAY</div><div class="s">🎂 祝 生後6ヶ月 🎂</div>',END_CARD,TOTAL+1,top=300,anim="up")
text("end2",'<div class="ask">パリピ度、何点?👇</div>',END_CARD+0.8,TOTAL+1,cls="plain",top=640,anim="up")
CSS=open(os.path.join(HERE,"style.css")).read()
open(os.path.join(HERE,"index.html"),"w").write(f'''<!doctype html>
<html lang="ja" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
{CSS}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
<div id="shake" class="abs" style="inset:0">
{chr(10).join(b)}
</div>
<div id="fade" class="abs" style="inset:0;background:#000;opacity:0;z-index:99"></div>
<audio id="music" class="clip" src="assets/music.wav" data-start="0" data-duration="{TOTAL}" data-volume="1" data-track-index="2"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.set(".tint",{{opacity:0}},0);
{chr(10).join(j)}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>''')
print("✓ index.html", TOTAL, "s")
