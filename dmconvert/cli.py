# Copyright (c) 2025 DanmakuConvert

import argparse
import sys
import os
import logging
import textwrap
from dmconvert.convert import convert_xml_to_ass


def cli():
    parser = argparse.ArgumentParser(
        prog="dmconvert",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
        The Python toolkit package and cli designed for convert danmaku from xml to ass format.
        Source code at https://github.com/timerring/DanmakuConvert
        """
        ),
        epilog=textwrap.dedent(
            """
        Example:
        dmconvert -i input.xml -o output.ass
        dmconvert -fn "Microsoft YaHei" -f 38 -sf 30 -x 1920 -y 1080 -d 1.0 -r 12 -ft 5 -a 0.8 -b 1 -ol 1.0 -sh 0.0 -i input.xml -o output.ass
        """
        ),
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="dmconvert 0.0.4 and source code at https://github.com/timerring/DanmakuConvert",
        help="Print version information",
    )
    parser.add_argument(
        "-fn",
        "--fontname",
        default="Microsoft YaHei",
        type=str,
        help="The font name of the danmaku, default is 'Microsoft YaHei'",
    )
    parser.add_argument(
        "-f",
        "--fontsize",
        default=38,
        type=int,
        help="The font size of the danmaku, default is 38",
    )
    parser.add_argument(
        "-sf",
        "--scfontsize",
        default=38,
        type=int,
        help="The font size of the superchat and gift, default is 38",
    )
    parser.add_argument(
        "-x",
        "--resolutionx",
        default=1920,
        type=int,
        help="The resolution x of the danmaku, default is 1920",
    )
    parser.add_argument(
        "-y",
        "--resolutiony",
        default=1080,
        type=int,
        help="The resolution y of the danmaku, default is 1080",
    )
    parser.add_argument(
        "-d",
        "--displayarea",
        default=1.0,
        type=float,
        help="The display area of the normal danmaku, default is 1.00. (0.00-1.00)",
    )
    parser.add_argument(
        "-r",
        "--roll-time",
        default=12,
        type=int,
        help="The show time of the rolling danmaku, default is 12"
    )
    parser.add_argument(
        "-ft",
        "--fix-time",
        default=5,
        type=int,
        help="The show time of the fix danmaku, default is 5"
    )
    parser.add_argument(
        "-a",
        "--alpha",
        default=0.8,
        type=float,
        help="The opacity value of the danmaku, default is 0.8. (0.0-1.0)",
    )
    parser.add_argument(
        "-b",
        "--bold",
        default=0,
        type=int,
        help="The bold value of the danmaku, default is 0. [0,1]",
    )
    parser.add_argument(
        "-ol",
        "--outline",
        default=1.0,
        type=float,
        help="The outline width of the danmaku, default is 1.0"
    )
    parser.add_argument(
        "-sh",
        "--shadow",
        default=0.0,
        type=float,
        help="The shadow width of the danmaku, default is 0.0"
    )
    parser.add_argument(
        "-i", "--xml", required=True, type=str, help="The input xml file"
    )
    parser.add_argument("-o", "--ass", default="", type=str, help="The output ass file")

    args = parser.parse_args()

    if os.path.splitext(args.xml)[1] == ".xml":
        xml_file = os.path.abspath(args.xml)
        ass_file = (
            os.path.abspath(args.ass)
            if args.ass
            else os.path.abspath(os.path.splitext(xml_file)[0] + ".ass")
        )
        convert_xml_to_ass(
            args.fontname,
            args.fontsize,
            args.scfontsize,
            args.resolutionx,
            args.resolutiony,
            args.displayarea,
            args.roll_time,
            args.fix_time,
            args.alpha,
            args.bold,
            args.outline,
            args.shadow,
            xml_file,
            ass_file,
        )
    else:
        print("Please assign the correct input xml file.")


if __name__ == "__main__":
    cli()
