# Copyright (c) 2025 DanmakuConvert

from .danmaku_array import DanmakuArray
from ..utils import format_time, get_str_len, remove_emojis


# R2L danmaku algorithm
def get_position_y(font_size, appear_time, text_length, resolution_x, roll_time, array):
    velocity = (text_length + resolution_x) / roll_time
    best_row = 0
    best_bias = float("-inf")
    for i in range(array.rows):
        previous_appear_time = array.get_time(i)
        if previous_appear_time < 0:
            array.set_time_length(i, appear_time, text_length)
            return 1 + i * font_size
        previous_length = array.get_length(i)
        previous_velocity = (previous_length + resolution_x) / roll_time
        delta_velocity = velocity - previous_velocity
        # abs_velocity = abs(delta_velocity)
        # The initial difference length
        delta_x = (appear_time - previous_appear_time) * previous_velocity - (
            previous_length + text_length
        ) / 2
        # If the initial difference length is negative, which means overlapped. Skip.
        if delta_x < 0:
            continue
        if delta_velocity <= 0:
            array.set_time_length(i, appear_time, text_length)
            return 1 + i * font_size
        delta_time = delta_x / delta_velocity
        bias = appear_time - previous_appear_time - delta_time
        if bias > 0:
            array.set_time_length(i, appear_time, text_length)
            return 1 + i * font_size
        else:
            if bias > best_bias:
                best_bias = bias
                best_row = i
    return 1 + best_row * font_size


# Bottom danmaku algorithm
def get_fixed_y(font_size, appear_time, resolution_y, array):
    best_row = 0
    best_bias = -1
    for i in range(array.rows):
        previous_appear_time = array.get_time(i)
        if previous_appear_time < 0:
            array.set_time_length(i, appear_time, 0)
            return resolution_y - font_size * (i + 1) + 1
        else:
            delta_time = appear_time - previous_appear_time
            if delta_time > 5:
                array.set_time_length(i, appear_time, 0)
                return resolution_y - font_size * (i + 1) + 1
            else:
                if delta_time > best_bias:
                    best_bias = delta_time
                    best_row = i
    return resolution_y - font_size * (best_row + 1) + 1


def draw_normal_danmaku(
    ass_file, root, font_size, roll_array, btm_array, resolution_x, resolution_y
):
    with open(ass_file, "a", encoding="utf-8") as f:
        # Convert each danmaku
        all_normal_danmaku = root.findall(".//d")
        danmaku_count = len(all_normal_danmaku)
        print(f"The normal danmaku pool is {danmaku_count}.", flush=True)
        for d in all_normal_danmaku:
            # Parse attributes
            p_attrs = d.get("p").split(",")
            appear_time = float(p_attrs[0])
            danmaku_type = int(p_attrs[1])

            # Convert color from decimal to hex
            color = int(p_attrs[3])
            color_hex = hex(color)
            color_reverse = "".join(
                reversed([color_hex[i : i + 2] for i in range(0, len(color_hex), 2)])
            )
            color_hex = color_reverse[:-2].ljust(6, "0").upper()  # Remove 0x
            color_text = f"\\c&H{color_hex}"

            roll_time = 12
            fix_time = 5

            # Format times
            start_time = format_time(appear_time)

            # Format text
            text = remove_emojis(d.text)

            # For rolling danmakus (most common type)
            if danmaku_type == 1:
                layer = 0
                end_time = format_time(appear_time + roll_time)
                style = "R2L"
                text_length = get_str_len(
                    text, font_size
                )  # Estimate the length of the text
                x1 = resolution_x + int(text_length / 2)  # Start from right edge
                x2 = -int(text_length / 2)  # End at left edge
                y = get_position_y(
                    font_size,
                    appear_time,
                    text_length,
                    resolution_x,
                    roll_time,
                    roll_array,
                )
                effect = f"\\move({x1},{y},{x2},{y})"

            # For BTM danmakus
            else:
                layer = 1
                end_time = format_time(appear_time + fix_time)
                style = "BTM"
                x = int(resolution_x / 2)
                y = get_fixed_y(font_size, appear_time, resolution_y, btm_array)
                effect = f"\\pos({x},{y})"

            line = f"Dialogue: {layer},{start_time},{end_time},{style},,0000,0000,0000,,{{{effect}}}{{{color_text}}}{text}\n"
            f.write(line)
