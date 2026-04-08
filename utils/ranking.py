def rank_format_options(formats):

    # PRIORITY CONSTANTS
    CODEC_PRIORITY = ["av01", "vp9", "avc1"]
    EXT_PRIORITY = ["mp4", "webm"]

    rank_data = []

    # loops thru all formats and then if they match any of the priority items, it ranks them with their dict item.
    for i, f in enumerate(formats):
        # making it easy to get dict values
        f_vcodec = f.get("vcodec")
        f_ext = f.get("ext")
        f_res = f.get("height")

        # loops thru codec and check if the format vcodec startswith that priority codec items and index + 1 is the rank. (Lower the rank, the better)
        for codec in CODEC_PRIORITY:
            if f_vcodec and f_vcodec.startswith(codec) and f_ext in EXT_PRIORITY:
                codec_rank = CODEC_PRIORITY.index(codec)
                ext_rank = EXT_PRIORITY.index(f_ext)
                data = {
                    "idx": i,
                    "codec_rank": codec_rank,
                    "ext_rank": ext_rank,
                    "resolution": f_res,
                }
                rank_data.append(data)

    return rank_data
