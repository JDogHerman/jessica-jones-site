# Jessica Jones website: WordPress version

This folder turns the site into a WordPress site that Jessica can edit in WordPress's visual editor, with no code.

| File | What it is |
|---|---|
| `jessica-jones-theme.zip` | The theme: fonts, colours, menu, header and footer. Upload it as is (don't unzip). |
| `jessica-jones-content.xml` | All nine pages (text, links, poems, images). Import it once. |
| `jessica-jones/` | The theme's source files (only needed if someone wants to change the design). |
| `build_wordpress.py` | Rebuilds the two files above from `../content.json`. |

## Which WordPress?

The theme is a custom upload, so you need WordPress that allows uploading themes:

- **Self-hosted WordPress** (WordPress installed by a web host such as SiteGround, DreamHost, Bluehost or Hostinger, usually a one-click install). Works on any plan. **Recommended.**
- **WordPress.com Business or Commerce plan.** These allow uploaded themes. The cheaper WordPress.com plans (Free, Personal, Premium) do **not** allow uploaded themes. On those plans you can still import the pages (step 3) and use a built-in theme such as *Twenty Twenty-Five*, but the site won't have this design.

It needs WordPress 6.6 or newer (any new install will be).

## Setting it up (about 15 minutes)

### 1. Basic settings
In the WordPress dashboard:
1. **Settings → General:** set *Site Title* to `Jessica Jones` and *Tagline* to `Poet · Educator · Writer of Place`.
2. **Settings → Permalinks:** choose **Post name**, then **Save**. (The pages' internal links expect addresses like `/poems/`.)
3. **Settings → Reading:** tick **Discourage search engines from indexing this site** while the site is still a draft. Untick it at launch.

### 2. Install the theme
1. **Appearance → Themes → Add New Theme → Upload Theme.**
2. Choose `jessica-jones-theme.zip`, click **Install Now**, then **Activate**.

### 3. Import the pages and images
1. **Tools → Import → WordPress.** If it says *Install Now*, click that first, then *Run Importer*.
2. Choose `jessica-jones-content.xml` and click **Upload file and import**.
3. On the next screen, assign the posts to your own user, and **tick "Download and import file attachments"**. This copies all 17 images into the Media Library.
4. Click **Submit**. It takes a minute while the images download.

The images are copied from the current GitHub Pages site (`jdogherman.github.io/jessica-jones-site`), so **keep that site online until the import is finished**.

### 4. Tidy up
1. **Pages:** delete WordPress's demo **Sample Page** (and **Posts → Hello world!**) so they don't appear in the menu.
2. Open the site. The theme makes the page called **Home** the front page automatically the first time you visit the dashboard after importing. If it doesn't, set it under **Settings → Reading → Your homepage displays → A static page → Homepage: Home**.

## Editing the site

- **Text, links, poems, events:** **Pages →** the page → edit in place → **Update**. Each section is an ordinary block (paragraph, heading, list, quote, image), so you can type, drag or delete as in a word processor.
- **Poems** are in *Verse* blocks, which keep line breaks and indentation exactly as typed.
- **Placeholders** look like highlighted text in [square brackets]. Replace the whole highlighted text, brackets included.
- **Menu:** the menu lists the pages automatically, in the order set by each page's *Order* number (Page settings → Page attributes → Order). A new page appears in the menu when it's published.
- **Footer** (copyright and "not an official Kent State University website" note): **Appearance → Editor → Patterns → Footer**.
- **Colours and fonts:** **Appearance → Editor → Styles**.

## Search engines and sharing

WordPress writes the page titles automatically. For custom search descriptions and social-media preview images, install the free **Yoast SEO** or **The SEO Framework** plugin (not possible on the cheaper WordPress.com plans).

## Rebuilding after changing `content.json`

The WordPress pages are now the place to edit. If you'd rather keep editing `content.json` and re-import, run `python3 wordpress/build_wordpress.py`, then delete the existing pages before importing again (the importer skips pages whose titles already exist).
