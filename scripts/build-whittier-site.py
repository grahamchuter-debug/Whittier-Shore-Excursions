#!/usr/bin/env python3
"""Generate Whittier Shore Excursions static site with clean URLs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://whittiershoreexcursions.com"
SITE = "Whittier Shore Excursions"
DATE = "2026-06-24"
ENQUIRY_EMAIL = "enquiries@whittiershoreexcursions.com"
FONTS = (
    "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;600;700"
    "&family=DM+Sans:wght@400;500;600;700&display=swap"
)
HERO_GRADIENT = (
    "linear-gradient(135deg, rgba(12, 74, 110, 0.78) 0%, "
    "rgba(8, 145, 178, 0.62) 52%, rgba(15, 118, 110, 0.58) 100%)"
)
ACCENT = "text-teal-400"

IMG = {
    "home": ("images/hero-whittier.png", "Prince William Sound fjords and glaciers near Whittier Alaska"),
    "best": ("images/best-whittier-excursions.png", "Best Whittier shore excursions for Alaska cruise passengers"),
    "port": ("images/whittier-port.png", "Cruise ship at Whittier Alaska port on Passage Canal"),
    "wildlife": ("images/wildlife.png", "Marine wildlife in Prince William Sound near Whittier Alaska"),
    "pws": ("images/prince-william-sound.png", "Prince William Sound glacier and fjord scenery from Whittier"),
    "pws_wildlife": ("images/pws-wildlife.png", "Whale and wildlife viewing on a Prince William Sound cruise from Whittier"),
    "pws_glacier": ("images/pws-glacier.png", "Tidewater glacier calving in Prince William Sound from Whittier"),
    "spencer": ("images/spencer-glacier.png", "Spencer Glacier and river float trip near Whittier Alaska"),
    "blackstone": ("images/blackstone-bay.png", "Blackstone Bay glacier cruise from Whittier Alaska"),
    "scenic": ("images/whittier-scenic.png", "Scenic Whittier and Passage Canal viewpoints Alaska"),
    "transfer": ("images/anchorage-transfer.png", "Scenic transfer from Whittier toward Anchorage Alaska"),
    "train": ("images/glacier-train.png", "Alaska Railroad Glacier Discovery train near Whittier"),
    "portage": ("images/portage-glacier.png", "Portage Glacier and lake near Whittier Alaska"),
    "tunnel": ("images/tunnel.png", "Anton Anderson Memorial Tunnel entrance near Whittier Alaska"),
    "vs_seward": ("images/vs-seward.png", "Whittier versus Seward Alaska cruise port comparison"),
    "portage_pass": ("images/portage-pass.png", "Portage Pass Trail alpine views above Whittier"),
    "begich": ("images/begich-towers.png", "Begich Towers and Whittier Alaska waterfront history"),
    "independent": ("images/independent.png", "Independent travellers exploring Whittier Alaska and Prince William Sound"),
    "intro": ("images/intro.png", "Prince William Sound cruise departing Whittier Alaska"),
    "faq": ("images/faq.png", "Cruise passengers planning Whittier shore excursions"),
    "planner": ("images/planner.png", "Whittier Alaska cruise day planner for shore excursions"),
    "enquire": ("images/enquire.png", "Enquire about Whittier shore excursions for cruise passengers"),
    "schedule": ("images/schedule.png", "Whittier Alaska cruise ship schedule and port calls"),
    "best_time": ("images/best-time.png", "Best time to visit Whittier Alaska for Prince William Sound cruises"),
    "things": ("images/things.png", "Things to do in Whittier from a cruise ship"),
    "cruise_snapshot": ("images/cruise-snapshot.png", "Cruise ship docked at Whittier Alaska cruise port"),
}


def meta_desc(text: str) -> str:
    first = text.split(". ")[0].rstrip(".")
    return first + "."


def u(slug: str = "") -> str:
    return "/" if not slug else f"/{slug}"


def write(path: str, content: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"  wrote {path}")


def write_page(slug: str, html: str) -> None:
    path = "index.html" if not slug else f"{slug}/index.html"
    write(path, html)


def breadcrumb_schema(slug: str, name: str) -> dict:
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"}]
    if slug:
        items.append({"@type": "ListItem", "position": 2, "name": name, "item": f"{DOMAIN}/{slug}"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def faq_schema(qa: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa
        ],
    }


def website_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE,
        "url": f"{DOMAIN}/",
        "publisher": {
            "@type": "Organization",
            "name": SITE,
            "url": f"{DOMAIN}/",
            "email": ENQUIRY_EMAIL,
        },
    }


def inject_schemas(html: str, schemas: list[dict]) -> str:
    block = "".join(
        f'  <script type="application/ld+json">\n{json.dumps(s, indent=2)}\n  </script>\n'
        for s in schemas
    )
    return html.replace('  <meta name="twitter:card"', block + '  <meta name="twitter:card"', 1)


def page_shell(
    *,
    title: str,
    description: str,
    keywords: str,
    slug: str,
    data_page: str,
    hero: str,
    content: str,
    preload: str,
    trust: bool = True,
) -> str:
    canon = f"{DOMAIN}/" if not slug else f"{DOMAIN}/{slug}"
    trust_attr = '\n  data-trust-strip="/partials/trust-strip.html"' if trust else ""
    content_file = content if content.startswith("/content/") else f"/content/{content}"
    hero_path = hero if hero.startswith("/") else f"/{hero}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canon}" />
  <link rel="preload" as="image" href="/{preload}" fetchpriority="high" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{DOMAIN}/{preload}" />
  <meta property="og:site_name" content="{SITE}" />
  <meta name="twitter:card" content="summary_large_image" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="/js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="{FONTS}" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
<body class="bg-white text-gray-800 antialiased" data-page="{data_page}" data-hero="{hero_path}" data-content="{content_file}"{trust_attr}>
  <div id="site-nav"></div>
  <div id="page-hero"></div>
  <div id="page-trust-strip"></div>
  <main id="page-content"></main>
  <div id="site-footer"></div>
  <script src="/js/site.js"></script>
</body>
</html>
"""


def _wave() -> str:
    return '<div class="absolute bottom-0 left-0 right-0"><svg viewBox="0 0 1440 48" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" class="site-hero__wave" aria-hidden="true"><path d="M0 24 C360 48 1080 0 1440 24 L1440 48 L0 48 Z" fill="white"/></svg></div>'


def hero(
    eyebrow: str,
    title: str,
    lead: str,
    image_key: str,
    breadcrumb: str = "",
    cta: tuple[str, str] | None = None,
    tags: list[str] | None = None,
) -> str:
    image, aria = IMG[image_key]
    bc = ""
    if breadcrumb:
        bc = f"""<nav class="site-hero__breadcrumb flex items-center gap-2 mb-4 text-xs text-white/65" aria-label="Breadcrumb">
        <a href="/" class="hover:text-white transition-colors">Home</a>
        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <span class="text-white/85">{breadcrumb}</span>
      </nav>"""
    cta_html = (
        f'<a href="{u(cta[0])}" class="btn-ocean inline-flex items-center justify-center gap-2 text-white '
        f'font-semibold px-7 py-3 rounded-full text-sm shadow-xl">{cta[1]}</a>'
        if cta
        else ""
    )
    tags_html = ""
    if tags:
        tags_html = '<div class="site-hero__tags flex flex-wrap gap-2 mt-5 pt-4 border-t border-white/20">' + "".join(
            f'<span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full '
            f'px-3.5 py-1.5 text-xs font-semibold text-white">{t}</span>'
            for t in tags
        ) + "</div>"
    return f"""<section class="site-hero">
  <div class="absolute inset-0 hero-bg-custom" style="background-image: {HERO_GRADIENT}, url('/{image}');" role="img" aria-label="{aria}"></div>
  <div class="site-hero__inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl">{bc}
      <div class="site-hero__eyebrow inline-flex items-center gap-2 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 mb-3">
        <span class="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
        <span class="text-white/90 text-xs font-semibold tracking-widest uppercase">{eyebrow}</span>
      </div>
      <h1 class="site-hero__title text-4xl sm:text-5xl lg:text-[3.25rem] font-display font-bold text-white leading-tight mb-3">{title}</h1>
      <p class="site-hero__lead text-base sm:text-lg text-white/85 font-light leading-relaxed mb-5 max-w-2xl">{lead}</p>
      <div class="site-hero__actions flex flex-col sm:flex-row gap-3">{cta_html}</div>
      {tags_html}
    </div>
  </div>
  {_wave()}
</section>"""


def internal_links() -> str:
    links = [
        ("best-whittier-shore-excursions", "Best Excursions"),
        ("whittier-cruise-port-guide", "Port Guide"),
        ("prince-william-sound-guide", "Prince William Sound"),
        ("whittier-wildlife-guide", "Wildlife Guide"),
        ("whittier-tunnel-guide", "Tunnel Guide"),
        ("things-to-do-in-whittier-from-a-cruise-ship", "Things To Do"),
        ("whittier-faq", "FAQ"),
        ("enquire", "Enquire"),
    ]
    parts = []
    for i, (slug, label) in enumerate(links):
        if i:
            parts.append('<span class="text-gray-300">·</span>')
        parts.append(f'<a href="{u(slug)}" class="text-ocean-600 hover:text-ocean-800 font-medium">{label}</a>')
    return f"""<nav class="mt-10 pt-8 border-t border-gray-100" aria-label="Related Whittier guides">
  <p class="text-sm font-semibold text-gray-900 mb-3">Plan your Whittier port day</p>
  <div class="flex flex-wrap gap-3 text-sm">{"".join(parts)}</div>
</nav>"""


def help_cta() -> str:
    return f"""<div class="text-center mt-8 p-6 bg-alpine-50 rounded-2xl border border-alpine-100">
  <p class="text-gray-700 font-medium mb-3">Need help choosing the right Whittier excursion?</p>
  <a href="{u('enquire')}" class="btn-ocean inline-flex items-center justify-center text-white text-sm font-semibold px-6 py-3 rounded-full">Get personalised advice →</a>
</div>"""


