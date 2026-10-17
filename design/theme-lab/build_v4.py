#!/usr/bin/env python3
"""Generate public/theme-lab/index.html — Graah identity exploration, iteration 4.

Shield studies: minimalist, modernised variations of the Graah arms.
Every variant keeps the two non-negotiables: the rainbow arc and the three stars.

Run:  python3 design/theme-lab/build_v4.py
Pure stdlib. Each variant is drawn in a 200×240 box and rendered with a palette
(colour on night, colour on paper, one-colour brass, one-colour ink).
"""

from __future__ import annotations

import itertools
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_v2 import DEFS, RUNES  # noqa: E402
from build_v3 import ARC, CSS as V3CSS, glow_runes, sky  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "public" / "theme-lab" / "v4" / "index.html"

_uid = itertools.count(1)
SEAL_TEXT = "ᚴᚱᛅᛅᚼ ᛬ ᛋᚢᛚᛁᛋᛏᛁᛏ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᛋᚢᛚᛁᛋᛏᛁᛏ ᛬"

# ───────────────────────── palettes ─────────────────────────

ARMS = dict(field="#EEF1F4", a1="#2F55D4", a2="#E9B824", a3="#D0222F", star="#D0222F")
NIGHT = dict(ARMS, line="#0B0F1A", ink="#DCE6EE", metal="#C9A15E", bg="#0B0F1A", light=False, mono=False)
PAPER = dict(ARMS, line="#1C1A18", ink="#1C1A18", metal="#8C6A2F", bg="#F4F0E8", light=True, mono=False)


def mono(color: str, bg: str, light: bool) -> dict:
    return dict(field="none", a1=color, a2=color, a3=color, star=color, line=color, ink=color, metal=color,
                bg=bg, light=light, mono=True)


BRASS = mono("#C9A15E", "#0B0F1A", False)
INK = mono("#1C1A18", "#F4F0E8", True)
WAXBRASS = mono("#C9A15E", "#6E1414", False)

# ───────────────────────── geometry ─────────────────────────

SHAPES = dict(
    heritage="M20 32 Q20 16 36 16 H164 Q180 16 180 32 V116 C180 172 152 206 100 226 C48 206 20 172 20 116 Z",
    geo="M24 20 H176 V112 A150 150 0 0 1 100 228 A150 150 0 0 1 24 112 Z",
    ushape="M24 20 H176 V124 A76 76 0 0 1 24 124 Z",
    facet="M44 18 H156 L182 44 V126 L100 230 L18 126 V44 Z",
    kite="M100 14 C152 14 182 32 182 72 C182 140 142 196 100 232 C58 196 18 140 18 72 C18 32 48 14 100 14 Z",
    round="M8 120 A92 92 0 1 0 192 120 A92 92 0 1 0 8 120 Z",
)


def star_pts(cx: float, cy: float, R: float, ratio: float = 0.42) -> str:
    pts = []
    for i in range(12):
        a = math.radians(-90 + i * 30)
        r = R if i % 2 == 0 else R * ratio
        pts.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
    return " ".join(pts)


def stars(pos, R, ratio, fill, extra=""):
    out = []
    for p in pos:
        r = p[2] if len(p) > 2 else R
        out.append(f'<polygon points="{star_pts(p[0], p[1], r, ratio)}" fill="{fill}" {extra}/>')
    return "".join(out)


def bend(y, rise):
    return f"M-20 {y:.1f} Q100 {y - 2 * rise:.1f} 220 {y:.1f}"


def bands(p, y_edge, rise, s, w=None, mono_w=0.6, cols=None, extra=""):
    """Three parallel bands following a gentle arch. Mono: gaps so the three stay readable."""
    w = w or s
    if p["mono"]:
        w = s * mono_w
    cols = cols or (p["a1"], p["a2"], p["a3"])
    return "".join(
        f'<path d="{bend(y_edge + i * s, rise)}" stroke="{cols[i]}" stroke-width="{w:.1f}" fill="none" {extra}/>'
        for i in range(3)
    )


def wrap(inner: str, h: int, label: str = "Graah arms", cls: str = "") -> str:
    w = round(h * 200 / 240)
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} width="{w}" height="{h}" viewBox="0 0 200 240" role="img" aria-label="{label}">{inner}</svg>'


# ───────────────────────── variants ─────────────────────────
# Each returns the inner SVG markup for a 200×240 box.


def v_heritage(p):
    u = next(_uid)
    d = SHAPES["heritage"]
    field = "none" if p["mono"] else "#F2F3F5"
    cols = (p["a1"], p["a2"], p["a3"]) if p["mono"] else ("#2B4FD8", "#F5C518", "#D11A2A")
    seams = "" if p["mono"] else "".join(
        f'<path d="{bend(120 + i * 16, 26)}" stroke="#1A1A1E" stroke-width="2.5" fill="none"/>' for i in range(4)
    )
    sfill = p["star"] if p["mono"] else "#D11A2A"
    sstroke = "" if p["mono"] else 'stroke="#1A1A1E" stroke-width="2.5" stroke-linejoin="round"'
    line = p["ink"] if p["mono"] else "#1A1A1E"
    return (
        f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath></defs>'
        f'<path d="{d}" fill="{field}"/>'
        f'<g clip-path="url(#c{u})">{bands(p, 128, 26, 16, cols=cols)}{seams}</g>'
        + stars([(60, 60), (140, 60), (100, 186)], 25, 0.5, sfill, sstroke)
        + f'<path d="{d}" fill="none" stroke="{line}" stroke-width="5"/>'
    )


