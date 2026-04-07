# Whytube

A simple command-line tool to download YouTube videos in your preferred resolution. (WIP)

## Requirements

- Python 3.10+ (though it lists 3.14 in uv.lock)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/) (required for merging video and audio)
- uv as a package manager (You can still run it with pip but thats on you to configure)

```bash
uv add yt-dlp[default]
```

## Setup

1. Clone the repo
2. Configure your download preferences in `config.json`
3. sync packages with `uv sync` command

## Usage

```bash
uv run main.py
```

You'll be prompted to paste a URL, then choose a resolution from the available options.

## Notes

- Currently only downloads `mp4` formats encoded with `av01` codec
- Merges selected video stream with best available audio via FFmpeg
