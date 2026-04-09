# Whytube

A clean command-line YouTube downloader that intelligently selects the best available quality using codec and container preference rankings. (WIP)

## How it works

Whytube doesn't just grab any format — it ranks every available stream by:

1. **Resolution** — higher is better
2. **Codec** — preferred order: `av01 → vp9 → avc1`
3. **Container** — preferred order: `mp4 → webm`

If your preferred codec or container isn't available, it gracefully falls back to the next best option. Only resolutions 720p and above are shown (unless none are available).

## Requirements

- Python 3.10+
- [FFmpeg](https://ffmpeg.org/) — required for merging video and audio streams
- [uv](https://github.com/astral-sh/uv) — recommended package manager
- Node.js or Deno — required for solving YouTube's JS challenges

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/whytube.git
cd whytube
```

### 2. Install dependencies

```bash
uv sync
```

> [!TIP]
> If you prefer pip: `pip install yt-dlp[default]`

### 3. Run

```bash
uv run main.py
```

Whytube will automatically detect your Node.js or Deno installation and configure itself. No manual path setup needed.

## Usage

### Single video

1. Paste a YouTube URL when prompted
2. Pick a resolution from the list (720p and above, falls back to lower if unavailable)
3. Done — video saves to `~/Downloads/WT_Downloads/`

### Playlist

Paste a playlist URL and Whytube handles the rest automatically — no per-video prompts. Caps at 1080p by default (configurable).

### Audio

Set `download_type` or `playlist_download_type` to `"audio"` in `config.json` to download audio-only as `.m4a`.

## Module breakdown

| Module               | What it does                                                 |
| -------------------- | ------------------------------------------------------------ |
| `source_handler.py`  | Loads config, sets up the download directory                 |
| `URLresolver.py`     | Handles URL input, validates it, fetches media info          |
| `MediaPipeline.py`   | Routes to the right handler — video, audio, or playlist      |
| `downloader.py`      | Wraps yt-dlp's YoutubeDL and triggers the download           |
| `format_ranking.py`  | Ranks available formats by codec and container preference    |
| `format_resolver.py` | Deduplicates and filters ranked formats, enforces 720p floor |
| `dependencies.py`    | Checks for FFmpeg, detects and configures JS runtime         |
| `cleanup.py`         | Removes leftover thumbnail files after each download         |
| `terminal.py`        | Cross-platform terminal clear                                |

## Config

Full `config.json` for reference:

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
> `js_runtimes` paths are automatically detected and updated at startup — you don't need to set these manually.

> [!WARNING]
> `outtmpl` is overridden at runtime to save files in `~/Downloads/WT_Downloads/`. Editing it in `config.json` only changes the filename template, not the folder.

## Download types

Control what gets downloaded via these keys in `config.json`:

- `download_type` — applies to single video URLs. Set to `"video"` or `"audio"`
- `playlist_download_type` — applies to playlist URLs. Set to `"video"` or `"audio"`

> [!NOTE]
> If any key is missing or set to an unrecognised value, it defaults to `"video"`.

## Subtitles

Whytube can download a separate subtitle file alongside the video. Controlled via these keys in `config.json`:

- `writeautomaticsub` — downloads auto-generated subtitles. On by default. Works on almost every video
- `writesubtitles` — downloads manually uploaded subtitles if the creator provided them
- `subtitleslangs` — list of language tracks to download. Defaults to `["en"]`
- `subtitlesformat` — preferred format. `srt/ass/vtt` tries each in order, falling back if unavailable

```json
"writesubtitles": false,
"writeautomaticsub": true,
"subtitleslangs": ["en"],
"subtitlesformat": "srt/ass/vtt"
```

> [!NOTE]
> With the default config you'll get one `.srt` file for almost every video. Enabling both `writesubtitles` and `writeautomaticsub` may produce two subtitle files on videos that have both manual and auto-generated tracks.

> [!TIP]
> To disable subtitles entirely, set both `writesubtitles` and `writeautomaticsub` to `false`.

## Thumbnails

Whytube embeds thumbnails directly into the video file and cleans up the leftover image file automatically after each download. No stray `.jpg` or `.webp` files.

To disable thumbnail embedding:

```json
"writethumbnail": false,
"embedthumbnail": false,
"postprocessors": []
```

## Notes

- Video and audio are downloaded as separate streams and merged via FFmpeg into a final `.mp4`
- Audio is re-encoded to AAC for maximum compatibility
- FFmpeg is required — Whytube will exit with a clear error message if it's not found
- JS runtime (Node.js or Deno) is required for solving YouTube's challenge — Whytube auto-detects whichever is installed
- Config is reloaded every download loop, so changes to `config.json` take effect without restarting