def v_flat(p):
    u = next(_uid)
    d = SHAPES["geo"]
    field = "none" if p["mono"] else ("#E3E8ED" if p["light"] else p["field"])
    outline = f'<path d="{d}" fill="none" stroke="{p["ink"]}" stroke-width="5"/>' if p["mono"] else ""
    return (
        f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath></defs>'
        f'<path d="{d}" fill="{field}"/>'
        f'<g clip-path="url(#c{u})">{bands(p, 132, 26, 15)}</g>'
        + stars([(64, 62), (136, 62), (100, 186)], 24, 0.42, p["star"])
        + outline
    )


def v_hairline(p):
    u = next(_uid)
    d = SHAPES["geo"]
    return (
        f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath></defs>'
        f'<g clip-path="url(#c{u})">{bands(p, 140, 26, 10, w=3.6, mono_w=0.36)}</g>'
        + stars([(68, 66), (132, 66), (100, 184)], 17, 0.42, p["star"])
        + f'<path d="{d}" fill="none" stroke="{p["ink"]}" stroke-width="2.6"/>'
    )


def v_rainbow(p):
    u = next(_uid)
    d = SHAPES["ushape"]
    field = "none" if p["mono"] else ("#E3E8ED" if p["light"] else p["field"])
    w = 8 if p["mono"] else 13
    arcs = "".join(
        f'<path d="M{100 - r} 168 A{r} {r} 0 0 1 {100 + r} 168" stroke="{c}" stroke-width="{w}" fill="none"/>'
        for r, c in ((64, p["a1"]), (51, p["a2"]), (38, p["a3"]))
    )
    outline = f'<path d="{d}" fill="none" stroke="{p["ink"]}" stroke-width="5"/>' if p["mono"] else ""
    return (
        f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath></defs>'
        f'<path d="{d}" fill="{field}"/>'
        f'<g clip-path="url(#c{u})">{arcs}</g>'
        + stars([(58, 58), (142, 58), (100, 152, 15)], 18, 0.42, p["star"])
        + outline
    )


def v_polar(p):
    u = next(_uid)
    d = SHAPES["geo"]
    if p["mono"]:
        return v_hairline(p)
    cols = ("#4A72E8", "#E2B64E", "#E0364A")
    return (
        f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath></defs>'
        f'<path d="{d}" fill="#111829"/>'
        f'<g clip-path="url(#c{u})">{bands(p, 134, 26, 12, cols=cols)}</g>'
        + stars([(64, 62), (136, 62), (100, 186)], 22, 0.42, "#EEF1F4")
        + f'<path d="{d}" fill="none" stroke="#C9A15E" stroke-width="2.4"/>'
        + f'<path d="{d}" fill="none" stroke="#C9A15E" stroke-width=".8" transform="translate(100 124) scale(.93) translate(-100 -124)" opacity=".6"/>'
    )


def v_facet(p):
    u = next(_uid)
    d = SHAPES["facet"]
    pos = [(66, 66), (134, 66), (100, 188)]
    R = 23
    if p["mono"]:
        return (
            f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath></defs>'
            f'<g clip-path="url(#c{u})">{bands(p, 134, 30, 15)}</g>'
            + stars(pos, R, 0.42, p["star"])
            + f'<path d="{d}" fill="none" stroke="{p["ink"]}" stroke-width="5" stroke-linejoin="round"/>'
        )
    shade = "".join(
        f'<clipPath id="h{u}_{i}"><rect x="{x}" y="{y - R}" width="{R}" height="{2 * R}"/></clipPath>' for i, (x, y) in enumerate(pos)
    )
    halves = "".join(
        f'<polygon points="{star_pts(x, y, R)}" fill="#000" opacity=".22" clip-path="url(#h{u}_{i})"/>' for i, (x, y) in enumerate(pos)
    )
    field = "#E3E8ED" if p["light"] else "#F2F4F6"
    edge = f'<path d="{d}" fill="none" stroke="{p["line"]}" stroke-width="1.5" stroke-linejoin="round"/>' if p["light"] else ""
    return (
        f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath>{shade}</defs>'
        f'<path d="{d}" fill="{field}"/>'
        f'<g clip-path="url(#c{u})">{bands(p, 134, 30, 15)}'
        f'<rect x="100" y="0" width="100" height="240" fill="#0B0F1A" opacity=".13"/>'
        f'<line x1="100" y1="0" x2="100" y2="240" stroke="#fff" stroke-width=".8" opacity=".5"/></g>'
        + stars(pos, R, 0.42, p["star"])
        + halves
        + edge
    )


