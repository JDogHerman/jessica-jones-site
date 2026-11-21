# Jessica Jones: personal website

A small, plain HTML/CSS site with no build step. All of the words on the site live in **one file, `content.json`**.

```
content.json          ← all the site's text: edit this
images/               ← headshot, book cover, photographs
docs/                 ← CV (PDF), when you have one
index.html …          ← the 9 pages (layout only; rarely need editing)
assets/css/style.css  ← colours, fonts, layout
assets/js/site.js     ← reads content.json and fills in each page
TODO.md               ← everything still to confirm or add before launch
```

Pages: Home · Poems · Books & Anthologies · Teaching · Residencies · Photography & Art · Bio · Events · Contact

---

## Editing the content

Open `content.json` in any text editor. On GitHub you can click the file and then the pencil icon. Change only the text **between quotation marks**.

**A few rules:**

| You want to… | Do this |
|---|---|
| Make a title italic | Wrap it in asterisks: `"*Bitterroot*"` |
| Mark something as "still to do" | Put it in square brackets: `"[year]"`. It shows on the site as a highlighted placeholder. Remove the brackets once you've filled it in. |
| Add a link | Put the full address in the `"url"` field: `"url": "https://…"`. Leave it `""` for no link. |
| Hide a section | Make its list empty: `"awards": []` |
| Show a hidden section | Add entries to it, e.g. `"awards": ["Award name, year"]` |
| Use quotation marks inside text | Use curly quotes “ ” (or type `\"`) |

**Examples:**

Add an event:
```json
"upcoming": [
  { "date": "March 4, 2027", "title": "Reading at …", "place": "Canton, Ohio", "url": "https://…" }
],
```

Add a journal credit (in `poems` → `groups` → the "Journals" group):
```json
{ "title": "“Poem Title”", "venue": "Journal Name", "year": "2025", "url": "https://…" },
```

Add a featured poem (only with permission). Line breaks are written as `\n`:
```json
"featuredPoems": [
  { "title": "“Poem Title”", "text": "First line\nSecond line\n\nNew stanza", "credit": "First published in …" }
],
```

Add your CV: put the PDF in `docs/`, then set `"cv": { "file": "docs/jessica-jones-cv.pdf", "label": "Download CV (PDF)" }`.

**If a page goes blank after an edit**, there's almost always a missing comma or quotation mark in `content.json`. The page shows a message saying so. Paste the whole file into <https://jsonlint.com> and it will point to the line. Every entry in a list needs a comma after it **except the last one**.

## Adding images

Save images with these exact names (or change the `"src"` paths in `content.json` to match yours):

| File | Used on | Suggested size |
|---|---|---|
| `images/headshot.jpg` | Home, Bio | 1000 × 1250 px (portrait, 4:5) |
| `images/bitterroot-cover.jpg` | Home, Books | 800 px wide |
| `images/photos/granite-county-ghosts.jpg` | Home, Photography | 1600 px wide (4:3 is shown best) |
| `images/photos/butte-alley-with-bicyclist.jpg` | Photography | 1600 px wide |
| `images/og-image.jpg` | Preview when shared on social media | 1200 × 630 px |

Keep each file under ~400 KB. Squoosh (<https://squoosh.app>) is a free tool that shrinks them. Until a file exists, the site shows a striped placeholder box with the expected filename.

**Alt text:** for each photograph, replace the `"alt"` placeholder with a short description of what the picture shows (e.g. "A narrow brick alley in Butte with a cyclist passing at dusk"). Screen-reader users rely on this.

To add more photographs, copy one entry in `photography` → `photos` and change the `id`, `title`, `src` and `alt`.

## Previewing on your computer

Because the pages read `content.json`, opening `index.html` by double-clicking it won't work in most browsers. Run a tiny local server instead, from inside this folder:

```bash
python3 -m http.server 8000
```

Then visit <http://localhost:8000>.

## Deploying

### Option A: Netlify (simplest)
1. Sign up at <https://app.netlify.com>.
2. Choose **Add new site → Deploy manually**, and drag this whole folder onto the page.
3. Netlify gives you an address like `something.netlify.app`. You can rename it or connect your own domain under **Domain settings**.
4. To update later, drag the folder in again. Or connect a GitHub repository (Option B, step 1) so that every edit you save on GitHub goes live automatically.

### Option B: GitHub Pages
1. Create a free GitHub account and a new **public** repository (e.g. `jessica-jones-site`). Upload all the files in this folder, including the hidden `.nojekyll` file.
2. In the repository, go to **Settings → Pages**. Under "Build and deployment" choose **Deploy from a branch**, branch `main`, folder `/ (root)`, and save.
3. After a minute the site appears at `https://<your-username>.github.io/jessica-jones-site/`.
4. To edit, open `content.json` on GitHub, click the pencil, make your change and **Commit changes**. The site updates within a minute or two.

### Live site
The site is hosted with GitHub Pages at <https://jdogherman.github.io/jessica-jones-site/> (repository: `JDogHerman/jessica-jones-site`). Edit `content.json` on GitHub and the live site updates within a minute or two.

While it's a draft, each page has a `noindex` line (marked DRAFT) that asks search engines not to list it. Remove that line from all nine `.html` files when you're ready to launch.

### If you change the web address
Each page's `<head>` contains `https://YOUR-SITE-URL` (used for search engines and social-media previews). Replace it in all nine `.html` files with your real address, without a trailing slash, e.g. `https://jessicajones.net`. Most editors have "Find in files / Replace all". The page titles and descriptions for search engines are in the same `<head>` sections if you ever want to reword them.

### If a change doesn't show up
Browsers keep copies of the site's style and script files for a while. If you change `assets/css/style.css` or `assets/js/site.js`, also bump the number after `?v=` where those files are linked in the nine `.html` files (any new number works). Text changes in `content.json` don't need this.

## WordPress version
The `wordpress/` folder has the same site as a WordPress theme plus an import file with all nine pages, so it can be edited in WordPress's visual editor. See `wordpress/README.md` for setup.

## Design notes
- Fonts: Cormorant Garamond (headings) and Source Serif 4 (body), from Google Fonts.
- Colours are defined at the top of `assets/css/style.css`: paper `#faf7f0`, ink `#1f2a2c`, moss green `#3d5a40`, copper `#8f5430` and sage `#a9b49a`. All text colours meet WCAG AA contrast.
- Accessibility: a skip-to-content link, keyboard-friendly menu (Escape closes it on mobile), visible focus outlines, semantic headings, and alt text for every image.
- This is a personal site. It uses no Kent State logos, seals or branding, and the footer of every page says it isn't an official university website.
