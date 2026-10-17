#!/usr/bin/env python3
"""Faithful vector trace of public/graah-coa.png (the family's original arms).

Geometry and shading were measured from the 156×192 PNG (edge fitting, radial
profiles, colour regression), not redrawn by eye. Units are the PNG's pixels,
so the SVG overlays the original 1:1.

Run:  python3 design/coa/build_coa.py
Writes:
  public/graah-coa.svg       full-colour arms, shaded like the original
  public/graah-coa-flat.svg  same geometry, flat tinctures (print, embroidery)
  public/graah-coa-mono.svg  same geometry, one colour (currentColor) for seals, signets, etching
"""

from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

AX = 78.0  # axis of symmetry

# ── shield outline (centre-line of the dark border) ──
TOP = 2.04
SIDE_L, SIDE_R = 2.25, 153.75
ARC_Y = 70.2  # where the straight sides turn into compass arcs
ARC_R = 129.3
_cx_r = SIDE_R - ARC_R
TIP_Y = ARC_Y + math.sqrt(ARC_R**2 - (AX - _cx_r) ** 2)
SHIELD = (
    f"M{SIDE_L} {TOP} H{SIDE_R} V{ARC_Y} "
    f"A{ARC_R} {ARC_R} 0 0 1 {AX} {TIP_Y:.2f} "
    f"A{ARC_R} {ARC_R} 0 0 1 {SIDE_L} {ARC_Y} Z"
)
BORDER_W = 1.6

# ── the bend: three concentric bands ──
BAND_C = (AX, 222.65)
BAND_R = (156.3, 141.6, 127.9, 113.6)  # outer of blue → inner of red

# ── stars: six-pointed, point up ──
STARS = ((42.58, 38.52), (113.42, 38.52), (78.0, 142.3))
STAR_R, STAR_r = 25.9, 12.85


def star(cx: float, cy: float, R: float = STAR_R, r: float = STAR_r) -> str:
    pts = []
    for i in range(12):
        a = math.radians(-90 + i * 30)
        rr = R if i % 2 == 0 else r
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    return " ".join(pts)


def ring(r_out: float, r_in: float) -> str:
    """Annular band clipped later by the shield; drawn as two arcs across the full width."""
    cx, cy = BAND_C

    def pt(r: float, x: float) -> tuple[float, float]:
        return x, cy - math.sqrt(r * r - (x - cx) ** 2)

    x0, x1 = -4.0, 160.0
    a, b = pt(r_out, x0), pt(r_out, x1)
    c, d = pt(r_in, x1), pt(r_in, x0)
    return (
        f"M{a[0]:.2f} {a[1]:.2f} A{r_out} {r_out} 0 0 1 {b[0]:.2f} {b[1]:.2f} "
        f"L{c[0]:.2f} {c[1]:.2f} A{r_in} {r_in} 0 0 0 {d[0]:.2f} {d[1]:.2f} Z"
    )


BANDS = [ring(BAND_R[i], BAND_R[i + 1]) for i in range(3)]
TITLE = "The Graah coat of arms: three red six-pointed stars and a blue, gold and red bend on a silver shield"


