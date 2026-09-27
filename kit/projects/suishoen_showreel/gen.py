import json
HEAD='''<!doctype html>
<html lang="ja" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face { font-family:"SR"; font-weight:300; src: local("Noto Serif CJK JP Light"); }
@font-face { font-family:"SR"; font-weight:400; src: local("Noto Serif CJK JP"); }
@font-face { font-family:"SR"; font-weight:700; src: local("Noto Serif CJK JP Bold"); }
@font-face { font-family:"SR"; font-weight:900; src: local("Noto Serif CJK JP Black"); }
@font-face { font-family:"SS"; font-weight:400; src: local("Noto Sans CJK JP"); }
@font-face { font-family:"SS"; font-weight:900; src: local("Noto Sans CJK JP Black"); }
@font-face { font-family:"IT"; font-style:italic; src: local("DejaVu Serif Italic"), local("FreeSerif Italic"); }
:root { --ink:#0d1511; --jade:#2f6b4f; --jade2:#7fbf9a; --ivory:#f3eee3; --red:#c4452c; --gold:#c9a45c; }
* { margin:0; padding:0; box-sizing:border-box; }
html,body { width:1080px; height:1920px; overflow:hidden; background:var(--ink); }
#root { position:relative; width:1080px; height:1920px; overflow:hidden; background:var(--ink); font-family:"SR",serif; color:var(--ivory); }
#shake { position:absolute; inset:0; }
.shot { position:absolute; inset:0; overflow:hidden; }
.img { position:absolute; background-size:cover; background-position:center; }
.abs { position:absolute; }
.c { left:0; width:1080px; text-align:center; }
.ch { display:inline-block; }
.lbl { font-family:"SS",sans-serif; font-weight:400; letter-spacing:10px; font-size:26px; color:var(--jade2); }
.num { font-family:"SS",sans-serif; font-weight:900; }
.col { display:inline-block; overflow:hidden; vertical-align:top; }
.col > div { display:block; }
.col span { display:block; text-align:center; }
.grain { position:absolute; left:0; top:0; width:1140px; height:1980px; background:url(assets/grain.png); background-size:270px 480px; opacity:0.06; mix-blend-mode:overlay; z-index:99; pointer-events:none; }
.flash { position:absolute; inset:0; background:#fff; opacity:0; z-index:98; }
.fade { position:absolute; inset:0; background:#000; opacity:0; z-index:97; }
.vt { writing-mode:vertical-rl; }
</style>
</head>
<body>
'''
def chars(s,cls='ch',style=''):
    return ''.join(f'<span class="{cls}" style="{style}">{c if c!=" " else "&nbsp;"}</span>' for c in s)
def odo(digits,h,fs,color='var(--ivory)',idp='o'):
    cols=[]
    for i,d in enumerate(digits):
        if not d.isdigit():
            cols.append(f'<span class="col num" style="height:{h}px;font-size:{fs}px;line-height:{h}px;color:{color}">{d}</span>'); continue
        stack=''.join(f'<span style="height:{h}px">{k%10}</span>' for k in range(20))
        cols.append(f'<span class="col num" style="height:{h}px;font-size:{fs}px;line-height:{h}px;color:{color}"><div id="{idp}{i}">{stack}</div></span>')
    return ''.join(cols)
def odo_js(digits,h,t,idp='o',dur=1.0,stag=0.08):
    js=[]; k=0
    for i,d in enumerate(digits):
        if d.isdigit():
            js.append(f'tl.fromTo("#{idp}{i}",{{y:0}},{{y:{-(10+int(d))*h},duration:{dur+k*0.15},ease:"expo.out"}},{t+k*stag});'); k+=1
    return js
def page(cid,body,js,dur,extra_audio=''):
    return HEAD+f'''<div id="root" data-composition-id="{cid}" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920">
<div id="shake">
{body}
</div>
<div class="grain" id="grain"></div>
<div class="flash" id="flash"></div>
<div class="fade" id="fade"></div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
for (let i=0;i<{int(dur*12)};i++) tl.set("#grain",{{x:-(i*37%60),y:-(i*53%60)}},i/12);
window.__timelines = window.__timelines || {{}};
window.__timelines["{cid}"] = tl;
tl.seek(0);
</script>
</body></html>'''
def shake(js,t,amp=18,n=6):
    for k in range(n):
        a=amp*(1-k/n)*(1 if k%2 else -1)
        js.append(f'tl.to("#shake",{{x:{a:.1f},y:{-a*0.6:.1f},duration:0.03,ease:"none"}},{t+k*0.03:.3f});')
    js.append(f'tl.to("#shake",{{x:0,y:0,duration:0.03}},{t+n*0.03:.3f});')
