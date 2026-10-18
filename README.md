# GRAAH

Source for `graah.se`, built with Vite, React, Tailwind CSS, and Hero UI.

## Theme

`graah-theme/` is the Graah visual identity as a reusable kit: tokens, CSS,
a HeroUI v3 theme, React brand components, the arms, the seal and fonts.
Other products can copy it in with `npx degit graadient/graah/graah-theme`.
See `graah-theme/README.md`.

## Development

```sh
npm install
npm run dev
```

## Checks

```sh
npm run verify
```

## Deployment

GitHub Pages deploys `dist/` from the `main` branch through
`.github/workflows/pages.yml`. The custom domain is set by `public/CNAME`.