def shaded(uid: str = "g") -> str:
    """Matches the original's lighting: light from the upper left."""
    stops = lambda pairs: "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in pairs)  # noqa: E731
    cx, cy = BAND_C
    rr = BAND_R[0]
    # radial overlay: each band a touch darker at its inner edge, lighter at its outer edge
    radial = []
    for i in range(3):
        o_out, o_in = BAND_R[i] / rr, BAND_R[i + 1] / rr
        radial.append((o_in + 0.0005, "#000", 0.06))
        radial.append((o_out - 0.0005, "#000", 0))
    radial = [
        f'<stop offset="{o:.4f}" stop-color="{c}" stop-opacity="{op}"/>' for o, c, op in sorted(radial)
    ]
    defs = (
        f'<clipPath id="{uid}-clip"><path d="{SHIELD}"/></clipPath>'
        f'<linearGradient id="{uid}-field" gradientUnits="userSpaceOnUse" x1="20" y1="10" x2="142" y2="178">'
        + stops([(0, "#FFFFFF"), (0.18, "#FEFEFE"), (0.33, "#F9F9FA"), (0.55, "#F0F1F2"), (0.8, "#E0E1E4"), (1, "#D2D4D8")])
        + "</linearGradient>"
        f'<linearGradient id="{uid}-blue" gradientUnits="userSpaceOnUse" x1="10" y1="0" x2="146" y2="0">'
        + stops([(0, "#1D7CFC"), (0.5, "#0360E8"), (1, "#0042C6")])
        + "</linearGradient>"
        f'<linearGradient id="{uid}-gold" gradientUnits="userSpaceOnUse" x1="10" y1="0" x2="146" y2="0">'
        + stops([(0, "#FFDB24"), (0.5, "#FFCC0F"), (1, "#FCBA02")])
        + "</linearGradient>"
        f'<linearGradient id="{uid}-red" gradientUnits="userSpaceOnUse" x1="10" y1="0" x2="146" y2="0">'
        + stops([(0, "#FF1416"), (0.5, "#E80203"), (1, "#BA0101")])
        + "</linearGradient>"
        f'<radialGradient id="{uid}-depth" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{rr}">'
        + "".join(radial)
        + "</radialGradient>"
        f'<linearGradient id="{uid}-star" gradientUnits="userSpaceOnUse" x1="22" y1="12" x2="112" y2="172">'
        + stops([(0, "#FF2427"), (0.55, "#E8080B"), (1, "#BE0003")])
        + "</linearGradient>"
        f'<filter id="{uid}-shadow" x="-5%" y="-5%" width="115%" height="115%">'
        f'<feDropShadow dx=".9" dy="1.3" stdDeviation=".8" flood-color="#1C2127" flood-opacity=".5"/></filter>'
        f'<linearGradient id="{uid}-rim" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="156" y2="192">'
        + stops([(0, "#3A424B"), (1, "#1C2127")])
        + "</linearGradient>"
    )
    band_edge = 'stroke="#000" stroke-opacity=".42" stroke-width=".9"'
    body = (
        f'<path d="{SHIELD}" fill="#fff" filter="url(#{uid}-shadow)"/>'
        f'<path d="{SHIELD}" fill="url(#{uid}-field)"/>'
        f'<g clip-path="url(#{uid}-clip)">'
        f'<path d="{BANDS[0]}" fill="url(#{uid}-blue)" {band_edge}/>'
        f'<path d="{BANDS[1]}" fill="url(#{uid}-gold)" {band_edge}/>'
        f'<path d="{BANDS[2]}" fill="url(#{uid}-red)" {band_edge}/>'
        f'<path d="{ring(BAND_R[0], BAND_R[3])}" fill="url(#{uid}-depth)"/>'
        "</g>"
        f'<g fill="url(#{uid}-star)" stroke="#7A0003" stroke-opacity=".55" stroke-width=".8" stroke-linejoin="miter">'
        + "".join(f'<polygon points="{star(x, y)}"/>' for x, y in STARS)
        + "</g>"
        f'<path d="{SHIELD}" fill="none" stroke="url(#{uid}-rim)" stroke-width="{BORDER_W}" stroke-linejoin="miter"/>'
    )
    return f"<defs>{defs}</defs>{body}"


def flat(uid: str = "f") -> str:
    return (
        f'<defs><clipPath id="{uid}-clip"><path d="{SHIELD}"/></clipPath></defs>'
        f'<path d="{SHIELD}" fill="#F4F5F7"/>'
        f'<g clip-path="url(#{uid}-clip)">'
        f'<path d="{BANDS[0]}" fill="#0A5FE0"/><path d="{BANDS[1]}" fill="#FCC514"/><path d="{BANDS[2]}" fill="#DA0A0C"/></g>'
        + "".join(f'<polygon points="{star(x, y)}" fill="#E5090C"/>' for x, y in STARS)
        + f'<path d="{SHIELD}" fill="none" stroke="#262C33" stroke-width="{BORDER_W}"/>'
    )


def mono(uid: str = "m", color: str = "currentColor", gap: float = 1.6, border: float = 3.2) -> str:
    """One colour. Bands are solid with hairline gaps between them so the three stay legible;
    stars are knocked out of nothing — they sit on the empty field like the original."""
    cx, cy = BAND_C
    gaps = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#000" stroke-width="{gap}"/>' for r in BAND_R[1:3]
    )
    return (
        f'<defs><clipPath id="{uid}-clip"><path d="{SHIELD}"/></clipPath>'
        f'<mask id="{uid}-gaps" maskUnits="userSpaceOnUse" x="0" y="0" width="156" height="192">'
        f'<rect width="156" height="192" fill="#fff"/>{gaps}</mask></defs>'
        f'<g fill="{color}">'
        f'<g clip-path="url(#{uid}-clip)"><path d="{ring(BAND_R[0], BAND_R[3])}" mask="url(#{uid}-gaps)"/></g>'
        + "".join(f'<polygon points="{star(x, y)}"/>' for x, y in STARS)
        + "</g>"
        f'<path d="{SHIELD}" fill="none" stroke="{color}" stroke-width="{border}"/>'
    )


def doc(inner: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 156 192" role="img">\n'
        f"  <title>{TITLE}</title>\n  {inner}\n</svg>\n"
    )


if __name__ == "__main__":
    out = {
        "graah-coa.svg": doc(shaded()),
        "graah-coa-flat.svg": doc(flat()),
        "graah-coa-mono.svg": doc(mono()),
    }
    for name, svg in out.items():
        (ROOT / "public" / name).write_text(svg, encoding="utf-8")
        print("wrote public/" + name, f"({len(svg)} bytes)")
    print(f"tip y = {TIP_Y:.2f}")
