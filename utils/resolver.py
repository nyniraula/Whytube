def resolve_format_options(rank_data, formats):
    # sorts ranked data:  high -> low resolution order, low -> high codec rank & extension rank order
    sorted_data = sorted(
        rank_data, key=lambda d: (-d["resolution"], d["codec_rank"], d["ext_rank"])
    )

    sanitized_data = []
    resolution_hash = []

    # loop thru the sorted data and if a resolution is not in the hash, add it to the sanitized_data and add it to the hash to remove repeating values, since the first value is always the highest rank aka best preference, the best quality option for that resolution is only displayed
    for data in sorted_data:
        if data["resolution"] not in resolution_hash:
            sanitized_data.append(data)
            resolution_hash.append(data["resolution"])

    # list comp generator exp for a True False list passed to any to resolve True if any value is True
    if any(res >= 720 for res in resolution_hash):
        resolved_data = [data for data in sanitized_data if data["resolution"] >= 720]
    else:
        resolved_data = sanitized_data

    # get the actual format info from the resolved_data
    downloadable_formats = []
    for data in resolved_data:
        downloadable_formats.append(formats[data["idx"]])

    return downloadable_formats
