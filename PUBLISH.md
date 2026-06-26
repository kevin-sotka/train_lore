# Publish Train Lore to GitHub Pages

The site is ready. The sandbox can't push (no token by design), so run these on **your Mac**,
one time. After this, every `git push` to `main` redeploys the site automatically via the
Actions workflow at `.github/workflows/pages.yml`.

Remote: `https://github.com/kevin-sotka/train_lore`

> **Important:** GitHub Pages is **not available on private repos on the free plan**
> (you'll get `HTTP 422 / "your current plan does not support GitHub Pages"`). The repo
> must be **public**. Step 1 below makes it public.

## 1. Make the repo public

```bash
gh repo edit kevin-sotka/train_lore \
  --visibility public --accept-visibility-change-consequences
```

Or web UI: repo → **Settings** → **Danger Zone** → **Change visibility** → **Public**.

Nothing sensitive lives in this repo (the `ghp_xxx` in `scripts/push-lore.sh` is only a
placeholder in a comment), but note that once public, all files — including
`image-prompts.md`, the backlog, and the helper scripts — are world-readable.

## 2. Commit and push everything

```bash
cd /Users/kevinsotka/Meatbag_Labs/train_lore

# optional cleanup: the old root posts are superseded by the restyled ones in stories/
git rm deschutes-canyon-railroad-war-blog-post.html \
       great-big-baked-potato-blog-post.html \
       john-stevens-marias-pass-blog-post.html \
       stampede-pass-blog-post.html \
       wellington-avalanche-blog-post.html

git add -A
git commit -m "Train Lore: depot-board site + 7 tales + GitHub Pages workflow"
git push origin main
```

If `git push` asks for credentials, use a GitHub Personal Access Token as the password
(or run `gh auth login` first).

## 3. Enable Pages from the Actions workflow (once)

```bash
gh api -X POST repos/kevin-sotka/train_lore/pages -f build_type=workflow
```

Or web UI: repo → **Settings → Pages** → under "Build and deployment",
set **Source = GitHub Actions**.

## 4. Trigger / watch the deploy

Enabling Pages does **not** by itself build the site — a workflow run has to finish first.
If you already pushed before enabling Pages, kick a run manually:

```bash
gh workflow run "Deploy Train Lore to GitHub Pages"   # manual trigger (workflow_dispatch)
gh run watch                                          # follow it to completion
```

When the run is green, the site is live at:

**https://kevin-sotka.github.io/train_lore/**

(Homepage = the depot board `index.html`; tales at `…/train_lore/stories/<slug>.html`.)

> First deploy can take 1–2 minutes after the run goes green, and the URL 404s
> ("There isn't a GitHub Pages site here") until then. Give it a moment and refresh.

## Troubleshooting "There isn't a GitHub Pages site here"

That message = Pages is on, but no successful deploy has published yet. Check in order:

```bash
gh api repos/kevin-sotka/train_lore/pages          # is Pages enabled + what's the source/status?
gh run list --workflow "Deploy Train Lore to GitHub Pages" --limit 5   # did a run happen / pass?
gh run view --log-failed                            # if a run failed, see why
```

Most common fixes:
- **No run yet** → `gh workflow run "Deploy Train Lore to GitHub Pages"`.
- **Run failed on permissions** → confirm repo is public and Settings → Actions →
  "Workflow permissions" allows the GITHUB_TOKEN (the workflow already requests
  `pages: write` + `id-token: write`).
- **Source set to "Deploy from a branch" instead of "GitHub Actions"** → switch it
  (`-f build_type=workflow` above, or the Pages settings dropdown).
- **Still 404 right after green** → wait 1–2 min, hard-refresh.

## Ongoing

- The weekly scheduled task writes a new tale into this repo each Sunday.
- To auto-publish, set up the launchd pusher in `SETUP-mac-pusher.md` (it runs `git push`
  for you) — that push triggers this same Pages workflow and the site updates.
- Drop diorama images into `images/` anytime; the next weekly run wires them in and the
  following push publishes them.
