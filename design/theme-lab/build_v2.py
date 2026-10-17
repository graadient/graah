#!/usr/bin/env python3
"""Generate public/theme-lab/v2/index.html — Graah identity exploration, iteration 2.

Run:  python3 design/theme-lab/build_v2.py
Pure stdlib. All SVG ornament is generated here so the page is static.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "public" / "theme-lab" / "v2" / "index.html"

RUNES = "ᚴᚱᛅᛅᚼ"
# Runestone formula, Younger Futhark: "kraah raisþu stain þansi" ~ "the Graahs raised this stone"
STONE_TEXT = "ᚴᚱᛅᛅᚼ ᛬ ᚱᛅᛁᛋᚦᚢ ᛬ ᛋᛏᛅᛁᚾ ᛬ ᚦᛅᚾᛋᛁ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᚱᛅᛁᛋᚦᚢ ᛬ ᛋᛏᛅᛁᚾ ᛬ ᚦᛅᚾᛋᛁ ᛬"


# ───────────────────────── geometry helpers ─────────────────────────


def star_points(R: float = 10, r: float = 5, cx: float = 0, cy: float = 0) -> str:
    """Six-pointed heraldic mullet, matching the arms."""
    pts = []
    for i in range(12):
        a = math.radians(-90 + i * 30)
        rr = R if i % 2 == 0 else r
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    return " ".join(pts)


def cord(width: int, h: int, period: int, c1: str, c2: str, bg: str, sw: float = 2.4) -> str:
    """Two-strand Norse cord with real over/under at every crossing."""
    a = h / 2 - sw - 1
    mid = h / 2
    out = []
    n = math.ceil(width / period) * 2
    half = period / 2
    for k in range(n):
        x0, x1 = k * half, (k + 1) * half
        s = 1 if k % 2 == 0 else -1
        ya0, ya1 = mid + a * s, mid - a * s
        yb0, yb1 = mid - a * s, mid + a * s
        k1 = half * 0.42
        pa = f"M{x0:.1f} {ya0:.1f} C{x0 + k1:.1f} {ya0:.1f} {x1 - k1:.1f} {ya1:.1f} {x1:.1f} {ya1:.1f}"
        pb = f"M{x0:.1f} {yb0:.1f} C{x0 + k1:.1f} {yb0:.1f} {x1 - k1:.1f} {yb1:.1f} {x1:.1f} {yb1:.1f}"
        under, over = ((pa, c1), (pb, c2)) if k % 2 == 0 else ((pb, c2), (pa, c1))
        out.append(f'<path d="{under[0]}" stroke="{under[1]}"/>')
        out.append(f'<path d="{over[0]}" stroke="{bg}" stroke-width="{sw + 4}"/>')
        out.append(f'<path d="{over[0]}" stroke="{over[1]}"/>')
    return (
        f'<svg class="cord" viewBox="0 0 {width} {h}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
        f'<g fill="none" stroke-width="{sw}" stroke-linecap="butt">{"".join(out)}</g></svg>'
    )


def field(seed: int, n: int, w: int, h: int, fill: str, rmax: float = 1.1, ymax: float = 1.0) -> str:
    rnd = random.Random(seed)
    dots = []
    for _ in range(n):
        dots.append(
            f'<circle cx="{rnd.random() * w:.1f}" cy="{rnd.random() * h * ymax:.1f}" '
            f'r="{rnd.random() * rmax + 0.2:.2f}" fill="{fill}" opacity="{rnd.random() * 0.6 + 0.15:.2f}"/>'
        )
    return "".join(dots)


def sparks(seed: int, n: int) -> str:
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = 600 + (rnd.random() - 0.5) * 1100
        y = 120 + rnd.random() * 330
        r = rnd.random() * 1.6 + 0.4
        col = rnd.choice(["#F0B44C", "#F0B44C", "#FFD98A", "#D2382B"])
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{col}" opacity="{rnd.random() * 0.7 + 0.2:.2f}"/>')
    return "".join(out)


def ring_text_seal(
    uid: str, wax: str, rim: str, metal: str, text: str, size: int = 180, shield_vars: str = ""
) -> str:
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 200 200" role="img" aria-label="Graah seal">
  <defs><path id="ring-{uid}" d="M100 100 m-75 0 a75 75 0 1 1 150 0 a75 75 0 1 1 -150 0"/></defs>
  <circle cx="100" cy="100" r="97" fill="{wax}"/>
  <circle cx="100" cy="100" r="92" fill="none" stroke="{rim}" stroke-width="2"/>
  <circle cx="100" cy="100" r="60" fill="none" stroke="{metal}" stroke-width="1"/>
  <text font-family="Noto Sans Runic" font-size="14.5" fill="{metal}" letter-spacing="5.2"><textPath href="#ring-{uid}">{text}</textPath></text>
  <g style="{shield_vars}"><use href="#shield" x="67" y="58" width="66" height="81"/></g>
</svg>"""


# ───────────────────────── shared svg defs ─────────────────────────

STAR = star_points(10, 5)

DEFS = f"""<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<defs>
  <symbol id="mullet" viewBox="-10 -10 20 20"><polygon points="{STAR}"/></symbol>
  <clipPath id="fieldclip"><path d="M12 26 Q12 14 24 14 L132 14 Q144 14 144 26 V92 C144 138 122 166 78 180 C34 166 12 138 12 92 Z"/></clipPath>
  <symbol id="shield" viewBox="0 0 156 192">
    <path d="M12 26 Q12 14 24 14 L132 14 Q144 14 144 26 V92 C144 138 122 166 78 180 C34 166 12 138 12 92 Z" fill="var(--sf)"/>
    <g clip-path="url(#fieldclip)">
      <path d="M4 96 Q78 56 152 96 L152 109 Q78 69 4 109 Z" fill="var(--a1)"/>
      <path d="M4 109 Q78 69 152 109 L152 122 Q78 82 4 122 Z" fill="var(--a2)"/>
      <path d="M4 122 Q78 82 152 122 L152 135 Q78 95 4 135 Z" fill="var(--a3)"/>
    </g>
    <g fill="var(--ss)">
      <use href="#mullet" x="25" y="26" width="44" height="44"/>
      <use href="#mullet" x="87" y="26" width="44" height="44"/>
      <use href="#mullet" x="56" y="126" width="44" height="44"/>
    </g>
    <path d="M12 26 Q12 14 24 14 L132 14 Q144 14 144 26 V92 C144 138 122 166 78 180 C34 166 12 138 12 92 Z" fill="none" stroke="var(--sl)" stroke-width="3"/>
  </symbol>
  <symbol id="shield-line" viewBox="0 0 156 192">
    <path d="M12 26 Q12 14 24 14 L132 14 Q144 14 144 26 V92 C144 138 122 166 78 180 C34 166 12 138 12 92 Z" fill="none" stroke="currentColor" stroke-width="2"/>
    <g clip-path="url(#fieldclip)" fill="none" stroke-width="4">
      <path d="M4 100 Q78 60 152 100" stroke="var(--a1)"/>
      <path d="M4 114 Q78 74 152 114" stroke="var(--a2)"/>
      <path d="M4 128 Q78 88 152 128" stroke="var(--a3)"/>
    </g>
    <g fill="var(--ss)">
      <use href="#mullet" x="33" y="32" width="28" height="28"/>
      <use href="#mullet" x="95" y="32" width="28" height="28"/>
      <use href="#mullet" x="64" y="134" width="28" height="28"/>
    </g>
  </symbol>
  <!-- crest horns: left red→blue, right blue→gold, as on the helm -->
  <clipPath id="hlow"><rect x="0" y="82" width="200" height="90"/></clipPath>
  <clipPath id="hhigh"><rect x="0" y="0" width="200" height="82"/></clipPath>
  <path id="horn" d="M70 166 C18 142 14 52 72 6 C42 58 46 128 98 156 Z"/>
  <symbol id="horns" viewBox="0 0 200 170">
    <g clip-path="url(#hlow)">
      <use href="#horn" fill="var(--h1)"/>
      <use href="#horn" fill="var(--h2)" transform="translate(200 0) scale(-1 1)"/>
    </g>
    <g clip-path="url(#hhigh)">
      <use href="#horn" fill="var(--h2)"/>
      <use href="#horn" fill="var(--h3)" transform="translate(200 0) scale(-1 1)"/>
    </g>
    <g fill="none" stroke="var(--hl,transparent)" stroke-width="1.2">
      <use href="#horn"/><use href="#horn" transform="translate(200 0) scale(-1 1)"/>
    </g>
  </symbol>
  <symbol id="horns-line" viewBox="0 0 200 170">
    <g fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round">
      <use href="#horn"/><use href="#horn" transform="translate(200 0) scale(-1 1)"/>
      <path d="M22 84 Q32 78 44 84"/><path d="M178 84 Q168 78 156 84"/>
    </g>
  </symbol>
  <!-- the new everyday mark: crest horns cradling one star from the arms -->
  <symbol id="hornstar" viewBox="0 0 200 180">
    <use href="#horns" width="200" height="170"/>
    <use href="#mullet" x="70" y="88" width="60" height="60" fill="var(--ss)"/>
  </symbol>
</defs>
</svg>"""


