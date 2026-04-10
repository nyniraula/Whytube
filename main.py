from time import sleep

from utils import cleanup, dependencies, media_pipeline, source_handler, url_resolver


def main():
    # check for ffmpeg:
    if not dependencies.ffmpeg_exists():
        print("FFmpeg not found. Genuinely how?")
        return

    # manage js_runtime_config
    dependencies.config_js_runtime()

    # Program Loop
    while True:
        # Loads the config from the json file and also manages output dir and path
        config, DOWNLOAD_TYPE, PLAYLIST_DOWNLOAD_TYPE, PLAYLIST_DOWNLOAD_CAP = (
            source_handler.setup()
        )

        url, media_info = url_resolver.fetch_media_info(config)
        title = media_info.get("title")

        # runs block if url is a playlist
        if url_resolver.check_if_playlist(url):
            media_pipeline.handle_playlist(
                title, url, config, PLAYLIST_DOWNLOAD_TYPE, PLAYLIST_DOWNLOAD_CAP
            )
        else:
            media_pipeline.handle_video(
                title, url, config, media_info, DOWNLOAD_TYPE
            )  # for normal video

        print("\nDone. Go touch grass.")

        # Runs cleanup function
        cleanup.run()

        sleep(1)

        # download another prompt to re-loop
        quit_status = input(
            "\nYour storage called. It's crying. Download another? [y/N]: "
        )

        if not quit_status.lower() == "y":
            print("\nCtrl+C. The last resort of a broken man. Goodbye.")
            break


if __name__ == "__main__":
    main()