def commercial_strip(best_for: str, wildlife: str, return_ship: str, pre_post: str) -> str:
    return f"""<aside class="commercial-strip" aria-label="Cruise passenger highlights">
  <h3>Why cruise passengers choose this</h3>
  <ul>
    <li><strong>Best for cruise passengers:</strong> {best_for}</li>
    <li><strong>Wildlife/glacier opportunities:</strong> {wildlife}</li>
    <li><strong>Return-to-ship timing:</strong> {return_ship}</li>
    <li><strong>Pre/post-cruise suitability:</strong> {pre_post}</li>
  </ul>
  {help_cta()}
</aside>"""


def cruise_snapshot(**kw: str) -> str:
    defaults = dict(
        time_in_port="6-10 hours for most Whittier calls; longer on embark/disembark days",
        best_for="Prince William Sound cruises, glacier viewing, wildlife, scenic transfers",
        activity_level="Easy boat tours to moderate trail walks depending on itinerary",
        family="Family-friendly with age-appropriate cruise-day options",
        return_ship="Most operators plan 60-90 minute buffer before all-aboard",
        popular="PWS wildlife cruise, glacier cruise, Spencer Glacier, scenic tours",
        pre_post="Strong gateway for Anchorage transfers and rail extensions",
    )
    defaults.update(kw)
    rows = "".join(
        f'<div class="cruise-snapshot__item"><dt>{k}</dt><dd>{v}</dd></div>'
        for k, v in [
            ("Typical Time In Port", defaults["time_in_port"]),
            ("Best For", defaults["best_for"]),
            ("Activity Level", defaults["activity_level"]),
            ("Family Friendly", defaults["family"]),
            ("Return To Ship Friendly", defaults["return_ship"]),
            ("Popular Excursion Types", defaults["popular"]),
            ("Pre/Post-Cruise", defaults["pre_post"]),
        ]
    )
    img, alt = IMG["cruise_snapshot"]
    return f"""<aside class="cruise-snapshot cruise-snapshot--with-image mb-10 px-4 sm:px-0" aria-label="Cruise passenger snapshot">
  <h3 class="font-display font-bold text-lg text-gray-900 mb-4">Cruise Passenger Snapshot</h3>
  <div class="cruise-snapshot__layout">
    <div class="cruise-snapshot__image info-image rounded-2xl overflow-hidden shadow-md"><img src="/{img}" alt="{alt}" width="640" height="480" loading="lazy" decoding="async" /></div>
    <dl class="cruise-snapshot__grid">{rows}</dl>
  </div>
</aside>"""


def excursion_meta(
    duration: str,
    fitness: str,
    wildlife: str,
    glacier_scenic: str,
    photography: str,
    best_for: str,
    return_ship: str,
    pre_post: str,
) -> str:
    cards = [
        ("Duration", duration),
        ("Fitness Level", fitness),
        ("Wildlife Opportunities", wildlife),
        ("Glacier Highlights", glacier_scenic),
        ("Photography Opportunities", photography),
        ("Best For", best_for),
        ("Return-To-Ship Confidence", return_ship),
        ("Pre/Post-Cruise Suitability", pre_post),
    ]
    body = "".join(
        f'<div class="excursion-meta__card"><h4>{h}</h4><p>{p}</p></div>' for h, p in cards
    )
    return f'<div class="excursion-meta max-w-5xl mx-auto px-4">{body}</div>'


def faq_block(items: list[tuple[str, str]]) -> str:
    body = "".join(
        f'<details class="faq-item rounded-2xl border border-alpine-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">{q}</summary><p class="mt-4 text-sm text-gray-500">{a}</p></details>'
        for q, a in items
    )
    return f'<section class="py-8"><div class="max-w-3xl mx-auto px-4 space-y-4"><h2 class="text-2xl font-display font-bold text-gray-900 mb-6">Frequently Asked Questions</h2>{body}</div></section>'


def card_grid(cards: list[tuple[str, str, str, str, str]]) -> str:
    items = []
    for img_key, title, desc, slug, label in cards:
        img, alt = IMG[img_key]
        items.append(f"""<div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-alpine-50 flex flex-col">
      <div class="card-media h-44 relative overflow-hidden"><img src="/{img}" alt="{alt}" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1">
        <h3 class="text-lg font-display font-semibold text-gray-900 mb-2">{title}</h3>
        <p class="text-sm text-gray-500 leading-relaxed flex-1">{desc}</p>
        <a href="{u(slug)}" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">{label}</a>
      </div>
    </div>""")
    return '<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">' + "".join(items) + "</div>"


def comparison_table() -> str:
    rows = [
        ("Prince William Sound Wildlife Cruise", "5-6 hrs", "Whales, otters and seabirds", "Easy", "prince-william-sound-wildlife-cruise"),
        ("Prince William Sound Glacier Cruise", "4.5-5 hrs", "Tidewater glaciers and fjords", "Easy", "prince-william-sound-glacier-cruise"),
        ("Spencer Glacier Float", "6-7 hrs", "Glacier views plus river float", "Moderate", "spencer-glacier-float"),
        ("Blackstone Bay Cruise", "5-6 hrs", "Remote glaciers and waterfalls", "Easy", "blackstone-bay-cruise"),
        ("Whittier Scenic Tour", "2.5-3 hrs", "Town, tunnel and canal views", "Easy", "whittier-scenic-tour"),
        ("Anchorage Transfer with Sightseeing", "4-6 hrs", "One-way transfer plus stops", "Easy", "anchorage-transfer-with-sightseeing"),
        ("Glacier Discovery Train", "6-8 hrs", "Railway glacier corridor", "Easy", "glacier-discovery-train"),
        ("Portage Glacier Tour", "4-5 hrs", "Lake cruise to glacier face", "Easy", "portage-glacier-tour"),
    ]
    body = "".join(
        f"""<tr class="border-b border-alpine-50 hover:bg-sand-50/80">
      <td class="py-4 pr-4 font-semibold text-gray-900"><a href="{u(link)}" class="text-ocean-600 hover:text-ocean-800">{name}</a></td>
      <td class="py-4 px-3 text-gray-600">{dur}</td>
      <td class="py-4 px-3 text-gray-600">{best}</td>
      <td class="py-4 px-3 text-gray-600">{act}</td>
      <td class="py-4 pl-3"><a href="{u(link)}" class="text-teal-600 font-medium text-xs whitespace-nowrap">Guide →</a></td>
    </tr>"""
        for name, dur, best, act, link in rows
    )
    return f"""<section class="py-16 bg-sand-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 text-center mb-4">Which Whittier Excursion Is Right for Me?</h2>
  <p class="text-center text-gray-600 text-sm max-w-2xl mx-auto mb-10">Compare durations, fitness, wildlife potential and return-to-ship confidence across Whittier's Prince William Sound experiences.</p>
  <div class="overflow-x-auto rounded-3xl border border-alpine-100 shadow-sm">
    <table class="w-full text-sm text-left min-w-[720px]">
      <thead class="bg-ocean-800 text-white"><tr>
        <th class="py-4 px-4 font-semibold rounded-tl-3xl">Excursion</th>
        <th class="py-4 px-3 font-semibold">Duration</th>
        <th class="py-4 px-3 font-semibold">Best For</th>
        <th class="py-4 px-3 font-semibold">Fitness Level</th>
        <th class="py-4 px-4 font-semibold rounded-tr-3xl">Details</th>
      </tr></thead>
      <tbody class="bg-white">{body}</tbody>
    </table>
  </div>
</div></section>"""


def excursion_page(ex: dict) -> str:
    img, alt = IMG[ex["image"]]
    bullets = "".join(
        f'<li class="flex gap-2 text-sm text-gray-600"><span class="text-ocean-500">✓</span>{b}</li>'
        for b in ex["bullets"]
    )
    snap = cruise_snapshot(**ex.get("cruise_snapshot", {}))
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div><p class="text-gray-600 leading-relaxed mb-6">{ex["intro"]}</p><ul class="space-y-3 mb-6">{bullets}</ul></div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg"><img src="/{img}" alt="{alt}" width="600" height="450" loading="lazy" decoding="async" /></div>
</div></div></section>
<section class="pb-4 bg-white">{excursion_meta(ex["duration"], ex["fitness"], ex["wildlife"], ex["glacier_scenic"], ex["photography"], ex["best_for"], ex["return_ship"], ex["pre_post"])}</section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">{commercial_strip(ex["best_for"], ex["wildlife"], ex["return_ship"], ex["pre_post"])}</div></section>
{faq_block(ex["faq"])}
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <a href="{u('enquire')}" class="btn-ocean inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full shadow-lg">{ex["cta"]}</a>
  {internal_links()}
</div></section>"""


def content_home() -> str:
    cards = card_grid([
        ("pws_wildlife", "Prince William Sound Wildlife Cruise", "Marine mammals, seabirds and fjord scenery on Whittier's signature water day.", "prince-william-sound-wildlife-cruise", "View Guide"),
        ("pws_glacier", "Prince William Sound Glacier Cruise", "Tidewater glaciers and blue ice in a compact cruise-day format.", "prince-william-sound-glacier-cruise", "View Guide"),
        ("spencer", "Spencer Glacier Float", "Rail corridor access, glacier views and a gentle river float adventure.", "spencer-glacier-float", "View Guide"),
        ("blackstone", "Blackstone Bay Cruise", "Remote waterfalls and glacier faces in a quieter sound channel.", "blackstone-bay-cruise", "View Guide"),
    ])
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div>
    <div class="inline-flex items-center gap-2 text-ocean-600 text-xs font-semibold tracking-widest uppercase mb-3"><div class="w-8 h-px bg-ocean-400"></div>Whittier · Prince William Sound</div>
    <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-5">Gateway to the sound.<br/><span class="text-ocean-600">Glacier country by sea.</span></h2>
    <p class="text-gray-600 leading-relaxed mb-5">Whittier opens directly onto Prince William Sound — a protected marine wilderness of tidewater glaciers, whale routes and rainforest mountains. This guide helps cruise guests match boat days, rail adventures and transfers to ship timing through the Anton Anderson Tunnel.</p>
    <a href="{u('best-whittier-shore-excursions')}" class="btn-ocean inline-flex items-center gap-2 text-white font-semibold px-7 py-3.5 rounded-full text-sm shadow-lg">Browse All Excursions</a>
  </div>
  <div class="info-image rounded-3xl aspect-[4/3] shadow-2xl overflow-hidden"><img src="/{IMG['intro'][0]}" alt="{IMG['intro'][1]}" width="800" height="600" loading="lazy" decoding="async" /></div>
</div></div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{cruise_snapshot()}</div></section>
<section class="py-16 bg-sand-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div class="text-center mb-12"><h2 class="text-3xl font-display font-bold text-gray-900">Top Prince William Sound Experiences</h2></div>
  {cards}
</div></section>
{comparison_table()}
<section class="py-16 cta-gradient"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-white mb-4">Plan Your Whittier Port Day</h2>
  <div class="flex flex-col sm:flex-row gap-4 justify-center">
    <a href="{u('whittier-cruise-port-guide')}" class="btn-primary inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Port Guide</a>
    <a href="{u('prince-william-sound-guide')}" class="btn-outline inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Prince William Sound Guide</a>
  </div>
</div></section>"""


