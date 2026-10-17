#!/usr/bin/env python3
"""Generate public/theme-lab/index.html — Graah identity exploration, iteration 3.

Converges on: the Night Smithy hero, the Forge II seal, glowing runes, and Forum.

Run:  python3 design/theme-lab/build_v3.py
Pure stdlib. Reuses the shared SVG symbols and helpers from build_v2.
"""

from __future__ import annotations

import json
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_v2 import DEFS, RUNES, cord  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "public" / "theme-lab" / "index.html"
EN = json.loads((ROOT / "src" / "i18n" / "locales" / "en.json").read_text(encoding="utf-8"))

SEAL_TEXT = "ᚴᚱᛅᛅᚼ ᛬ ᛋᚢᛚᛁᛋᛏᛁᛏ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᛋᚢᛚᛁᛋᛏᛁᛏ ᛬"

# Night Smithy palette, extended with the Forge II wax and a rune-glow highlight
C = dict(
    night="#0B0F1A", fjord="#111829", line="#26304A", glacier="#DCE6EE", smoke="#8EA0B8",
    brass="#C9A15E", glow="#E9C98A", red="#C8283A", wax="#6E1414", steel="#3E62B8",
)


# ───────────────────────── pieces ─────────────────────────


def sky(seed: int, n: int = 170) -> str:
    """Starfield. A handful of stars twinkle; three are heraldic mullets."""
    rnd = random.Random(seed)
    dots = []
    for i in range(n):
        x, y = rnd.random() * 1200, rnd.random() * 520
        r = rnd.random() * 1.1 + 0.2
        o = rnd.random() * 0.6 + 0.15
        tw = ""
        if i % 9 == 0:
            tw = f' class="tw" style="animation-delay:{rnd.random() * 6:.2f}s"'
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{C["glacier"]}" opacity="{o:.2f}"{tw}/>')
    return (
        '<svg class="sky" viewBox="0 0 1200 700" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
        + "".join(dots)
        + f'<use href="#mullet" x="170" y="110" width="14" height="14" fill="{C["red"]}" opacity=".85"/>'
        + f'<use href="#mullet" x="1010" y="84" width="11" height="11" fill="{C["brass"]}" opacity=".9"/>'
        + f'<use href="#mullet" x="905" y="270" width="8" height="8" fill="{C["glacier"]}" opacity=".7"/>'
        + "</svg>"
    )


ARC = f"""<svg class="arc" viewBox="0 0 1200 300" preserveAspectRatio="none" aria-hidden="true">
  <defs><linearGradient id="planet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101a33"/><stop offset="1" stop-color="{C['night']}"/></linearGradient></defs>
  <path class="aur" d="M-20 300 Q600 40 1220 300" stroke="{C['steel']}" stroke-width="46" fill="none" opacity=".13"/>
  <path d="M-20 300 Q600 40 1220 300 Z" fill="url(#planet)"/>
  <path d="M-20 300 Q600 40 1220 300" stroke="{C['steel']}" stroke-width="1.3" fill="none" vector-effect="non-scaling-stroke"/>
  <path d="M-20 315 Q600 55 1220 315" stroke="{C['brass']}" stroke-width="1.1" fill="none" vector-effect="non-scaling-stroke"/>
  <path d="M-20 330 Q600 70 1220 330" stroke="{C['red']}" stroke-width="1.1" fill="none" vector-effect="non-scaling-stroke"/>
</svg>"""


def glow_runes(cls: str = "", seq: bool = False) -> str:
    if not seq:
        return f'<span class="rune glow {cls}">{RUNES}</span>'
    spans = "".join(f'<span style="animation-delay:{i * 0.28:.2f}s">{r}</span>' for i, r in enumerate(RUNES))
    return f'<span class="rune seq {cls}">{spans}</span>'