def flash(js,t,peak=0.85,d=0.18):
    js.append(f'tl.set("#flash",{{opacity:{peak}}},{t:.3f});')
    js.append(f'tl.to("#flash",{{opacity:0,duration:{d},ease:"power2.out"}},{t+0.001:.3f});')

# ================= PART 1 (0-10s) =================
b=[];j=[]
b.append(f'''<div class="shot" id="A">
  <div class="abs" id="A_line" style="left:90px;top:958px;width:900px;height:2px;background:var(--jade2);transform-origin:0 50%"></div>
  <div class="abs c lbl" id="A_top" style="top:880px;font-size:24px;letter-spacing:14px">EST. 1925 · MITSUI VILLA</div>
  <div class="abs c lbl" id="A_bot" style="top:990px;color:var(--ivory);font-size:30px;letter-spacing:16px">HAKONE · KOWAKIDANI</div>
  <div class="abs c" id="A_kanji" style="top:430px;font-size:900px;line-height:1000px;font-weight:900;color:transparent;background:url(assets/forest.jpg);background-size:1300px 1733px;background-position:50% 40%;-webkit-background-clip:text;background-clip:text;opacity:0">翠</div>
  <div class="abs c lbl" id="A_sub" style="top:1500px;opacity:0;letter-spacing:22px;font-size:28px">S U I S H O E N</div>
</div>''')
j+=['tl.fromTo("#A_line",{scaleX:0},{scaleX:1,duration:0.7,ease:"expo.inOut"},0.05);',
    'tl.fromTo("#A_top",{opacity:0,y:20},{opacity:1,y:0,duration:0.5,ease:"power3.out"},0.35);',
    'tl.fromTo("#A_bot",{opacity:0,y:-20},{opacity:1,y:0,duration:0.5,ease:"power3.out"},0.45);',
    'tl.to(["#A_line","#A_top","#A_bot"],{opacity:0,duration:0.25},1.0);',
    'tl.fromTo("#A_kanji",{opacity:0,scale:1.7},{opacity:1,scale:1,duration:1.0,ease:"expo.out"},1.0);',
    'tl.fromTo("#A_kanji",{backgroundPosition:"50% 20%"},{backgroundPosition:"50% 60%",duration:1.6,ease:"none"},1.0);',
    'tl.fromTo("#A_sub",{opacity:0,y:30},{opacity:1,y:0,duration:0.5,ease:"power3.out"},1.3);',
    'tl.to("#A_sub",{opacity:0,duration:0.2},2.0);',
    'tl.to("#A_kanji",{scale:16,duration:0.55,ease:"power4.in"},2.0);',
    'tl.set("#A",{opacity:0},2.55);']
title="箱根・小涌谷の森へ。"
b.append(f'''<div class="shot" id="B" style="opacity:0">
  <div class="img" id="B_img" style="inset:-4%;background-image:url(assets/forest.jpg)"></div>
  <div class="abs" style="left:0;top:1100px;width:1080px;height:820px;background:linear-gradient(to bottom,rgba(13,21,17,0),rgba(13,21,17,0.92))"></div>
  <div class="abs c" id="B_t" style="top:1400px;font-size:84px;font-weight:700;letter-spacing:4px">{chars(title,"ch bt")}</div>
  <div class="abs c lbl" id="B_s" style="top:1540px;color:var(--ivory);letter-spacing:12px">EMBRACED BY THE FORESTS OF HAKONE</div>
</div>''')
j+=['tl.set("#B",{opacity:1},2.45);',
    'tl.fromTo("#B_img",{scale:1.5},{scale:1.05,duration:1.4,ease:"expo.out"},2.45);',
    'tl.to("#B_img",{scale:1.0,y:-30,duration:1.2,ease:"none"},3.85);',
    'tl.fromTo("#B .bt",{opacity:0,y:70,rotation:6},{opacity:1,y:0,rotation:0,duration:0.6,ease:"back.out(1.6)",stagger:0.05},2.75);',
    'tl.fromTo("#B_s",{opacity:0,y:20},{opacity:1,y:0,duration:0.5,ease:"power3.out"},3.3);']
