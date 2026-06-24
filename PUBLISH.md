# Publish Train Lore to GitHub Pages

The site is ready. The sandbox can't push (no token by design), so run these on **your Mac**,
one time. After this, every `git push` to `main` redeploys the site automatically via the
Actions workflow already added at `.github/workflows/pages.yml`.

Remote: `https://github.com/kevin-sotka/train_lore`

## 1. Commit and push everything

```bash
cd /Users/kevinsotka/Meatbag_Labs/train_lore

# optional cleanup: the old root posts are now superseded by the restyled ones in stories/
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
(or set up the `gh` CLI — see step 2).

## 2. Turn on GitHub Pages (once)

**Easiest — with the GitHub CLI** (`brew install gh` if you don't have it):

```bash
gh auth login          # if not already logged in
gh api -X POST repos/kevin-sotka/train_lore/pages \
  -f build_type=workflow
```

**Or in the web UI:** GitHub → your `train_lore` repo → **Settings → Pages** →
under "Build and deployment", set **Source = GitHub Actions**. Done.

## 3. Watch it deploy

The push triggers the "Deploy Train Lore to GitHub Pages" workflow. Watch it:

```bash
gh run watch
```

or repo → **Actions** tab. When it's green, your site is live at:

**https://kevin-sotka.github.io/train_lore/**

(The homepage is the depot board `index.html`; individual tales live at
`…/train_lore/stories/<slug>.html`.)

## Ongoing

- The weekly scheduled task writes a new tale into this repo each Sunday.
- To auto-publish those, set up the launchd pusher in `SETUP-mac-pusher.md` (it runs
  `git push` for you) — that push will trigger this same Pages workflow and the site updates.
- Drop diorama images into `images/` anytime; the next weekly run wires them in and the
  following push publishes them.
