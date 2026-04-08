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

1. Paste a YouTube URL when prompted
2. Pick a resolution from the list
3. Done — video saves to your `~/Downloads` folder

## Config

Full `config.json` for reference:

```json
{
  "no_warnings": true,
  "quiet": false,
  "merge_output_format": "mp4",
  "outtmpl": "%(title)s.%(ext)s - %(uploader)s",
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

## Notes

- Video and audio are downloaded as separate streams and merged via FFmpeg into a final `.mp4`
- Audio is re-encoded to AAC for maximum compatibility
- The merge step may take a few seconds depending on file size — this is normal
