#!/usr/bin/env python3
"""Generate public/theme-lab/index.html — iteration 5: the original arms, traced faithfully,
placed into the Night Smithy hero and the Forge II seal.

Run:  python3 design/coa/build_coa.py && python3 design/theme-lab/build_v5.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "coa"))
import build_coa as coa  # noqa: E402
from build_v2 import DEFS  # noqa: E402
from build_v3 import ARC, CSS as V3CSS, HORNS, SEAL_TEXT, glow_runes, sky  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "public" / "theme-lab" / "v5" / "index.html"
BRASS, WAX, RIM = "#C9A15E", "#6E1414", "#9A2A2A"


def arms(h: int, kind: str = "shaded", cls: str = "", uid: str = "a", color: str = BRASS) -> str:
    w = round(h * 156 / 192)
    inner = {"shaded": coa.shaded(uid), "flat": coa.flat(uid), "mono": coa.mono(uid, color)}[kind]
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="{w}" height="{h}" viewBox="0 0 156 192" role="img" aria-label="The Graah arms">{inner}</svg>'


def seal(uid: str, size: int = 200, centre: str = "mono") -> str:
    inner = coa.mono(uid, BRASS, border=4) if centre == "mono" else coa.shaded(uid)
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 200 200" role="img" aria-label="The Graah seal">'
        f'<defs><path id="ring-{uid}" d="M100 100 m-75 0 a75 75 0 1 1 150 0 a75 75 0 1 1 -150 0"/></defs>'
        f'<circle cx="100" cy="100" r="97" fill="{WAX}"/>'
        f'<circle cx="100" cy="100" r="92" fill="none" stroke="{RIM}" stroke-width="2"/>'
        f'<circle cx="100" cy="100" r="60" fill="none" stroke="{BRASS}" stroke-width="1"/>'
        f'<text font-family="Noto Sans Runic" font-size="14.5" fill="{BRASS}" letter-spacing="5.2"><textPath href="#ring-{uid}">{SEAL_TEXT}</textPath></text>'
        f'<svg x="68" y="61" width="64" height="79" viewBox="0 0 156 192">{inner}</svg></svg>'
    )


def hero(variant: str, uid: str) -> str:
    if variant == "arms":
        emblem = arms(170, "shaded", "h-arms", uid)
    elif variant == "crest":
        emblem = f'<div class="h-crest">{HORNS}{arms(150, "shaded", "h-arms", uid)}</div>'
    else:  # brass
        emblem = arms(170, "mono", "h-arms brass", uid)
    nav_arms = arms(24, "shaded", "", uid + "n")
    return f"""
<div class="hz">
  {sky(7)}
  {ARC}
  <div class="hin">
    <nav class="hnav"><span class="brand">{nav_arms}Graah</span><span class="mid">I — IX</span><span>1462 → now</span></nav>
    <div class="hcopy">{emblem}<h3 class="wm">GRAAH</h3>{glow_runes("under")}<p class="tag">Five centuries. Three kingdoms. One name.</p></div>
  </div>
