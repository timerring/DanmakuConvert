# Copyright (c) 2025 DanmakuConvert

import argparse
import sys
import os
import logging
from dmconvert.convert import convert_xml_to_ass
from dmconvert.normal.danmaku_array import DanmakuArray

def cli():
    parser = argparse.ArgumentParser(description='The Python toolkit package and cli designed for convert danmaku to ass.')
    parser.add_argument('-V', '--version', action='version', version='dmconvert 0.0.1', help='Print version information')
    parser.add_argument('-f', '--fontsize', default=38, type=int, help='The font size of the danmaku')
    parser.add_argument('-x', '--resolutionx', default=1920, type=int, help='The resolution x of the danmaku')
    parser.add_argument('-y', '--resolutiony', default=1080, type=int, help='The resolution y of the danmaku')
    parser.add_argument('-i', '--xml', required=True, type=str, help='The input xml file')
    parser.add_argument('-o', '--ass', default='', type=str, help='The output ass file')

    args = parser.parse_args()

    if os.path.splitext(args.xml)[1] == '.xml':
        xml_file = args.xml
        ass_file = args.ass if args.ass else os.path.splitext(xml_file)[0] + '.ass'
        roll_array = DanmakuArray(args.resolutionx, args.resolutiony)
        btm_array = DanmakuArray(args.resolutionx, args.resolutiony)
        convert_xml_to_ass(args.fontsize, args.resolutionx, args.resolutiony, xml_file, ass_file, roll_array, btm_array)
    else:
        print("Please assign the correct input xml file.")

if __name__ == '__main__':
    cli()