def seal(
    uid: str,
    style: str = "flat",
    size: int = 180,
    wax: str = C["wax"],
    rim: str = "#9A2A2A",
    metal: str = C["brass"],
    center: str = "shield",
    text: bool = True,
    cls: str = "",
) -> str:
    """The Forge II seal and its finishes: flat (as liked), wax, foil, ink."""
    shield_vars = f"--sf:{wax};--ss:{metal};--a1:{metal};--a2:{wax};--a3:{metal};--sl:{metal}"
    if style == "foil":
        shield_vars = f"--sf:{C['fjord']};--ss:{metal};--a1:{metal};--a2:{C['fjord']};--a3:{metal};--sl:{metal}"
    if style == "ink":
        shield_vars = f"--sf:transparent;--ss:{metal};--a1:{metal};--a2:transparent;--a3:{metal};--sl:{metal}"
    if center == "shield":
        mid = f'<g style="{shield_vars}"><use href="#shield" x="67" y="58" width="66" height="81"/></g>'
    else:
        mid = (
            f'<g style="--h1:{metal};--h2:{metal};--h3:{metal};--ss:{metal}">'
            f'<use href="#hornstar" x="62" y="64" width="76" height="68"/></g>'
        )
    ring = ""
    if text:
        ring = (
            f'<text font-family="Noto Sans Runic" font-size="14.5" fill="{metal}" letter-spacing="5.2">'
            f'<textPath href="#ring-{uid}">{SEAL_TEXT}</textPath></text>'
        )
    defs = f'<path id="ring-{uid}" d="M100 100 m-75 0 a75 75 0 1 1 150 0 a75 75 0 1 1 -150 0"/>'

    if style == "wax":
        rnd = random.Random(sum(map(ord, uid)))
        pts = []
        n = 40
        for i in range(n):
            a = 2 * math.pi * i / n
            r = 95 + rnd.uniform(-2.2, 3.2) + (3.5 if i % 11 == 0 else 0)
            pts.append((100 + r * math.cos(a), 100 + r * math.sin(a)))
        d = f"M{(pts[0][0] + pts[-1][0]) / 2:.1f} {(pts[0][1] + pts[-1][1]) / 2:.1f}"
        for i in range(n):
            p, q = pts[i], pts[(i + 1) % n]
            d += f" Q{p[0]:.1f} {p[1]:.1f} {(p[0] + q[0]) / 2:.1f} {(p[1] + q[1]) / 2:.1f}"
        defs += (
            f'<radialGradient id="wg-{uid}" cx=".36" cy=".3" r=".85"><stop offset="0" stop-color="#9b2a24"/>'
            f'<stop offset=".55" stop-color="{wax}"/><stop offset="1" stop-color="#3d0a0a"/></radialGradient>'
            f'<radialGradient id="wp-{uid}" cx=".5" cy=".5" r=".5"><stop offset=".86" stop-color="#5a1010"/>'
            f'<stop offset="1" stop-color="#7d1b18"/></radialGradient>'
            f'<filter id="emb-{uid}"><feDropShadow dx="0" dy="-.8" stdDeviation=".3" flood-color="#000" flood-opacity=".55"/>'
            f'<feDropShadow dx="0" dy=".8" stdDeviation=".3" flood-color="#d9806a" flood-opacity=".35"/></filter>'
        )
        body = (
            f'<path d="{d}" fill="url(#wg-{uid})"/>'
            f'<circle cx="100" cy="100" r="86" fill="url(#wp-{uid})"/>'
            f'<circle cx="100" cy="100" r="86" fill="none" stroke="#2e0707" stroke-width="1.4" opacity=".7"/>'
            f'<g filter="url(#emb-{uid})">'
            f'<circle cx="100" cy="100" r="60" fill="none" stroke="{metal}" stroke-width="1"/>{ring}{mid}</g>'
        )
    elif style == "foil":
        body = (
            f'<circle cx="100" cy="100" r="97" fill="{C["fjord"]}"/>'
            f'<circle cx="100" cy="100" r="94" fill="none" stroke="{metal}" stroke-width="1.2"/>'
            f'<circle cx="100" cy="100" r="89" fill="none" stroke="{metal}" stroke-width=".5" opacity=".7"/>'
            f'<circle cx="100" cy="100" r="60" fill="none" stroke="{metal}" stroke-width="1"/>{ring}{mid}'
        )
    elif style == "ink":
        body = (
            f'<circle cx="100" cy="100" r="96" fill="none" stroke="{metal}" stroke-width="2.4"/>'
            f'<circle cx="100" cy="100" r="88" fill="none" stroke="{metal}" stroke-width=".8"/>'
            f'<circle cx="100" cy="100" r="60" fill="none" stroke="{metal}" stroke-width="1.4"/>{ring}{mid}'
        )
    else:  # flat — Forge II exactly
        body = (
            f'<circle cx="100" cy="100" r="97" fill="{wax}"/>'
            f'<circle cx="100" cy="100" r="92" fill="none" stroke="{rim}" stroke-width="2"/>'
            f'<circle cx="100" cy="100" r="60" fill="none" stroke="{metal}" stroke-width="1"/>{ring}{mid}'
        )
    if not text:
        body = body.replace(ring, "") if ring else body
    return (
        f'<svg class="seal {cls}" width="{size}" height="{size}" viewBox="0 0 200 200" role="img" '
        f'aria-label="The Graah seal"><defs>{defs}</defs>{body}</svg>'
    )


HORNS = f'<svg class="horns" viewBox="0 0 200 170" style="color:{C["brass"]}" aria-hidden="true"><use href="#horns-line"/></svg>'
BRAND = (
    f'<span class="brand"><svg width="22" height="20" viewBox="0 0 200 180" '
    f'style="--h1:{C["red"]};--h2:{C["steel"]};--h3:{C["brass"]};--ss:{C["brass"]}"><use href="#hornstar"/></svg>Graah</span>'
)


def hero(kind: str, full: bool = False) -> str:
    """kind: smithy | rising | crest | runes."""
    if full:
        nav = (
            f'<nav class="hnav">{BRAND}<span class="links"><a>Chronicle</a><a>The arms</a><a>Timeline</a><a>Sources</a></span>'
            f'<span class="lang">EN · SV · NO · DA</span></nav>'
        )
    else:
        nav = f'<nav class="hnav">{BRAND}<span class="mid">I — IX</span><span>1462 → now</span></nav>'

    tagline = '<p class="tag">Five centuries. Three kingdoms. One name.</p>'
    if kind == "smithy":
        copy = f'{HORNS}<h3 class="wm">GRAAH</h3>{glow_runes("under")}{tagline}'
        extra = ""
    elif kind == "crest":
        copy = f'{seal("crest", size=200, cls="crest-seal")}<h3 class="wm">GRAAH</h3>{glow_runes("under")}{tagline}'
        extra = ""
    elif kind == "rising":
        copy = f'<div class="kick">The family chronicle · MCDLXII</div><h3 class="wm">GRAAH</h3>{glow_runes("under")}{tagline}'
        extra = seal("rising", size=300, cls="rising-seal")
    else:  # runes
        copy = f'{glow_runes("giant")}<h3 class="wm small">GRAAH</h3>{tagline}'
        extra = ""

    cue = '<div class="cue">Chapter I · The Stolen Castle <span>↓</span></div>' if full else ""
    return f"""
<div class="hz hz-{kind}{' full' if full else ''}">
  {sky(7)}
  {extra}
  {ARC}
  <div class="hin">{nav}<div class="hcopy">{copy}</div>{cue}</div>
</div>"""


