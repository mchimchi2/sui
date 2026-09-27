exec(open('helpers.py').read())
VID='''<video id="{id}" class="clip" src="assets/{src}" data-start="{st}" data-duration="{du}" data-media-start="0" muted playsinline style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;{extra}"></video>'''
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
for i,(img,lab) in enumerate([("room2","LIVING"),("onsen","BATH"),("room3","BEDROOM")]):
    panels+=f'''<div class="abs pn" id="P{i}" style="left:{i*360}px;top:0;width:360px;height:1920px;overflow:hidden;border-right:2px solid var(--ink)">
      <div class="img pi" id="PI{i}" style="left:-270px;top:-5%;width:900px;height:110%;background-image:url(assets/{img}.jpg)"></div>
      <div class="abs lbl vt" style="right:26px;bottom:60px;color:var(--ivory);letter-spacing:12px;font-size:24px">{lab}</div></div>'''
b.append(f'<div class="shot" id="F" style="opacity:0">{panels}</div>')
j+=['tl.set("#F",{opacity:1},1.5);','tl.set("#E",{opacity:0},2.1);',
    'tl.fromTo("#P0",{y:-1920},{y:0,duration:0.6,ease:"expo.out"},1.5);',
    'tl.fromTo("#P1",{y:1920},{y:0,duration:0.6,ease:"expo.out"},1.6);',
    'tl.fromTo("#P2",{y:-1920},{y:0,duration:0.6,ease:"expo.out"},1.7);',
    'tl.fromTo("#PI0",{y:200},{y:-60,duration:2.0,ease:"power2.out"},1.5);',
    'tl.fromTo("#PI1",{y:-200},{y:60,duration:2.0,ease:"power2.out"},1.6);',
    'tl.fromTo("#PI2",{y:200},{y:-60,duration:2.0,ease:"power2.out"},1.7);',
    'tl.to("#P0",{x:-400,opacity:0,duration:0.4,ease:"expo.in"},3.1);',
    'tl.to("#P2",{x:400,opacity:0,duration:0.4,ease:"expo.in"},3.1);',
    'tl.to("#P1",{scale:1.25,opacity:0,duration:0.45,ease:"expo.in"},3.1);']
# G: live room tour clip (living -> open-air bath)
rings=''.join(f'<div class="abs rg" style="left:340px;top:1060px;width:400px;height:400px;border-radius:50%;border:3px solid rgba(243,238,227,0.8);opacity:0"></div>' for _ in range(4))
b.append(f'''<div class="shot" id="G" style="opacity:0">
  {VID.format(id="G_v1",src="v_room.mp4",st=3.45,du=2.95,extra="")}
  <div class="abs" style="inset:0;background:linear-gradient(to bottom,rgba(13,21,17,0.55),rgba(13,21,17,0) 35%,rgba(13,21,17,0) 60%,rgba(13,21,17,0.8))"></div>
  {rings}
  <div class="abs vt" id="G_v" style="right:70px;top:120px;font-size:140px;font-weight:900;letter-spacing:10px;line-height:1;text-shadow:0 4px 30px rgba(0,0,0,0.5)">{chars("源泉掛け流し","ch gv")}</div>
  <div class="abs" id="G_bar" style="left:84px;top:1560px;width:420px;height:4px;background:var(--gold);transform-origin:0 50%"></div>
  <div class="abs" id="G_t" style="left:80px;top:1585px;font-size:64px;font-weight:700;letter-spacing:4px">全室、露天風呂付き。</div>
  <div class="abs lbl" id="G_l" style="left:84px;top:1690px;color:var(--ivory);letter-spacing:10px">OPEN-AIR BATH IN EVERY ROOM</div>
</div>''')
j+=['tl.set("#G",{opacity:1},3.45);','tl.set("#F",{opacity:0},3.6);',
    'tl.fromTo("#G",{clipPath:"circle(0% at 50% 50%)"},{clipPath:"circle(75% at 50% 50%)",duration:0.5,ease:"expo.out"},3.45);',
    'tl.fromTo("#G_v1",{scale:1.15},{scale:1.0,duration:3.0,ease:"power1.out"},3.45);',
    'tl.fromTo("#G .rg",{scale:0.1,opacity:0.9},{scale:3.0,opacity:0,duration:1.8,ease:"power2.out",stagger:0.35},4.6);',
    'tl.fromTo("#G .gv",{opacity:0,y:-90},{opacity:1,y:0,duration:0.45,ease:"expo.out",stagger:0.07},3.8);',
    'tl.fromTo("#G_bar",{scaleX:0},{scaleX:1,duration:0.6,ease:"expo.out"},4.5);',
    'tl.fromTo("#G_t",{opacity:0,x:-60},{opacity:1,x:0,duration:0.5,ease:"power3.out"},4.6);',
    'tl.fromTo("#G_l",{opacity:0},{opacity:1,duration:0.5},4.8);']
