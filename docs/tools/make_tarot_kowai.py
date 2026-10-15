# 「怖い札ほど、やさしい」Instagram・Threads用の5枚（1080×1350）を site/tarot/index.html の札から作る
# 使い方：python3 docs/tools/make_tarot_kowai.py 出力先フォルダ   （Playwrightが必要）
from playwright.sync_api import sync_playwright
import base64, os, sys

out = sys.argv[1] if len(sys.argv) > 1 else "docs/assets/instagram_tarot_kowai"
os.makedirs(out, exist_ok=True)
brand = base64.b64encode(open("site/images/brand.webp", "rb").read()).decode()

CSS = '''
*{box-sizing:border-box;margin:0}
body{font-family:"Noto Sans CJK JP",sans-serif;color:#2A2118}
.serif{font-family:"Noto Serif CJK JP",serif;font-weight:700}
.cv{position:relative;overflow:hidden;width:1080px;height:1350px;background:radial-gradient(120% 60% at 50% 0%,#FFF8E6 0%,transparent 70%),#F7F1E3;display:flex;flex-direction:column;align-items:center;padding:110px 90px 96px}
.cv::after{content:"";position:absolute;inset:28px;border:3px solid #B93A24;border-radius:28px;pointer-events:none}
.card{position:relative;aspect-ratio:5/8;border-radius:.6em;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:.9em .5em .8em;color:#FFF6DC;
 font-family:"Noto Serif CJK JP",serif;font-weight:700;background:radial-gradient(circle at 50% 46%,var(--g) 0%,var(--c) 72%);box-shadow:0 .3em .9em rgba(60,40,10,.3);flex:none}
.card::after{content:"";position:absolute;inset:.35em;border:1px solid rgba(255,246,220,.6);border-radius:.4em}
.card .num{font-size:1.05em;letter-spacing:.12em;line-height:1}.card svg{width:80%}.card .nm{font-size:1.15em;letter-spacing:.14em;line-height:1.2;white-space:nowrap}
.fan{position:relative;flex:none}.fan .card{position:absolute;top:0;left:0}
.eyebrow{color:#8A6212;font-weight:700;letter-spacing:.22em}
.foot{position:absolute;left:90px;right:90px;bottom:76px;display:flex;align-items:center;justify-content:space-between;color:#6E6252;font-size:26px}
.foot span{display:flex;align-items:center;gap:14px}.foot img{border-radius:50%}
.foot b{color:#B93A24}
.row{display:flex;gap:16px;width:100%;margin-top:28px}
.box{flex:1;border-radius:20px;padding:22px 26px}
.box .k{font-size:22px;font-weight:700;letter-spacing:.08em}
.box .v{font-size:30px;font-weight:700;margin-top:6px;line-height:1.45}
.myth{background:#EDE6D6;color:#6E6252}.myth .v{text-decoration:line-through;text-decoration-color:#B93A24;text-decoration-thickness:3px}
.real{background:#B93A24;color:#fff}
.txt{width:100%;margin-top:26px;font-size:28px;line-height:1.75;background:#FFFCF4;border:2px solid #E3D8C0;border-radius:20px;padding:24px 30px}
.txt b{display:block;color:#8A6212;font-size:22px;letter-spacing:.08em;margin-bottom:4px}
'''

def fan(faces, w, fs):
    rot = [-14, 0, 14]; dx = [-0.62, 0, 0.62]; dy = [0.06, 0, 0.06]
    s = ""
    for k, f in enumerate(faces):
        s += f.replace('class="card ', 'class="card x').replace('style="', f'style="width:{w}px;font-size:{fs}px;transform:translate({dx[k]*w}px,{dy[k]*w}px) rotate({rot[k]}deg);z-index:{2 if k==1 else 1};', 1)
    return f'<div class="fan" style="width:{w}px;height:{w*1.6}px">{s}</div>'

def one(face, w, fs):
    return face.replace('style="', f'style="width:{w}px;font-size:{fs}px;', 1)

foot = f'<div class="foot"><span><img src="data:image/webp;base64,{brand}" width="56" height="56">まねき占い堂</span><b>福めくりタロット</b></div>'

# よく思われがちなイメージ（一般的な印象）と、サイトの札の文章
CARDS = [
    (13, "不吉・終わり"),
    (16, "災難・崩壊"),
    (15, "悪いこと・誘惑"),
]

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.goto("file://" + os.path.abspath("site/tarot/index.html"))
    faces = pg.evaluate("[13,16,15].map(i=>faceHTML(i))")
    data = pg.evaluate("[13,16,15].map(i=>CARDS[i])")
    pages = []
    # 1 表紙
    pages.append(f'''<div class="cv">
      <p class="eyebrow" style="font-size:30px">TAROT</p>
      <p class="serif" style="font-size:84px;line-height:1.35;text-align:center;margin-top:18px">怖い札ほど、<br>やさしい。</p>
      <p style="font-size:32px;color:#6E6252;margin-top:22px;text-align:center">死神・塔・悪魔の、ほんとうの読み方</p>
      <div style="margin-top:90px">{fan(faces, 250, 20)}</div>
      {foot}</div>''')
    # 2〜4 札ごと
    for (i, myth), face, d in zip(CARDS, faces, data):
        name, en, hito, kotoba, yaru = d['name'], d['en'], d['catch'], d['kotoba'], d['do']
        pages.append(f'''<div class="cv">
          <div style="display:flex;gap:44px;align-items:center;width:100%">
            {one(face, 250, 20)}
            <div><p class="eyebrow" style="font-size:24px">{en.upper()}</p>
            <p class="serif" style="font-size:92px;line-height:1.2">{name}</p>
            <p class="serif" style="font-size:36px;line-height:1.5;color:#B93A24;margin-top:10px">{hito}</p></div>
          </div>
          <div class="row"><div class="box myth"><p class="k">よく思われがち</p><p class="v">{myth}</p></div>
          <div class="box real"><p class="k">まねき占い堂の読み</p><p class="v">{hito}</p></div></div>
          <div class="txt"><b>今日のことば</b>{kotoba}</div>
          <div class="txt" style="margin-top:16px"><b>やるといいこと</b>{yaru}</div>
          {foot}</div>''')
    # 5 しめ
    pages.append(f'''<div class="cv" style="justify-content:center">
      <p class="serif" style="font-size:64px;line-height:1.5;text-align:center">あなたの今日の一枚は、<br>どの札？</p>
      <p style="font-size:32px;line-height:1.8;color:#6E6252;text-align:center;margin-top:30px">招き猫がタロットを1枚めくる<br>1日1回の無料占い</p>
      <p style="display:inline-block;margin-top:48px;background:#B93A24;color:#fff;font-weight:700;font-size:34px;border-radius:999px;padding:18px 48px">プロフィールのリンクから</p>
      <p style="font-size:24px;color:#8A6212;margin-top:40px">※タロットの一般的な意味をもとにした、まねき占い堂の読みです</p>
      {foot}</div>''')
    for k, html in enumerate(pages, 1):
        pg.set_content(f"<style>{CSS}</style>{html}")
        pg.wait_for_timeout(200)
        pg.locator(".cv").screenshot(path=f"{out}/tarot_kowai_{k}.png")
    b.close()
print("ok")
