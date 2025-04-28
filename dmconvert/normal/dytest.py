# Copyright (c) 2025 DanmakuConvert

from ..utils import format_time, remove_emojis
from ..header.header import draw_ass_header
from ..guardgift.gg_handler import draw_gift_and_guard


import re
import xml.etree.ElementTree as ET

max_rows = 15
video_end_time = 100  # 这个是视频总时长，或者设置一个比实际视频长一点的值


class Danmaku:
    text: str
    appear_time: float  # 出现时间（秒）
    current_row: int = 0  # 最下是1，逐渐上升
    user: str
    disappear_time: float = None

    def __init__(self, user, text, appear_time):
        self.user = user
        self.text = text
        self.appear_time = appear_time


class Move:
    text: str
    start_time: float
    end_time: float
    row: int


def record_move(dm, start_time, end_time, row):
    move = Move()
    move.text = dm.text
    move.start_time = start_time
    move.end_time = end_time
    move.row = row
    return move


def read_xml(xml_file):
    dm_list = []
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for dm in root.findall("d"):
        p_attrs = dm.get("p").split(",")
        appear_time = float(p_attrs[0])
        user = dm.get("user")
        text = remove_emojis(dm.text)
        dm_list.append(Danmaku(user, text, appear_time))
    return dm_list, root


def cal_move(dm_list):

    recorded_move = []
    active_danmaku = []
    dm_list = sorted(dm_list, key=lambda x: x.appear_time)

    # 处理在屏幕上停留的弹幕的移动
    last_time = 0
    for dm in dm_list:
        for i in range(
            len(active_danmaku) - 1, -1, -1
        ):  # 倒序遍历，避免remove操作影响遍历
            """
            这里的remove操作会导致索引变化，进而影响for循环的遍历，会跳过当前元素
            AI说逆序可以解决这个问题
            """
            d = active_danmaku[i]
            if d.current_row == max_rows:  # 这个地方没想好用行高判断还是list长度判断
                active_danmaku.remove(d)
                # move = record_move(d,last_time,dm.appear_time,d.current_row)
                # recorded_move.append(move)
                # last_time = dm.appear_time
            else:
                d.current_row += 1
                move = record_move(d, last_time, dm.appear_time, d.current_row)
                recorded_move.append(move)
                # last_time = dm.appear_time
        last_time = dm.appear_time
        active_danmaku.append(Danmaku(dm.user, dm.text, dm.appear_time))
        """
        for d in active_danmaku:
            print(d.text, d.appear_time, d.current_row)
        print("------------------------")
        """

    # for d in active_danmaku:
    # recorded_move.append(record_move(d,d.appear_time,video_end_time,d.current_row))

    # 排序,好观察结果
    sorted_move = sorted(recorded_move, key=lambda x: x.text)

    # for m in sorted_move:
    #   print(m.text, m.start_time, m.end_time, m.row)
    return sorted_move, active_danmaku, last_time


def draw_move(move, video_width, video_height, font_size):
    lines = ""
    for m in move:
        text = m.text
        start_time = m.start_time
        end_time = m.end_time
        row = m.row
        effect = f"\\pos({0},{video_height-(row+2)*font_size})"
        start_time = format_time(start_time)
        end_time = format_time(end_time)
        
        lines += f"Dialogue: {0},{start_time},{end_time},message_box,,0000,0000,0000,,{{{effect}}}{text}\n"

    return lines


def draw_tail_pos(start_time, active_danmaku, video_width, video_height, font_size):
    lines = ""
    end_time = start_time + video_end_time
    start_time = format_time(start_time)
    end_time = format_time(end_time)

    # 除了最后一个弹幕，其他弹幕都在屏幕上停留，在视频结尾显示
    for d in active_danmaku[:-1]:
        text = d.text
        row = d.current_row
        effect = f"\\pos({0},{video_height-(row+2)*font_size})"

        lines += f"Dialogue: {0},{start_time},{end_time},message_box,,0000,0000,0000,,{{{effect}}}{text}\n"
    return lines


def main():
    video_width = 720
    video_height = 1280
    font_size = 38
    sc_font_size = 24

    dm_list, root = read_xml("sample.xml")
    move, active_danmaku, last_time = cal_move(dm_list)

    # for d in dm_list:
    #    print(d.user, d.text, d.appear_time)

    lines = ""
    lines += draw_move(move, video_width, video_height, font_size)
    lines += draw_tail_pos(
        last_time, active_danmaku, video_width, video_height, font_size
    )
    draw_ass_header("dytest.ass", video_width, video_height, font_size, font_size)
    draw_gift_and_guard("dytest.ass", root, font_size, video_height)

    with open("dytest.ass", "a", encoding="utf-8") as f:
        f.write(lines)


if __name__ == "__main__":
    main()
