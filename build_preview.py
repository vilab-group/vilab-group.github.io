#!/usr/bin/env python3
"""Render preview.html — a single self-contained file that mimics the built
Jekyll site, using a hash router to switch between pages. Preview only; the
Jekyll templates in the repo are the source of truth."""

import html
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent
D = ROOT / "_data"

load = lambda n: yaml.safe_load((D / n).read_text(encoding="utf-8"))
import base64
_svg = (ROOT / "assets/img/favicon.svg").read_bytes()
ICON = "data:image/svg+xml;base64," + base64.b64encode(_svg).decode()
news, research, pubs = load("news.yml"), load("research.yml"), load("publications.yml")
projects, members, alumni = load("projects.yml"), load("members.yml"), load("alumni.yml")
css = (ROOT / "assets/css/main.css").read_text(encoding="utf-8")
e = html.escape

SITE = dict(
    title="Visual Intelligence", title_long="Visual Intelligence Lab",
    tagline="Medical & Aerial Imaging",
    institution="Dept. of Computer Science and Engineering", university="OO University",
    room="Room 000, Engineering Hall", street="00 Univ-ro, Nam-gu, Seoul, Korea",
    phone="+82-2-000-0000", email="lab@example.ac.kr",
)

NAV = [("research", "Research"), ("projects", "Projects"), ("publications", "Publications"),
       ("team", "Team"), ("news", "News"), ("contact", "Contact")]


def page_head(eyebrow, title, lede=""):
    return f"""<div class="pageHead">
  <div class="hero__graticule" aria-hidden="true"></div>
  <div class="shell">
    <p class="eyebrow eyebrow--onDark">{e(eyebrow)}</p>
    <h1>{e(title)}</h1>
    {f'<p class="lede">{e(lede)}</p>' if lede else ''}
  </div>
</div>"""


def news_card(n, truncate=None):
    tags = "".join(f'<span class="tag">{e(t)}</span>' for t in n.get("tags", []))
    ex = " ".join(n.get("excerpt", "").split())
    if truncate and len(ex) > truncate:
        ex = ex[:truncate].rstrip() + "…"
    d = n["date"]
    return f"""      <article class="newsCard">
        <div class="newsCard__thumb"></div>
        <div class="newsCard__body">
          <div class="tagRow">{tags}</div>
          <h3><a href="#news">{e(n['title'])}</a></h3>
          <p>{e(ex)}</p>
          <time datetime="{d}">{d.strftime('%b %-d, %Y')}</time>
        </div>
      </article>"""


# ---------------------------------------------------------------- home
ongoing = [p for p in projects if p["status"] == "ongoing"]

home = f"""<section class="hero">
  <div class="hero__graticule" aria-hidden="true"></div>
  <div class="hero__scan" aria-hidden="true"></div>
  <span class="hero__tick" style="top:22%;left:14%" aria-hidden="true">+</span>
  <span class="hero__tick" style="top:64%;left:31%" aria-hidden="true">+</span>
  <span class="hero__tick" style="top:38%;left:73%" aria-hidden="true">+</span>
  <div class="shell hero__body">
    <p class="eyebrow eyebrow--onDark">{SITE['institution']} · {SITE['university']}</p>
    <h1>We read images the eye cannot: <em>through the body, and from the sky</em>.</h1>
    <p class="lede">{SITE['title_long']} builds machine learning for medical scans and aerial
      imagery — two domains that share the same hard problems: dense pixels,
      scarce labels, and decisions that have to hold up outside the lab.</p>
    <p class="hero__meta">
      <a href="#publications"><b>{len(pubs)}</b> publications</a>
      <a href="#research"><b>{len(research)}</b> research areas</a>
      <a href="#projects"><b>{len(ongoing)}</b> funded projects</a>
      <a href="#contact"><b>Open</b> for graduate applicants</a>
    </p>
  </div>
</section>

<section class="band band--tint">
  <div class="shell">
    <div class="band__head">
      <div><p class="eyebrow">News</p><h2>Latest from the lab</h2></div>
      <a class="moreLink" href="#news">All news</a>
    </div>
    <div class="newsGrid">
{chr(10).join(news_card(n, 140) for n in news[:4])}
    </div>
  </div>
</section>"""

# ------------------------------------------------------------ research
items = "".join(f"""      <article class="researchItem">
        <span class="researchItem__id">{e(a['id'])}</span>
        <div>
          <h3>{e(a['title'])}</h3>
          <p>{e(' '.join(a['summary'].split()))}</p>
          <div class="chipRow">{''.join(f'<span class="chip">{e(t)}</span>' for t in a['tags'])}</div>
        </div>
      </article>
""" for a in research)