flash(j,2.5,0.9,0.25); shake(j,4.0,14,5)
j+=['tl.to("#B_img",{scale:1.12,duration:0.12,ease:"power2.out"},4.0);','tl.to("#B",{opacity:0,duration:0.001},4.0);']
# C heritage
b.append(f'''<div class="shot" id="C" style="opacity:0;background:var(--ink)">
  <div class="abs c" style="top:170px">{odo("1925",250,250,"var(--ivory)","yr")}</div>
  <div class="abs c" id="C_era" style="top:440px;font-size:54px;font-weight:700;letter-spacing:10px;color:var(--gold)">大正十四年</div>
  <div class="abs c" id="C_desc" style="top:530px;font-size:40px;font-weight:400;letter-spacing:4px">三井家の別邸として建てられた邸宅</div>
  <div class="abs" id="C_frame" style="left:90px;top:660px;width:900px;height:1000px;overflow:hidden">
    <div class="img" id="C_img" style="inset:-3%;background-image:url(assets/entrance.jpg)"></div>
  </div>
  <div class="abs" id="C_stamp" style="left:690px;top:1380px;width:300px;height:300px;background:var(--red);transform:rotate(-8deg);opacity:0;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 8px rgba(196,69,44,0.25)">
     <div style="writing-mode:vertical-rl;font-size:56px;font-weight:900;color:var(--ivory);letter-spacing:6px;line-height:1.15">登録有形<br>文化財</div>
  </div>
  <div class="abs c" id="C_cap1" style="top:1705px;font-size:46px;font-weight:700;letter-spacing:6px">国登録有形文化財</div>
  <div class="abs c lbl" id="C_cap2" style="top:1785px;letter-spacing:8px;font-size:22px">REGISTERED TANGIBLE CULTURAL PROPERTY</div>
</div>''')
j+=['tl.set("#C",{opacity:1},4.0);']
j+=odo_js("1925",250,4.05,"yr",0.9,0.07)
j+=['tl.fromTo("#C_era",{opacity:0,x:-60},{opacity:1,x:0,duration:0.5,ease:"power3.out"},4.45);',
    'tl.fromTo("#C_desc",{opacity:0,x:60},{opacity:1,x:0,duration:0.5,ease:"power3.out"},4.6);',
    'tl.fromTo("#C_frame",{clipPath:"inset(50% 0% 50% 0%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.8,ease:"expo.inOut"},4.3);',
    'tl.fromTo("#C_img",{scale:1.35,filter:"grayscale(1)"},{scale:1.05,filter:"grayscale(0)",duration:2.6,ease:"power2.out"},4.3);',
    'tl.fromTo("#C_stamp",{opacity:0,scale:3,rotation:-30},{opacity:1,scale:1,rotation:-8,duration:0.25,ease:"power4.in"},5.35);',
    'tl.fromTo("#C_cap1",{opacity:0,y:30},{opacity:1,y:0,duration:0.4,ease:"power3.out"},5.7);',
    'tl.fromTo("#C_cap2",{opacity:0},{opacity:1,duration:0.4},5.85);']
shake(j,5.6,22,7)
# D shutter -> momiji
bars=''.join(f'<div class="abs sb" style="left:0;top:{i*240}px;width:1080px;height:241px;background:{"var(--jade)" if i%2==0 else "#24533d"};transform-origin:{"0" if i%2==0 else "100%"} 50%"></div>' for i in range(8))
b.append(f'''<div class="shot" id="D" style="opacity:0">
  <div class="abs" id="D_f1" style="left:0;top:230px;width:1080px;height:864px;overflow:hidden"><div class="img" id="D_img" style="inset:-4%;background-image:url(assets/dining.jpg)"></div></div>
  <div class="abs" id="D_f2" style="left:0;top:1110px;width:1080px;height:491px;overflow:hidden"><div class="img" id="D_img2" style="inset:-4%;background-image:url(assets/lounge.jpg)"></div></div>
  <div class="abs lbl" id="D_l" style="left:70px;top:150px;letter-spacing:12px">RYOTEI MOMIJI</div>
  <div class="abs c" id="D_t" style="top:1640px;font-size:96px;font-weight:900;letter-spacing:20px">{chars("料亭 紅葉","ch dt")}</div>
  <div class="abs c" id="D_s" style="top:1790px;font-size:34px;letter-spacing:4px;color:#cfd8d2">大正の邸宅で味わう、旬の日本料理と鉄板焼き</div>
  <div class="abs" id="D_bars" style="left:0;top:0;width:1080px;height:1920px">{bars}</div>
</div>''')
j+=['tl.set("#D",{opacity:1},7.0);','tl.set("#C",{opacity:0},7.45);',
    'tl.fromTo("#D .sb",{scaleX:0},{scaleX:1,duration:0.35,ease:"power3.in",stagger:0.03},6.95);',
    'tl.set(".sb",{transformOrigin:(i)=>i%2==0?"100% 50%":"0% 50%"},7.45);',
    'tl.to("#D .sb",{scaleX:0,duration:0.45,ease:"power3.out",stagger:0.03},7.5);',
    'tl.fromTo("#D_img",{scale:1.25,x:40},{scale:1.05,x:-30,duration:2.5,ease:"power2.out"},7.4);',
    'tl.fromTo("#D_f2",{x:1080},{x:0,duration:0.7,ease:"expo.out"},7.9);',
    'tl.fromTo("#D_img2",{x:-120},{x:30,duration:2.1,ease:"none"},7.9);',
    'tl.fromTo("#D_l",{opacity:0,x:-40},{opacity:1,x:0,duration:0.5},7.8);',
    'tl.fromTo("#D .dt",{opacity:0,y:-80,scale:1.4},{opacity:1,y:0,scale:1,duration:0.5,ease:"expo.out",stagger:0.06},8.1);',
    'tl.fromTo("#D_s",{opacity:0,y:20},{opacity:1,y:0,duration:0.5},8.5);',
    'tl.to("#D",{scale:0.92,opacity:0,duration:0.3,ease:"power3.in"},9.7);']