</div>"""


CSS = r"""
.h-arms{width:clamp(70px,11cqw,170px);height:auto;margin-bottom:2cqw;filter:drop-shadow(0 0 2.4cqw rgba(62,98,184,.28))}
.h-arms.brass{filter:drop-shadow(0 0 2cqw rgba(201,161,94,.3))}
.h-crest{display:flex;flex-direction:column;align-items:center}
.h-crest .horns{width:clamp(56px,9cqw,140px);margin-bottom:-1.4cqw}
.h-crest .h-arms{width:clamp(60px,9.5cqw,150px)}
.hnav .brand svg{width:auto;height:22px}
.compare{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#26304A;border:1px solid #26304A}
.compare>div{background:#F4F0E8;padding:26px;display:flex;flex-direction:column;align-items:center;gap:14px}
.compare img,.compare svg{height:300px;width:auto}
.compare h4{font:500 11px/1.3 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#6E1414}
.compare p{font:400 14px/1.5 Geist;color:#4C4740;text-align:center;max-width:300px}
.hgrid3{display:grid;grid-template-columns:1fr;gap:34px}
.hgrid3 figcaption{font:300 14px/1.5 Geist;color:#A6B3C4;margin-top:12px}
.hgrid3 figcaption b{display:block;font:500 11px/1.3 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#C9A15E;margin-bottom:6px}
.seals{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.seals>div{background:#0e1424;border:1px solid #26304A;padding:26px;display:flex;flex-direction:column;align-items:center;gap:14px}
.seals h4{font:500 11px/1.3 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#C9A15E;align-self:flex-start}
.seals p{font:300 14px/1.5 Geist;color:#A6B3C4}
.files{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.files>div{border:1px solid #26304A;background:#0e1424;padding:22px;display:flex;flex-direction:column;gap:14px}
.files .art{height:170px;display:flex;align-items:center;justify-content:center;gap:18px}
.files .art.paper{background:#F4F0E8}
.files code{font:400 12px/1.4 "Geist Mono";color:#E9C98A}
.files p{font:300 14px/1.5 Geist;color:#A6B3C4}
.files a{font:500 11px/1 "Geist Mono";letter-spacing:.14em;text-transform:uppercase;color:#C9A15E}
.sizes2{display:flex;gap:26px;align-items:flex-end;flex-wrap:wrap;margin-top:28px}
.sizes2 span{display:flex;flex-direction:column;align-items:center;gap:8px;font:400 11px/1 "Geist Mono";color:#8EA0B8}
@media (max-width:960px){.compare,.seals,.files{grid-template-columns:1fr}.compare img,.compare svg{height:240px}}
"""


def page() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="robots" content="noindex, nofollow" />
<meta name="theme-color" content="#0B0F1A" />
<link rel="icon" href="/graah-coa.png" type="image/png" />
<title>Graah — Identity exploration v0.5 · The original arms</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Forum&family=Geist:wght@300..700&family=Geist+Mono:wght@400;500&family=Noto+Sans+Runic&display=swap" rel="stylesheet" />
<style>{V3CSS}{CSS}</style>
</head>
<body>
{DEFS}
<section class="intro"><div class="wrap">
  <div class="eyebrow">Graah · Visual identity · v0.5 · <a href="/theme-lab/">latest →</a> · <a href="/theme-lab/v4/">v0.4 (shield variants)</a> · <a href="/theme-lab/v3/">v0.3</a> · <a href="/theme-lab/v2/">v0.2</a> · <a href="/theme-lab/v1/">v0.1</a></div>
  <h1>The original arms,<br/><em>kept.</em></h1>
  <p class="lede">No redesign. The arms are traced from the family's original image: same shield outline, same star size and placement, same rainbow curve and the same light-from-the-upper-left shading. Measured from the pixels, not drawn by eye. They now sit in the Night Smithy start page and the Forge II seal.</p>
</div></section>

<section class="sec" id="trace"><div class="wrap">
  <div class="code">01 · The trace</div><h2>Original, old copy, new trace</h2>
  <p class="lede">The old SVG on the site was a loose redraw: black outlines, small stars, rounded corners. The new one matches the original to within a pixel, and scales to any size.</p>
  <div class="compare">
    <div><img src="/graah-coa.png" alt="The original Graah arms" style="image-rendering:auto"/><h4>Original · PNG, 156×192</h4><p>The family's image. Blurry when enlarged.</p></div>
    <div><img src="/theme-lab/v5/old-coa.svg" alt="The previous SVG redraw"/><h4>Old SVG redraw</h4><p>What the site used until now.</p></div>
    <div>{arms(300, "shaded", "", "t1")}<h4>New trace · SVG</h4><p>Same shapes and shading as the original, now sharp at any size.</p></div>
  </div>
</div></section>

<section class="sec" id="hero"><div class="wrap">
  <div class="code">02 · Night Smithy</div><h2>The arms in the start page</h2>
  <p class="lede">Same sky, aurora, Forum wordmark and glowing runes as before. The arms are the emblem.</p>
  <div class="hgrid3">
    <figure>{hero("arms", "h1")}<figcaption><b>A · Arms</b>The original arms in full colour above the name. My recommendation.</figcaption></figure>
    <figure>{hero("crest", "h2")}<figcaption><b>B · Arms with the crest horns</b>The horns sit above the shield, as on the helm in the full achievement.</figcaption></figure>
    <figure>{hero("brass", "h3")}<figcaption><b>C · Arms in brass</b>The same arms in one colour, matching the runes. Quieter; the colour is saved for inside the site.</figcaption></figure>
  </div>
</div></section>

<section class="sec" id="seal"><div class="wrap">
  <div class="code">03 · Forge II seal</div><h2>The seal, with the real arms</h2>
  <p class="lede">The seal you liked, with the traced arms in the centre. The ring still reads ᚴᚱᛅᛅᚼ ᛬ ᛋᚢᛚᛁᛋᛏᛁᛏ: Graah · Søllested.</p>
  <div class="seals">
    <div><h4>Brass arms</h4>{seal("s1", 220)}<p>One-colour arms in brass, like the runes. Works when stamped, engraved or pressed in wax.</p></div>
    <div><h4>Colour arms</h4>{seal("s2", 220, "colour")}<p>Full-colour arms on the wax. Richer on screen; can't be stamped.</p></div>
    <div><h4>Sizes</h4><div class="sizes2"><span>{seal("z1", 120)}120</span><span>{seal("z2", 64)}64</span><span>{arms(32, "shaded", "", "z3")}32</span><span>{arms(16, "shaded", "", "z4")}16</span></div><p>Below 64px, use the arms alone rather than the seal.</p></div>
  </div>
</div></section>

<section class="sec" id="files"><div class="wrap">
  <div class="code">04 · Files</div><h2>Three versions, one drawing</h2>
  <p class="lede">All three share exactly the same geometry. Only the finish changes.</p>
  <div class="files">
    <div><div class="art paper"><img src="/graah-coa.svg" alt="" height="150"/></div><code>/graah-coa.svg</code><p>Full colour with the original shading. The default.</p><a href="/graah-coa.svg" download>Download</a></div>
    <div><div class="art paper"><img src="/graah-coa-flat.svg" alt="" height="150"/></div><code>/graah-coa-flat.svg</code><p>Flat colour, no gradients. Print, embroidery, enamel pins.</p><a href="/graah-coa-flat.svg" download>Download</a></div>
    <div><div class="art">{arms(150, "mono", "", "f3")}</div><code>/graah-coa-mono.svg</code><p>One colour. Seals, signet rings, engraving, letterpress.</p><a href="/graah-coa-mono.svg" download>Download</a></div>
  </div>
</div></section>

<section class="sec" id="next"><div class="wrap">
  <div class="code">Next</div><h2>What to send back</h2>
  <div class="qs">
    <div><h4>1 · Start page</h4><p>A (colour arms), B (arms with horns) or C (brass arms)?</p></div>
    <div><h4>2 · Seal</h4><p>Brass arms or colour arms in the centre?</p></div>
    <div><h4>3 · Body font</h4><p>Geist or Newsreader? (Still open from v0.3.)</p></div>
    <div><h4>4 · Go live</h4><p>Once these are settled, I can rebuild graah.se in this style, in all eight languages.</p></div>
  </div>
</div></section>
<footer class="page"><div class="wrap">Exploration only. The traced arms are already used on graah.se. Generated by design/theme-lab/build_v5.py and design/coa/build_coa.py.</div></footer>
</body>
</html>
"""


if __name__ == "__main__":
    OUT.write_text(page(), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")