def content_best() -> str:
    cards = card_grid([
        ("pws_wildlife", "PWS Wildlife Cruise", "Longer marine day with strong whale and seabird potential.", "prince-william-sound-wildlife-cruise", "Guide"),
        ("pws_glacier", "PWS Glacier Cruise", "Glacier-first routing with dramatic fjord scenery.", "prince-william-sound-glacier-cruise", "Guide"),
        ("train", "Glacier Discovery Train", "Scenic rail day linking Whittier corridor glaciers.", "glacier-discovery-train", "Guide"),
        ("transfer", "Anchorage Transfer", "Sightseeing transfer for embark/disembark logistics.", "anchorage-transfer-with-sightseeing", "Guide"),
    ])
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Best Whittier Shore Excursions</h2>
  <p class="text-gray-600 leading-relaxed text-sm">Independent comparison for cruise passengers choosing between Prince William Sound cruises, Spencer Glacier adventures and Anchorage transfer products.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">{commercial_strip('Guests prioritising sound access from a compact port', 'Humpbacks, orcas, sea otters, puffins and glacier faces', 'Cruise-timed operators build conservative return windows', 'Transfers and rail days suit pre/post-cruise extensions')}</div></section>
{comparison_table()}
<section class="py-16 bg-white"><div class="max-w-7xl mx-auto px-4">
  <h2 class="text-2xl font-display font-bold text-center mb-8">Most Booked Guides</h2>
  {cards}
  <div class="mt-12 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>"""


def content_port() -> str:
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <p class="text-gray-600 leading-relaxed text-sm">Whittier sits at the head of Passage Canal, reached through the Anton Anderson Memorial Tunnel. Most cruise operations stage at the port terminal with tour pickups coordinated around tunnel traffic windows.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{cruise_snapshot(popular='PWS cruises, Spencer Glacier, scenic tours, transfers')}</div></section>
<section class="py-12 bg-sand-50"><div class="max-w-7xl mx-auto px-4">
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-8 max-w-5xl mx-auto"><img src="/{IMG['port'][0]}" alt="{IMG['port'][1]}" width="1200" height="514" loading="lazy" decoding="async" /></div>
  <div class="grid lg:grid-cols-2 gap-6 text-sm">
    <div class="bg-white rounded-3xl p-6 border border-alpine-100"><h3 class="font-display font-bold text-lg mb-2">Where Ships Dock</h3><p class="text-gray-600">Cruise ships use Whittier's deepwater terminal at the edge of town. The compact layout means harbor, tour offices and the tunnel portal are all within a short transfer.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-alpine-100"><h3 class="font-display font-bold text-lg mb-2">Tunnel Logistics</h3><p class="text-gray-600">Road access runs on a timed schedule through North America's longest highway tunnel. Confirm whether your tour includes tunnel coordination and allow buffer on self-drive days.</p></div>
  </div>
</div></section>
<section class="py-12 bg-white"><div class="max-w-7xl mx-auto px-4">
  <div class="grid sm:grid-cols-3 gap-6 text-sm">
    <div class="bg-sand-50 rounded-2xl p-6"><strong class="text-gray-900">Currency</strong><p class="mt-2 text-gray-600">US dollars. Cards widely accepted; keep cash for small vendors.</p></div>
    <div class="bg-ocean-50 rounded-2xl p-6"><strong class="text-gray-900">Weather</strong><p class="mt-2 text-gray-600">Prince William Sound is cool and wet even in summer. Waterproof layers are essential on boat days.</p></div>
    <div class="bg-sand-50 rounded-2xl p-6"><strong class="text-gray-900">Wildlife Season</strong><p class="mt-2 text-gray-600">Marine mammals are active May through September with peak whale sightings in midsummer.</p></div>
  </div>
  <p class="text-center mt-8"><a href="{u('whittier-tunnel-guide')}" class="text-ocean-600 font-semibold text-sm">Anton Anderson Tunnel guide →</a></p>
  <div class="mt-10 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>"""


def content_things() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 text-sm text-center mb-8">Sample timeline for a Whittier cruise day. Adjust for your ship schedule and tunnel traffic windows.</p>
  <ol class="space-y-4 text-sm">
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-alpine-100"><span class="font-bold text-ocean-600 shrink-0">07:30</span><div><strong>Disembark and meet guide</strong><p class="text-gray-600 mt-1">Confirm pickup point near the cruise terminal and pack rain gear.</p></div></li>
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-alpine-100"><span class="font-bold text-ocean-600 shrink-0">08:00</span><div><strong>Prince William Sound wildlife or glacier cruise</strong><p class="text-gray-600 mt-1">Morning departures maximise calm water and wildlife activity.</p></div></li>
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-alpine-100"><span class="font-bold text-ocean-600 shrink-0">14:00</span><div><strong>Whittier scenic tour or Begich Towers walk</strong><p class="text-gray-600 mt-1">Light afternoon option if your cruise returns early enough.</p></div></li>
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-alpine-100"><span class="font-bold text-ocean-600 shrink-0">16:00</span><div><strong>Return with tunnel buffer</strong><p class="text-gray-600 mt-1">Leave margin before all-aboard, especially on transfer days.</p></div></li>
  </ol>
  <div class="mt-10">{commercial_strip('Guests building a full Prince William Sound day', 'Morning water time delivers the strongest wildlife odds', 'Conservative return timing protects against weather delays', 'Works as template for pre/post-cruise rail or transfer days')}</div>
  <div class="mt-8">{internal_links()}</div>
</div></section>"""


def content_pws_guide() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>
    <p class="text-gray-600 leading-relaxed mb-6"><strong>Prince William Sound</strong> is one of Alaska's great marine wilderness areas — a maze of fjords, rainforest islands and active tidewater glaciers reachable within hours of Whittier. For cruise passengers, this is the reason to choose Whittier over a pure transit stop.</p>
    <p class="text-gray-600 text-sm mb-6">Boat routes vary by operator and conditions, but most cruises combine glacier viewing passes with wildlife scanning for whales, sea otters and seabird colonies. Morning departures from Whittier typically offer the smoothest sea state.</p>
    <ul class="space-y-3 mb-6 text-sm text-gray-600">
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Wildlife cruises</strong> emphasise marine mammals and birdlife across longer routes.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Glacier cruises</strong> focus on calving faces and blue ice in protected channels.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Blackstone Bay</strong> offers a more remote glacier experience for repeat visitors.</li>
    </ul>
    <a href="{u('prince-william-sound-wildlife-cruise')}" class="text-ocean-600 font-semibold text-sm">Wildlife cruise guide →</a>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg"><img src="/{IMG['pws'][0]}" alt="{IMG['pws'][1]}" width="600" height="450" loading="lazy" decoding="async" /></div>
</div></div></section>
<section class="pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">{commercial_strip('Travellers who want Alaska glacier country by boat', 'Whales, otters, puffins and tidewater glaciers on one route', 'Operators publish explicit return-to-ship policies', 'Excellent anchor for multi-day Southcentral extensions')}</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{internal_links()}</div></section>"""


def content_anchorage_guide() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-6">Whittier-to-Anchorage connections matter for cruise guests who embark or disembark in the sound rather than Seward. The corridor crosses Turnagain Arm and Portage Valley, and the best transfer products add glacier or wildlife stops instead of pure highway time.</p>
  <p class="text-gray-600 text-sm mb-8">Plan around the Anton Anderson Tunnel schedule, luggage handling and whether you need hotel or airport drop-off. Many guests pair a morning Portage Glacier visit with an afternoon Anchorage arrival.</p>
  <a href="{u('anchorage-transfer-with-sightseeing')}" class="btn-ocean inline-flex items-center justify-center text-white text-sm font-semibold px-6 py-3 rounded-full">Transfer with sightseeing guide →</a>
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_wildlife() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>
    <p class="text-gray-600 leading-relaxed mb-6">Prince William Sound from Whittier delivers consistent marine wildlife — humpback and orca sightings, rafts of sea otters, harbor seals and dramatic seabird colonies along glacier-fed coastlines.</p>
    <ul class="space-y-3 mb-6 text-sm text-gray-600">
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Whales:</strong> humpbacks and orcas frequent sound channels; timing varies by month.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Sea otters:</strong> common in kelp beds and protected coves.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Seabirds:</strong> puffins, kittiwakes and bald eagles on cliff colonies.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Land wildlife:</strong> mountain goats and bears appear on some scenic and trail routes.</li>
    </ul>
    <a href="{u('prince-william-sound-wildlife-cruise')}" class="text-ocean-600 font-semibold text-sm">PWS wildlife cruise →</a>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg"><img src="/{IMG['wildlife'][0]}" alt="{IMG['wildlife'][1]}" width="600" height="450" loading="lazy" decoding="async" /></div>