# ───────────────────────── permutations ─────────────────────────

STATS = [
    ("1", "castle lost to a king"),
    ("3", "kingdoms called home"),
    ("12,000", "spindles on one river"),
    ("7", "spellings of one name"),
]

PERMS: list[dict] = []

# 1 ─ FORGE II ──────────────────────────────────────────────
PERMS.append(
    dict(
        id="forge",
        code="C1",
        name="Forge II",
        tag="The original, refined",
        pitch=(
            "Direction C taken further. The crest's horns are now drawn properly — left horn red to blue, "
            "right blue to gold, exactly as on the helm. A real two-strand cord with over-and-under "
            "crossings replaces the zig-zag. The runes are cut into brass. Fjord-steel blue is added so the "
            "palette is the arms' own tinctures in metal and pigment, not just black and red."
        ),
        from_c=["Tar, iron, oxblood, brass", "Marcellus inscriptional caps", "Horns, seal, carved runes"],
        from_a=["—  (pure C, as a baseline)"],
        best="Seal, signet, bookplates, the family archive",
        dials=dict(ground="Tar", metal="Brass", display="Marcellus", arc="Horns", runes="Carved brass", ornament="●●●○"),
        vars=dict(
            bg="#1A1714", surface="#211D19", line="#3A322A", text="#E8DFCF", muted="#BFB3A0",
            metal="#C9A15E", accent="#B3202A", display="Marcellus", body="Newsreader", mono="'IBM Plex Mono'", ui="'Marcellus SC'",
            sf="#E8DFCF", ss="#B3202A", a1="#2A4A73", a2="#C9A15E", a3="#B3202A", sl="#15120F",
            h1="#B3202A", h2="#2A4A73", h3="#C9A15E",
        ),
        palette=[
            ("Tar", "#15120F", "ground"), ("Iron", "#211D19", "surface"), ("Bone", "#E8DFCF", "text"),
            ("Ash", "#8A8278", "muted"), ("Oxblood", "#6E1414", "depth"), ("Ember", "#B3202A", "accent"),
            ("Brass", "#C9A15E", "metal"), ("Fjord Steel", "#2A4A73", "cool"),
        ],
        ratio=[("#15120F", 52), ("#211D19", 18), ("#E8DFCF", 12), ("#B3202A", 7), ("#C9A15E", 6), ("#2A4A73", 5)],
        type=[
            ("Display", "Marcellus", '<div style="font:400 42px/1 Marcellus;letter-spacing:.08em">THE STOLEN CASTLE</div>'),
            ("Body", "Newsreader", '<div style="font:400 17px/1.55 Newsreader;color:var(--muted)">A castle, a king, and a grudge the family has carried for five hundred years.</div>'),
            ("Label", "Marcellus SC", '<div style="font:400 15px/1 \'Marcellus SC\';letter-spacing:.16em;color:var(--metal)">Søllestedgård · MCDLXII</div>'),
            ("Runic", "Noto Sans Runic", f'<div class="rune carved" style="font-size:30px;letter-spacing:.5em">{RUNES}</div>'),
        ],
        card=dict(
            num="I", meta="1462–1550 · Søllestedgård, Lolland", title="The Stolen Castle",
            body="For three generations Søllestedgård belonged to the Graas. In 1530 the King took it; twenty years later Christian III handed it to Jørgen Brahe — uncle of Tycho. The Brahes got the castle. The Graas got the road.",
            chip="A royal grudge",
        ),
        seal=ring_text_seal("forge", "#6E1414", "#9A2A2A", "#C9A15E", "ᚴᚱᛅᛅᚼ ᛬ ᛋᚢᛚᛁᛋᛏᛁᛏ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᛋᚢᛚᛁᛋᛏᛁᛏ ᛬",
                            shield_vars="--sf:#6E1414;--ss:#C9A15E;--a1:#C9A15E;--a2:#6E1414;--a3:#C9A15E;--sl:#C9A15E"),
        hero=f"""
<div class="hero hero-forge">
  <svg class="hero-horns" width="300" height="255" style="--h1:#B3202A;--h2:#2A4A73;--h3:#C9A15E;--hl:rgba(0,0,0,.35)"><use href="#horns"/></svg>
  <h3>GRAAH</h3>
  <div class="rune carved big">{RUNES}</div>
  <p>We lost the castle. We kept the name. Everything since has been built by hand.</p>
  {cord(1100, 22, 58, "#C9A15E", "#8E1C24", "#1B1815")}
</div>""",
    )
)

# 2 ─ EMBER ARC ─────────────────────────────────────────────
PERMS.append(
    dict(
        id="ember",
        code="C2",
        name="Ember Arc",
        tag="Bifröst, forged",
        pitch=(
            "The forge's materials with Bifröst's big idea: the arc from the shield as a horizon. "
            "Here it isn't an aurora but metal fresh out of the fire — molten brass, ember red, "
            "quenched steel — with sparks rising off it. Geist Mono carries A's coordinates and dates. "
            "This is the 1859 fire and the rebuild in one image."
        ),
        from_c=["Tar & iron ground", "Marcellus caps", "Brass + oxblood"],
        from_a=["The glowing arc horizon", "Mono coordinates & HUD line", "Wide, centred hero lockup"],
        best="Hero moments, film titles, the fire chapter, a keynote opener",
        dials=dict(ground="Tar", metal="Molten brass", display="Marcellus", arc="Glowing (fire)", runes="Glow", ornament="●●○○"),
        vars=dict(
            bg="#120F0D", surface="#1C1815", line="#352D26", text="#EDE4D3", muted="#BDB09C",
            metal="#F0B44C", accent="#D2382B", display="Marcellus", body="Newsreader", mono="'Geist Mono'", ui="Geist",
            sf="#EDE4D3", ss="#D2382B", a1="#3A5F8F", a2="#F0B44C", a3="#D2382B", sl="#120F0D",
            h1="#D2382B", h2="#3A5F8F", h3="#F0B44C",
        ),
        palette=[
            ("Tar", "#120F0D", "ground"), ("Iron", "#1C1815", "surface"), ("Bone", "#EDE4D3", "text"),
            ("Smoke", "#8C8277", "muted"), ("Molten", "#F0B44C", "metal / glow"), ("Ember", "#D2382B", "accent"),
            ("Oxblood", "#6E1414", "depth"), ("Quench Blue", "#3A5F8F", "cool"),
        ],
        ratio=[("#120F0D", 58), ("#1C1815", 16), ("#EDE4D3", 12), ("#F0B44C", 6), ("#D2382B", 5), ("#3A5F8F", 3)],
        type=[
            ("Display", "Marcellus", '<div style="font:400 42px/1 Marcellus;letter-spacing:.1em">OUT OF THE ASHES</div>'),
            ("Body", "Newsreader", '<div style="font:400 17px/1.55 Newsreader;color:var(--muted)">The mill burned down. He built it back bigger — then saved a bank.</div>'),
            ("Data", "Geist Mono", '<div style="font:400 13px/1.5 \'Geist Mono\';letter-spacing:.14em;color:var(--metal)">20.12.1859 · 23:00 · 59.92°N 10.75°E</div>'),
            ("Runic", "Noto Sans Runic", f'<div class="rune glow" style="font-size:28px;letter-spacing:.5em">{RUNES}</div>'),
        ],
        card=dict(
            num="VII", meta="Tuesday 20 December 1859 · around 23:00", title="The mill is burning",
            body="Cotton dust, wooden floors, oil and gaslight — in the dark of Christmas week, thirteen years of work went up in a single night. What Knud Graah did next is the whole family in one move: he had insured everything.",
            chip="Out of the ashes",
        ),
        seal=ring_text_seal("ember", "#2A1611", "#5A2A1E", "#F0B44C", "ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬",
                            shield_vars="--sf:#EDE4D3;--ss:#D2382B;--a1:#3A5F8F;--a2:#F0B44C;--a3:#D2382B;--sl:#120F0D"),
        hero=f"""
<div class="hero hero-ember">
  <div class="hud"><span>Graah · Chronicle</span><span>I — IX · 1462 → now</span><span>54.8°N · 11.3°E</span></div>
  <div class="ember-copy">
    <div class="kick">Five centuries · three kingdoms</div>
    <h3>GRAAH</h3>
    <div class="rune glow">{RUNES}</div>
  </div>
  <svg class="ember-arc" viewBox="0 0 1200 600" preserveAspectRatio="none" aria-hidden="true">
    <defs>
      <filter id="heat" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
      <linearGradient id="ground-e" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1310"/><stop offset="1" stop-color="#120F0D"/></linearGradient>
    </defs>
    <g>{sparks(11, 70)}</g>
    <g filter="url(#heat)">
      <path d="M-20 360 Q600 70 1220 360" stroke="#F0B44C" stroke-width="26" fill="none" opacity=".85"/>
      <path d="M-20 392 Q600 102 1220 392" stroke="#D2382B" stroke-width="22" fill="none" opacity=".8"/>
      <path d="M-20 422 Q600 132 1220 422" stroke="#3A5F8F" stroke-width="18" fill="none" opacity=".6"/>
    </g>
    <path d="M-20 360 Q600 70 1220 360" stroke="#FFE2A3" stroke-width="1.6" fill="none"/>
    <path d="M-20 392 Q600 102 1220 392" stroke="#FF8A6E" stroke-width="1.1" fill="none"/>
    <path d="M-20 422 Q600 132 1220 422" stroke="#8FB0DA" stroke-width="1" fill="none" opacity=".8"/>
    <path d="M-20 440 Q600 150 1220 440 L1220 600 L-20 600 Z" fill="url(#ground-e)"/>
  </svg>
  <p class="ember-line">The mill burned in 1859. It was rebuilt bigger within the year.</p>
</div>""",
    )
)

