#!/usr/bin/env python3
"""Builds the Reality series site: index.html (Chinese) and en/index.html (English).

    build.py <site dir>     (the dir that holds assets/)
"""
import html, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import SITE, APPS, HERO_TOP, HERO_BOTTOM

ROOT = sys.argv[1]
LANGS = {"zh": 0, "en": 1}
LOCALIZED = {"nas-wall", "nas-detail", "nas-subtitles", "office-slides", "office-pages", "office-sheets", "office-home"}

_dims = {}
def dims(key):
    if key not in _dims:
        out = subprocess.run(["magick", "identify", "-format", "%w %h", f"{ROOT}/assets/shots/{key}.webp"],
                             capture_output=True, text=True, check=True).stdout.split()
        _dims[key] = (int(out[0]), int(out[1]))
    return _dims[key]

HERE = os.path.dirname(os.path.abspath(__file__))
# cache-busting tag for the stylesheet and script: first 8 hex digits of their SHA-256
import hashlib
VER = {f: hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest()[:8] for f in ("site.css", "site.js")}

def e(s): return html.escape(s, quote=True)

class Page:
    def __init__(self, lang):
        self.lang = lang; self.i = LANGS[lang]
        self.pre = "" if lang == "zh" else "../"
    def t(self, pair): return pair[self.i]
    def s(self, key): return SITE[key][self.i]
    def shot(self, key):
        return f"{key}-{self.lang}" if key in LOCALIZED else key
    def img(self, key, alt, cls="", sizes="(min-width: 1208px) 1160px, calc(100vw - 48px)", lazy=True, eager_hi=False):
        # <key>-sm.webp 800 px, <key>-md.webp 1400 px, <key>.webp the full crop (1600-2880 px)
        k = self.shot(key); w, h = dims(k)
        src = f"{self.pre}assets/shots/{k}"
        load = 'loading="lazy" decoding="async"' if lazy else ('fetchpriority="high"' if eager_hi else 'decoding="async"')
        sets = [f"{src}-sm.webp 800w"] + ([f"{src}-md.webp 1400w"] if w > 1400 else []) + [f"{src}.webp {w}w"]
        return (f'<img class="{cls}" src="{src}-md.webp" srcset="{", ".join(sets)}" sizes="{sizes}" '
                f'data-full="{src}.webp" width="{w}" height="{h}" alt="{e(alt)}" {load}>')
    def icon(self, app, size_cls="", label=True):
        k = app["key"]; p = f"{self.pre}assets/icons/{k}"
        alt = f' role="img" aria-label="{e(app["name"])}"' if label else ' aria-hidden="true"'
        return (f'<span class="icon {size_cls}"{alt}><img src="{p}-bg.webp" alt="" class="l0">'
                f'<img src="{p}-fg2.webp" alt="" class="l1"><img src="{p}-fg3.webp" alt="" class="l2"></span>')

def link_label(page, kind):
    return page.s({"apk": "apk", "source": "source", "site": "site", "releases": "releases"}[kind])