open('p1.html','w').write(page('p1','\n'.join(b),j,10))

# ================= PART 2 (10-20s) =================
b=[];j=[]
grid=''.join(f'<div class="abs gl" style="left:{90+i*180}px;top:0;width:1px;height:1920px;background:rgba(127,191,154,0.18);transform-origin:50% 0"></div>' for i in range(6))
b.append(f'''<div class="shot" id="E">
  {grid}
  <svg class="abs" style="left:190px;top:460px" width="700" height="700" viewBox="0 0 700 700"><circle id="E_c" cx="350" cy="350" r="330" fill="none" stroke="#c9a45c" stroke-width="4" stroke-dasharray="2074" stroke-dashoffset="2074" transform="rotate(-90 350 350)"/></svg>
  <div class="abs c" style="top:560px">{odo("23",500,500,"var(--ivory)","rm")}</div>
  <div class="abs c lbl" id="E_l" style="top:1210px;font-size:34px;letter-spacing:24px;color:var(--gold)">SUITES</div>
  <div class="abs c" id="E_t" style="top:1300px;font-size:60px;font-weight:700;letter-spacing:6px">すべてが異なる、23の客室。</div>
  <div class="abs c" id="E_s" style="top:1400px;font-size:32px;color:#b9c7bf;letter-spacing:3px">間取りも、アートも、しつらえも。</div>
</div>''')
j+=['tl.fromTo("#E .gl",{scaleY:0},{scaleY:1,duration:0.6,ease:"expo.out",stagger:0.05},0);',
    'tl.fromTo("#E_c",{strokeDashoffset:2074},{strokeDashoffset:0,duration:1.1,ease:"expo.inOut"},0.1);']
j+=odo_js("23",500,0.05,"rm",1.0,0.1)
j+=['tl.fromTo("#E_l",{opacity:0,scaleX:1.6},{opacity:1,scaleX:1,duration:0.7,ease:"expo.out"},0.4);',
    'tl.fromTo("#E_t",{opacity:0,y:30},{opacity:1,y:0,duration:0.5,ease:"power3.out"},0.6);',
    'tl.fromTo("#E_s",{opacity:0},{opacity:1,duration:0.5},0.85);']
panels=''
for i,(img,lab) in enumerate([("room1","LIVING"),("room2","VIEW"),("room3","BEDROOM")]):
    panels+=f'''<div class="abs pn" id="P{i}" style="left:{i*360}px;top:0;width:360px;height:1920px;overflow:hidden;border-right:2px solid var(--ink)">
      <div class="img pi" id="PI{i}" style="left:-270px;top:-5%;width:900px;height:110%;background-image:url(assets/{img}.jpg)"></div>
      <div class="abs lbl vt" style="right:26px;bottom:60px;color:var(--ivory);letter-spacing:12px;font-size:24px">{lab}</div></div>'''
