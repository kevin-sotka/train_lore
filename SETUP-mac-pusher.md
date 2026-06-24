# Train Lore — Mac auto-push setup (one time)

The weekly scheduled task writes files into this repo but **cannot push** (the sandbox has no
GitHub token, by design). A small launchd job on your Mac does the push — same pattern as the
Gridiron Gazette's `com.gridirongazette.pushnews`.

You only do this once. After that, every weekly tale publishes itself.

---

## 1. Make a GitHub token (if you don't have one for this repo)

GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained token**.
Give it access to **only** the `train_lore` repo, with **Contents: Read and write**. Copy the token.

## 2. Store the token in the macOS keychain

Open Terminal and run (paste your real token in place of `ghp_xxx`):

```bash
security add-generic-password -a "$USER" -s "train_lore_github_token" -w "ghp_xxx"
```

The push script reads it from here — the token never lives in a file.

## 3. Make the push script executable

```bash
chmod +x /Users/kevinsotka/Meatbag_Labs/train_lore/scripts/push-lore.sh
```

Test it by hand once (it'll say "no changes" or push whatever's pending):

```bash
/Users/kevinsotka/Meatbag_Labs/train_lore/scripts/push-lore.sh
```

If `GH_USER` / `GH_REPO` in the script don't match your remote, fix them. Current remote:
`https://github.com/kevin-sotka/train_lore.git`

## 4. Schedule it with launchd

The weekly task runs Sunday ~9:03 AM. Have the pusher run a bit later, say **Sunday 9:30 AM**,
so the files are already written. Create this file:

`~/Library/LaunchAgents/com.trainlore.pushlore.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.trainlore.pushlore</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>/Users/kevinsotka/Meatbag_Labs/train_lore/scripts/push-lore.sh</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Weekday</key><integer>0</integer>   <!-- 0 = Sunday -->
    <key>Hour</key><integer>9</integer>
    <key>Minute</key><integer>30</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>/tmp/trainlore-push.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/trainlore-push.err</string>
</dict>
</plist>
```

Load it:

```bash
launchctl unload ~/Library/LaunchAgents/com.trainlore.pushlore.plist 2>/dev/null
launchctl load   ~/Library/LaunchAgents/com.trainlore.pushlore.plist
```

Check logs after a run: `cat /tmp/trainlore-push.log`

---

## How the weekly cycle flows

1. **Sunday ~9:03 AM** — scheduled task picks the next backlog topic, writes
   `stories/<slug>.html`, appends a diorama prompt to `image-prompts.md`, adds the story to
   `stories.json`, rebuilds `index.html`, and checks the topic off the backlog.
2. **Sunday ~9:30 AM** — this launchd job commits + pushes. Site updates.
3. **Whenever you feel like it** — open `image-prompts.md`, generate the diorama image in
   ChatGPT, save it with the **exact filename** listed, drop it in `images/`. The *next*
   weekly run wires it into the page and the board automatically (until then a clean
   "image pending" placeholder shows — never a broken image).
