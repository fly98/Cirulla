#!/usr/bin/env python3
"""
Genera il mazzo francese nello stile del burraco di riferimento:
colonna sinistra con valore grande e seme grande sotto, pannello avorio a destra
con i pips (o la figura per J/Q/K). Tutto disegnato qui: nessuna dipendenza da
set esterni tranne l'arte delle figure, presa dal set CC0 di Dmitry Fomin.

Uscita: WebP 200x280 in webp/.
"""
import io, os, glob, math
import cairosvg
from PIL import Image, ImageDraw, ImageFont

S = 4                                  # supersampling
W, H = 200 * S, 280 * S

ROSSO = (198, 32, 40)
NERO  = (26, 26, 26)
AVORIO = (246, 237, 203)
BORDO_PANNELLO = (90, 84, 62)

FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(px): return ImageFont.truetype(FB, int(px))

SEMI = {'s': '\u2660', 'h': '\u2665', 'd': '\u2666', 'c': '\u2663'}
COLORE = {'s': NERO, 'h': ROSSO, 'd': ROSSO, 'c': NERO}
NOMI = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
def rk(r): return NOMI.get(r, str(r))

# ---- geometria (frazioni della carta) ----
# Valori calibrati misurando il 9 di fiori del mazzo di riferimento:
# valore alto 0,251 H · seme grande 0,211 H · seme piccolo 0,099 H · pannello da (0,375; 0,243).
PAN = (0.375, 0.243, 0.952, 0.950)     # pannello avorio: x0,y0,x1,y1
RANK_C = (0.184, 0.156)                # centro del valore grande
RANK_PX = 0.335
SUIT_BIG_C = (0.186, 0.413)            # centro del seme grande
SUIT_BIG_PX = 0.216
SUIT_SM_C = (0.461, 0.093)             # seme piccolo in alto
SUIT_SM_PX = 0.101


def testo(d, xy, s, px, col, ancora='mm'):
    d.text((xy[0] * W, xy[1] * H), s, font=font(px * H), fill=col, anchor=ancora)


def pip(im, x, y, alt, seme, col, giu=False):
    """Disegna un seme centrato in (x,y), alto `alt` px, eventualmente capovolto."""
    f = font(alt * 1.34)
    t = Image.new('RGBA', (int(alt * 2.2), int(alt * 2.2)), (0, 0, 0, 0))
    ImageDraw.Draw(t).text((t.width / 2, t.height / 2), SEMI[seme], font=f,
                           fill=col + (255,), anchor='mm')
    if giu:
        t = t.rotate(180)
    im.alpha_composite(t, (int(x - t.width / 2), int(y - t.height / 2)))


# Disposizione dei pips dentro il pannello, in coordinate relative (0..1).
# Le carte alte hanno le file inferiori capovolte, come nei mazzi veri.
COLS = {'L': 0.26, 'C': 0.5, 'R': 0.74}
LAYOUT = {
    1:  [('C', .50, 1.9)],
    2:  [('C', .16), ('C', .84)],
    3:  [('C', .16), ('C', .50), ('C', .84)],
    4:  [('L', .16), ('R', .16), ('L', .84), ('R', .84)],
    5:  [('L', .16), ('R', .16), ('C', .50), ('L', .84), ('R', .84)],
    6:  [('L', .16), ('R', .16), ('L', .50), ('R', .50), ('L', .84), ('R', .84)],
    7:  [('L', .16), ('R', .16), ('C', .33), ('L', .50), ('R', .50), ('L', .84), ('R', .84)],
    8:  [('L', .16), ('R', .16), ('C', .33), ('L', .50), ('R', .50), ('C', .67), ('L', .84), ('R', .84)],
    9:  [('L', .14), ('R', .14), ('L', .38), ('R', .38), ('C', .50),
         ('L', .62), ('R', .62), ('L', .86), ('R', .86)],
    10: [('L', .14), ('R', .14), ('L', .38), ('R', .38), ('C', .28),
         ('L', .62), ('R', .62), ('C', .72), ('L', .86), ('R', .86)],
}

_figure = {}
def figura(r, s):
    """Miniatura della figura dal set CC0 di Fomin, ritagliata sull'arte."""
    key = (r, s)
    if key in _figure: return _figure[key]
    png = cairosvg.svg2png(url='carte/%s%s.svg' % (rk(r), s), output_width=520, output_height=780)
    im = Image.open(io.BytesIO(png)).convert('RGBA')
    im = im.crop((int(.14 * im.width), int(.10 * im.height),
                  int(.86 * im.width), int(.90 * im.height)))
    _figure[key] = im
    return im