def v_engraved(p):
    """Heraldic hatching (Petra Sancta): azure = horizontal, or = dots, gules = vertical. One colour by nature."""
    u = next(_uid)
    d = SHAPES["heritage"]
    ink = p["metal"] if not p["mono"] and not p["light"] else p["ink"]
    pats = (
        f'<pattern id="hz{u}" width="5" height="5" patternUnits="userSpaceOnUse"><path d="M0 2.5 H5" stroke="{ink}" stroke-width="1.3"/></pattern>'
        f'<pattern id="dt{u}" width="5" height="5" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r="1.05" fill="{ink}"/></pattern>'
        f'<pattern id="vt{u}" width="5" height="5" patternUnits="userSpaceOnUse"><path d="M2.5 0 V5" stroke="{ink}" stroke-width="1.3"/></pattern>'
        f'<pattern id="vs{u}" width="2.6" height="5" patternUnits="userSpaceOnUse"><path d="M1.3 0 V5" stroke="{ink}" stroke-width=".8"/></pattern>'
    )
    hatch = "".join(
        f'<path d="{bend(128 + i * 16, 26)}" stroke="url(#{pid}{u})" stroke-width="16" fill="none"/>'
        for i, pid in enumerate(("hz", "dt", "vt"))
    )
    seams = "".join(f'<path d="{bend(120 + i * 16, 26)}" stroke="{ink}" stroke-width="1.6" fill="none"/>' for i in range(4))
    return (
        f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath>{pats}</defs>'
        f'<g clip-path="url(#c{u})">{hatch}{seams}</g>'
        + stars([(62, 62), (138, 62), (100, 186)], 24, 0.42, f"url(#vs{u})", f'stroke="{ink}" stroke-width="1.6" stroke-linejoin="round"')
        + f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="4"/>'
        + f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="1" transform="translate(100 122) scale(.94) translate(-100 -122)"/>'
    )


def v_knockout(p):
    """Solid one-colour shield; the arc and stars are cut out of it."""
    u = next(_uid)
    d = SHAPES["geo"]
    col = p["ink"] if (p["mono"] or p["light"]) else p["metal"]
    cuts = "".join(f'<path d="{bend(136 + i * 13, 26)}" stroke="#000" stroke-width="7" fill="none"/>' for i in range(3))
    return (
        f'<defs><mask id="m{u}" maskUnits="userSpaceOnUse" x="0" y="0" width="200" height="240">'
        f'<rect width="200" height="240" fill="#fff"/>{cuts}'
        + stars([(64, 64), (136, 64), (100, 188)], 23, 0.42, "#000")
        + f'</mask></defs><path d="{d}" fill="{col}" mask="url(#m{u})"/>'
    )


def v_enamel(p):
    u = next(_uid)
    d = SHAPES["geo"]
    if p["mono"]:
        return v_flat(p)
    return (
        f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath>'
        f'<linearGradient id="rim{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F6DC94"/><stop offset=".45" stop-color="#B8892E"/>'
        f'<stop offset=".7" stop-color="#EFD07E"/><stop offset="1" stop-color="#8C6420"/></linearGradient>'
        f'<linearGradient id="fld{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#CDD5DE"/></linearGradient>'
        f'<linearGradient id="gl{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="st{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F04A55"/><stop offset="1" stop-color="#A3121E"/></linearGradient>'
        f'</defs>'
        f'<path d="{d}" fill="url(#fld{u})"/>'
        f'<g clip-path="url(#c{u})">{bands(p, 132, 26, 15, cols=("#2A4FCB", "#E7B21C", "#C81D2A"))}'
        f'<path d="{bend(124.5, 26)}" stroke="#fff" stroke-width="1" fill="none" opacity=".55"/>'
        f'<rect width="200" height="130" fill="url(#gl{u})"/></g>'
        + stars([(64, 62), (136, 62), (100, 186)], 24, 0.42, f"url(#st{u})", 'stroke="#7d0d16" stroke-width=".8"')
        + f'<path d="{d}" fill="none" stroke="url(#rim{u})" stroke-width="8"/>'
        + f'<path d="{d}" fill="none" stroke="#5a3f12" stroke-width="1" transform="translate(100 124) scale(.955) translate(-100 -124)" opacity=".7"/>'
    )


def v_glow(p):
    u = next(_uid)
    d = SHAPES["geo"]
    if p["mono"] or p["light"]:
        return v_hairline(p)
    cols = ("#6E8DFF", "#F1C76A", "#FF5468")
    glow_bands = bands(p, 140, 26, 10, w=9, cols=cols, extra=f'filter="url(#b{u})" opacity=".75"')
    core = bands(p, 140, 26, 10, w=2.4, cols=("#C9D6FF", "#FFE7B0", "#FFB0BA"))
    pos = [(68, 66), (132, 66), (100, 184)]
    return (
        f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath>'
        f'<filter id="b{u}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter></defs>'
        f'<path d="{d}" fill="none" stroke="#8EA0B8" stroke-width="7" opacity=".35" filter="url(#b{u})"/>'
        f'<g clip-path="url(#c{u})">{glow_bands}{core}</g>'
        + stars(pos, 19, 0.42, "#FF5468", f'filter="url(#b{u})" opacity=".9"')
        + stars(pos, 16, 0.42, "#FF8C99")
        + f'<path d="{d}" fill="none" stroke="#DCE6EE" stroke-width="1.8"/>'
    )


