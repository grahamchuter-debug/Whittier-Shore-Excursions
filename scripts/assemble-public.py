#!/usr/bin/env python3
"""
Phase 4B: assemble clean public/ site with build-time HTML inlining.
Preserves existing content/partials; remaps RED Seward/Kenai imagery.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public"
DOMAIN = "https://whittiershoreexcursions.com"
SITE = "Whittier Shore Excursions"
EMAIL = "hello@whittiershoreexcursions.com"
DATE = "2026-09-16"

# RED / contaminated → verified Whittier-unique assets + honest alts
IMAGE_REMAP: dict[str, tuple[str, str]] = {
    "/images/prince-william-sound.png": (
        "/images/blackstone-bay.png",
        "Glacier scenery in Prince William Sound near Whittier, Alaska",
    ),
    "/images/pws-glacier.png": (
        "/images/blackstone-bay.png",
        "Glacier scenery in Prince William Sound near Whittier, Alaska",
    ),
    "/images/intro.png": (
        "/images/hero-whittier.png",
        "Coastal scenery near Whittier, Alaska and Prince William Sound",
    ),
    "/images/portage-glacier.png": (
        "/images/hero-whittier.png",
        "Mountain and water scenery near Whittier and the Portage corridor, Alaska",
    ),
    "/images/enquire.png": (
        "/images/hero-whittier.png",
        "Whittier, Alaska scenery — enquire about shore excursions",
    ),
    "/images/planner.png": (
        "/images/hero-whittier.png",
        "Whittier, Alaska scenery for cruise day planning",
    ),
    "/images/vs-seward.png": (
        "/images/hero-whittier.png",
        "Whittier, Alaska coastal scenery for cruise port comparison",
    ),
    "/images/schedule.png": (
        "/images/whittier-port.png",
        "Cruise activity near Whittier, Alaska for schedule planning",
    ),
    "/images/faq.png": (
        "/images/hero-whittier.png",
        "Whittier, Alaska scenery for shore excursion planning questions",
    ),
    "/images/tunnel.png": (
        "/images/glacier-train.png",
        "Transport corridor scenery near Whittier, Alaska",
    ),
    "/images/anchorage-transfer.png": (
        "/images/glacier-train.png",
        "Scenic travel corridor between Whittier and Anchorage, Alaska",
    ),
    "/images/whittier-scenic.png": (
        "/images/hero-whittier.png",
        "Scenic views near Whittier, Alaska",
    ),
    "/images/begich-towers.png": (
        "/images/hero-whittier.png",
        "Whittier, Alaska waterfront setting",
    ),
    "/images/best-whittier-excursions.png": (
        "/images/spencer-glacier.png",
        "Spencer Glacier area near Whittier — popular shore excursion theme",
    ),
    "/images/independent.png": (
        "/images/hero-whittier.png",
        "Whittier, Alaska for independent travellers",
    ),
    "/images/portage-pass.png": (
        "/images/spencer-glacier.png",
        "Alpine glacier scenery near the Portage–Whittier corridor, Alaska",
    ),
    "/images/best-time.png": (
        "/images/blackstone-bay.png",
        "Seasonal glacier scenery near Whittier in Prince William Sound",
    ),
    "/images/things.png": (
        "/images/whittier-port.png",
        "Whittier cruise port area for things to do ashore",
    ),
}

OK_IMAGES = {
    "hero-whittier.png",
    "spencer-glacier.png",
    "blackstone-bay.png",
    "glacier-train.png",
    "cruise-snapshot.png",
    "whittier-port.png",
    "pws-wildlife.png",
    "wildlife.png",
    "ATTRIBUTION.md",
}

# Title/meta CTR pass only — no slug or intent changes
CTR: dict[str, tuple[str, str]] = {
    "": (
        "Whittier Shore Excursions | Prince William Sound & Cruise Port",
        "Plan Whittier shore excursions — Prince William Sound glacier and wildlife cruises, Spencer Glacier float, tunnel logistics and Anchorage transfers.",
    ),
    "spencer-glacier-float": (
        "Spencer Glacier Float | Whittier Shore Excursion Guide",
        "Spencer Glacier float near Whittier — rail corridor access, glacier views and cruise-day timing tips for Prince William Sound visitors.",
    ),
    "whittier-tunnel-guide": (
        "Whittier Tunnel Guide | Anton Anderson Memorial Tunnel",
        "Anton Anderson Memorial Tunnel guide for Whittier cruise passengers — timed traffic, rail sharing and port-day travel tips.",
    ),
    "prince-william-sound-guide": (
        "Prince William Sound Guide | From Whittier Cruise Port",
        "Cruise-passenger guide to Prince William Sound from Whittier — glacier routes, wildlife cruises and how to choose a port-day boat trip.",
    ),
    "prince-william-sound-glacier-cruise": (
        "Prince William Sound Glacier Cruise | From Whittier",
        "Tidewater glacier cruises from Whittier into Prince William Sound — timing, what to expect and cruise-day return buffers.",
    ),
    "prince-william-sound-wildlife-cruise": (
        "Prince William Sound Wildlife Cruise | From Whittier",
        "Wildlife cruises from Whittier on Prince William Sound — whales, otters, seabirds and fjord scenery for cruise passengers.",
    ),
    "anchorage-transfer-with-sightseeing": (
        "Anchorage Transfer with Sightseeing | From Whittier",
        "Whittier to Anchorage transfer with sightseeing — Portage corridor options, timing and pre/post-cruise planning tips.",
    ),
    "whittier-to-anchorage-guide": (
        "Whittier to Anchorage Guide | Transfer & Sightseeing",
        "Compare Whittier–Anchorage transfer and sightseeing options for cruise passengers and independent travellers.",
    ),
    "whittier-cruise-ship-schedule": (
        "Whittier Cruise Ship Schedule | Port Timing Guide",
        "How Whittier cruise call timing works for shore excursions — typical hours ashore and how to plan safer return buffers.",
    ),
    "whittier-cruise-port-guide": (
        "Whittier Cruise Port Guide | Pier, Tunnel & Port Day",
        "Whittier cruise port guide — pier logistics, Anton Anderson Tunnel timing and Prince William Sound excursion fit.",
    ),
    "best-time-to-visit-whittier": (
        "Best Time to Visit Whittier | Cruise Season Planning",
        "Best time to visit Whittier, Alaska for cruise passengers — wildlife, weather and tunnel traffic tradeoffs.",
    ),
    "whittier-vs-seward": (
        "Whittier vs Seward | Which Alaska Cruise Port Fits You?",
        "Whittier vs Seward for cruise passengers — Prince William Sound access versus Kenai Fjords, tunnel logistics and tour styles.",
    ),
    "enquire": (
        "Enquire About Whittier Shore Excursions",
        "Enquire about Whittier shore excursions — share your ship, date and interests. Enquiry-only planning help, no online checkout.",
    ),
}

PAGES: list[dict] = [
    {"slug": "", "content": "home.html", "hero": "hero-home.html", "data_page": "home", "name": "Home", "trust": True},
    {"slug": "best-whittier-shore-excursions", "content": "best-whittier-shore-excursions.html", "hero": "hero-best.html", "data_page": "excursions", "name": "Best Excursions", "trust": True},
    {"slug": "whittier-cruise-port-guide", "content": "whittier-cruise-port-guide.html", "hero": "hero-port.html", "data_page": "port", "name": "Port Guide", "trust": True},
    {"slug": "things-to-do-in-whittier-from-a-cruise-ship", "content": "things-to-do-in-whittier-from-a-cruise-ship.html", "hero": "hero-things.html", "data_page": "port", "name": "Things To Do", "trust": True},
    {"slug": "prince-william-sound-guide", "content": "prince-william-sound-guide.html", "hero": "hero-pws_guide.html", "data_page": "pws", "name": "Prince William Sound Guide", "trust": True},
    {"slug": "whittier-to-anchorage-guide", "content": "whittier-to-anchorage-guide.html", "hero": "hero-anchorage_guide.html", "data_page": "port", "name": "Anchorage Guide", "trust": True},
    {"slug": "whittier-vs-seward", "content": "whittier-vs-seward.html", "hero": "hero-vs_seward.html", "data_page": "port", "name": "Whittier vs Seward", "trust": True},
    {"slug": "whittier-tunnel-guide", "content": "whittier-tunnel-guide.html", "hero": "hero-tunnel.html", "data_page": "port", "name": "Tunnel Guide", "trust": True},
    {"slug": "whittier-cruise-planner", "content": "whittier-cruise-planner.html", "hero": "hero-planner.html", "data_page": "port", "name": "Cruise Planner", "trust": False},
    {"slug": "whittier-faq", "content": "whittier-faq.html", "hero": "hero-faq.html", "data_page": "faq", "name": "FAQ", "trust": True},
    {"slug": "enquire", "content": "enquire.html", "hero": "hero-enquire.html", "data_page": "excursions", "name": "Enquire", "trust": False},
    {"slug": "whittier-cruise-ship-schedule", "content": "whittier-cruise-ship-schedule.html", "hero": "hero-schedule.html", "data_page": "port", "name": "Cruise Schedule", "trust": True},
    {"slug": "best-time-to-visit-whittier", "content": "best-time-to-visit-whittier.html", "hero": "hero-best_time.html", "data_page": "port", "name": "Best Time To Visit", "trust": True},
    {"slug": "whittier-wildlife-guide", "content": "whittier-wildlife-guide.html", "hero": "hero-wildlife.html", "data_page": "wildlife", "name": "Wildlife Guide", "trust": True},
    {"slug": "portage-pass-trail-guide", "content": "portage-pass-trail-guide.html", "hero": "hero-portage_pass.html", "data_page": "port", "name": "Portage Pass Trail", "trust": True},
    {"slug": "begich-towers-and-whittier-history", "content": "begich-towers-and-whittier-history.html", "hero": "hero-begich.html", "data_page": "port", "name": "Begich Towers & History", "trust": True},
    {"slug": "whittier-for-independent-travellers", "content": "whittier-for-independent-travellers.html", "hero": "hero-independent.html", "data_page": "port", "name": "Independent Travellers", "trust": True},
    {"slug": "prince-william-sound-wildlife-cruise", "content": "prince-william-sound-wildlife-cruise.html", "hero": "hero-prince-william-sound-wildlife-cruise.html", "data_page": "excursions", "name": "PWS Wildlife Cruise", "trust": True},
    {"slug": "prince-william-sound-glacier-cruise", "content": "prince-william-sound-glacier-cruise.html", "hero": "hero-prince-william-sound-glacier-cruise.html", "data_page": "excursions", "name": "PWS Glacier Cruise", "trust": True},
    {"slug": "spencer-glacier-float", "content": "spencer-glacier-float.html", "hero": "hero-spencer-glacier-float.html", "data_page": "excursions", "name": "Spencer Glacier Float", "trust": True},
    {"slug": "blackstone-bay-cruise", "content": "blackstone-bay-cruise.html", "hero": "hero-blackstone-bay-cruise.html", "data_page": "excursions", "name": "Blackstone Bay Cruise", "trust": True},
    {"slug": "whittier-scenic-tour", "content": "whittier-scenic-tour.html", "hero": "hero-whittier-scenic-tour.html", "data_page": "excursions", "name": "Whittier Scenic Tour", "trust": True},
    {"slug": "anchorage-transfer-with-sightseeing", "content": "anchorage-transfer-with-sightseeing.html", "hero": "hero-anchorage-transfer-with-sightseeing.html", "data_page": "excursions", "name": "Anchorage Transfer", "trust": True},
    {"slug": "glacier-discovery-train", "content": "glacier-discovery-train.html", "hero": "hero-glacier-discovery-train.html", "data_page": "excursions", "name": "Glacier Discovery Train", "trust": True},
    {"slug": "portage-glacier-tour", "content": "portage-glacier-tour.html", "hero": "hero-portage-glacier-tour.html", "data_page": "excursions", "name": "Portage Glacier Tour", "trust": True},
]


def slash(slug: str) -> str:
    return "/" if not slug else f"/{slug}/"


def canon(slug: str) -> str:
    return DOMAIN + ("/" if not slug else f"/{slug}/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def remap_images(html: str) -> str:
    for old, (new, alt) in IMAGE_REMAP.items():
        if old not in html:
            continue
        html = html.replace(f"url('{old}')", f"url('{new}')")
        html = html.replace(f'url("{old}")', f'url("{new}")')
        html = html.replace(f"url({old})", f"url({new})")
        html = html.replace(f'src="{old}"', f'src="{new}"')
        html = html.replace(f"src='{old}'", f"src='{new}'")
        html = re.sub(
            rf'(url\([\'"]?{re.escape(new)}[\'"]?\)[^>]*)aria-label="[^"]*"',
            rf'\1aria-label="{alt}"',
            html,
            count=1,
        )
        html = re.sub(
            rf'(src="{re.escape(new)}"[^>]*alt=")[^"]*(")',
            rf"\1{alt}\2",
            html,
        )
        html = re.sub(
            rf'(alt=")[^"]*("[^>]*src="{re.escape(new)}")',
            rf"\1{alt}\2",
            html,
        )
    return html


def fix_internal_links(html: str) -> str:
    slugs = [p["slug"] for p in PAGES if p["slug"]]

    def repl(m: re.Match[str]) -> str:
        quote = m.group(1)
        path = m.group(2)
        if any(path.startswith(ext) for ext in ("/images/", "/css/", "/js/", "/fonts/")):
            return m.group(0)
        if path in ("/", ""):
            return f"href={quote}/{quote}"
        clean = path
        if clean.endswith(".html"):
            clean = clean[:-5]
        clean = clean.rstrip("/")
        leaf = clean.lstrip("/")
        if leaf in slugs:
            return f"href={quote}/{leaf}/{quote}"
        return m.group(0)

    return re.sub(r'href=(["\'])(/[^"\']*)\1', repl, html)


def extract_head_field(shell: str, name: str) -> str | None:
    m = re.search(
        rf'<meta[^>]+name=["\']{name}["\'][^>]+content=["\']([^"\']*)["\']',
        shell,
        re.I,
    )
    if m:
        return m.group(1)
    m = re.search(
        rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']{name}["\']',
        shell,
        re.I,
    )
    return m.group(1) if m else None


def extract_title(shell: str) -> str:
    m = re.search(r"<title>(.*?)</title>", shell, re.I | re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else SITE


def extract_og_image(shell: str) -> str:
    m = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        shell,
        re.I,
    )
    if m:
        return m.group(1)
    m = re.search(r'<link[^>]+rel=["\']preload["\'][^>]+href=["\']([^"\']+)["\']', shell, re.I)
    return m.group(1) if m else "/images/hero-whittier.png"


def extract_jsonld(shell: str) -> list[dict]:
    blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>',
        shell,
        re.I,
    )
    out: list[dict] = []
    for b in blocks:
        try:
            data = json.loads(b)
            if isinstance(data, list):
                out.extend(data)
            else:
                out.append(data)
        except json.JSONDecodeError:
            pass
    return out


def organization_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE,
        "url": f"{DOMAIN}/",
        "email": EMAIL,
        "description": "Independent Whittier Alaska shore excursion planning guide for cruise passengers — Prince William Sound focus.",
        "areaServed": {"@type": "Place", "name": "Whittier, Alaska"},
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer enquiry",
            "email": EMAIL,
            "url": f"{DOMAIN}/enquire/",
        },
    }


def website_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE,
        "url": f"{DOMAIN}/",
        "description": "Independent Whittier Alaska shore excursion planning guide",
    }


def webpage_schema(title: str, description: str, slug: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": canon(slug),
        "isPartOf": {"@type": "WebSite", "name": SITE, "url": f"{DOMAIN}/"},
    }


def breadcrumb_schema(slug: str, name: str) -> dict:
    items = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": f"{DOMAIN}/",
        }
    ]
    if slug:
        items.append(
            {
                "@type": "ListItem",
                "position": 2,
                "name": name,
                "item": canon(slug),
            }
        )
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def set_active_nav(nav: str, data_page: str) -> str:
    def repl(m: re.Match[str]) -> str:
        full = m.group(0)
        nav_key = m.group(1)
        if nav_key == data_page:
            full = re.sub(
                r'class="([^"]*)"',
                r'class="\1 text-ocean-600 font-semibold"',
                full,
                count=1,
            )
            if "aria-current" not in full:
                full = full.replace(">", ' aria-current="page">', 1)
        return full

    return re.sub(r'<a[^>]+data-nav="([^"]+)"[^>]*>', repl, nav)


def clean_enquire_hero(hero: str) -> str:
    hero = hero.replace("Book &amp; Enquire", "Enquire")
    hero = hero.replace("Book & Enquire", "Enquire")
    return hero


def fix_stale_emails(html: str) -> str:
    return html.replace("enquiries@whittiershoreexcursions.com", EMAIL)


def assemble_page(page: dict) -> str:
    slug = page["slug"]
    shell_path = ROOT / ("index.html" if not slug else f"{slug}/index.html")
    shell = read(shell_path)

    title = extract_title(shell)
    description = extract_head_field(shell, "description") or ""
    keywords = extract_head_field(shell, "keywords") or ""
    if slug in CTR:
        title, description = CTR[slug]

    og_image = extract_og_image(shell)
    for old, (new, _) in IMAGE_REMAP.items():
        if old in og_image or old.lstrip("/") in og_image:
            og_image = DOMAIN + new
            break
    if og_image.startswith("/"):
        og_image = DOMAIN + og_image

    preload = extract_og_image(shell)
    if preload.startswith("http"):
        preload = preload.replace(DOMAIN, "")
    for old, (new, _) in IMAGE_REMAP.items():
        if old in preload:
            preload = new
            break
    if preload.startswith("http"):
        preload = "/" + preload.split("/images/", 1)[-1]
        preload = "/images/" + preload if not preload.startswith("/images/") else preload

    nav = fix_internal_links(remap_images(read(ROOT / "partials/nav.html")))
    nav = set_active_nav(nav, page["data_page"])
    footer = fix_internal_links(remap_images(read(ROOT / "partials/footer.html")))
    footer = fix_stale_emails(footer)
    if EMAIL not in footer:
        footer = footer.replace(
            '<div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">',
            f'<div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">\n'
            f'      <p>Planning questions: <a href="mailto:{EMAIL}" class="text-white hover:underline">{EMAIL}</a>. '
            f"We reply when we can — not a 24/7 desk.</p>",
            1,
        )

    hero = fix_internal_links(remap_images(read(ROOT / "partials" / page["hero"])))
    if slug == "enquire":
        hero = clean_enquire_hero(hero)
    content = fix_stale_emails(
        fix_internal_links(remap_images(read(ROOT / "content" / page["content"])))
    )
    trust = ""
    if page.get("trust"):
        trust = fix_internal_links(
            remap_images(read(ROOT / "partials/trust-strip.html"))
        )

    schemas = extract_jsonld(shell)
    schemas = [
        s
        for s in schemas
        if s.get("@type") not in ("Product", "Offer")
        and "InStock" not in json.dumps(s)
    ]
    # Fix stale emails inside any retained schema
    schemas = json.loads(fix_stale_emails(json.dumps(schemas)))

    types = {s.get("@type") for s in schemas}
    if "Organization" not in types:
        schemas.insert(0, organization_schema())
    else:
        for s in schemas:
            if s.get("@type") == "Organization":
                s["email"] = EMAIL
                s.setdefault(
                    "contactPoint",
                    {
                        "@type": "ContactPoint",
                        "contactType": "customer enquiry",
                        "email": EMAIL,
                        "url": f"{DOMAIN}/enquire/",
                    },
                )
                if isinstance(s.get("contactPoint"), dict):
                    s["contactPoint"]["email"] = EMAIL
    if "WebSite" not in types:
        schemas.insert(0, website_schema())
    # Nested publisher Organization email
    for s in schemas:
        if s.get("@type") == "WebSite":
            s["url"] = f"{DOMAIN}/"
            pub = s.get("publisher")
            if isinstance(pub, dict):
                pub["email"] = EMAIL
                pub["url"] = f"{DOMAIN}/"
            elif "Organization" not in types:
                pass
    if "WebPage" not in types:
        schemas.append(webpage_schema(title, description, slug))
    if "BreadcrumbList" not in types:
        schemas.append(breadcrumb_schema(slug, page["name"]))
    for s in schemas:
        if s.get("@type") == "WebPage":
            s["url"] = canon(slug)
            s["name"] = title
            s["description"] = description
        if s.get("@type") == "BreadcrumbList":
            for item in s.get("itemListElement", []):
                if item.get("position") == 1:
                    item["item"] = f"{DOMAIN}/"
                elif item.get("position") == 2 and slug:
                    item["item"] = canon(slug)
                    item["name"] = page["name"]
        if s.get("@type") == "FAQPage":
            # keep genuine FAQ; ensure no product offers
            pass

    # Prefer standalone Organization when only nested under WebSite
    if "Organization" not in {s.get("@type") for s in schemas}:
        schemas.insert(0, organization_schema())

    schema_html = "".join(
        f'  <script type="application/ld+json">\n{json.dumps(s, indent=2)}\n  </script>\n'
        for s in schemas
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canon(slug)}" />
  <link rel="preload" as="image" href="{preload}" fetchpriority="high" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canon(slug)}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{og_image}" />
  <meta property="og:site_name" content="{SITE}" />
  <meta name="twitter:card" content="summary_large_image" />
{schema_html}  <script src="https://cdn.tailwindcss.com"></script>
  <script src="/js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;600;700&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
<body class="bg-white text-gray-800 antialiased" data-page="{page["data_page"]}">
{nav}
{hero}
{trust}
<main id="page-content">
{content}
</main>
{footer}
</body>
</html>
"""


