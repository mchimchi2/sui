"""timing.json → index.html (HyperFrames)。台詞・口パク・カード・テロップをすべて声の時刻に合わせて配置する。"""
import json, os, math, random, shutil
HERE=os.path.dirname(os.path.abspath(__file__)); T=json.load(open(os.path.join(HERE,"timing.json")))
TOTAL=T["total"]; L=T["lines"]; FPS=30
CH=os.path.join(HERE,"..","..","assets","character","poses"); AD=os.path.join(HERE,"assets","ch"); os.makedirs(AD,exist_ok=True)
for f in os.listdir(CH): shutil.copy(os.path.join(CH,f),AD)
POSES=["serious","smile","shock"]
b=[]; j=[]
def T3(x): return f"{x:.3f}"
# ---------- 背景: ゆっくり回る集中線
b.append('''<div id="bg" class="abs" style="inset:0;background:#15324a"></div>
<div id="rays" class="abs" style="left:-660px;top:-240px;width:2400px;height:2400px;border-radius:50%;
 background:repeating-conic-gradient(from 0deg, rgba(255,255,255,0.07) 0deg 6deg, rgba(255,255,255,0) 6deg 15deg);transform-origin:50% 50%"></div>
<div class="abs" style="inset:0;background:radial-gradient(circle at 50% 42%, rgba(0,0,0,0) 35%, rgba(5,15,28,0.55) 100%)"></div>''')
j.append(f'tl.fromTo("#rays",{{rotation:0}},{{rotation:40,duration:{TOTAL},ease:"none"}},0);')
# ---------- キャラクター(表情3種×口3段)
imgs=''.join(f'<img id="c_{p}_{k}" class="cimg" src="assets/ch/{p}_{k}.png" alt="">' for p in POSES for k in range(3))
b.append(f'<div id="chwrap" class="abs" style="left:90px;top:1030px;width:900px;height:900px;transform-origin:50% 42%"><div id="ch" class="abs" style="inset:0">{imgs}</div></div>')
state=None
def show(pose,k,t):
    global state
    if state==(pose,k): return
    j.append(f'tl.set(".cimg",{{opacity:0}},{T3(t)});tl.set("#c_{pose}_{k}",{{opacity:1}},{T3(t)});'); state=(pose,k)
show(L[0]["pose"],0,0)
j.append('tl.set("#ch",{y:0,scaleY:1},0);tl.set("#chwrap",{scale:1,y:0},0);')
for i,l in enumerate(L):
    s=l["start"]
    for f,m in enumerate(l["mouth"]): show(l["pose"],m,s+f/FPS)
    show(l["pose"],0,s+len(l["mouth"])/FPS)
    # 寄り/引き(転換効果は使わずカットで切り替え)。長い台詞は途中でもう1回切り替えて約1.5秒ごとに画を変える
    shots=[l["shot"]]; 
    if l["dur"]>2.6: shots.append("wide" if l["shot"]=="close" else "close")
    for n,sh in enumerate(shots):
        t=s-0.05+n*l["dur"]/len(shots)
        sc,y=(1.4,110) if sh=="close" else (1.0,0)
        j.append(f'tl.set("#chwrap",{{scale:{sc},y:{y}}},{T3(t)});')
    # 話し始めにぴょこっと跳ねる
    j.append(f'tl.fromTo("#ch",{{y:0,scaleY:1}},{{y:-36,scaleY:1.03,duration:0.12,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{T3(s)});')
# ---------- テロップ(袋文字)
for i,l in enumerate(L):
    rows=l["telop"].split("\n")
    html="".join(f'<div class="tl{" hl" if n==len(rows)-1 and len(rows)>1 else ""}">{r}</div>' for n,r in enumerate(rows))
    b.append(f'<div id="tp{i}" class="abs telop" style="opacity:0">{html}</div>')
    end=L[i+1]["start"]-0.02 if i+1<len(L) else TOTAL
    j.append(f'tl.fromTo("#tp{i}",{{opacity:0,scale:0.82}},{{opacity:1,scale:1,duration:0.22,ease:"back.out(2.2)"}},{T3(l["start"]-0.04)});')
    j.append(f'tl.set("#tp{i}",{{opacity:0}},{T3(end)});')
