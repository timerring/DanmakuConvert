# Copyright (c) 2025 DanmakuConvert

def format_time(seconds):
    """Convert seconds to ASS time format (H:MM:SS.cc)"""
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    centiseconds = int((seconds % 1) * 100)
    seconds = int(seconds)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"

def is_utf8(s):
    try:
        s.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False

def get_str_len(s, fontSizeSet):
    if s is None:
        return -1

    if isinstance(s, bytes):
        str_bytes = s
    else:
        str_bytes = s.encode('utf-8')

    if is_utf8(str_bytes):
        cnt = 0
        index = 0
        while index < len(str_bytes):
            byte = str_bytes[index]
            if byte >= 0xC0:
                cnt += 1
            elif byte < 0x80:
                cnt += 1
            index += 1
    else:
        cnt = len(str_bytes)

    len_result = cnt * int((fontSizeSet) / 1.2)
    return len_result

def get_color(price):
    price = int(price)
    if price >= 2000:
        upper_box_color = "\\c&HD8D8FF"
        lower_box_color = "\\c&H321AAB"
        user_name_color = "\\c&H1B0E5E"
    elif price >= 1000:
        upper_box_color = "\\c&HE4E7FF"
        lower_box_color = "\\c&H4D4DE5"
        user_name_color = "\\c&H333398"
    elif price >= 500:
        upper_box_color = "\\c&HD2EAFF"
        lower_box_color = "\\c&H4394E0"
        user_name_color = "\\c&H2C6193"
    elif price >= 100:
        upper_box_color = "\\c&HC5F1FF"
        lower_box_color = "\\c&H2BB5E2"
        user_name_color = "\\c&H1C7795"
    elif price >= 50:
        upper_box_color = "\\c&HFDFFDB"
        lower_box_color = "\\c&H9E7D42"
        user_name_color = "\\c&H514022"
    else:
        upper_box_color = "\\c&HFFF5ED"
        lower_box_color = "\\c&HB2602A"
        user_name_color = "\\c&H653617"
    
    return upper_box_color, lower_box_color, user_name_color