# ───────────────────────── page sections ─────────────────────────


def kept() -> str:
    tiles = [
        ("Night Smithy hero", "The starting page you loved — polar night, starfield, hairline aurora, brass horns. Kept as is, now set in Forum.",
         f'<div class="mini-hero">{hero("smithy")}</div>'),
        ("Forge II seal", "Oxblood wax, brass runes, the arms in the centre. The ring reads ᚴᚱᛅᛅᚼ ᛬ ᛋᚢᛚᛁᛋᛏᛁᛏ — <em>Graah · Søllested</em>: the name and the castle we lost.",
         seal("k1", size=150)),
        ("Glowing runes", "From Ember Arc. Now in brass so they belong to the night palette, with a slow breathing glow.",
         f'<div class="kept-runes">{glow_runes()}</div>'),
        ("Forum", "Roman capitals with a little warmth. Calmer and more neoclassical than Marcellus, so the Viking parts can do the talking.",
         '<div class="kept-forum">GRAAH<small>The Glacier You Must Not Name</small></div>'),
    ]
    out = "".join(f'<div class="kt"><div class="kart">{art}</div><h4>{t}</h4><p>{d}</p></div>' for t, d, art in tiles)
    return f'<div class="kept">{out}</div>'


def hero_variants() -> str:
    v = [
        ("smithy", "H1 · Smithy", "As you liked it. Horns over the wordmark, runes glowing beneath."),
        ("rising", "H2 · Seal rising", "The seal sits on the horizon like a sun coming up over the aurora. No horns."),
        ("crest", "H3 · Seal as crest", "The seal takes the horns' place above the name. More formal, more heraldic."),
        ("runes", "H4 · Runes first", "The glowing runes lead and the Latin name sits under them like a translation."),
    ]
    return '<div class="hgrid">' + "".join(
        f'<figure>{hero(k)}<figcaption><b>{t}</b>{d}</figcaption></figure>' for k, t, d in v
    ) + "</div>"


def seal_studies() -> str:
    items = [
        ("S1 · Forge II", "Exactly as you liked it. Flat oxblood, brass runes. For screens.", seal("s1", size=190)),
        ("S2 · Real wax", "Same seal, pressed into wax. Uneven edge, sunk centre, raised runes. For invitations and letters.", seal("s2", "wax", size=190)),
        ("S3 · Night foil", "Brass on deep fjord blue, like gold foil on a navy card. Belongs to the night palette.", seal("s3", "foil", size=190)),
        ("S4 · One ink", "One colour, lines only. Signet ring, embossing, letterpress, engraving.", seal("s4", "ink", size=190)),
    ]
    grid = "".join(f'<div class="st"><div class="sart">{art}</div><h4>{t}</h4><p>{d}</p></div>' for t, d, art in items)
    sizes = "".join(
        f'<div class="sz"><div>{seal("z" + str(s), size=s, text=s >= 64, center="shield" if s >= 40 else "hornstar")}</div><small>{s}px</small></div>'
        for s in (160, 96, 64, 40, 24)
    )
    centers = (
        f'<div class="centers"><div>{seal("c1", size=130)}<small>Arms in the centre</small></div>'
        f'<div>{seal("c2", size=130, center="hornstar")}<small>Horns &amp; star in the centre</small></div></div>'
    )
    return f"""
<div class="sgrid">{grid}</div>
<div class="srow">
  <div class="panel"><span class="label">Scale</span><div class="sizes">{sizes}</div>
    <p class="note">Below 64px the rune ring drops off. Below 40px the arms become the horns-and-star mark, which stays readable at favicon size.</p></div>
  <div class="panel"><span class="label">Centre</span>{centers}</div>
</div>"""


def rune_studies() -> str:
    glows = [
        ("Brass", "glow", "Recommended. Warm, quiet, part of the night palette."),
        ("Ember", "glow ember", "From Ember Arc. Hotter, for the fire chapter and film titles."),
        ("Aurora", "glow aurora", "Cold blue. For the Greenland chapter only."),
    ]
    g = "".join(
        f'<div class="gt"><span class="label">{n}</span><div class="gart"><span class="rune {c}">{RUNES}</span></div><p>{d}</p></div>'
        for n, c, d in glows
    )
    uses = f"""
<div class="uses">
  <div class="panel"><span class="label">Loader · runes light one by one</span><div class="uart">{glow_runes("load", seq=True)}</div></div>
  <div class="panel"><span class="label">Section divider</span><div class="uart"><div class="divider"><i></i>{glow_runes("small")}<i></i></div></div></div>
  <div class="panel"><span class="label">Link hover</span><div class="uart"><a class="glink" href="#runes">Read the chronicle →</a></div><p class="note">Hover it: the underline lights up like the runes.</p></div>
</div>"""
    return f'<div class="ggrid">{g}</div>{uses}'


