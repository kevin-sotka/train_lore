#!/usr/bin/env python3
"""Give every tale a voice: generate an ElevenLabs narration per story and
put an audio player at the top of the story page.

For each story in stories.json that has no audio yet:
  1. pick the next voice in the six-voice rotation (oldest tale first),
  2. read the tale aloud (title + everything before the first <hr>; the
     "What Really Happened" record and sources are not narrated),
  3. save audio/<slug>.mp3,
  4. insert the player under the byline and record voice_id + audio in stories.json.

Idempotent: stories that already have audio are skipped, so it is safe to run
after each weekly tale. Standard library only; needs ffmpeg to join chunks.

Usage:
    python3 make_narration.py --dry-run          # character counts + voice plan, no API calls
    python3 make_narration.py                    # narrate everything still silent
    python3 make_narration.py --only hillyard-hills-yard
    python3 make_narration.py --latest 6 --max-credits 30000
    python3 make_narration.py --wire-only        # just (re)insert players for existing mp3s

The API key comes from the ELEVENLABS_API_KEY environment variable, or failing
that from a .env file next to this script or in ../Lookout Logs/. Never commit a key.
"""
import argparse, html, json, os, re, subprocess, sys, tempfile, time
import urllib.error, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
STORIES_DIR = os.path.join(ROOT, "stories")
AUDIO_DIR = os.path.join(ROOT, "audio")
SJ_PATH = os.path.join(ROOT, "stories.json")

VOICES = [
    "LNV6ahDtkAOqwn1X3R7a",
    "H2CgnIux8C0XLWQ97uPA",
    "a5zfmqTslZJBP0jutmVY",
    "HJkTIwTKRE1PiQuSYBRV",
    "Rr2hEGqGe4GdbJo9ta2k",
    "bJ6Nel1LlZx0UKyZhsk0",
]
MODEL = os.environ.get("LORE_TTS_MODEL", "eleven_v4")
OUTPUT_FORMAT = "mp3_44100_64"   # plenty for speech, about 3 MB per tale
CHUNK_CHARS = 2500               # stay well under per-request text limits

PLAYER_RE = re.compile(r'\n?[ \t]*<div class="narration">.*?</div>\n?', re.DOTALL)