def v_bold(p):
    u = next(_uid)
    d = SHAPES["geo"]
    field = "none" if p["mono"] else ("#E3E8ED" if p["light"] else p["field"])
    outline = f'<path d="{d}" fill="none" stroke="{p["ink"]}" stroke-width="5"/>' if p["mono"] else ""
    return (
        f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath></defs>'
        f'<path d="{d}" fill="{field}"/>'
        f'<g clip-path="url(#c{u})">{bands(p, 104, 30, 22, mono_w=0.7)}</g>'
        + stars([(58, 44, 16), (142, 44, 16), (100, 194, 22)], 16, 0.42, p["star"])
        + outline
    )


def v_kite(p):
    u = next(_uid)
    d = SHAPES["kite"]
    field = "none" if p["mono"] else ("#E3E8ED" if p["light"] else p["field"])
    outline = f'<path d="{d}" fill="none" stroke="{p["ink"]}" stroke-width="5"/>' if p["mono"] else ""
    return (
        f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath></defs>'
        f'<path d="{d}" fill="{field}"/>'
        f'<g clip-path="url(#c{u})">{bands(p, 116, 24, 14)}</g>'
        + stars([(66, 62), (134, 62), (100, 178, 18)], 20, 0.42, p["star"])
        + outline
    )


def v_round(p):
    u = next(_uid)
    d = SHAPES["round"]
    field = "none" if p["mono"] else ("#E3E8ED" if p["light"] else p["field"])
    rim = p["ink"] if p["mono"] else p["metal"]
    rivets = "".join(
        f'<circle cx="{100 + 86 * math.cos(math.radians(a)):.1f}" cy="{120 + 86 * math.sin(math.radians(a)):.1f}" r="2.2" fill="{p["bg"] if p["mono"] else "#8C6420"}"/>'
        for a in range(0, 360, 30)
    )
    return (
        f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath></defs>'
        f'<path d="{d}" fill="{field}"/>'
        f'<g clip-path="url(#c{u})">{bands(p, 132, 26, 15)}</g>'
        + stars([(68, 74), (132, 74), (100, 178)], 20, 0.42, p["star"])
        + f'<path d="{d}" fill="none" stroke="{rim}" stroke-width="9"/>{rivets}'
    )


def v_stripe(p):
    """Bands float inside the outline with rounded ends and gaps, like modern stripes."""
    d = SHAPES["geo"]
    w = 9 if not p["mono"] else 6
    arcs = "".join(
        f'<path d="M44 {138 + i * 16} Q100 {106 + i * 16} 156 {138 + i * 16}" stroke="{c}" stroke-width="{w}" stroke-linecap="round" fill="none"/>'
        for i, c in enumerate((p["a1"], p["a2"], p["a3"]))
    )
    field = "none" if p["mono"] else ("#E3E8ED" if p["light"] else p["field"])
    edge = p["ink"] if p["mono"] else ("#C9A15E" if not p["light"] else p["line"])
    return (
        f'<path d="{d}" fill="{field}" stroke="{edge}" stroke-width="{4 if p["mono"] else 0}"/>'
        f'{arcs}'
        + stars([(66, 70), (134, 70), (100, 198, 16)], 20, 0.42, p["star"])
    )


def v_split(p):
    """Per pale: silver and night halves, tinctures counterchanged across the line."""
    u = next(_uid)
    d = SHAPES["geo"]
    if p["mono"]:
        col = p["ink"]
        other = p["bg"]
    else:
        col, other = "#111829", "#EEF1F4"
    pos = [(64, 62), (136, 62), (100, 186)]
    left_star, right_star = (p["star"], "#EEF1F4") if not p["mono"] else (col, other)
    return (
        f'<defs><clipPath id="c{u}"><path d="{d}"/></clipPath>'
        f'<clipPath id="l{u}"><rect width="100" height="240"/></clipPath>'
        f'<clipPath id="r{u}"><rect x="100" width="100" height="240"/></clipPath></defs>'
        f'<g clip-path="url(#c{u})">'
        f'<rect width="100" height="240" fill="{"none" if p["mono"] else other}"/>'
        f'<rect x="100" width="100" height="240" fill="{col}"/>'
        f'{bands(p, 132, 26, 15)}</g>'
        f'<g clip-path="url(#l{u})">{stars(pos, 23, 0.42, left_star)}</g>'
        f'<g clip-path="url(#r{u})">{stars(pos, 23, 0.42, right_star)}</g>'
        + (f'<path d="{d}" fill="none" stroke="{p["ink"]}" stroke-width="5"/>' if p["mono"] or p["light"] else
           f'<path d="{d}" fill="none" stroke="#C9A15E" stroke-width="1.6"/>')
    )