research_pg = page_head("Research", "Research", "Medical scans and aerial imagery look like "
                        "different worlds. The modelling problems underneath them are close "
                        "to identical.") + f"""
<section class="band band--dark">
  <div class="shell"><div class="researchList">
{items}  </div></div>
</section>"""

# ------------------------------------------------------------ projects
def project_row(p):
    partners = f'<p class="project__partners">With {e(", ".join(p["partners"]))}</p>' if p.get("partners") else ""
    summary = f'<p class="project__summary">{e(" ".join(p["summary"].split()))}</p>' if p.get("summary") else ""
    chips = "".join(f'<span class="chip chip--light">{e(t)}</span>' for t in p.get("tags", []))
    role_mod = p["role"].lower().replace("-", "")
    return f"""      <article class="project">
        <div class="project__period">
          <b>{e(p['start'])}</b><span aria-hidden="true">↓</span><b>{e(p['end'])}</b>
        </div>
        <div>
          <h3>{e(p['title'])}</h3>
          <p class="project__agency">{e(p['agency'])} · {e(p.get('program',''))}</p>
          {summary}{partners}
          <div class="project__meta">
            <span class="role role--{role_mod}">{e(p['role'])}</span>
            <span class="status status--{p['status']}">{p['status']}</span>{chips}
          </div>
        </div>
      </article>
"""

groups = ""
for label, key in (("Ongoing", "ongoing"), ("Completed", "completed")):
    rows = sorted([p for p in projects if p["status"] == key], key=lambda x: x["end"], reverse=True)
    if rows:
        groups += (f'    <div class="projectGroup">\n      <h3>{label} · {len(rows)}</h3>\n'
                   + "".join(project_row(p) for p in rows) + "    </div>\n")

projects_pg = page_head("Research projects", "Projects",
                        "Funded research programmes the lab currently runs or has "
                        "completed.") + f"""
<section class="band">
  <div class="shell">
{groups}  </div>
</section>"""

# -------------------------------------------------------- publications
by_year = {}
for p in pubs:
    by_year.setdefault(p["year"], []).append(p)

blocks = ""
for yr in sorted(by_year, reverse=True):
    blocks += f'    <h2 class="pubYear">{yr}</h2>\n'
    for p in sorted(by_year[yr], key=lambda x: x["date"], reverse=True):
        links = "".join(f'<a href="{l["url"]}">{e(l["label"])}</a>' for l in p["links"])
        met = f'\n        <p class="pub__metrics">{e(p["metrics"])}</p>' if p.get("metrics") else ""
        note = f'\n        <p class="pub__note">{e(p["note"])}</p>' if p.get("note") else ""
        blocks += f"""    <article class="pub">
      <div class="pub__thumb"></div>
      <div>
        <h3>{e(p['title'])}</h3>
        <p class="pub__authors">{p['authors']}</p>
        <p class="pub__venue">{e(p['venue'])}</p>{met}{note}
        <div class="pub__links">{links}</div>
      </div>
    </article>
"""

pubs_pg = page_head("Publications", "Publications",
                    "Peer-reviewed work, newest first. Lab members are in "
                    "bold.") + f"""
<section class="band">
  <div class="shell">
{blocks}  </div>
</section>"""

# ---------------------------------------------------------------- team
team_blocks = ""
for grp in members:
    cards = "".join(f"""        <div class="person">
          <div class="person__photo"></div>
          <p class="person__role">{e(p['role'])}</p>
          <p class="person__name">{e(p['name'])}</p>
          <p class="person__kr">{e(p['kr'])}</p>
          <p class="person__topic">{e(p['topic'])}</p>
        </div>
""" for p in grp["people"])
    team_blocks += (f'    <div class="teamGroup">\n      <h3>{e(grp["group"])}</h3>\n'
                    f'      <div class="peopleGrid">\n{cards}      </div>\n    </div>\n')

alum = "".join(f'        <li><strong>{e(a["name"])}</strong> ({e(a["kr"])})'
               f'<span>{e(a["degree"])}{" → " + e(a["career"]) if a.get("career") else ""}</span></li>\n'
               for a in alumni)
team_blocks += f'    <div class="teamGroup">\n      <h3>Alumni</h3>\n      <ul class="alumniList">\n{alum}      </ul>\n    </div>\n'

team_pg = page_head("Our team", "Team", "The people doing the work.") + f"""
<section class="band">
  <div class="shell">
{team_blocks}  </div>
</section>"""