b.append(f'<div class="shot" id="F" style="opacity:0">{panels}</div>')
j+=['tl.set("#F",{opacity:1},1.5);','tl.set("#E",{opacity:0},2.1);',
    'tl.fromTo("#P0",{y:-1920},{y:0,duration:0.6,ease:"expo.out"},1.5);',
    'tl.fromTo("#P1",{y:1920},{y:0,duration:0.6,ease:"expo.out"},1.6);',
    'tl.fromTo("#P2",{y:-1920},{y:0,duration:0.6,ease:"expo.out"},1.7);',
    'tl.fromTo("#PI0",{y:200},{y:-60,duration:2.4,ease:"power2.out"},1.5);',
    'tl.fromTo("#PI1",{y:-200},{y:60,duration:2.4,ease:"power2.out"},1.6);',
    'tl.fromTo("#PI2",{y:200},{y:-60,duration:2.4,ease:"power2.out"},1.7);',
    'tl.to("#P1",{x:1080,duration:0.5,ease:"expo.in"},3.4);','tl.to("#P2",{x:1080,duration:0.5,ease:"expo.in"},3.35);',
    'tl.to("#P0",{width:1080,duration:0.6,ease:"expo.inOut"},3.45);',
    'tl.to("#PI0",{left:0,width:1080,duration:0.6,ease:"expo.inOut"},3.45);']
rings=''.join(f'<div class="abs rg" style="left:340px;top:760px;width:400px;height:400px;border-radius:50%;border:3px solid rgba(243,238,227,0.8);opacity:0"></div>' for _ in range(5))
b.append(f'''<div class="shot" id="G" style="opacity:0">
  <div class="img" id="G_img" style="inset:0;background-image:url(assets/tub.jpg)"></div>
  <div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(13,21,17,0.1),rgba(13,21,17,0.75))"></div>
  {rings}
  <div class="abs vt" id="G_v" style="right:90px;top:180px;font-size:150px;font-weight:900;letter-spacing:10px;line-height:1">{chars("源泉掛け流し","ch gv")}</div>
  <div class="abs" id="G_t" style="left:80px;top:1380px;font-size:64px;font-weight:700;letter-spacing:4px">全室、露天風呂付き。</div>
  <div class="abs lbl" id="G_l" style="left:84px;top:1480px;color:var(--ivory);letter-spacing:10px">OPEN-AIR BATH IN EVERY ROOM</div>
  <div class="abs" id="G_bar" style="left:84px;top:1360px;width:420px;height:4px;background:var(--gold);transform-origin:0 50%"></div>
</div>''')
j+=['tl.set("#G",{opacity:1},4.05);','tl.set("#F",{opacity:0},4.1);',
    'tl.fromTo("#G_img",{scale:1.0},{scale:1.35,duration:2.5,ease:"power1.inOut"},4.05);',
    'tl.fromTo("#G .rg",{scale:0.1,opacity:0.9},{scale:3.2,opacity:0,duration:2.0,ease:"power2.out",stagger:0.35},4.2);',
    'tl.fromTo("#G .gv",{opacity:0,y:-90},{opacity:1,y:0,duration:0.45,ease:"expo.out",stagger:0.07},4.3);',
    'tl.fromTo("#G_bar",{scaleX:0},{scaleX:1,duration:0.6,ease:"expo.out"},4.9);',
    'tl.fromTo("#G_t",{opacity:0,x:-60},{opacity:1,x:0,duration:0.5,ease:"power3.out"},5.0);',
    'tl.fromTo("#G_l",{opacity:0},{opacity:1,duration:0.5},5.2);']