def render(lang):
    P = Page(lang); t = P.t; s = P.s
    shot_alt = {}
    for a in APPS:
        for key, alt in a["shots"]:
            shot_alt[key] = f'{a["name"]} · {t(alt)}'
    other = "en/" if lang == "zh" else "../"
    out = []
    w = out.append
    w(f'''<!doctype html>
<html lang="{"zh-CN" if lang == "zh" else "en"}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(s("title"))}</title>
<meta name="description" content="{e(s("description"))}">
<meta property="og:title" content="{e(s("title"))}">
<meta property="og:description" content="{e(s("description"))}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://jason-jm.github.io/reality-team/assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#07090D">
<link rel="icon" href="{P.pre}assets/favicon.png">
<link rel="alternate" hreflang="zh-CN" href="https://jason-jm.github.io/reality-team/">
<link rel="alternate" hreflang="en" href="https://jason-jm.github.io/reality-team/en/">
<link rel="stylesheet" href="{P.pre}assets/site.css?v={VER["site.css"]}">
</head>
<body>
<a class="skip" href="#series">{e(s("skip"))}</a>
<header class="nav" id="nav">
  <div class="nav-in">
    <a class="brand" href="#top" aria-label="Reality">
      <span class="brand-mark" aria-hidden="true">{"".join(f'<i style="--c:{a["color"]}"></i>' for a in APPS)}</span>
      <span class="brand-name">Reality</span><span class="brand-by">The Reality Team</span>
    </a>
    <nav class="mini" aria-label="{e(s("nav_apps"))}">
      {"".join(f'<a href="#{a["key"]}" data-app="{a["key"]}" title="{e(a["name"])}">{P.icon(a, "xs", label=False)}<span>{e(a["name"].replace("Reality ", ""))}</span></a>' for a in APPS)}
    </nav>
    <div class="nav-links">
      <a href="#series">{e(s("nav_apps"))}</a>
      <a href="#download">{e(s("nav_download"))}</a>
      <a class="lang" href="{other}" hreflang="{"en" if lang == "zh" else "zh-CN"}">{e(s("lang_other"))}</a>
    </div>
  </div>
</header>

<main id="top">
<section class="hero">
  <div class="glow" aria-hidden="true">{"".join(f'<i style="--c:{a["color"]}"></i>' for a in APPS)}</div>
  <div class="hero-in">
    <p class="eyebrow">{e(s("eyebrow"))}</p>
    <h1>{s("h1")}</h1>
    <p class="hero-lede">{e(s("lede"))}</p>
    <div class="hero-cta">
      <a class="btn btn-light" href="#series">{e(s("cta_all"))}</a>
      <a class="btn btn-ghost" href="#download">{e(s("cta_download"))}</a>
    </div>
  </div>
  <ul class="dock" aria-label="{e(s("nav_apps"))}">
''')
    for a in APPS:
        w(f'    <li><a href="#{a["key"]}" style="--c:{a["color"]}">{P.icon(a, "lg", label=False)}'
          f'<span class="dock-name">{e(a["name"].replace("Reality ", ""))}</span>'
          f'<span class="dock-cat">{e(t(a["category"]))}</span></a></li>\n')
    w('  </ul>\n  <div class="strips" aria-hidden="true">\n')
    for row, keys in (("a", HERO_TOP), ("b", HERO_BOTTOM)):
        cards = "".join(f'<figure class="card">{P.img(k, "", sizes="(max-width: 680px) 300px, 440px", lazy=(row == "b"))}</figure>' for k in keys)
        w(f'    <div class="strip strip-{row}"><div class="track">{cards}{cards}</div></div>\n')
    w('  </div>\n  <ul class="facts">\n')
    for pair in SITE["facts"]:
        big, small = pair[P.i]
        w(f'    <li><b>{e(big)}</b><span>{e(small)}</span></li>\n')
    w('  </ul>\n</section>\n')

    # ---- overview
    w(f'''
<section class="overview" id="series">
  <div class="wrap">
    <p class="kicker">{e(s("overview_kicker"))}</p>
    <h2 class="display">{e(s("overview_h2"))}</h2>
    <p class="section-lede">{e(s("overview_p"))}</p>
    <div class="cards">
''')
    for a in APPS:
        w(f'''      <a class="app-card" href="#{a["key"]}" style="--c:{a["color"]};--ink:{a["ink"]};--tint:{a["tint"]}">
        {P.icon(a, "md", label=False)}
        <span class="app-card-cat">{e(t(a["category"]))}</span>
        <h3>{e(a["name"])}</h3>
        <p>{e(t(a["oneliner"]))}</p>
        <span class="app-card-ver">{e(t(a["badge"]))}</span>
      </a>
''')
    w('    </div>\n    <ul class="common">\n')
    for pair in SITE["common"]:
        h, p = pair[P.i]
        w(f'      <li><h3>{e(h)}</h3><p>{e(p)}</p></li>\n')
    w('    </ul>\n  </div>\n</section>\n')

    # ---- apps by chapter
    order = ["create", "watch", "tools"]
    num = 0
    for ci, ch in enumerate(order):
        title, sub = SITE["chapters"][ch][P.i]
        names = " · ".join(a["name"].replace("Reality ", "") for a in APPS if a["chapter"] == ch)
        w(f'''
<section class="chapter" aria-labelledby="ch-{ch}">
  <div class="wrap chapter-in">
    <span class="chapter-no">0{ci + 1}</span>
    <div><h2 id="ch-{ch}">{e(title)}</h2><p>{e(sub)}</p></div>
    <span class="chapter-apps">{e(names)}</span>
  </div>
</section>
''')
        for a in [x for x in APPS if x["chapter"] == ch]:
            num += 1
            first, rest = a["shots"][0], a["shots"][1:]
            links = "".join(
                f'<a class="btn {"btn-accent" if j == 0 else "btn-line"}" href="{e(u)}" rel="noopener">{e(link_label(P, kind))}</a>'
                for j, (kind, u) in enumerate(a["links"]))
            badge = e(t(a["badge"]))
            w(f'''
<section class="app{" dark" if a.get("theme") == "dark" else ""}" id="{a["key"]}" data-app="{a["key"]}" style="--c:{a["color"]};--ink:{a["ink"]};--tint:{a["tint"]}">
  <div class="wrap">
    <div class="app-head">
      {P.icon(a, "xl")}
      <div class="app-title">
        <p class="app-meta"><span>{num:02d} / 08</span><span>{e(t(a["category"]))}</span><span class="badge">{badge}</span></p>
        <h2>{e(a["name"])}</h2>
        <p class="app-oneliner">{e(t(a["oneliner"]))}</p>
      </div>
      <div class="app-intro">
        <p>{e(t(a["lede"]))}</p>
        {f'<div class="app-links">{links}</div>' if links else ''}
      </div>
    </div>
    <figure class="shot-main" data-gallery="{a["key"]}">
      <button class="zoom" type="button" data-index="0">{P.img(first[0], shot_alt[first[0]])}</button>
      <figcaption>{e(t(first[1]))}</figcaption>
    </figure>
    <h3 class="sub">{e(s("features"))}</h3>
    <ul class="features">
''')
            for f in a["features"]:
                h, p = f[P.i]
                w(f'      <li><h4>{e(h)}</h4><p>{e(p)}</p></li>\n')
            w('    </ul>\n')
            if rest:
                w(f'    <h3 class="sub">{e(s("gallery"))}</h3>\n    <div class="gallery" data-gallery="{a["key"]}">\n')
                for j, (key, alt) in enumerate(rest, start=1):
                    w(f'      <figure><button class="zoom" type="button" data-index="{j}">{P.img(key, shot_alt[key], sizes="(min-width: 1208px) 380px, (min-width: 680px) 32vw, 48vw")}</button><figcaption>{e(t(alt))}</figcaption></figure>\n')
                w('    </div>\n')
            w(f'    <ul class="chips" aria-label="{e(s("specs"))}">' + "".join(f'<li>{e(t(c))}</li>' for c in a["specs"]) + '</ul>\n')
            w('  </div>\n</section>\n')

    # ---- download
    w(f'''
<section class="download" id="download">
  <div class="wrap">
    <p class="kicker">{e(s("download_kicker"))}</p>
    <h2 class="display">{e(s("download_h2"))}</h2>
    <p class="section-lede">{e(s("download_p"))}</p>
    <div class="dl-table" role="table">
      <div class="dl-row dl-headrow" role="row"><span role="columnheader">{e(s("col_app"))}</span><span role="columnheader">{e(s("col_version"))}</span><span role="columnheader">{e(s("col_platform"))}</span><span role="columnheader">{e(s("col_get"))}</span></div>
''')
    for a in APPS:
        links = " ".join(f'<a href="{e(u)}" rel="noopener">{e(link_label(P, kind))}</a>' for kind, u in a["links"])
        w(f'''      <div class="dl-row" role="row" style="--c:{a["color"]}"><span role="cell" class="dl-app">{P.icon(a, "sm", label=False)}<a href="#{a["key"]}">{e(a["name"])}</a></span><span role="cell">{e(t(a["version"]))}</span><span role="cell">{e(t(a["platform"]))}</span><span role="cell" class="dl-get">{links or '<em>' + e(s("not_yet")) + '</em>'}</span></div>
''')
    w(f'''    </div>
  </div>
</section>
</main>

<footer class="foot">
  <div class="wrap foot-in">
    <div class="foot-brand"><span class="brand-mark" aria-hidden="true">{"".join(f'<i style="--c:{a["color"]}"></i>' for a in APPS)}</span><b>The Reality Team</b></div>
    <ul class="foot-apps">{"".join(f'<li><a href="#{a["key"]}">{e(a["name"])}</a></li>' for a in APPS)}</ul>
    <p>{e(s("footer_note"))}</p>
    <p>© 2026 The Reality Team · <a href="https://github.com/jason-jm">GitHub</a> · <a href="{other}">{e(s("lang_other"))}</a></p>
  </div>
</footer>

<dialog class="lightbox" id="lightbox" aria-label="Screenshots">
  <button class="lb-close" type="button" aria-label="{e(s("close"))}">×</button>
  <button class="lb-prev" type="button" aria-label="{e(s("prev"))}">‹</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-next" type="button" aria-label="{e(s("next"))}">›</button>
</dialog>
<script src="{P.pre}assets/site.js?v={VER["site.js"]}" defer></script>
</body>
</html>
''')
    return "".join(out)

os.makedirs(f"{ROOT}/en", exist_ok=True)
open(f"{ROOT}/index.html", "w").write(render("zh"))
open(f"{ROOT}/en/index.html", "w").write(render("en"))
for f in ("site.css", "site.js"):   # keep the served copies in step with the sources beside this script
    shutil.copyfile(os.path.join(HERE, f), f"{ROOT}/assets/{f}")
print("built", ROOT)
