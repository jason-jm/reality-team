# The Reality Team · Reality series website

Website for the eight Reality apps for PICO Space Pro: Reality Office, Reality Image Studio,
Reality Video Editor, Reality CAD, Reality NAS Player, Reality File Transfer, Reality Unzip and
Reality Rocket.

Live site: https://jason-jm.github.io/reality-team/ (Chinese) and https://jason-jm.github.io/reality-team/en/ (English)

## Editing

- Text for both languages: `src/content.py`
- Design and behaviour: `src/site.css`, `src/site.js`
- Screenshots and icons: `assets/shots/*.webp` (1800 px and `-sm` 900 px), `assets/icons/<app>-{bg,fg2,fg3}.webp` (the three PICO icon layers)

Rebuild the pages from the repository root:

```sh
python3 src/build.py .
```

The build needs Python 3 and ImageMagick (`magick`, used to read screenshot sizes). The site is plain HTML, CSS and JavaScript with no external fonts or scripts.