</div></div></section>
<section class="pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">{commercial_strip('Wildlife-first itineraries from Whittier', 'Marine mammals and seabirds on dedicated wildlife cruises', 'Cruise-timed departures with published return buffers', 'Strong for photographers with telephoto gear')}</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{internal_links()}</div></section>"""


def content_vs_seward() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-8">Whittier and Seward both connect cruise travelers to Southcentral Alaska's glacier and wildlife country, but they serve different strengths. Whittier is the direct gateway to Prince William Sound; Seward opens onto Resurrection Bay and Kenai Fjords National Park.</p>
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-10"><img src="/{IMG['vs_seward'][0]}" alt="{IMG['vs_seward'][1]}" width="1200" height="514" loading="lazy" decoding="async" /></div>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Glacier cruises</h2>
  <p class="text-gray-600 text-sm mb-6"><strong>Whittier</strong> routes explore Prince William Sound — Blackstone Bay, Harriman Fjord and College Fjord-style scenery with rainforest mountains plunging into the water. <strong>Seward</strong> focuses on Kenai Fjords with iconic Aialik and Holgate glacier faces. Both deliver tidewater glacier moments; Whittier feels more fjord-maze intimate, Seward more national-park dramatic.</p>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Whale watching</h2>
  <p class="text-gray-600 text-sm mb-6">Both ports offer strong humpback and orca potential in season. Prince William Sound from Whittier spreads sightings across protected channels with fewer competing boats than some Seward routes. Seward's longer wildlife cruises can reach deeper into Kenai Fjords for extended marine mammal scanning.</p>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Wildlife beyond whales</h2>
  <p class="text-gray-600 text-sm mb-6">Whittier excels at sea otters, puffins and seal colonies on sound cruises. Seward adds strong seabird cliffs plus land options like Exit Glacier walks. Neither port guarantees specific species — season and route matter more than port name.</p>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Accessibility and logistics</h2>
  <p class="text-gray-600 text-sm mb-6">Seward has open highway access year-round. Whittier requires the timed Anton Anderson Tunnel — a unique constraint that tour operators manage but independent drivers must schedule. Whittier's town footprint is smaller; most guests go straight to water or rail products.</p>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Cruise itineraries and embarkation</h2>
  <p class="text-gray-600 text-sm mb-6">Some Alaska cruise tours use Whittier for one-way Gulf of Alaska segments, pairing sound access with Anchorage transfers. Seward appears on more classic round-trip Inside Passage and Gulf combinations with broader pre/post hotel choice.</p>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Independent travellers</h2>
  <p class="text-gray-600 text-sm mb-6">Seward offers easier independent planning with more lodging, dining and self-drive flexibility. Whittier suits travelers comfortable booking tunnel-aware tours or rail products — see our <a href="{u('whittier-for-independent-travellers')}" class="text-ocean-600 font-semibold">independent travellers guide</a>.</p>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Families</h2>
  <p class="text-gray-600 text-sm mb-6">Both ports work for families on easy boat tours. Whittier's compact port day reduces walking; Seward adds the Alaska SeaLife Center and more in-town options if younger children need a break from boats.</p>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Photography</h2>
  <p class="text-gray-600 text-sm mb-8">Whittier delivers moody fjord light, waterfall curtains and glacier reflections in protected water. Seward offers dramatic cliff seabird colonies and Exit Glacier access on land. Serious wildlife photographers often book dedicated sound cruises from Whittier for otter and whale action at close range.</p>
  <p class="text-sm text-gray-600 mb-8">For the Seward perspective on this comparison, see the editorial guide at <a href="https://sewardshoreexcursion.com/seward-vs-whittier-cruise-port" class="text-ocean-600 font-semibold" rel="noopener noreferrer">sewardshoreexcursion.com/seward-vs-whittier-cruise-port</a>.</p>
  {commercial_strip('Travelers choosing between Southcentral embarkation ports', 'Both deliver marine wildlife; glacier scenery differs by sound versus fjords', 'Both work with cruise-aware operator timing', 'Whittier emphasises sound access; Seward offers broader town infrastructure')}
  <div class="mt-8">{internal_links()}</div>
</div></section>"""


def content_tunnel() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-6">The <strong>Anton Anderson Memorial Tunnel</strong> is the only road link between Whittier and the rest of the road system. At roughly 2.5 miles, it is North America's longest highway tunnel — and it shares a single lane with the Alaska Railroad.</p>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Timed traffic</h2>
  <p class="text-gray-600 text-sm mb-6">Vehicle traffic runs on a published schedule alternating direction roughly every 30 minutes. Arrive early for your window; missing a slot can delay tours and cruise transfers significantly during peak summer days.</p>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Rail sharing</h2>
  <p class="text-gray-600 text-sm mb-6">When trains pass, vehicle windows pause. Spencer Glacier and Glacier Discovery train guests experience the tunnel from the rail side — a memorable approach to Whittier that many cruise extensions include.</p>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Travel tips</h2>
  <ul class="space-y-3 text-sm text-gray-600 mb-6">
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Check the current schedule before self-driving from Anchorage.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Tunnel fees apply; tour operators often include coordination in packages.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Allow extra buffer on embarkation days with luggage and rental returns.</li>
  </ul>
  <h2 class="text-xl font-display font-bold text-gray-900 mb-3">Cruise passenger advice</h2>
  <p class="text-gray-600 text-sm mb-8">Most shore excursions handle tunnel timing for you. If you book independently, confirm whether pickup is inside Whittier or at the tunnel portal on the Portage side. Cruise lines sometimes bus guests through the tunnel on turn-around days — follow ship instructions rather than assuming public schedules.</p>
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-8"><img src="/{IMG['tunnel'][0]}" alt="{IMG['tunnel'][1]}" width="1200" height="514" loading="lazy" decoding="async" /></div>
  {commercial_strip('Anyone driving or booking independent Whittier access', 'Tunnel timing affects all road-based arrivals', 'Build buffer on cruise embark/disembark days', 'Rail products bypass road-schedule stress')}
  <div class="mt-8">{internal_links()}</div>
</div></section>"""


def content_portage_pass() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>
    <p class="text-gray-600 leading-relaxed mb-6">The <strong>Portage Pass Trail</strong> climbs from the tunnel area to alpine views over Portage Glacier and Passage Canal. It is one of the few substantial hikes reachable on a Whittier-focused itinerary, though most cruise-day guests choose boat tours instead due to timing.</p>
    <p class="text-gray-600 text-sm mb-6">The trail is roughly four miles round trip with moderate elevation gain. Weather changes quickly; carry layers, rain gear and bear-aware practices. Independent travelers with extra days pair this hike with a Whittier sound cruise.</p>
    <ul class="space-y-3 mb-6 text-sm text-gray-600">
      <li class="flex gap-2"><span class="text-ocean-500">✓</span>Best in clear weather for glacier and sound panoramas.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span>Not typical for short cruise calls — verify duration carefully.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span>Strong photography at the pass on calm days.</li>
    </ul>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg"><img src="/{IMG['portage_pass'][0]}" alt="{IMG['portage_pass'][1]}" width="600" height="450" loading="lazy" decoding="async" /></div>
</div></div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{internal_links()}</div></section>"""


def content_begich() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>
    <p class="text-gray-600 leading-relaxed mb-6">Whittier's story is unlike any other Alaska town. Built rapidly during World War II as a secret military port, most residents once lived under one roof in the <strong>Begich Towers</strong> — a fourteen-story building that still houses condos, offices and the post office.</p>
    <p class="text-gray-600 text-sm mb-6">Walking the waterfront reveals rusted rail infrastructure, tunnel mouths and mountains that trap sound and weather. Understanding this context deepens a Prince William Sound visit beyond checking off a glacier cruise.</p>
    <ul class="space-y-3 mb-6 text-sm text-gray-600">
      <li class="flex gap-2"><span class="text-ocean-500">✓</span>Combine a short town walk with a scenic tour on lighter port days.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span>Respect residents — Whittier is a living community, not a museum set.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span>Pair with tunnel and rail history for a fuller picture.</li>
    </ul>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg"><img src="/{IMG['begich'][0]}" alt="{IMG['begich'][1]}" width="600" height="450" loading="lazy" decoding="async" /></div>
</div></div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{internal_links()}</div></section>"""


def content_independent() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-6">Whittier rewards independent travelers who plan around the tunnel, book sound cruises directly and accept a smaller town footprint than Seward or Anchorage. You trade restaurant variety for immediate access to Prince William Sound wilderness.</p>
  <p class="text-gray-600 text-sm mb-6"><strong>Practical tips:</strong> reserve tunnel slots and cruise tickets early in July and August; consider one night in Whittier to avoid rushing a single port-day window; rail products to Spencer Glacier integrate smoothly with Anchorage lodging.</p>
  <ul class="space-y-3 text-sm text-gray-600 mb-8">
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Book PWS cruises directly with operators that publish return policies.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Use Anchorage as your supply hub; Whittier has limited services.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Portage Pass and Begich Towers suit extra days, not tight cruise calls.</li>
  </ul>
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-8"><img src="/{IMG['independent'][0]}" alt="{IMG['independent'][1]}" width="1200" height="514" loading="lazy" decoding="async" /></div>
  {commercial_strip('Self-planned Alaska travelers using Whittier as a sound base', 'Direct access to PWS without a large tour port infrastructure', 'You manage tunnel and return timing on cruise days', 'Excellent for rail-plus-cruise hybrid itineraries')}
  <div class="mt-8">{internal_links()}</div>
</div></section>"""


def content_best_time() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-8">Whittier cruise and excursion season runs late spring through early fall, with Prince William Sound boat operations peaking when cruise ships call. Month choice shifts wildlife activity, daylight and crowd pressure at the tunnel.</p>
  <div class="space-y-4 text-sm mb-8">
    <div class="bg-sand-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">May-June</strong><p class="mt-2 text-gray-600">Longer daylight, cooler conditions and fewer tunnel traffic jams than midsummer peaks.</p></div>
    <div class="bg-ocean-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">July-August</strong><p class="mt-2 text-gray-600">Peak cruise demand, strongest whale activity and busiest booking window for sound cruises.</p></div>
    <div class="bg-sand-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">September</strong><p class="mt-2 text-gray-600">Shoulder season with softer light, fewer ships and often good value on extensions.</p></div>
  </div>
  <p class="text-sm text-gray-600 mb-8">Cross-check your date on the <a href="{u('whittier-cruise-ship-schedule')}" class="text-ocean-600 font-semibold">Whittier cruise ship schedule</a> page.</p>
  {internal_links()}