# 3 ─ NIGHT SMITHY ──────────────────────────────────────────
PERMS.append(
    dict(
        id="night",
        code="C3",
        name="Night Smithy",
        tag="Forge metals under a polar sky",
        pitch=(
            "The most even split. Bifröst's polar-night ground, starfield and hairline aurora — "
            "but every metal and pigment comes from the forge: brass instead of bright gold, oxblood "
            "stars, steel-blue. Marcellus replaces Cormorant, so it reads carved, not delicate. "
            "The horns stand over the wordmark as line art, like an engraving on a blade."
        ),
        from_c=["Brass & oxblood", "Marcellus caps", "Horns, carved runes, seal"],
        from_a=["Polar Night ground", "Starfield + hairline aurora", "Geist / Geist Mono UI, pill buttons"],
        best="The website default, dark mode, the Greenland & war chapters",
        dials=dict(ground="Polar night", metal="Brass", display="Marcellus", arc="Hairline aurora", runes="Brass", ornament="●●○○"),
        vars=dict(
            bg="#0B0F1A", surface="#111829", line="#26304A", text="#DCE6EE", muted="#A6B3C4",
            metal="#C9A15E", accent="#C8283A", display="Marcellus", body="Geist", mono="'Geist Mono'", ui="Geist",
            sf="#DCE6EE", ss="#C8283A", a1="#3E62B8", a2="#C9A15E", a3="#C8283A", sl="#0B0F1A",
            h1="#C8283A", h2="#3E62B8", h3="#C9A15E",
        ),
        palette=[
            ("Polar Night", "#0B0F1A", "ground"), ("Deep Fjord", "#111829", "surface"), ("Glacier", "#DCE6EE", "text"),
            ("Sea Smoke", "#8EA0B8", "muted"), ("Brass", "#C9A15E", "metal"), ("Star Red", "#C8283A", "accent"),
            ("Oxblood", "#8E1C24", "depth"), ("Steel Blue", "#3E62B8", "link / arc"),
        ],
        ratio=[("#0B0F1A", 60), ("#111829", 16), ("#DCE6EE", 12), ("#C9A15E", 5), ("#C8283A", 4), ("#3E62B8", 3)],
        type=[
            ("Display", "Marcellus", '<div style="font:400 42px/1 Marcellus;letter-spacing:.1em">INTO THE ICE</div>'),
            ("Body", "Geist 300", '<div style="font:300 16px/1.6 Geist;color:var(--muted)">A king’s orders, a lost colony and one open skin boat against the entire Arctic.</div>'),
            ("Data", "Geist Mono", '<div style="font:400 13px/1.5 \'Geist Mono\';letter-spacing:.14em;color:var(--metal)">08.08.1829 · 65.4°N 39.2°W · −38°C</div>'),
            ("Runic", "Noto Sans Runic", f'<div class="rune" style="font-size:28px;letter-spacing:.5em;color:var(--metal)">{RUNES}</div>'),
        ],
        card=dict(
            num="IV", meta="1828–1831 · East coast of Greenland", title="The Glacier You Must Not Name",
            body="Where the British hurled warships at the Arctic, W.A. Graah went the other way: an open skin boat rowed by Greenlandic women, kayaks scouting ahead, no lifeline home. On 8 August 1829 the pack ice slammed shut at Dannebrog Island.",
            chip="Into the ice",
        ),
        seal=ring_text_seal("night", "#111829", "#26304A", "#C9A15E", "ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬",
                            shield_vars="--sf:#DCE6EE;--ss:#C8283A;--a1:#3E62B8;--a2:#C9A15E;--a3:#C8283A;--sl:#0B0F1A"),
        hero=f"""
<div class="hero hero-night">
  <svg class="sky" viewBox="0 0 1200 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    {field(7, 170, 1200, 600, "#DCE6EE", 1.1, 0.75)}
    <use href="#mullet" x="170" y="96" width="14" height="14" fill="#C8283A" opacity=".85"/>
    <use href="#mullet" x="1010" y="70" width="11" height="11" fill="#C9A15E" opacity=".85"/>
    <use href="#mullet" x="900" y="250" width="8" height="8" fill="#DCE6EE" opacity=".7"/>
    <path d="M-20 640 Q600 390 1220 640 L1220 700 L-20 700Z" fill="#0f1830" opacity=".9"/>
    <path d="M-20 640 Q600 390 1220 640" stroke="#3E62B8" stroke-width="44" fill="none" opacity=".12"/>
    <path d="M-20 640 Q600 390 1220 640" stroke="#3E62B8" stroke-width="1.2" fill="none"/>
    <path d="M-20 655 Q600 405 1220 655" stroke="#C9A15E" stroke-width="1" fill="none"/>
    <path d="M-20 670 Q600 420 1220 670" stroke="#C8283A" stroke-width="1" fill="none"/>
  </svg>
  <div class="night-nav"><span class="brand"><svg width="22" height="20" style="--h1:#C8283A;--h2:#3E62B8;--h3:#C9A15E;--ss:#C9A15E"><use href="#hornstar"/></svg>Graah</span><span>I — IX</span><span>1462 → now</span></div>
  <div class="night-copy">
    <svg class="night-horns" width="170" height="145" style="color:#C9A15E"><use href="#horns-line"/></svg>
    <h3>GRAAH</h3>
    <div class="rune">{RUNES}</div>
    <p>Five centuries. Three kingdoms. One name.</p>
  </div>
</div>""",
    )
)

