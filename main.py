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
            print("Invalid URL pattern")

    return url


def fetch_media_info():
    with YoutubeDL(opts) as ydl:
        while True:
            try:
                url = get_media_url()
                media_info = ydl.extract_info(url, download=False)
                break

            except DownloadError:
                print("Invalid url, Try again!")

        return media_info
    

    
