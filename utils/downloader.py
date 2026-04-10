from yt_dlp import YoutubeDL


def start(fmt, url, config):
    config["format"] = f"{fmt}"

    with YoutubeDL(config) as ydl:
        print("\nBribing YouTube's servers...", end="\n")

        ydl.download(url)
