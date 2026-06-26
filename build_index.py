#!/usr/bin/env python3
"""Build index.html (the depot board) from stories.json.
Newest story on top. Missing thumbnails render as a placeholder block,
not a broken image. The weekly scheduled task runs this after adding a story."""
import json, os, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT, "stories.json")) as f:
    data = json.load(f)

stories = sorted(data["stories"], key=lambda s: s.get("date", ""), reverse=True)

rows = []
for s in stories:
    slug = s["slug"]
    headline = html.escape(s["headline"])
    dek = html.escape(s.get("dek", ""))
    date = s.get("date", "")
    try:
        date_label = datetime.date.fromisoformat(date).strftime("%B %-d, %Y")
    except Exception:
        date_label = date
    num = s.get("topic_num", "")
    thumb_rel = s.get("thumb", "")
    thumb_abs = os.path.join(ROOT, thumb_rel) if thumb_rel else ""
    if thumb_rel and os.path.exists(thumb_abs):
        thumb_html = f'<img class="thumb" src="{html.escape(thumb_rel)}" alt="">'
    else:
        thumb_html = '<div class="thumb placeholder">image<br>pending</div>'
    rows.append(f'''    <a class="entry" href="stories/{html.escape(slug)}.html">
      {thumb_html}
      <div class="meta">
        <div class="num">Tale No. {num}</div>
        <div class="headline">{headline}</div>
        <div class="dek">{dek}</div>
        <div class="date">{date_label}</div>
      </div>
    </a>''')

board = "\n".join(rows) if rows else '<p style="color:var(--ink-dim)">No tales set down yet.</p>'

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Train Lore — Tales from the High Iron</title>
<meta name="description" content="A weekly retelling of Pacific Northwest railroad history, set down by the lantern-keeper.">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="icons/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<meta name="theme-color" content="#0a0a0a">
<link rel="stylesheet" href="lore.css">
</head>
<body>
<div class="wrap">

  <header class="masthead">
    <a href="index.html">
      <span class="lockup">
        <img class="brand-icon" src="icons/icon-192.png" alt="">
        <span class="wordmark">
          <span class="title">Train Lore</span>
          <span class="sub">Tales from the High Iron</span>
        </span>
      </span>
    </a>
  </header>

  <p style="text-align:center;color:var(--ink-dim);font-style:italic;margin-bottom:2.6em;">
    A new tale of the Pacific Northwest railroads, retold each week by lantern light.
  </p>

  <div class="board">
{board}
  </div>

  <footer>
    Train Lore &middot; a weekly retelling from the Meatbag Labs depot &middot; last updated {data.get("updated","")}
  </footer>

</div>
</body>
</html>
'''

with open(os.path.join(ROOT, "index.html"), "w") as f:
    f.write(page)

print(f"index.html built — {len(stories)} tale(s) on the board")
