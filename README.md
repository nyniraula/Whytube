<div align="center">

# Whytube

##### Getting you the absolute best YouTube quality without the headache, bro.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org) [![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-green.svg?style=for-the-badge&logo=ffmpeg&logoColor=white)](https://ffmpeg.org) [![uv](https://img.shields.io/badge/uv-Recommended-purple.svg?style=for-the-badge)](https://github.com/astral-sh/uv)
[![Node.js](https://img.shields.io/badge/Node.js-Ready-339933.svg?style=for-the-badge&logo=nodedotjs&logoColor=white)](https://nodejs.org/) [![Deno](https://img.shields.io/badge/Deno-Ready-000000.svg?style=for-the-badge&logo=deno&logoColor=white)](https://deno.land/)

<img alt="Mike Wazowoski" height="280" src="/assets/whytube_banner.png" />

</div>

</div>

## ⇁ TOC

- [Why This Exists](#-why-this-exists)
- [How We Fix It](#-how-we-fix-it)
- [What You Need](#-what-you-need)
- [Quick Setup](#-quick-setup)
- [Firing It Up](#-firing-it-up)
- [Configs & Tweaks](#-configs--tweaks)
- [Under the Hood](#-under-the-hood)
- [Heads Up](#-heads-up)

## ⇁ Why This Exists

Parsing format IDs just to get decent video and audio sucks. Most CLI tools either hand you a trash 360p fallback or force you to write a paragraph of arguments just for a clean 1080p MP4. We needed something smarter and faster.

## ⇁ How We Fix It

**Whytube (WIP)** doesn't settle. It ranks every single stream and automatically snags the absolute best one based on:

1. **Resolution** — higher is always better.
2. **Codec** — preferred order: `av01 → vp9 → avc1`.
3. **Container** — preferred order: `mp4 → webm`.

If the top pick is missing, it gracefully falls back. We also enforce a strict 720p floor so your eyes don't bleed (unless it's literally the only resolution left).

## ⇁ What You Need

- **Python 3.10+**
- **[FFmpeg](https://ffmpeg.org/)** — Required for merging video/audio streams.
- **[uv](https://github.com/astral-sh/uv)** — Highly recommended for package management.
- **Node.js or Deno** — Needed to bypass YouTube's JS challenges.

## ⇁ Quick Setup

Grab the repo and install dependencies in one go:

```bash
git clone https://github.com/nyniraula/Whytube.git
cd whytube
uv sync

# `pip install yt-dlp[default]` if you're old school
```

## ⇁ Firing It Up

To get started, just run:

```bash
uv run main.py
```

_(Whytube auto-detects your Node/Deno setup, so no manual path config needed.)_

### Single Video

1. Paste the URL when prompted.
2. Pick a resolution (caps at 720p minimum).
3. Done. Video saves to `~/Downloads/WT_Downloads/`.

### Playlists

Paste a playlist URL and Whytube handles it on autopilot. No per-video prompts. Caps at 1080p by default so it doesn't nuke your storage.

### Audio Only

Just want the tunes? Change `download_type` or `playlist_download_type` to `"audio"` in `config.json` to rip straight to `.m4a`.

## ⇁ Configs & Tweaks

Whytube is fully customizable. Here's your `config.json`:

```json
{
  "no_warnings": true,
  "quiet": true,
  "merge_output_format": "mp4",
  "outtmpl": "%(title)s - %(uploader)s.%(ext)s",
  "download_type": "video",
  "writesubtitles": false,
  "writeautomaticsub": true,
  "subtitleslangs": ["en"],
  "subtitlesformat": "srt/ass/vtt",
  "playlist_download_type": "video",
  "playlist_download_cap": "1080",
  "postprocessor_args": {
    "ffmpeg": ["-c:a", "aac"]
  },
  "writethumbnail": true,
  "embedthumbnail": true,
  "postprocessors": [
    {
      "key": "EmbedThumbnail"
    }
  ],
  "js_runtimes": {
    "deno": { "path": null },
    "node": { "path": null }
  }
}
```

> [!NOTE]
> `js_runtimes` paths auto-update at startup. Also, editing `outtmpl` only changes the _filename_ template—files will always route to `~/Downloads/WT_Downloads/`.

### Subtitles

- `writeautomaticsub`: Grabs auto-generated subs.
- `writesubtitles`: Grabs manually uploaded subs.
- `subtitleslangs`: Array of languages, defaults to `["en"]`.
- Disable entirely by setting both write flags to `false`.

### Thumbnails

Thumbnails are automatically embedded into the `.mp4` and leftover images are deleted. To turn this off, set `writethumbnail` and `embedthumbnail` to `false` and empty the `postprocessors` array.

## ⇁ Under the Hood

| Module               | What it actually does                                        |
| -------------------- | ------------------------------------------------------------ |
| `source_handler.py`  | Loads config and preps the download directory.               |
| `URLresolver.py`     | Validates URLs and fetches media info.                       |
| `MediaPipeline.py`   | The traffic cop — routes to video, audio, or playlist logic. |
| `downloader.py`      | Wraps yt-dlp and fires off the download.                     |
| `format_ranking.py`  | Ranks formats based on codec and container preferences.      |
| `format_resolver.py` | Cleans up ranked formats and enforces the 720p floor.        |
| `dependencies.py`    | Auto-detects FFmpeg and JS runtimes.                         |
| `cleanup.py`         | Wipes out leftover thumbnail files after a run.              |
| `terminal.py`        | Cross-platform terminal clear to keep the UI clean.          |

## ⇁ Heads Up

- Video and audio stream separately and are merged via FFmpeg.
- Audio is always re-encoded to AAC for maximum compatibility.
- **FFmpeg is mandatory.** The script will exit if it can't find it.
- You **must** have a JS runtime installed (Node.js or Deno) to bypass anti-bot checks.
- Configs reload on every download loop! You can tweak `config.json` while the app is running and it catches the updates instantly.
