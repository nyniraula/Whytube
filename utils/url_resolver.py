from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from utils import terminal


def get_media_url():
    while True:
        try:
            url = input("the link: ").strip()
            if not url:
                raise ValueError
            break

        except ValueError:
            terminal.clear()
            pass

    return url


def fetch_media_info(config):
    with YoutubeDL(config) as ydl:
        while True:
            try:
                url = get_media_url()
                media_info = ydl.extract_info(url, download=False)
                break

            except DownloadError:
                terminal.clear()
                print("That's a link to what exactly? Try again.")

        return (url, media_info)


def check_if_playlist(url):
    return "list=" in url
