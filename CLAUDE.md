# train_lore — Pacific Northwest Railroad History Blog

Longform narrative blog posts about Pacific Northwest railroad history, written by Kevin Sotka for [meatbagmade.com](https://meatbagmade.com) and the [@traindewd Substack newsletter](https://substack.com/@traindewd).

## Project Structure

```
train_lore/
├── CLAUDE.md                              # This file
├── pacific-northwest-railroad-topics.md   # 32 story ideas, tracked with [x]/[ ]
├── published-to-substack.json             # Tracks which posts have been sent to Substack
├── images/
│   └── bakedpotato.png                    # Featured image (North Coast Limited article)
├── .claude/
│   └── skills/
│       └── substack-publish/
│           └── SKILL.md                   # /substack-publish skill
└── *-blog-post.html                       # Articles (one per file)
```

## Article HTML Structure

Each article is a self-contained HTML file:

1. `<head>` with inline CSS — Georgia serif, 800px max-width, `#3498db` blue accent
2. `<h1>` — article title
3. `<p>` paragraphs, `<h2>` section headings, `<blockquote>` pull quotes
4. `<hr>` + `<p><strong>Sources & Further Reading:</strong></p>` + `<ul>` of linked sources
5. `<hr>` + `<p><em>Written by Kevin Sotka for meatbagmade.com...</em></p>` — footer byline

**Exception:** `wellington-avalanche-blog-post.html` has a large base64-encoded `<img class="featured-image">` before the `<h1>`. This is stripped when publishing to Substack (see skill).

## Published Articles (5 of 32)

| File | Title |
|------|-------|
| `wellington-avalanche-blog-post.html` | White Death at Wellington: America's Deadliest Avalanche |
| `deschutes-canyon-railroad-war-blog-post.html` | The Deschutes Canyon Railroad War: Dynamite, Sabotage, and the Last Great Railroad Battle |
| `stampede-pass-blog-post.html` | Stampede Pass: The $1,000 Race Through the Mountain |
| `john-stevens-marias-pass-blog-post.html` | The Night He Walked Alone: John F. Stevens' Discovery of Marias Pass |
| `great-big-baked-potato-blog-post.html` | The Great Big Baked Potato: How Northern Pacific's North Coast Limited Made Culinary History |

Substack publish status for each is tracked in `published-to-substack.json`.

## Topic Tracker

`pacific-northwest-railroad-topics.md` contains 32 story ideas across categories: disasters, engineering marvels, railroad titans, labor history, Native community impact, urban development, famous trains, company rise/fall, logging railroads, and heritage preservation. Use `[x]` for completed articles and `[ ]` for pending.

## Publishing to Substack

Run `/substack-publish` to push an article to the @traindewd Substack newsletter.

### Setup (one-time)

`SUBSTACK_CONNECT_SID` must be set as an environment variable before the skill can run.

**Get the cookie:**
1. Log into substack.com in Chrome or Firefox
2. DevTools (F12) → Application → Cookies → `https://substack.com`
3. Copy the `connect.sid` value (looks like `s%3A...`)

**Configure it in Claude Code on the web:**
- Open environment settings for this project → add `SUBSTACK_CONNECT_SID` = `<value>`

**Configure it in Claude Code CLI:**
```bash
export SUBSTACK_CONNECT_SID="s%3Ayour-value-here"
```

Or add to `.claude/settings.json` (do not commit if it contains the live cookie):
```json
{ "env": { "SUBSTACK_CONNECT_SID": "s%3Ayour-value-here" } }
```

**Verify it works:**
```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  -H "Cookie: connect.sid=${SUBSTACK_CONNECT_SID}" \
  "https://substack.com/api/v1/me"
```
`HTTP 200` = ready to publish.

### What the skill does

Handles: article selection, HTML parsing, Substack API draft creation, publish confirmation, tracking file updates. See `.claude/skills/substack-publish/SKILL.md` for full workflow.

## Writing Style

- Narrative-first: strong opening hook, active voice, human drama over technical specs
- Audience: curious non-experts — history that sounds like a great story told at a bar
- Tone: engaged, slightly irreverent, backed by solid sourcing
- Length: 800–1,100 words typical

## Author

**Kevin Sotka** — meatbagmade@gmail.com · [meatbagmade.com](https://meatbagmade.com) · [@TrainDewd](https://twitter.com/TrainDewd)
