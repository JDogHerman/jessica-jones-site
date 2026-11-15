# Before launch: facts to confirm and content to add

Everything below shows on the site as a highlighted **[placeholder]** (or a striped image box) until it's filled in.
Tick each item off as you go. Nothing should go live until every **Confirm** item has been checked.

## 1. Confirm (marked [confirm] in the brief)

- [x] **Title wording.** "Lecturer, Kent State University at Stark campus" (changed everywhere at your request).
- [ ] **Poets for Science.** Title corrected to "Ghost Flight, Berkeley Pit" from the published text. Still to confirm: spelling of "Exocoetidae", its year and link (Ghost Flight is done: 2025), and the wording "five poems selected".


## 2. Fill in (placeholders on the site)

### Site-wide (`content.json` → `site`)
- [x] Tagline: "Poet · Educator · Writer of Place".
- [ ] Professional email address
- [x] Facebook link. Added (Contact page).
- [ ] Optional: any other social media links (Instagram, etc.)
- [x] Website address set to https://jdogherman.github.io/jessica-jones-site (change it in all 9 `.html` files if you add a custom domain later)
- [ ] **Before announcing the site:** remove the `<meta name="robots" content="noindex, nofollow">` line (marked DRAFT) from the `<head>` of all 9 `.html` files so search engines can list it

### Images (put files in `/images`; see README for names and sizes)
- [x] `images/headshot.jpg`: portrait (Home and Bio). Added; a larger original (1000px+ wide) would look sharper on high-resolution screens. Check the alt text in `content.json`.
- [x] `images/bitterroot-cover.jpg`: *Bitterroot* cover (Home and Books). Added.
- [ ] Optional: who painted the *Bitterroot* cover art, if you want a credit line; and whether to mention "New Women’s Voices Series, #143" (shown on the cover) on the Books page
- [x] `images/photos/granite-county-ghosts.jpg`. Added, with alt text; please check it.
- [x] `images/photos/butte-alley-with-bicyclist.jpg`. Added, with alt text and the caption "© 2024 Jessica Jones"; please check the alt text.
- [ ] `images/og-image.jpg`: the picture shown when the site is shared on social media (1200 × 630)
- [x] Alt text for both photographs. Drafted; please check.
- [x] *Light Enters the Grove* cover. Added (Home and Books).
- [ ] Optional: add the subtitle "Exploring Cuyahoga Valley National Park through Poetry" and the editors (Charles Malone, Carrie George and Jason Harris), as shown on the cover?

### *Bitterroot* description (added from the text you supplied)
- [ ] Decide whether to add the two honors it mentions to an Awards section: runner-up with Open Country Press, and honorable mention with CutBank at the University of Montana. Give the year and the name of each prize or contest. The section stays hidden until you decide.
- [ ] Check the description against its source. Was "modeled by beauty" meant to be "marked by beauty"? Is "Jennifer Finley Greene" spelled right? ("CutBank" is fixed.) Apart from that fix, I kept your wording exactly; the only other changes are italics on the title and a proper dash in place of "--".
- [x] Source credit: now "— Finishing Line Press".
- [ ] The short line under the book says "Poems set on the Flathead Indian Reservation." The description says the poems travel from Stevensville to the Reservation. Keep the line, reword it, or remove it?

### Artwork (Photography page, "Drawing & collage" section; `content.json` → `photography` → `art`)
- [ ] Pencil drawing of the house (handwritten "late May."): title, plus medium and year for the caption. Is "late May." the title?
- [ ] Collage: title, plus medium and year for the caption
- [ ] Check the alt text I drafted for both pieces
- [ ] *And/Or* cover painting: the painting's title (publisher and year added: Finishing Line Press, 2025)
- [ ] Should the *And/Or* cover art also be mentioned in the bio?
- [x] Menu item renamed "Photography & Art"; section heading "Art".

### *Wide Branches, Deep Roots* (new: edited collection, Books page)
- [ ] After December 2026, change `"status": "Forthcoming"` (or remove it) in `content.json` → `books` → `edited`, and "· Forthcoming" in `home` → `featured`
- [x] Added to "Featured work" on the Home page.
- [x] Added to the short and long bios (they also say "forthcoming December 2026"; update after release).
- [ ] Her name on the cover is "Jessica M. Jones". Keep "Jessica Jones" everywhere else on the site?
- [ ] Check the alt text for the cover

