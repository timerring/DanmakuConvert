import re
import math
import xml.etree.ElementTree as ET
from danmaku_array import DanmakuArray
from superchat import SuperChat
from guard_and_gift import extract_gift_data, merge_gifts, adjust_time_conflicts, calculate_moves, generate_ass_line
from utils import format_time, get_str_len, get_color

# R2L danmaku algorithm
def get_position_y(font_size, appear_time, text_length, resolution_x, roll_time, array):
    velocity = (text_length + resolution_x) / roll_time
    best_row = 0
    best_bias = float('-inf')
    for i in range(array.rows):
        previous_appear_time = array.get_time(i)
        if previous_appear_time == 0:
            array.set_time_length(i, appear_time, text_length)
            return 1 + i * font_size
        previous_length = array.get_length(i)
        previous_velocity = (previous_length + resolution_x) / roll_time
        delta_velocity = velocity - previous_velocity
        # abs_velocity = abs(delta_velocity)
        # The initial difference length
        delta_x = (appear_time - previous_appear_time) * previous_velocity - (previous_length + text_length) / 2
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
        if previous_appear_time == 0:
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

def get_text_line_num(text):
    line_num = 1
    result_text = text
    
    if len(text) > 10:
        result_text = ''
        for i in range(0, len(text), 10):
            chunk = text[i:i+10]
            result_text += chunk
            if i + 10 < len(text):
                result_text += "\\N"
                line_num += 1
    
    return result_text, line_num

def get_sc_height(line_num, sc_font_size=38):
    radius = sc_font_size / 2
    top_box_height = math.ceil(sc_font_size + sc_font_size*(4.0/5.0) + radius/2)
    btm_box_height = math.ceil(line_num * sc_font_size + radius/2)
    sc_height = btm_box_height + top_box_height
    return sc_height, top_box_height, btm_box_height

def draw_superchat(ass_file, root):
    sc_list = []
    for sc in root.findall('.//sc'):
        appear_time = float(sc.get('ts'))
        user_name = sc.get('user')
        price = sc.get('price')
        disapper_time = float(sc.get('ts')) + float(sc.get('time'))
        text = sc.text
        processed_text, line_num = get_text_line_num(text)
        sc_height, _, btm_box_height = get_sc_height(line_num)
        process = ""
        sc_list.append([appear_time, disapper_time, sc_height, user_name, price, processed_text, btm_box_height, process])
    
    render_superchat(ass_file, sc_list)

def render_superchat(ass_file, data):
    # get all events
    events = []
    for i, (start, end, sc_height, user_name, price, text, btm_box_height, process_record) in enumerate(data):
        events.append((start, 'start', i))
        events.append((end, 'end', i))

    # sort events by time
    events.sort()

    # still alive
    active = []

    # process each event
    for time, event_type, index in events:
        current_start = data[index][0]
        current_end = data[index][1]
        if event_type == 'start':
            # new superchat appears
            for active_index in active:
                active_start = data[active_index][0]
                active_end = data[active_index][1]
                if active_start <= current_start < active_end:
                    # if the current superchat appears in the duration of the active superchat
                    data[active_index][7] += f"-{data[index][2]}@{time} "
            active.append(index)
        else:
            # superchat disappears
            active.remove(index)
            for active_index in active:
                active_start = data[active_index][0]
                active_end = data[active_index][1]
                if active_start <= current_start < active_end and time < active_end:
                    # if the current superchat disappears in the duration of the active superchat
                    data[active_index][7] += f"+{data[index][2]}@{time} "
    
    for i, (start, end, sc_height, user_name, price, text, btm_box_height, result) in enumerate(data):
        print(f"\nSC {i} ({start}-{end}):")
        # Initial y coordinate
        previous_y = 1280
        current_y = 1280 - sc_height
        current_time = start
        print(f"Time {start}: y = {current_y}, previous_y = {previous_y}")

        # if the position has changed
        if result:
            changes = result.strip().split()
            for change in changes:
                delta_y, time = change.split('@')
                prev_time = current_time
                current_time = float(time)
                # the shift height
                height_change = float(delta_y[1:])
                SuperChat(prev_time, current_time, user_name, price, btm_box_height, current_y, previous_y, text).write_superchat(ass_file)
                previous_y = current_y
                if delta_y[0] == '-':
                    current_y -= height_change
                else:
                    current_y += height_change
                print(f"Time {time}: y = {current_y}, previous_y = {previous_y}")
        prev_time = current_time
        current_time = end
        SuperChat(prev_time, current_time, user_name, price, btm_box_height, current_y, previous_y, text).write_superchat(ass_file)

