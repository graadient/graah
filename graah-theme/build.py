#!/usr/bin/env python3
"""Regenerate the generated files in graah-theme/ from the values below.

Run:  python3 graah-theme/build.py

Edit the tokens HERE, not in the generated files. Writes:
  tokens/tokens.json   design tokens (W3C DTCG format) for any platform
  tokens/tokens.css    the same tokens as CSS custom properties
  tailwind.css         Tailwind v4 bridge (bg-graah-night, font-graah-display, ...)
  assets/arms/*.svg    the arms: shaded, flat, mono (currentColor), brass
  assets/seal/*.svg    the seal: wax and one-colour
  assets/favicon.svg
  react/geometry.ts    arms + seal geometry for the React components

Stdlib only. If fontTools is installed (pip install fonttools), the seal's rune
ring is converted to outlines, so the seal SVGs need no font. Otherwise the
existing outlines in react/geometry.ts are kept.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tools"))
import arms as A  # noqa: E402

# ───────────────────────── tokens ─────────────────────────

# key, value, name, role
COLORS = [
    ("night", "#0B0F1A", "Polar Night", "Page ground. About 60% of any screen."),
    ("abyss", "#080B14", "Abyss", "Footer and the deepest bands."),
    ("fjord", "#111829", "Deep Fjord", "Cards and panels."),
    ("fjord-deep", "#0E1424", "Fjord Deep", "Inset panels and form fields."),
    ("fjord-2", "#16203A", "Fjord 2", "Raised surface."),
    ("fjord-3", "#1B2642", "Fjord 3", "Highest surface, hover."),
    ("line", "#26304A", "Fjord Line", "Hairlines and borders, always 1px."),
    ("separator", "#1D2640", "Separator", "Quiet dividers inside panels."),
    ("rime", "#F2F6F9", "Rime", "Headlines and the wordmark."),
    ("glacier", "#DCE6EE", "Glacier", "Body text. 15:1 on night."),
    ("mist", "#A6B3C4", "Mist", "Secondary text. 9:1 on night."),
    ("smoke", "#8EA0B8", "Sea Smoke", "Muted text, captions. 7:1 on night."),
    ("brass", "#C9A15E", "Brass", "The one action colour: buttons, focus, labels, metal. 8:1 on night."),
    ("glow", "#E9C98A", "Rune Glow", "Links, highlights, glowing runes."),
    ("red", "#C8283A", "Star Red", "The stars and danger. Large text or fills only (3.5:1 on night)."),
    ("red-soft", "#FF8C99", "Star Red Soft", "Danger text on dark grounds."),
    ("wax", "#6E1414", "Wax", "The seal."),
    ("wax-rim", "#9A2A2A", "Wax Rim", "The seal's rim."),
    ("steel", "#3E62B8", "Steel Blue", "The aurora. Decorative only (3.3:1 on night)."),
]

# Heraldic tinctures: ONLY for the arms themselves, never for UI.
HERALDRY = [
    ("argent", "#F4F5F7", "Argent", "The silver field."),
    ("azure", "#0A5FE0", "Azure", "Outer band of the bend."),
    ("or", "#FCC514", "Or", "Middle band of the bend."),
    ("gules", "#DA0A0C", "Gules", "Inner band of the bend."),
    ("star", "#E5090C", "Star", "The three six-pointed stars."),
    ("border", "#262C33", "Border", "The shield outline."),
]

FONTS = [
    ("display", '"Forum", "Cormorant Garamond", Georgia, serif', "Wordmark, headlines, numerals, card titles. One weight (400)."),
    ("body", '"Geist", ui-sans-serif, system-ui, sans-serif', "Body text, buttons, UI. Weights 300-500."),
    ("body-alt", '"Newsreader", Georgia, serif', "Optional bookish body text (long reading)."),
    ("mono", '"Geist Mono", ui-monospace, monospace', "Labels, dates, places, tabs, chips. Uppercase, tracked."),
    ("runes", '"Noto Sans Runic", sans-serif', "The runes."),
]

DIMENSIONS = [
    ("radius-control", "999px", "Buttons, tabs, toggles, chips: pills."),
    ("radius-surface", "2px", "Cards, panels, alerts: nearly square."),
    ("radius-field", "4px", "Inputs, selects."),
    ("hairline", "1px", "Every border."),
    ("tracking-wordmark", "0.16em", "GRAAH at hero size."),
    ("tracking-signature", "0.32em", "GRAAH in nav, footer, seal."),
    ("tracking-label", "0.2em", "Mono uppercase labels."),
    ("tracking-runes", "1em", "ᚴᚱᛅᛅᚼ under the wordmark."),
]

EFFECTS = [
    ("glow-text", "0 0 6px rgba(233, 201, 138, 0.55), 0 0 22px rgba(201, 161, 94, 0.45)", "text-shadow for glowing runes (bright phase)."),
    ("glow-text-dim", "0 0 3px rgba(233, 201, 138, 0.35), 0 0 12px rgba(201, 161, 94, 0.25)", "text-shadow for glowing runes (dim phase)."),
    ("glow-brass", "0 0 22px -4px rgba(233, 201, 138, 0.55)", "box-shadow on hover of brass buttons and on the active tab."),
    ("shadow-overlay", "0 0 0 1px #26304A inset, 0 18px 40px -12px rgba(0, 0, 0, 0.6)", "Menus, popovers, dialogs."),
    ("sky", "radial-gradient(120% 90% at 50% 120%, #1B2C52 0%, #0F1830 38%, #0B0F1A 70%)", "The night-sky ground behind heroes."),
    ("aurora", "linear-gradient(90deg, #3E62B8, #C9A15E 50%, #C8283A)", "Steel to brass to red, the colours of the bend. Progress bars, timelines."),
    ("duration-breathe", "5s", "Rune glow cycle."),
    ("duration-twinkle", "4.5s", "Star twinkle cycle."),
    ("ease", "cubic-bezier(0.2, 0.7, 0.2, 1)", "Default easing."),
]

RUNES = "ᚴᚱᛅᛅᚼ"
SEAL_TEXT = "ᚴᚱᛅᛅᚼ ᛬ ᛋᚢᛚᛁᛋᛏᛁᛏ ᛬ ᚴᚱᛅᛅᚼ ᛬ ᛋᚢᛚᛁᛋᛏᛁᛏ ᛬"

HEADER_CSS = "/* GENERATED by graah-theme/build.py — edit the values there, not here. */\n"


def tokens_json() -> str:
    def group(rows):
        return {k: {"$type": "color", "$value": v, "$description": f"{n}. {r}"} for k, v, n, r in rows}

    data = {
        "$description": "Graah theme design tokens (Night Smithy). Generated by graah-theme/build.py.",
        "color": group(COLORS),
        "heraldry": group(HERALDRY),
        "font": {k: {"$type": "fontFamily", "$value": v, "$description": d} for k, v, d in FONTS},
        "dimension": {k: {"$type": "dimension", "$value": v, "$description": d} for k, v, d in DIMENSIONS},
        "effect": {k: {"$type": "string", "$value": v, "$description": d} for k, v, d in EFFECTS},
        "text": {
            "runes": {"$type": "string", "$value": RUNES, "$description": "GRAAH in Younger Futhark."},
            "seal": {"$type": "string", "$value": SEAL_TEXT, "$description": "Seal ring: Graah · Søllested, twice."},
        },
    }
    return json.dumps(data, ensure_ascii=False, indent=4) + "\n"


def tokens_css() -> str:
    out = [HEADER_CSS, ":root {"]
    out.append("    /* Colour */")
    out += [f"    --graah-{k}: {v}; /* {n} */" for k, v, n, _ in COLORS]
    out.append("\n    /* Heraldic tinctures: the arms only, never UI */")
    out += [f"    --graah-heraldry-{k}: {v};" for k, v, _, _ in HERALDRY]
    out.append("\n    /* Type */")
    out += [f"    --graah-font-{k}: {v};" for k, v, _ in FONTS]
    out.append("\n    /* Shape and spacing */")
    out += [f"    --graah-{k}: {v};" for k, v, _ in DIMENSIONS]
    out.append("\n    /* Light and motion */")
    out += [f"    --graah-{k}: {v};" for k, v, _ in EFFECTS]
    out.append("}")
    return "\n".join(out) + "\n"


def tailwind_css() -> str:
    lines = [
        HEADER_CSS,
        "/*",
        " * Graah theme for Tailwind CSS v4. Import after tailwindcss:",
        ' *   @import "tailwindcss";',
        ' *   @import "./graah-theme/tailwind.css";',
        " * Gives bg-graah-night, text-graah-brass, font-graah-display, rounded-graah-control, ...",
        " */",
        '@import "./graah.css";',
        "",
        "@theme inline {",
    ]
    lines += [f"    --color-graah-{k}: var(--graah-{k});" for k, *_ in COLORS]
    lines += [f"    --font-graah-{k}: var(--graah-font-{k});" for k, *_ in FONTS]
    lines += [f"    --radius-graah-{k.removeprefix('radius-')}: var(--graah-{k});" for k, *_ in DIMENSIONS if k.startswith("radius")]
    lines += [f"    --tracking-graah-{k.removeprefix('tracking-')}: var(--graah-{k});" for k, *_ in DIMENSIONS if k.startswith("tracking")]
    lines += ["    --shadow-graah-glow: var(--graah-glow-brass);", "    --shadow-graah-overlay: var(--graah-shadow-overlay);"]
    lines.append("}")
    return "\n".join(lines) + "\n"


# ───────────────────────── seal ─────────────────────────

SEAL_ARMS = (68, 63.5, 64, 79)  # x, y, w, h — optically centred (a shield's weight sits high)


def seal_arms_transform() -> str:
    """The SEAL_ARMS box as a transform on the 156×192 arms (fit and centre, like viewBox meet)."""
    x, y, w, h = SEAL_ARMS
    k = min(w / 156, h / 192)
    return f"translate({x + (w - 156 * k) / 2:.3f} {y + (h - 192 * k) / 2:.3f}) scale({k:.5f})"


def outline_ring() -> str | None:
    """The seal's rune ring as one path, in the seal's 200×200 space. Mirrors the SVG
    <textPath> it replaces: radius 75, starts at 9 o'clock, runs clockwise,
    font-size 14.5, letter-spacing 5.2."""
    try:
        from fontTools.pens.svgPathPen import SVGPathPen
        from fontTools.pens.transformPen import TransformPen
        from fontTools.ttLib import TTFont
    except ImportError:
        return None
    font_path = HERE / "tools" / "NotoSansRunic-Regular.ttf"
    if not font_path.exists():
        return None
    font = TTFont(font_path)
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    k = 14.5 / font["head"].unitsPerEm
    r, s, parts = 75.0, 0.0, []
    for ch in SEAL_TEXT:
        name = cmap[ord(ch)]
        adv = gs[name].width * k
        mid = s + adv / 2
        th = math.pi + mid / r
        px, py = 100 + r * math.cos(th), 100 + r * math.sin(th)
        rot = th + math.pi / 2
        c, n = math.cos(rot), math.sin(rot)
        # glyph unit (u, v) → local (u*k - adv/2, -v*k) → rotate → translate
        t = (k * c, k * n, k * n, -k * c, px - adv / 2 * c, py - adv / 2 * n)
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        gs[name].draw(TransformPen(pen, t))
        parts.append(pen.getCommands())
        s += adv + 5.2
    return "".join(parts)


def seal_svg(ring: str, mono: bool = False) -> str:
    m = "currentColor" if mono else "#C9A15E"
    arms_inner = A.mono("s", m, border=4)
    if mono:
        rings = (
            f'<circle cx="100" cy="100" r="96" fill="none" stroke="{m}" stroke-width="2.4"/>'
            f'<circle cx="100" cy="100" r="88" fill="none" stroke="{m}" stroke-width=".8"/>'
        )
    else:
        rings = (
            '<circle cx="100" cy="100" r="97" fill="#6E1414"/>'
            '<circle cx="100" cy="100" r="92" fill="none" stroke="#9A2A2A" stroke-width="2"/>'
        )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img">\n'
        "  <title>The Graah seal: the arms in brass, ringed by runes reading Graah · Søllested</title>\n  "
        + rings
        + f'<circle cx="100" cy="100" r="60" fill="none" stroke="{m}" stroke-width="1"/>'
        + f'<path fill="{m}" d="{ring}"/>'
        + f'<g transform="{seal_arms_transform()}">{arms_inner}</g>'
        + "\n</svg>\n"
    )


# ───────────────────────── react geometry ─────────────────────────


def ts_string(s: str) -> str:
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def geometry_ts(ring: str) -> str:
    shaded = A.shaded("__UID__")
    flat = A.flat("__UID__")
    mono = A.mono("__UID__", "__COLOR__")
    stars = [A.star(x, y) for x, y in A.STARS]
    return f"""// GENERATED by graah-theme/build.py — do not edit by hand.