VARIANTS = [
    dict(id="heritage", fn=v_heritage, code="00", name="Heritage", ref=True,
         idea="The arms as on the site today, for reference. Rounded corners, black outlines, a seam between each band, wide stars.",
         best="Reference only"),
    dict(id="flat", fn=v_flat, code="01", name="Flat",
         idea="All outlines removed. The shield is drawn with compass arcs, the way a classic heater shield is constructed. The stars are sharper. This is the arms redrawn the way a modern brand would do it.",
         best="Default everywhere: site, social, documents"),
    dict(id="hairline", fn=v_hairline, code="02", name="Hairline",
         idea="Only lines. A thin outline, the rainbow as three fine strokes, small solid stars. Light and precise, like an engraved instrument.",
         best="Nav bar, footer, beside the Forum wordmark"),
    dict(id="rainbow", fn=v_rainbow, code="03", name="Rainbow",
         idea="The arc becomes a real rainbow of three concentric rings. The third star sits beneath it like a rising sun. Rounded U-shaped shield. The freest reading that still keeps every element.",
         best="App icon, avatar, playful uses"),
    dict(id="polar", fn=v_polar, code="04", name="Polar",
         idea="The arms inverted for night. A polar-night field, brightened rainbow, silver stars and a double brass rim. Made for the dark site.",
         best="Night Smithy hero, dark UI, merchandise"),
    dict(id="facet", fn=v_facet, code="05", name="Facet",
         idea="A chamfered, angular shield split down the middle so one half catches light and the other falls into shade. The stars are faceted the same way. Machined metal; the most futurist.",
         best="Orders of Magnitude, tech contexts, motion"),
    dict(id="engraved", fn=v_engraved, code="06", name="Engraved",
         idea="Colour shown by heraldic hatching, the old engravers' code: horizontal lines for blue, dots for gold, vertical lines for red. So the rainbow survives in one ink.",
         best="Signet ring, letterpress, bookplate, seal"),
    dict(id="knockout", fn=v_knockout, code="07", name="Knockout",
         idea="A solid one-colour shield with the rainbow and stars cut out of it. Holds up at the smallest sizes and in any material.",
         best="Favicon, stamps, embroidery, laser-etching"),
    dict(id="enamel", fn=v_enamel, code="08", name="Enamel",
         idea="Like an enamel badge: a gold rim, glossy colour, shaded stars. Grand-marque car-badge luxury rather than medieval.",
         best="Pins, cufflinks, physical objects, the hero"),
    dict(id="glow", fn=v_glow, code="09", name="Glow",
         idea="The shield as light. A hairline outline, a rainbow that glows like the aurora and the runes, stars burning red. Lives only on the night ground.",
         best="Night hero, video, loading screen"),
    dict(id="bold", fn=v_bold, code="10", name="Bold",
         idea="The rainbow scaled up to fill the shield. Small stars on top, a big one at the base. Poster-like and readable from across a room.",
         best="Flags, banners, merch, large formats"),
    dict(id="kite", fn=v_kite, code="11", name="Kite",
         idea="A long kite shield, the shape the Normans (Norse settlers in France) carried. Sleek and tall, still clearly a shield.",
         best="Vertical layouts, book spine, tall banners"),
    dict(id="stripe", fn=v_stripe, code="12", name="Stripe",
         idea="The rainbow as three floating stripes with rounded ends and space between them, inside a hairline brass outline. Reads like a modern product logo while staying clearly heraldic.",
         best="Digital products, app splash, OoM-adjacent uses"),
    dict(id="split", fn=v_split, code="13", name="Split",
         idea="Divided down the middle: one half silver, one half polar night, with the stars switching colour across the line. Day and night, old and new, in one shield. The rainbow runs unbroken across both.",
         best="A statement mark, covers, the light/dark site toggle"),
    dict(id="round", fn=v_round, code="14", name="Round",
         idea="A Viking round shield: the arms painted on a circle with an iron rim and rivets. The most Nordic of the set, and it fits round avatars.",
         best="Avatars, coins, seals, Viking accents"),
]
VMAP = {v["id"]: v for v in VARIANTS}


def render(vid: str, pal: dict, h: int, cls: str = "") -> str:
    return wrap(VMAP[vid]["fn"](pal), h, f"Graah arms — {VMAP[vid]['name']}", cls)


# ───────────────────────── contexts ─────────────────────────


def seal_with(vid: str, size: int = 200) -> str:
    u = next(_uid)
    inner = VMAP[vid]["fn"](WAXBRASS)
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 200 200" role="img" aria-label="The Graah seal">'
        f'<defs><path id="r{u}" d="M100 100 m-75 0 a75 75 0 1 1 150 0 a75 75 0 1 1 -150 0"/></defs>'
        f'<circle cx="100" cy="100" r="97" fill="#6E1414"/><circle cx="100" cy="100" r="92" fill="none" stroke="#9A2A2A" stroke-width="2"/>'
        f'<circle cx="100" cy="100" r="60" fill="none" stroke="#C9A15E" stroke-width="1"/>'
        f'<text font-family="Noto Sans Runic" font-size="14.5" fill="#C9A15E" letter-spacing="5.2"><textPath href="#r{u}">{SEAL_TEXT}</textPath></text>'
        f'<svg x="68" y="60" width="64" height="77" viewBox="0 0 200 240">{inner}</svg></svg>'
    )


