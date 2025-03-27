# Copyright (c) 2025 DanmakuConvert

from .guard_and_gift import (
    merge_gifts,
    adjust_time_conflicts,
    calculate_moves,
    generate_ass_line,
)


def extract_gift_data(element):
    """extract the common attributes of gifts and guards"""
    fixed_time = 2  # the time of gift danmaku
    data = {
        "appear_time": float(element.get("ts")),
        "over_time": float(element.get("ts")) + fixed_time,
        "user": element.get("user"),
        "name": element.get("giftname"),
        "count": int(element.get("giftcount" if element.tag == "gift" else "count")),
        "price": element.get("price"),
        "move": 0,
        "height": 0,
        "move_time": -1,
        "disappear_time": -2,
    }
    return data


def draw_gift_and_guard(ass_file, root, sc_font_size, resolution_y):
    with open(ass_file, "a", encoding="utf-8") as f:
        # Convert gifts and guards
        raw_gifts = [
            extract_gift_data(e) for e in root.iter() if e.tag in ("gift", "guard")
        ]

        # data processing pipeline
        processed = merge_gifts(raw_gifts)
        processed = adjust_time_conflicts(processed)
        processed = calculate_moves(processed)

        # generate the output
        for gift in processed:
            lines = generate_ass_line(
                gift, resolution_y, sc_font_size
            )  # example parameters
            f.writelines(lines)