def forum_studies() -> str:
    return f"""
<div class="fgrid">
  <div class="panel">
    <span class="label">Wordmark tracking</span>
    <div class="track"><span style="letter-spacing:.08em">GRAAH</span><small>.08em · tight, for small sizes</small></div>
    <div class="track"><span style="letter-spacing:.16em">GRAAH</span><small>.16em · hero (current)</small></div>
    <div class="track"><span style="letter-spacing:.32em">GRAAH</span><small>.32em · nav, seal, signature</small></div>
  </div>
  <div class="panel">
    <span class="label">Hierarchy · Forum has one weight, so size and spacing do the work</span>
    <div class="scale">
      <div style="font-size:64px;letter-spacing:.02em">The Glacier</div>
      <div style="font-size:40px">You Must Not Name</div>
      <div style="font-size:24px;letter-spacing:.14em;text-transform:uppercase">Chapter IV · Into the ice</div>
      <div class="mono">1828–1831 · EAST COAST OF GREENLAND</div>
    </div>
  </div>
</div>
<div class="pair">
  <div class="panel"><span class="label">Body option 1 · Geist (Night Smithy)</span><h5>Out of the Ashes</h5><p class="geist">For most men the fire would have been the end. For Knud Graah it was barely an intermission — every brick, bobbin and bale was insured.</p><small>Clean and modern. Leans futurist.</small></div>
  <div class="panel"><span class="label">Body option 2 · Newsreader</span><h5>Out of the Ashes</h5><p class="news">For most men the fire would have been the end. For Knud Graah it was barely an intermission — every brick, bobbin and bale was insured.</p><small>Bookish and warm. Leans chronicle.</small></div>
</div>"""


def palette() -> str:
    sw = [
        ("Polar Night", C["night"], "ground"), ("Deep Fjord", C["fjord"], "surface"), ("Fjord Line", C["line"], "rules"),
        ("Glacier", C["glacier"], "text"), ("Sea Smoke", C["smoke"], "muted"), ("Brass", C["brass"], "metal / action"),
        ("Rune Glow", C["glow"], "glow highlight"), ("Star Red", C["red"], "stars, one accent"), ("Wax", C["wax"], "the seal"),
        ("Steel Blue", C["steel"], "aurora / link"),
    ]
    tiles = "".join(f'<div class="sw"><i style="background:{h}"></i><b>{n}</b><small>{h} · {r}</small></div>' for n, h, r in sw)
    ratio = [(C["night"], 58), (C["fjord"], 16), (C["glacier"], 12), (C["brass"], 6), (C["wax"], 3), (C["red"], 2), (C["steel"], 3)]
    bar = "".join(f'<span style="flex:{f};background:{c}"></span>' for c, f in ratio)
    return f'<div class="panel"><div class="swatches">{tiles}</div><div class="ratio">{bar}</div><p class="note">Usage by area: about 75% night and fjord, 12% glacier text, and brass, wax, red and steel together under 15%.</p></div>'


def page_preview() -> str:
    ch = EN["chapters"][3]
    record = "".join(f'<li><span>{r["year"]}</span>{r["text"]}</li>' for r in ch["record"])
    stops = EN["timelineSection"]["stops"]
    pick = [stops[i] for i in (0, 1, 4, 6, 10, len(stops) - 2)]
    tl = "".join(f'<div class="stop"><i></i><b>{s["year"]}</b><span>{s["text"]}</span></div>' for s in pick)
    stats = "".join(
        f'<div class="stat"><span class="v">{s["value"]}</span><span class="k">{s["label"]}</span></div>' for s in EN["chronicleStats"]
    )
    return f"""
<div class="site">
  {hero("smithy", full=True)}
  <section class="s-intro">
    <div class="divider"><i></i>{glow_runes("small")}<i></i></div>
    <p class="big">{EN['hero']['intro']}</p>
    <p class="em">{EN['hero']['introEmphasis']}</p>
  </section>
  <section class="s-chapter">
    <div class="ch-head">
      <span class="numeral">{ch['numeral']}</span>
      <div><div class="mono">{ch['years']} · {ch['place']}</div><h3>{ch['title']}</h3><p class="kicker">{ch['kicker']}</p></div>
    </div>
    <div class="ch-body">
      <div class="ch-text"><p>{ch['paragraphs'][0]}</p><p>{ch['paragraphs'][1]}</p>
        <span class="chip"><i></i>{ch['mood']['label']}</span></div>
      <aside>
        <figure class="ch-fig"><img src="{ch['image']['src']}" alt="{ch['image']['alt']}" loading="lazy"/><figcaption>{ch['image']['caption']}</figcaption></figure>
        <div class="receipts"><span class="label">{EN['chapterRecordHeading']}</span><ul>{record}</ul></div>
      </aside>
    </div>
  </section>
  <section class="s-stats"><div class="stats">{stats}</div></section>
  <section class="s-tl"><span class="label">{EN['timelineSection']['eyebrow']}</span><h3>{EN['timelineSection']['title']}</h3><div class="tl">{tl}</div></section>
  <footer class="s-foot">
    {seal("foot", size=120)}
    <div><div class="fwm">GRAAH</div>{glow_runes("small")}<p>Told the way the family tells it — the good parts kept in.</p></div>
    <div class="flinks"><a>Chronicle</a><a>The arms</a><a>Timeline</a><a>Sources</a></div>
  </footer>
</div>"""


# ───────────────────────── css ─────────────────────────

