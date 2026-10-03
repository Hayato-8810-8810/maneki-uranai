# 今日の一枚（タロット）のリンクカード（1200×630）とInstagram表紙（1080×1350）を、site/tarot/index.html の札から作り直す
# 使い方：python3 docs/tools/make_tarot_images.py   （Playwrightが必要）
from playwright.sync_api import sync_playwright
import base64, os
brand=base64.b64encode(open("site/images/brand.webp","rb").read()).decode()
CSS='''
*{box-sizing:border-box;margin:0}
body{font-family:"Noto Sans CJK JP",sans-serif;color:#2A2118}
.serif{font-family:"Noto Serif CJK JP",serif;font-weight:700}
.cv{position:relative;overflow:hidden;background:radial-gradient(120% 60% at 50% 0%,#FFF8E6 0%,transparent 70%),#F7F1E3;display:flex;align-items:center}
.cv::after{content:"";position:absolute;inset:28px;border:3px solid #B93A24;border-radius:28px}
.card{position:relative;aspect-ratio:5/8;border-radius:.6em;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:.9em .5em .8em;color:#FFF6DC;
 font-family:"Noto Serif CJK JP",serif;font-weight:700;background:radial-gradient(circle at 50% 46%,var(--g) 0%,var(--c) 72%);box-shadow:0 .3em .9em rgba(60,40,10,.3);flex:none}
.card::after{content:"";position:absolute;inset:.35em;border:1px solid rgba(255,246,220,.6);border-radius:.4em}
.card .num{font-size:1.05em;letter-spacing:.12em;line-height:1}.card svg{width:80%}.card .nm{font-size:1.15em;letter-spacing:.14em;line-height:1.2;white-space:nowrap}
.fan{position:relative;flex:none}
.fan .card{position:absolute;top:0;left:0}
.eyebrow{color:#8A6212;font-weight:700;letter-spacing:.22em}
.pill{display:inline-block;background:#B93A24;color:#fff;font-weight:700;border-radius:999px}
.foot{display:flex;align-items:center;gap:14px;color:#6E6252}.foot img{border-radius:50%}
'''
def fan(faces,w,fs):
    rot=[-14,0,14]; dx=[-0.62,0,0.62]; dy=[0.06,0,0.06]
    out=""
    for k,f in enumerate(faces):
        out+=f.replace('class="card ','class="card x').replace('style="',f'style="width:{w}px;font-size:{fs}px;transform:translate({dx[k]*w}px,{dy[k]*w}px) rotate({rot[k]}deg);z-index:{2 if k==1 else 1};',1)
    return f'<div class="fan" style="width:{w}px;height:{w*1.6}px">{out}</div>'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto("file://"+os.path.abspath("site/tarot/index.html"))
    faces=pg.evaluate("[17,19,18].map(i=>faceHTML(i))")   # 星・太陽・月
    b_img=f'<img src="data:image/webp;base64,{brand}"'
    ogp=f'''<div class="cv" style="width:1200px;height:630px;padding:0 90px;gap:150px">
      <div style="margin-left:110px">{fan(faces,210,17)}</div>
      <div style="position:relative;z-index:1"><p class="eyebrow" style="font-size:24px">TAROT · 1日1枚</p>
      <p class="serif" style="font-size:96px;line-height:1.3;letter-spacing:.06em">今日の一枚</p>
      <p style="font-size:30px;line-height:1.7;color:#6E6252;margin-top:8px">招き猫が、あなたの今日のために<br>タロットを1枚めくります。</p>
      <p class="foot" style="font-size:26px;margin-top:28px">{b_img} width="52" height="52">まねき占い堂</p></div></div>'''
    ig=f'''<div class="cv" style="width:1080px;height:1350px;flex-direction:column;padding:120px 80px 96px">
      <p class="eyebrow" style="font-size:30px">TAROT · 1日1枚</p>
      <p class="serif" style="font-size:132px;line-height:1.3;letter-spacing:.06em;margin-top:8px">今日の一枚</p>
      <div style="margin-top:56px">{fan(faces,280,23)}</div>
      <p style="font-size:38px;line-height:1.7;text-align:center;margin-top:84px">招き猫が、あなたの今日のために<br>タロットを1枚めくります。</p>
      <p class="pill" style="font-size:36px;padding:18px 52px;margin-top:36px">無料・1日1回・ワンタップ</p>
      <p class="foot" style="font-size:28px;margin-top:auto;position:relative;z-index:1">{b_img} width="56" height="56">まねき占い堂　@manekiuranai</p></div>'''
    for html,w,h,out in [(ogp,1200,630,"site/tarot/images/ogp.png"),(ig,1080,1350,"docs/assets/instagram/tarot_01.png")]:
        pg.set_viewport_size({"width":w,"height":h}); pg.set_content(f"<style>{CSS}</style>{html}"); pg.wait_for_timeout(300)
        pg.screenshot(path=out); print(out)
    b.close()