# ---------- カード(上半分)
def card(i,l):
    c=l["card"]; s=l["start"]; end=L[i+1]["start"]-0.02 if i+1<len(L) else TOTAL; cid=f"cd{i}"
    if c is None:
        return
    ty=c["type"]
    if ty=="title":
        h='''<div class="ep">ちび審査員が行く</div><div class="ep-n">#01</div><div class="ep-t">熱海<br>ATAMI せかいえ</div>'''
    elif ty=="big":
        h=f'''<div class="lbl">ACCESS</div>
        <div class="route"><span class="dot"></span><span class="bar"><span id="{cid}_run" class="run"></span></span><span class="dot o"></span></div>
        <div class="route-n"><span>東京駅</span><span>熱海</span></div>
        <div class="big"><span class="num">{c["big"]}</span><span class="unit">{c["unit"]}</span></div>'''
        j.append(f'tl.fromTo("#{cid}_run",{{scaleX:0}},{{scaleX:1,duration:1.0,ease:"expo.out"}},{T3(s+0.3)});')
    elif ty=="sea":
        h=f'''<div class="sea"><div class="sun"></div><div class="glint"></div><div class="tub"></div>
        <div class="badge">全室 露天風呂付き</div><div class="img-note">イメージ</div></div>'''
        j.append(f'tl.fromTo("#{cid} .sun",{{y:40}},{{y:-10,duration:{l["dur"]+0.4},ease:"none"}},{T3(s)});')
    elif ty=="vert":
        h=f'''<div class="steam"><i></i><i></i><i></i></div><div class="vt">源泉<br>かけ流し</div>
        <div class="vsub">鎌倉時代から続く<br>伊豆山温泉</div>'''
        j.append(f'tl.fromTo("#{cid} .steam i",{{y:40,opacity:0}},{{y:-60,opacity:0.8,duration:1.6,stagger:0.3,ease:"none"}},{T3(s)});')
    elif ty=="check":
        rows=''.join(f'<div class="row" id="{cid}_r{n}"><span class="ok">✓</span>{it}</div>' for n,it in enumerate(c["items"]))
        h=f'<div class="lbl">KIDS CHECK</div><div class="panel">{rows}</div>'
        for n in range(len(c["items"])):
            j.append(f'tl.fromTo("#{cid}_r{n}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.25,ease:"back.out(2)"}},{T3(s+0.5+n*0.55)});')
    elif ty=="warn":
        h=f'''<div class="warn-tag">⚠ 予約前に要チェック</div>
        <div class="warn-big" id="{cid}_big">{c["big"]}<span>以上</span></div><div class="warn-sub">{c["sub"]}</div>'''
        j.append(f'tl.fromTo("#{cid}_big",{{scale:3,opacity:0}},{{scale:1,opacity:1,duration:0.18,ease:"power4.in"}},{T3(s+1.02)});')
        for k in range(6):
            a=22*(1-k/6)*(1 if k%2 else -1); j.append(f'tl.to("#shake",{{x:{a:.1f},y:{-a*0.5:.1f},duration:0.03}},{T3(s+1.2+k*0.04)});')
        j.append(f'tl.to("#shake",{{x:0,y:0,duration:0.03}},{T3(s+1.45)});')
        j.append(f'tl.set("#bg",{{background:"#3a2a12"}},{T3(s+1.2)});tl.set("#bg",{{background:"#15324a"}},{T3(end)});')
    elif ty=="rooms":
        tiles=''.join(f'<div class="tile" id="{cid}_t{n}">{it.split(" ")[0]}<b>{it.split(" ")[1]}</b></div>' for n,it in enumerate(c["items"]))
        h=f'<div class="lbl">BABY-FRIENDLY</div><div class="rooms-h">〈せかいえ棟〉</div><div class="tiles">{tiles}</div>'
        for n in range(len(c["items"])):
            j.append(f'tl.fromTo("#{cid}_t{n}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{T3(s+0.4+n*0.25)});')
    elif ty=="stamp":
        random.seed(3)
        conf=''.join(f'<i class="cf" style="left:{random.randint(0,1060)}px;background:{random.choice(["#ffd84a","#ff7a59","#7fd1ff","#ffffff","#9be7a6"])};width:{random.randint(14,24)}px;height:{random.randint(24,40)}px"></i>' for _ in range(46))
        h=f'<div class="stamp" id="{cid}_st"><b>合格</b><span>行きたい!</span></div>'
        b.append(f'<div id="conf" class="abs" style="left:0;top:0;width:1080px;height:1920px;z-index:40;pointer-events:none">{conf}</div>')
        j.append(f'tl.fromTo("#{cid}_st",{{scale:3.2,opacity:0,rotation:-30}},{{scale:1,opacity:1,rotation:-10,duration:0.2,ease:"power4.in"}},{T3(s+0.82)});')
        j.append(f'tl.set("#bg",{{background:"#6b3a2a"}},{T3(s+1.0)});')
        for n in range(46):   # 紙吹雪の落ち方は Python 側で乱数を固定して決める(描画を毎回同じにする)
            j.append(f'tl.fromTo("#conf .cf:nth-child({n+1})",{{y:-80,rotation:0,x:0}},{{y:{random.randint(1900,2250)},rotation:{random.randint(-360,360)},x:{random.randint(-100,100)},duration:2.6,ease:"power1.in"}},{T3(s+1.0+n*0.02)});')
    elif ty=="cta":
        h=f'''<div class="cta-b">🔖</div><div class="cta">子連れ宿を<br>毎週審査中</div><div class="cta-a">@chibi.shinsain</div>
        <div class="src">ATAMI せかいえ｜静岡県熱海市伊豆山<br>※当アカウントは未宿泊。公式サイト・予約サイトの情報(2026年9月時点)より<br>※料金・条件は予約前に公式サイトでご確認ください</div>'''
        j.append(f'tl.set("#bg",{{background:"#15324a"}},{T3(s)});')
    b.append(f'<div id="{cid}" class="abs card" style="opacity:0">{h}</div>')
    j.append(f'tl.fromTo("#{cid}",{{opacity:0,y:50}},{{opacity:1,y:0,duration:0.28,ease:"back.out(1.8)"}},{T3(s+0.05)});')
    j.append(f'tl.set("#{cid}",{{opacity:0}},{T3(end)});')
for i,l in enumerate(L): card(i,l)
j.append(f'tl.to("#fade",{{opacity:1,duration:0.5}},{T3(TOTAL-0.5)});')
CSS=open(os.path.join(HERE,"style.css")).read()
html=f'''<!doctype html>
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
<div class="chip">未宿泊・公式情報より</div><div class="acct">@chibi.shinsain</div>
<div class="ai">キャラクターはAIで生成したイラストです</div>
<div id="fade" class="abs" style="inset:0;background:#000;opacity:0;z-index:99"></div>
<audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-volume="1" data-track-index="2"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(j)}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>'''
open(os.path.join(HERE,"index.html"),"w").write(html); print("✓ index.html", TOTAL, "s")
