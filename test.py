import json

from yt_dlp import YoutubeDL

opts = {"quiet": True, "no_warnings": True}

url = input("URL?: ")

li = []
with YoutubeDL(opts) as ydl, open("info.json", "w") as file:
    info = ydl.extract_info(url, download=False)
    formats = info["formats"]
    for f in formats:
        if f["ext"] == "mp4" and f["vcodec"].find("av01") >= 0:
            print(f.get("format_id"), f.get("resolution"), f.get("ext"))
            li.append(f)

    json.dump(li, file, indent=2)