# 4 ─ RIMFROST ──────────────────────────────────────────────
PERMS.append(
    dict(
        id="rime",
        code="C4",
        name="Rimfrost",
        tag="Iron & ice — the futurist edge",
        pitch=(
            "The forge gone cold. Gunmetal and frost instead of tar and bone, brass kept only for "
            "hairlines, a single red seal. Bifröst's wide-tracked Cormorant is the display face. "
            "Everything is engraved: a monoline shield, hairline horns, coordinates. It's the "
            "direction that sits most naturally next to Spotify, Revolut and a deck for Orders of Magnitude."
        ),
        from_c=["Engraved metal, horns & seal", "Brass hairlines", "Seal red, used once"],
        from_a=["Cormorant set wide", "Monoline shield & arc", "Coordinates, cold palette, quiet glow"],
        best="Hannes's own site & decks, product UI, OoM — the modern chapter",
        dials=dict(ground="Gunmetal", metal="Brass hairline", display="Cormorant wide", arc="Engraved lines", runes="Etched", ornament="●○○○"),
        vars=dict(
            bg="#16191D", surface="#1E2227", line="#323941", text="#E6EDF1", muted="#A9B5BF",
            metal="#B99357", accent="#B3202A", display="'Cormorant Garamond'", body="Geist", mono="'Geist Mono'", ui="Geist",
            sf="#E6EDF1", ss="#B3202A", a1="#8FB3CC", a2="#B99357", a3="#B3202A", sl="#16191D",
            h1="#B3202A", h2="#8FB3CC", h3="#B99357",
        ),
        palette=[
            ("Gunmetal", "#16191D", "ground"), ("Iron", "#1E2227", "surface"), ("Frost", "#E6EDF1", "text"),
            ("Rime", "#F7FAFB", "highlight"), ("Steel", "#6F7B86", "muted"), ("Glacier", "#8FB3CC", "cool / data"),
            ("Brass", "#B99357", "hairline"), ("Seal Red", "#B3202A", "the one red"),
        ],
        ratio=[("#16191D", 60), ("#1E2227", 18), ("#E6EDF1", 14), ("#8FB3CC", 4), ("#B99357", 3), ("#B3202A", 1)],
        type=[
            ("Display", "Cormorant 300", '<div style="font:300 46px/1 \'Cormorant Garamond\';letter-spacing:.12em">ORDERS OF MAGNITUDE</div>'),
            ("Body", "Geist 300", '<div style="font:300 16px/1.6 Geist;color:var(--muted)">Find the new infrastructure of the age, cross the border, and build.</div>'),
            ("Data", "Geist Mono", '<div style="font:400 13px/1.5 \'Geist Mono\';letter-spacing:.12em;color:var(--a1)">1462 → 2026 · Δ 564y · 10⁰ … 10⁹</div>'),
            ("Runic", "Noto Sans Runic", f'<div class="rune" style="font-size:26px;letter-spacing:.6em;color:var(--muted)">{RUNES}</div>'),
        ],
        card=dict(
            num="X", meta="Now · Stockholm · London · in transit", title="Orders of Magnitude",
            body="Waterfalls became spindles. Spindles became banks. Radio became streams, and banks became apps. Spotify, Revolut, Zeal, Orders of Magnitude — the same family move on new infrastructure.",
            chip="The modern chapter",
        ),
        seal=ring_text_seal("rime", "#1E2227", "#323941", "#B99357", "ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬",
                            shield_vars="--sf:#E6EDF1;--ss:#B3202A;--a1:#8FB3CC;--a2:#B99357;--a3:#B3202A;--sl:#16191D"),
        hero="""
<div class="hero hero-rime">
  <div class="rime-grid">
    <div class="rime-left">
      <div class="coords"><span>65.4°N</span><span>39.2°W</span></div>
      <h3>GRAAH</h3>
      <div class="rune">ᚴᚱᛅᛅᚼ</div>
      <p>Charting new coasts since 1462. Castle, pulpit, harbour, ice, waterfall, radio, software.</p>
      <div class="ticks"><span>1462</span><span>1591</span><span>1767</span><span>1829</span><span>1859</span><span>1945</span><span class="now">Now</span></div>
    </div>
    <div class="rime-right">
      <svg class="rime-horns" width="150" height="128" style="color:#B99357"><use href="#horns-line"/></svg>
      <svg class="rime-shield" width="230" height="283" style="color:#E6EDF1;--a1:#8FB3CC;--a2:#B99357;--a3:#B3202A;--ss:#B3202A"><use href="#shield-line"/></svg>
    </div>
  </div>
</div>""",
    )
)

# 5 ─ RUNESTONE ─────────────────────────────────────────────
PERMS.append(
    dict(
        id="stone",
        code="C5",
        name="Runestone",
        tag="Daylight companion",
        pitch=(
            "A light mode for long reading, so the forge has a daytime. Viking runestones were "
            "originally painted — red ochre and black in the carved grooves — so that is the palette: "
            "limewash, granite, iron ink, ochre red, with brass and fjord blue from the arms. "
            "The hero is a stone with the name running round its serpent band, as on the real ones."
        ),
        from_c=["Marcellus caps", "Carved runes, horns, cord", "Oxblood + brass"],
        from_a=["Mono for dates & sources", "Generous, centred, quiet layout"],
        best="Reading the chronicle in daylight, print, invitations",
        dials=dict(ground="Limewash", metal="Brass", display="Marcellus", arc="Serpent band", runes="Painted ochre", ornament="●●○○"),
        vars=dict(
            bg="#ECE5D8", surface="#F6F2EA", line="#D3C9B6", text="#1C1A18", muted="#4C4740",
            metal="#8C6A2F", accent="#A63A25", display="Marcellus", body="Newsreader", mono="'IBM Plex Mono'", ui="'Marcellus SC'",
            sf="#F6F2EA", ss="#A63A25", a1="#2A4A73", a2="#B8913A", a3="#A63A25", sl="#1C1A18",
            h1="#A63A25", h2="#2A4A73", h3="#B8913A",
        ),
        palette=[
            ("Limewash", "#ECE5D8", "ground"), ("Chalk", "#F6F2EA", "surface"), ("Granite", "#8A867E", "stone"),
            ("Iron Ink", "#1C1A18", "text"), ("Ochre Red", "#A63A25", "accent"), ("Oxblood", "#6E1414", "depth"),
            ("Brass", "#B8913A", "ornament"), ("Fjord", "#2A4A73", "link"),
        ],
        ratio=[("#ECE5D8", 56), ("#F6F2EA", 18), ("#1C1A18", 14), ("#A63A25", 5), ("#B8913A", 4), ("#2A4A73", 3)],
        type=[
            ("Display", "Marcellus", '<div style="font:400 42px/1 Marcellus;letter-spacing:.06em">The Voice That Survived</div>'),
            ("Body", "Newsreader", '<div style="font:400 17px/1.55 Newsreader;color:var(--muted)">The mill-owner’s granddaughter chose resistance over comfort.</div>'),
            ("Data", "IBM Plex Mono", '<div style="font:500 12px/1.5 \'IBM Plex Mono\';letter-spacing:.14em;color:var(--a1)">OSLO · GRINI · RAVENSBRÜCK · NRK</div>'),
            ("Runic", "Noto Sans Runic", f'<div class="rune" style="font-size:28px;letter-spacing:.5em;color:var(--accent)">{RUNES}</div>'),
        ],
        card=dict(
            num="VIII", meta="1908–2001 · Oslo — Grini — Ravensbrück — NRK", title="The Voice That Survived",
            body="Anne “Lille” Graah, granddaughter of the industrialist, went to work for the illegal press when Germany occupied Norway — the underground newspapers that kept the truth moving. She survived Ravensbrück and became a voice of the nation on NRK.",
            chip="Resistance",
        ),
        seal=ring_text_seal("stone", "#A63A25", "#C2563F", "#F6F2EA", "ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᚴᚱᛅᛅᚼ ᛬",
                            shield_vars="--sf:#F6F2EA;--ss:#A63A25;--a1:#2A4A73;--a2:#B8913A;--a3:#A63A25;--sl:#1C1A18"),
        hero=f"""
<div class="hero hero-stone">
  <svg class="stone" viewBox="0 0 400 470" aria-hidden="true">
    <defs>
      <path id="band" d="M78 452 L78 190 C78 70 322 70 322 190 L322 452"/>
      <linearGradient id="granite" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A39E95"/><stop offset="1" stop-color="#7E7A72"/></linearGradient>
    </defs>
    <clipPath id="stoneclip"><path d="M40 466 L46 176 C52 30 348 30 354 176 L360 466 Z"/></clipPath>
    <path d="M40 466 L46 176 C52 30 348 30 354 176 L360 466 Z" fill="url(#granite)"/>
    <g opacity=".22" clip-path="url(#stoneclip)">{field(3, 140, 400, 470, "#2a2824", 1.4)}</g>
    <path d="M60 456 L60 186 C64 52 336 52 340 186 L340 456" fill="none" stroke="#1C1A18" stroke-width="1.2" opacity=".55"/>
    <path d="M96 456 L96 194 C100 92 300 92 304 194 L304 456" fill="none" stroke="#1C1A18" stroke-width="1.2" opacity=".55"/>
    <text font-family="Noto Sans Runic" font-size="21" fill="#A63A25" letter-spacing="3"><textPath href="#band">{STONE_TEXT}</textPath></text>
    <g style="--sf:#E9E3D7;--ss:#A63A25;--a1:#2A4A73;--a2:#B8913A;--a3:#A63A25;--sl:#1C1A18"><use href="#shield" x="138" y="176" width="124" height="153"/></g>
    <use href="#mullet" x="183" y="360" width="34" height="34" fill="#1C1A18" opacity=".75"/>
  </svg>
  <div class="stone-copy">
    <div class="kick">The family chronicle · MCDLXII</div>
    <h3>GRAAH</h3>
    <p>Five hundred years of kings, fires, fortunes and comebacks — the good parts kept in.</p>
    <div class="stone-cap">Band reads <span class="rune">ᚴᚱᛅᛅᚼ ᛬ ᚱᛅᛁᛋᚦᚢ ᛬ ᛋᛏᛅᛁᚾ ᛬ ᚦᛅᚾᛋᛁ</span> — roughly “the Graahs raised this stone”, in the formula of the real stones.</div>
    {cord(560, 20, 52, "#A63A25", "#1C1A18", "#ECE5D8", 2.2)}
  </div>
</div>""",
    )
)


