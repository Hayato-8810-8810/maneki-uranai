# 「札の図鑑」Instagram・Threads用の4枚（1080×1350）を site/tarot/index.html の札から作る
# 使い方：python3 docs/tools/make_tarot_zukan.py 出力先フォルダ   （Playwrightが必要）
from playwright.sync_api import sync_playwright
import base64, os, sys

out = sys.argv[1] if len(sys.argv) > 1 else "docs/assets/instagram_tarot_zukan"
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

CSS += '.grid{display:grid;grid-template-columns:repeat(8,96px);gap:16px 14px;margin-top:50px}\n.grid .cell{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:16px;font-weight:700;color:#2A2118}\n.grid .lock .card{background:#E3D8C0;box-shadow:none;color:#8C8070}\n.grid .lock{color:#8C8070;font-weight:400}\n.trio{display:flex;gap:40px;margin-top:70px}\n.trio .it{width:280px;display:flex;flex-direction:column;align-items:center;text-align:center}\n.trio .nm2{font-family:"Noto Serif CJK JP",serif;font-weight:700;font-size:44px;margin-top:26px}\n.trio .ct{font-size:26px;line-height:1.6;color:#6E6252;margin-top:10px}\n'

GOT = [0, 8, 13, 17, 18, 19, 21]   # 表紙の「図鑑のイメージ」に表で出す札（見本）
SETS = [("夜空の3枚", "星・月・太陽", [17, 18, 19]), ("はじまりと、めぐりと、完成", "愚者・運命の輪・世界", [0, 10, 21])]
ROMAN = ["0","I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX","XXI"]
avg = round(22 * sum(1 / k for k in range(1, 23)))

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.goto("file://" + os.path.abspath("site/tarot/index.html"))
    faces = pg.evaluate("CARDS.map((c,i)=>faceHTML(i))")
    data = pg.evaluate("CARDS.map(c=>[c.name,c.catch])")
    pages = []
    cells = ""
    for i in range(22):
        if i in GOT:
            cells += f'<div class="cell">{one(faces[i], 96, 8)}<span>{data[i][0]}</span></div>'
        else:
            cells += f'<div class="cell lock"><div class="card" style="width:96px;font-size:26px;justify-content:center">？</div><span>{ROMAN[i]}</span></div>'
    pages.append(f'''<div class="cv" style="padding-top:96px">
      <p class="eyebrow" style="font-size:28px">COLLECTION</p>
      <p class="serif" style="font-size:76px;line-height:1.35;text-align:center;margin-top:14px">1日1枚、<br>図鑑がうまっていく。</p>
      <div class="grid">{cells}</div>
      <p style="font-size:24px;color:#8A6212;margin-top:30px">図鑑のイメージ（7 / 22 枚）</p>
      {foot}</div>''')
    for title, sub, idx in SETS:
        its = "".join(f'<div class="it">{one(faces[i], 240, 19)}<p class="nm2">{data[i][0]}</p><p class="ct">{data[i][1].replace('、', '、<br>')}</p></div>' for i in idx)
        pages.append(f'''<div class="cv">
          <p class="eyebrow" style="font-size:26px">22枚のなかには</p>
          <p class="serif" style="font-size:66px;line-height:1.35;text-align:center;margin-top:16px">{title}</p>
          <p style="font-size:30px;color:#6E6252;margin-top:12px">{sub}</p>
          <div class="trio">{its}</div>
          {foot}</div>''')
    pages.append(f'''<div class="cv" style="justify-content:center">
      <p style="font-size:34px;color:#6E6252">どの札をタップしても、22枚から1枚</p>
      <p class="serif" style="font-size:66px;line-height:1.5;text-align:center;margin-top:24px">ぜんぶそろうまで、<br>計算上の平均は</p>
      <p class="serif" style="font-size:150px;line-height:1.2;color:#B93A24">約{avg}日</p>
      <p style="font-size:30px;line-height:1.8;color:#6E6252;text-align:center;margin-top:24px">同じ札がまた出る日もあるから、<br>22日ではそろいません。</p>
      <p style="display:inline-block;margin-top:44px;background:#B93A24;color:#fff;font-weight:700;font-size:34px;border-radius:999px;padding:18px 48px">プロフィールのリンクから</p>
      <p style="font-size:22px;color:#8A6212;margin-top:30px">引いた札の記録は、あなたの端末の中だけ。送信しません</p>
      {foot}</div>''')
    for k, html in enumerate(pages, 1):
        pg.set_content(f"<style>{CSS}</style>{html}")
        pg.wait_for_timeout(200)
        pg.locator(".cv").screenshot(path=f"{out}/tarot_zukan_{k}.png")
    b.close()
print("ok")