steam=''.join(f'<div class="abs st" style="left:{80+i*140}px;top:1500px;width:420px;height:420px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,0.35),rgba(255,255,255,0) 70%);opacity:0"></div>' for i in range(7))
b.append(f'''<div class="shot" id="H" style="opacity:0;background:#0b120f">
  <div class="img" id="H_img" style="inset:-6%;background-image:url(assets/tub.jpg);filter:blur(14px) brightness(0.55)"></div>
  {steam}
  <div class="abs c lbl" id="H_l" style="top:720px;color:var(--gold);letter-spacing:16px">HOT SPRING</div>
  <div class="abs c" id="H_t1" style="top:800px;font-size:58px;font-weight:400;letter-spacing:6px">肌にやさしい、</div>
  <div class="abs c" id="H_t2" style="top:900px;font-size:92px;font-weight:900;letter-spacing:6px">{chars("弱アルカリ性","ch ht")}</div>
  <div class="abs c" id="H_t3" style="top:1030px;font-size:92px;font-weight:900;letter-spacing:6px">{chars("単純温泉","ch ht")}</div>
  <div class="abs c lbl" id="H_s" style="top:1190px;color:#cfd8d2;letter-spacing:8px">MILDLY ALKALINE SIMPLE HOT SPRING</div>
</div>''')
j+=['tl.set("#H",{opacity:1},6.5);','tl.set("#G",{opacity:0},6.55);']
flash(j,6.5,0.6,0.3)
j+=['tl.fromTo("#H_img",{scale:1.2},{scale:1.05,duration:2.0,ease:"power2.out"},6.5);',
    'tl.fromTo("#H .st",{y:0,opacity:0,scale:0.6},{y:-1300,opacity:0.9,scale:1.6,duration:2.0,ease:"sine.out",stagger:0.12},6.5);',
    'tl.fromTo("#H_l",{opacity:0},{opacity:1,duration:0.4},6.6);',
    'tl.fromTo("#H_t1",{opacity:0,y:20},{opacity:1,y:0,duration:0.4},6.7);',
    'tl.fromTo("#H .ht",{opacity:0,scale:0.3,filter:"blur(10px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:0.45,ease:"back.out(2)",stagger:0.04},6.85);',
    'tl.fromTo("#H_s",{opacity:0},{opacity:1,duration:0.4},7.4);']
cuts=[("forest","FOREST"),("room3","REST"),("bath","BATH"),("room2","STAY")]
for i,(img,w) in enumerate(cuts):
    t=8.5+i*0.375
    b.append(f'''<div class="shot" id="Q{i}" style="opacity:0">
      <div class="img" id="QI{i}" style="inset:-3%;background-image:url(assets/{img}.jpg)"></div>
      <div class="abs" style="inset:0;background:rgba(13,21,17,0.25)"></div>
      <div class="abs c num" id="QT{i}" style="top:780px;font-size:250px;letter-spacing:6px;color:transparent;-webkit-text-stroke:4px var(--ivory)">{w}</div></div>''')
    j+=[f'tl.set("#Q{i}",{{opacity:1}},{t:.3f});',f'tl.fromTo("#QI{i}",{{scale:1.25}},{{scale:1.05,duration:0.4,ease:"expo.out"}},{t:.3f});',
        f'tl.fromTo("#QT{i}",{{scale:1.6,opacity:0}},{{scale:1,opacity:1,duration:0.25,ease:"expo.out"}},{t:.3f});']
    if i>0: j.append(f'tl.set("#Q{i-1}",{{opacity:0}},{t+0.01:.3f});')
    flash(j,t,0.5,0.12)
j+=['tl.set("#H",{opacity:0},8.52);','tl.to("#Q3",{opacity:0,duration:0.12},9.88);']
open('p2.html','w').write(page('p2','\n'.join(b),j,10))

# ================= PART 3 (20-30s) =================
b=[];j=[]
b.append(f'''<div class="shot" id="J" style="background:var(--jade)">
  <div class="abs" id="J_l" style="inset:0;background:var(--ivory);clip-path:polygon(0 0,62% 0,38% 100%,0 100%)"></div>
  <div class="abs" id="J_r" style="inset:0;background:var(--red);clip-path:polygon(62% 0,100% 0,100% 100%,38% 100%)"></div>
  <div class="abs vt" id="J_a" style="left:150px;top:300px;font-size:170px;font-weight:900;color:var(--ink);letter-spacing:12px">{chars("日本料理","ch ja")}</div>
  <div class="abs vt" id="J_b" style="right:150px;top:720px;font-size:170px;font-weight:900;color:var(--ivory);letter-spacing:12px">{chars("鉄板焼き","ch jb")}</div>
  <div class="abs c num" id="J_x" style="top:820px;font-size:200px;color:var(--gold)">×</div>
  <div class="abs c lbl" id="J_s" style="top:1740px;height:70px;line-height:70px;background:var(--ink);color:var(--ivory);letter-spacing:10px;font-size:24px">JAPANESE CUISINE × TEPPANYAKI</div>
</div>''')
j+=['tl.fromTo("#J_l",{x:-1100},{x:0,duration:0.5,ease:"expo.out"},0);',
    'tl.fromTo("#J_r",{x:1100},{x:0,duration:0.5,ease:"expo.out"},0.05);',
    'tl.fromTo("#J .ja",{opacity:0,y:-60},{opacity:1,y:0,duration:0.35,ease:"expo.out",stagger:0.05},0.3);',
    'tl.fromTo("#J .jb",{opacity:0,y:60},{opacity:1,y:0,duration:0.35,ease:"expo.out",stagger:0.05},0.45);',
    'tl.fromTo("#J_x",{rotation:-180,scale:0},{rotation:0,scale:1,duration:0.6,ease:"back.out(1.8)"},0.55);',
    'tl.fromTo("#J_s",{opacity:0},{opacity:1,duration:0.4},0.9);',
    'tl.to(["#J_l","#J_a"],{x:-1100,duration:0.45,ease:"expo.in"},1.75);',
    'tl.to(["#J_r","#J_b"],{x:1100,duration:0.45,ease:"expo.in"},1.75);',
    'tl.to(["#J_x","#J_s"],{opacity:0,scale:0.5,duration:0.3},1.75);']