def write_404() -> None:
    nav = fix_internal_links(read(ROOT / "partials/nav.html"))
    footer = fix_stale_emails(fix_internal_links(read(ROOT / "partials/footer.html")))
    if EMAIL not in footer:
        footer = footer.replace(
            '<div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">',
            f'<div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">\n'
            f'      <p>Planning questions: <a href="mailto:{EMAIL}" class="text-white hover:underline">{EMAIL}</a>.</p>',
            1,
        )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Page not found | {SITE}</title>
  <meta name="robots" content="noindex,follow" />
  <meta name="description" content="This page was not found on Whittier Shore Excursions." />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="/js/tailwind-config.js"></script>
  <link rel="stylesheet" href="/css/site.css" />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;600;700&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
</head>
<body class="bg-white text-gray-800 antialiased">
{nav}
<main class="max-w-3xl mx-auto px-4 py-24 text-center">
  <h1 class="text-4xl font-display font-bold text-gray-900 mb-4">Page not found</h1>
  <p class="text-gray-600 mb-8">This page does not exist on Whittier Shore Excursions. Try one of these guides instead.</p>
  <div class="flex flex-wrap justify-center gap-3 text-sm">
    <a href="/" class="btn-ocean text-white font-semibold px-5 py-2.5 rounded-full">Homepage</a>
    <a href="/spencer-glacier-float/" class="border border-slate-300 font-semibold px-5 py-2.5 rounded-full">Spencer Glacier Float</a>
    <a href="/prince-william-sound-guide/" class="border border-slate-300 font-semibold px-5 py-2.5 rounded-full">Prince William Sound</a>
    <a href="/whittier-cruise-port-guide/" class="border border-slate-300 font-semibold px-5 py-2.5 rounded-full">Port Guide</a>
    <a href="/whittier-cruise-ship-schedule/" class="border border-slate-300 font-semibold px-5 py-2.5 rounded-full">Cruise Schedule</a>
    <a href="/enquire/" class="border border-slate-300 font-semibold px-5 py-2.5 rounded-full">Enquire</a>
  </div>
  <p class="mt-10 text-sm text-gray-500">Questions: <a class="text-ocean-600 underline" href="mailto:{EMAIL}">{EMAIL}</a></p>