CSS = r"""
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:#0B0F1A;color:#DCE6EE;font-family:Geist,system-ui,sans-serif;-webkit-font-smoothing:antialiased;font-variant-numeric:lining-nums}
h1,h2,h3,h4,h5,p,figure{margin:0}
svg{display:block}
a{color:inherit}
.wrap{max-width:1240px;margin:0 auto;padding:0 28px}
.rune{font-family:"Noto Sans Runic",sans-serif}
.label{display:block;font:500 11px/1.4 "Geist Mono",monospace;letter-spacing:.2em;text-transform:uppercase;color:#8EA0B8;margin-bottom:16px}
.note{font:400 13px/1.55 Geist;color:#8EA0B8;margin-top:16px}
.panel{background:#111829;border:1px solid #26304A;padding:26px}
.mono{font:400 12px/1.4 "Geist Mono";letter-spacing:.16em;text-transform:uppercase;color:#C9A15E}

/* glowing runes */
.glow{color:#E9C98A;text-shadow:0 0 6px rgba(233,201,138,.55),0 0 22px rgba(201,161,94,.45);animation:breathe 5s ease-in-out infinite}
.glow.ember{color:#F0B44C;text-shadow:0 0 6px rgba(240,180,76,.7),0 0 26px rgba(210,56,43,.45)}
.glow.aurora{color:#C3D2FF;text-shadow:0 0 6px rgba(160,185,255,.6),0 0 26px rgba(62,98,184,.6)}
@keyframes breathe{50%{text-shadow:0 0 3px rgba(233,201,138,.35),0 0 12px rgba(201,161,94,.25)}}
.glow.ember{animation-name:breathe-e}.glow.aurora{animation-name:breathe-a}
@keyframes breathe-e{50%{text-shadow:0 0 3px rgba(240,180,76,.4),0 0 12px rgba(210,56,43,.25)}}
@keyframes breathe-a{50%{text-shadow:0 0 3px rgba(160,185,255,.35),0 0 12px rgba(62,98,184,.3)}}
.seq span{color:#3a4258;animation:lit 2.8s ease-in-out infinite}
@keyframes lit{0%,100%{color:#3a4258;text-shadow:none}30%,60%{color:#E9C98A;text-shadow:0 0 6px rgba(233,201,138,.6),0 0 20px rgba(201,161,94,.5)}}
.tw{animation:twinkle 4.5s ease-in-out infinite}
@keyframes twinkle{50%{opacity:.08}}
.aur{animation:aur 9s ease-in-out infinite}
@keyframes aur{50%{opacity:.22}}

/* ───── hero (container-query sized, so the same hero works full-bleed or as a thumbnail) ───── */
.hz{container-type:inline-size;position:relative;overflow:hidden;background:radial-gradient(120% 90% at 50% 120%,#1b2c52 0%,#0f1830 38%,#0B0F1A 70%);aspect-ratio:16/10;border:1px solid #26304A}
.hz.full{aspect-ratio:auto;min-height:min(100svh,880px);border:0;border-bottom:1px solid #26304A}
.hz .sky{position:absolute;inset:0;width:100%;height:100%}
.hz .arc{position:absolute;left:-4%;width:108%;bottom:0;height:30cqw;z-index:2}
.hin{position:relative;z-index:3;display:flex;flex-direction:column;height:100%;min-height:inherit}
.hz.full .hin{min-height:min(100svh,880px)}
.hnav{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:max(14px,2.2cqw) max(16px,2.4cqw);font:400 max(9px,.85cqw)/1 "Geist Mono";letter-spacing:.2em;text-transform:uppercase;color:#8EA0B8}
.hnav .brand{display:flex;gap:10px;align-items:center;color:#DCE6EE;font:400 max(12px,1.15cqw)/1 Forum;letter-spacing:.32em}
.hnav .links{display:flex;gap:2.4cqw}
.hnav .links a{cursor:pointer}
.hcopy{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 16px 13cqw}
.hz .horns{width:clamp(56px,11cqw,170px);height:auto;margin-bottom:-.3cqw}
.wm{font:400 clamp(48px,13.5cqw,196px)/.9 Forum,serif;letter-spacing:.16em;padding-left:.16em;color:#F2F6F9;margin:0}
.wm.small{font-size:clamp(22px,4.4cqw,64px);letter-spacing:.5em;padding-left:.5em;color:#DCE6EE;margin-top:1.6cqw}
.rune.under{font-size:clamp(15px,1.9cqw,28px);letter-spacing:1em;padding-left:1em;margin-top:1.1cqw}
.rune.giant{font-size:clamp(38px,9cqw,132px);letter-spacing:.45em;padding-left:.45em;line-height:1}
.tag{font:400 clamp(9px,1cqw,15px)/1.4 "Geist Mono";letter-spacing:.2em;text-transform:uppercase;color:#A6B3C4;margin-top:clamp(12px,2.2cqw,32px)}
.kick{font:400 clamp(9px,.9cqw,12px)/1 "Geist Mono";letter-spacing:.3em;text-transform:uppercase;color:#C9A15E;margin-bottom:1.6cqw}
.crest-seal{width:clamp(70px,12cqw,180px);height:auto;margin-bottom:1.6cqw;filter:drop-shadow(0 0 2cqw rgba(201,161,94,.18))}
.hz-rising .hcopy{justify-content:flex-start;padding-top:5cqw}
.rising-seal{position:absolute;z-index:1;left:50%;width:24cqw;height:24cqw;bottom:1cqw;transform:translateX(-50%);filter:drop-shadow(0 0 3cqw rgba(201,161,94,.35))}
@container (max-width:560px){.tag{display:none}.hz .horns{width:13cqw}}
.cue{text-align:center;padding:0 0 26px;font:400 11px/1 "Geist Mono";letter-spacing:.2em;text-transform:uppercase;color:#8EA0B8;position:relative;z-index:3}
.cue span{display:block;margin-top:10px;color:#C9A15E}

/* intro */
.intro{padding:72px 0 56px}
.eyebrow{font:500 12px/1.5 "Geist Mono";letter-spacing:.2em;text-transform:uppercase;color:#8EA0B8}
.eyebrow a{color:#C9A15E}
.intro h1{font:400 clamp(46px,7vw,96px)/.95 Forum;letter-spacing:.02em;margin:20px 0 22px;color:#F2F6F9}
.intro h1 em{font-style:normal;color:#E9C98A;text-shadow:0 0 24px rgba(201,161,94,.45)}
.lede{max-width:780px;font:300 18px/1.6 Geist;color:#A6B3C4}
.kept{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:1px;background:#26304A;border:1px solid #26304A;margin-top:40px}
.kt{background:#0e1424;padding:22px;display:flex;flex-direction:column;gap:14px}
.kart{min-height:170px;display:flex;align-items:center;justify-content:center}
.kt h4{font:500 11px/1.3 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#C9A15E}
.kt p{font:300 14px/1.55 Geist;color:#A6B3C4}
.kt p em{color:#DCE6EE;font-style:normal}
.mini-hero{width:100%}
.mini-hero .hz{border-color:#26304A}
.kept-runes .rune{font-size:40px;letter-spacing:.4em;padding-left:.4em}
.kept-forum{font:400 54px/1 Forum;letter-spacing:.14em;text-align:center;color:#F2F6F9}
.kept-forum small{display:block;font-size:17px;letter-spacing:.02em;color:#A6B3C4;margin-top:12px}
.toc{display:flex;flex-wrap:wrap;gap:10px;margin-top:30px}
.toc a{font:500 12px/1 "Geist Mono";letter-spacing:.12em;text-transform:uppercase;text-decoration:none;border:1px solid #26304A;padding:11px 14px;border-radius:999px}
.toc a:hover{border-color:#C9A15E;color:#C9A15E}

/* section scaffolding */
.sec{padding:80px 0;border-top:1px solid #26304A}
.sec>.wrap>h2{font:400 clamp(40px,5.6vw,72px)/1 Forum;letter-spacing:.02em;color:#F2F6F9;margin:12px 0 14px}
.sec>.wrap>.lede{margin-bottom:34px}
.code{font:500 12px/1 "Geist Mono";letter-spacing:.2em;text-transform:uppercase;color:#C9A15E}

/* hero variants */
.hgrid{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.hgrid figcaption{font:300 14px/1.5 Geist;color:#A6B3C4;margin-top:12px}
.hgrid figcaption b{display:block;font:500 11px/1.3 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#C9A15E;margin-bottom:6px}

/* seals */
.sgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#26304A;border:1px solid #26304A}
.st{padding:26px 22px;display:flex;flex-direction:column;gap:14px}
.st:nth-child(1),.st:nth-child(3){background:#0e1424}
.st:nth-child(2){background:radial-gradient(circle at 50% 35%,#2a2420,#1a1512)}
.st:nth-child(4){background:#ECE5D8}
.st:nth-child(4) h4{color:#6E1414}.st:nth-child(4) p{color:#4C4740}
.sart{height:220px;display:flex;align-items:center;justify-content:center}
.st:nth-child(2) .seal{filter:drop-shadow(0 6px 10px rgba(0,0,0,.55))}
.st h4{font:500 11px/1.3 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#C9A15E}
.st p{font:300 14px/1.5 Geist;color:#A6B3C4}
.srow{display:grid;grid-template-columns:1.5fr 1fr;gap:28px;margin-top:28px}
.sizes{display:flex;align-items:flex-end;gap:22px;flex-wrap:wrap}
.sz{display:flex;flex-direction:column;align-items:center;gap:8px}
.sz small,.centers small{font:400 11px/1 "Geist Mono";color:#8EA0B8}
.centers{display:flex;gap:26px;justify-content:center}
.centers>div{display:flex;flex-direction:column;align-items:center;gap:12px}

/* runes */
.ggrid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.gt{background:#080b14;border:1px solid #26304A;padding:24px}
.gart{height:150px;display:flex;align-items:center;justify-content:center}
.gart .rune{font-size:46px;letter-spacing:.4em;padding-left:.4em}
.gt p{font:300 14px/1.5 Geist;color:#A6B3C4}
.uses{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;margin-top:28px}
.uart{height:90px;display:flex;align-items:center;justify-content:center}
.rune.load{font-size:34px;letter-spacing:.5em;padding-left:.5em}
.rune.small{font-size:16px;letter-spacing:.8em;padding-left:.8em}
.divider{display:flex;align-items:center;gap:18px;width:100%}
.divider i{flex:1;height:1px;background:linear-gradient(90deg,transparent,#C9A15E)}
.divider i:last-child{background:linear-gradient(90deg,#C9A15E,transparent)}
.glink{font:400 24px/1 Forum;letter-spacing:.04em;text-decoration:none;padding-bottom:6px;background:linear-gradient(#C9A15E,#C9A15E) 0 100%/100% 1px no-repeat;transition:all .4s}
.glink:hover{color:#E9C98A;background-image:linear-gradient(#E9C98A,#E9C98A);filter:drop-shadow(0 0 8px rgba(233,201,138,.6))}

/* forum */
.fgrid{display:grid;grid-template-columns:1fr 1.3fr;gap:28px}
.track{display:flex;flex-direction:column;gap:6px;padding:14px 0;border-top:1px solid #26304A}
.track span{font:400 46px/1 Forum;color:#F2F6F9}
.track small{font:400 11px/1 "Geist Mono";color:#8EA0B8}
.scale{display:grid;gap:14px;font-family:Forum;color:#F2F6F9;line-height:1}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:28px}
.pair h5{font:400 34px/1 Forum;color:#F2F6F9;margin-bottom:12px}
.pair p{color:#C5D0DC;margin-bottom:12px}
.pair small{font:400 11px/1 "Geist Mono";letter-spacing:.1em;text-transform:uppercase;color:#C9A15E}
.geist{font:300 17px/1.65 Geist}
.news{font:400 18px/1.6 Newsreader}

/* palette */
.swatches{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}
.sw{display:flex;flex-direction:column;gap:7px}
.sw i{display:block;height:84px;border-radius:2px;box-shadow:inset 0 0 0 1px rgba(220,230,238,.12)}
.sw b{font:600 13px/1.2 Geist}
.sw small{font:400 11px/1.3 "Geist Mono";color:#8EA0B8}
.ratio{display:flex;height:12px;margin-top:18px;border-radius:2px;overflow:hidden;box-shadow:0 0 0 1px rgba(220,230,238,.12)}

/* site preview */
.site{border:1px solid #26304A;background:#0B0F1A}
.s-intro{max-width:880px;margin:0 auto;padding:90px 28px 70px;text-align:center}
.s-intro .divider{max-width:420px;margin:0 auto 40px}
.s-intro .big{font:400 clamp(26px,3vw,38px)/1.3 Forum;color:#F2F6F9}
.s-intro .em{font:400 13px/1.5 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#C9A15E;margin-top:24px}
.s-chapter{padding:70px 56px;border-top:1px solid #26304A;background:#0d1220}
.ch-head{display:flex;gap:28px;align-items:flex-end;margin-bottom:40px}
.numeral{font:400 clamp(90px,12vw,160px)/.8 Forum;color:transparent;-webkit-text-stroke:1px #C9A15E}
.ch-head h3{font:400 clamp(36px,4.6vw,62px)/1 Forum;color:#F2F6F9;margin:12px 0 10px}
.kicker{font:300 18px/1.45 Geist;color:#A6B3C4}
.ch-body{display:grid;grid-template-columns:1.25fr 1fr;gap:48px}
.ch-text p{font:300 17px/1.7 Geist;color:#C5D0DC;margin-bottom:18px}
.chip{display:inline-flex;align-items:center;gap:9px;font:500 11px/1 "Geist Mono";letter-spacing:.14em;text-transform:uppercase;padding:9px 13px;border:1px solid #26304A;border-radius:999px}
.chip i{width:7px;height:7px;border-radius:50%;background:#C8283A}
.ch-fig{border:1px solid #26304A;padding:10px;background:#111829}
.ch-fig img{display:block;width:100%;height:auto;filter:saturate(.8) contrast(1.02)}
.ch-fig figcaption{font:400 11px/1.5 "Geist Mono";letter-spacing:.04em;color:#8EA0B8;padding:10px 2px 2px}
.receipts{margin-top:26px}
.receipts ul{list-style:none;padding:0;margin:0}
.receipts li{display:grid;grid-template-columns:56px 1fr;gap:12px;padding:10px 0;border-top:1px solid #26304A;font:300 14px/1.45 Geist;color:#C5D0DC}
.receipts li span{font:400 12px/1.6 "Geist Mono";color:#C9A15E}
.s-stats{padding:0 56px 70px;background:#0d1220}
.stats{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid #26304A;background:#111829}
.stat{padding:24px 22px}
.stat+.stat{border-left:1px solid #26304A}
.stat .v{display:block;font:400 60px/.9 Forum;color:#E9C98A;margin-bottom:10px}
.stat .k{display:block;font:500 11px/1.35 "Geist Mono";letter-spacing:.14em;text-transform:uppercase;color:#8EA0B8}
.s-tl{padding:70px 56px;border-top:1px solid #26304A}
.s-tl h3{font:400 52px/1 Forum;color:#F2F6F9;margin-bottom:40px}
.tl{display:grid;grid-template-columns:repeat(6,1fr);position:relative}
.tl::before{content:"";position:absolute;left:0;right:0;top:5px;height:1px;background:linear-gradient(90deg,#3E62B8,#C9A15E 50%,#C8283A)}
.stop{position:relative;padding-right:16px}
.stop i{display:block;width:11px;height:11px;border-radius:50%;background:#0B0F1A;border:1px solid #C9A15E;margin-bottom:16px;position:relative}
.stop:last-child i{background:#C9A15E;box-shadow:0 0 12px rgba(233,201,138,.7)}
.stop b{display:block;font:400 30px/1 Forum;color:#F2F6F9;margin-bottom:8px}
.stop span{font:300 13px/1.45 Geist;color:#A6B3C4}
.s-foot{display:grid;grid-template-columns:auto 1fr auto;gap:36px;align-items:center;padding:48px 56px;border-top:1px solid #26304A;background:#080b14}
.fwm{font:400 30px/1 Forum;letter-spacing:.32em;color:#F2F6F9;margin-bottom:10px}
.s-foot p{font:300 14px/1.5 Geist;color:#8EA0B8;margin-top:12px}
.flinks{display:grid;gap:10px;font:400 11px/1 "Geist Mono";letter-spacing:.16em;text-transform:uppercase;color:#A6B3C4}

/* questions */
.qs{display:grid;grid-template-columns:repeat(4,1fr);gap:28px}
.qs div{border-top:1px solid #26304A;padding-top:16px}
.qs h4{font:500 11px/1.3 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#C9A15E;margin-bottom:10px}
.qs p{font:300 15px/1.55 Geist;color:#C5D0DC}
footer.page{padding:30px 0 60px;font:400 12px/1.6 "Geist Mono";color:#5d6a80;border-top:1px solid #26304A}
footer.page a{color:#8EA0B8}

@media (max-width:960px){
  .wrap{padding:0 18px}
  .kept{grid-template-columns:1fr 1fr}
  .kt:first-child{grid-column:1/-1}
  .hgrid,.srow,.fgrid,.pair,.ggrid,.uses,.ch-body,.qs{grid-template-columns:1fr}
  .hz{aspect-ratio:4/5}
  .hz.full{aspect-ratio:auto}
  .hz .arc{height:44cqw}
  .rising-seal{width:44cqw;height:44cqw;bottom:-2cqw}
  .hcopy{padding-bottom:22cqw}
  .hnav .links{display:none}
  .hnav .mid{display:none}
  .sgrid{grid-template-columns:1fr 1fr}
  .swatches{grid-template-columns:repeat(2,1fr)}
  .s-chapter,.s-stats,.s-tl{padding-left:20px;padding-right:20px}
  .s-foot{grid-template-columns:1fr;padding:40px 20px}
  .stats{grid-template-columns:1fr 1fr}
  .stat:nth-child(3){border-left:0}
  .stat:nth-child(n+3){border-top:1px solid #26304A}
  .tl{grid-template-columns:1fr 1fr;row-gap:28px}
  .tl::before{display:none}
  .ch-head{flex-direction:column;align-items:flex-start;gap:10px}
}
@media (max-width:560px){
  .kept,.sgrid{grid-template-columns:1fr}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important;transition:none!important}
  .seq span{color:#E9C98A}
}
"""