/** viewBox of the arms. */
export const ARMS_VIEWBOX = '0 0 156 192'
export const ARMS_ASPECT = 156 / 192
export const ARMS_TITLE = {ts_string(A.TITLE)}

/** The shield outline. */
export const SHIELD_PATH = {ts_string(A.SHIELD)}

/** Blue, gold and red bands of the bend (clip them to SHIELD_PATH). */
export const BAND_PATHS = [{", ".join(ts_string(b) for b in A.BANDS)}] as const

/** The three six-pointed stars, as <polygon points>. */
export const STAR_POINTS = [{", ".join(ts_string(p) for p in stars)}] as const

/** Full SVG inner markup per variant. Replace __UID__ with a unique id; mono also takes __COLOR__. */
export const ARMS_MARKUP = {{
    shaded: {ts_string(shaded)},
    flat: {ts_string(flat)},
    mono: {ts_string(mono)},
}} as const

/** GRAAH in Younger Futhark. */
export const RUNES = '{RUNES}'

/** The seal's ring text: Graah · Søllested, twice. */
export const SEAL_TEXT = '{SEAL_TEXT}'

/** The seal's ring text as outlines, in the seal's 200×200 space. */
export const SEAL_RING_PATH = {ts_string(ring)}

/** Where the arms sit inside the seal (optically centred), as a transform on the 156×192 arms. */
export const SEAL_ARMS_TRANSFORM = '{seal_arms_transform()}'
"""


# ───────────────────────── main ─────────────────────────


def write(rel: str, text: str) -> None:
    p = HERE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print(f"wrote {rel} ({len(text.encode()) // 1024 or 1} KB)")


def main() -> None:
    write("tokens/tokens.json", tokens_json())
    write("tokens/tokens.css", tokens_css())
    write("tailwind.css", tailwind_css())

    write("assets/arms/graah-arms.svg", A.doc(A.shaded()))
    write("assets/arms/graah-arms-flat.svg", A.doc(A.flat()))
    write("assets/arms/graah-arms-mono.svg", A.doc(A.mono()))
    write("assets/arms/graah-arms-brass.svg", A.doc(A.mono("b", "#C9A15E", border=4)))
    write("assets/favicon.svg", A.doc(A.flat()))

    ring = outline_ring()
    if ring is None:
        old = (HERE / "react" / "geometry.ts").read_text(encoding="utf-8")
        ring = re.search(r"SEAL_RING_PATH =\s*'([^']*)'", old).group(1)
        print("fontTools or the runic font is missing: keeping the existing seal outlines")
    write("assets/seal/graah-seal.svg", seal_svg(ring))
    write("assets/seal/graah-seal-mono.svg", seal_svg(ring, mono=True))
    write("react/geometry.ts", geometry_ts(ring))
    print("now run: npx biome format --write graah-theme")


if __name__ == "__main__":
    main()