steam=''.join(f'<div class="abs st" style="left:{80+i*140}px;top:1300px;width:420px;height:420px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,0.3),rgba(255,255,255,0) 70%);opacity:0"></div>' for i in range(7))
b.append(f'''<div class="shot" id="H" style="opacity:0;background:#0b120f">
  <div class="img" id="H_img" style="inset:0;background-image:url(assets/onsen.jpg);filter:brightness(0.62);transform-origin:50% 55%"></div>
  {steam}
  <div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 35%,rgba(0,0,0,0.55),rgba(0,0,0,0) 65%)"></div>
  <div class="abs c lbl" id="H_l" style="top:360px;color:var(--gold);letter-spacing:16px">HOT SPRING</div>
  <div class="abs c" id="H_t1" style="top:440px;font-size:58px;font-weight:400;letter-spacing:6px">肌にやさしい、</div>
  <div class="abs c" id="H_t2" style="top:540px;font-size:92px;font-weight:900;letter-spacing:6px">{chars("弱アルカリ性","ch ht")}</div>
  <div class="abs c" id="H_t3" style="top:670px;font-size:92px;font-weight:900;letter-spacing:6px">{chars("単純温泉","ch ht")}</div>
  <div class="abs c lbl" id="H_s" style="top:830px;color:#cfd8d2;letter-spacing:8px">MILDLY ALKALINE SIMPLE HOT SPRING</div>
</div>''')
j+=['tl.set("#H",{opacity:1},6.4);','tl.set("#G",{opacity:0},6.45);']
flash(j,6.4,0.6,0.3)
j+=['tl.fromTo("#H_img",{scale:1.0},{scale:1.22,duration:2.1,ease:"power1.inOut"},6.4);',
    'tl.fromTo("#H .st",{y:0,opacity:0,scale:0.6},{y:-1100,opacity:0.9,scale:1.6,duration:2.0,ease:"sine.out",stagger:0.12},6.4);',
    'tl.fromTo("#H_l",{opacity:0},{opacity:1,duration:0.4},6.5);',
    'tl.fromTo("#H_t1",{opacity:0,y:20},{opacity:1,y:0,duration:0.4},6.6);',
    'tl.fromTo("#H .ht",{opacity:0,scale:0.3,filter:"blur(10px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:0.45,ease:"back.out(2)",stagger:0.04},6.75);',
    'tl.fromTo("#H_s",{opacity:0},{opacity:1,duration:0.4},7.3);']
