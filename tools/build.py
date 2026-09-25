"""Generate index.html and projects/*.html from data/projects.json.

Run from the repo root:  python3 tools/build.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'data' / 'projects.json').read_text(encoding='utf-8'))
SITE = json.loads((ROOT / 'data' / 'site.json').read_text(encoding='utf-8'))
PROJECTS = {p['key']: p for p in DATA}

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9"/></svg>')
ARROW_BTN = f'<span class="arrow" aria-hidden="true">{ARROW}{ARROW}</span>'
CLOSE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>')
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800'
         '&family=Inter:wght@600&family=Noto+Sans+TC:wght@400;500;700&display=swap">')

e = html.escape


def head(title, base, desc):
    return f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta name="theme-color" content="#0c0c0c">
<link rel="icon" type="image/png" href="{base}assets/icons/favicon.png">
<link rel="apple-touch-icon" href="{base}assets/icons/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="{base}assets/css/style.css">
<script src="{base}assets/js/main.js" defer></script>
</head>'''


def project_tile(card, delay):
    p = PROJECTS[card['key']]
    half = ' project--half' if card.get('half') else ''
    video = ''
    if card.get('video'):
        video = f'<video data-src="assets/video/{card["video"]}" muted loop playsinline preload="none" aria-hidden="true"></video>'
    return f'''<a class="card project reveal{half}" style="--d:{delay}" href="projects/{p['key']}.html" aria-label="{e(p['title'])}：{e(p['subtitle'])}">
  <div class="project__media">
    <img src="assets/img/{card['image']}" alt="" loading="lazy">
    {video}
  </div>
  <span class="project__num">{card['num']}</span>
  <span class="arrow arrow--corner" aria-hidden="true">{ARROW}{ARROW}</span>
  <div class="pill">
    <div class="pill__text">
      <div class="pill__title">{e(p['title'])}</div>
      <div class="pill__sub">{e(p['subtitle'])}</div>
    </div>
    {ARROW_BTN}
  </div>
</a>'''


def build_index():
    cards = {c['key']: c for c in SITE['cards']}
    t = lambda key, d: project_tile(cards[key], d)
    skills = '\n      '.join(f'<img src="assets/img/{s["file"]}" alt="{e(s["name"])}" title="{e(s["name"])}" loading="lazy">'
                             for s in SITE['skills'])
    ext = 'target="_blank" rel="noopener"'
    socials = '\n    '.join(
        f'<a class="card social" href="{e(s["url"])}" {ext} aria-label="{s["name"]}">'
        f'<img src="assets/icons/{s["icon"]}" alt="" style="width:{s["w"]}px;height:{s["h"]}px"></a>' for s in SITE['socials'])
    hero = SITE['hero']
    body = f'''
<body>
<main class="bento">
  <section class="card hero span-2 reveal" style="--d:0">
    <div class="hero__brand">
      <img class="hero__logo" src="assets/img/logo.webp" alt="Wei logo">
      <span class="label hero__kicker">{e(hero['kicker'])}</span>
    </div>
    <h1><span class="hi">Hi, </span>{e(hero['title'])}</h1>
    <p>{e(hero['intro'])}</p>
  </section>
  {t('dashboard', 1)}
  {t('sport-journey', 2)}
  {t('digital-resume', 3)}
  <section class="card toolkit span-2 reveal" style="--d:4">
    <span class="label">TOOLKIT</span>
    <h2>{e(SITE['toolkit'])}</h2>
    <div class="skills">
      {skills}
    </div>
  </section>
  {t('toeic-fc', 5)}
  <section class="card about reveal" style="--d:6">
    <span class="label">ABOUT</span>
    <p>{'<br>'.join(e(x) for x in SITE['about'].split(chr(10)))}</p>
  </section>
  {t('campaign-page', 7)}
  <section class="card contact reveal" style="--d:8">
    <p>{e(SITE['contact'])}</p>
    <img class="contact__img" src="assets/img/contact.webp" alt="" loading="lazy">
    <button class="btn" type="button" data-copy-email>Email</button>
  </section>
  <nav class="socials reveal" style="--d:9" aria-label="社群連結">
    {socials}
  </nav>
</main>
<section class="m-contact">
  <p>{e(SITE['contact'])}</p>
  <button class="btn" type="button" data-copy-email>Email</button>
</section>
<div class="toast" role="status" aria-live="polite"></div>
</body>
</html>
'''
    page = head(SITE['title'], '', SITE['description']) + body
    (ROOT / 'index.html').write_text(page, encoding='utf-8')


def text_block(b):
    paras = [p for p in b['body'].split('\n\n') if p.strip()]
    out = []
    for para in paras:
        lines = [l for l in para.split('\n') if l.strip()]
        if len(lines) > 1 and lines[0].rstrip().endswith('：'):
            items = ''.join(f'<li>{e(l)}</li>' for l in lines[1:])
            out.append(f'<p>{e(lines[0])}</p><ul>{items}</ul>')
        else:
            out.append(''.join(f'<p>{e(l)}</p>' for l in lines))
    return f'<section class="section scroll-in"><h2>{e(b["title"])}</h2>{"".join(out)}</section>'


def media_block(b, title):
    if b['kind'] == 'img':
        return (f'<figure class="media scroll-in" style="margin:0"><img src="../assets/img/{b["file"]}" '
                f'width="{b["w"]}" height="{b["h"]}" alt="{e(title)} 畫面" loading="lazy"></figure>')
    total_w = sum(i['w'] for i in b['items'])
    style = [f'gap:{b["gap"] / 7.6:.2f}%']
    if b['bg']:
        pad_y = (b['h'] - max(i['h'] for i in b['items'])) / 2
        style += [f'background:{b["bg"]}', f'border-radius:{b["radius"]}px',
                  f'padding:{pad_y / 7.6:.2f}% {max(b["pad"][1], 20) / 7.6:.2f}%']
    if b['justify'] == 'SPACE_BETWEEN':
        style.append('justify-content:space-between')
    items = ''.join(
        f'<div style="flex:{i["w"]} 1 0"><img src="../assets/img/{i["file"]}" width="{i["w"]}" height="{i["h"]}" '
        f'alt="{e(title)} 畫面" loading="lazy"></div>' for i in b['items'])
    return f'<div class="row scroll-in" style="{";".join(style)}">{items}</div>'


def build_project(p):
    tools = SITE['tools'][p['key']]
    tool_imgs = ''.join(f'<img src="../assets/img/{f}" alt="{e(n)}" title="{e(n)}">' for f, n in zip(p['tools'], tools))
    blocks = '\n      '.join(text_block(b) if b['kind'] == 'text' else media_block(b, p['title']) for b in p['blocks'])
    body = f'''
<body>
<main class="detail">
  <article class="sheet">
    <a class="close" href="../index.html" aria-label="關閉，回到首頁">{CLOSE}</a>
    <div class="content">
      <header>
        <h1>{e(p['title'])}</h1>
        <div class="subtitle">{e(p['subtitle'])}</div>
      </header>
      <div class="info">
        <div class="panel panel--meta">
          <img class="meta__icon" src="../assets/img/{p['icon']}" alt="">
          <div class="meta__text">
            <div class="field"><span class="field__label">類型</span><span class="field__value">{e(p['type'])}</span></div>
            <div class="field"><span class="field__label">使用工具</span><div class="tools">{tool_imgs}</div></div>
          </div>
        </div>
        <div class="panel panel--summary">
          <div class="field"><span class="field__label">簡介</span><span class="field__value field__value--lead">{e(p['intro'])}</span></div>
          <div class="field"><span class="field__label">背景</span><span class="field__value field__value--body">{e(p['background'])}</span></div>
          <a class="open-btn" href="{e(p['link'])}" target="_blank" rel="noopener">開啟專案 ↗</a>
        </div>
      </div>
      {blocks}
    </div>
  </article>
  <a class="btn back" href="../index.html">Back</a>
</main>
</body>
</html>
'''
    page = head(f'{p["title"]} · {SITE["title"]}', '../', p['intro']) + body
    (ROOT / 'projects' / f'{p["key"]}.html').write_text(page, encoding='utf-8')


if __name__ == '__main__':
    (ROOT / 'projects').mkdir(exist_ok=True)
    build_index()
    for p in DATA:
        build_project(p)
    print('built index.html +', len(DATA), 'project pages')
