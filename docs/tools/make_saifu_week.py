# 数秘診断「財布の紐カレンダー」投稿画像（1080×1350×5枚）を site/suuhi/index.html の DAY から作る
# 使い方：python3 docs/tools/make_saifu_week.py 開始日(YYYY-MM-DD) 出力先フォルダ
from PIL import Image, ImageDraw, ImageFont
import datetime as dt, glob, os, re, sys

START = dt.date.fromisoformat(sys.argv[1] if len(sys.argv) > 1 else "2026-10-26")
OUT = sys.argv[2] if len(sys.argv) > 2 else "docs/assets/instagram_saifu"
os.makedirs(OUT, exist_ok=True)
SRC = open("site/suuhi/index.html", encoding="utf-8").read()

def font(path, size):
    for i in range(12):
        f = ImageFont.truetype(path, size, index=i)
        if "JP" in f.getname()[0]:
            return f
    return ImageFont.truetype(path, size)

SANS = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = (glob.glob("/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc") + glob.glob("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"))[0]
SER = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
BG = (246, 244, 250); SURF = (253, 252, 255); INK = (34, 28, 58); MUTED = (107, 101, 130); LINE = (226, 221, 238)
GOLD = (154, 110, 28); GOLDS = (243, 232, 207); PLUM = (94, 58, 147); PLUMS = (236, 228, 247)
W, H = 1080, 1350
KC = {"use": (GOLDS, GOLD, "使う"), "hold": (PLUMS, PLUM, "締める"), "tidy": (SURF, MUTED, "整える")}

# サイトの DAY をそのまま読む
DAY = {int(n): (s, k, m) for n, s, k, m in re.findall(r'(\d):\{short:"([^"]+)",k:"(\w+)",msg:"([^"]+)"\}', SRC)}
assert len(DAY) == 9

red = lambda n: n if n <= 9 else red(sum(map(int, str(n))))
ds = lambda n: sum(map(int, str(n)))
def pday(bm, bd, d):  # サイトの personalDay と同じ計算
    py = red(ds(bm) + ds(bd) + ds(d.year))
    return red(py + ds(d.month) + ds(d.day))

def ctext(d, x, y, t, f, fill):
    d.text((x - d.textlength(t, font=f) / 2, y), t, font=f, fill=fill)

def wrap(d, t, f, maxw):
    lines, cur = [], ""
    for ch in t:
        if d.textlength(cur + ch, font=f) > maxw and cur and ch not in "、。」）":
            lines.append(cur); cur = ch
        else:
            cur += ch
    return lines + [cur]

def pill(d, x, y, w, h, k, f):
    bg, fg, label = KC[k]
    d.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=bg, outline=fg if k == "tidy" else None, width=2)
    ctext(d, x + w / 2, y + (h - f.size) / 2 - 4, label, f, fg)

neko = Image.open("docs/assets/originals/maneki_neko.png").convert("RGBA"); c0 = neko.size[0] // 2
neko = neko.crop((c0 - 606, c0 - 606, c0 + 606, c0 + 606)).resize((64, 64), Image.LANCZOS)
m = Image.new("L", (128, 128), 0); ImageDraw.Draw(m).ellipse((0, 0, 127, 127), fill=255); neko.putalpha(m.resize((64, 64), Image.LANCZOS))
def base():
    I = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(I)
    d.rectangle((0, H - 150, W, H), fill=SURF); d.line((0, H - 150, W, H - 150), fill=LINE, width=2)
    I.paste(neko, (80, H - 108), neko); d.text((160, H - 100), "まねき占い堂", font=font(SER, 32), fill=INK)
    t = "仕事とお金の数秘診断｜プロフィールのリンクから"; f = font(SANS, 22); d.text((W - 80 - d.textlength(t, font=f), H - 90), t, font=f, fill=GOLD)
    return I, d

WD = "月火水木金土日"
days = [START + dt.timedelta(days=i) for i in range(7)]

