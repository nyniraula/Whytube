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

### 3. Configure Node.js path (for JS challenge solving)

Open `config.json` and update the `node` path under `js_runtimes` to match your Node.js installation:

```json
"js_runtimes": {
  "node": {
    "path": "C:\\Program Files\\nodejs\\node.exe"
  }
}
```

Find your Node path with `where node` (Windows) or `which node` (Mac/Linux).

### 4. Run

```bash
uv run main.py
```

## Usage

### Single video

1. Paste a YouTube URL when prompted
2. Pick a resolution from the list (720p and above, provides lower res when >720 unavailable)
3. Done — video saves to your `~/Downloads` folder

### Playlist

Paste a playlist URL and Whytube handles the rest automatically — no per-video prompts. Caps at 1080p by default (configurable).

- `playlist_download_cap` — maximum resolution for playlist video downloads. Accepts height values only: `"720"`, `"1080"`, `"1440"`, `"2160"` etc. yt-dlp will pick the best available quality at or below that cap. Defaults to `"1080"` if missing.

```json
"playlist_download_cap": "1080"
```

## Download types

Control what gets downloaded via these keys in `config.json`:

- `download_type` — applies to single video URLs. Set to `"video"` or `"audio"`
- `playlist_download_type` — applies to playlist URLs. Set to `"video"` or `"audio"`

> [!NOTE]
> If any key is missing or set to an unrecognised value, it defaults to `"video"`.

```json
"download_type": "video",
"playlist_download_type": "audio"
```

## Subtitles

Whytube can download a separate subtitle file alongside the video. Controlled via these keys in `config.json`:

- `writeautomaticsub` — downloads auto-generated subtitles (YouTube's AI captions). On by default. Works on almost every video
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
> With the default config, you'll get one `.srt` file for almost every video. Enabling both `writesubtitles` and `writeautomaticsub` may produce two subtitle files on videos that have both manual and auto-generated tracks.

> [!TIP]
> To disable subtitles entirely, set both `writesubtitles` and `writeautomaticsub` to `false`.

## Config

Full `config.json` for reference:

```json
{
  "no_warnings": true,
  "quiet": true,

  //Output config
  "merge_output_format": "mp4",
  "outtmpl": "%(title)s - %(uploader)s.%(ext)s",
  "download_type": "video",

  //Subtitle Config
  "writesubtitles": false,
  "writeautomaticsub": true,
  "subtitleslangs": ["en"],
  "subtitlesformat": "srt/ass/vtt",

  //Playlist Config
  "playlist_download_type": "audio",
  "playlist_download_cap": "1080",

  
  "postprocessor_args": {
    "ffmpeg": ["-c:a", "aac"]
  },
  "js_runtimes": {
    "deno": {
      "path": null
    },
    "node": {
      "path": "C:\\Program Files\\nodejs\\node.exe"
    }
  }
}
```

> [!WARNING]
> `outtmpl` is overridden at runtime to save files in your `~/Downloads` folder. Editing it in `config.json` has no effect unless you modify the path in `main.py`.

## Notes

- Video and audio are downloaded as separate streams and merged via FFmpeg into a final `.mp4`
- Audio is re-encoded to AAC for maximum compatibility
- The merge step may take a few seconds depending on file size — this is normal
- Playlist downloads default to best available quality up to 1080p with no user interaction required