</div></section>"""


def content_schedule() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-6">Whittier receives select Alaska cruise traffic, often on Gulf of Alaska repositioning or one-way itineraries. Embarkation and disembarkation days add tunnel logistics that standard port calls avoid.</p>
  <p class="text-gray-600 text-sm mb-6"><strong>Typical pattern:</strong> excursion departures cluster in morning windows to protect afternoon return margins and tunnel coordination.</p>
  <ul class="space-y-3 text-sm text-gray-600 mb-8">
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Book Prince William Sound cruises early on popular ship days.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Allow extra margin on transfer days with Anchorage flights or rail.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Reconfirm meeting point and tunnel timing 24 hours before tour date.</li>
  </ul>
  <a href="{u('whittier-cruise-planner')}" class="text-ocean-600 font-semibold text-sm">Use the Whittier cruise planner →</a>
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_planner() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 text-sm text-center mb-8">Checklist your priorities, then match tours on our <a href="{u('best-whittier-shore-excursions')}" class="text-ocean-600 font-semibold">best excursions page</a>.</p>
  <div class="planner-checklist space-y-3 mb-10">
    <label><input type="checkbox" /> I want maximum Prince William Sound wildlife</label>
    <label><input type="checkbox" /> Tidewater glacier scenery is my top priority</label>
    <label><input type="checkbox" /> I prefer an easy, mostly seated boat tour</label>
    <label><input type="checkbox" /> I need family-friendly activities</label>
    <label><input type="checkbox" /> I want a rail or Spencer Glacier experience</label>
    <label><input type="checkbox" /> I need transfer support to Anchorage</label>
    <label><input type="checkbox" /> I care most about conservative return timing</label>
  </div>
  {help_cta()}
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_enquire() -> str:
    return f"""<section class="pt-8 pb-16 bg-white"><div class="max-w-xl mx-auto px-4">
  <p class="text-gray-600 text-sm text-center mb-8">Tell us your ship, date and priorities and we will suggest the best Whittier excursion options for your timing and comfort level.</p>
  <form class="enquire-form" action="mailto:{ENQUIRY_EMAIL}" method="post" enctype="text/plain">
    <label for="name">Your name</label>
    <input id="name" name="name" type="text" required />
    <label for="email">Email</label>
    <input id="email" name="email" type="email" required />
    <label for="ship">Cruise ship and date</label>
    <input id="ship" name="ship" type="text" placeholder="e.g. Ship name, 15 July 2026" required />
    <label for="interest">Interested in</label>
    <select id="interest" name="interest">
      <option>Prince William Sound Wildlife Cruise</option>
      <option>Prince William Sound Glacier Cruise</option>
      <option>Spencer Glacier Float</option>
      <option>Blackstone Bay Cruise</option>
      <option>Whittier Scenic Tour</option>
      <option>Anchorage Transfer with Sightseeing</option>
      <option>Glacier Discovery Train</option>
      <option>Portage Glacier Tour</option>
      <option>Not sure, help me choose</option>
    </select>
    <label for="message">Message</label>
    <textarea id="message" name="message" rows="4" placeholder="Group size, mobility needs, timing concerns..."></textarea>
    <button type="submit" class="btn-ocean w-full text-white font-semibold py-3 rounded-full">Send enquiry</button>
  </form>
  <p class="text-xs text-gray-400 text-center mt-6">We respond within 1-2 business days. Not affiliated with any cruise line.</p>
