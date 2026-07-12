#!/usr/bin/env python3
"""Gera os icones do PWA Impulso (marca: seta de impulso/momentum sobre tile escuro)."""
import math
from PIL import Image, ImageDraw, ImageFilter

SS = 4  # supersampling

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))

def vertical_gradient(size, top, bottom):
    w, h = size
    grad = Image.new("RGB", (1, h))
    for y in range(h):
        grad.putpixel((0, y), lerp(top, bottom, y / max(1, h - 1)))
    return grad.resize((w, h))

def radial_glow(size, color, cx, cy, radius, max_alpha):
    w, h = size
    layer = Image.new("L", (w, h), 0)
    px = layer.load()
    for y in range(h):
        for x in range(w):
            d = math.hypot(x - cx, y - cy) / radius
            if d < 1:
                px[x, y] = int(max_alpha * (1 - d) ** 2)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    solid = Image.new("RGBA", (w, h), color + (255,))
    out.paste(solid, (0, 0), layer)
    return out

def draw_impulse(D, cx, cy, scale, col):
    """Seta de impulso: haste + chevron arredondado, apontando pra cima."""
    lw = int(58 * scale)
    top_y = cy - int(150 * scale)
    bot_y = cy + int(150 * scale)
    spread = int(118 * scale)
    head_y = top_y + int(120 * scale)
    # haste
    D.line([(cx, bot_y), (cx, top_y)], fill=col, width=lw, joint="curve")
    # chevron
    D.line([(cx - spread, head_y), (cx, top_y), (cx + spread, head_y)],
           fill=col, width=lw, joint="curve")
    # caps arredondados
    r = lw // 2
    for (x, y) in [(cx, bot_y), (cx, top_y), (cx - spread, head_y), (cx + spread, head_y)]:
        D.ellipse([x - r, y - r, x + r, y + r], fill=col)

def make_icon(px, maskable=False, path="icon.png"):
    S = px * SS
    # base: tile escuro com gradiente + glow quente no topo (assinatura do app)
    img = vertical_gradient((S, S), (0x26, 0x2B, 0x33), (0x0C, 0x0E, 0x10)).convert("RGBA")
    glow_bg = radial_glow((S // 4, S // 4), (0xF0, 0xA6, 0x3C),
                          (S // 8), (S // 8) - S // 14, S // 6, 70).resize((S, S))
    img = Image.alpha_composite(img, glow_bg)

    cx = cy = S // 2
    scale = (S / 512.0) * (0.80 if maskable else 1.0)

    # glow da seta
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    Dg = ImageDraw.Draw(glow)
    draw_impulse(Dg, cx, cy, scale, (0xF0, 0xA6, 0x3C, 255))
    glow = glow.filter(ImageFilter.GaussianBlur(int(22 * SS)))
    img = Image.alpha_composite(img, glow)

    # mascara da seta -> preenche com gradiente laranja
    mask = Image.new("L", (S, S), 0)
    Dm = ImageDraw.Draw(mask)
    draw_impulse(Dm, cx, cy, scale, 255)
    arrow_grad = vertical_gradient((S, S), (0xFF, 0xCE, 0x82), (0xD9, 0x87, 0x27)).convert("RGBA")
    img.paste(arrow_grad, (0, 0), mask)

    # highlight sutil no topo da seta
    hi = Image.new("L", (S, S), 0)
    Dh = ImageDraw.Draw(hi)
    Dh.ellipse([cx - int(30*scale), cy - int(170*scale),
                cx + int(30*scale), cy - int(110*scale)], fill=90)
    hi = hi.filter(ImageFilter.GaussianBlur(int(6*SS)))
    white = Image.new("RGBA", (S, S), (255, 245, 230, 255))
    img.paste(white, (0, 0), hi)

    img = img.resize((px, px), Image.LANCZOS)
    img.save(path)
    print("wrote", path, px)

base = "/home/user/APP-PWA-IMPULSO"
make_icon(512, maskable=False, path=f"{base}/icons/icon-512.png")
make_icon(192, maskable=False, path=f"{base}/icons/icon-192.png")
make_icon(512, maskable=True,  path=f"{base}/icons/icon-maskable-512.png")
make_icon(180, maskable=False, path=f"{base}/icons/apple-touch-icon.png")
make_icon(32,  maskable=False, path=f"{base}/icons/favicon-32.png")
