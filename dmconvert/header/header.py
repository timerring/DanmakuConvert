# Copyright (c) 2025 DanmakuConvert


def draw_ass_header(ass_file, resolution_x, resolution_y, font_name, font_size, sc_font_size, opacity, bold, outline, shadow):
    # Write ASS header
    alpha = format(int((1 - float(opacity)) * 255), '02X')
    primary_color = f"&H{alpha}FFFFFF"
    back_color = f"&H{alpha}000000"
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

Style: R2L,{font_name},{font_size},{primary_color},&H00FFFFFF,&H00000000,{back_color},{bold},0,0,0,100.00,100.00,0.00,0.00,1,{outline},{shadow},7,0,0,0,1
Style: L2R,{font_name},{font_size},{primary_color},&H00FFFFFF,&H00000000,{back_color},{bold},0,0,0,100.00,100.00,0.00,0.00,1,{outline},{shadow},9,0,0,0,1
Style: TOP,{font_name},{font_size},{primary_color},&H00FFFFFF,&H00000000,{back_color},{bold},0,0,0,100.00,100.00,0.00,0.00,1,{outline},{shadow},8,0,0,0,1
Style: BTM,{font_name},{font_size},{primary_color},&H00FFFFFF,&H00000000,{back_color},{bold},0,0,0,100.00,100.00,0.00,0.00,1,{outline},{shadow},2,0,0,0,1
Style: SP,{font_name},{font_size},&H00FFFFFF,&H00FFFFFF,&H00000000,{back_color},{bold},0,0,0,100.00,100.00,0.00,0.00,1,{outline},{shadow},7,0,0,0,1
Style: message_box,{font_name},{sc_font_size},&H00FFFFFF,&H00FFFFFF,&H00000000,{back_color},{bold},0,0,0,100.00,100.00,0.00,0.00,1,0.0,0.7,7,0,0,0,1
Style: price,{font_name},{int(sc_font_size * 0.7)},&H00FFFFFF,&H00FFFFFF,&H00000000,{back_color},{bold},0,0,0,100.00,100.00,0.00,0.00,1,0.0,0.7,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(ass_header)
