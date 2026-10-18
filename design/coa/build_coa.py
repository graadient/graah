#!/usr/bin/env python3
"""Writes the site's copies of the arms (public/graah-coa*.svg).

The geometry lives in theme/tools/arms.py. The theme's own copies are
written by theme/build.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "theme" / "tools"))
from arms import *  # noqa: E402,F403
from arms import TIP_Y, doc, flat, mono, shaded  # noqa: E402

if __name__ == "__main__":
    out = {
        "graah-coa.svg": doc(shaded()),
        "graah-coa-flat.svg": doc(flat()),
        "graah-coa-mono.svg": doc(mono()),
        "graah-coa-brass.svg": doc(mono("b", "#C9A15E", border=4)),
    }
    for name, svg in out.items():
        (ROOT / "public" / name).write_text(svg, encoding="utf-8")
        print("wrote public/" + name, f"({len(svg)} bytes)")
    print(f"tip y = {TIP_Y:.2f}")