def context_payload(vid: str) -> dict:
    return dict(
        hero=render(vid, NIGHT, 170, "hshield"),
        seal=seal_with(vid, 190),
        nav=render(vid, NIGHT, 26),
        fav=render(vid, NIGHT, 16),
        paper=render(vid, PAPER, 96),
        sizes="".join(f'<span>{render(vid, NIGHT, s)}<small>{s}</small></span>' for s in (64, 32, 16)),
    )


# ───────────────────────── page ─────────────────────────


def gallery() -> str:
    cards = []
    for v in VARIANTS:
        small = "".join(f'<span>{render(v["id"], NIGHT, s)}<small>{s}px</small></span>' for s in (48, 32, 16))
        tag = '<em class="ref">reference</em>' if v.get("ref") else ""
        cards.append(
            f'<article class="vc{" isref" if v.get("ref") else ""}" id="v-{v["id"]}">'
            f'<div class="vart">{render(v["id"], NIGHT, 230)}</div>'
            f'<div class="vsmall">{small}</div>'
            f'<div class="vtext"><div class="vcode">{v["code"]} · {v["name"]} {tag}</div><p>{v["idea"]}</p>'
            f'<div class="vbest"><span>Best for</span>{v["best"]}</div></div></article>'
        )
    return f'<div class="vgrid">{"".join(cards)}</div>'


def matrix() -> str:
    head = "<tr><th></th><th>Colour · night</th><th>Colour · paper</th><th>One colour · brass</th><th>One colour · ink</th><th>24px</th></tr>"
    rows = []
    for v in VARIANTS:
        vid = v["id"]
        rows.append(
            f'<tr><td class="rn"><a href="#v-{vid}">{v["code"]} · {v["name"]}</a></td>'
            f'<td class="n">{render(vid, NIGHT, 110)}</td>'
            f'<td class="p">{render(vid, PAPER, 110)}</td>'
            f'<td class="n">{render(vid, BRASS, 110)}</td>'
            f'<td class="p">{render(vid, INK, 110)}</td>'
            f'<td class="n">{render(vid, NIGHT, 24)}</td></tr>'
        )
    return f'<div class="mwrap"><table class="matrix"><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table></div>'


def context_board() -> str:
    data = {v["id"]: context_payload(v["id"]) for v in VARIANTS}
    first = "flat"
    d0 = data[first]
    buttons = "".join(
        f'<button type="button" data-v="{v["id"]}"{" aria-pressed=\"true\"" if v["id"] == first else ""}>{v["code"]} · {v["name"]}</button>'
        for v in VARIANTS
    )
    board = f"""
<div class="picker" role="group" aria-label="Choose a shield variant">{buttons}</div>
<div class="board">
  <div class="hz bhero">
    {sky(7)}
    {ARC}
    <div class="hin">
      <nav class="hnav"><span class="brand"><span class="slot" data-k="nav">{d0['nav']}</span>Graah</span><span class="mid">I — IX</span><span>1462 → now</span></nav>
      <div class="hcopy"><span class="slot" data-k="hero">{d0['hero']}</span><h3 class="wm">GRAAH</h3>{glow_runes("under")}<p class="tag">Five centuries. Three kingdoms. One name.</p></div>
    </div>
  </div>
  <div class="bside">
    <div class="bcell sealcell"><span class="label">Forge II seal</span><span class="slot" data-k="seal">{d0['seal']}</span></div>
    <div class="bcell papercell"><span class="label">Letterhead</span>
      <div class="letter"><span class="slot" data-k="paper">{d0['paper']}</span><div class="lwm">GRAAH</div><div class="lline"></div><div class="laddr">Stockholm · Oslo · Søllested</div></div></div>
    <div class="bcell tabcell"><span class="label">Browser tab &amp; sizes</span>
      <div class="tab"><span class="slot" data-k="fav">{d0['fav']}</span><span>Graah — The family chronicle</span><i>×</i></div>
      <div class="szrow slot" data-k="sizes">{d0['sizes']}</div></div>
  </div>
</div>
<script>
(()=>{{
  const D={json.dumps(data, ensure_ascii=False)};
  const btns=document.querySelectorAll('.picker button');
  const set=v=>{{
    document.querySelectorAll('.board .slot').forEach(s=>{{s.innerHTML=D[v][s.dataset.k]}});
    btns.forEach(b=>b.setAttribute('aria-pressed',b.dataset.v===v?'true':'false'));
  }};
  btns.forEach(b=>b.addEventListener('click',()=>set(b.dataset.v)));
}})();
</script>"""
    return board


