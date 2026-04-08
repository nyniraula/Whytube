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
# Load download type constants
DOWNLOAD_TYPE = config.get("download_type", "video").lower()
PLAYLIST_DOWNLOAD_TYPE = config.get("playlist_download_type", "video").lower()
PLAYLIST_DOWNLOAD_CAP = config.get("playlist_download_cap", "1080")

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
            url = input("Video url: ").strip()
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


def check_if_playlist(url):
    return "list=" in url


def download_media(fmt, url):
    opts = copy.deepcopy(config)
    opts["format"] = f"{fmt}"

    with YoutubeDL(opts) as ydl:
        ydl.download(url)


def main():

    url, media_info = fetch_media_info()
    title = media_info.get("title")

    # runs if block if url is a playlist
    if check_if_playlist(url):
        print(f"\n[DOWNLOADING PLAYLIST]: {title}")

        if PLAYLIST_DOWNLOAD_TYPE == "audio":
            download_media("bestaudio[ext=m4a]", url)
        else:
            download_media(
                f"bestvideo[height<={PLAYLIST_DOWNLOAD_CAP}]+bestaudio[ext=m4a]", url
            )

        print("\n Finished Playlist download")
        return

    # for normal video
    print(f"\nTitle: {title}\n")

    if DOWNLOAD_TYPE == "audio":
        download_media("bestaudio[ext=m4a]", url)
    else:
        formats = media_info.get("formats")

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

        fmt = f"{format_id}+bestaudio[ext=m4a]"

        download_media(fmt, url)

    print("\nFinished Downloading")


if __name__ == "__main__":
    main()
