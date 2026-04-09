import json
from pathlib import Path


def set_output_path(config):
    WT_dowload_dir = Path.home() / "Downloads" / "WT_Downloads"

    # Fallback: Create Download Directory, if it already exists -> leave it as is (exist_ok=True), also checks for "WT_Download" folder inside downloads. Just creates what is missing, doesnt touch if
    WT_dowload_dir.mkdir(exist_ok=True, parents=True)

    config["outtmpl"] = str(WT_dowload_dir / config["outtmpl"])

    return config


def setup():
    with open("config.json", "r") as config_file:
        config = set_output_path(json.load(config_file))

    DOWNLOAD_TYPE = config.get("download_type", "video").lower()
    PLAYLIST_DOWNLOAD_TYPE = config.get("playlist_download_type", "video").lower()
    PLAYLIST_DOWNLOAD_CAP = config.get("playlist_download_cap", "1080")

    return (config, DOWNLOAD_TYPE, PLAYLIST_DOWNLOAD_TYPE, PLAYLIST_DOWNLOAD_CAP)