# ───────────────────────── page assembly ─────────────────────────


def var_block(p: dict) -> str:
    v = p["vars"]
    return (
        f"#{p['id']}{{--bg:{v['bg']};--surface:{v['surface']};--line:{v['line']};--text:{v['text']};"
        f"--muted:{v['muted']};--metal:{v['metal']};--accent:{v['accent']};--display:{v['display']};"
        f"--body:{v['body']};--mono:{v['mono']};--ui:{v['ui']};--sf:{v['sf']};--ss:{v['ss']};--a1:{v['a1']};"
        f"--a2:{v['a2']};--a3:{v['a3']};--sl:{v['sl']};--h1:{v['h1']};--h2:{v['h2']};--h3:{v['h3']}}}"
    )


def section(p: dict) -> str:
    sw = "".join(
        f'<div class="sw"><i style="background:{h}"></i><b>{n}</b><small>{h} · {r}</small></div>' for n, h, r in p["palette"]
    )
    ratio = "".join(f'<span style="flex:{f};background:{c}"></span>' for c, f in p["ratio"])
    typ = "".join(f'<div class="row"><small>{a}<br/>{b}</small>{c}</div>' for a, b, c in p["type"])
    stats = "".join(f'<div class="stat"><span class="v">{v}</span><span class="k">{k}</span></div>' for v, k in STATS)
    fc = "".join(f"<li>{x}</li>" for x in p["from_c"])
    fa = "".join(f"<li>{x}</li>" for x in p["from_a"])
    c = p["card"]
    return f"""
<section class="perm" id="{p['id']}">
  <div class="wrap">
    <div class="head">
      <div>
        <div class="code">{p['code']} · {p['tag']}</div>
        <h2>{p['name']}</h2>
        <p class="pitch">{p['pitch']}</p>
      </div>
      <div class="dna2">
        <div><span class="label">From C · Forge</span><ul>{fc}</ul></div>
        <div><span class="label">From A · Bifröst</span><ul>{fa}</ul></div>
        <div class="best"><span class="label">Best for</span>{p['best']}</div>
      </div>
    </div>
    {p['hero']}
    <div class="kit">
      <div class="panel"><span class="label">Palette</span><div class="swatches">{sw}</div><div class="ratio">{ratio}</div></div>
      <div class="panel spec"><span class="label">Type</span>{typ}</div>
    </div>
    <div class="comps">
      <div class="card">
        <span class="num">{c['num']}</span>
        <div class="meta">{c['meta']}</div>
        <h4>{c['title']}</h4>
        <p>{c['body']}</p>
        <div class="btnrow"><span class="chip"><i></i>{c['chip']}</span></div>
      </div>
      <div class="panel marks">
        <span class="label">Seal · mark · controls</span>
        <div class="markrow">
          {p['seal']}
          <svg width="96" height="86"><use href="#hornstar"/></svg>
        </div>
        <div class="btnrow"><button class="btn p" type="button">Read the chronicle</button><button class="btn s" type="button">Sources</button></div>
      </div>
    </div>
    <div class="stats">{stats}</div>
  </div>
</section>"""


def dial_table() -> str:
    keys = [("ground", "Ground"), ("metal", "Metal"), ("display", "Display face"), ("arc", "The arc"), ("runes", "Runes"), ("ornament", "Ornament")]
    head = "".join(f'<th><a href="#{p["id"]}">{p["code"]} · {p["name"]}</a></th>' for p in PERMS)
    rows = "".join(
        f"<tr><td>{label}</td>" + "".join(f"<td>{p['dials'][k]}</td>" for p in PERMS) + "</tr>" for k, label in keys
    )
    chips = "<tr><td>Palette</td>" + "".join(
        "<td><div class='mini'>" + "".join(f"<i style='background:{c}'></i>" for c, _ in p["ratio"]) + "</div></td>"
        for p in PERMS
    ) + "</tr>"
    return f'<div class="tablewrap"><table class="dials"><thead><tr><th></th>{head}</tr></thead><tbody>{chips}{rows}</tbody></table></div>'


