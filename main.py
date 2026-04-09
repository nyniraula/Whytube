import copy

from yt_dlp import YoutubeDL

from utils import URLresolver, format_ranking, format_resolver, source_handler, terminal

# Loads the config from the json file and also manages output dir and path
config, DOWNLOAD_TYPE, PLAYLIST_DOWNLOAD_TYPE, PLAYLIST_DOWNLOAD_CAP = (
    source_handler.setup()
)


def download_media(fmt, url):
    opts = copy.deepcopy(config)
    opts["format"] = f"{fmt}"

    with YoutubeDL(opts) as ydl:
        ydl.download(url)


def main():

    # TODO: Organize CODE STRUCTURE
    # TODO: FFMPEG CHECK and fallbacks

    while True:
        url, media_info = URLresolver.fetch_media_info(config)
        title = media_info.get("title")

        # runs if block if url is a playlist
        if URLresolver.check_if_playlist(url):
            print(f"\n[DOWNLOADING PLAYLIST]: {title}")

            if PLAYLIST_DOWNLOAD_TYPE == "audio":
                download_media("bestaudio[ext=m4a]", url)
            else:
                download_media(
                    f"bestvideo[height<={PLAYLIST_DOWNLOAD_CAP}]+bestaudio[ext=m4a]",
                    url,
                )
        else:
            # for normal video
            print(f"\nTitle: {title}\n")

            if DOWNLOAD_TYPE == "audio":
                download_media("bestaudio[ext=m4a]", url)
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

                download_media(fmt, url)

        print("\nFinished Downloading")

        # Download Another Prompt
        quit_status = input("\nDownload Another? [y/N]: ")

        if not quit_status.lower() == "y":
            print("System Shutting Down")
            break

        terminal.clear()


if __name__ == "__main__":
    main()
