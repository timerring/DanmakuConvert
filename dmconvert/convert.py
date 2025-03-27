# Copyright (c) 2025 DanmakuConvert

import re
import math
import xml.etree.ElementTree as ET
from .utils import format_time, get_str_len, get_color
from dmconvert.normal.normal_handler import draw_normal_danmaku
from dmconvert.guardgift.gg_handler import draw_gift_and_guard
from dmconvert.superchat.superchat_handler import draw_superchat
from dmconvert.normal.danmaku_array import DanmakuArray
from dmconvert.header.header import draw_ass_header


def convert_xml_to_ass(font_size, sc_font_size, resolution_x, resolution_y, xml_file, ass_file):
    # Parse XML
    print("DanmakuConvert v0.0.3", flush=True)
    print("https://github.com/timerring/DanmakuConvert", flush=True)
    tree = ET.parse(xml_file)
    root = tree.getroot()
    roll_array = DanmakuArray(resolution_x, resolution_y)
    btm_array = DanmakuArray(resolution_x, resolution_y)
    draw_ass_header(ass_file, resolution_x, resolution_y, font_size, sc_font_size)
    draw_normal_danmaku(
        ass_file, root, font_size, roll_array, btm_array, resolution_x, resolution_y
    )
    draw_gift_and_guard(ass_file, root, sc_font_size, resolution_y)
    draw_superchat(ass_file, sc_font_size, resolution_y, root)
    print(f"Convert {xml_file} to {ass_file} successfully.", flush=True)


if __name__ == "__main__":
    xml_file = "sample.xml"
    ass_file = "sample.ass"
    convert_xml_to_ass(38, 38, 720, 1280, xml_file, ass_file)
