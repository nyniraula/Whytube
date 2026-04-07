import os
import subprocess

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

opts = {"no_warnings": True, "quiet": True}


def get_media_url():
    while True:
        try:
            url = input("Media Url: ").strip()
            if not url:
                raise ValueError
            break

        except ValueError:
            subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
            pass

    return url


def fetch_media_info():
    with YoutubeDL(opts) as ydl:
        while True:
            try:
                url = get_media_url()
                media_info = ydl.extract_info(url, download=False)
                break

            except DownloadError:
                subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
                print("Invalid url, Try again!")

        return media_info


def sanitize_formats(formats):

    sanitized_data = []
    for format in formats:
        ext = format.get("ext")
        vcodec = format.get("vcodec")

        if ext == "mp4" and vcodec.find("av01") >= 0:
            sanitized_data.append(format)

    return sanitized_data


def main():
    media_info = fetch_media_info()
    formats = media_info["formats"]

    downloadable_formats = sanitize_formats(formats)

    print(downloadable_formats)


main()