cuts=[("img","forest","FOREST"),("vid","v_bed.mp4","REST"),("vid","v_bath.mp4","BATH"),("img","room2","STAY")]
for i,(kind,src,w) in enumerate(cuts):
    t=8.5+i*0.375
    media=(f'<div class="img" id="QI{i}" style="inset:-3%;background-image:url(assets/{src}.jpg)"></div>' if kind=="img"
           else VID.format(id=f"QI{i}",src=src,st=round(t,3),du=0.4 if i<3 else 0.5,extra=""))
    b.append(f'''<div class="shot" id="Q{i}" style="opacity:0">{media}
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
# J: kaiseki montage
b.append(f'''<div class="shot" id="J1">
  <div class="img" id="J1_img" style="inset:0;background-image:url(assets/hassun.jpg)"></div>
  <div class="abs" style="inset:0;background:linear-gradient(to right,rgba(13,21,17,0) 45%,rgba(13,21,17,0.7))"></div>
  <div class="abs vt" id="J1_k" style="right:70px;top:150px;font-size:230px;font-weight:900;letter-spacing:20px;line-height:1;text-shadow:0 6px 40px rgba(0,0,0,0.5)">{chars("懐石","ch jk")}</div>
  <div class="abs lbl vt" id="J1_l" style="right:330px;top:160px;color:var(--ivory);letter-spacing:16px;font-size:26px">KAISEKI · RYOTEI MOMIJI</div>
</div>''')
j+=['tl.fromTo("#J1",{clipPath:"circle(0% at 50% 45%)"},{clipPath:"circle(80% at 50% 45%)",duration:0.6,ease:"expo.out"},0);',
    'tl.fromTo("#J1_img",{scale:1.3,rotation:-3},{scale:1.05,rotation:0,duration:1.4,ease:"expo.out"},0);',
    'tl.fromTo("#J1 .jk",{opacity:0,y:-120,scale:1.5},{opacity:1,y:0,scale:1,duration:0.5,ease:"expo.out",stagger:0.1},0.2);',
    'tl.fromTo("#J1_l",{opacity:0,y:-40},{opacity:1,y:0,duration:0.5},0.45);']
b.append('''<div class="shot" id="J2" style="opacity:0;background:var(--ink)">
  <div class="img" style="inset:-6%;background-image:url(assets/sashimi.jpg);filter:blur(24px) brightness(0.45)"></div>
  <div class="abs" id="J2_f" style="left:60px;top:420px;width:960px;height:822px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,0.5)"><div class="img" id="J2_img" style="inset:0;background-image:url(assets/sashimi.jpg)"></div></div>
</div>''')
j+=['tl.set("#J2",{opacity:1},1.15);',
    'tl.fromTo("#J2_f",{y:1500,rotation:8},{y:0,rotation:0,duration:0.5,ease:"expo.out"},1.15);',
    'tl.fromTo("#J2_img",{scale:1.3},{scale:1.05,duration:1.0,ease:"power2.out"},1.15);']
b.append('''<div class="shot" id="J3" style="opacity:0;background:var(--ink)">
  <div class="img" id="J3_img" style="inset:0;background-image:url(assets/menu.jpg);background-position:36% 20%"></div>
  <div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(0,0,0,0),rgba(0,0,0,0.55))"></div>
</div>''')
j+=['tl.set("#J3",{opacity:1},2.0);','tl.set("#J1",{opacity:0},2.0);',
    'tl.fromTo("#J3",{clipPath:"inset(0% 100% 0% 0%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.35,ease:"expo.out"},2.0);',
    'tl.fromTo("#J3_img",{scale:1.25,x:60},{scale:1.08,x:-30,duration:0.9,ease:"power2.out"},2.0);']
b.append(f'''<div class="shot" id="J4" style="opacity:0;background:var(--ink)">
  {VID.format(id="J4_v",src="v_bfast.mp4",st=2.75,du=0.8,extra="transform-origin:50% 100%")}
  <div class="abs" style="inset:0;background:linear-gradient(to bottom,rgba(13,21,17,0.8),rgba(13,21,17,0) 40%)"></div>
</div>''')
j+=['tl.set("#J4",{opacity:1},2.75);','tl.set(["#J2","#J3"],{opacity:0},2.8);',
    'tl.fromTo("#J4_v",{scale:1.6},{scale:1.45,duration:0.8,ease:"power1.out"},2.75);']
# persistent food captions (above all J shots)
b.append('''<div class="shot" id="Jcap" style="pointer-events:none;z-index:20">
  <div class="abs c" id="Jc1" style="top:1560px;font-size:56px;font-weight:700;letter-spacing:6px;text-shadow:0 4px 24px rgba(0,0,0,0.6)">四季を映す、料亭 紅葉の日本料理</div>
  <div class="abs c" style="top:1665px"><span id="Jc2" style="display:inline-block;padding:10px 28px;border:2px solid var(--gold);font-size:30px;letter-spacing:4px;background:rgba(13,21,17,0.55)">夕食は懐石 または 鉄板焼き</span></div>
  <div class="abs c" id="Jc3" style="top:260px;font-size:60px;font-weight:700;letter-spacing:8px;opacity:0;text-shadow:0 4px 24px rgba(0,0,0,0.6)">朝は、和の御膳。</div>
