# Copyright (c) 2025 DanmakuConvert

from .guard_and_gift import extract_gift_data, merge_gifts, adjust_time_conflicts, calculate_moves, generate_ass_line

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