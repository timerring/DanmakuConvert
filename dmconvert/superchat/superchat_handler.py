# Copyright (c) 2025 DanmakuConvert

import math
from .superchat import SuperChat

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