CSS = r"""
.vgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#26304A;border:1px solid #26304A}
.vc{background:#0d1220;display:flex;flex-direction:column}
.vc.isref{background:#0a0d16}
.vart{height:300px;display:flex;align-items:center;justify-content:center;background:radial-gradient(60% 60% at 50% 45%,#16203a,transparent 75%)}
.vsmall{display:flex;gap:22px;align-items:flex-end;justify-content:center;padding:4px 0 18px;border-bottom:1px solid #1d2640}
.vsmall span,.szrow span{display:flex;flex-direction:column;align-items:center;gap:6px}
.vsmall small,.szrow small{font:400 10px/1 "Geist Mono";color:#5f6e86}
.vtext{padding:20px 22px 24px;display:flex;flex-direction:column;gap:12px;flex:1}
.vcode{font:500 12px/1.3 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#C9A15E}
.vcode .ref{font-style:normal;color:#8EA0B8;border:1px solid #26304A;border-radius:999px;padding:3px 8px;margin-left:6px;font-size:10px}
.vtext p{font:300 14.5px/1.55 Geist;color:#B7C3D1}
.vbest{margin-top:auto;font:400 13px/1.4 Geist;color:#DCE6EE;border-top:1px solid #1d2640;padding-top:12px}
.vbest span{display:block;font:500 10px/1 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#8EA0B8;margin-bottom:6px}
.rules2{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#26304A;border:1px solid #26304A;margin-top:40px}
.rules2>div{background:#0e1424;padding:22px}
.rules2 h4{font:500 11px/1.3 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#C9A15E;margin-bottom:10px}
.rules2 p{font:300 14.5px/1.55 Geist;color:#B7C3D1}
.anatomy{display:flex;gap:40px;align-items:center;justify-content:center;flex-wrap:wrap}
.mwrap{overflow-x:auto;border:1px solid #26304A}
.matrix{border-collapse:collapse;width:100%;min-width:760px}
.matrix th{font:500 10px/1.3 "Geist Mono";letter-spacing:.16em;text-transform:uppercase;color:#8EA0B8;padding:14px;text-align:center;background:#0e1424;border-bottom:1px solid #26304A}
.matrix td{padding:16px;border-bottom:1px solid #1d2640;text-align:center;vertical-align:middle}
.matrix td svg{margin:0 auto}
.matrix td.n{background:#0B0F1A}
.matrix td.p{background:#F4F0E8}
.matrix .rn{text-align:left;font:500 11px/1.3 "Geist Mono";letter-spacing:.14em;text-transform:uppercase;white-space:nowrap;background:#0e1424}
.matrix .rn a{color:#C9A15E;text-decoration:none}
.picker{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:22px}
.picker button{font:500 11px/1 "Geist Mono";letter-spacing:.12em;text-transform:uppercase;background:transparent;color:#DCE6EE;border:1px solid #26304A;border-radius:999px;padding:10px 13px;cursor:pointer}
.picker button[aria-pressed="true"]{background:#C9A15E;border-color:#C9A15E;color:#0B0F1A}
.board{display:grid;grid-template-columns:1.6fr 1fr;gap:20px}
.bhero{aspect-ratio:auto;min-height:620px}
.bhero .hin{min-height:620px}
.bhero .hcopy{padding-bottom:150px}
.hshield{height:auto;width:clamp(90px,12cqw,150px);margin-bottom:22px;filter:drop-shadow(0 0 28px rgba(62,98,184,.25))}
.brand .slot svg{width:auto;height:22px}
.bside{display:grid;gap:20px;grid-template-rows:auto auto auto}
.bcell{border:1px solid #26304A;background:#0e1424;padding:18px 20px}
.sealcell{display:flex;flex-direction:column;align-items:center}
.sealcell .label{align-self:flex-start}
.papercell .letter{background:#F4F0E8;padding:26px;display:flex;flex-direction:column;align-items:center;gap:10px;box-shadow:0 10px 30px rgba(0,0,0,.35)}
.lwm{font:400 22px/1 Forum;letter-spacing:.42em;padding-left:.42em;color:#1C1A18}
.lline{width:80px;height:1px;background:#B8913A}
.laddr{font:500 9px/1 "IBM Plex Mono","Geist Mono";letter-spacing:.24em;text-transform:uppercase;color:#6b645a}
.tab{display:flex;align-items:center;gap:10px;background:#1b2338;border-radius:10px 10px 0 0;padding:10px 14px;font:400 12px/1 Geist;color:#DCE6EE;max-width:300px}
.tab i{margin-left:auto;font-style:normal;color:#8EA0B8}
.szrow{display:flex;gap:20px;align-items:flex-end;margin-top:18px}
@media (max-width:960px){
  .vgrid{grid-template-columns:1fr 1fr}
  .rules2,.board{grid-template-columns:1fr}
  .bhero{min-height:520px}.bhero .hin{min-height:520px}
  .vart{height:240px}.vart svg{height:190px;width:auto}
}
@media (max-width:560px){
  .vgrid{grid-template-columns:1fr}
}
"""


