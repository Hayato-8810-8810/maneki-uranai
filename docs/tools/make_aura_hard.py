# 魂の色診断「すれ違いやすい色とコツ」投稿画像（1080×1350）を、site/aura/index.html の PAIRS から作る
# 使い方：python3 docs/tools/make_aura_hard.py 出力先フォルダ
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import glob, math, os, random, re, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "docs/assets/instagram_aura_hard"
os.makedirs(OUT, exist_ok=True)
SRC = open("site/aura/index.html", encoding="utf-8").read()

def font(path, size):
    for i in range(12):
        f = ImageFont.truetype(path, size, index=i)
        if "JP" in f.getname()[0]:
            return f
    return ImageFont.truetype(path, size)

SANS = glob.glob("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")[0]
SER = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
REG = (glob.glob("/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc") + glob.glob("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"))[0]
SERR = (glob.glob("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc") + [SER])[0]
CREAM = (244, 238, 221); SOFT = (207, 195, 238); GOLD = (242, 201, 92)
W, H = 1080, 1350
hx = lambda h: tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

COL = {"crimson": ("深紅", "#C8324B", "#FF6F86"), "rose": ("薔薇", "#D9668F", "#FFA3C2"), "amber": ("琥珀", "#D98A2B", "#FFC46B"),
       "jade": ("翡翠", "#2E9C7A", "#6FE0B8"), "moon": ("月白", "#C9CDE0", "#FFFFFF"), "indigo": ("藍", "#3B4FC4", "#7F92FF"),
       "violet": ("菫", "#8A4FD8", "#C79BFF"), "silver": ("銀灰", "#9AA3B5", "#DDE3F0")}
RING = ["crimson", "moon", "rose", "silver", "amber", "indigo", "violet", "jade"]

def pair(a, b):
    m = re.search(r'"' + a + r'\|' + b + r'":\[(.*?)\]', SRC) or re.search(r'"' + b + r'\|' + a + r'":\[(.*?)\]', SRC)
    return re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))

def night(seed):
    random.seed(seed)
    g = Image.new("RGB", (W, H), (14, 10, 31)); d = ImageDraw.Draw(g)
    d.ellipse((W/2-700, H*0.40-700, W/2+700, H*0.40+700), fill=(58, 42, 107))
    I = g.filter(ImageFilter.GaussianBlur(260)); d = ImageDraw.Draw(I)
    for _ in range(110):
        x, y = random.randint(0, W), random.randint(0, H); r = random.choice([1, 1, 1, 2]); a = random.randint(90, 230)
        d.ellipse((x-r, y-r, x+r, y+r), fill=(a, a, min(255, a+15)))
    return I

def orb(I, cx, cy, r, c, g):
    col = Image.new("RGB", (W, H), hx(c))
    a = Image.new("L", (W, H), 0); ImageDraw.Draw(a).ellipse((cx-r*1.9, cy-r*1.9, cx+r*1.9, cy+r*1.9), fill=120)
    I.paste(col, (0, 0), a.filter(ImageFilter.GaussianBlur(r*0.8)))
    S = 4; size = int(r*2*S)
    core = Image.new("RGB", (size, size)); dc = ImageDraw.Draw(core)
    for k in range(60, 0, -1):
        t = k/60; rr = size/2*t
        cc = tuple(int(hx(g)[i]*(1-t)**1.2 + hx(c)[i]*(1-(1-t)**1.2)) for i in range(3))
        dc.ellipse((size/2-rr, size/2-rr, size/2+rr, size/2+rr), fill=cc)
    mask = Image.new("L", (size, size), 0); ImageDraw.Draw(mask).ellipse((0, 0, size-1, size-1), fill=255)
    I.paste(core.resize((int(r*2), int(r*2)), Image.LANCZOS), (int(cx-r), int(cy-r)), mask.resize((int(r*2), int(r*2)), Image.LANCZOS))

