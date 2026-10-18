# Graah brand guidelines

Neoclassical, a little futuristic, with Nordic and Viking hints. It should feel like a polar
night over a smithy: dark and calm, lit by brass. Not like a fantasy game.

## The arms

The family's original arms: a silver shield with three red six-pointed stars and a bend of
blue, gold and red. The files in `assets/arms/` are a measured trace of the original, not a
redesign.

- Always use the supplied files or `<Arms>`. Never redraw, simplify or "modernise" them.
- Always keep **all three stars** and **all three bands** (blue, gold, red, in that order from the outside).
- Variants: `graah-arms.svg` (shaded, for screens), `-flat` (print, embroidery, under 32px),
  `-mono` (one colour via `currentColor`: etching, stamps, watermarks), `-brass` (the seal's metal).
- Heraldic colours (`--graah-heraldry-*`) belong to the arms only. Never use them for UI.
- Don't stretch, rotate, outline, crop, put text on, or add effects. The one allowed effect
  is a soft steel-blue glow on dark grounds (`drop-shadow(0 0 28px rgba(62,98,184,.3))`).
- Clear space: at least a quarter of the shield's width on every side. Smallest size: 16px tall.
- The horns are an optional crest only. They never replace the shield.

## The seal

Oxblood wax, a brass ring of runes, the arms in brass in the middle.

- The ring reads **ᚴᚱᛅᛅᚼ ᛬ ᛋᚢᛚᛁᛋᛏᛁᛏ**, twice: *Graah · Søllested*, the name and the family's
  castle on Lolland. Younger Futhark has no G, E, Ø or D, so ᚴ stands for G, ᛁ for E, ᚢ for Ø
  and ᛏ for D. ᛬ is the word divider. Don't change or extend the text.
- Use it as a signature: footers, letters, invitations, about pages. Not as a button or icon.
- 64px and larger only. Below that, use the arms alone.
- `graah-seal.svg` for screens. `graah-seal-mono.svg` (one colour) for signet rings, embossing,
  letterpress.

## The runes

ᚴᚱᛅᛅᚼ is GRAAH in Younger Futhark: kaun, reið, ár, ár, hagall.

- Only ever the whole name, set under or next to the Latin wordmark, glowing in brass (`.graah-runes`, `<Runes>`).
- **Never use ᚼ (hagall) on its own, and never as a logo, icon or ornament.** The standalone
  six-armed rune has far-right associations, and the family chronicle includes resistance to
  the Nazis and Ravensbrück. Inside the name it is fine.
- Don't write new text in runes, and don't use runes as decoration or dividers on their own.
- Runes are decorative for screen readers: give them `aria-label="Graah, in runes"` or hide them.

## Colour

Dark only. By area: about 75% night and fjord, 12% glacier text, and everything else together
under 15%.

| Colour | Hex | Role | Contrast on night |
| --- | --- | --- | --- |
| Polar Night | `#0B0F1A` | Ground | |
| Deep Fjord | `#111829` | Cards, panels | |
| Fjord Line | `#26304A` | All borders, 1px | decorative |
| Rime | `#F2F6F9` | Headlines | 17:1 |
| Glacier | `#DCE6EE` | Body text | 15:1 |
| Mist | `#A6B3C4` | Secondary text | 9:1 |
| Sea Smoke | `#8EA0B8` | Muted text, captions | 7.2:1 |
| Brass | `#C9A15E` | The one action colour: buttons, focus rings, labels | 8:1 |
| Rune Glow | `#E9C98A` | Links, highlights | 12:1 |
| Star Red | `#C8283A` | Danger and the stars. Fills and large text only | 3.5:1 |
| Star Red Soft | `#FF8C99` | Danger as small text | |
| Wax | `#6E1414` | The seal | |
| Steel Blue | `#3E62B8` | The aurora. Decorative only | 3.3:1 |

- Brass is the only call-to-action colour. One primary (brass) button per view.
- Text on brass is Polar Night (8:1). Text on Star Red is Rime (5:1).
- The aurora gradient (steel → brass → red) is the bend's colours. Use it for horizon lines,
  progress bars and timelines, never for large fills.

## Type

| Role | Font | Settings |
| --- | --- | --- |
| Wordmark | Forum | Uppercase GRAAH, tracking 0.16em (hero) or 0.32em (nav, footer) |
| Headlines, card titles, numerals | Forum | 400 only. Use size and space for hierarchy, not weight |
| Body | Geist | 300–400, 16–18px, line-height 1.6–1.7 |
| Long reading (optional) | Newsreader | `data-body="newsreader"` |
| Labels, dates, places, tabs, chips | Geist Mono | 11–12px, uppercase, tracking 0.12–0.2em, brass or smoke |
| Runes | Noto Sans Runic | Only ᚴᚱᛅᛅᚼ, tracking 1em |

- Never fake-bold Forum. Never set body text in Forum or in Geist Mono.
- Chapter numerals: outlined brass Forum (`.graah-numeral`).
- Use lining numerals (already set in the base styles).

## Shape, line and light

- Controls (buttons, tabs, toggles, chips) are pills. Surfaces (cards, panels, alerts) are nearly
  square (2px). Fields are 4px.
- Every border is a 1px Fjord Line. No heavy shadows; depth comes from the fjord shades.
- Light comes from brass: a soft glow on brass buttons when hovered, on the active tab, on the
  runes and on links when hovered. Nothing else glows.
- Focus is always visible: a 2px brass ring.

## Motion

Slow and quiet. The runes breathe over 5s, a few stars twinkle over 4.5s. No bounces, no
parallax. Everything stops for `prefers-reduced-motion` (the brand classes already do this).

## The start page

The Night Smithy hero (`<NightHero>`, or see `examples/plain.html`): the sky gradient, a
starfield, the aurora arc at the horizon, and centred above it the arms in colour, the GRAAH
wordmark in Forum, and the glowing runes beneath.

## Voice

Plain, warm and specific: dates, places, names. Short sentences. Proud, never pompous.
