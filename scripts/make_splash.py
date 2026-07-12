#!/usr/bin/env python3
"""Splash screens (launch images) escuros para iOS — evita flash branco na abertura."""
import math
from PIL import Image, ImageDraw, ImageFilter

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))

def vgrad(w, h, top, bot):
    g = Image.new("RGB", (1, h))
    for y in range(h):
        g.putpixel((0, y), lerp(top, bot, y / max(1, h - 1)))
    return g.resize((w, h))

def draw_impulse(D, cx, cy, s, col):
    lw = int(58 * s)
    top_y = cy - int(150 * s); bot_y = cy + int(150 * s)
    spread = int(118 * s); head_y = top_y + int(120 * s)
    D.line([(cx, bot_y), (cx, top_y)], fill=col, width=lw, joint="curve")
    D.line([(cx - spread, head_y), (cx, top_y), (cx + spread, head_y)], fill=col, width=lw, joint="curve")
    r = lw // 2
    for (x, y) in [(cx, bot_y), (cx, top_y), (cx - spread, head_y), (cx + spread, head_y)]:
        D.ellipse([x - r, y - r, x + r, y + r], fill=col)

def make_splash(w, h, path):
    img = vgrad(w, h, (0x15, 0x18, 0x1C), (0x0A, 0x0B, 0x0D)).convert("RGBA")
    # glow quente sutil no centro-topo (assinatura)
    glow = Image.new("L", (w, h), 0); gp = glow.load()
    cx, cy = w // 2, int(h * 0.44)
    rad = w * 0.55
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            d = math.hypot(x - cx, y - cy) / rad
            if d < 1:
                v = int(38 * (1 - d) ** 2)
                gp[x, y] = v
                if x + 1 < w: gp[x + 1, y] = v
                if y + 1 < h: gp[x, y + 1] = v
    orange = Image.new("RGBA", (w, h), (0xF0, 0xA6, 0x3C, 255))
    img.paste(orange, (0, 0), glow)

    scale = (w / 512.0) * 0.42
    # glow da seta
    gl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_impulse(ImageDraw.Draw(gl), cx, cy, scale, (0xF0, 0xA6, 0x3C, 255))
    gl = gl.filter(ImageFilter.GaussianBlur(int(w * 0.02)))
    img = Image.alpha_composite(img, gl)
    # seta com gradiente
    mask = Image.new("L", (w, h), 0)
    draw_impulse(ImageDraw.Draw(mask), cx, cy, scale, 255)
    ag = vgrad(w, h, (0xFF, 0xCE, 0x82), (0xD9, 0x87, 0x27)).convert("RGBA")
    img.paste(ag, (0, 0), mask)
    img.convert("RGB").save(path, "PNG")
    print("wrote", path, f"{w}x{h}")

base = "/home/user/APP-PWA-IMPULSO/icons"
# Pro Max classe 6.7"/6.9" (dpr 3)
make_splash(1290, 2796, f"{base}/splash-1290x2796.png")   # 430w  (14/15/16/17 Pro Max)
make_splash(1320, 2868, f"{base}/splash-1320x2868.png")   # 440w  (16/17 Pro Max)
make_splash(1179, 2556, f"{base}/splash-1179x2556.png")   # 393w  (Pro)
make_splash(1206, 2622, f"{base}/splash-1206x2622.png")   # 402w  (16/17 Pro)