</div>''')
j+=['tl.fromTo("#Jc1",{opacity:0,y:30},{opacity:1,y:0,duration:0.5,ease:"power3.out"},0.5);',
    'tl.fromTo("#Jc2",{opacity:0,scale:0.8},{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"},0.8);',
    'tl.to(["#Jc1","#Jc2"],{opacity:0,duration:0.2},2.7);',
    'tl.fromTo("#Jc3",{opacity:0,y:-30},{opacity:1,y:0,duration:0.35,ease:"power3.out"},2.85);',
    'tl.to("#Jc3",{opacity:0,duration:0.1},3.4);']
flash(j,1.15,0.4,0.12); flash(j,2.75,0.4,0.12)
# K: spa (Sisley amenity photo in an arch)
circ=''.join(f'<circle cx="540" cy="540" r="{220+i*70}" fill="none" stroke="rgba(243,238,227,{0.35-i*0.05:.2f})" stroke-width="2" stroke-dasharray="{8+i*6} {14+i*5}"/>' for i in range(5))
b.append(f'''<div class="shot" id="K" style="opacity:0;background:radial-gradient(circle at 50% 40%,#3d7a5c,#16281f);z-index:21">
  <svg class="abs" id="K_svg" style="left:0;top:250px" width="1080" height="1080" viewBox="0 0 1080 1080">{circ}</svg>
  <div class="abs" id="K_f" style="left:290px;top:300px;width:500px;height:760px;overflow:hidden;border-radius:250px 250px 0 0;box-shadow:0 20px 60px rgba(0,0,0,0.45)"><div class="img" id="K_img" style="inset:0;background-image:url(assets/sisley.jpg);background-position:50% 55%"></div></div>
  <div class="abs c lbl" id="K_l" style="top:1150px;color:var(--gold);letter-spacing:18px">SPA</div>
  <div class="abs c" id="K_t" style="top:1200px;font-family:'IT',serif;font-style:italic;font-size:112px;color:var(--ivory)">{chars("Spa by Sisley","ch kt")}</div>
  <div class="abs c" id="K_s" style="top:1400px;font-size:44px;letter-spacing:6px">植物の力に、身をゆだねる。</div>
