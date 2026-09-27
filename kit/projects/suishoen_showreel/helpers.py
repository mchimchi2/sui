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