FONTS = (
    "https://fonts.googleapis.com/css2?family=Forum&family=Geist:wght@300..700&family=Geist+Mono:wght@400;500"
    "&family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400&family=Noto+Sans+Runic&display=swap"
)


def page() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="robots" content="noindex, nofollow" />
<meta name="theme-color" content="#0B0F1A" />
<link rel="icon" href="/graah-coa.png" type="image/png" />
<title>Graah — Identity exploration v0.3 · Night Smithy</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="{FONTS}" rel="stylesheet" />
<style>{CSS}</style>
</head>
<body>
{DEFS}
<section class="intro">
  <div class="wrap">
    <div class="eyebrow">Graah · Visual identity · v0.3 · <a href="/theme-lab/v2/">v0.2 (five permutations)</a> · <a href="/theme-lab/v1/">v0.1 (four directions)</a></div>
    <h1>Night Smithy,<br/><em>sealed.</em></h1>
    <p class="lede">This round narrows to one direction. The base is the Night Smithy starting page. Added on top: the Forge II seal, the glowing runes and Forum as the display font. Below are four hero layouts, four seal finishes, rune and type studies, and a preview of what the real site would look like with your chronicle in it.</p>
    {kept()}
    <nav class="toc"><a href="#heroes">Hero layouts</a><a href="#seal">The seal</a><a href="#runes">Glowing runes</a><a href="#forum">Forum</a><a href="#palette">Palette</a><a href="#preview">Site preview</a><a href="#next">Next</a></nav>
  </div>
