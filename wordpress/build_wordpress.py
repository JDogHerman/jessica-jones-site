#!/usr/bin/env python3
"""
Build the WordPress version of the site from content.json.

Writes two files next to this script:
  jessica-jones-content.xml   WordPress import file (Tools > Import > WordPress)
  jessica-jones-theme.zip     the theme (Appearance > Themes > Add New > Upload)

Run from anywhere:  python3 wordpress/build_wordpress.py
"""
import html
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# Images are fetched from the live GitHub Pages site during import.
IMAGE_BASE = "https://jdogherman.github.io/jessica-jones-site/"

PLACEHOLDER = '<mark style="background-color:#fff4d6" class="has-inline-color">[{}]</mark>'

# Internal links on the static site -> WordPress page slugs (relative to the home page)
LINKS = {
    "index.html": "./", "poems.html": "poems/", "books.html": "books/",
    "teaching.html": "teaching/", "residencies.html": "residencies/",
    "photography.html": "photography/", "bio.html": "bio/",
    "events.html": "events/", "contact.html": "contact/",
}


# ---------------------------------------------------------------- text helpers
def is_blank(s):
    if s is None:
        return True
    t = str(s).strip()
    return t == "" or bool(re.fullmatch(r"\[[^\]]*\]", t))


def fmt(s):
    """Escape text, then *italic* -> <em>, [placeholder] -> highlighted mark."""
    t = html.escape(str(s or ""), quote=False)
    t = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]", lambda m: PLACEHOLDER.format(m.group(1)), t)
    return t


def attr(s):
    return html.escape(str(s or ""), quote=True)


def href(url):
    if url in LINKS:
        return LINKS[url]
    m = re.match(r"([a-z]+\.html)(#.*)?$", url or "")
    if m and m.group(1) in LINKS:
        return LINKS[m.group(1)] + (m.group(2) or "")
    return url


def link(inner, url):
    return inner if is_blank(url) else f'<a href="{attr(href(url))}">{inner}</a>'


def img_url(src):
    return src if re.match(r"https?://", src) else IMAGE_BASE + src


def meta(parts):
    return " · ".join(fmt(p) for p in parts if p and str(p).strip())