def load_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key:
        return key
    for path in (os.path.join(ROOT, ".env"),
                 os.path.join(ROOT, "..", "Lookout Logs", ".env")):
        if os.path.exists(path):
            for line in open(path):
                if line.strip().startswith("ELEVENLABS_API_KEY="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
    sys.exit("No ELEVENLABS_API_KEY found (env var or .env).")


def narration_blocks(page_src):
    """Spoken text of a story page, as a list of paragraphs."""
    art = re.search(r"<article>(.*?)</article>", page_src, re.DOTALL).group(1)
    tale = art.split("<hr>", 1)[0]
    tale = PLAYER_RE.sub("\n", tale)
    blocks = []
    for m in re.finditer(r"<(h1|h2|p|blockquote)(\s[^>]*)?>(.*?)</\1>", tale, re.DOTALL):
        tag, attrs, inner = m.group(1), m.group(2) or "", m.group(3)
        if "byline" in attrs:
            continue
        text = html.unescape(re.sub(r"<[^>]+>", "", inner))
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        if tag in ("h1", "h2") and text[-1] not in ".!?":
            text += "."
        blocks.append(text)
    return blocks


def chunks_of(blocks):
    out, cur = [], ""
    for b in blocks:
        if cur and len(cur) + len(b) + 2 > CHUNK_CHARS:
            out.append(cur)
            cur = b
        else:
            cur = f"{cur}\n\n{b}" if cur else b
    if cur:
        out.append(cur)
    return out


def tts(key, voice, text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format={OUTPUT_FORMAT}"
    payload = {"text": text, "model_id": MODEL}
    for attempt in range(4):
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "audio/mpeg")
        req.add_header("xi-api-key", key)
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                return resp.read(), int(resp.headers.get("character-cost") or 0)
        except urllib.error.HTTPError as err:
            body = err.read().decode("utf-8", "replace")[:400]
            if err.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            raise RuntimeError(f"HTTP {err.code}: {body}") from None
        except urllib.error.URLError as err:
            if attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            raise RuntimeError(f"Network error: {err.reason}") from None


def join_mp3(parts, dest):
    if len(parts) == 1:
        os.replace(parts[0], dest)
        return
    listing = dest + ".txt"
    with open(listing, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", listing, "-c:a", "libmp3lame", "-b:a", "64k", "-ac", "1", dest],
                   check=True)
    os.remove(listing)


def wire_player(slug):
    """Insert (or refresh) the audio player under the byline."""
    page = os.path.join(STORIES_DIR, f"{slug}.html")
    src = PLAYER_RE.sub("\n", open(page).read())
    player = (
        '\n    <div class="narration">\n'
        '      <span class="narration-label">Hear the tale told</span>\n'
        f'      <audio controls preload="none" src="../audio/{html.escape(slug)}.mp3"></audio>\n'
        '    </div>\n'
    )
    new, n = re.subn(r'(<p class="byline">.*?</p>)\n?', lambda m: m.group(1) + player, src,
                     count=1, flags=re.DOTALL)
    if n != 1:
        raise RuntimeError(f"{slug}: no byline to hang the player on")
    with open(page, "w") as f:
        f.write(new)


def main():
    ap = argparse.ArgumentParser(description="Narrate Train Lore tales with ElevenLabs")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--wire-only", action="store_true")
    ap.add_argument("--only", help="comma-separated slugs")
    ap.add_argument("--latest", type=int, help="only the N most recent tales")
    ap.add_argument("--max-credits", type=int, default=0,
                    help="stop before starting a tale once this many credits are spent")
    args = ap.parse_args()

    data = json.load(open(SJ_PATH))
    stories = sorted(data["stories"], key=lambda s: s.get("date", ""))

    # Voice rotation: oldest tale gets voice 1, then round the six. A voice
    # already recorded in stories.json is kept; new tales continue the rotation.
    nxt = 0
    for s in stories:
        if s.get("voice_id") in VOICES:
            nxt = (VOICES.index(s["voice_id"]) + 1) % len(VOICES)
        else:
            s["_voice"] = VOICES[nxt]
            nxt = (nxt + 1) % len(VOICES)

    def save():
        clean = {**data, "stories": [{k: v for k, v in s.items() if not k.startswith("_")}
                                     for s in data["stories"]]}
        with open(SJ_PATH, "w") as f:
            json.dump(clean, f, indent=2)
            f.write("\n")

    only = set(args.only.split(",")) if args.only else None
    if args.latest:
        latest = {s["slug"] for s in stories[-args.latest:]}
        only = latest if only is None else only & latest
    credits = 0
    os.makedirs(AUDIO_DIR, exist_ok=True)
    key = None
    total = 0
    for s in stories:
        slug = s["slug"]
        if only and slug not in only:
            continue
        mp3 = os.path.join(AUDIO_DIR, f"{slug}.mp3")
        voice = s.get("voice_id") or s["_voice"]
        blocks = narration_blocks(open(os.path.join(STORIES_DIR, f"{slug}.html")).read())
        parts = chunks_of(blocks)
        chars = sum(len(p) for p in parts)

        if os.path.exists(mp3):
            if not args.dry_run:
                wire_player(slug)
                s["voice_id"], s["audio"] = voice, f"audio/{slug}.mp3"
                save()
            print(f"  have   {slug}")
            continue
        total += chars
        if args.dry_run or args.wire_only:
            print(f"  todo   {slug:48s} {chars:6d} chars  {len(parts)} chunk(s)  voice {voice}")
            continue

        if args.max_credits and credits >= args.max_credits:
            print(f"  stop   credit cap reached ({credits}); {slug} left silent")
            break
        key = key or load_key()
        print(f"  speak  {slug} ({chars} chars, voice {voice})", flush=True)
        with tempfile.TemporaryDirectory() as tmp:
            files = []
            for i, text in enumerate(parts):
                p = os.path.join(tmp, f"{i:02d}.mp3")
                audio, cost = tts(key, voice, text)
                credits += cost
                with open(p, "wb") as f:
                    f.write(audio)
                files.append(p)
            join_mp3(files, mp3)
        print(f"         {credits} credits so far", flush=True)
        wire_player(slug)
        s["voice_id"], s["audio"] = voice, f"audio/{slug}.mp3"
        save()

    print(f"{'would send' if args.dry_run or args.wire_only else 'sent'} {total} characters"
          + (f", charged {credits} credits" if credits else ""))


if __name__ == "__main__":
    main()
