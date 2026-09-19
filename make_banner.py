# -*- coding: utf-8 -*-
"""Анимированная плашка 3:1 для GitHub-профиля.
За основу взят визуал "терминал" из AIM referral media pack (94 ref cards):
тёмный лист, слабая сетка, поле ячеек активности в зелёной шкале, одна красная ячейка.
Canvas-анимация заменена на SMIL, потому что GitHub не исполняет JS в README.
"""
import io

W, H = 1200, 400
COLS, ROWS = 22, 9
CELL_AR, GAP_K, R_K = 1.35, 0.26, 0.18
GX, GY, GW = 0.530, 0.166, 0.430
RED_CELL = (14, 4)

MONO = "ui-monospace,'SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(
        bg="#0A0E14", grid="rgba(255,255,255,0.035)", dead="#161B22",
        ramp=["#0E4429", "#006D32", "#26A641", "#39D353"], red="#D92027",
        ink="#F2F0E9", sub="#C9CDC7", mute="#6E7673", glow="#39D353",
    ),
    "light": dict(
        bg="#F2F0E9", grid="rgba(17,18,16,0.055)", dead="#E3E1D8",
        ramp=["#9BE9A8", "#40C463", "#30A14E", "#216E39"], red="#B82032",
        ink="#111210", sub="#3D423C", mute="#7C817A", glow="#216E39",
    ),
}


def rnd32(seed):
    a = seed
    def f():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = ((t ^ (t >> 15)) * (1 | t)) & 0xFFFFFFFF
        t = (t + (((t ^ (t >> 7)) * (61 | t)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return (((t ^ (t >> 14)) & 0xFFFFFFFF)) / 4294967296
    return f


def build(theme_name):
    T = THEMES[theme_name]
    x0, y0, gw = GX * W, GY * H, GW * W
    cw = gw / (COLS + GAP_K * (COLS - 1))
    gap = cw * GAP_K
    ch = cw * CELL_AR
    rad = cw * R_K
    grid_h = ROWS * ch + (ROWS - 1) * gap

    o = io.StringIO()
    o.write(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Mykhailo Yatsenko — AI creator, AI video and generative content">\n'
    )
    o.write('<defs>\n')
    o.write(f'<radialGradient id="bloom"><stop offset="0%" stop-color="{T["glow"]}" stop-opacity="0.20"/>'
            f'<stop offset="100%" stop-color="{T["glow"]}" stop-opacity="0"/></radialGradient>\n')
    o.write('</defs>\n')

    # лист
    o.write(f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>\n')

    # слабая сетка листа
    o.write(f'<g stroke="{T["grid"]}" stroke-width="1">\n')
    step = 40
    for x in range(step, W, step):
        o.write(f'<path d="M{x} 0 V{H}"/>')
    for y in range(step, H, step):
        o.write(f'<path d="M0 {y} H{W}"/>')
    o.write('\n</g>\n')

    # свечение под полем
    cxg, cyg = x0 + gw / 2, y0 + grid_h / 2
    o.write(f'<ellipse cx="{cxg:.0f}" cy="{cyg:.0f}" rx="{gw*0.75:.0f}" ry="{grid_h*0.85:.0f}" fill="url(#bloom)">'
            f'<animate attributeName="opacity" values="0.55;1;0.55" dur="7s" repeatCount="indefinite"/></ellipse>\n')

    # ---- текстовый блок ----
    tx = 85
    o.write(f'<g font-family="{MONO}">\n')
    # тег в рамке
    tag = "{ai creator}"
    tag_w = len(tag) * 9.6 + 26
    o.write(f'<rect x="{tx}" y="78" width="{tag_w:.0f}" height="34" rx="3" fill="none" '
            f'stroke="{T["ink"]}" stroke-width="1.5"/>\n')
    o.write(f'<text x="{tx+13}" y="101" font-size="16" font-weight="700" letter-spacing="1.2" '
            f'fill="{T["ink"]}">{tag}</text>\n')
    # заголовок
    o.write(f'<text x="{tx}" y="186" font-size="48" font-weight="800" letter-spacing="-0.5" '
            f'fill="{T["ink"]}">Mykhailo Yatsenko</text>\n')
    # подзаголовок
    o.write(f'<text x="{tx}" y="228" font-size="21" fill="{T["sub"]}">AI video &#183; generative content</text>\n')
    # пояснение
    o.write(f'<text x="{tx}" y="266" font-size="13.5" letter-spacing="0.4" fill="{T["mute"]}">'
            f'15+ yrs in VFX &amp; 3D &#183; Sony Music &#183; AT&amp;T &#183; Autodesk</text>\n')
    # домен + курсор
    o.write(f'<text x="{tx}" y="336" font-size="17" font-weight="700" letter-spacing="0.6" '
            f'fill="{T["ink"]}">mykhailus.netlify.app</text>\n')
    o.write(f'<rect x="{tx+208}" y="322" width="10" height="18" fill="{T["ramp"][-1] if theme_name=="dark" else T["ramp"][2]}">'
            f'<animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>\n')
    o.write('</g>\n')

    # ---- поле ячеек ----
    rnd = rnd32(515)
    o.write('<g>\n')
    for r in range(ROWS):
        for c in range(COLS):
            x = x0 + c * (cw + gap)
            y = y0 + r * (ch + gap)
            base = rnd()
            phase = rnd()
            speed = rnd()
            is_red = (c, r) == RED_CELL
            if is_red:
                o.write(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" '
                        f'rx="{rad:.1f}" fill="{T["red"]}"/>')
                continue
            # тихие ячейки остаются погашенными — поле должно дышать, а не гореть целиком
            if base < 0.40:
                o.write(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" '
                        f'rx="{rad:.1f}" fill="{T["dead"]}"/>')
                continue
            # у каждой ячейки свой набор оттенков и своя скорость — как активность в терминале
            n = 4 + int(base * 3)
            vals = []
            for k in range(n):
                v = (base * 0.55 + phase * 0.3 + ((c * 7 + r * 13 + k * 29) % 17) / 17 * 0.45) % 1
                if v < 0.52:
                    vals.append(T["dead"])
                else:
                    vals.append(T["ramp"][min(3, int((v - 0.52) / 0.48 * 4))])
            vals.append(vals[0])  # замкнуть луп
            dur = 3.2 + speed * 6.5
            begin = -(phase * dur)
            o.write(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" '
                    f'rx="{rad:.1f}" fill="{vals[0]}">'
                    f'<animate attributeName="fill" values="{";".join(vals)}" '
                    f'dur="{dur:.2f}s" begin="{begin:.2f}s" repeatCount="indefinite"/></rect>')
        o.write('\n')
    o.write('</g>\n')

    # бегущий курсор под полем
    cur_y = y0 + grid_h + ch * 0.55
    o.write(f'<rect x="{x0:.1f}" y="{cur_y:.1f}" width="{cw:.1f}" height="3" '
            f'fill="{T["ramp"][-1] if theme_name=="dark" else T["ramp"][2]}">'
            f'<animate attributeName="x" values="{x0:.1f};{x0+gw-cw:.1f};{x0:.1f}" dur="9s" '
            f'repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.35;1;0.35" dur="1.4s" repeatCount="indefinite"/></rect>\n')

    o.write('</svg>\n')
    return o.getvalue()


for name in ("dark", "light"):
    p = f"banner-{name}.svg"
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(build(name))
    print(name, "->", len(build(name)), "bytes")
