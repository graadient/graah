# Graah theme

The visual identity of the Graah family ("Night Smithy"), packaged so any product can use it.
Polar-night ground, glacier text, brass for action, the original arms, the brass seal,
Forum capitals and glowing runes.

- **Live reference:** https://www.graah.se/theme-lab/ (every component, real content, mobile and desktop)
- **Plain HTML example:** [`examples/plain.html`](examples/plain.html) (open it straight from disk)
- **Rules:** [`GUIDELINES.md`](GUIDELINES.md). **For AI coding agents:** [`AGENTS.md`](AGENTS.md)

Version 1.0.1. Dark only, by design.

## Get it

The theme lives at `theme/` in the [graah repo](https://github.com/graadient/graah/tree/main/theme).
Copy it into your project as `graah-theme/` (recommended; then it is yours to pin and update).
The examples below assume that folder name:

```sh
npx degit graadient/graah/theme graah-theme
```

Or link straight from the CDN, pinned to a release tag (no copy):

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/graadient/graah@theme-v1.0.1/theme/graah.css" />
```

## Use it

Put `data-theme="graah"` on `<html>`, then pick the one entry file that matches your stack.

| Stack | Import | You get |
| --- | --- | --- |
| Any web page | `graah.css` | Fonts, tokens (`--graah-*`), base styles, brand classes |
| Tailwind CSS v4 | `tailwind.css` | All of the above, plus `bg-graah-night`, `text-graah-brass`, `font-graah-display`, `rounded-graah-control`, ... |
| HeroUI v3 | `heroui.css` | All of the above, plus every HeroUI component restyled |
| React | `react/` | `<Arms>`, `<Seal>`, `<Runes>`, `<NightHero>`, `<Starfield>`, `<AuroraArc>` |
| iOS, Android, Figma, email, print | `tokens/tokens.json` + `assets/` | Tokens in W3C design-token format, SVG and PNG artwork |

**Plain HTML / any framework**

```html
<html lang="en" data-theme="graah">
  <link rel="stylesheet" href="graah-theme/graah.css" />
  <h1 class="graah-wordmark">GRAAH</h1>
  <span class="graah-runes" role="img" aria-label="Graah, in runes">ᚴᚱᛅᛅᚼ</span>
```

**Tailwind CSS v4**

```css
@import "tailwindcss";
@import "./graah-theme/tailwind.css";
```

**HeroUI v3** (import unlayered and after HeroUI, exactly like this)

```css
@layer theme, base, components, utilities;
@import "tailwindcss";
@import "@heroui/styles";
@import "./graah-theme/heroui.css";
```

Then use stock HeroUI components. `<Button>` is brass, `<Tabs>` get a glowing brass indicator,
`<Card.Title>` is set in Forum, `<Chip>` in tracked Geist Mono, and so on.

**React brand pieces** (React 18+, no other dependencies; need one of the CSS entries above)

```tsx
import { Arms, NightHero, Runes, Seal } from './graah-theme/react'

<NightHero top={<nav>…</nav>}>
    <Arms className="mb-6 w-[clamp(84px,12vw,150px)]" />
    <h1 className="graah-wordmark text-[clamp(56px,13vw,176px)]">GRAAH</h1>
    <Runes className="mt-3 text-[clamp(16px,2vw,26px)]" />
</NightHero>

<Seal size={96} />
```

**Body font.** Geist by default. For long reading, switch to Newsreader:
`<html data-theme="graah" data-body="newsreader">`.

## What's inside

```
graah.css            entry: plain CSS (imports fonts, tokens, base, brand)
tailwind.css         entry: Tailwind v4 (graah.css + Tailwind utilities)       GENERATED
heroui.css           entry: HeroUI v3 (tailwind.css + HeroUI theme)
tokens/tokens.json   all tokens, W3C DTCG format                               GENERATED
tokens/tokens.css    all tokens as --graah-* custom properties                 GENERATED
css/base.css         element styles under [data-theme="graah"]
css/brand.css        .graah-wordmark, .graah-runes, .graah-label, .graah-panel, ...
fonts/               Forum, Geist, Geist Mono, Newsreader, Noto Sans Runic (woff2, OFL)
assets/arms/         the arms: shaded, flat, mono (currentColor), brass, original PNG
assets/seal/         the seal: wax, and one-colour (currentColor); runes are outlines
assets/icons/        favicons, apple-touch-icon, 192/512 app icons
assets/favicon.svg   flat arms
assets/aurora-arc.svg  the hero's horizon arc
react/               React components + generated geometry
examples/plain.html  the whole look with no build step
build.py             regenerates the GENERATED files and the SVG artwork
tools/arms.py        the traced geometry of the arms
```

## Tokens at a glance

| Token | Hex | Use |
| --- | --- | --- |
| `--graah-night` | `#0B0F1A` | Page ground |
| `--graah-fjord` | `#111829` | Cards, panels |
| `--graah-line` | `#26304A` | Every border (1px) |
| `--graah-rime` | `#F2F6F9` | Headlines, wordmark |
| `--graah-glacier` | `#DCE6EE` | Body text |
| `--graah-smoke` | `#8EA0B8` | Muted text |
| `--graah-brass` | `#C9A15E` | Action, focus, labels |
| `--graah-glow` | `#E9C98A` | Links, glowing runes |
| `--graah-red` | `#C8283A` | Stars, danger |
| `--graah-wax` | `#6E1414` | The seal |
| `--graah-steel` | `#3E62B8` | The aurora |

Full list with roles: [`tokens/tokens.css`](tokens/tokens.css).

## Changing the theme

Edit the values in `build.py` (colours, fonts, radii, effects), then:

```sh
python3 theme/build.py                # pip install fonttools first to re-outline the seal's runes
npx biome format --write theme        # in the graah repo
```

`heroui.css`, `graah.css` and `css/*.css` are hand-written and read the tokens, so they follow.
The PNG icons are rendered from the SVGs and are not regenerated by `build.py`.
Tag a new release (`theme-vX.Y.Z`) so products can pin it.

## Licences

Fonts: SIL Open Font License 1.1, see [`fonts/OFL.txt`](fonts/OFL.txt).
The arms and seal belong to the Graah family; use them only in Graah family products.