</section>

<section class="sec" id="heroes"><div class="wrap">
  <div class="code">01 · Hero layouts</div><h2>Four ways to open the door</h2>
  <p class="lede">Same sky, aurora, runes and Forum wordmark each time. Only the emblem above or behind the name changes.</p>
  {hero_variants()}
</div></section>

<section class="sec" id="seal"><div class="wrap">
  <div class="code">02 · The seal</div><h2>The Forge II seal, four finishes</h2>
  <p class="lede">The design stays the same. Only the material changes for where it's used: on screen, wax, foil or a signet ring.</p>
  {seal_studies()}
</div></section>

<section class="sec" id="runes"><div class="wrap">
  <div class="code">03 · Glowing runes</div><h2><span class="rune glow" style="font-size:.7em;letter-spacing:.3em">{RUNES}</span></h2>
  <p class="lede">GRAAH in Younger Futhark: kaun, reið, ár, ár, hagall. The glow breathes slowly. It's switched off for anyone who has reduced motion turned on.</p>
  {rune_studies()}
</div></section>

<section class="sec" id="forum"><div class="wrap">
  <div class="code">04 · Forum</div><h2>Forum for everything that speaks</h2>
  <p class="lede">Forum sets the wordmark, headlines, numerals and stats. Geist Mono handles dates, places and labels. The open choice is the body text: Geist or Newsreader.</p>
  {forum_studies()}