circ=''.join(f'<circle cx="540" cy="540" r="{160+i*70}" fill="none" stroke="rgba(243,238,227,{0.35-i*0.05:.2f})" stroke-width="2" stroke-dasharray="{8+i*6} {14+i*5}"/>' for i in range(5))
b.append(f'''<div class="shot" id="K" style="opacity:0;background:radial-gradient(circle at 50% 45%,#3d7a5c,#16281f)">
  <svg class="abs" id="K_svg" style="left:0;top:420px" width="1080" height="1080" viewBox="0 0 1080 1080">{circ}</svg>
  <div class="abs c lbl" id="K_l" style="top:840px;color:var(--gold);letter-spacing:18px">SPA</div>
  <div class="abs c" id="K_t" style="top:900px;font-family:'IT',serif;font-style:italic;font-size:118px;color:var(--ivory)">{chars("Spa by Sisley","ch kt")}</div>
  <div class="abs c" id="K_s" style="top:1110px;font-size:44px;letter-spacing:6px">植物の力に、身をゆだねる。</div>
</div>''')
j+=['tl.set("#K",{opacity:1},2.0);',
    'tl.fromTo("#K_svg",{rotation:-40,scale:0.6,opacity:0},{rotation:20,scale:1,opacity:1,duration:2.0,ease:"power2.out"},2.0);',
    'tl.fromTo("#K_l",{opacity:0},{opacity:1,duration:0.4},2.15);',
    'tl.fromTo("#K .kt",{opacity:0,y:40,rotation:8},{opacity:1,y:0,rotation:0,duration:0.5,ease:"power3.out",stagger:0.035},2.2);',
    'tl.fromTo("#K_s",{opacity:0,y:20},{opacity:1,y:0,duration:0.5},2.75);',
    'tl.to("#K",{clipPath:"circle(0% at 50% 50%)",duration:0.5,ease:"expo.in"},3.55);']
leaves=''
import random; random.seed(4)
for i in range(16):
    x=random.randint(-50,1050); s=random.randint(26,56); col=random.choice(["#c4452c","#d9722f","#c9a45c","#a8321f"])
    leaves+=f'<div class="abs lf" style="left:{x}px;top:-120px;width:{s}px;height:{s}px;background:{col};border-radius:0 70% 0 70%;opacity:0.9"></div>'
b.append(f'''<div class="shot" id="L" style="opacity:0">
  <div class="img" id="L_img" style="inset:-5%;background-image:url(assets/garden.jpg)"></div>
  <div class="abs" style="left:0;top:900px;width:1080px;height:1020px;background:linear-gradient(to bottom,rgba(13,21,17,0),rgba(13,21,17,0.9))"></div>
  {leaves}
  <div class="abs lbl" id="L_l" style="left:80px;top:1250px;color:var(--gold);letter-spacing:14px">THE GARDEN</div>
  <div class="abs" style="left:80px;top:1320px"><div class="abs" id="L_b1" style="left:-20px;top:10px;width:560px;height:110px;background:var(--jade);transform-origin:0 50%"></div><div class="abs" id="L_t1" style="left:0;top:0;white-space:nowrap;font-size:96px;font-weight:900">約3,000坪</div></div>
  <div class="abs" style="left:80px;top:1470px"><div class="abs" id="L_b2" style="left:-20px;top:8px;width:620px;height:96px;background:var(--red);transform-origin:0 50%"></div><div class="abs" id="L_t2" style="left:0;top:0;white-space:nowrap;font-size:80px;font-weight:900">樹齢300年の楓</div></div>
  <div class="abs" id="L_s" style="left:80px;top:1620px;font-size:36px;letter-spacing:3px;color:#dfe6e1">四季の移ろいを、庭の散策で。</div>
</div>''')
j+=['tl.set("#L",{opacity:1},3.55);',
    'tl.fromTo("#L_img",{scale:1.3},{scale:1.02,duration:3.4,ease:"power2.out"},3.55);',
    'tl.fromTo("#L .lf",{y:0,x:0,rotation:0},{y:2200,x:(i)=>((i*97)%300)-150,rotation:(i)=>540+(i*67)%400,duration:(i)=>2.6+(i%5)*0.35,ease:"none",stagger:0.12},3.6);',
    'tl.fromTo("#L_l",{opacity:0},{opacity:1,duration:0.4},4.1);',
    'tl.fromTo("#L_b1",{scaleX:0},{scaleX:1,duration:0.4,ease:"expo.out"},4.2);',
    'tl.fromTo("#L_t1",{opacity:0,x:-40},{opacity:1,x:0,duration:0.4,ease:"power3.out"},4.3);',
    'tl.fromTo("#L_b2",{scaleX:0},{scaleX:1,duration:0.4,ease:"expo.out"},4.55);',
    'tl.fromTo("#L_t2",{opacity:0,x:-40},{opacity:1,x:0,duration:0.4,ease:"power3.out"},4.65);',
    'tl.fromTo("#L_s",{opacity:0,y:20},{opacity:1,y:0,duration:0.5},5.0);',
    'tl.to("#L",{opacity:0,duration:0.001},7.0);']
