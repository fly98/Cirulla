#!/usr/bin/env python3
"""
Icone dell'app Burraco: tre carte a ventaglio su panno verde.

Disegno: fondo verde con vignettatura, tre carte bianche ruotate a ventaglio
con angoli arrotondati e ombra, i semi in evidenza sulla carta centrale.
Nessun testo: a 60 px sulla home una scritta non si leggerebbe comunque.

Uscita in icone/: icon-burraco-180/192/512.png e icon-burraco-maskable-512.png.
"""
import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 1024                      # lato di lavoro, poi si riduce
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

VERDE_A = (24, 106, 72)
VERDE_B = (8, 52, 35)
ROSSO   = (198, 40, 46)
NERO    = (26, 26, 26)
CARTA   = (253, 251, 246)
AVORIO  = (245, 235, 200)

SEMI = {'s': '\u2660', 'h': '\u2665', 'd': '\u2666', 'c': '\u2663'}


def fondo(lato):
    """Panno verde con una luce diffusa al centro."""
    im = Image.new('RGB', (lato, lato), VERDE_B)
    d = ImageDraw.Draw(im)
    cx = cy = lato / 2
    passi = 90
    for i in range(passi, 0, -1):
        t = i / passi
        r = lato * 0.78 * t
        k = 1 - t
        col = tuple(int(VERDE_B[j] + (VERDE_A[j] - VERDE_B[j]) * (k ** 1.25)) for j in range(3))
        d.ellipse([cx - r, cy - r * 0.92, cx + r, cy + r * 0.92], fill=col)
    return im.filter(ImageFilter.GaussianBlur(lato / 90))


def carta(w, h, seme, grande=False):
    """Una carta con angoli arrotondati e il suo seme."""
    m = int(w * 0.05)
    im = Image.new('RGBA', (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([m, m, m + w, m + h], radius=int(w * 0.12), fill=CARTA + (255,))
    col = ROSSO if seme in 'hd' else NERO
    if grande:
        px0, py0 = m + w * 0.15, m + h * 0.17
        px1, py1 = m + w * 0.85, m + h * 0.83
        d.rounded_rectangle([px0, py0, px1, py1], radius=int(w * 0.06), fill=AVORIO + (255,))
        f = ImageFont.truetype(FB, int(h * 0.42))
        d.text(((px0 + px1) / 2, (py0 + py1) / 2), SEMI[seme], font=f, fill=col + (255,), anchor='mm')
    else:
        # sulle laterali resta scoperto solo il bordo esterno: il seme va li'
        f = ImageFont.truetype(FB, int(h * 0.26))
        d.text((m + w * 0.24, m + h * 0.20), SEMI[seme], font=f, fill=col + (255,), anchor='mm')
    return im


def ruota_su_perno(c, ang, giu):
    """Ruota la carta attorno a un perno posto `giu` px sotto il suo bordo inferiore:
    e' quello che fa aprire le carte a ventaglio invece di girarle su se stesse."""
    P = int(c.height + giu)
    tela = Image.new('RGBA', (2 * P, 2 * P), (0, 0, 0, 0))
    tela.alpha_composite(c, (P - c.width // 2, P - c.height - int(giu)))
    return tela.rotate(ang, resample=Image.BICUBIC)


def ventaglio(lato, scala=1.0):
    im = Image.new('RGBA', (lato, lato), (0, 0, 0, 0))
    w = int(lato * 0.34 * scala)
    h = int(w * 1.4)
    giu = h * 0.55
    # `ruota_su_perno` mette il PERNO al centro della sua tela: per centrare le
    # carte bisogna abbassare il perno di mezza carta piu' la distanza del perno.
    cx = lato / 2
    cy = lato * 0.47 + giu + h / 2

    for ang, seme, grande in [(24, 'c', False), (-24, 'h', False), (0, 's', True)]:
        r = ruota_su_perno(carta(w, h, seme, grande), ang, giu)
        x, y = int(cx - r.width / 2), int(cy - r.height / 2)
        ombra = Image.new('RGBA', r.size, (0, 0, 0, 0))
        ombra.paste((0, 0, 0, 120), (0, 0), r.split()[3])
        ombra = ombra.filter(ImageFilter.GaussianBlur(lato * 0.016))
        im.alpha_composite(ombra, (x, y + int(lato * 0.015)))
        im.alpha_composite(r, (x, y))
    return im


def icona(forma='tonda'):
    """forma: 'tonda' (web/Android), 'piena' (apple-touch-icon: iOS applica da
    solo la maschera, e un PNG gia' smussato con angoli trasparenti si vede male),
    'maskable' (contenuto ristretto all'80% centrale perche' i bordi vengono tagliati)."""
    im = fondo(S).convert('RGBA')
    im.alpha_composite(ventaglio(S, 0.72 if forma == 'maskable' else 1.0))
    if forma != 'tonda':
        return im
    m = Image.new('L', (S, S), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, S, S], radius=int(S * 0.22), fill=255)
    out = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    out.paste(im, (0, 0), m)
    return out


if __name__ == '__main__':
    os.makedirs('icone', exist_ok=True)
    icona('piena').resize((180, 180), Image.LANCZOS).save('icone/icon-burraco-180.png')
    tonda = icona('tonda')
    for n in (192, 512):
        tonda.resize((n, n), Image.LANCZOS).save('icone/icon-burraco-%d.png' % n)
    icona('maskable').resize((512, 512), Image.LANCZOS).save('icone/icon-burraco-maskable-512.png')
    tot = sum(os.path.getsize('icone/' + f) for f in os.listdir('icone'))
    print('icone generate:', sorted(os.listdir('icone')), '|', round(tot / 1024, 1), 'KB')
