/*
 * Renders each page from content.json.
 * You should not need to edit this file to update the site's text:
 * change content.json instead (see README.md).
 */
(function () {
  "use strict";

  // ---------- Mobile menu ----------
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
        toggle.focus();
      }
    });
  }

  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ---------- Helpers ----------
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  // Empty, or entirely a [bracketed placeholder]
  function isBlank(s) {
    if (s == null) return true;
    var t = String(s).trim();
    return t === "" || /^\[[^\]]*\]$/.test(t);
  }

  // Escape, then *italic* → <em>, [placeholder] → highlighted span
  function fmt(s) {
    return esc(s)
      .replace(/\*([^*]+)\*/g, "<em>$1</em>")
      .replace(/\[([^\]]+)\]/g, '<span class="placeholder">[$1]</span>');
  }

  function link(html, url, cls) {
    if (isBlank(url)) return html;
    var external = /^https?:\/\//.test(url);
    return '<a href="' + esc(url) + '"' + (cls ? ' class="' + cls + '"' : "") +
      (external ? ' rel="noopener"' : "") + ">" + html + "</a>";
  }

  // An image that turns into a visible placeholder box if the file is missing.
  function img(src, alt, cls) {
    var label = "[Add image: " + (src || "file not set") + "]";
    if (isBlank(src)) return '<div class="img-ph ' + (cls || "") + '">' + fmt(label) + "</div>";
    var altText = isBlank(alt) ? "" : alt;
    return '<img class="' + (cls || "") + '" src="' + esc(src) + '" alt="' + esc(altText) +
      '" loading="lazy" decoding="async" data-ph="' + esc(label) + '">';
  }

  function wireImages(root) {
    root.querySelectorAll("img[data-ph]").forEach(function (el) {
      function fail() {
        var box = document.createElement("div");
        box.className = "img-ph " + el.className;
        box.innerHTML = fmt(el.getAttribute("data-ph"));
        el.replaceWith(box);
      }
      if (el.complete && el.naturalWidth === 0) fail();
      else el.addEventListener("error", fail, { once: true });
    });
  }

  function paras(list) {
    return (list || []).map(function (p) { return "<p>" + fmt(p) + "</p>"; }).join("");
  }

  function section(title, body, opts) {
    opts = opts || {};
    var id = opts.id ? ' id="' + esc(opts.id) + '"' : "";
    var cls = "section" + (opts.cls ? " " + opts.cls : "");
    return "<section" + id + ' class="' + cls + '">' +
      (title ? "<h2>" + fmt(title) + "</h2>" : "") + body + "</section>";
  }

  function meta(parts) {
    return parts.filter(function (p) { return p && String(p).trim() !== ""; })
      .map(fmt).join(' <span aria-hidden="true">·</span> ');
  }

  // Optional second gallery for drawings, collage and other artwork
  function renderArt(a) {
    if (!a || !a.pieces || !a.pieces.length) return "";
    return '<section class="section wide art-section"><h2>' + fmt(a.heading) + "</h2>" +
      (isBlank(a.intro) ? "" : "<p>" + fmt(a.intro) + "</p>") +
      '<ul class="gallery art-gallery">' + a.pieces.map(function (ph) {
        return "<li><figure>" + img(ph.src, ph.alt, "art") +
          "<figcaption><em>" + fmt(ph.title) + "</em>" +
          (ph.caption ? '<span class="caption">' + fmt(ph.caption) + "</span>" : "") +
          "</figcaption></figure></li>";
      }).join("") + "</ul></section>";
  }

  // ---------- Page renderers ----------
  var pages = {
    home: function (c) {
      var s = c.site, h = c.home, out = "";

      out += '<section class="hero">' +
        '<div class="hero-text">' +
        '<h1 class="hero-name">' + fmt(s.name) + "</h1>" +
        '<p class="hero-tagline">' + fmt(s.tagline) + "</p>" +
        '<p class="hero-title">' + fmt(s.title) + "</p>" +
        "</div>" +
        '<div class="hero-photo">' + img(s.headshot.src, s.headshot.alt, "headshot") + "</div>" +
        "</section>";

      out += section("", '<div class="lede">' + paras(h.intro) + "</div>", { cls: "intro" });

      if (h.quote && !isBlank(h.quote.text)) {
        out += '<section class="section quote-section" aria-label="In her words">' +
          '<figure class="pull-quote"><blockquote><p>' + fmt(h.quote.text) + "</p></blockquote>" +
          "<figcaption>— " + fmt(h.quote.attribution) + "</figcaption></figure></section>";
      }

      if (c.praise && c.praise.length) {
        out += section("Praise", c.praise.map(function (q) {
          return '<figure class="praise"><blockquote><p>' + fmt(q.text) + "</p></blockquote><figcaption>— " +
            fmt(q.source) + "</figcaption></figure>";
        }).join(""));
      }

      if (h.featured && h.featured.length) {
        out += section("Featured work", '<div class="cards cards-' + h.featured.length + '">' + h.featured.map(function (f) {
          return '<article class="card">' +
            (f.image ? '<div class="card-media">' + img(f.image.src, f.image.alt, "cover") + "</div>" : "") +
            '<div class="card-body"><p class="eyebrow">' + fmt(f.kind) + "</p>" +
            "<h3><em>" + fmt(f.title) + "</em></h3><p>" + fmt(f.detail) + "</p>" +
            '<p><a class="more" href="' + esc(f.href) + '">' + fmt(f.linkLabel) + ' <span aria-hidden="true">→</span></a></p>' +
            "</div></article>";
        }).join("") + "</div>", { cls: "featured" });
      }

      var t = h.photoTeaser;
      if (t) {
        var photo = (c.photography.photos || []).filter(function (p) { return p.id === t.photo; })[0];
        out += section(t.heading,
          '<div class="teaser">' +
          (photo ? '<figure class="teaser-photo">' + img(photo.src, photo.alt, "photo") +
            "<figcaption><em>" + fmt(photo.title) + "</em></figcaption></figure>" : "") +
          '<div><p>' + fmt(t.text) + '</p><p><a class="more" href="photography.html">View the photographs <span aria-hidden="true">→</span></a></p></div>' +
          "</div>");
      }

      if (h.explore && h.explore.length) {
        out += section("Explore", '<ul class="explore">' + h.explore.map(function (e) {
          return '<li><a href="' + esc(e.href) + '"><span class="explore-label">' + fmt(e.label) +
            '</span><span class="explore-blurb">' + fmt(e.blurb) + "</span></a></li>";
        }).join("") + "</ul>");
      }
      return out;
    },

    poems: function (c) {
      var p = c.poems, out = '<p class="lede">' + fmt(p.intro) + "</p>";
      if (p.featuredPoems && p.featuredPoems.length) {
        out += section(p.featuredPoems.length > 1 ? "Featured poems" : "Featured poem", p.featuredPoems.map(function (fp) {
          return '<article class="poem"><h3>' + fmt(fp.title) + "</h3>" +
            (fp.place ? '<p class="credit-meta">' + fmt(fp.place) + "</p>" : "") +
            '<div class="poem-scroll" tabindex="0" role="region" aria-label="Poem text: ' + esc(fp.title) + '"><div class="poem-text">' +
            esc(fp.text) + "</div></div>" + (fp.credit ? '<p class="credit credit-meta">' + link(fmt(fp.credit), fp.creditUrl) + "</p>" : "") + "</article>";
        }).join(""), { cls: "poems-featured" });
      }
      (p.groups || []).forEach(function (g) {
        out += section(g.heading,
          (g.note ? "<p>" + fmt(g.note) + "</p>" : "") +
          '<ul class="credits">' + g.items.map(function (it) {
            var title = link(fmt(it.title), it.url);
            var m = meta([it.venue, it.year]);
            return "<li><span class=\"credit-title\">" + title + "</span>" +
              (m ? ' <span class="credit-meta">' + m + "</span>" : "") +
              (isBlank(it.url) && !isBlank(it.title) ? ' <span class="placeholder">[link]</span>' : "") +
              "</li>";
          }).join("") + "</ul>");
      });
      return out;
    },

    books: function (c) {
      var b = c.books.chapbook, out = "";
      var ed = c.books.edited;
      if (ed && ed.items && ed.items.length) {
        out += '<section class="section edited" id="edited"><h2>' + fmt(ed.heading) + "</h2>" + ed.items.map(function (x) {
          return '<div class="book">' +
            '<div class="book-cover">' + img(x.cover.src, x.cover.alt, "cover") + "</div>" +
            '<div class="book-info">' +
            (x.status ? '<p class="eyebrow">' + fmt(x.status) + "</p>" : "") +
            "<h3><em>" + fmt(x.title) + (x.subtitle ? ": " + fmt(x.subtitle) : "") + "</em></h3>" +
            "<p>" + fmt(x.role) + "</p>" +
            '<p class="book-meta">' + meta([x.publisher, x.date]) + "</p>" +
            (x.quote ? '<figure class="book-blurb small"><blockquote>' + paras(x.quote.paragraphs) + "</blockquote>" +
              (x.quote.source ? "<figcaption>— " + fmt(x.quote.source) + "</figcaption>" : "") + "</figure>" : "") +
            '<p class="book-actions">' +
            (isBlank(x.buyUrl) ? "" : '<a class="button" href="' + esc(x.buyUrl) + '" rel="noopener">' + fmt(x.buyLabel || "Buy the book") + "</a>") +
            (isBlank(x.url) ? "" : '<a class="more" href="' + esc(x.url) + '" rel="noopener">' + fmt(x.linkLabel || "Learn more") + ' <span aria-hidden="true">→</span></a>') +
            "</p>" +
            "</div></div>";
        }).join("") + "</section>";
      }
      out += '<section class="section book">' +
        '<div class="book-cover">' + img(b.cover.src, b.cover.alt, "cover") + "</div>" +
        '<div class="book-info"><p class="eyebrow">' + fmt(b.kind) + "</p>" +
        "<h2><em>" + fmt(b.title) + "</em></h2>" +
        '<p class="book-meta">' + meta([b.publisher, b.year]) + "</p>" +
        "<p>" + fmt(b.description) + "</p>" +
        (isBlank(b.buyUrl)
          ? '<p>' + fmt(b.buyLabel) + "</p>"
          : '<p><a class="button" href="' + esc(b.buyUrl) + '" rel="noopener">Buy <em>' + fmt(b.title) + "</em></a></p>") +
        "</div></section>";

      if (b.about && b.about.paragraphs && b.about.paragraphs.length) {
        out += section(b.about.heading, '<figure class="book-blurb"><blockquote>' + paras(b.about.paragraphs) +
          "</blockquote>" + (b.about.source ? "<figcaption>— " + fmt(b.about.source) + "</figcaption>" : "") +
          "</figure>", { id: "about-bitterroot" });
      }

      out += section("Anthologies", '<ul class="anthologies">' + c.books.anthologies.map(function (a) {
        var title = link("<em>" + fmt(a.title) + (a.subtitle ? ": " + fmt(a.subtitle) : "") + "</em>", a.url);
        return "<li" + (a.cover ? ' class="has-cover"' : "") + ">" +
          (a.cover ? '<div class="antho-cover">' + img(a.cover.src, a.cover.alt, "cover") + "</div>" : "") +
          "<div><h3>" + title + "</h3>" +
          '<p class="book-meta">' + meta([a.publisher, a.year]) +
          (isBlank(a.url) ? ' <span aria-hidden="true">·</span> <span class="placeholder">[link]</span>' : "") + "</p>" +
          (a.description ? "<p>" + fmt(a.description) + "</p>" : "") +
          (a.quote && (!isBlank(a.quote.text) || (a.quote.paragraphs && a.quote.paragraphs.length)) ? '<figure class="book-blurb small"><blockquote>' +
            (a.quote.paragraphs ? paras(a.quote.paragraphs) : "<p>" + fmt(a.quote.text) + "</p>") +
            "</blockquote>" + (a.quote.source ? "<figcaption>— " + fmt(a.quote.source) + "</figcaption>" : "") + "</figure>" : "") +
          (isBlank(a.url) ? "" : '<p><a class="more" href="' + esc(a.url) + '" rel="noopener">Buy the book <span aria-hidden="true">→</span></a></p>') +
          "</div></li>";
      }).join("") + "</ul>", { id: "anthologies" });
      return out;
    },

    teaching: function (c) {
      var t = c.teaching, out = '<p class="lede">' + fmt(t.intro) + "</p>";
      out += section("Courses at the Stark campus", '<ul class="tidy">' + t.courses.map(function (x) {
        return "<li>" + fmt(x) + "</li>";
      }).join("") + "</ul>");
      out += section("A place-based approach", paras(t.approach));
      out += section("Earlier teaching", paras(t.earlier));
      out += section("Community & workshops", '<div class="stack">' + t.community.map(function (w) {
        var lnk = isBlank(w.url)
          ? (w.linkLabel ? "<p>" + fmt(w.linkLabel) + "</p>" : "")
          : '<p><a class="more" href="' + esc(w.url) + '" rel="noopener">' + fmt(w.linkLabel || "Visit") + ' <span aria-hidden="true">→</span></a></p>';
        return '<article class="entry"><h3>' + fmt(w.title) + "</h3><p>" + fmt(w.text) + "</p>" + lnk + "</article>";
      }).join("") + "</div>", { id: "community" });
      return out;
    },

    residencies: function (c) {
      return '<div class="stack">' + c.residencies.map(function (r) {
        var lnk = isBlank(r.url)
          ? (r.linkLabel ? "<p>" + fmt(r.linkLabel) + "</p>" : "")
          : '<p><a class="more" href="' + esc(r.url) + '" rel="noopener">' + fmt(r.linkLabel || "Learn more") + ' <span aria-hidden="true">→</span></a></p>';
        (r.extraLinks || []).forEach(function (l) {
          if (!isBlank(l.url)) lnk += '<p><a class="more" href="' + esc(l.url) + '" rel="noopener">' + fmt(l.label) + ' <span aria-hidden="true">→</span></a></p>';
        });
        return '<article class="section entry residency">' +
          '<p class="eyebrow">' + meta([r.dates]) + "</p>" +
          "<h2>" + fmt(r.title) + "</h2>" +
          '<p class="book-meta">' + meta([r.role, r.place]) + "</p>" +
          (r.photos && r.photos.length ? '<div class="residency-body"><div>' + paras(r.description) + lnk + "</div>" +
            '<div class="residency-photos">' + r.photos.map(function (ph) {
              return '<figure class="residency-photo">' + img(ph.src, ph.alt, "res-img") +
                "<figcaption>" + fmt(ph.caption) + "</figcaption></figure>";
            }).join("") + "</div></div>"
            : paras(r.description) + lnk) + "</article>";
      }).join("") + "</div>";
    },

    photography: function (c) {
      var p = c.photography;
      return '<p class="lede">' + fmt(p.intro) + "</p>" +
        '<ul class="gallery">' + p.photos.map(function (ph) {
          return "<li><figure>" + img(ph.src, ph.alt, "photo") +
            "<figcaption><em>" + fmt(ph.title) + "</em>" +
            (ph.caption ? '<span class="caption">' + fmt(ph.caption) + "</span>" : "") +
            (isBlank(ph.alt) ? ' <span class="placeholder">[alt text]</span>' : "") +
            "</figcaption></figure></li>";
        }).join("") + "</ul>" + renderArt(p.art);
    },

    bio: function (c) {
      var b = c.bio, out = "";
      out += '<div class="bio-head">' + img(c.site.headshot.src, c.site.headshot.alt, "headshot small") +
        '<figure class="pull-quote small"><blockquote><p>' + fmt(c.home.quote.text) + "</p></blockquote></figure></div>";
      out += section("Short bio", "<p>" + fmt(b.short) + "</p>", { id: "short-bio" });
      out += section("Long bio", paras(b.long), { id: "long-bio" });
      if (c.awards && c.awards.length) {
        out += section("Awards & honors", '<ul class="tidy">' + c.awards.map(function (a) {
          return "<li>" + fmt(a) + "</li>";
        }).join("") + "</ul>");
      }
      if (b.cv && !isBlank(b.cv.file)) {
        out += section("", '<p><a class="button" href="' + esc(b.cv.file) + '" download>' + fmt(b.cv.label) + "</a></p>");
      }
      return out;
    },

    events: function (c) {
      var e = c.events;
      function list(items) {
        return '<ul class="events">' + items.map(function (ev) {
          return '<li><p class="event-date">' + fmt(ev.date) + "</p>" +
            '<div><p class="event-title">' + link(fmt(ev.title), ev.url) + "</p>" +
            (ev.place ? '<p class="credit-meta">' + fmt(ev.place) + "</p>" : "") + "</div></li>";
        }).join("") + "</ul>";
      }
      var out = '<p class="lede">' + fmt(e.intro) + "</p>";
      if (e.photos && e.photos.length) {
        out += '<div class="event-photos">' + e.photos.map(function (ph) {
          return '<figure class="event-photo">' + img(ph.src, ph.alt, ph.fit ? "event-img fit" : "event-img") +
            "<figcaption>" + fmt(ph.caption) +
            (ph.credit ? '<span class="caption">' + fmt(ph.credit) + "</span>" : "") +
            "</figcaption></figure>";
        }).join("") + "</div>";
      }
      if (e.upcoming && e.upcoming.length) out += section("Upcoming", list(e.upcoming));
      if (e.past && e.past.length) out += section("Past", list(e.past));
      return out;
    },

    contact: function (c) {
      var s = c.site;
      var email = isBlank(s.email)
        ? fmt(s.email)
        : '<a href="mailto:' + esc(s.email) + '">' + esc(s.email) + "</a>";
      var social = (s.social || []).map(function (l) {
        return "<li>" + (isBlank(l.url) ? fmt(l.label) : '<a href="' + esc(l.url) + '" rel="noopener me">' + fmt(l.label) + "</a>") + "</li>";
      }).join("");
      return '<p class="lede">' + fmt(c.contact.intro) + "</p>" +
        section("Email", '<p class="contact-email">' + email + "</p>") +
        (social ? section("Elsewhere", '<ul class="tidy">' + social + "</ul>") : "");
    }
  };

  // ---------- Boot ----------
  var page = document.body.getAttribute("data-page");
  var target = document.getElementById("content");
  if (!target || !pages[page]) return;

  fetch("content.json", { cache: "no-cache" })
    .then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(function (c) {
      var disc = document.getElementById("disclaimer");
      if (disc && c.site && !isBlank(c.site.disclaimer)) disc.textContent = c.site.disclaimer;
      target.innerHTML = pages[page](c);
      wireImages(target);
      target.removeAttribute("aria-busy");
    })
    .catch(function (err) {
      target.removeAttribute("aria-busy");
      target.innerHTML = '<div class="load-error"><p><strong>The page content could not be loaded.</strong></p>' +
        "<p>If you just edited <code>content.json</code>, check it for a missing comma or quotation mark " +
        '(paste it into <a href="https://jsonlint.com">jsonlint.com</a> to find the problem). ' +
        "If you opened this file directly from your computer, preview it with a local server instead (see README.md).</p>" +
        '<p class="credit-meta">' + esc(err.message) + "</p></div>";
    });
})();