### Poems (`content.json` → `poems`)
- [ ] Titles of the other three Poets for Science poems (optional)
- [ ] Journal publications: poem title, journal, year and link for each
- [x] Featured poem: "Ghost Flight, Berkeley Pit" added with its exact spacing. Confirm Jessica is happy for the full text to be on the site.
- [x] "Ghost Flight, Berkeley Pit": credited to Poets for Science, *Nature of Our Times*, January 15, 2025, with link.
- [ ] The poem text has "Berkely Pit" in one line (elsewhere "Berkeley"). Kept exactly as sent; fix only if it's a typo.

### Books & Anthologies (`content.json` → `books`)
- [x] *Bitterroot*: purchase link (Amazon). Added. Optional: also link to the Finishing Line Press page, if it’s still listed there.
- [x] *Light Enters the Grove*: link (Kent State University Press page). Added.
- [x] *Poems Across the Big Sky*: cover and introduction excerpt (Margaret C. Kingsland). Added.
- [x] *Poems Across the Big Sky*: purchase link (Amazon). Added.
- [x] *Poems Across the Big Sky*: Many Voices Press, 2006. Added.
- [ ] Optional: add the subtitle "An Anthology of Montana Poets" and "Edited by Lowell Jaeger", as shown on the cover?
- [x] *Bright Bones*: cover, publisher and year (Open Country Press, 2018). Added.
- [ ] *Bright Bones*: link
- [x] *Bright Bones*: subtitle and description added (credited to Open Country Press; confirm that's the source). The description says "currently available at Open Country Press"; keep it, or trim that sentence so it doesn't date?
- [x] *Dear Vaccine*: cover, publisher and year (Kent State University Press, 2022). Added.
- [x] *Dear Vaccine*: link (Kent State University Press). Added.
- [x] *Dear Vaccine*: book description. Added, credited to Kent State University Press.
- [x] *Dear Vaccine*: publication year confirmed as 2022.
- [ ] Optional: add the subtitle "Global Voices Speak to the Pandemic" and the editors (Naomi Shihab Nye, David Hassler and Tyler Meier), as shown on the cover?

### Teaching (`content.json` → `teaching`)
- [ ] A few sentences, in your own words, about your place-based teaching approach
- [x] "Dear Philipsburg" link. Added (Teaching and Residencies).

### Residencies (`content.json` → `residencies`)
- [ ] High school photo (Open AIR entry): name the other person, or leave her unnamed? Check the alt text.
- [ ] Philipsburg library photo (Open AIR entry): confirm it's Jessica and that it was taken during the 2024 residency; is that flyer for her workshops? (I can add that to the caption.)
- [x] "Dear Philipsburg" link on the Open AIR residency. Added.
- [ ] Optional: a link to the Open AIR residency's own website
- [ ] Cuyahoga Valley National Park (2007–2008): a sentence or two of description
- [ ] Calcutta Mercy Hospital: year, plus a sentence or two of description

### Events (`content.json` → `events`)
- [ ] Philipsburg artist talk (graphic and Past list): date and venue. Was it part of the 2024 Open AIR residency?
- [ ] Country Bookshelf reading (photo caption and Past list): confirm it's Jessica; date; what she read or the event name
- [x] Blaeser event: March 6, 2024. Added.
- [ ] Blaeser event: check the photo's alt text
- [ ] Upcoming readings and talks (date, title, venue and city, optional link)
- [ ] Past readings and talks

### Bio (`content.json` → `bio`)
- [ ] Read the short bio (121 words) and long bio (362 words). I wrote them only from the facts you gave me, but they're in your voice, so please approve or edit them.
- [ ] CV: add a PDF to `/docs` and set `bio.cv.file` (e.g. `"docs/jessica-jones-cv.pdf"`). The download button stays hidden until you do.

## 3. Hidden until you add content
These sections don't appear at all right now. Add entries to make them show up.
- `awards`: Awards & honors (shown on the Bio page)
- `praise`: quotes about your work from others (shown on the Home page). Use only real quotes with permission and a source.
- `poems.featuredPoems`: featured poem text

## 4. Worth double-checking
- [ ] The exact official name "Calcutta Mercy Hospital", and whether you want "Calcutta" or "Kolkata"
- [ ] Open AIR session name: the site says "Summer II (July–August) 2024"
- [ ] Wording used for the two community items on the Teaching page: "two adult writing workshops and one teen workshop at the local library" and "taught art camp at the local elementary school"