</div></section>

<section class="sec" id="palette"><div class="wrap">
  <div class="code">05 · Palette</div><h2>Polar night, brass and wax</h2>
  <p class="lede">Night Smithy's colours plus two additions: wax oxblood from the seal and a lighter brass for the rune glow.</p>
  {palette()}
</div></section>

<section class="sec" id="preview"><div class="wrap">
  <div class="code">06 · Site preview</div><h2>graah.se, in the new skin</h2>
  <p class="lede">Real chronicle content: the hero, the intro, chapter IV with its engraving and receipts, the stats, the timeline and a footer with the seal. Text and structure are as on the site today.</p>
</div>
<div class="wrap">{page_preview()}</div></section>

<section class="sec" id="next"><div class="wrap">
  <div class="code">07 · Next</div><h2>What to send back</h2>
  <div class="qs">
    <div><h4>1 · Hero</h4><p>H1 Smithy, H2 Seal rising, H3 Seal as crest, or H4 Runes first?</p></div>
    <div><h4>2 · Seal centre</h4><p>The arms or the horns-and-star in the middle? The ring text Graah · Søllested: keep it or change it?</p></div>
    <div><h4>3 · Body font</h4><p>Geist (cleaner, more future) or Newsreader (warmer, more chronicle)?</p></div>
    <div><h4>4 · Go live?</h4><p>If this is the direction, the next step is to rebuild graah.se in it, in all eight languages.</p></div>
  </div>
</div></section>
<footer class="page"><div class="wrap">Exploration only — graah.se itself is unchanged. Generated by design/theme-lab/build_v3.py. Fonts: Google Fonts (OFL).</div></footer>
</body>
</html>
"""


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page(), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")