</div></section>"""


FAQ_QA = [
    ("How long do cruise ships stay in Whittier?", "Most excursion windows are planned around roughly 6-10 hour operating ranges, but always confirm your exact schedule."),
    ("Is Whittier only a cruise port?", "No — Whittier is primarily a gateway to Prince William Sound. Most visitors come for glacier and wildlife cruises, rail adventures and scenic transfers."),
    ("Do I need to worry about the tunnel?", "Tour operators usually coordinate Anton Anderson Tunnel timing. Independent drivers must follow the published vehicle schedule."),
    ("Which Whittier excursion is best for glaciers?", "Prince William Sound glacier cruises and Blackstone Bay routes focus on tidewater ice. Portage Glacier Tour adds a lake approach near the tunnel."),
    ("Can I see whales from Whittier?", "Yes. Dedicated wildlife cruises and many glacier routes scan for humpbacks, orcas and sea otters throughout the season."),
    ("Whittier or Seward for my cruise?", "Choose Whittier for Prince William Sound fjords; Seward for Kenai Fjords and more town infrastructure. See our comparison guide for detail."),
]


def content_faq() -> str:
    return f"""<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{cruise_snapshot(best_for='Quick planning answers for Whittier')}</div></section>
{faq_block(FAQ_QA)}
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{internal_links()}</div></section>"""


EXCURSIONS = [
    {
        "slug": "prince-william-sound-wildlife-cruise",
        "label": "Prince William Sound Wildlife Cruise",
        "hero_title": f"Prince William Sound<br/><span class=\"{ACCENT}\">Wildlife Cruise</span>",
        "hero_lead": "Whittier's flagship marine day — whales, sea otters, puffins and glacier-carved fjords in one route.",
        "image": "pws_wildlife",
        "intro": "This is the essential Prince William Sound experience from Whittier: protected channels, rainforest coastlines and high wildlife potential with naturalist narration focused on marine ecology and glacial landscapes.",
        "bullets": [
            "Strong odds for humpbacks, sea otters and seabird colonies",
            "Best first-choice excursion for Prince William Sound newcomers",
            "Longer route depth than shorter glacier-only cruises",
            "Cruise-timed operators include conservative return margins",
        ],
        "duration": "5-6 hours",
        "fitness": "Easy — mostly seated marine touring",
        "wildlife": "Humpbacks, orcas, sea otters, seals, puffins and seabird cliffs",
        "glacier_scenic": "Fjord walls and glacier viewpoints on suitable routes",
        "photography": "Excellent for telephoto wildlife and fjord landscapes from deck",
        "best_for": "Guests wanting Whittier's most complete marine wildlife day",
        "return_ship": "High confidence on cruise-day departures with published return windows",
        "pre_post": "Excellent extension when you have a full sound-access day",
        "faq": [
            ("How rough is the water?", "Prince William Sound is relatively protected, but conditions vary; operators adjust routes for comfort."),
            ("Will I definitely see whales?", "Wildlife is never guaranteed, but this route offers among the strongest odds from Whittier."),
            ("Is food included?", "Many operators provide snacks or meal options depending on package."),
        ],
        "cta": "Enquire about this tour →",
        "cruise_snapshot": {"best_for": "Maximum wildlife and fjord value in one day", "popular": "Top-booked Prince William Sound cruise from Whittier"},
    },

    {
        "slug": "prince-william-sound-glacier-cruise",
        "label": "Prince William Sound Glacier Cruise",
        "hero_title": f"Prince William Sound<br/><span class=\"{ACCENT}\">Glacier Cruise</span>",
        "hero_lead": "Tidewater glacier scenery and blue ice in a balanced half-day from Whittier.",
        "image": "pws_glacier",
        "intro": "A focused glacier cruise for guests who want dramatic ice faces and fjord scenery without committing to the longest wildlife routes. Ideal when your ship schedule favours a medium-duration boat day.",
        "bullets": [
            "Close passes at tidewater glacier faces when conditions allow",
            "Often easier fit for tighter port windows",
            "Comfortable for families and mixed ages",
            "Strong photo opportunities at calving viewpoints",
        ],
        "duration": "4.5-5 hours",
        "fitness": "Easy",
        "wildlife": "Sea otters, seals, seabirds and possible whale sightings",
        "glacier_scenic": "Tidewater glacier focus with waterfall and fjord scenery",
        "photography": "Strong glacier reflections and ice-blue detail shots from vessel",
        "best_for": "Guests prioritising glacier views with moderate trip length",
        "return_ship": "Very good confidence when matched to your ship schedule",
        "pre_post": "Works for cruise day and pre/post sound sightseeing",
        "faq": [
            ("How is this different from the wildlife cruise?", "This option is usually shorter and more glacier-concentrated."),
            ("Can children join?", "Yes, it is commonly selected by families."),
            ("Do routes change?", "Captains adapt for weather, sea state and ice conditions."),
        ],
        "cta": "Enquire about this tour →",
        "cruise_snapshot": {"best_for": "Glacier-first sightseeing with flexible timing"},
    },
    {
        "slug": "spencer-glacier-float",
        "label": "Spencer Glacier Float",
        "hero_title": f"Spencer Glacier<br/><span class=\"{ACCENT}\">Float Trip</span>",
        "hero_lead": "Alaska Railroad access, glacier views and a gentle river float through Spencer Lake country.",
        "image": "spencer",
        "intro": "The Spencer Glacier experience combines rail travel through the Whittier corridor with glacier viewing and a guided float on calm river water. It is one of Whittier's most distinctive adventure formats beyond standard sound cruises.",
        "bullets": [
            "Rail segment through mountain and glacier scenery",
            "Float section suitable for beginners with proper gear",
            "Higher activity level than seated boat tours",
            "Popular pre/post-cruise product with advance booking",
        ],
        "duration": "6-7 hours",
        "fitness": "Moderate — short walks plus float participation",
        "wildlife": "Occasional mountain goat and bird sightings; wildlife secondary",
        "glacier_scenic": "Spencer Glacier terminus and alpine lake setting",
        "photography": "Landscape and glacier panoramas; action shots on float section",
        "best_for": "Adventurous guests wanting rail plus active outdoor time",
        "return_ship": "Good when booked on compatible departure times only",
        "pre_post": "Primary use case is extensions outside strict port-call windows",
        "faq": [
            ("Do I need experience floating?", "No — guided floats use stable craft with instruction provided."),
            ("What should I wear?", "Expect splash risk; operators provide gear lists for layers and footwear."),
            ("Is this feasible on a short port call?", "Verify duration carefully — this is longer than typical scenic tours."),
        ],
        "cta": "Enquire about this tour →",
        "cruise_snapshot": {"activity_level": "Most active popular Whittier day trip"},
    },
    {
        "slug": "blackstone-bay-cruise",
        "label": "Blackstone Bay Cruise",
        "hero_title": f"Blackstone Bay<br/><span class=\"{ACCENT}\">Cruise</span>",
        "hero_lead": "Remote waterfalls, glacier faces and quiet channels in Prince William Sound.",
        "image": "blackstone",
        "intro": "Blackstone Bay routes reach some of the sound's most photogenic glacier and waterfall combinations with fewer vessels than busier corridors. A strong choice for repeat Alaska visitors who want a quieter ice experience from Whittier.",
        "bullets": [
            "Dramatic waterfall curtains on glacier-fed cliffs",
            "Less crowded routing than some headline fjords",
            "Naturalist interpretation on geology and ice dynamics",
            "Excellent for photographers seeking moody sound light",
        ],
        "duration": "5-6 hours",
        "fitness": "Easy — vessel-based touring",
        "wildlife": "Sea otters, seals and seabirds; whales possible in transit",
        "glacier_scenic": "Blackstone and Beloit glacier areas with waterfall scenery",
        "photography": "Outstanding waterfall and glacier combination shots",
        "best_for": "Guests wanting remote sound scenery with glacier payoff",
        "return_ship": "High confidence on standard cruise-day scheduling",
        "pre_post": "Strong full-day option for sound-focused extensions",
        "faq": [
            ("Is Blackstone Bay rougher than other routes?", "Routes are generally protected, but weather still affects comfort."),
            ("How does this compare to the glacier cruise?", "Blackstone Bay emphasises remote channels and waterfalls."),
            ("Is lunch included?", "Check your operator — longer routes may include meal service."),
        ],
        "cta": "Enquire about this tour →",
        "cruise_snapshot": {"best_for": "Remote glacier and waterfall photography"},
    },
    {
        "slug": "whittier-scenic-tour",
        "label": "Whittier Scenic Tour",
        "hero_title": f"Whittier Scenic<br/><span class=\"{ACCENT}\">Tour</span>",
        "hero_lead": "Passage Canal, tunnel context and town history without a full-day boat commitment.",
        "image": "scenic",
        "intro": "A relaxed overview of Whittier's unique setting — harbor views, tunnel approach, Begich Towers context and Prince William Sound lookouts. Ideal for guests who prefer gentle pacing or need a shorter excursion window.",
        "bullets": [
            "Minimal walking with easy logistics",
            "Good orientation for first-time Whittier visitors",
            "Often fits afternoon slots after a morning cruise",
            "Pairs with independent tunnel and waterfront exploration",
        ],
        "duration": "2.5-3 hours",
        "fitness": "Easy",
        "wildlife": "Occasional eagle and marine sightings; wildlife secondary",
        "glacier_scenic": "Distant glacier and mountain panoramas from viewpoints",
        "photography": "Harbor, tunnel and mountain vista opportunities",
        "best_for": "Guests preferring low-activity touring and local context",
        "return_ship": "Very high confidence due to short duration",
        "pre_post": "Useful add-on before rail departures or Anchorage transfers",
        "faq": [
            ("Is this mostly driving?", "Yes, with short viewpoint and photo stops."),
            ("Can this replace a sound cruise?", "It complements rather than replaces glacier and wildlife boat days."),
            ("Is this suitable for seniors?", "Yes — one of Whittier's easiest excursion types."),
        ],
        "cta": "Enquire about this tour →",
        "cruise_snapshot": {"best_for": "Low-effort sightseeing and orientation"},
    },
    {
        "slug": "anchorage-transfer-with-sightseeing",
        "label": "Anchorage Transfer with Sightseeing",
        "hero_title": f"Anchorage Transfer<br/><span class=\"{ACCENT}\">with Sightseeing</span>",
        "hero_lead": "Move between Whittier and Anchorage with meaningful glacier and valley stops en route.",
        "image": "transfer",
        "intro": "High-utility for cruise travelers ending or starting in Whittier: transfer between Anchorage and the sound while still seeing Portage Valley highlights rather than losing the day to highway miles alone.",
        "bullets": [
            "Best fit for disembarkation or embarkation logistics",
            "Luggage-aware planning with scenic stop structure",
            "Tunnel scheduling coordinated by experienced drivers",
            "Can align with flight times when booked early",
        ],
        "duration": "4-6 hours",
        "fitness": "Easy",
        "wildlife": "Occasional roadside sightings depending on route and season",
        "glacier_scenic": "Portage Valley and Turnagain Arm corridor scenery",
        "photography": "Mountain and water viewpoints on scheduled stops",
        "best_for": "Guests transferring between Whittier and Anchorage efficiently",
        "return_ship": "Transfer-focused timing rather than same-ship return product",
        "pre_post": "Primary use case is pre/post cruise movement",
        "faq": [
            ("Can I bring luggage?", "Yes, transfer products are built for luggage handling."),
            ("Is hotel drop-off available?", "Many operators offer this — confirm your endpoint."),
            ("Can this work after a morning cruise?", "Sometimes, depending on exact timing and tunnel windows."),
        ],
        "cta": "Enquire about this tour →",
        "cruise_snapshot": {"pre_post": "Top pre/post cruise logistics product from Whittier"},
    },
    {
        "slug": "glacier-discovery-train",
        "label": "Glacier Discovery Train",
        "hero_title": f"Glacier Discovery<br/><span class=\"{ACCENT}\">Train</span>",
        "hero_lead": "Scenic Alaska Railroad day linking glaciers, tunnels and mountain corridors near Whittier.",
        "image": "train",
        "intro": "The Glacier Discovery route showcases Alaska Railroad scenery through the Whittier corridor — tunnel transit, alpine valleys and glacier views from comfortable rail cars with narration and photo windows.",
        "bullets": [
            "Unique tunnel experience shared with highway traffic schedule",
            "Less weather exposure than open-deck boat days",
            "Strong option for rail enthusiasts and multi-modal itineraries",
            "Often combined with Spencer Glacier products on longer days",
        ],
        "duration": "6-8 hours",
        "fitness": "Easy — mostly seated rail travel with optional stops",
        "wildlife": "Occasional mountain goat and eagle sightings from train",
        "glacier_scenic": "Spencer and corridor glacier views from rail alignment",
        "photography": "Large windows and designated stop opportunities",
        "best_for": "Guests wanting iconic Alaska rail scenery near Whittier",
        "return_ship": "Good when booked on cruise-compatible departures",
        "pre_post": "Excellent anchor for Anchorage–Whittier extensions",
        "faq": [
            ("Does the train go into Whittier?", "Corridor services connect the Whittier area with Anchorage routing — confirm your ticket endpoints."),
            ("Is this better in rain?", "Rail can be a strong all-weather alternative to boat tours."),
            ("Can I combine with a sound cruise?", "Usually separate days unless you have a long port window."),
        ],
        "cta": "Enquire about this tour →",
        "cruise_snapshot": {"best_for": "Rail-first scenic day from the Whittier corridor"},
    },
    {
        "slug": "portage-glacier-tour",
        "label": "Portage Glacier Tour",
        "hero_title": f"Portage Glacier<br/><span class=\"{ACCENT}\">Tour</span>",
        "hero_lead": "Lake cruise to glacier ice near the tunnel — strong half-day option from Whittier access.",
        "image": "portage",
        "intro": "Portage Glacier tours reach active ice across Portage Lake, often paired with tunnel-area logistics. This works well for guests who want tangible glacier contact without committing to a full Prince William Sound boat day.",
        "bullets": [
            "Short lake cruise to glacier viewing distance",
            "Can pair with Anchorage transfer itineraries",
            "Good weather-resilient glacier alternative",
            "Interpretation on ice retreat and lake dynamics",
        ],
        "duration": "4-5 hours",
        "fitness": "Easy — boat and short walking at visitor areas",
        "wildlife": "Limited marine focus; occasional bird sightings",
        "glacier_scenic": "Portage Glacier face across lake icebergs",
        "photography": "Blue ice, berg details and mountain backdrop shots",
        "best_for": "Guests wanting accessible glacier viewing near the tunnel",
        "return_ship": "Very good confidence on half-day scheduling",
        "pre_post": "Excellent shoulder-day activity before or after cruise",
        "faq": [
            ("How close do we get to the glacier?", "Lake cruises approach viewing distance; exact proximity varies with ice conditions."),
            ("Is this inside Prince William Sound?", "No — Portage is a separate lake system near the tunnel portal."),
            ("Can I combine with a PWS cruise?", "Only on long port days — most guests choose one glacier experience per day."),
        ],
        "cta": "Enquire about this tour →",
        "cruise_snapshot": {"best_for": "Accessible glacier viewing near Whittier access"},
    },
]


EXC_NAV = {ex["slug"]: ex["label"] for ex in EXCURSIONS}


def content_map() -> dict[str, str]:
    return {
        "home.html": content_home(),
        "best-whittier-shore-excursions.html": content_best(),
        "whittier-cruise-port-guide.html": content_port(),
        "things-to-do-in-whittier-from-a-cruise-ship.html": content_things(),
        "prince-william-sound-guide.html": content_pws_guide(),
        "whittier-to-anchorage-guide.html": content_anchorage_guide(),
        "whittier-vs-seward.html": content_vs_seward(),
        "whittier-tunnel-guide.html": content_tunnel(),
        "whittier-cruise-planner.html": content_planner(),
        "whittier-faq.html": content_faq(),
        "enquire.html": content_enquire(),
        "whittier-cruise-ship-schedule.html": content_schedule(),
        "best-time-to-visit-whittier.html": content_best_time(),
        "whittier-wildlife-guide.html": content_wildlife(),
        "portage-pass-trail-guide.html": content_portage_pass(),
        "begich-towers-and-whittier-history.html": content_begich(),
        "whittier-for-independent-travellers.html": content_independent(),
    }


def heroes() -> dict[str, str]:
    return {
        "home": hero(
            "Prince William Sound · Alaska",
            "Whittier Shore Excursions",
            "Gateway to Prince William Sound, glacier cruises and unforgettable Alaska adventures.",
            "home",
            cta=("best-whittier-shore-excursions", "Compare Excursions"),
            tags=["Prince William Sound", "Glacier Cruises", "Wildlife", "Return-To-Ship Confidence"],
        ),
        "best": hero("Independent Guide", f"Best Whittier<br/><span class=\"{ACCENT}\">Shore Excursions</span>", "Compare eight Prince William Sound tours by duration, fitness, wildlife payoff and transfer suitability.", "best", breadcrumb="Best Excursions", cta=("enquire", "Need help choosing? →")),
        "port": hero("Cruise Passenger Guide", f"Whittier<br/><span class=\"{ACCENT}\">Cruise Port Guide</span>", "Dock logistics, tunnel timing and practical planning for your Whittier port window.", "port", breadcrumb="Port Guide"),
        "things": hero("Port Day Timeline", f"Things To Do in<br/><span class=\"{ACCENT}\">Whittier</span> from a Cruise Ship", "A practical sequence to combine Prince William Sound cruises while protecting return time.", "things", breadcrumb="Things To Do"),
        "pws_guide": hero("Marine Wilderness", f"Prince William Sound<br/><span class=\"{ACCENT}\">Guide</span>", "Route strategy, glacier expectations and booking tips for Whittier's signature sound experiences.", "pws", breadcrumb="Prince William Sound"),
        "anchorage_guide": hero("Logistics + Sightseeing", f"Whittier to Anchorage<br/><span class=\"{ACCENT}\">Transfer Guide</span>", "Choose transfer products that protect tunnel logistics while still delivering scenic value.", "transfer", breadcrumb="Anchorage Guide"),
        "vs_seward": hero("Port Comparison", f"Whittier vs Seward<br/><span class=\"{ACCENT}\">Cruise Ports</span>", "Prince William Sound access versus Kenai Fjords — an honest comparison for cruise passengers.", "vs_seward", breadcrumb="Whittier vs Seward"),
        "tunnel": hero("Anton Anderson Tunnel", f"Whittier<br/><span class=\"{ACCENT}\">Tunnel Guide</span>", "Timed traffic, rail sharing and cruise passenger advice for North America's longest highway tunnel.", "tunnel", breadcrumb="Tunnel Guide"),
        "wildlife": hero("Marine Wildlife", f"Whittier<br/><span class=\"{ACCENT}\">Wildlife Guide</span>", "What you can see by season and which excursions maximise Prince William Sound wildlife.", "wildlife", breadcrumb="Wildlife Guide"),
        "portage_pass": hero("Alpine Hiking", f"Portage Pass<br/><span class=\"{ACCENT}\">Trail Guide</span>", "Alpine views over Portage Glacier and Passage Canal for independent hikers with extra time.", "portage_pass", breadcrumb="Portage Pass"),
        "begich": hero("Town History", f"Begich Towers &amp;<br/><span class=\"{ACCENT}\">Whittier History</span>", "WWII port origins, tunnel access and the remarkable story of Alaska's building-in-a-building town.", "begich", breadcrumb="Begich Towers"),
        "independent": hero("Self-Planned Travel", f"Whittier for<br/><span class=\"{ACCENT}\">Independent Travellers</span>", "Tunnel-aware planning, direct cruise booking and making the most of a compact sound gateway.", "independent", breadcrumb="Independent Travellers"),
        "best_time": hero("Seasonal Planning", f"Best Time To Visit<br/><span class=\"{ACCENT}\">Whittier</span>", "Month-by-month tradeoffs for wildlife, weather and tunnel traffic on cruise days.", "best_time", breadcrumb="Best Time To Visit"),
        "schedule": hero("Port Calls", f"Whittier Cruise<br/><span class=\"{ACCENT}\">Ship Schedule</span>", "How to align excursion choices to your date, return windows and transfer needs.", "schedule", breadcrumb="Cruise Schedule"),
        "planner": hero("Plan Your Day", f"Whittier<br/><span class=\"{ACCENT}\">Cruise Planner</span>", "Checklist your priorities and build the right Whittier day plan in minutes.", "planner", breadcrumb="Cruise Planner"),
        "faq": hero("Planning Answers", f"Whittier<br/><span class=\"{ACCENT}\">FAQ</span>", "Quick answers to tunnel timing, sound cruises, transfers and booking questions.", "faq", breadcrumb="FAQ"),
        "enquire": hero("Book and Enquire", f"Enquire About<br/><span class=\"{ACCENT}\">Whittier Tours</span>", "Tell us your cruise timing and we'll recommend best-fit Prince William Sound options.", "enquire", breadcrumb="Enquire"),
    }


def pages_meta() -> list[dict]:
    return [
        dict(slug="", file_content="home.html", title=f"{SITE} | Prince William Sound Glacier & Wildlife Cruises", description="Plan Whittier shore excursions for cruise passengers with independent comparisons across Prince William Sound wildlife cruises, glacier tours and Anchorage transfers.", keywords="Whittier shore excursions, Whittier Alaska cruise excursions, Prince William Sound cruise Whittier", data_page="home", hero="partials/hero-home.html", preload=IMG["home"][0], extra_schema=[website_schema()]),
        dict(slug="best-whittier-shore-excursions", file_content="best-whittier-shore-excursions.html", title="Best Whittier Shore Excursions | Compare 8 Cruise-Day Options", description="Compare the best Whittier shore excursions by timing, activity level, wildlife focus and pre/post-cruise suitability.", keywords="best Whittier shore excursions, Whittier cruise port tours, Whittier excursion comparison", data_page="excursions", hero="partials/hero-best.html", preload=IMG["best"][0]),
        dict(slug="whittier-cruise-port-guide", file_content="whittier-cruise-port-guide.html", title="Whittier Cruise Port Guide | Cruise Passenger Planning", description="Whittier cruise port guide with pier logistics, tunnel timing and excursion fit for Prince William Sound cruise days.", keywords="Whittier cruise port guide, Whittier Alaska cruise port, Whittier port day", data_page="port", hero="partials/hero-port.html", preload=IMG["port"][0]),
        dict(slug="things-to-do-in-whittier-from-a-cruise-ship", file_content="things-to-do-in-whittier-from-a-cruise-ship.html", title="Things to Do in Whittier from a Cruise Ship", description="Sample Whittier cruise-day timeline with practical sequencing for Prince William Sound cruises and return margin.", keywords="things to do Whittier cruise ship, Whittier port day itinerary", data_page="port", hero="partials/hero-things.html", preload=IMG["things"][0]),
        dict(slug="prince-william-sound-guide", file_content="prince-william-sound-guide.html", title="Prince William Sound Guide | Whittier Planning Tips", description="Cruise-passenger guide to choosing and planning Prince William Sound cruises and glacier routes from Whittier.", keywords="Prince William Sound guide, Whittier PWS cruise tips", data_page="pws", hero="partials/hero-pws_guide.html", preload=IMG["pws"][0]),
        dict(slug="whittier-to-anchorage-guide", file_content="whittier-to-anchorage-guide.html", title="Whittier to Anchorage Guide | Transfer & Sightseeing Options", description="Compare transfer-plus-sightseeing options between Whittier and Anchorage for pre/post-cruise travel.", keywords="Whittier to Anchorage transfer, Whittier transfer sightseeing", data_page="port", hero="partials/hero-anchorage_guide.html", preload=IMG["transfer"][0]),
        dict(slug="whittier-vs-seward", file_content="whittier-vs-seward.html", title="Whittier vs Seward Cruise Port | Which is Better?", description="Whittier vs Seward comparison for glacier cruises, wildlife, accessibility, families and photography.", keywords="Whittier vs Seward cruise port, Alaska cruise port comparison", data_page="port", hero="partials/hero-vs_seward.html", preload=IMG["vs_seward"][0]),
        dict(slug="whittier-tunnel-guide", file_content="whittier-tunnel-guide.html", title="Whittier Tunnel Guide | Anton Anderson Memorial Tunnel", description="Anton Anderson Memorial Tunnel guide with timed traffic, rail sharing and cruise passenger travel tips.", keywords="Whittier tunnel guide, Anton Anderson tunnel cruise, Whittier tunnel schedule", data_page="port", hero="partials/hero-tunnel.html", preload=IMG["tunnel"][0]),
        dict(slug="whittier-cruise-planner", file_content="whittier-cruise-planner.html", title="Whittier Cruise Planner | Build Your Port Day", description="Interactive Whittier cruise planner checklist to match Prince William Sound excursions with your priorities.", keywords="Whittier cruise planner, plan Whittier port day", data_page="port", hero="partials/hero-planner.html", preload=IMG["planner"][0], trust=False),
        dict(slug="whittier-faq", file_content="whittier-faq.html", title="Whittier Shore Excursions FAQ | Cruise Planning Answers", description="Whittier shore excursion FAQ with practical answers about tunnel timing, sound cruises, transfers and booking.", keywords="Whittier shore excursions FAQ, Whittier cruise questions", data_page="faq", hero="partials/hero-faq.html", preload=IMG["faq"][0], extra_schema=[faq_schema(FAQ_QA)]),
        dict(slug="enquire", file_content="enquire.html", title="Enquire | Whittier Shore Excursions", description="Enquire about Whittier shore excursions and get recommendations matched to your ship and timing.", keywords="enquire Whittier shore excursions, Whittier tour advice", data_page="excursions", hero="partials/hero-enquire.html", preload=IMG["enquire"][0], trust=False),
        dict(slug="whittier-cruise-ship-schedule", file_content="whittier-cruise-ship-schedule.html", title="Whittier Cruise Ship Schedule | Excursion Timing Guide", description="How to use Whittier cruise schedule timing to choose tours with safer return buffers.", keywords="Whittier cruise ship schedule, Whittier port calls", data_page="port", hero="partials/hero-schedule.html", preload=IMG["schedule"][0]),
        dict(slug="best-time-to-visit-whittier", file_content="best-time-to-visit-whittier.html", title="Best Time to Visit Whittier | Seasonal Cruise Planning", description="Best time to visit Whittier by season, including wildlife, weather and tunnel traffic tradeoffs.", keywords="best time to visit Whittier, Whittier cruise season", data_page="port", hero="partials/hero-best_time.html", preload=IMG["best_time"][0]),
        dict(slug="whittier-wildlife-guide", file_content="whittier-wildlife-guide.html", title="Whittier Wildlife Guide | Prince William Sound Marine Life", description="Whittier wildlife guide for cruise passengers with whale, sea otter and seabird planning tips.", keywords="Whittier wildlife guide, Prince William Sound wildlife cruise passengers", data_page="wildlife", hero="partials/hero-wildlife.html", preload=IMG["wildlife"][0]),
        dict(slug="portage-pass-trail-guide", file_content="portage-pass-trail-guide.html", title="Portage Pass Trail Guide | Hiking Near Whittier", description="Portage Pass Trail guide with alpine views, fitness expectations and timing for Whittier visitors.", keywords="Portage Pass trail Whittier, Portage Pass hike Alaska", data_page="port", hero="partials/hero-portage_pass.html", preload=IMG["portage_pass"][0]),
        dict(slug="begich-towers-and-whittier-history", file_content="begich-towers-and-whittier-history.html", title="Begich Towers & Whittier History | Port Town Guide", description="Begich Towers and Whittier history — WWII port origins, tunnel access and life in Alaska's unique waterfront town.", keywords="Begich Towers Whittier, Whittier Alaska history", data_page="port", hero="partials/hero-begich.html", preload=IMG["begich"][0]),
        dict(slug="whittier-for-independent-travellers", file_content="whittier-for-independent-travellers.html", title="Whittier for Independent Travellers | Self-Planned Sound Access", description="Independent traveller guide to Whittier — tunnel logistics, direct cruise booking and Prince William Sound extensions.", keywords="Whittier independent travel, self plan Whittier Alaska", data_page="port", hero="partials/hero-independent.html", preload=IMG["independent"][0]),
    ]


def main() -> None:
    print(f"Building {SITE} site...")

    write("partials/nav.html", f"""<nav class="fixed top-0 left-0 right-0 z-50 bg-white/90 border-b border-alpine-100 shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-12">
      <a href="/" class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full btn-ocean flex items-center justify-center">
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2C8 2 4 5 4 9c0 5 4 9 8 13 4-4 8-8 8-13 0-4-4-7-8-7z"/></svg>
        </div>
        <span class="font-display font-semibold text-ocean-800 text-base leading-tight">Whittier<br/><span class="text-[10px] font-body font-normal text-teal-600 tracking-widest uppercase">Shore Excursions</span></span>
      </a>
      <div class="hidden lg:flex items-center gap-4 text-sm font-medium">
        <a href="/" data-nav="home" class="text-gray-600 hover:text-ocean-600 transition-colors">Home</a>
        <a href="{u('best-whittier-shore-excursions')}" data-nav="excursions" class="text-gray-600 hover:text-ocean-600 transition-colors">Excursions</a>
        <a href="{u('prince-william-sound-guide')}" data-nav="pws" class="text-gray-600 hover:text-ocean-600 transition-colors">Prince William Sound</a>
        <a href="{u('whittier-cruise-port-guide')}" data-nav="port" class="text-gray-600 hover:text-ocean-600 transition-colors">Port Guide</a>
        <a href="{u('whittier-faq')}" data-nav="faq" class="text-gray-600 hover:text-ocean-600 transition-colors">FAQ</a>
      </div>
      <a href="{u('enquire')}" class="hidden md:inline-flex items-center gap-2 btn-ocean text-white text-sm font-semibold px-4 py-2 rounded-full shadow-md">Enquire</a>
      <button type="button" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-sand-50" aria-label="Open menu">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </div>
