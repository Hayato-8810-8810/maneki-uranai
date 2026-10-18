# 「来週をのぞく、3つの占い」表紙（1080×1350）を作る
# 使い方：python3 docs/tools/make_weekly_cover.py 出力ファイル
from playwright.sync_api import sync_playwright
import base64, os, sys
out = sys.argv[1]
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
brand = b64("site/images/brand.webp")
charas = "".join(f'<img src="data:image/webp;base64,{b64(f"site/suuhi/images/chara_{n}.webp")}">' for n in range(1, 10))
auras = [("#C8324B","#FF6F86"),("#D9668F","#FFA3C2"),("#D98A2B","#FFC46B"),("#2E9C7A","#6FE0B8"),("#C9CDE0","#FFFFFF"),("#3B4FC4","#7F92FF"),("#8A4FD8","#C79BFF"),("#9AA3B5","#DDE3F0")]
orbs = "".join(f'<i style="--c:{c};--g:{g}"></i>' for c, g in auras)
fuda = "".join(f'<i style="--c:{c};--g:{g}"></i>' for c, g in [("#463656","#9478A2"),("#B8661A","#E6A238"),("#2B4A94","#7698DC"),("#363B75","#7A82C4"),("#2A7F53","#6FBF90")])
html = f'''<style>
*{{box-sizing:border-box;margin:0}}
body{{font-family:"Noto Sans CJK JP",sans-serif}}
.cv{{width:1080px;height:1350px;position:relative;overflow:hidden;color:#EDE8F7;padding:96px 80px;
 background:radial-gradient(90% 55% at 50% 0%,#3A2A6B 0%,transparent 70%),linear-gradient(180deg,#1B1436,#0E0A1F)}}
.serif{{font-family:"Noto Serif CJK JP",serif;font-weight:700}}
.ey{{color:#E2C47E;font-weight:700;letter-spacing:.22em;font-size:28px;text-align:center}}
h1{{font-size:78px;line-height:1.35;text-align:center;margin-top:14px;color:#F4EEDD}}
.sub{{text-align:center;color:#CFC3EE;font-size:30px;margin-top:14px}}
.row{{margin-top:40px;border-radius:24px;padding:26px 30px;display:flex;flex-direction:column;gap:14px}}
.row h2{{font-size:38px;display:flex;align-items:baseline;gap:16px}}
.row h2 small{{font-family:"Noto Sans CJK JP",sans-serif;font-weight:700;font-size:22px;opacity:.85}}
.r1{{background:#F6F4FA;color:#221C3A}} .r1 small{{color:#5E3A93}}
.r2{{background:rgba(255,255,255,.06);border:1px solid rgba(226,196,126,.35)}} .r2 small{{color:#E2C47E}}
.r3{{background:linear-gradient(180deg,#FFFCF4,#F7F1E3);color:#2A2118}} .r3 small{{color:#B93A24}}
.ch{{display:flex;gap:6px}} .ch img{{width:84px;height:84px;border-radius:50%}}
.ob{{display:flex;gap:18px}} .ob i{{width:60px;height:60px;border-radius:50%;background:radial-gradient(circle at 40% 35%,var(--g),var(--c) 70%);box-shadow:0 0 18px var(--c)}}
.fd{{display:flex;gap:14px}} .fd i{{width:56px;height:90px;border-radius:8px;background:radial-gradient(circle at 50% 46%,var(--g),var(--c) 72%);box-shadow:0 3px 8px rgba(60,40,10,.3)}}
.foot{{position:absolute;left:80px;right:80px;bottom:64px;display:flex;justify-content:space-between;align-items:center;font-size:26px;color:#CFC3EE}}
.foot span{{display:flex;align-items:center;gap:14px}} .foot img{{width:56px;height:56px;border-radius:50%}} .foot b{{color:#E2C47E}}
</style>
<div class="cv">
 <p class="ey">SUNDAY NIGHT</p>
 <h1 class="serif">来週をのぞく、<br>3つの占い</h1>
 <p class="sub">ぜんぶ無料。1分あればできます</p>
 <div class="row r1"><h2 class="serif">仕事とお金の数秘診断<small>生年月日で9匹のどれかに</small></h2><div class="ch">{charas}</div></div>
 <div class="row r2"><h2 class="serif">魂の色診断<small>8つの問いで、あなたの色</small></h2><div class="ob">{orbs}</div></div>
 <div class="row r3"><h2 class="serif">福めくりタロット<small>毎朝1枚、今日のヒント</small></h2><div class="fd">{fuda}</div></div>
 <div class="foot"><span><img src="data:image/webp;base64,{brand}">まねき占い堂</span><b>プロフィールのリンクから</b></div>
</div>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.set_content(html); pg.wait_for_timeout(300)
    pg.locator(".cv").screenshot(path=out); b.close()
print("ok")
