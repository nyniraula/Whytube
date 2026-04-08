import copy
import json
import os
import subprocess
from pathlib import Path

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from utils import ranking, resolver

# Loads the config from the json file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Sets the download Folder
home_folder = Path.home()
downloads = home_folder / "Downloads"  # pathlib join those into single path
config["outtmpl"] = str(
    downloads / "%(title)s - %(uploader)s.%(ext)s"
)  # updates save path to downloads dir


def clearTerminal():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)


def get_media_url():
    while True:
        try:
            url = input("Media Url: ").strip()
            if not url:
                raise ValueError
            break

        except ValueError:
            clearTerminal()
            pass

    return url


def fetch_media_info():
    with YoutubeDL(config) as ydl:
        while True:
            try:
                url = get_media_url()
                media_info = ydl.extract_info(url, download=False)
                break

            except DownloadError:
                clearTerminal()
                print("Invalid url, Try again!")

        return (url, media_info)


def download_media(format_id, url):
    opts = copy.deepcopy(config)
    opts["format"] = f"{format_id}+bestaudio[ext=m4a]"

    with YoutubeDL(opts) as ydl:
        ydl.download(url)


def main():
    url, media_info = fetch_media_info()
    title = media_info.get("title")
    formats = media_info.get("formats")

    print(f"\nTitle: {title}\n")
    print("Choose a resolution to download: \n")

    ranked_data = ranking.rank_format_options(formats)

    downloadable_formats = resolver.resolve_format_options(ranked_data, formats)

    for i, f in enumerate(downloadable_formats):
        print(f"{i + 1}. {f.get('format_note')} ({f.get('resolution')})")

    while True:
        try:
            choice = int(input(": "))
            if choice < 1 or choice > len(downloadable_formats):
                raise ValueError("Choice exceeds the limiting capacity")

            break

        except ValueError:
            # clearTerminal()
            pass

    format_id = downloadable_formats[choice - 1].get("format_id")

    download_media(format_id, url)

    print("\nFinished Downloading")


if __name__ == "__main__":
    main()
