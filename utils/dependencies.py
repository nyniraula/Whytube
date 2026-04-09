import json
import shutil


def check_tool_exists(tool):
    result = shutil.which(tool)
    return result


def ffmpeg_exists():
    return bool(check_tool_exists("ffmpeg"))


def config_js_runtime():
    deno = check_tool_exists("deno")
    node = check_tool_exists("node")

    if bool(deno):
        # print("Found DENO")
        js_runtimes = {"deno": {"path": deno}}

    elif bool(node):
        # print("Found NODE")
        js_runtimes = {
            "deno": {"path": None},
            "node": {"path": node},
        }

    else:
        return

    with open("config.json", "r+") as file:
        config = json.load(file)
        config.update({"js_runtimes": js_runtimes})

        # Moves cursor back to start of the file cause reading leaves it at end
        file.seek(0)
        json.dump(config, file, indent=2)  # load new config
        file.truncate()  # deletes any extra stuff
