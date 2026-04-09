from pathlib import Path


def run():
    home = Path.home()
    wtdownloads = home / "Downloads" / "WT_Downloads"

    for file in wtdownloads.iterdir():
        file_path = Path(file)
        if file_path.suffix.lower() in [".jpg", ".png", ".webp"]:
            file_path.unlink()


if __name__ == "__main__":
    run()