</div>''')
j+=['tl.set("#K",{opacity:1},3.4);','tl.set("#J4",{opacity:0},3.5);',
    'tl.fromTo("#K",{clipPath:"inset(100% 0% 0% 0%)"},{clipPath:"inset(0% 0% 0% 0%)",duration:0.45,ease:"expo.out"},3.4);',
    'tl.fromTo("#K_svg",{rotation:-40,scale:0.6,opacity:0},{rotation:20,scale:1,opacity:1,duration:1.5,ease:"power2.out"},3.4);',
    'tl.fromTo("#K_f",{y:120,opacity:0},{y:0,opacity:1,duration:0.6,ease:"expo.out"},3.5);',
    'tl.fromTo("#K_img",{scale:1.3},{scale:1.05,duration:1.4,ease:"power2.out"},3.5);',
    'tl.fromTo("#K_l",{opacity:0},{opacity:1,duration:0.3},3.7);',
    'tl.fromTo("#K .kt",{opacity:0,y:40,rotation:8},{opacity:1,y:0,rotation:0,duration:0.45,ease:"power3.out",stagger:0.03},3.75);',
    'tl.fromTo("#K_s",{opacity:0,y:20},{opacity:1,y:0,duration:0.45},4.15);',
    'tl.to("#K",{clipPath:"circle(0% at 50% 50%)",duration:0.45,ease:"expo.in"},4.55);']
leaves=''
import random; random.seed(4)
for i in range(16):
    x=random.randint(-50,1050); s_=random.randint(26,56); col=random.choice(["#c4452c","#d9722f","#c9a45c","#a8321f"])
    leaves+=f'<div class="abs lf" style="left:{x}px;top:-120px;width:{s_}px;height:{s_}px;background:{col};border-radius:0 70% 0 70%;opacity:0.9"></div>'
b.append(f'''<div class="shot" id="L" style="opacity:0;z-index:5">
  <div class="img" id="L_img" style="inset:-5%;background-image:url(assets/garden.jpg)"></div>
  <div class="abs" style="left:0;top:900px;width:1080px;height:1020px;background:linear-gradient(to bottom,rgba(13,21,17,0),rgba(13,21,17,0.9))"></div>
  {leaves}
  <div class="abs lbl" id="L_l" style="left:80px;top:1250px;color:var(--gold);letter-spacing:14px">THE GARDEN</div>
  <div class="abs" style="left:80px;top:1320px"><div class="abs" id="L_b1" style="left:-20px;top:10px;width:560px;height:110px;background:var(--jade);transform-origin:0 50%"></div><div class="abs" id="L_t1" style="left:0;top:0;white-space:nowrap;font-size:96px;font-weight:900">約3,000坪</div></div>
  <div class="abs" style="left:80px;top:1470px"><div class="abs" id="L_b2" style="left:-20px;top:8px;width:620px;height:96px;background:var(--red);transform-origin:0 50%"></div><div class="abs" id="L_t2" style="left:0;top:0;white-space:nowrap;font-size:80px;font-weight:900">樹齢300年の楓</div></div>
  <div class="abs" id="L_s" style="left:80px;top:1620px;font-size:36px;letter-spacing:3px;color:#dfe6e1">四季の移ろいを、庭の散策で。</div>
</div>''')
j+=['tl.set("#L",{opacity:1},4.55);',
    'tl.fromTo("#L_img",{scale:1.3},{scale:1.02,duration:2.45,ease:"power2.out"},4.55);',
    'tl.fromTo("#L .lf",{y:0,x:0,rotation:0},{y:2200,x:(i)=>((i*97)%300)-150,rotation:(i)=>540+(i*67)%400,duration:(i)=>2.2+(i%5)*0.3,ease:"none",stagger:0.08},4.55);',
    'tl.fromTo("#L_l",{opacity:0},{opacity:1,duration:0.4},4.9);',
    'tl.fromTo("#L_b1",{scaleX:0},{scaleX:1,duration:0.4,ease:"expo.out"},5.0);',
    'tl.fromTo("#L_t1",{opacity:0,x:-40},{opacity:1,x:0,duration:0.4,ease:"power3.out"},5.1);',
    'tl.fromTo("#L_b2",{scaleX:0},{scaleX:1,duration:0.4,ease:"expo.out"},5.35);',
    'tl.fromTo("#L_t2",{opacity:0,x:-40},{opacity:1,x:0,duration:0.4,ease:"power3.out"},5.45);',
    'tl.fromTo("#L_s",{opacity:0,y:20},{opacity:1,y:0,duration:0.5},5.8);',
    'tl.to("#L",{opacity:0,duration:0.001},7.0);']
b.append(f'''<div class="shot" id="M" style="opacity:0;z-index:30">
  <div class="img" id="M_img" style="inset:-5%;background-image:url(assets/forest.jpg);filter:brightness(0.45) saturate(0.9)"></div>
  <div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 50%,rgba(13,21,17,0.2),rgba(13,21,17,0.85))"></div>
  <div class="abs c lbl" id="M_l" style="top:700px;color:var(--gold);letter-spacing:18px">SMALL LUXURY RESORT</div>
  <div class="abs" id="M_ln1" style="left:90px;top:960px;width:900px;height:2px;background:var(--gold);transform-origin:50% 50%"></div>
  <div class="abs c" style="top:780px;height:170px;overflow:hidden"><div id="M_t" style="font-size:132px;font-weight:900;letter-spacing:10px;line-height:170px">箱根・翠松園</div></div>
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
