#!/usr/bin/env python3
"""Generate public/theme-lab/index.html — iteration 6: the chosen system.

Decisions so far:
  - Night Smithy hero, layout A: the original arms in full colour above the Forum wordmark
  - Forge II seal with the arms in brass
  - Glowing brass runes, Forum display
  - Open: body font (Geist vs Newsreader) — toggle on the page

Run:  python3 design/coa/build_coa.py && python3 design/theme-lab/build_v6.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "coa"))
import build_v3 as v3  # noqa: E402
from build_v2 import DEFS  # noqa: E402
from build_v5 import arms, seal  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "public" / "theme-lab" / "index.html"


def preview() -> str:
    html = v3.page_preview()
    html = html.replace(v3.HORNS, arms(170, "shaded", "h-arms", "hero"), 1)
    html = html.replace(v3.BRAND, f'<span class="brand">{arms(24, "shaded", "", "nav")}Graah</span>', 1)
    html = html.replace(v3.seal("foot", size=120), seal("foot", 120), 1)
    return html


CSS = r"""
.h-arms{width:clamp(80px,11cqw,170px);height:auto;margin-bottom:2cqw;filter:drop-shadow(0 0 2.4cqw rgba(62,98,184,.28))}
.hnav .brand svg{width:auto;height:22px}
.decided{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#26304A;border:1px solid #26304A;margin-top:36px}
.decided>div{background:#0e1424;padding:22px;display:flex;flex-direction:column;gap:12px}
.decided .art{height:150px;display:flex;align-items:center;justify-content:center}
.decided h4{font:500 11px/1.3 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#C9A15E}
.decided p{font:300 14px/1.5 Geist;color:#A6B3C4}
.decided .open h4{color:#E0675A}
.fontpick{display:flex;gap:8px;align-items:center;margin:0 0 18px;flex-wrap:wrap}
.fontpick span{font:500 11px/1 "Geist Mono";letter-spacing:.16em;text-transform:uppercase;color:#8EA0B8;margin-right:6px}
.fontpick button{font:500 12px/1 "Geist Mono";letter-spacing:.1em;background:transparent;color:#DCE6EE;border:1px solid #26304A;border-radius:999px;padding:10px 14px;cursor:pointer}
.fontpick button[aria-pressed="true"]{background:#C9A15E;border-color:#C9A15E;color:#0B0F1A}
.fontpick .geist{font-family:Geist;text-transform:none;letter-spacing:0;font-size:14px}
.fontpick .news{font-family:Newsreader;text-transform:none;letter-spacing:0;font-size:15px}
.site.body-news .s-intro .big{font-family:Newsreader;font-size:clamp(24px,2.7vw,34px)}
.site.body-news .ch-text p,.site.body-news .kicker,.site.body-news .receipts li,.site.body-news .stop span,.site.body-news .s-foot p{font-family:Newsreader;font-weight:400}
.site.body-news .ch-text p{font-size:18px;line-height:1.65}
.decided .hnav span:not(.brand){display:none}
@media (max-width:960px){.decided{grid-template-columns:1fr 1fr}}
@media (max-width:560px){.decided{grid-template-columns:1fr}}
"""


def page() -> str:
    hero_thumb = (
        '<div style="width:100%;font-size:0">'
        + v3.hero("smithy").replace(v3.HORNS, arms(170, "shaded", "h-arms", "thumb"), 1).replace(
            v3.BRAND, f'<span class="brand">{arms(24, "shaded", "", "thumbnav")}Graah</span>', 1
        )
        + "</div>"
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="robots" content="noindex, nofollow" />
<meta name="theme-color" content="#0B0F1A" />
<link rel="icon" href="/graah-coa.png" type="image/png" />
<title>Graah — Identity v0.6 · The chosen system</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="{v3.FONTS}" rel="stylesheet" />
<style>{v3.CSS}{CSS}</style>
</head>
<body>
{DEFS}
<section class="intro"><div class="wrap">
  <div class="eyebrow">Graah · Visual identity · v0.6 · <a href="/theme-lab/v5/">v0.5 (traced arms)</a> · <a href="/theme-lab/v4/">v0.4</a> · <a href="/theme-lab/v3/">v0.3</a> · <a href="/theme-lab/v2/">v0.2</a> · <a href="/theme-lab/v1/">v0.1</a></div>
  <h1>The Graah system,<br/><em>chosen.</em></h1>
  <p class="lede">Everything you've picked, put together. One choice is still open, the body font. Flip between the two in the site preview below.</p>
  <div class="decided">
    <div><div class="art">{hero_thumb}</div><h4>Start page · A</h4><p>Night Smithy: polar night, starfield, aurora. The original arms in colour above the Forum wordmark.</p></div>
    <div><div class="art">{seal("dec", 140)}</div><h4>Seal · brass arms</h4><p>Forge II: oxblood wax, brass rune ring reading Graah · Søllested, the arms in brass.</p></div>
    <div><div class="art">{v3.glow_runes("load")}</div><h4>Runes · Forum</h4><p>ᚴᚱᛅᛅᚼ glowing in brass beneath the name. Forum for the wordmark, headlines and numbers.</p></div>
    <div class="open"><div class="art" style="flex-direction:column;gap:10px"><span style="font:300 26px/1 Geist">Geist</span><span style="font:400 28px/1 Newsreader">Newsreader</span></div><h4>Open · body font</h4><p>Geist is cleaner and more modern. Newsreader is warmer and more like a book. Try both below.</p></div>
  </div>
</div></section>

<section class="sec" id="preview"><div class="wrap">
  <div class="code">Site preview</div><h2>graah.se, in the chosen style</h2>
  <p class="lede">Real chronicle content: the start page, the intro, chapter IV with its engraving and records, the stats, the timeline, and the footer with the seal.</p>
  <div class="fontpick" role="group" aria-label="Body font">
    <span>Body font</span>
    <button type="button" class="geist" data-f="geist" aria-pressed="true">Geist</button>
    <button type="button" class="news" data-f="news" aria-pressed="false">Newsreader</button>
  </div>
</div>
<div class="wrap">{preview()}</div></section>

<section class="sec" id="next"><div class="wrap">
  <div class="code">Next</div><h2>What to send back</h2>
  <div class="qs">
    <div><h4>1 · Body font</h4><p>Geist or Newsreader?</p></div>
    <div><h4>2 · Go live</h4><p>Should I then rebuild graah.se in this style, in all eight languages, replacing the current template?</p></div>
  </div>
</div></section>
<footer class="page"><div class="wrap">Exploration only. graah.se itself still uses the template theme. Generated by design/theme-lab/build_v6.py.</div></footer>
<script>
(()=>{{
  const site=document.querySelector('.site');
  const btns=document.querySelectorAll('.fontpick button');
  btns.forEach(b=>b.addEventListener('click',()=>{{
    site.classList.toggle('body-news',b.dataset.f==='news');
    btns.forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));
  }}));
}})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    OUT.write_text(page(), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")