def j(d):
    return json.dumps(d, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------- block helpers
def p(inner, cls=None):
    if cls:
        return f'<!-- wp:paragraph {j({"className": cls})} -->\n<p class="{cls}">{inner}</p>\n<!-- /wp:paragraph -->'
    return f"<!-- wp:paragraph -->\n<p>{inner}</p>\n<!-- /wp:paragraph -->"


def h(inner, level=2, cls=None, anchor=None):
    a = {}
    if level != 2:
        a["level"] = level
    if anchor:
        a["anchor"] = anchor
    if cls:
        a["className"] = cls
    comment = f"<!-- wp:heading {j(a)} -->" if a else "<!-- wp:heading -->"
    classes = "wp-block-heading" + (f" {cls}" if cls else "")
    id_attr = f' id="{anchor}"' if anchor else ""
    return f'{comment}\n<h{level} class="{classes}"{id_attr}>{inner}</h{level}>\n<!-- /wp:heading -->'


def ul(items):
    lis = "\n\n".join(f"<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->" for i in items)
    return f'<!-- wp:list -->\n<ul class="wp-block-list">{lis}</ul>\n<!-- /wp:list -->'


def quote(paragraphs, cite=None, cls=None):
    a = j({"className": cls}) + " " if cls else ""
    classes = "wp-block-quote" + (f" {cls}" if cls else "")
    inner = "\n\n".join(p(x) for x in paragraphs)
    c = f"<cite>{cite}</cite>" if cite else ""
    return f'<!-- wp:quote {a}-->\n<blockquote class="{classes}">{inner}{c}</blockquote>\n<!-- /wp:quote -->'


def image(src, alt, cls=None, caption=None):
    a = {"linkDestination": "none"}
    if cls:
        a["className"] = cls
    classes = "wp-block-image" + (f" {cls}" if cls else "")
    cap = f'<figcaption class="wp-element-caption">{caption}</figcaption>' if caption else ""
    return (f"<!-- wp:image {j(a)} -->\n<figure class=\"{classes}\"><img src=\"{attr(img_url(src))}\" "
            f"alt=\"{attr('' if is_blank(alt) else alt)}\"/>{cap}</figure>\n<!-- /wp:image -->")


def columns(cols, wide=False):
    """cols: list of (inner_blocks_list, width or None)."""
    a = {"align": "wide"} if wide else {}
    comment = f"<!-- wp:columns {j(a)} -->" if a else "<!-- wp:columns -->"
    classes = "wp-block-columns" + (" alignwide" if wide else "")
    out = []
    for blocks, width in cols:
        if width:
            out.append(f'<!-- wp:column {j({"width": width})} -->\n<div class="wp-block-column" style="flex-basis:{width}">'
                       + "\n\n".join(blocks) + "</div>\n<!-- /wp:column -->")
        else:
            out.append('<!-- wp:column -->\n<div class="wp-block-column">' + "\n\n".join(blocks) + "</div>\n<!-- /wp:column -->")
    return f'{comment}\n<div class="{classes}">' + "\n\n".join(out) + "</div>\n<!-- /wp:columns -->"


def group(blocks, cls):
    return (f'<!-- wp:group {j({"className": cls, "layout": {"type": "default"}})} -->\n<div class="wp-block-group {cls}">'
            + "\n\n".join(blocks) + "</div>\n<!-- /wp:group -->")


def buttons(items):
    """items: list of (label_html, url, outline)"""
    bs = []
    for label, url, outline in items:
        if is_blank(url):
            continue
        if outline:
            bs.append('<!-- wp:button {"className":"is-style-outline"} -->\n<div class="wp-block-button is-style-outline">'
                      f'<a class="wp-block-button__link wp-element-button" href="{attr(url)}">{label}</a></div>\n<!-- /wp:button -->')
        else:
            bs.append('<!-- wp:button -->\n<div class="wp-block-button">'
                      f'<a class="wp-block-button__link wp-element-button" href="{attr(url)}">{label}</a></div>\n<!-- /wp:button -->')
    if not bs:
        return ""
    return '<!-- wp:buttons -->\n<div class="wp-block-buttons">' + "\n\n".join(bs) + "</div>\n<!-- /wp:buttons -->"


def separator():
    return '<!-- wp:separator -->\n<hr class="wp-block-separator has-alpha-channel-opacity"/>\n<!-- /wp:separator -->'


def verse(text):
    return f'<!-- wp:verse -->\n<pre class="wp-block-verse">{html.escape(text, quote=False)}</pre>\n<!-- /wp:verse -->'


def more(label, url):
    return p(f'<a href="{attr(href(url))}">{fmt(label)} →</a>')


def join(blocks):
    return "\n\n".join(b for b in blocks if b)


# ---------------------------------------------------------------- pages
def page_home(c):
    s, hm = c["site"], c["home"]
    out = [columns([
        ([h(fmt(s["name"]), 1, "jj-hero-name"), p(fmt(s["tagline"]), "jj-tagline"), p(fmt(s["title"]), "jj-meta")], "60%"),
        ([image(s["headshot"]["src"], s["headshot"]["alt"], "jj-headshot")], "40%"),
    ], wide=True)]
    out += [p(fmt(x)) for x in hm["intro"]]
    if hm.get("quote") and not is_blank(hm["quote"]["text"]):
        out.append(quote([fmt(hm["quote"]["text"])], fmt(hm["quote"]["attribution"]), "jj-pull"))
    if c.get("praise"):
        out.append(h("Praise"))
        out += [quote([fmt(q["text"])], fmt(q["source"])) for q in c["praise"]]
    if hm.get("featured"):
        out.append(h("Featured work"))
        cols = []
        for f in hm["featured"]:
            blocks = []
            if f.get("image"):
                blocks.append(image(f["image"]["src"], f["image"]["alt"], "jj-cover"))
            blocks += [p(fmt(f["kind"]), "jj-eyebrow"), h(f"<em>{fmt(f['title'])}</em>", 3),
                       p(fmt(f["detail"])), more(f["linkLabel"], f["href"])]
            cols.append(([group(blocks, "jj-card")], None))
        out.append(columns(cols, wide=True))
    t = hm.get("photoTeaser")
    if t:
        photo = next((x for x in c["photography"]["photos"] if x["id"] == t["photo"]), None)
        out.append(h(fmt(t["heading"])))
        left = [image(photo["src"], photo["alt"], "jj-photo", f"<em>{fmt(photo['title'])}</em>")] if photo else []
        out.append(columns([(left, None), ([p(fmt(t["text"])), more("View the photographs", "photography.html")], None)]))
    if hm.get("explore"):
        out.append(h("Explore"))
        out.append(ul([f'<a href="{attr(href(e["href"]))}">{fmt(e["label"])}</a> — {fmt(e["blurb"])}' for e in hm["explore"]]))
    return join(out)


def page_poems(c):
    pm = c["poems"]
    out = [p(fmt(pm["intro"]))]
    fps = pm.get("featuredPoems") or []
    if fps:
        out.append(h("Featured poems" if len(fps) > 1 else "Featured poem"))
        for fp in fps:
            out.append(h(fmt(fp["title"]), 3))
            if fp.get("place"):
                out.append(p(fmt(fp["place"]), "jj-meta"))
            out.append(verse(fp["text"]))
            if fp.get("credit"):
                out.append(p(link(fmt(fp["credit"]), fp.get("creditUrl")), "jj-meta"))
    for g in pm["groups"]:
        out.append(h(fmt(g["heading"])))
        if g.get("note"):
            out.append(p(fmt(g["note"])))
        items = []
        for it in g["items"]:
            line = link(fmt(it["title"]), it.get("url"))
            m = meta([it.get("venue"), it.get("year")])
            if m:
                line += f"<br>{m}"
            items.append(line)
        out.append(ul(items))
    return join(out)


def anthology_title(a):
    t = f"<em>{fmt(a['title'])}" + (f": {fmt(a['subtitle'])}" if a.get("subtitle") else "") + "</em>"
    return link(t, a.get("url"))


def page_books(c):
    bk = c["books"]
    out = []
    ed = bk.get("edited")
    if ed and ed.get("items"):
        out.append(h(fmt(ed["heading"]), anchor="edited"))
        for x in ed["items"]:
            info = []
            if x.get("status"):
                info.append(p(fmt(x["status"]), "jj-eyebrow"))
            info += [h(f"<em>{fmt(x['title'])}" + (f": {fmt(x['subtitle'])}" if x.get("subtitle") else "") + "</em>", 3),
                     p(fmt(x["role"])), p(meta([x["publisher"], x["date"]]), "jj-meta")]
            if x.get("quote"):
                info.append(quote([fmt(q) for q in x["quote"]["paragraphs"]], "— " + fmt(x["quote"]["source"])))
            info.append(buttons([(fmt(x.get("buyLabel") or "Buy the book"), x.get("buyUrl"), False),
                                 (fmt(x.get("linkLabel") or "Learn more"), x.get("url"), True)]))
            out.append(columns([([image(x["cover"]["src"], x["cover"]["alt"], "jj-cover")], "30%"), ([b for b in info if b], "70%")]))
        out.append(separator())
    b = bk["chapbook"]
    info = [p(fmt(b["kind"]), "jj-eyebrow"), h(f"<em>{fmt(b['title'])}</em>", 3),
            p(meta([b["publisher"], b["year"]]), "jj-meta"), p(fmt(b["description"]))]
    if is_blank(b.get("buyUrl")):
        info.append(p(fmt(b["buyLabel"])))
    else:
        info.append(buttons([(f"Buy <em>{fmt(b['title'])}</em>", b["buyUrl"], False)]))
    out.append(columns([([image(b["cover"]["src"], b["cover"]["alt"], "jj-cover")], "30%"), (info, "70%")]))
    if b.get("about"):
        out.append(h(fmt(b["about"]["heading"]), 4))
        out.append(quote([fmt(x) for x in b["about"]["paragraphs"]], "— " + fmt(b["about"]["source"])))
    out.append(h("Anthologies", anchor="anthologies"))
    for a in bk["anthologies"]:
        m = meta([a["publisher"], a["year"]])
        if is_blank(a.get("url")):
            m += " · " + PLACEHOLDER.format("link")
        info = [h(anthology_title(a), 3), p(m, "jj-meta")]
        if a.get("description"):
            info.append(p(fmt(a["description"])))
        q = a.get("quote")
        if q and (q.get("paragraphs") or not is_blank(q.get("text"))):
            info.append(quote([fmt(x) for x in (q.get("paragraphs") or [q["text"]])],
                              "— " + fmt(q["source"]) if q.get("source") else None))
        if not is_blank(a.get("url")):
            info.append(more(a.get("linkLabel") or "Buy the book", a["url"]))
        if a.get("cover"):
            out.append(columns([([image(a["cover"]["src"], a["cover"]["alt"], "jj-cover jj-cover-small")], "20%"), (info, "80%")]))
        else:
            out += info
    return join(out)


def page_teaching(c):
    t = c["teaching"]
    out = [p(fmt(t["intro"])), h("Courses at the Stark campus"), ul([fmt(x) for x in t["courses"]]),
           h("A place-based approach")] + [p(fmt(x)) for x in t["approach"]]
    out += [h("Earlier teaching")] + [p(fmt(x)) for x in t["earlier"]]
    out.append(h("Community &amp; workshops", anchor="community"))
    for w in t["community"]:
        out += [h(fmt(w["title"]), 3), p(fmt(w["text"]))]
        if not is_blank(w.get("url")):
            out.append(more(w.get("linkLabel") or "Visit", w["url"]))
        elif w.get("linkLabel"):
            out.append(p(fmt(w["linkLabel"])))
    return join(out)


def page_residencies(c):
    out = []
    for i, r in enumerate(c["residencies"]):
        if i:
            out.append(separator())
        out += [p(fmt(r["dates"]), "jj-eyebrow"), h(fmt(r["title"])), p(meta([r["role"], r["place"]]), "jj-meta")]
        out += [p(fmt(x)) for x in r["description"]]
        if not is_blank(r.get("url")):
            out.append(more(r.get("linkLabel") or "Learn more", r["url"]))
        elif r.get("linkLabel"):
            out.append(p(fmt(r["linkLabel"])))
        for l in r.get("extraLinks") or []:
            if not is_blank(l.get("url")):
                out.append(more(l["label"], l["url"]))
        if r.get("photos"):
            out.append(columns([([image(ph["src"], ph["alt"], "jj-art", fmt(ph["caption"]))], None) for ph in r["photos"]]))
    return join(out)


def caption(title, cap):
    return f"<em>{fmt(title)}</em>" + (f"<br>{fmt(cap)}" if cap else "")


def page_photography(c):
    ph = c["photography"]
    out = [p(fmt(ph["intro"])),
           columns([([image(x["src"], x["alt"], "jj-photo", caption(x["title"], x.get("caption")))], None) for x in ph["photos"]], wide=True)]
    art = ph.get("art")
    if art and art.get("pieces"):
        out.append(h(fmt(art["heading"])))
        if not is_blank(art.get("intro")):
            out.append(p(fmt(art["intro"])))
        out.append(columns([([image(x["src"], x["alt"], "jj-art", caption(x["title"], x.get("caption")))], None) for x in art["pieces"]], wide=True))
    return join(out)


def page_bio(c):
    b = c["bio"]
    out = [columns([([image(c["site"]["headshot"]["src"], c["site"]["headshot"]["alt"], "jj-headshot")], "30%"),
                    ([quote([fmt(c["home"]["quote"]["text"])], None, "jj-pull")], "70%")]),
           h("Short bio", anchor="short-bio"), p(fmt(b["short"])), h("Long bio", anchor="long-bio")]
    out += [p(fmt(x)) for x in b["long"]]
    if c.get("awards"):
        out += [h("Awards &amp; honors"), ul([fmt(a) for a in c["awards"]])]
    if b.get("cv") and not is_blank(b["cv"].get("file")):
        out.append(buttons([(fmt(b["cv"]["label"]), img_url(b["cv"]["file"]), False)]))
    return join(out)


def event_p(ev):
    parts = [f"<strong>{fmt(ev['date'])}</strong>", link(fmt(ev["title"]), ev.get("url"))]
    if ev.get("place"):
        parts.append(fmt(ev["place"]))
    return p("<br>".join(parts), "jj-event")


def page_events(c):
    e = c["events"]
    out = [p(fmt(e["intro"]))]
    if e.get("photos"):
        out.append(columns([([image(x["src"], x["alt"], "jj-art" if x.get("fit") else "jj-photo", fmt(x["caption"]))], None)
                            for x in e["photos"]], wide=True))
    if e.get("upcoming"):
        out += [h("Upcoming")] + [event_p(x) for x in e["upcoming"]]
    if e.get("past"):
        out += [h("Past")] + [event_p(x) for x in e["past"]]
    return join(out)


def page_contact(c):
    s = c["site"]
    email = fmt(s["email"]) if is_blank(s["email"]) else f'<a href="mailto:{attr(s["email"])}">{html.escape(s["email"])}</a>'
    out = [p(fmt(c["contact"]["intro"])), h("Email"), p(email)]
    social = [(f'<a href="{attr(l["url"])}">{fmt(l["label"])}</a>' if not is_blank(l.get("url")) else fmt(l["label"]))
              for l in s.get("social") or []]
    if social:
        out += [h("Elsewhere"), ul(social)]
    return join(out)


PAGES = [
    ("home", "Home", page_home),
    ("poems", "Poems", page_poems),
    ("books", "Books & Anthologies", page_books),
    ("teaching", "Teaching", page_teaching),
    ("residencies", "Residencies", page_residencies),
    ("photography", "Photography & Art", page_photography),
    ("bio", "Bio", page_bio),
    ("events", "Events", page_events),
    ("contact", "Contact", page_contact),
]


# ---------------------------------------------------------------- WXR
def cdata(s):
    return "<![CDATA[" + s.replace("]]>", "]]]]><![CDATA[>") + "]]>"


def build_wxr(c):
    now = datetime.now(timezone.utc)
    date, gmt = now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S")
    rss_date = now.strftime("%a, %d %b %Y %H:%M:%S +0000")
    items, pages = [], {}
    for order, (slug, title, fn) in enumerate(PAGES):
        pid = order + 1
        content = fn(c)
        pages[slug] = content
        items.append(f"""	<item>
		<title>{cdata(title)}</title>
		<link>{IMAGE_BASE}{slug}/</link>
		<pubDate>{rss_date}</pubDate>
		<dc:creator>{cdata("jessica")}</dc:creator>
		<guid isPermaLink="false">{IMAGE_BASE}?page_id={pid}</guid>
		<description></description>
		<content:encoded>{cdata(content)}</content:encoded>
		<excerpt:encoded>{cdata("")}</excerpt:encoded>
		<wp:post_id>{pid}</wp:post_id>
		<wp:post_date>{cdata(date)}</wp:post_date>
		<wp:post_date_gmt>{cdata(gmt)}</wp:post_date_gmt>
		<wp:comment_status>{cdata("closed")}</wp:comment_status>
		<wp:ping_status>{cdata("closed")}</wp:ping_status>
		<wp:post_name>{cdata(slug)}</wp:post_name>
		<wp:status>{cdata("publish")}</wp:status>
		<wp:post_parent>0</wp:post_parent>
		<wp:menu_order>{order}</wp:menu_order>
		<wp:post_type>{cdata("page")}</wp:post_type>
		<wp:post_password>{cdata("")}</wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
	</item>""")
    # One attachment per image, so the importer downloads each into the Media Library
    # and rewrites the image addresses in the pages to point at the new copies.
    all_content = "\n".join(pages.values())
    urls = sorted(set(re.findall(r'src="(' + re.escape(IMAGE_BASE) + r'[^"]+)"', all_content)))
    for n, u in enumerate(urls):
        aid = 100 + n
        name = Path(u).stem
        items.append(f"""	<item>
		<title>{cdata(name.replace("-", " ").capitalize())}</title>
		<link>{u}</link>
		<pubDate>{rss_date}</pubDate>
		<dc:creator>{cdata("jessica")}</dc:creator>
		<guid isPermaLink="false">{u}</guid>
		<description></description>
		<content:encoded>{cdata("")}</content:encoded>
		<excerpt:encoded>{cdata("")}</excerpt:encoded>
		<wp:post_id>{aid}</wp:post_id>
		<wp:post_date>{cdata(date)}</wp:post_date>
		<wp:post_date_gmt>{cdata(gmt)}</wp:post_date_gmt>
		<wp:comment_status>{cdata("closed")}</wp:comment_status>
		<wp:ping_status>{cdata("closed")}</wp:ping_status>
		<wp:post_name>{cdata(name)}</wp:post_name>
		<wp:status>{cdata("inherit")}</wp:status>
		<wp:post_parent>0</wp:post_parent>
		<wp:menu_order>0</wp:menu_order>
		<wp:post_type>{cdata("attachment")}</wp:post_type>
		<wp:post_password>{cdata("")}</wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
		<wp:attachment_url>{cdata(u)}</wp:attachment_url>
	</item>""")
    head = f"""<?xml version="1.0" encoding="UTF-8" ?>
<!-- WordPress import file for the Jessica Jones website. Generated by wordpress/build_wordpress.py from content.json. -->
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/"
>
<channel>
	<title>Jessica Jones</title>
	<link>{IMAGE_BASE}</link>
	<description>{html.escape(c["site"]["tagline"])}</description>
	<pubDate>{rss_date}</pubDate>
	<language>en-US</language>
	<wp:wxr_version>1.2</wp:wxr_version>
	<wp:base_site_url>{IMAGE_BASE}</wp:base_site_url>
	<wp:base_blog_url>{IMAGE_BASE}</wp:base_blog_url>
	<wp:author><wp:author_id>1</wp:author_id><wp:author_login>{cdata("jessica")}</wp:author_login><wp:author_email>{cdata("")}</wp:author_email><wp:author_display_name>{cdata("Jessica Jones")}</wp:author_display_name><wp:author_first_name>{cdata("Jessica")}</wp:author_first_name><wp:author_last_name>{cdata("Jones")}</wp:author_last_name></wp:author>
"""
    return head + "\n".join(items) + "\n</channel>\n</rss>\n", len(urls)


def build_theme_zip():
    src = HERE / "jessica-jones"
    out = HERE / "jessica-jones-theme.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(src.rglob("*")):
            if f.is_file():
                z.write(f, Path("jessica-jones") / f.relative_to(src))
    return out


def main():
    c = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
    xml, n_images = build_wxr(c)
    (HERE / "jessica-jones-content.xml").write_text(xml, encoding="utf-8")
    z = build_theme_zip()
    print(f"Wrote jessica-jones-content.xml ({len(PAGES)} pages, {n_images} images) and {z.name}")


if __name__ == "__main__":
    main()