# ---------------------------------------------------------------- news
news_pg = page_head("News", "News") + f"""
<section class="band band--tint">
  <div class="shell"><div class="newsGrid">
{chr(10).join(news_card(n) for n in news)}
  </div></div>
</section>"""

# ------------------------------------------------------------- contact
contact_pg = page_head("Contact", "Contact", "Where to find us, and how to join.") + f"""
<section class="band band--tint">
  <div class="shell">
    <div class="contactGrid">
      <div class="mapStub">GOOGLE MAPS EMBED</div>
      <dl class="addr addr--light">
        <dt>Address</dt>
        <dd>{SITE['title_long']}, {SITE['room']}<br>{SITE['institution']}, {SITE['university']}<br>{SITE['street']}</dd>
        <dt>Phone</dt><dd>{SITE['phone']}</dd>
        <dt>Email</dt><dd><a href="mailto:{SITE['email']}">{SITE['email']}</a></dd>
        <dt>Join us</dt>
        <dd>We are looking for graduate students and interns interested in
            medical or aerial image understanding. Email a CV and a short note
            about what you want to build.</dd>
      </dl>
    </div>
  </div>
</section>"""

PAGES = [("home", home), ("research", research_pg), ("projects", projects_pg),
         ("publications", pubs_pg), ("team", team_pg), ("news", news_pg),
         ("contact", contact_pg)]

nav_html = "".join(f'      <a href="#{slug}" data-nav="{slug}">{label}</a>\n' for slug, label in NAV)
pages_html = "".join(f'<div data-page="{slug}">\n{body}\n</div>\n' for slug, body in PAGES)

doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{SITE['title']}</title>
<link rel="icon" href="{ICON}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>
{css}

/* preview-only helpers */
[data-page][hidden] {{ display: none; }}
.mapStub {{
  height: 340px; border-radius: 4px; border: 1px dashed var(--line);
  background: var(--paper); display: flex; align-items: center; justify-content: center;
  font-family: var(--mono); font-size: .72rem; letter-spacing: .14em; color: var(--slate);
}}
</style>
</head>
<body>
<a class="skip" href="#content">Skip to content</a>

<header class="masthead">
  <div class="shell masthead__row">
    <a class="brand" href="#home">
      <img class="brand__icon" src="{ICON}" alt="" width="26" height="26">
      <span class="brand__mark">{SITE['title']}</span>
      <span class="brand__sub">{SITE['tagline']}</span>
    </a>
    <button class="navToggle" aria-expanded="false" aria-controls="primaryNav">Menu</button>
    <nav class="nav" id="primaryNav" aria-label="Primary">
{nav_html}    </nav>
  </div>
</header>

<main id="content">
{pages_html}</main>

<footer class="colophon">
  <div class="shell">
    <span>© 2026 {SITE['title_long']}, {SITE['university']} · {SITE['room']} ·
      <a href="mailto:{SITE['email']}">{SITE['email']}</a></span>
    <span><a href="#home">GitHub</a> · <a href="#home">Google Scholar</a></span>
  </div>
</footer>

<script>
// Preview router. The real site is a normal multi-page Jekyll build; this
// only exists so the whole thing can be reviewed from one file.
(function () {{
  var pages = document.querySelectorAll('[data-page]');
  var links = document.querySelectorAll('[data-nav]');
  function route() {{
    var want = (location.hash || '#home').slice(1);
    var known = false;
    pages.forEach(function (p) {{ if (p.dataset.page === want) known = true; }});
    if (!known) want = 'home';
    pages.forEach(function (p) {{ p.hidden = p.dataset.page !== want; }});
    links.forEach(function (a) {{
      if (a.dataset.nav === want) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    }});
    window.scrollTo(0, 0);
  }}
  window.addEventListener('hashchange', route);
  route();

  var btn = document.querySelector('.navToggle');
  var nav = document.getElementById('primaryNav');
  var mq = window.matchMedia('(max-width: 860px)');
  function sync() {{
    if (mq.matches) {{ nav.hidden = true; btn.setAttribute('aria-expanded', 'false'); }}
    else {{ nav.hidden = false; }}
  }}
  btn.addEventListener('click', function () {{
    var open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    nav.hidden = open;
  }});
  nav.addEventListener('click', function (ev) {{ if (ev.target.tagName === 'A' && mq.matches) sync(); }});
  mq.addEventListener('change', sync);
  sync();
}})();
</script>
</body>
</html>
"""

(ROOT / "preview.html").write_text(doc, encoding="utf-8")
print(f"preview.html rebuilt — {len(PAGES)} pages, {len(pubs)} publications, "
      f"{len(projects)} projects, {len(doc):,} bytes")