def ctext(d, x, y, t, f, fill):
    w = d.textlength(t, font=f); d.text((x-w/2, y), t, font=f, fill=fill)

def wrap(d, t, f, maxw):
    lines, cur = [], ""
    for ch in t:
        if d.textlength(cur+ch, font=f) > maxw and cur and ch not in "、。」）":
            lines.append(cur); cur = ch
        else:
            cur += ch
    return lines + [cur]

neko = Image.open("docs/assets/originals/maneki_neko.png").convert("RGBA"); c0 = neko.size[0]//2
neko = neko.crop((c0-606, c0-606, c0+606, c0+606)).resize((64, 64), Image.LANCZOS)
m = Image.new("L", (128, 128), 0); ImageDraw.Draw(m).ellipse((0, 0, 127, 127), fill=255); neko.putalpha(m.resize((64, 64), Image.LANCZOS))
def footer(I, d):
    I.paste(neko, (80, H-110), neko); d.text((160, H-102), "まねき占い堂", font=font(SER, 32), fill=CREAM)
    t = "魂の色診断｜プロフィールのリンクから"; f = font(SANS, 24); d.text((W-80-d.textlength(t, font=f), H-94), t, font=f, fill=GOLD)

# 1 表紙：すれ違いやすい4組
HARD = [("crimson", "silver"), ("rose", "violet"), ("moon", "amber"), ("indigo", "jade")]
I = night(5)
pos = [(W/2-235, 560), (W/2+235, 560), (W/2-235, 900), (W/2+235, 900)]
for (a, b), (x, y) in zip(HARD, pos):
    orb(I, x-62, y, 56, COL[a][1], COL[a][2]); orb(I, x+62, y, 56, COL[b][1], COL[b][2])
d = ImageDraw.Draw(I)
for (a, b), (x, y) in zip(HARD, pos):
    ctext(d, x, y+82, f"{COL[a][0]} × {COL[b][0]}", font(SER, 38), CREAM)
    ctext(d, x, y+138, pair(a, b)[0], font(SANS, 24), SOFT)
ctext(d, W/2, 90, "魂の色診断", font(SANS, 30), SOFT)
ctext(d, W/2, 150, "なぜか、あの人とは", font(SER, 70), CREAM)
ctext(d, W/2, 240, "すれ違う。", font(SER, 70), CREAM)
ctext(d, W/2, 345, "相性が悪いのではなく、大切にするものがちがうだけ", font(SANS, 28), GOLD)
ctext(d, W/2, 1120, "すれ違うときと、うまくいくコツ →", font(SANS, 30), CREAM)
footer(I, d); I.save(f"{OUT}/aura_hard_1.png", optimize=True)

# 2〜5 組み合わせごと
for no, (a, b) in enumerate(HARD, 2):
    name, what, good, care, tip = pair(a, b)
    I = night(40+no)
    orb(I, W/2-150, 330, 110, COL[a][1], COL[a][2]); orb(I, W/2+150, 330, 110, COL[b][1], COL[b][2])
    d = ImageDraw.Draw(I)
    ctext(d, W/2, 80, "すれ違いやすい色", font(SANS, 30), GOLD)
    ctext(d, W/2, 300, "×", font(SER, 48), CREAM)
    ctext(d, W/2-150, 460, COL[a][0], font(SER, 44), CREAM); ctext(d, W/2+150, 460, COL[b][0], font(SER, 44), CREAM)
    ctext(d, W/2, 545, f"― {name} ―", font(SER, 54), CREAM)
    y = 650
    for label, body in [("すれ違うとき", care), ("うまくいくコツ", tip)]:
        d.text((110, y), label, font=font(SANS, 28), fill=GOLD); y += 48
        for line in wrap(d, body, font(SERR, 36), W-220):
            d.text((110, y), line, font=font(SERR, 36), fill=CREAM); y += 58
        y += 34
    footer(I, d); I.save(f"{OUT}/aura_hard_{no}.png", optimize=True)
print("ok")