CSS = r"""
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:#0f0d0b;color:#E8DFCF;font-family:Geist,system-ui,sans-serif;-webkit-font-smoothing:antialiased;font-variant-numeric:lining-nums}
.wrap{max-width:1240px;margin:0 auto;padding:0 28px}
h1,h2,h3,h4,p{margin:0}
svg{display:block}
a{color:inherit}
.rune{font-family:"Noto Sans Runic",sans-serif}
.label{display:block;font:500 11px/1 "Geist Mono",monospace;letter-spacing:.2em;text-transform:uppercase;opacity:.65;margin-bottom:16px}

/* intro */
.intro{padding:72px 0 60px;background:radial-gradient(80% 60% at 70% 0%,rgba(179,32,42,.16),transparent 70%),radial-gradient(70% 60% at 0% 0%,rgba(62,98,184,.14),transparent 70%),#0f0d0b;border-bottom:1px solid #2c2620}
.eyebrow{font:500 12px/1.4 "Geist Mono",monospace;letter-spacing:.2em;text-transform:uppercase;color:#9a8f80}
.eyebrow a{color:#C9A15E}
.intro h1{font:400 clamp(44px,7vw,96px)/.95 Marcellus,serif;letter-spacing:.02em;margin:20px 0 22px}
.intro h1 em{font-style:normal;color:#C9A15E}
.lede{max-width:780px;font:400 18px/1.6 Newsreader,serif;color:#cfc4b2}
.notes{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;background:#2c2620;border:1px solid #2c2620;margin-top:44px}
.notes>div{background:#14110f;padding:24px 22px}
.notes h4{font:500 11px/1.3 "Geist Mono",monospace;letter-spacing:.18em;text-transform:uppercase;color:#C9A15E;margin-bottom:10px}
.notes p{font:400 15px/1.55 Newsreader,serif;color:#cfc4b2}
.notes .warn h4{color:#E0675A}
.tablewrap{overflow-x:auto;margin-top:40px;border:1px solid #2c2620}
.dials{width:100%;border-collapse:collapse;min-width:860px;font:400 13px/1.35 Geist,sans-serif}
.dials th,.dials td{padding:12px 14px;border-bottom:1px solid #2c2620;text-align:left;vertical-align:middle}
.dials th{font:500 11px/1.3 "Geist Mono",monospace;letter-spacing:.12em;text-transform:uppercase;color:#C9A15E;background:#14110f}
.dials th a{text-decoration:none}
.dials td:first-child{font:500 11px/1 "Geist Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:#9a8f80;width:120px}
.mini{display:flex;height:16px;border-radius:2px;overflow:hidden;width:120px;box-shadow:0 0 0 1px rgba(255,255,255,.08)}
.mini i{flex:1}
.mini i:first-child{flex:3}

/* permutation scaffold */
.perm{background:var(--bg);color:var(--text);padding:0 0 84px;border-top:1px solid var(--line)}
.head{padding:66px 0 34px;display:grid;grid-template-columns:1.15fr 1fr;gap:44px;align-items:end}
.code{font:500 12px/1 "Geist Mono",monospace;letter-spacing:.2em;text-transform:uppercase;color:var(--metal)}
.head h2{font-family:var(--display);font-weight:400;font-size:clamp(54px,7.4vw,104px);line-height:.92;letter-spacing:.03em;margin:14px 0 22px}
.pitch{font:400 18px/1.55 var(--body);color:var(--muted);max-width:600px}
.dna2{display:grid;grid-template-columns:1fr 1fr;gap:18px 24px}
.dna2 ul{list-style:none;margin:0;padding:0;display:grid;gap:7px}
.dna2 li{font:400 14px/1.4 Geist,sans-serif;padding-left:18px;position:relative;color:var(--text);opacity:.9}
.dna2 li::before{content:"";position:absolute;left:0;top:.38em;width:9px;height:9px;background:var(--accent);clip-path:polygon(50% 0,62% 29%,93% 25%,75% 50%,93% 75%,62% 71%,50% 100%,38% 71%,7% 75%,25% 50%,7% 25%,38% 29%)}
.dna2 .best{grid-column:1/-1;border-top:1px solid var(--line);padding-top:14px;font:400 15px/1.45 var(--body)}
.dna2 .best .label{margin-bottom:8px}
.hero{position:relative;overflow:hidden;min-height:580px;border:1px solid var(--line)}
.kit{display:grid;grid-template-columns:1.2fr 1fr;gap:28px;margin-top:28px}
.panel{background:var(--surface);border:1px solid var(--line);padding:28px;position:relative}
.swatches{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.sw{display:flex;flex-direction:column;gap:7px}
.sw i{display:block;height:80px;border-radius:2px;box-shadow:inset 0 0 0 1px rgba(127,127,127,.25)}
.sw b{font:600 13px/1.2 Geist,sans-serif}
.sw small{font:400 11px/1.3 "Geist Mono",monospace;opacity:.7}
.ratio{display:flex;height:12px;margin-top:16px;border-radius:2px;overflow:hidden;box-shadow:0 0 0 1px rgba(127,127,127,.2)}
.spec{display:grid;gap:18px;align-content:start}
.spec .row{display:grid;grid-template-columns:118px 1fr;gap:16px;align-items:baseline;border-top:1px solid var(--line);padding-top:14px}
.spec .row small{font:400 11px/1.4 "Geist Mono",monospace;opacity:.6;letter-spacing:.06em;text-transform:uppercase}
.comps{display:grid;grid-template-columns:1.3fr 1fr;gap:28px;margin-top:28px}
.card{background:var(--surface);border:1px solid var(--line);padding:36px 34px;position:relative;overflow:hidden}
.card .num{position:absolute;right:28px;top:22px;font:400 96px/.9 var(--display);color:transparent;-webkit-text-stroke:1px var(--metal);opacity:.85}
.card .meta{font:500 11px/1.4 var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--metal);max-width:70%}
.card h4{font:400 42px/1.02 var(--display);margin:16px 0 14px;max-width:74%;letter-spacing:.01em}
.card p{font:400 17px/1.6 var(--body);color:var(--muted);max-width:560px}
.chip{display:inline-flex;align-items:center;gap:9px;font:500 11px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;padding:8px 12px;border:1px solid var(--line);color:var(--text)}
.chip i{width:7px;height:7px;background:var(--accent);border-radius:50%}
.btnrow{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:22px}
.btn{font:500 13px/1 var(--ui);letter-spacing:.12em;padding:15px 22px;cursor:pointer;border-radius:0}
.btn.p{background:var(--metal);color:var(--bg);border:1px solid var(--metal)}
.btn.s{background:transparent;color:var(--text);border:1px solid var(--line)}
.marks{display:flex;flex-direction:column;justify-content:space-between}
.markrow{display:flex;gap:34px;align-items:center;justify-content:center;padding:4px 0 6px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);margin-top:28px;border:1px solid var(--line);background:var(--surface)}
.stat{padding:22px 20px}
.stat+.stat{border-left:1px solid var(--line)}
.stat .v{display:block;font:400 58px/.9 var(--display);color:var(--metal);margin-bottom:10px}
.stat .k{display:block;font:500 11px/1.35 var(--mono);letter-spacing:.14em;text-transform:uppercase;opacity:.75}
.cord{width:100%;height:22px}
.carved{background:linear-gradient(#D9B676,#8a6a37);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 -1px 0 rgba(0,0,0,.7))}
.glow{color:#F0B44C;text-shadow:0 0 18px rgba(240,180,76,.55)}

/* C1 forge */
.hero-forge{background:radial-gradient(70% 60% at 50% 38%,rgba(179,32,42,.24),transparent 70%),repeating-linear-gradient(90deg,rgba(255,255,255,.012) 0 2px,transparent 2px 7px),#15120F;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:60px 28px}
.hero-forge .hero-horns{width:min(220px,50%);height:auto;margin-bottom:6px}
.hero-forge h3{font:400 clamp(70px,12vw,170px)/.9 Marcellus;letter-spacing:.16em;padding-left:.16em}
.hero-forge .big{font-size:clamp(28px,4vw,44px);letter-spacing:.7em;padding-left:.7em;margin-top:8px}
.hero-forge p{font:400 italic 21px/1.45 Newsreader;color:#bfb3a0;max-width:560px;margin:22px 0 26px}
#forge .card{border-left:6px solid var(--accent)}
#forge .chip{background:var(--accent);border-color:var(--accent);color:#F3EBDD;font:400 13px/1 "Marcellus SC";letter-spacing:.12em}
#forge .chip i{background:#C9A15E}
#forge .btn.p{clip-path:polygon(10px 0,100% 0,calc(100% - 10px) 100%,0 100%);font-size:15px}
#forge .btn{font-size:15px}

/* C2 ember */
.hero-ember{background:radial-gradient(90% 70% at 50% 110%,#2a1510 0%,#1a120e 40%,#120F0D 72%);min-height:600px}
.hud{position:relative;z-index:3;display:flex;justify-content:space-between;padding:22px 28px;font:400 11px/1 "Geist Mono";letter-spacing:.2em;text-transform:uppercase;color:#8C8277}
.ember-copy{position:relative;z-index:3;text-align:center;padding:48px 24px 0}
.ember-copy .kick{font:400 11px/1 "Geist Mono";letter-spacing:.32em;text-transform:uppercase;color:#F0B44C}
.ember-copy h3{font:400 clamp(70px,13vw,180px)/.88 Marcellus;letter-spacing:.14em;padding-left:.14em;margin:20px 0 10px;color:#F6EEDF;text-shadow:0 0 50px rgba(210,56,43,.35)}
.ember-copy .rune{font-size:22px;letter-spacing:1em;padding-left:1em}
.ember-arc{position:absolute;left:-10%;width:120%;bottom:-22%;height:88%;z-index:2}
.ember-line{position:absolute;z-index:3;left:0;right:0;bottom:30px;text-align:center;font:400 12px/1 "Geist Mono";letter-spacing:.2em;text-transform:uppercase;color:#BDB09C}
#ember .card{background:linear-gradient(180deg,#1f1915,#16120f)}
#ember .card::after{content:"";position:absolute;left:34px;bottom:0;width:140px;height:3px;background:linear-gradient(90deg,#3A5F8F 0 33.3%,#F0B44C 33.3% 66.6%,#D2382B 66.6%)}
#ember .btn{border-radius:999px;letter-spacing:.04em;font-weight:500}

/* C3 night */
.hero-night{background:radial-gradient(120% 90% at 50% 120%,#1b2c52 0%,#0f1830 38%,#0B0F1A 70%)}
.hero-night .sky{position:absolute;inset:0;width:100%;height:100%}
.night-nav{position:relative;z-index:3;display:flex;justify-content:space-between;align-items:center;padding:22px 28px;font:400 11px/1 "Geist Mono";letter-spacing:.2em;text-transform:uppercase;color:#8EA0B8}
.night-nav .brand{display:flex;gap:10px;align-items:center;color:#DCE6EE;font:400 15px/1 Marcellus;letter-spacing:.24em}
.night-copy{position:relative;z-index:3;display:flex;flex-direction:column;align-items:center;text-align:center;padding:30px 24px 0}
.night-horns{width:150px;height:auto;margin-bottom:-4px}
.night-copy h3{font:400 clamp(66px,12vw,168px)/.9 Marcellus;letter-spacing:.16em;padding-left:.16em;color:#F2F6F9}
.night-copy .rune{font-size:22px;letter-spacing:1em;padding-left:1em;color:#C9A15E;margin-top:12px}
.night-copy p{font:400 15px/1 "Geist Mono";letter-spacing:.2em;text-transform:uppercase;color:#A6B3C4;margin-top:26px}
#night .btn{border-radius:999px;letter-spacing:.04em}
#night .chip{border-radius:999px}
#night .card .num{-webkit-text-stroke:1px #C9A15E}

/* C4 rime */
.hero-rime{background:linear-gradient(135deg,#1f2429 0%,#16191D 55%,#121519 100%);min-height:560px}
.hero-rime::before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(115deg,rgba(230,237,241,.035) 0 1px,transparent 1px 9px);pointer-events:none}
.rime-grid{position:relative;display:grid;grid-template-columns:1.25fr 1fr;align-items:center;min-height:560px;padding:40px 48px}
.coords{display:flex;gap:22px;font:400 12px/1 "Geist Mono";letter-spacing:.2em;color:#8FB3CC}
.rime-left h3{font:300 clamp(70px,11vw,160px)/.9 "Cormorant Garamond";letter-spacing:.2em;margin:24px 0 6px;color:#F7FAFB}
.rime-left .rune{font-size:20px;letter-spacing:1.1em;color:#6F7B86}
.rime-left p{font:300 17px/1.6 Geist;color:#A9B5BF;max-width:430px;margin-top:26px}
.ticks{display:flex;justify-content:space-between;margin-top:34px;border-top:1px solid #B99357;padding-top:10px;max-width:520px;font:400 11px/1 "Geist Mono";letter-spacing:.06em;color:#A9B5BF}
.ticks span{position:relative}
.ticks span::before{content:"";position:absolute;left:0;top:-15px;width:1px;height:9px;background:#B99357}
.ticks .now{color:#E0675A}
.ticks .now::before{background:#B3202A;width:7px;height:7px;border-radius:50%;top:-14px;left:-3px}
.rime-right{position:relative;display:flex;flex-direction:column;justify-content:center;align-items:center}
.rime-shield{filter:drop-shadow(0 0 24px rgba(143,179,204,.18))}
.rime-horns{margin-bottom:-26px;opacity:.9}
#rime .card .num{font-weight:300}
#rime .stat .v{font-weight:300;color:#F7FAFB}
#rime .btn{font-weight:400;letter-spacing:.14em;text-transform:uppercase;font-size:11px}
#rime .btn.p{background:#E6EDF1;border-color:#E6EDF1}
#rime .chip i{border-radius:0;width:6px;height:6px}

/* C5 stone */
.hero-stone{background:#ECE5D8;display:grid;grid-template-columns:auto 1fr;gap:48px;align-items:center;padding:44px 56px}
.stone{width:360px;height:auto}
.stone-copy .kick{font:500 12px/1 "IBM Plex Mono";letter-spacing:.24em;text-transform:uppercase;color:#2A4A73}
.stone-copy h3{font:400 clamp(70px,10vw,150px)/.9 Marcellus;letter-spacing:.14em;margin:20px 0 18px;color:#1C1A18}
.stone-copy p{font:400 italic 22px/1.45 Newsreader;color:#4C4740;max-width:520px}
.stone-cap{font:400 13px/1.55 "IBM Plex Mono";color:#6b645a;margin:22px 0 22px;max-width:520px}
.stone-cap .rune{color:#A63A25;letter-spacing:.12em}
.stone-copy .cord{max-width:520px}
#stone .card{outline:1px solid #B8913A;outline-offset:-9px}
#stone .card .num{-webkit-text-stroke:0;color:#A63A25;opacity:.9}
#stone .stat .v{color:#1C1A18}
#stone .stat:first-child .v{color:#A63A25}
#stone .btn.p{background:#1C1A18;border-color:#1C1A18;color:#F6F2EA}
#stone .btn.s{border-color:#B8913A}
#stone .btn{font-size:14px}

/* marks */
.marks-sec{background:#14110f;padding:80px 0;border-top:1px solid #2c2620}
.marks-sec h2,.next h2{font:400 clamp(44px,6vw,76px)/.95 Marcellus;letter-spacing:.02em}
.marks-sec .lede{margin-top:16px}
.markgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#2c2620;border:1px solid #2c2620;margin-top:36px}
.markgrid>div{background:#1a1714;padding:28px 22px 24px;display:flex;flex-direction:column;gap:18px}
.markgrid .art{height:170px;display:flex;align-items:center;justify-content:center;gap:14px}
.markgrid h4{font:500 11px/1.3 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#C9A15E}
.markgrid p{font:400 15px/1.5 Newsreader;color:#cfc4b2}
.favs{display:flex;gap:10px;align-items:end}
.favs .f{display:grid;place-items:center;border-radius:6px}
.typeduel{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#2c2620;border:1px solid #2c2620;margin-top:44px}
.typeduel>div{background:#1a1714;padding:26px 22px}
.typeduel .w{font-size:40px;line-height:1;color:#F2EADB;margin:14px 0 12px}
.typeduel .t{font-size:22px;line-height:1.1;color:#cfc4b2}
.typeduel small{display:block;font:400 12px/1.5 Newsreader;color:#9a8f80;margin-top:14px}
.next{background:#0f0d0b;padding:80px 0 100px;border-top:1px solid #2c2620}
.qs{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;margin-top:36px}
.qs div{border-top:1px solid #3a322a;padding-top:16px}
.qs h4{font:500 11px/1.3 "Geist Mono";letter-spacing:.18em;text-transform:uppercase;color:#C9A15E;margin-bottom:10px}
.qs p{font:400 16px/1.55 Newsreader;color:#cfc4b2}
footer{background:#0f0d0b;color:#6f665b;font:400 12px/1.6 "Geist Mono";padding:0 0 60px}
footer a{color:#9a8f80}

@media (max-width:960px){
  .wrap{padding:0 18px}
  .head,.kit,.comps,.notes,.qs{grid-template-columns:1fr}
  .markgrid,.typeduel{grid-template-columns:1fr 1fr}
  .swatches{grid-template-columns:repeat(2,1fr)}
  .stats{grid-template-columns:1fr 1fr}
  .stat:nth-child(3){border-left:0}
  .stat:nth-child(n+3){border-top:1px solid var(--line)}
  .spec .row{grid-template-columns:1fr;gap:8px}
  .hero{min-height:520px}
  .hud span:nth-child(2),.night-nav span:nth-child(2){display:none}
  .card .num{font-size:60px;right:18px;top:16px}
  .card h4,.card .meta{max-width:100%}
  .card h4{font-size:34px}
  .card .meta{margin-top:56px}
  .markrow{flex-wrap:wrap;gap:20px}
  .rime-grid{grid-template-columns:1fr;padding:34px 22px;gap:10px}
  .rime-right{order:-1}
  .rime-shield{width:150px;height:185px}
  .rime-horns{width:100px;height:85px;margin-bottom:-16px}
  .hero-stone{grid-template-columns:1fr;padding:30px 22px;gap:18px}
  .stone{width:min(300px,80%);margin:0 auto}
  .ember-line{font-size:10px;letter-spacing:.12em;padding:0 16px}
}
@media (max-width:560px){
  .markgrid,.typeduel{grid-template-columns:1fr}
  .dna2{grid-template-columns:1fr}
}
"""

