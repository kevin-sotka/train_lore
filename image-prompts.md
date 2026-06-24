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

<!-- TEMPLATE for the weekly job to copy below this line:

## Tale No. <N> — <Title> (<year>)
slug: `<story-slug>`

- [ ] **hero** → `<story-slug>-hero.png` (png)
  > <diorama prompt, 2-4 sentences, PNW steam-era, miniature/tabletop look, 3:2 landscape>

-->
