from yt_dlp import YoutubeDL


def start(fmt, url, config):
    config["format"] = f"{fmt}"

    print(config)
    with YoutubeDL(config) as ydl:
        ydl.download(url)
