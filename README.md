# DanmakuConvert

Convert XML danmaku to ASS danmaku.

The python implementation of the [DanmakuFactory](https://github.com/hihkm/DanmakuFactory).

## Features

- Convert XML danmaku to ASS danmaku.
- More efficient arrangement of danmaku. See the [issue](https://github.com/hihkm/DanmakuFactory/issues/104#issuecomment-2716857788).
- Remove the abundant emojis which [cannot be rendered by ffmpeg](https://trac.ffmpeg.org/ticket/5777).
- Support different kinds of OS with Python.
- Do not require any third-party libraries.
- Support different resolutions.
- Support different font sizes.
- Support different colors.
- Support some persistence preset parameter sets.(WIP)
- More features will be added in the future, if you have any suggestions, welcome to [open an issue](https://github.com/timerring/DanmakuConvert/issues).

## Installation

```bash
pip install dmconvert
```

## Usage

### CLI Version

```bash
dmconvert -i sample.xml

# usage: dmconvert [-h] [-V] [-f FONTSIZE] [-x RESOLUTIONX] [-y RESOLUTIONY] -i XML [-o ASS]

# The Python toolkit package and cli designed for convert danmaku to ass.

# options:
#   -h, --help            show this help message and exit
#   -V, --version         Print version information
#   -f FONTSIZE, --fontsize FONTSIZE
#                         The font size of the danmaku, default is 38
#   -x RESOLUTIONX, --resolutionx RESOLUTIONX
#                         The resolution x of the danmaku, default is 1920
#   -y RESOLUTIONY, --resolutiony RESOLUTIONY
#                         The resolution y of the danmaku, default is 1080
#   -i XML, --xml XML     The input xml file
#   -o ASS, --ass ASS     The output ass file
```

### Source Version

```python
from dmconvert.convert import convert_xml_to_ass

# eg.
# xml_file = "sample.xml"
# ass_file = "sample.ass"
# font_size = 38
# resolution_x = 720
# resolution_y = 1280
convert_xml_to_ass(font_size, resolution_x, resolution_y, xml_file, ass_file)
```
