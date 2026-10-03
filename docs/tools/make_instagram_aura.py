from playwright.sync_api import sync_playwright
import json, base64, os, math, sys
out=sys.argv[1]
brand=base64.b64encode(open("site/images/brand.webp","rb").read()).decode()
css='''
*{box-sizing:border-box;margin:0}
body{background:#000;font-family:"Noto Sans CJK JP",sans-serif}
.card{width:1080px;height:1350px;position:relative;overflow:hidden;color:#ECE7F5;display:flex;flex-direction:column;align-items:center;padding:92px 88px 84px;
 background:radial-gradient(120% 60% at 50% -5%,#2A2050 0%,transparent 60%),radial-gradient(90% 50% at 50% 108%,#1A1233 0%,transparent 60%),#0B0A14}
.card::before{content:"";position:absolute;inset:0;background-image:radial-gradient(2px 2px at 12% 18%,#fff9,transparent),radial-gradient(2px 2px at 72% 9%,#fffa,transparent),radial-gradient(3px 3px at 38% 42%,#fff5,transparent),radial-gradient(2px 2px at 88% 36%,#fff8,transparent),radial-gradient(2px 2px at 22% 74%,#fff6,transparent),radial-gradient(3px 3px at 62% 82%,#fff6,transparent),radial-gradient(2px 2px at 50% 26%,#fff5,transparent),radial-gradient(2px 2px at 8% 52%,#fff7,transparent),radial-gradient(2px 2px at 94% 66%,#fff6,transparent);background-size:520px 640px}
.card::after{content:"";position:absolute;inset:32px;border:1px solid rgba(217,183,106,.35);border-radius:24px}
.card>*{position:relative;z-index:1}
.serif{font-family:"Noto Serif CJK JP",serif;font-weight:700}
.eyebrow{color:#D9B76A;letter-spacing:.34em;font-size:26px;font-weight:700}
.orb{position:relative;border-radius:50%;flex:none}
.orb i{position:absolute;inset:-26%;border-radius:50%;background:radial-gradient(circle,var(--g) 0%,transparent 62%);opacity:.45;filter:blur(26px)}
.orb b{position:absolute;inset:0;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffffffcc 0%,transparent 22%),radial-gradient(circle at 40% 40%,var(--g) 0%,var(--c) 48%,#0B0A14 100%);box-shadow:0 0 90px var(--c),inset 0 0 60px rgba(0,0,0,.5)}
.orb u{position:absolute;inset:-11%;border-radius:50%;border:1.5px solid rgba(217,183,106,.4)}
.foot{margin-top:auto;display:flex;align-items:center;gap:16px;font-size:26px;color:#A39CBA}
.foot img{width:52px;height:52px;border-radius:50%}
.foot span{color:#D9B76A}
.q{font-size:60px;line-height:1.6;text-align:center;letter-spacing:.08em}
.sub{font-size:34px;color:#A39CBA;line-height:1.8;text-align:center}
.ring{position:relative;width:520px;height:520px;margin:56px 0 48px}
.ring .dot{position:absolute;width:92px;height:92px;margin:-46px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff9,transparent 40%),var(--c);box-shadow:0 0 36px var(--c)}
.ring .mid{position:absolute;inset:150px}
.name{font-size:112px;letter-spacing:.16em;margin-top:40px;line-height:1.2}
.en{font-family:"Noto Serif CJK JP",serif;font-style:italic;color:#D9B76A;font-size:34px;letter-spacing:.14em}
.catch{font-size:38px;line-height:1.6;text-align:center;margin-top:26px}
.box{margin-top:30px;width:100%;border:1px solid rgba(217,183,106,.28);border-radius:24px;background:rgba(255,255,255,.04);padding:30px 40px;font-size:29px;line-height:1.8;color:#D9D3E6}
.match{margin-top:26px;font-size:28px;color:#A39CBA;display:flex;align-items:center;gap:16px}
.match em{font-style:normal;color:#D9B76A}
.match .d{width:34px;height:34px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff9,transparent 40%),var(--c);box-shadow:0 0 14px var(--c)}
.pill{margin-top:44px;background:linear-gradient(180deg,#E8CC86,#C9A04E);color:#1A1408;font-weight:700;font-size:38px;border-radius:999px;padding:22px 56px}
.swipe{font-size:28px;color:#D9B76A;letter-spacing:.2em;margin-top:20px}
'''
foot=f'<div class="foot"><img src="data:image/webp;base64,{brand}"><span>まねき占い堂</span>@manekiuranai</div>'
def orb(c,g,size): return f'<div class="orb" style="width:{size}px;height:{size}px;--c:{c};--g:{g}"><i></i><u></u><b></b></div>'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1080,"height":1350})
    pg.goto("file://"+os.path.abspath("site/aura/index.html"))
    D=json.loads(pg.evaluate("JSON.stringify({C,ORDER,good:Object.fromEntries(ORDER.map(a=>[a,ORDER.filter(b=>relation(a,b)==='good')]))})"))
    C,ORDER=D["C"],D["ORDER"]
    dots="".join(f'<span class="dot" style="--c:{C[k]["c"]};left:{260+215*math.cos(-math.pi/2+i*math.pi/4):.0f}px;top:{260+215*math.sin(-math.pi/2+i*math.pi/4):.0f}px"></span>' for i,k in enumerate(ORDER))
    cards=[f'''<div class="card"><p class="eyebrow">MANEKI URANAI · AURA</p>
      <div class="ring">{dots}<div class="mid">{orb("#8A4FD8","#C79BFF",220)}</div></div>
      <p class="q serif">あなたの魂は、<br>何色ですか。</p>
      <p class="sub" style="margin-top:28px">8つの問いでわかる「魂の色診断」</p>
      <p class="swipe">8色を見る　→</p>{foot}</div>''']
    for n,k in enumerate(ORDER,1):
        c=C[k]
        m="".join(f'<span class="d" style="--c:{C[x]["c"]}"></span>{C[x]["name"]}' for x in D["good"][k])
        cards.append(f'''<div class="card"><p class="eyebrow">魂の色　{n} / 8</p>
          <div style="margin-top:64px">{orb(c["c"],c["g"],250)}</div>
          <p class="name serif">{c["name"]}</p><p class="en">{c["en"]}</p>
          <p class="catch serif">{c["catch"]}</p>
          <div class="box">{c["soul"]}</div>
          <p class="match"><em>◎ 縁が結ばれやすい色</em>{m}</p>{foot}</div>''')
    cards.append(f'''<div class="card"><p class="eyebrow">MANEKI URANAI · AURA</p>
      <div style="margin-top:110px">{orb("#3B4FC4","#C79BFF",260)}</div>
      <p class="q serif" style="margin-top:90px">あなたは、何色でしたか。</p>
      <p class="sub" style="margin-top:36px">8つの問いに答えるだけ。<br>縁の結び方と、8色との相性まで読めます。</p>
      <p class="pill">無料・約1分</p>
      <p class="sub" style="margin-top:36px;color:#ECE7F5">プロフィールのリンクから<br>「魂の色診断」へ</p>
      <p class="sub" style="font-size:24px;margin-top:28px;margin-bottom:28px">この診断はエンターテインメントです</p>{foot}</div>''')
    pg.set_content(f"<style>{css}</style>"+"".join(cards)); pg.wait_for_timeout(500)
    for i in range(len(cards)):
        el=pg.locator(".card").nth(i)
        gap=el.evaluate("e=>{const f=e.querySelector('.foot'),p=f.previousElementSibling;return Math.round(f.getBoundingClientRect().top-p.getBoundingClientRect().bottom)}")
        el.screenshot(path=f"{out}/aura_{i+1:02d}.png"); print(i+1,"gap above footer:",gap)
    b.close()