def page() -> str:
    pals = "".join(
        f'<div class="sw"><i style="background:{h}"></i><b>{n}</b><small>{h} · {r}</small></div>'
        for n, h, r in (("Argent", ARMS["field"], "field"), ("Azure", ARMS["a1"], "rainbow 1"), ("Or", ARMS["a2"], "rainbow 2"),
                        ("Gules", ARMS["a3"], "rainbow 3 · stars"), ("Brass", "#C9A15E", "one-colour"))
    )
    anatomy = (
        f'<div class="anatomy">{render("heritage", NIGHT, 220)}<span style="font:400 40px/1 Forum;color:#C9A15E">→</span>'
        f'{render("flat", NIGHT, 220)}{render("hairline", NIGHT, 220)}{render("knockout", NIGHT, 220)}</div>'
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="robots" content="noindex, nofollow" />
<meta name="theme-color" content="#0B0F1A" />
<link rel="icon" href="/graah-coa.png" type="image/png" />
<title>Graah — Identity exploration v0.4 · The shield</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Forum&family=Geist:wght@300..700&family=Geist+Mono:wght@400;500&family=IBM+Plex+Mono:wght@500&family=Noto+Sans+Runic&display=swap" rel="stylesheet" />
<style>{V3CSS}{CSS}</style>
</head>
<body>
{DEFS}
<section class="intro">
  <div class="wrap">
    <div class="eyebrow">Graah · Visual identity · v0.4 · <a href="/theme-lab/">latest →</a> · <a href="/theme-lab/v3/">v0.3 (Night Smithy)</a> · <a href="/theme-lab/v2/">v0.2</a> · <a href="/theme-lab/v1/">v0.1</a></div>
    <h1>The shield,<br/><em>modernised.</em></h1>
    <p class="lede">The shield stays the primary mark, and the horns go back to being an optional crest. Below are fourteen modern, simplified versions of the arms. Each one keeps the two things that make it ours: the rainbow arc and the three stars. Everything else could change: the shield's outline, the line weight, the colour, the material and the angle of the arc.</p>
    {anatomy}
    <div class="rules2">
      <div><h4>Always kept</h4><p>Three bands in blue, gold and red, in that order from the top, arching upwards. Three six-pointed stars, two above the arc and one below. Red stars on a silver field whenever there's colour.</p></div>
      <div><h4>Free to change</h4><p>The shield's outline (heater, kite, U, chamfered, round). Outlines or none. How deep the arc is and how thick the bands are. How sharp the stars are. The material: flat, enamel, light, engraved.</p></div>
      <div><h4>How to read the page</h4><p>01 is the gallery: each version large, then at 48, 32 and 16px. 02 is the stress test: colour, paper and one colour. 03 lets you tap through every version in the hero, the seal, a letterhead and a browser tab.</p></div>
    </div>
    <nav class="toc"><a href="#gallery">01 · Gallery</a><a href="#matrix">02 · Stress test</a><a href="#context">03 · Try it in context</a><a href="#next">Next</a></nav>
  </div>
</section>

<section class="sec" id="gallery"><div class="wrap">
  <div class="code">01 · Gallery</div><h2>Fourteen shields, one family</h2>
  <p class="lede">Ordered from closest to the heritage arms to furthest from them. 00 is today's arms, for comparison.</p>
  {gallery()}
  <div class="panel" style="margin-top:28px"><span class="label">Tinctures, slightly tuned for screens</span><div class="swatches">{pals}</div></div>
</div></section>

<section class="sec" id="matrix"><div class="wrap">
  <div class="code">02 · Stress test</div><h2>Night, paper, one colour</h2>
  <p class="lede">A family mark has to survive a wax seal, a fax and an embroidery machine. In the one-colour columns, gaps between the bands keep the rainbow readable as three.</p>
  {matrix()}
</div></section>

<section class="sec" id="context"><div class="wrap">
  <div class="code">03 · Try it in context</div><h2>Tap a shield</h2>
  <p class="lede">Swaps the shield in the Night Smithy hero, the nav, the Forge II seal, a letterhead and a browser tab. In the seal it's shown in one colour, brass on wax.</p>
  {context_board()}
</div></section>

<section class="sec" id="next"><div class="wrap">
  <div class="code">Next</div><h2>What to send back</h2>
  <div class="qs">
    <div><h4>1 · Shortlist</h4><p>Pick two or three numbers you like. Mixing is fine, e.g. the shape of 05 with the line of 02.</p></div>
    <div><h4>2 · One or a family?</h4><p>One shield used everywhere, or a set: a primary (e.g. 01), a small-size version (07) and a ceremonial version (06 or 08)?</p></div>
    <div><h4>3 · Shape</h4><p>Keep the heater shape, or go Nordic with the kite (11) or the round shield (14)?</p></div>
    <div><h4>4 · Hero</h4><p>In the Night Smithy hero, should the shield replace the horns, or should the horns sit above the shield as the crest?</p></div>
  </div>
</div></section>
<footer class="page"><div class="wrap">Exploration only — graah.se itself is unchanged. Generated by design/theme-lab/build_v4.py.</div></footer>
</body>
</html>
"""


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page(), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")
