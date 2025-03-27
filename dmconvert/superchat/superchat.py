# Copyright (c) 2025 DanmakuConvert

import math
from ..utils import format_time, get_color


class SuperChat:
    def __init__(
        self,
        appear_time,
        disappear_time,
        user_name,
        price,
        btm_box_height,
        position_y,
        previous_y,
        message,
        sc_font_size,
        msg_box_position_x=10,
        msg_box_position_y=0,
        msg_space_x=450,
        msg_space_y=1080,
        move_time=0.2,
    ):
        """
        Args:
            <sc ts="10.000" uid="1234556657" user="the_user_name" price="30" time="60">This is a sc</sc>
        """
        self.msg_box_position_x = msg_box_position_x
        self.msg_box_position_y = msg_box_position_y
        self.msg_space_x = msg_space_x
        self.msg_space_y = msg_space_y
        self.sc_font_size = sc_font_size
        self.radius = int(sc_font_size / 2)
        self.appear_time = appear_time
        self.disappear_time = disappear_time
        self.user_name = user_name
        self.price = price
        self.message = message
        self.position_y = position_y
        self.btm_box_height = btm_box_height
        self.previous_y = previous_y
        self.move_time = move_time

    # example: Dialogue: 0,0:04:01.25,0:04:02.75,message_box,,0000,0000,0000,,{\pos(20,782)\c&HD8D8FF\p1\bord0\shad0}m 0 19 b 0 9 9 0 19 0 l 481 0 b 491 0 500 9 500 19 l 500 77 l 0 77
    def draw_upper_box(self, upper_box_color, start_time, end_time, effect):
        """
        Draw the upper box of the superchat.(The back ground of the user name and the price)

        Args:
            upper_box_color (str): the color of the upper box
        """
        top_box_height = self.sc_font_size * 1.8
        upper_box = (
            f"Dialogue: 0,{start_time},{end_time},message_box,,0000,0000,0000,,{{{effect}{upper_box_color}\\p1\\bord0\\shad0}}m 0 {self.radius} "  # start point
            f"b 0 {self.radius/2} {self.radius/2} 0 {self.radius} 0 "  # the left-top corner
            f"l {self.msg_space_x - self.radius} 0 "  # the top line
            f"b {self.msg_space_x - self.radius/2} 0 {self.msg_space_x} {self.radius/2} {self.msg_space_x} {self.radius} "  # the right-top corner
            f"l {self.msg_space_x} {top_box_height} "  # the right line
            f"l 0 {top_box_height}"  # the bottom line
        )
        return upper_box

    # example: Dialogue: 1,0:04:01.25,0:04:02.75,message_box,,0000,0000,0000,,{\pos(29,788)\c&H1B0E5E\b1\bord0\shad0}bili_54854929052
    def draw_user_name(self, user_name_color, start_time, end_time, effect):
        """
        Draw the user name of the superchat.

        Args:
            user_name_color (str): the color of the user name
        """
        user_name_line = f"Dialogue: 1,{start_time},{end_time},message_box,,0000,0000,0000,,{{{effect}{user_name_color}\\bord0\\shad0}}{self.user_name}"
        return user_name_line

    # Dialogue: 1,0:04:01.25,0:04:02.75,message_box,,0000,0000,0000,,{\pos(29,826)\c&H313131\fs30\bord0\shad0}SuperChat CNY 30
    def draw_superchat_price(self, start_time, end_time, effect):
        """
        Draw the price of the superchat.
        """
        # font_size = self.sc_font_size
        superchat_price = f"Dialogue: 1,{start_time},{end_time},price,,0000,0000,0000,,{{{effect}\\c&H313131\\bord0\\shad0}}SuperChat CNY {self.price}"
        return superchat_price

    # example: Dialogue: 0,0:04:01.25,0:04:02.75,message_box,,0000,0000,0000,,{\pos(20,859)\p1\c&H321AAB\bord0\shad0}m 0 0 l 500 0 l 500 66 b 500 76 491 85 481 85 l 19 85b 9 85 0 76 0 66
    def draw_lower_box(self, lower_box_color, start_time, end_time, effect):
        """
        Draw the lower box of the superchat.(The back ground of the message)

        Args:
            lower_box_color (str): the color of the lower box
            btm_box_height (int): the height of the lower box
        """
        lower_box = (
            f"Dialogue: 0,{start_time},{end_time},message_box,,0000,0000,0000,,{{{effect}\\p1{lower_box_color}\\bord0\\shad0}}m 0 0 "  # start point
            f"l {self.msg_space_x} 0 "  # the top line
            f"l {self.msg_space_x} {self.btm_box_height - self.radius} "  # the right line
            f"b {self.msg_space_x} {self.btm_box_height - self.radius/2} {self.msg_space_x - self.radius/2} {self.btm_box_height} {self.msg_space_x - self.radius} {self.btm_box_height} "  # the right-bottom corner
            f"l {self.radius} {self.btm_box_height} "  # the bottom line
            f"b {self.radius/2} {self.btm_box_height} 0  {self.btm_box_height - self.radius/2} 0 {self.btm_box_height - self.radius} "  # the left line
        )
        return lower_box

    # example: Dialogue: 1,0:04:01.25,0:04:02.75,message_box,,0000,0000,0000,,{\pos(29,859)\c&HFFFFFF\bord0\shad0}This is a superchat\Ntext
    def draw_superchat_message(self, start_time, end_time, effect):
        """
        Draw the message of the superchat.
        """
        superchat_message = f"Dialogue: 1,{start_time},{end_time},message_box,,0000,0000,0000,,{{{effect}\\c&HFFFFFF\\bord0\\shad0}}{self.message}"
        return superchat_message

    # def get_border_and_mask(start_time, end_time, self.msg_space_x, msg_height, border_color, mask_color):
    #     #
    #     # \clip(m 20 19 b 20 9 29 0 39 0 l 501 0 b 511 0 520 9 520 19 l 520 1080 l 20 1080)
    #     #
    #     start_time = format_time(float(sc.get('ts')))
    #     end_time = format_time(float(sc.get('ts')) + float(sc.get('time')))
    #     msg_box_position_x = 20
    #     msg_box_position_y = 90
    #     msg_box_self.radius = 19
    #     msg_box_size_x = 600
    #     msg_box_size_y = 100
    #     border_and_mask = f"\\clip(m {msg_box_position_x} {msg_box_position_y + msg_box_self.radius} " # start_point
    #     + f"b {msg_box_position_x} {msg_box_position_y + msg_box_self.radius/2} {msg_box_position_x + msg_box_self.radius/2} {msg_box_position_y} {msg_box_position_x + msg_box_self.radius} {msg_box_position_y} " # the left-top corner
    #     + f"l {msg_box_size_x - msg_box_self.radius + msg_box_position_x} {msg_box_position_y} " # the left-top line
    #     + f"b {msg_box_size_x - msg_box_self.radius/2 + msg_box_position_x} {msg_box_position_y} {msg_box_size_x + msg_box_position_x} {msg_box_self.radius/2 + msg_box_position_y} {msg_box_size_x + msg_box_position_x} {msg_box_self.radius + msg_box_position_y} " # the right-top corner
    #     + f"l {msg_box_size_x + msg_box_position_x} {msg_box_size_y + msg_box_position_y} " # the right line
    #     + f"l {msg_box_position_x} {msg_box_size_y + msg_box_position_y})" # bottom_line
    #     return border_and_mask

    def write_superchat(self, ass_path):
        upper_box_color, lower_box_color, user_name_color = get_color(self.price)

        format_move_time = format_time(self.appear_time)
        format_pos_time = format_time(self.appear_time + self.move_time)
        end_time = format_time(self.disappear_time)

        upper_box_position_y = self.position_y
        user_name_position_y = upper_box_position_y + int(self.sc_font_size / 6)
        superchat_price_position_y = user_name_position_y + self.sc_font_size * 0.8
        lower_box_position_y = upper_box_position_y + self.sc_font_size * 1.8 # top_box_height

        pre_upper_box_position_y = self.previous_y
        pre_user_name_position_y = pre_upper_box_position_y + int(self.sc_font_size / 6)
        pre_superchat_price_position_y = pre_user_name_position_y + self.sc_font_size * 0.8
        pre_lower_box_position_y = pre_upper_box_position_y + self.sc_font_size * 1.8

        effect_upper_box_move = (
            f"\\move(10,{pre_upper_box_position_y},10,{upper_box_position_y})"
        )
        effect_user_name_move = (
            f"\\move(20,{pre_user_name_position_y},20,{user_name_position_y})"
        )
        effect_superchat_price_move = f"\\move(20,{pre_superchat_price_position_y},20,{superchat_price_position_y})"
        effect_lower_box_move = (
            f"\\move(10,{pre_lower_box_position_y},10,{lower_box_position_y})"
        )
        effect_superchat_msg_move = f"\\move(20,{pre_lower_box_position_y},20,{lower_box_position_y})"

        with open(ass_path, "a") as f:
            f.write(
                self.draw_upper_box(
                    upper_box_color,
                    format_move_time,
                    format_pos_time,
                    effect_upper_box_move,
                )
                + "\n"
            )
            f.write(
                self.draw_lower_box(
                    lower_box_color,
                    format_move_time,
                    format_pos_time,
                    effect_lower_box_move,
                )
                + "\n"
            )
            f.write(
                self.draw_user_name(
                    user_name_color,
                    format_move_time,
                    format_pos_time,
                    effect_user_name_move,
                )
                + "\n"
            )
            f.write(
                self.draw_superchat_price(
                    format_move_time, format_pos_time, effect_superchat_price_move
                )
                + "\n"
            )
            f.write(
                self.draw_superchat_message(
                    format_move_time, format_pos_time, effect_superchat_msg_move
                )
                + "\n"
            )

        effect_upper_box_position = f"\\pos(10,{upper_box_position_y})"
        effect_user_name_position = f"\\pos(20,{user_name_position_y})"
        effect_superchat_price_position = f"\\pos(20,{superchat_price_position_y})"
        effect_lower_box_position = f"\\pos(10,{lower_box_position_y})"
        effect_superchat_msg_position = f"\\pos(20,{lower_box_position_y})"

        with open(ass_path, "a") as f:
            f.write(
                self.draw_upper_box(
                    upper_box_color,
                    format_pos_time,
                    end_time,
                    effect_upper_box_position,
                )
                + "\n"
            )
            f.write(
                self.draw_lower_box(
                    lower_box_color,
                    format_pos_time,
                    end_time,
                    effect_lower_box_position,
                )
                + "\n"
            )
            f.write(
                self.draw_user_name(
                    user_name_color,
                    format_pos_time,
                    end_time,
                    effect_user_name_position,
                )
                + "\n"
            )
            f.write(
                self.draw_superchat_price(
                    format_pos_time, end_time, effect_superchat_price_position
                )
                + "\n"
            )
            f.write(
                self.draw_superchat_message(
                    format_pos_time, end_time, effect_superchat_msg_position
                )
                + "\n"
            )
