#!/bin/bash
# make_bg_video.sh — turn a raw AI-generated clip into a web-ready looping background.
#
# 1. Generate your clip and save it as:  video/bg-source.mp4
# 2. Run:  bash make_bg_video.sh
#
# Produces, in video/:
#   bg.mp4   — H.264, muted, seamless forward+reverse loop, ~1080p, compressed
#   bg.webm  — VP9 version (smaller, modern browsers prefer it)
#   bg-poster.jpg — first-frame still (fallback for mobile / reduced-motion)
#
# Requires ffmpeg:  brew install ffmpeg

set -euo pipefail
cd "$(dirname "$0")/video"

SRC="bg-source.mp4"
[ -f "$SRC" ] || { echo "Missing video/bg-source.mp4 — drop your clip there first."; exit 1; }

# 1) Boomerang: play forward then reversed so the loop has no visible seam.
ffmpeg -y -i "$SRC" -filter_complex \
  "[0:v]scale=-2:1080,setsar=1,split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0[v]" \
  -map "[v]" -an boomerang.mp4

# 2) Compressed MP4 (H.264) — broad compatibility, no audio.
ffmpeg -y -i boomerang.mp4 -an -c:v libx264 -profile:v high -crf 28 \
  -preset slow -pix_fmt yuv420p -movflags +faststart bg.mp4

# 3) WebM (VP9) — smaller for browsers that take it.
ffmpeg -y -i boomerang.mp4 -an -c:v libvpx-vp9 -crf 36 -b:v 0 bg.webm

# 4) Poster still from the first frame.
ffmpeg -y -i boomerang.mp4 -vframes 1 -q:v 3 bg-poster.jpg

rm -f boomerang.mp4
echo "done — video/bg.mp4, bg.webm, bg-poster.jpg created."
ls -lh bg.mp4 bg.webm bg-poster.jpg