</main>
{footer}
</body>
</html>
"""
    (OUT / "404.html").write_text(html, encoding="utf-8")


def write_sitemap() -> None:
    urls = []
    for p in PAGES:
        loc = canon(p["slug"])
        priority = "1.0" if not p["slug"] else "0.8"
        if p["slug"] in ("spencer-glacier-float", "whittier-cruise-ship-schedule"):
            priority = "0.9"
        urls.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{DATE}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>"""
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (OUT / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_robots() -> None:
    (OUT / "robots.txt").write_text(
        f"User-Agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n",
        encoding="utf-8",
    )


def copy_assets() -> None:
    css_dst = OUT / "css"
    css_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "css/site.css", css_dst / "site.css")

    js_dst = OUT / "js"
    js_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "js/tailwind-config.js", js_dst / "tailwind-config.js")
    # Do NOT copy site.js — no client content fetch

    img_dst = OUT / "images"
    img_dst.mkdir(parents=True, exist_ok=True)
    for name in OK_IMAGES:
        src = ROOT / "images" / name
        if src.exists():
            shutil.copy2(src, img_dst / name)
    (img_dst / "ATTRIBUTION.md").write_text(
        "# Image attribution\n\n"
        "Verified Whittier / Prince William Sound photography assets only. "
        "Seward, Kenai Fjords, Exit Glacier and shared multi-destination cruise-ship "
        "placeholders were removed in World 2.0 Phase 4B.\n",
        encoding="utf-8",
    )


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    print("Assembling Whittier public/ (build-time HTML inlining)…")
    for page in PAGES:
        html = assemble_page(page)
        if page["slug"]:
            dest = OUT / page["slug"] / "index.html"
            dest.parent.mkdir(parents=True, exist_ok=True)
        else:
            dest = OUT / "index.html"
        dest.write_text(html, encoding="utf-8")
        print(f"  wrote {dest.relative_to(OUT)}")

    write_404()
    write_sitemap()
    write_robots()
    copy_assets()
    print(f"Done. Output: {OUT}")


if __name__ == "__main__":
    main()
