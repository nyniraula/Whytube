from utils import MediaPipeline, URLresolver, cleanup, source_handler


def main():
    # TODO: FFMPEG CHECK and fallbacks

    # Loads the config from the json file and also manages output dir and path
    config, DOWNLOAD_TYPE, PLAYLIST_DOWNLOAD_TYPE, PLAYLIST_DOWNLOAD_CAP = (
        source_handler.setup()
    )

    # Program Loop
    while True:
        url, media_info = URLresolver.fetch_media_info(config)
        title = media_info.get("title")

        # runs block if url is a playlist
        if URLresolver.check_if_playlist(url):
            MediaPipeline.handle_playlist(
                title, url, config, PLAYLIST_DOWNLOAD_TYPE, PLAYLIST_DOWNLOAD_CAP
            )
        else:
            MediaPipeline.handle_video(
                title, url, config, media_info, DOWNLOAD_TYPE
            )  # for normal video

        print("\nFinished Downloading")

        # Runs cleanup function
        cleanup.run()

        # download another prompt to re-loop
        quit_status = input("\nDownload Another? [y/N]: ")

        if not quit_status.lower() == "y":
            print("Exit Command Detected! Halting Execution")
            break


if __name__ == "__main__":
    main()