FONTS = (
    "https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300"
    "&family=Forum&family=Geist:wght@300..700&family=Geist+Mono:wght@400;500&family=IBM+Plex+Mono:wght@400;500"
    "&family=Marcellus&family=Marcellus+SC&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400"
    "&family=Noto+Sans+Runic&display=swap"
)


def marks_section() -> str:
    hv = "--h1:#B3202A;--h2:#2A4A73;--h3:#C9A15E;--ss:#C9A15E"
    fav = lambda bg, sz, style: (  # noqa: E731
        f'<div class="f" style="background:{bg};width:{sz}px;height:{sz}px">'
        f'<svg width="{int(sz * .74)}" height="{int(sz * .66)}" style="{style}"><use href="#hornstar"/></svg></div>'
    )
    return f"""
<section class="marks-sec">
  <div class="wrap">
    <div class="eyebrow">Shared across all five</div>
    <h2>Marks to carry forward</h2>
    <p class="lede">Whatever palette wins, these pieces travel with it. All of them come from the real arms and crest, not invented ornament.</p>
    <div class="markgrid">
      <div>
        <div class="art"><svg width="150" height="135" style="{hv}"><use href="#hornstar"/></svg></div>
        <h4>New everyday mark · Horns &amp; star</h4>
        <p>The crest's two horns cradling one star from the shield. Unique to Graah, readable at 16&nbsp;px, and Norse without borrowing anyone else's symbol. Replaces the <span class="rune">ᚼ</span> star from v1.</p>
      </div>
      <div>
        <div class="art favs">{fav("#15120F", 64, hv)}{fav("#0B0F1A", 48, "--h1:#C8283A;--h2:#3E62B8;--h3:#C9A15E;--ss:#C9A15E")}{fav("#ECE5D8", 36, "--h1:#A63A25;--h2:#2A4A73;--h3:#B8913A;--ss:#A63A25")}{fav("#16191D", 24, "--h1:#B3202A;--h2:#8FB3CC;--h3:#B99357;--ss:#B3202A")}</div>
        <h4>At favicon &amp; app-icon size</h4>
        <p>Same mark on four grounds, 64 → 24&nbsp;px. The two-tone horns stay legible; the star keeps it from reading as just “horns”.</p>
      </div>
      <div>
        <div class="art"><svg width="120" height="148" style="--sf:#E8DFCF;--ss:#B3202A;--a1:#2A4A73;--a2:#C9A15E;--a3:#B3202A;--sl:#15120F"><use href="#shield"/></svg><svg width="96" height="118" style="color:#E8DFCF;--a1:#3E62B8;--a2:#C9A15E;--a3:#C8283A;--ss:#C8283A"><use href="#shield-line"/></svg></div>
        <h4>The full arms · ceremony only</h4>
        <p>Filled shield for print, seal and the hero. Monoline shield for screens and the futurist directions. Use the shield sparingly so it keeps its weight.</p>
      </div>
      <div>
        <div class="art" style="flex-direction:column;gap:18px">
          <div style="font:400 34px/1 Marcellus;letter-spacing:.32em;padding-left:.32em;color:#F2EADB">GRAAH</div>
          <div class="rune carved" style="font-size:22px;letter-spacing:.9em;padding-left:.9em">{RUNES}</div>
          {cord(220, 18, 40, "#C9A15E", "#8E1C24", "#1a1714", 2)}
        </div>
        <h4>Wordmark · runes · cord</h4>
        <p>Marcellus wordmark with the Younger Futhark spelling beneath. The two-strand cord is the divider. Runes only ever appear as the name, never in running text.</p>
      </div>
    </div>

    <div class="typeduel">
      <div><span class="label">Marcellus</span><div class="w" style="font-family:Marcellus;letter-spacing:.12em">GRAAH</div><div class="t" style="font-family:Marcellus">The Glacier You Must Not Name</div><small>Roman inscriptional with flared strokes. Carved, warm, sturdy at all sizes. Current favourite.</small></div>
      <div><span class="label">Cormorant · wide</span><div class="w" style="font:300 40px/1 'Cormorant Garamond';letter-spacing:.2em">GRAAH</div><div class="t" style="font:400 24px/1.1 'Cormorant Garamond'">The Glacier You Must Not Name</div><small>Bifröst's face. Elegant and cool, but thin on screens. Best in Rimfrost.</small></div>
      <div><span class="label">Forum</span><div class="w" style="font-family:Forum;letter-spacing:.14em">GRAAH</div><div class="t" style="font-family:Forum">The Glacier You Must Not Name</div><small>Plainer Roman capitals. More neoclassical, less Viking. A calmer fallback.</small></div>
      <div><span class="label">Cinzel</span><div class="w" style="font-family:Cinzel;letter-spacing:.12em">GRAAH</div><div class="t" style="font-family:Cinzel">The Glacier You Must Not Name</div><small>Most dramatic, all caps only. Used on a lot of fantasy and film posters, so it reads less personal.</small></div>
    </div>
  </div>
</section>"""


