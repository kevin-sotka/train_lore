#!/usr/bin/env python3
"""Generate all favicon / app-icon sizes from one square source.

Put your 1024x1024 (or larger) square icon at images/icon-source.png, then run:
    python3 make_icons.py

Produces:
  favicon.ico                 (multi-size: 16/32/48) — browser tab
  icons/favicon-32.png        — modern browsers
  icons/apple-touch-icon.png  (180x180) — iOS "Add to Home Screen" / Save as Web App
  icons/icon-192.png          — Android/Chrome install
  icons/icon-512.png          — Android/Chrome install + maskable

Requires Pillow:  pip install pillow --break-system-packages
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "images", "icon-source.png")
ICONS = os.path.join(ROOT, "icons")
os.makedirs(ICONS, exist_ok=True)

if not os.path.exists(SRC):
    raise SystemExit("Missing images/icon-source.png — generate the icon and save it there first.")

img = Image.open(SRC).convert("RGBA")

def save_png(size, path):
    img.resize((size, size), Image.LANCZOS).save(path)
    print("wrote", os.path.relpath(path, ROOT))

save_png(32,  os.path.join(ICONS, "favicon-32.png"))
save_png(180, os.path.join(ICONS, "apple-touch-icon.png"))
save_png(192, os.path.join(ICONS, "icon-192.png"))
save_png(512, os.path.join(ICONS, "icon-512.png"))

# multi-resolution .ico for the classic favicon
ico_path = os.path.join(ROOT, "favicon.ico")
img.save(ico_path, sizes=[(16, 16), (32, 32), (48, 48)])
print("wrote favicon.ico")
print("done — commit and push to publish.")
