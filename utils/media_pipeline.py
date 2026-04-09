from utils import downloader, format_ranking, format_resolver


def handle_audio(url, config):
    config.update(
        {
            "writesubtitles": False,
            "writeautomaticsub": False,
            "writethumbnail": False,
            "embedthumbnail": False,
            "postprocessors": [],
        }
    )
    downloader.start("bestaudio[ext=m4a]", url, config)


def handle_video(title, url, config, media_info, DOWNLOAD_TYPE):
    print(f"\nTitle: {title}\n")

    if DOWNLOAD_TYPE == "audio":
        handle_audio(url, config)
    else:
        formats = media_info.get("formats")
        print("Choose a resolution to download: \n")
        ranked_data = format_ranking.rank_format_options(formats)
        downloadable_formats = format_resolver.resolve_format_options(
            ranked_data, formats
        )

        for i, f in enumerate(downloadable_formats):
            print(f"{i + 1}. {f.get('format_note')} ({f.get('resolution')})")

        while True:
            try:
                choice = int(input(": "))
                if choice < 1 or choice > len(downloadable_formats):
                    raise ValueError("Choice exceeds the limiting capacity")
                break
            except ValueError:
                # terminal.clear()
                pass

        format_id = downloadable_formats[choice - 1].get("format_id")
        fmt = f"{format_id}+bestaudio[ext=m4a]"
        downloader.start(fmt, url, config)


def handle_playlist(title, url, config, PLAYLIST_DOWNLOAD_TYPE, PLAYLIST_DOWNLOAD_CAP):
    print(f"\n[DOWNLOADING PLAYLIST]: {title}")

    if PLAYLIST_DOWNLOAD_TYPE == "audio":
        handle_audio(url, config)
    else:
        fmt = f"bestvideo[height<={PLAYLIST_DOWNLOAD_CAP}]+bestaudio[ext=m4a]"
        downloader.start(fmt, url, config)
