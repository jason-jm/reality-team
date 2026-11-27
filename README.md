# The Reality Team · Reality series website

Website for the eight Reality apps for PICO Space Pro: Reality Office, Reality Image Studio,
Reality Video Editor, Reality CAD, Reality NAS Player, Reality File Transfer, Reality Unzip and
Reality Rocket.

Live site: https://jason-jm.github.io/reality-team/ (Chinese) and https://jason-jm.github.io/reality-team/en/ (English)

## Editing

- Text for both languages: `src/content.py`
- Design and behaviour: `src/site.css`, `src/site.js`
- Screenshots: `assets/shots/<name>.webp` is the full crop (1840 to 2880 px wide), `<name>-md.webp` 1400 px and `<name>-sm.webp` 800 px; pages let the browser choose by screen density, and the lightbox opens the full crop. Names ending in `-zh` or `-en` are per language. Most captures are 3200 × 3200 spatial views from the PICO 6.2 emulator (`pico-cli capture screenshot --spatial --size 3200x3200`), cropped around the window without scaling and lightly sharpened.
- Icons: `assets/icons/<app>-{bg,fg2,fg3}.webp` (the three PICO icon layers)

Rebuild the pages from the repository root:

```sh
python3 src/build.py .
```

The build needs Python 3 and ImageMagick (`magick`, used to read screenshot sizes). The site is plain HTML, CSS and JavaScript with no external fonts or scripts.