name="箱根・翠松園"
b.append(f'''<div class="shot" id="M" style="opacity:0">
  <div class="img" id="M_img" style="inset:-5%;background-image:url(assets/forest.jpg);filter:brightness(0.45) saturate(0.9)"></div>
  <div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(13,21,17,0.2),rgba(13,21,17,0.85))"></div>
  <div class="abs c lbl" id="M_l" style="top:700px;color:var(--gold);letter-spacing:18px">SMALL LUXURY RESORT</div>
  <div class="abs" id="M_ln1" style="left:90px;top:960px;width:900px;height:2px;background:var(--gold);transform-origin:50% 50%"></div>
  <div class="abs c" style="top:780px;height:170px;overflow:hidden"><div id="M_t" style="font-size:132px;font-weight:900;letter-spacing:10px;line-height:170px">{name}</div></div>
  <div class="abs c lbl" id="M_e" style="top:990px;color:var(--ivory);letter-spacing:22px;font-size:30px">HAKONE SUISHOEN</div>
  <div class="abs c" id="M_a" style="top:1080px;font-size:32px;letter-spacing:3px;color:#cfd8d2">神奈川県箱根町小涌谷　／　都心から車で2時間圏内</div>
  <div class="abs c" id="M_th" style="top:1500px;font-family:'IT',serif;font-style:italic;font-size:54px;color:var(--ivory)">Thank you for a wonderful stay.</div>
  <div class="abs c" id="M_th2" style="top:1590px;font-size:36px;letter-spacing:6px;color:#dfe6e1">素敵な時間を、ありがとうございました。</div>
</div>''')
j+=['tl.set("#M",{opacity:1},7.0);']
flash(j,7.0,1.0,0.35); shake(j,7.0,20,6)
j+=['tl.fromTo("#M_img",{scale:1.3},{scale:1.05,duration:3.0,ease:"power2.out"},7.0);',
    'tl.fromTo("#M_t",{y:170},{y:0,duration:0.7,ease:"expo.out"},7.15);',
    'tl.fromTo("#M_ln1",{scaleX:0},{scaleX:1,duration:0.8,ease:"expo.inOut"},7.3);',
    'tl.fromTo("#M_l",{opacity:0,scaleX:1.5},{opacity:1,scaleX:1,duration:0.8,ease:"expo.out"},7.4);',
    'tl.fromTo("#M_e",{opacity:0,y:20},{opacity:1,y:0,duration:0.6,ease:"power3.out"},7.6);',
    'tl.fromTo("#M_a",{opacity:0},{opacity:1,duration:0.6},7.9);',
    'tl.fromTo("#M_th",{opacity:0,y:20},{opacity:1,y:0,duration:0.7,ease:"power3.out"},8.4);',
    'tl.fromTo("#M_th2",{opacity:0,y:20},{opacity:1,y:0,duration:0.7,ease:"power3.out"},8.6);',
    'tl.to("#fade",{opacity:1,duration:0.5,ease:"sine.in"},9.5);']
open('p3.html','w').write(page('p3','\n'.join(b),j,10))
print('ok')