</nav>""")

    exc_links = "".join(
        f'<li><a href="{u(s)}" class="hover:text-white transition-colors">{lbl}</a></li>'
        for s, lbl in EXC_NAV.items()
    )
    guide_links = "".join(
        f'<li><a href="{u(slug)}" class="hover:text-white transition-colors">{label}</a></li>'
        for slug, label in [
            ("whittier-cruise-port-guide", "Port Guide"),
            ("things-to-do-in-whittier-from-a-cruise-ship", "Things To Do"),
            ("prince-william-sound-guide", "Prince William Sound Guide"),
            ("whittier-to-anchorage-guide", "Anchorage Guide"),
            ("whittier-vs-seward", "Whittier vs Seward"),
            ("whittier-tunnel-guide", "Tunnel Guide"),
            ("whittier-wildlife-guide", "Wildlife Guide"),
            ("portage-pass-trail-guide", "Portage Pass Trail"),
            ("begich-towers-and-whittier-history", "Begich Towers & History"),
            ("whittier-for-independent-travellers", "Independent Travellers"),
            ("best-time-to-visit-whittier", "Best Time To Visit"),
            ("whittier-cruise-ship-schedule", "Cruise Schedule"),
            ("whittier-cruise-planner", "Cruise Planner"),
            ("whittier-faq", "FAQ"),
            ("enquire", "Enquire"),
        ]
    )
    write("partials/footer.html", f"""<footer class="bg-gray-900 text-gray-400 py-14">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
      <div class="sm:col-span-2 lg:col-span-1">
        <a href="/" class="font-display font-semibold text-white text-lg">{SITE}</a>
        <p class="mt-3 text-sm leading-relaxed">Independent planning guide for cruise visitors to Whittier, Alaska — gateway to Prince William Sound glacier cruises, wildlife and tunnel-aware logistics.</p>
      </div>
      <div>
        <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Excursions</h3>
        <ul class="space-y-2 text-sm">
          <li><a href="{u('best-whittier-shore-excursions')}" class="hover:text-white transition-colors">All Excursions</a></li>
          {exc_links}
        </ul>
      </div>
      <div>
        <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Guides</h3>
        <ul class="space-y-2 text-sm">
          {guide_links}
        </ul>
      </div>
    </div>
    <div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">
      <p>&copy; 2026 {SITE}. Verify timings and prices directly before booking.</p>
    </div>
  </div>
