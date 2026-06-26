# Train Lore — Image Prompts Ledger

How this works:
1. Each week the scheduled task appends a block here for the new tale — a diorama-style
   image prompt, the **exact target filename**, file type, and which slot in the article it fills.
2. You generate the image (ChatGPT / whatever), save it with that **exact filename**, and drop it
   into the `images/` folder — whenever you like, at random intervals.
3. On its next run the task scans `images/`. Any file whose name matches a pending slot gets wired
   into that story's page automatically (and onto the depot board as the thumbnail). Until then the
   page shows a tasteful "image pending" placeholder — never a broken image.

Naming rule: `<story-slug>-<slot>.png`  (slots: `hero`, `inset1`, `inset2`).
Keep filenames lowercase, hyphenated, exactly as written below.

House look for every image: **model-railroad diorama / miniature scene**, shot like a
tabletop layout — shallow depth of field, slightly oversaturated, tiny painted figures,
visible scenery texture. Pacific Northwest mountains, period-correct steam-era railroading.
Aim 3:2, landscape.

---

## Tale No. 1 — White Death at Wellington (1910)
slug: `wellington-avalanche`

- [ ] **hero** → `wellington-avalanche-hero.png` (png)
  > Model-railroad diorama of the Wellington disaster, Cascade Mountains, March 1910. Two
  > miniature Great Northern passenger trains swept off a snowy ledge and tumbled into a
  > timbered canyon below, half-buried in a churned white avalanche. Steep evergreen slopes,
  > a wooden snowshed splintered, gray storm light and blowing snow. No visible figures,
  > somber and stark. Tabletop miniature look, shallow depth of field, slightly desaturated,
  > visible scenery texture. 3:2 landscape.

## Tale No. 2 — Rogers Pass Twin Avalanche (1910)
slug: `rogers-pass-twin-avalanche`

- [ ] **hero** → `rogers-pass-twin-avalanche-hero.png` (png)
  > Model-railroad diorama of a snowbound mountain pass at night in the Selkirk Mountains,
  > 1910. A miniature steam rotary snowplow with its blades half-buried in a fresh avalanche,
  > tiny painted figures of laborers with lanterns and shovels working in a deep snow cut
  > between two towering white slopes. Lantern glow, blue-black night sky, falling snow.
  > Shallow depth of field, tabletop miniature look, slightly oversaturated, visible scenery
  > texture. 3:2 landscape.

## Tale No. 4 — Massacre at Deep Creek (1887)
slug: `deep-creek-massacre`

- [ ] **hero** → `deep-creek-massacre-hero.png` (png)
  > Model-railroad diorama of the deep Hells Canyon gorge on the Snake River at dusk,
  > 1887. Towering miniature rock walls in shadow, a thin silver river far below, a tiny
  > abandoned Chinese mining camp on a gravel bank — small tents, a sluice box, a wisp of
  > smoke from a burned-out fire. Somber, low gold light, long shadows, no figures.
  > Tabletop miniature look, shallow depth of field, slightly desaturated and elegiac,
  > visible scenery texture. 3:2 landscape.

## Tale No. 3 — The Deschutes Canyon Railroad War (1909–1911)
slug: `deschutes-canyon-railroad-war`

- [ ] **hero** → `deschutes-canyon-railroad-war-hero.png` (png)
  > Model-railroad diorama of two rival rail grades being blasted up opposite walls of
  > Oregon's Deschutes River canyon, 1910. Tiny painted construction crews, a puff of
  > dynamite smoke on a cliff face, dump carts and timber trestles clinging to dry basalt
  > walls, the green river winding below. Warm high-desert light, dust in the air, a sense
  > of rivalry and tension. Tabletop miniature look, shallow depth of field, slightly
  > oversaturated, visible scenery texture. 3:2 landscape.

## Tale No. 7 — Stampede Pass: The $1,000 Race (1888)
slug: `stampede-pass`

- [ ] **hero** → `stampede-pass-hero.png` (png)
  > Model-railroad diorama of the Stampede Pass tunnel breakthrough, Cascade Range, 1888.
  > A miniature tunnel portal cut into granite, tiny painted laborers with drills and
  > lanterns crowding the dark opening, a Northern Pacific steam locomotive waiting on fresh
  > track outside. Dramatic lantern light spilling from the bore, cool mountain shadow,
  > evergreen slopes above. Tabletop miniature look, shallow depth of field, slightly
  > oversaturated, visible scenery texture. 3:2 landscape.

## Tale No. 9 — The Night He Walked Alone: Marias Pass (1889)
slug: `john-stevens-marias-pass`

- [ ] **hero** → `john-stevens-marias-pass-hero.png` (png)
  > Model-railroad diorama of a lone figure of surveyor John F. Stevens in a snowy mountain
  > pass at night, Montana, 1889. A single tiny painted man in a heavy coat pacing to keep
  > warm beside a small fire on a windswept saddle of the Continental Divide, vast dark
  > peaks and deep snow around him, cold blue moonlight and blowing snow. Lonely and
  > austere. Tabletop miniature look, shallow depth of field, slightly desaturated, visible
  > scenery texture. 3:2 landscape.

## Tale No. 22 — The Great Big Baked Potato (early 1900s)
slug: `great-big-baked-potato`

- [ ] **hero** → `great-big-baked-potato-hero.png` (png)
  > Model-railroad diorama of a Northern Pacific dining car interior on the North Coast
  > Limited, early 1900s. A miniature white-linen dining table with a comically large baked
  > potato on a plate, tiny painted waiter in a white jacket, brass lamps and arched
  > windows showing a blurred mountain landscape rushing past. Warm cozy lamplight, rich
  > reds and golds, a touch of whimsy. Tabletop miniature look, shallow depth of field,
  > slightly oversaturated, visible scenery texture. 3:2 landscape.

<!-- TEMPLATE for the weekly job to copy below this line:

## Tale No. <N> — <Title> (<year>)
slug: `<story-slug>`

- [ ] **hero** → `<story-slug>-hero.png` (png)
  > <diorama prompt, 2-4 sentences, PNW steam-era, miniature/tabletop look, 3:2 landscape>

-->
