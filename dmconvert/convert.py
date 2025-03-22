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

def convert_xml_to_ass(font_size, resolution_x, resolution_y, xml_file, ass_file, roll_array, btm_array):
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    draw_ass_header(ass_file, resolution_x, resolution_y, font_size)
    draw_normal_danmaku(ass_file, root, font_size, roll_array, btm_array, resolution_x, resolution_y)
    draw_gift_and_guard(ass_file, root, font_size, resolution_y)
    draw_superchat(ass_file, font_size, resolution_y, root)

if __name__ == "__main__":
    xml_file = "sample.xml"
    ass_file = "converted.ass"
    roll_array = DanmakuArray(720, 1280)
    btm_array = DanmakuArray(720, 1280)
    convert_xml_to_ass(38, 720, 1280, xml_file, ass_file, roll_array, btm_array)