</footer>""")

    write("partials/trust-strip.html", """<section class="trust-strip" aria-label="Whittier shore excursion highlights">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <ul class="trust-strip__list">
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Prince William Sound</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Glacier Cruises</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Wildlife</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Return-To-Ship Confidence</li>
    </ul>
  </div>
</section>""")

    for key, html in heroes().items():
        write(f"partials/hero-{key}.html", html)

    for ex in EXCURSIONS:
        write(
            f"partials/hero-{ex['slug']}.html",
            hero(
                "Whittier Shore Excursion",
                ex["hero_title"],
                ex["hero_lead"],
                ex["image"],
                breadcrumb=ex["label"],
                cta=("enquire", "Enquire about this tour →"),
            ),
        )
        write(f"content/{ex['slug']}.html", excursion_page(ex))

    for name, html in content_map().items():
        write(f"content/{name}", html)

    pages = pages_meta()
    for ex in EXCURSIONS:
        pages.append(
            dict(
                slug=ex["slug"],
                file_content=f"{ex['slug']}.html",
                title=f"{ex['label']} | Whittier Shore Excursion Guide",
                description=meta_desc(ex["intro"]),
                keywords=f"Whittier {ex['slug'].replace('-', ' ')}, Whittier cruise excursion, Prince William Sound tour",
                data_page="excursions",
                hero=f"partials/hero-{ex['slug']}.html",
                preload=IMG[ex["image"]][0],
                extra_schema=[faq_schema(ex["faq"])],
            )
        )

    for p in pages:
        slug = p["slug"]
        name = p["title"].split("|")[0].strip()
        schemas = [breadcrumb_schema(slug, name)] + p.get("extra_schema", [])
        html = page_shell(
            title=p["title"],
            description=p["description"],
            keywords=p["keywords"],
            slug=slug,
            data_page=p["data_page"],
            hero=p["hero"],
            content=p["file_content"],
            preload=p["preload"],
            trust=p.get("trust", True),
        )
        write_page(slug, inject_schemas(html, schemas))

    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    priorities = {
        "": "1.0",
        "best-whittier-shore-excursions": "0.9",
        "whittier-cruise-port-guide": "0.8",
        "prince-william-sound-guide": "0.8",
    }
    for slug in [p["slug"] for p in pages]:
        loc = f"{DOMAIN}/" if not slug else f"{DOMAIN}/{slug}"
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{DATE}</lastmod>",
            "    <changefreq>monthly</changefreq>",
            f"    <priority>{priorities.get(slug, '0.7')}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    write("sitemap.xml", "\n".join(lines) + "\n")

    write("package.json", '{\n  "name": "whittier-shore-excursions",\n  "private": true,\n  "scripts": {\n    "build": "python3 scripts/build-whittier-site.py",\n    "deploy": "wrangler deploy",\n    "preview": "python3 -m http.server 8904"\n  },\n  "devDependencies": {\n    "wrangler": "^4.94.0"\n  }\n}\n')
    write("wrangler.jsonc", '{\n  "$schema": "node_modules/wrangler/config-schema.json",\n  "name": "whittier-shore-excursions",\n  "compatibility_date": "2026-06-24",\n  "observability": { "enabled": true },\n  "assets": {\n    "directory": ".",\n    "html_handling": "auto-trailing-slash"\n  },\n  "routes": [\n    {\n      "pattern": "whittiershoreexcursions.com",\n      "custom_domain": true\n    }\n  ]\n}\n')
    write("deploy.sh", f"#!/bin/bash\nset -euo pipefail\ncd \"$(dirname \"$0\")\"\nif [[ ! -f node_modules/.bin/wrangler ]]; then npm install; fi\necho \"Deploying {SITE} to Cloudflare...\"\nnpx wrangler deploy\necho \"Done. Check {DOMAIN}/ shortly.\"\n")
    (ROOT / "deploy.sh").chmod(0o755)
    write("images/ATTRIBUTION.md", f"# Image attribution\n\nLocal Alaska photography assets for {SITE}.\n")
    print("Done.")


if __name__ == "__main__":
    main()