def draw_ass_header(ass_file, resolution_x, resolution_y, font_size):
    # Write ASS header
    ass_header = f"""[Script Info]
ScriptType: v4.00+
Collisions: Normal
PlayResX: {resolution_x}
PlayResY: {resolution_y}
Timer: 100.0000
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding

Style: R2L,Microsoft YaHei,{font_size},&H4BFFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,8,0,0,0,1
Style: L2R,Microsoft YaHei,{font_size},&H4BFFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,8,0,0,0,1
Style: TOP,Microsoft YaHei,{font_size},&H4BFFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,8,0,0,0,1
Style: BTM,Microsoft YaHei,{font_size},&H4BFFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,8,0,0,0,1
Style: SP,Microsoft YaHei,{font_size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,7,0,0,0,1
Style: message_box,Microsoft YaHei,{font_size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,0.7,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ass_file, 'w', encoding='utf-8') as f:
        f.write(ass_header)

def draw_normal_danmaku(ass_file, root, font_size, roll_array, btm_array, resolution_x, resolution_y):
    with open(ass_file, 'a', encoding='utf-8') as f:
        # Convert each danmaku
        for d in root.findall('.//d'):
            # Parse attributes
            p_attrs = d.get('p').split(',')
            appear_time = float(p_attrs[0])
            danmaku_type = int(p_attrs[1])

            # Convert color from decimal to hex
            color = int(p_attrs[3])
            color_hex = hex(color)
            color_reverse = ''.join(reversed([color_hex[i:i+2] for i in range(0, len(color_hex), 2)]))
            color_hex = color_reverse[:-2].ljust(6, '0').upper() # Remove 0x
            color_text = f"\\c&H{color_hex}"
            
            roll_time = 12
            fix_time = 5

            # Format times
            start_time = format_time(appear_time)
            
            # Format text
            text = d.text
            
            # For rolling danmakus (most common type)
            if danmaku_type == 1:
                layer = 0
                end_time = format_time(appear_time + roll_time)
                style = "R2L"
                text_length = get_str_len(text, font_size) # Estimate the length of the text
                x1 = resolution_x + int(text_length / 2)  # Start from right edge
                x2 = -int(text_length / 2)      # End at left edge
                y = get_position_y(font_size, appear_time, text_length, resolution_x, roll_time, roll_array)
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

def draw_gift_and_guard(ass_file, root, font_size, resolution_y):
    with open(ass_file, 'a', encoding='utf-8') as f:
        # Convert gifts and guards
        raw_gifts = [extract_gift_data(e) for e in root.iter() if e.tag in ('gift', 'guard')]
        
        # data processing pipeline    
        processed = merge_gifts(raw_gifts)
        processed = adjust_time_conflicts(processed)
        processed = calculate_moves(processed)

        # generate the output
        for gift in processed:
            lines = generate_ass_line(gift, resolution_y, font_size)  # example parameters
            f.writelines(lines)

def convert_xml_to_ass(font_size, resolution_x, resolution_y, xml_file, ass_file, roll_array, btm_array):
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    draw_ass_header(ass_file, resolution_x, resolution_y, font_size)
    draw_normal_danmaku(ass_file, root, font_size, roll_array, btm_array, resolution_x, resolution_y)
    draw_gift_and_guard(ass_file, root, font_size, resolution_y)
    draw_superchat(ass_file, root)


if __name__ == "__main__":
    xml_file = "sample.xml"
    ass_file = "converted_gift.ass"
    roll_array = DanmakuArray(720, 1280)
    btm_array = DanmakuArray(720, 1280)
    convert_xml_to_ass(38, 720, 1280, xml_file, ass_file, roll_array, btm_array)