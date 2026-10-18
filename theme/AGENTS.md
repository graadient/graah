# Implementing the Graah theme (brief for AI coding agents)

You've been asked to apply the Graah theme to a product. This directory is the whole theme.
Read this file, then `GUIDELINES.md` (the brand rules). `README.md` has the file map.
See it working: https://www.graah.se/theme-lab/ and `examples/plain.html`.

## 1. Get the files

If this directory isn't in the project yet, copy it in. Don't link to it from another repo:

```sh
npx degit graadient/graah/theme graah-theme
```

The theme's source is `theme/` in the graah repo; in your project it lives in `graah-theme/`.
Don't edit files inside `graah-theme/`. Put product-specific CSS in the product's own files.
If the theme itself must change, change `theme/build.py` upstream in the graah repo.

## 2. Wire it up for the stack

Pick exactly one CSS entry:

- **HeroUI v3** (`@heroui/react`): in the global CSS, after HeroUI, unlayered:
  ```css
  @layer theme, base, components, utilities;
  @import "tailwindcss";
  @import "@heroui/styles";
  @import "./graah-theme/heroui.css";
  ```
- **Tailwind v4, no HeroUI:** `@import "tailwindcss";` then `@import "./graah-theme/tailwind.css";`
- **Anything else on the web:** load `graah-theme/graah.css` (link tag or CSS import).
- **Native (iOS, Android, Flutter), Figma, email:** read `tokens/tokens.json` (W3C DTCG format)
  and map it to the platform's theme. Use the SVG or PNG artwork from `assets/`. Get TTF fonts
  from Google Fonts: Forum, Geist, Geist Mono, Newsreader, Noto Sans Runic.

Then:

- Set `<html data-theme="graah">`. Remove any other theme attribute or class (such as `dark`
  or `light`) that the product's old theme set. If the product has a light/dark switch, remove it
  or make it a no-op: Graah is dark only.
- Set `<meta name="theme-color" content="#0B0F1A">`.
- Icons: `assets/favicon.svg` (`<link rel="icon" type="image/svg+xml">`), `assets/icons/favicon-32.png`
  as fallback, `assets/icons/apple-touch-icon.png`, `icon-192.png` and `icon-512.png` in the web manifest.
- Fonts come with `graah.css`. Delete the product's old font links (Google Fonts, Inter, etc.).

## 3. Restyle the product

- Replace the old colours with tokens. Use Tailwind classes (`bg-graah-fjord`, `text-graah-smoke`,
  `border-graah-line`) or CSS variables (`var(--graah-brass)`). With HeroUI, prefer HeroUI's
  semantic classes (`bg-surface`, `text-muted`, `border-border`, `text-accent`): they're mapped.
  Don't add new hex values.
- Use stock components (HeroUI or the product's own) and let the theme style them. Don't
  hand-style buttons, tabs or chips to look Graah: the theme does it.
- Headlines (`h1`–`h3`) are Forum automatically. Labels, dates and places use `.graah-label`.
  Cards and panels use the fjord surface with a 1px line (`.graah-panel` or HeroUI `<Card>`).
- Brand pieces: the logo is `<Arms>` (or `assets/arms/graah-arms.svg`) beside the wordmark
  `<span className="graah-signature">GRAAH</span>`. Use `<Seal>` in the footer. Use `<NightHero>`
  only for a landing or start page.
- Don't put horizontal margins (`m-0`, `mx-*`) on `.graah-wordmark`, `.graah-signature` or
  `.graah-runes`: a negative right margin keeps their wide letter-spacing centred. Use `mt-*`/`mb-*`.
- React components: `import { Arms, Seal, Runes, NightHero } from './graah-theme/react'`.
  If the project's TypeScript config only includes `src`, add `graah-theme/react` to `include`.

## 4. Hard rules

- Never redraw, recolour or simplify the arms. All three stars and the blue-gold-red bend, always.
- Never use the rune ᚼ on its own, or any rune as an icon or ornament. Runes appear only as the
  full name ᚴᚱᛅᛅᚼ.
- Brass is the only action colour. Star Red is for danger only. Steel Blue is decorative only.
- No light mode. No new fonts. No heavy drop shadows. Borders are 1px `--graah-line`.
- Keep focus rings visible and respect `prefers-reduced-motion`.

## 5. Check before you finish

- [ ] `<html data-theme="graah">` everywhere, including error pages and the 404 page.
- [ ] The background is `#0B0F1A`, body text is Geist in `#DCE6EE`, and headlines are Forum.
- [ ] Primary buttons are brass pills with dark text. There's one primary button per view.
- [ ] The arms appear unaltered in the header or nav. The favicon is the arms.
- [ ] No leftover colours, fonts or theme switches from the old design (search the code for hex values and font names).
- [ ] Text contrast is at least 4.5:1. Smoke on fjord is the lowest allowed for small text.
- [ ] Keyboard focus is visible on every control.
- [ ] Checked at 390px and 1440px wide.
- [ ] The product's own lint, typecheck and build pass.
