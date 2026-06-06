---
name: substack-publish
description: Publish a Pacific Northwest railroad history blog post from this project to Substack. Reads an existing HTML article, adapts it for Substack (extracts title/subtitle, cleans footer, adds CTA), posts as a draft, then optionally publishes it live. Use when Kevin wants to push one of the train_lore HTML articles to the @traindewd Substack newsletter. Triggers on "publish", "Substack", "@traindewd", or "post to newsletter".
---

# Substack Publish Skill

Publish one of Kevin's Pacific Northwest railroad history articles to Substack as @traindewd. The workflow is: pick an unpublished article → read and parse it → adapt the content for Substack → post as a draft → confirm → publish.

## Before You Start

Make a todo list for all tasks in this workflow and work through them one at a time.

---

## One-Time Setup: Configure SUBSTACK_CONNECT_SID

Before this skill can run, `SUBSTACK_CONNECT_SID` must be configured as an environment variable in your Claude Code environment. This only needs to be done once (refresh it when it expires).

### Step 1 — Get the cookie from your browser

1. Log in to [substack.com](https://substack.com) in Chrome or Firefox
2. Open DevTools: **F12** (or right-click → Inspect)
3. Go to **Application** tab → **Storage** → **Cookies** → `https://substack.com`
4. Find the row named **`connect.sid`**
5. Copy the full **Value** (it looks like `s%3A...` — copy everything)

The cookie is valid until you log out of Substack or it expires (typically 30+ days).

### Step 2 — Add it to Claude Code

**In Claude Code on the web (claude.ai/code):**
1. Open your environment settings for this project
2. Add an environment variable: `SUBSTACK_CONNECT_SID` = `<your cookie value>`
3. Save and restart the session

**In Claude Code CLI (local):**
Add to your shell profile or a `.env` file in the project:
```bash
export SUBSTACK_CONNECT_SID="s%3Ayour-cookie-value-here"
```

**Via Claude Code settings.json** (project-level, `.claude/settings.json`):
```json
{
  "env": {
    "SUBSTACK_CONNECT_SID": "s%3Ayour-cookie-value-here"
  }
}
```
Note: Do not commit `settings.json` if it contains the cookie value — add it to `.gitignore`.

### Step 3 — Verify it works

Run the auth check manually to confirm before publishing anything:
```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" \
  -H "Cookie: connect.sid=${SUBSTACK_CONNECT_SID}" \
  "https://substack.com/api/v1/me"
```
`HTTP 200` means you're authenticated and ready to go.

---

## Workflow

### 1. Preflight — Check for Session Cookie

Verify `SUBSTACK_CONNECT_SID` is set in the environment:

```bash
echo ${SUBSTACK_CONNECT_SID:+SET}
```

If the output is empty (not `SET`), **stop immediately** and tell the user to follow the **One-Time Setup** section above.

### 2. Load the Tracking File

Read `published-to-substack.json` from the project root. This records which articles have been pushed to Substack.

```bash
cat /home/user/train_lore/published-to-substack.json 2>/dev/null || echo '{"posts":[]}'
```

If the file doesn't exist, treat it as `{"posts": []}` — it will be created in step 9.

Extract the list of filenames that already have `"status": "published"` in the posts array.

### 3. Select an Article

List the HTML articles in the project:

```bash
ls /home/user/train_lore/*-blog-post.html
```

The five current articles are:
- `deschutes-canyon-railroad-war-blog-post.html`
- `great-big-baked-potato-blog-post.html`
- `john-stevens-marias-pass-blog-post.html`
- `stampede-pass-blog-post.html`
- `wellington-avalanche-blog-post.html`

Cross-reference against the tracking file. Present the user with the unpublished ones (or all of them if none are tracked yet). If the user already named a specific article in their request, use that one.

If the chosen article appears in the tracking file with `"status": "published"`, **warn** the user:
> "This article was already published to Substack on [published_at]. Publish again anyway? (yes/no)"

Do not hard-block — re-publishing a revised version is legitimate.

If all articles are published, report this and stop.

### 4. Read and Parse the HTML File

Read the selected HTML file. Extract three things:

**Title:** Text content of the first `<h1>` tag.

**Subtitle:** Text content of the first `<p>` immediately after the `<h1>`. This opening paragraph doubles as the Substack subtitle. If it is longer than ~120 characters, use only the first sentence (up to the first period).

**Body HTML:** All content starting from the `<h1>` tag through (and including) the closing `</ul>` that ends the Sources & Further Reading section. This includes `<h1>`, `<p>`, `<h2>`, `<blockquote>`, `<hr>`, and `<ul>` tags.

**Strip the following — do not include them in the body:**
- The entire `<head>` block (including inline `<style>`)
- The `<html>` and `<body>` wrapper tags
- The footer `<p><em>Written by Kevin Sotka for meatbagmade.com...</em></p>` paragraph at the bottom
- The `<hr>` separator immediately before that footer paragraph

### 5. Image Handling (Wellington Article Only)

`wellington-avalanche-blog-post.html` contains a large base64-encoded `<img class="featured-image">` element before the `<h1>`. It looks like:
```html
<img class="featured-image" src="data:image/webp;base64,AAAA..." alt="...">
```

**Strip this entire `<img>` tag from the body HTML.** Substack's API does not support base64 image data in post bodies, and it would bloat the payload to several MB.

After publishing, tell the user:
> "The Wellington featured image was stripped from the body (Substack doesn't accept base64 images via API). To add it: open the draft in your Substack editor, click the image placeholder at the top, and upload `images/bakedpotato.png` or the original source image."

For all other articles: no special image handling needed.

### 6. Build the Final Body HTML

Assemble the Substack body:

1. The extracted body HTML (title through sources list, cleaned per steps 4–5)
2. A closing `<hr>` separator
3. This CTA footer paragraph:

```html
<hr>
<p><em>Written by Kevin Sotka. More Pacific Northwest railroad history at <a href="https://meatbagmade.com">meatbagmade.com</a>. Find me on X/Twitter at <a href="https://twitter.com/TrainDewd">@TrainDewd</a>. If you found this interesting, share it with someone who loves trains.</em></p>
```

### 7. Verify Authentication

Before any write operations, confirm the session cookie is valid:

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "Cookie: connect.sid=${SUBSTACK_CONNECT_SID}" \
  "https://substack.com/api/v1/me"
```

- **200**: authenticated — proceed.
- **401 or 403**: stop and tell the user their `SUBSTACK_CONNECT_SID` cookie has expired or is invalid. They need to log in to substack.com, copy a fresh `connect.sid` value, and update the environment variable.
- **Any other status**: report it and stop.

### 8. Create the Draft

Build the JSON payload and POST it to Substack. **Use a temp file for the payload** — do not use shell variable interpolation directly in the `-d` flag, because the HTML body contains quotes, newlines, and special characters that will break the JSON.

Use Python to build the JSON safely:

```bash
python3 -c "
import json, sys

title = sys.argv[1]
subtitle = sys.argv[2]
body = sys.argv[3]

payload = {
    'draft_title': title,
    'draft_subtitle': subtitle,
    'draft_body': body,
    'audience': 'everyone'
}
print(json.dumps(payload))
" "TITLE_HERE" "SUBTITLE_HERE" "BODY_HTML_HERE" > /tmp/substack_payload.json
```

Then POST:

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Cookie: connect.sid=${SUBSTACK_CONNECT_SID}" \
  -d @/tmp/substack_payload.json \
  "https://substack.com/api/v1/post_management/drafts"
```

Capture the full JSON response. On success, extract:
- `id` — the numeric draft ID (needed for the publish call)
- `slug` — the URL slug
- Draft URL: `https://substack.com/@traindewd/p/<slug>`

On failure (non-2xx HTTP or an `error` field in the response body), display the full API error and stop. Do not attempt to publish. The tracking file is not updated for failed drafts.

Clean up: `rm -f /tmp/substack_payload.json`

### 9. Confirm Before Publishing

Show the user a summary:
```
Draft created successfully!
  Title:     [title]
  Subtitle:  [subtitle]
  Draft URL: https://substack.com/@traindewd/p/[slug]
```

Ask: **"Publish now to all subscribers? (yes/no)"**

- If **no**: update `published-to-substack.json` with `status: "draft"` and stop. The draft remains on Substack for manual review and publishing.
- If **yes**: proceed to step 10.

### 10. Publish the Draft

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Cookie: connect.sid=${SUBSTACK_CONNECT_SID}" \
  "https://substack.com/api/v1/post_management/drafts/${DRAFT_ID}/publish"
```

On success (HTTP 200): the post is live.

On failure: display the full API error. The draft still exists on Substack and can be published manually from the dashboard.

### 11. Update the Tracking File

Read the existing `published-to-substack.json`, append a new entry to the `posts` array, and write it back:

```json
{
  "filename": "stampede-pass-blog-post.html",
  "title": "Stampede Pass: The $1,000 Race Through the Mountain",
  "post_id": 12345678,
  "slug": "stampede-pass-the-1000-race-through-the",
  "draft_url": "https://substack.com/@traindewd/p/stampede-pass-the-1000-race-through-the",
  "status": "published",
  "published_at": "2026-06-06T14:30:00Z"
}
```

Use `status: "draft"` if the user chose not to publish in step 9. Use ISO 8601 UTC for `published_at`.

Preserve all existing entries when writing.

### 12. Check the Topic Tracker

Open `pacific-northwest-railroad-topics.md`. Find the entry for the article just published and verify it is marked `[x]`. If it shows `[ ]`, change it to `[x]`. (All 5 current articles should already be `[x]` — this step matters for future articles written and published for the first time.)

---

## Error Reference

| Situation | Action |
|-----------|--------|
| `SUBSTACK_CONNECT_SID` not set | Stop — instruct user to extract cookie from browser DevTools |
| Auth check returns 401/403 | Stop — cookie expired, instruct user to get a fresh one |
| Auth check returns other error | Stop — report HTTP status |
| Draft creation fails | Display full API response, stop, do not update tracking file |
| Publish call fails | Display full API response; note draft still exists on Substack |
| All articles already published | Report and offer to re-publish with explicit confirmation |
| Wellington base64 image | Strip `<img>` tag, warn user to upload manually in editor |
| JSON escaping issues | Always use the Python temp-file approach, never raw shell interpolation |

---

## Wrap Up

End with a summary:

```
Done!
  Article:   [title]
  Status:    Published / Saved as draft
  URL:       [substack url]
  Tracking:  published-to-substack.json updated

[Any warnings, e.g. Wellington image stripped]
[Next step suggestion, e.g. "Share the post link on Twitter @TrainDewd"]
```
