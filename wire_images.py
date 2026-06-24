#!/usr/bin/env python3
"""Scan images/ for newly-dropped diorama files and wire them into their story pages.

A story page carries placeholder blocks like:
  <div class="img-placeholder" data-slot="hero" data-expect="rogers-pass-twin-avalanche-hero.png"> ... </div>

If images/<expected-filename> now exists, the placeholder is replaced with a real <img>.
Also refreshes the thumb path in stories.json so the depot board picks it up.
Idempotent: safe to run every week. Prints what it wired."""
import os, re, json, glob, html

ROOT = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(ROOT, "images")
STORIES_DIR = os.path.join(ROOT, "stories")

available = set(os.path.basename(p) for p in glob.glob(os.path.join(IMAGES, "*")))
wired = []

placeholder_re = re.compile(
    r'<div class="img-placeholder"[^>]*data-slot="(?P<slot>[^"]+)"[^>]*data-expect="(?P<expect>[^"]+)"[^>]*>.*?</div>',
    re.DOTALL,
)

for page in glob.glob(os.path.join(STORIES_DIR, "*.html")):
    with open(page) as f:
        src = f.read()
    changed = False

    def repl(m):
        global changed
        expect = m.group("expect")
        slot = m.group("slot")
        if expect in available:
            changed = True
            alt = html.escape(os.path.splitext(expect)[0].replace("-", " "))
            cls = "featured" if slot == "hero" else ""
            wired.append(f"{os.path.basename(page)} :: {expect}")
            return f'<img class="{cls}" src="../images/{html.escape(expect)}" alt="{alt}" data-slot="{slot}">'
        return m.group(0)

    new_src = placeholder_re.sub(repl, src)
    if changed:
        with open(page, "w") as f:
            f.write(new_src)

# refresh thumbs in stories.json (board uses these)
sj_path = os.path.join(ROOT, "stories.json")
with open(sj_path) as f:
    data = json.load(f)
for s in data["stories"]:
    expected_hero = f'{s["slug"]}-hero.png'
    if expected_hero in available:
        s["thumb"] = f"images/{expected_hero}"
with open(sj_path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

if wired:
    print("Wired images:\n  " + "\n  ".join(wired))
else:
    print("No new images to wire (all pending slots still awaiting files).")