def cornice(r, s):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([2 * S, 2 * S, W - 2 * S, H - 2 * S], radius=9 * S,
                        fill=(255, 255, 255, 255), outline=NERO + (255,), width=int(1.6 * S))
    col = COLORE[s]

    # pannello avorio
    px0, py0, px1, py1 = (PAN[0] * W, PAN[1] * H, PAN[2] * W, PAN[3] * H)
    d.rectangle([px0, py0, px1, py1], fill=AVORIO + (255,),
                outline=BORDO_PANNELLO + (255,), width=max(1, int(.9 * S)))

    # colonna sinistra: valore grande, seme grande sotto
    px = RANK_PX * (0.74 if r == 10 else 1.0)          # "10" ha due cifre
    # la J ha una discendente: rimpicciolita e alzata, altrimenti tocca il seme sotto
    c_rank = RANK_C if r != 11 else (RANK_C[0], RANK_C[1] - 0.022)
    testo(d, c_rank, rk(r), px * (0.90 if r == 11 else 1.0), col + (255,))
    pip(im, SUIT_BIG_C[0] * W, SUIT_BIG_C[1] * H, SUIT_BIG_PX * H, s, col)
    pip(im, SUIT_SM_C[0] * W, SUIT_SM_C[1] * H, SUIT_SM_PX * H, s, col)

    # contenuto del pannello
    if r in (11, 12, 13):
        fig = figura(r, s)
        bw, bh = int(px1 - px0) - 2 * S, int(py1 - py0) - 2 * S
        k = min(bw / fig.width, bh / fig.height)
        fig = fig.resize((max(1, int(fig.width * k)), max(1, int(fig.height * k))), Image.LANCZOS)
        im.alpha_composite(fig, (int(px0 + (px1 - px0 - fig.width) / 2),
                                 int(py0 + (py1 - py0 - fig.height) / 2)))
    else:
        alt = (py1 - py0) * (0.30 if r == 1 else 0.155)
        for spec in LAYOUT[r]:
            cx, ry = spec[0], spec[1]
            scala = spec[2] if len(spec) > 2 else 1.0
            x = px0 + COLS[cx] * (px1 - px0)
            y = py0 + ry * (py1 - py0)
            pip(im, x, y, alt * scala, s, col, giu=(ry > 0.55 and r > 3))
    return im


def jolly(rosso):
    col = ROSSO if rosso else NERO
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([2 * S, 2 * S, W - 2 * S, H - 2 * S], radius=9 * S,
                        fill=(255, 255, 255, 255), outline=NERO + (255,), width=int(1.6 * S))
    px0, py0, px1, py1 = (PAN[0] * W, PAN[1] * H, PAN[2] * W, PAN[3] * H)
    d.rectangle([px0, py0, px1, py1], fill=AVORIO + (255,),
                outline=BORDO_PANNELLO + (255,), width=max(1, int(.9 * S)))
    # colonna: "JLY" e una stella
    d.text((RANK_C[0] * W, RANK_C[1] * H), '\u2605', font=font(.30 * H),
           fill=col + (255,), anchor='mm')
    d.text((SUIT_BIG_C[0] * W, SUIT_BIG_C[1] * H), 'JOLLY', font=font(.066 * H),
           fill=col + (255,), anchor='mm')
    d.text((SUIT_SM_C[0] * W, SUIT_SM_C[1] * H), '\u2605', font=font(.13 * H),
           fill=col + (255,), anchor='mm')
    # pannello: jester stilizzato
    cx, cy = (px0 + px1) / 2, (py0 + py1) / 2
    rr = (px1 - px0) * .30
    d.ellipse([cx - rr, cy - rr * .85, cx + rr, cy + rr * 1.05], fill=(255, 255, 255, 255),
              outline=NERO + (255,), width=int(1.2 * S))
    for k, off in enumerate((-1, 0, 1)):
        x = cx + off * rr * .78
        d.polygon([(x - rr * .42, cy - rr * .72), (x, cy - rr * 1.75), (x + rr * .42, cy - rr * .72)],
                  fill=col + (255,), outline=NERO + (255,))
    d.ellipse([cx - rr * .95, cy - rr * .95, cx + rr * .95, cy - rr * .45],
              fill=col + (255,), outline=NERO + (255,), width=int(1.0 * S))
    for off in (-.38, .38):
        d.ellipse([cx + off * rr - rr * .13, cy - rr * .22, cx + off * rr + rr * .13, cy + rr * .06],
                  fill=NERO + (255,))
    d.arc([cx - rr * .5, cy - rr * .1, cx + rr * .5, cy + rr * .78], 20, 160,
          fill=NERO + (255,), width=int(1.6 * S))
    return im


def dorso():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([2 * S, 2 * S, W - 2 * S, H - 2 * S], radius=9 * S,
                        fill=(255, 255, 255, 255), outline=NERO + (255,), width=int(1.6 * S))
    inner = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    di = ImageDraw.Draw(inner)
    di.rectangle([0, 0, W, H], fill=(122, 31, 43, 255))
    for i in range(-H, W + H, 14 * S):
        di.line([(i, 0), (i + H, H)], fill=(93, 22, 32, 255), width=6 * S)
    maschera = Image.new('L', (W, H), 0)
    ImageDraw.Draw(maschera).rounded_rectangle(
        [7 * S, 7 * S, W - 7 * S, H - 7 * S], radius=6 * S, fill=255)
    im.paste(inner, (0, 0), maschera)
    d.rounded_rectangle([7 * S, 7 * S, W - 7 * S, H - 7 * S], radius=6 * S,
                        outline=(242, 226, 200, 255), width=int(1.8 * S))
    return im


def salva(im, nome):
    im = im.resize((200, 280), Image.LANCZOS)
    sfondo = Image.new('RGBA', im.size, (255, 255, 255, 0))
    sfondo.alpha_composite(im)
    sfondo.save('webp/%s.webp' % nome, 'WEBP', quality=90, method=6)


if __name__ == '__main__':
    os.makedirs('webp', exist_ok=True)
    for f in glob.glob('webp/*.webp'): os.remove(f)
    n = 0
    for s in 'shdc':
        for r in range(1, 14):
            salva(cornice(r, s), rk(r) + s); n += 1
    salva(jolly(True), 'JK-r'); salva(jolly(False), 'JK-b'); salva(dorso(), 'BACK'); n += 3
    tot = sum(os.path.getsize(f) for f in glob.glob('webp/*.webp'))
    print('generate', n, 'carte |', round(tot / 1024, 1), 'KB')
