import os
import subprocess


def clear():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)


if __name__ == "__main__":
    clear()
