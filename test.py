from yt_dlp import YoutubeDL

opts = {"quiet": True, "no_warnings": True, "format": "399+bestaudio"}

url = input("URL?: ")

li = []
with YoutubeDL(opts) as ydl:
    ydl.download(url)