def page() -> str:
    perms = "".join(section(p) for p in PERMS)
    varcss = "\n".join(var_block(p) for p in PERMS)
    toc = "".join(f'<a href="#{p["id"]}">{p["code"]} · {p["name"]}</a>' for p in PERMS)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="robots" content="noindex, nofollow" />
<link rel="icon" href="/graah-coa.png" type="image/png" />
<title>Graah — Identity exploration v0.2 · Forge × Bifröst</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="{FONTS}" rel="stylesheet" />
<style>{CSS}
{varcss}
.toc{{display:flex;flex-wrap:wrap;gap:10px;margin-top:34px}}
.toc a{{font:500 12px/1 "Geist Mono",monospace;letter-spacing:.12em;text-transform:uppercase;text-decoration:none;border:1px solid #3a322a;padding:11px 14px;border-radius:999px}}
.toc a:hover{{border-color:#C9A15E;color:#C9A15E}}
</style>
</head>
<body>
{DEFS}
<section class="intro">
  <div class="wrap">
    <div class="eyebrow">Graah · Visual identity · v0.2 · <a href="/theme-lab/v1/">v0.1 (all four directions)</a> · <a href="/theme-lab/">latest →</a></div>
    <h1>Forge, <em>under</em><br/>the northern sky.</h1>
    <p class="lede">You picked C · Forge as the base and wanted parts of A · Bifröst. B · Gustavian and D · Meridian are dropped. Below are five ways to combine the two. Each moves the same dials: ground, metal, display face, how the arc shows up, how the runes are treated, and how much ornament. They run from pure forge to cold and futurist, plus a daylight version for reading.</p>
    <div class="notes">
      <div><h4>What changed since v0.1</h4><p>The crest horns are redrawn with their true tinctures. The cord has real over-and-under crossings. Fjord-steel blue is back in every palette, so the arms' blue, gold and red always appear together.</p></div>
      <div class="warn"><h4>Retired: the <span class="rune">ᚼ</span> star as a logo</h4><p>The six-armed hagall rune I proposed as the everyday mark was also used by the SS (on the Totenkopf ring) and is still used by far-right groups today. That's a bad fit for a family whose chronicle includes Ravensbrück and the resistance. It stays only inside the name <span class="rune">ᚴᚱᛅᛅᚼ</span>, and the horns-and-star mark replaces it.</p></div>
      <div><h4>Reading the page</h4><p>Every direction gets the same kit: a hero, palette with usage ratio, type, a chapter card, seal and mark, buttons and the stats row. The table below compares them at a glance.</p></div>
    </div>
    {dial_table()}
    <nav class="toc">{toc}<a href="#marks">Marks &amp; type</a></nav>
  </div>
</section>
{perms}
<div id="marks"></div>
{marks_section()}
<section class="next">
  <div class="wrap">
    <h2>What to send back</h2>
    <div class="qs">
      <div><h4>1 · Ground</h4><p>Tar (warm black), Polar Night (blue black), Gunmetal (cold grey), or Limewash (light)? You can pick one dark and one light.</p></div>
      <div><h4>2 · Display face</h4><p>Marcellus (carved), Cormorant wide (refined), or Forum (plain Roman)? This one choice sets most of the mood.</p></div>
      <div><h4>3 · How much Viking</h4><p>The ornament dial: C1 has the most horns, cord and carving. C4 has the least, just hairlines. Where on that line feels like the family?</p></div>
    </div>
  </div>
</section>
<footer><div class="wrap">Exploration only — not wired into graah.se. Generated by design/theme-lab/build_v2.py. Fonts: Google Fonts (OFL). Runic spellings in Younger Futhark.</div></footer>
</body>
</html>
"""


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page(), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")