# 1 表紙：同じ1週間でも、人によってちがう（例2人分を実際に計算）
I, d = base()
ctext(d, W / 2, 80, "財布の紐カレンダー", font(SANS, 30), GOLD)
ctext(d, W / 2, 140, "来週、財布を", font(SER, 76), INK)
ctext(d, W / 2, 235, "開いていい日は？", font(SER, 76), INK)
ctext(d, W / 2, 352, "同じ1週間でも、生年月日でこんなにちがう", font(SANS, 30), PLUM)
for row, (bm, bd) in enumerate([(4, 12), (8, 3)]):
    y0 = 450 + row * 330
    d.rounded_rectangle((70, y0, W - 70, y0 + 290), radius=24, fill=SURF, outline=LINE, width=2)
    d.text((110, y0 + 28), f"例{'AB'[row]}：{bm}月{bd}日生まれの人", font=font(SANS, 30), fill=INK)
    cw = (W - 180) / 7
    for i, day in enumerate(days):
        x = 90 + cw * i
        ctext(d, x + cw / 2, y0 + 96, f"{day.month}/{day.day}", font(REG, 24), MUTED)
        ctext(d, x + cw / 2, y0 + 128, WD[day.weekday()], font(SANS, 26), INK)
        pill(d, int(x + 8), y0 + 190, int(cw - 16), 60, DAY[pday(bm, bd, day)][1], font(SANS, 24))
ctext(d, W / 2, 1125, "使う日・締める日・整める日の意味は →".replace("整める", "整える"), font(SANS, 30), INK)
I.save(f"{OUT}/saifu_1.png", optimize=True)

# 2〜4 日の種類ごと
for no, (k, title, sub) in enumerate([("use", "使っていい日", "財布を開くなら、この日"), ("hold", "締める日", "買う前に、ひと呼吸"), ("tidy", "整える日", "出すより、片づける")], 2):
    I, d = base()
    ctext(d, W / 2, 80, "財布の紐カレンダー", font(SANS, 30), GOLD)
    pill(d, W // 2 - 100, 140, 200, 68, k, font(SANS, 34))
    ctext(d, W / 2, 228, title, font(SER, 64), INK)
    ctext(d, W / 2, 322, sub, font(SANS, 28), MUTED)
    nums = [n for n in range(1, 10) if DAY[n][1] == k]
    fb = font(REG, 26)
    tot = sum(80 + len(wrap(d, DAY[n][2], fb, W - 300)) * 42 + 16 for n in nums) - 16
    y = 395 + max(0, (1110 - 395 - tot) // 2)
    for n in nums:
        short, _, msg = DAY[n]
        body = wrap(d, msg, fb, W - 300)
        h = 80 + len(body) * 42
        d.rounded_rectangle((70, y, W - 70, y + h), radius=22, fill=SURF, outline=LINE, width=2)
        bg, fg, _ = KC[k]
        d.ellipse((100, y + 24, 164, y + 88), fill=bg, outline=fg, width=2)
        ctext(d, 132, y + 28, str(n), font(SER, 40), fg)
        d.text((196, y + 20), short, font=font(SANS, 32), fill=INK)
        for j, line in enumerate(body):
            d.text((196, y + 72 + j * 42), line, font=fb, fill=MUTED)
        y += h + 16
    ctext(d, W / 2, 1140, "数字は、生年月日と日付から計算した「個人日数」", font(REG, 22), MUTED)
    I.save(f"{OUT}/saifu_{no}.png", optimize=True)

# 5 しめ：自分のカレンダーへ
I, d = base()
ctext(d, W / 2, 80, "財布の紐カレンダー", font(SANS, 30), GOLD)
ctext(d, W / 2, 140, "あなたの1か月は、", font(SER, 70), INK)
ctext(d, W / 2, 235, "どんな色？", font(SER, 70), INK)
# 例A の今月カレンダー（実計算）
y0, x0, cs = 450, 120, 120
nx = START + dt.timedelta(days=7); mon = dt.date(nx.year, nx.month, 1)
d.text((x0, y0 - 60), f"例：4月12日生まれの人の{mon.month}月", font=font(SANS, 28), fill=MUTED)
for i, w in enumerate("日月火水木金土"):
    ctext(d, x0 + cs * i + cs / 2 - 10, y0, w, font(SANS, 24), MUTED)
first = (mon.weekday() + 1) % 7; ndays = ((mon.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - mon).days
for dd in range(1, ndays + 1):
    p = first + dd - 1; cx = x0 + cs * (p % 7); cy = y0 + 50 + 92 * (p // 7)
    bg, fg, _ = KC[DAY[pday(4, 12, mon.replace(day=dd))][1]]
    d.rounded_rectangle((cx + 4, cy, cx + cs - 24, cy + 80), radius=14, fill=bg, outline=fg if bg == SURF else None, width=2)
    ctext(d, cx + cs / 2 - 10, cy + 18, str(dd), font(SANS, 30), fg)
ctext(d, W / 2, 1060, "生年月日を入れるだけで、今日・7日間・1か月分", font(SANS, 30), INK)
ctext(d, W / 2, 1110, "入力は画面の中だけ。送信・保存はしません", font(REG, 24), MUTED)
I.save(f"{OUT}/saifu_5.png", optimize=True)
print("ok")
