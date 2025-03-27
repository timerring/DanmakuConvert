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
        description=textwrap.dedent('''
        The Python toolkit package and cli designed for convert danmaku from xml to ass format.
        Source code at https://github.com/timerring/DanmakuConvert
        '''),
        epilog=textwrap.dedent('''
        Example:
        dmconvert -i input.xml -o output.ass
        dmconvert -f 38 -sf 30 -x 1920 -y 1080 -i input.xml -o output.ass
        '''),
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="dmconvert 0.0.3 and source code at https://github.com/timerring/DanmakuConvert",
        help="Print version information",
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
        "-i", "--xml", required=True, type=str, help="The input xml file"
    )
    parser.add_argument("-o", "--ass", default="", type=str, help="The output ass file")

    args = parser.parse_args()

    if os.path.splitext(args.xml)[1] == ".xml":
        xml_file = os.path.abspath(args.xml)
        ass_file = os.path.abspath(args.ass) if args.ass else os.path.abspath(os.path.splitext(xml_file)[0] + ".ass")
        convert_xml_to_ass(
            args.fontsize,
            args.scfontsize,
            args.resolutionx,
            args.resolutiony,
            xml_file,
            ass_file,
        )
    else:
        print("Please assign the correct input xml file.")


if __name__ == "__main__":
    cli()
