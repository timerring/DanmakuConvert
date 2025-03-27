<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/headerDark.svg" />
    <img src="assets/headerLight.svg" alt="dmconvert" />
  </picture>

English | [简体中文](./README.md)

Convert XML danmaku to ASS danmaku.

The python implementation of the [DanmakuFactory](https://github.com/hihkm/DanmakuFactory).

</div>

## Features

- Convert XML danmaku to ASS danmaku.
- More efficient arrangement of danmaku. See the [issue](https://github.com/hihkm/DanmakuFactory/issues/104#issuecomment-2716857788).
- Remove the abundant emojis which [cannot be rendered by ffmpeg](https://trac.ffmpeg.org/ticket/5777).
- Support different kinds of OS with Python.
- No third-party libraries.
- Dynamically adjust the size of superchat according to different resolutions.
- Support different font sizes.
- Support different colors.
- Support some persistence preset parameter sets.(WIP)
- More features will be added in the future, if you have any suggestions, welcome to [open an issue](https://github.com/timerring/DanmakuConvert/issues).

## The result display

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-03-23-15-38-54.jpg)

## Installation

```bash
pip install dmconvert
```

## Usage

### CLI Version

```bash
dmconvert -i sample.xml
```

More details:

```bash
dmconvert -h
# options:
#   -h, --help            show this help message and exit
#   -V, --version         Print version information
#   -f FONTSIZE, --fontsize FONTSIZE
#                         The font size of the danmaku, default is 38
#   -sf SCFONTSIZE, --scfontsize SCFONTSIZE
#                         The font size of the superchat and gift, default is 38
#   -x RESOLUTIONX, --resolutionx RESOLUTIONX
#                         The resolution x of the danmaku, default is 1920
#   -y RESOLUTIONY, --resolutiony RESOLUTIONY
#                         The resolution y of the danmaku, default is 1080
#   -i XML, --xml XML     The input xml file
#   -o ASS, --ass ASS     The output ass file

# Example:
# dmconvert -i input.xml -o output.ass
# dmconvert -f 38 -sf 30 -x 1920 -y 1080 -i input.xml -o output.ass
```

### Source Version

```python
from dmconvert.convert import convert_xml_to_ass

# eg.
# xml_file = "sample.xml"
# ass_file = "sample.ass"
# font_size = 38
# sc_font_size = 30
# resolution_x = 720
# resolution_y = 1280
convert_xml_to_ass(font_size, sc_font_size, resolution_x, resolution_y, xml_file, ass_file)
```

## The implementation algorithm

> The article is also posted on my blog [Implement danmaku rendering algorithm from scratch](https://blog.timerring.com/posts/implement-danmaku-rendering-algorithm-from-scratch/), feel free to check the latest revision.

This article presents a comprehensive implementation of a danmaku rendering algorithm from the ground up, along with a thorough analysis of the danmaku rendering algorithm. The source code is available on [GitHub](https://github.com/timerring/DanmakuConvert).

## The component of the danmaku rendering

Normally, a danmaku rendering image is comprised of the following components:

- Superchat message
- Gift message(include premium member joining info)
- Bottom danmakus
- Rolling danmakus

![The components of the danmaku rendering](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-03-23-15-20-16.png)

So how to implement the danmaku rendering algorithm from scratch? We should know the main format of the danmaku file.

## XML Danmaku File Structure

First, we can analyze the structure of XML danmaku file.

```xml
<?xml version='1.0' encoding='utf-8'?>
<i>
    <chatserver>chat.bilibili.com</chatserver>
    <chatid>0</chatid>
    <mission>0</mission>
    <maxlimit>0</maxlimit>
    <state>0</state>
    <real_name>0</real_name>
    <source>e-r</source>
    <metadata>
        <user_name>user_name</user_name>
        <room_id>room_id</room_id>
        <room_title>room_title</room_title>
        <area>area</area>
        <parent_area>parent_area</parent_area>
        <live_start_time>2024-12-01T18:03:59+08:00</live_start_time>
        <record_start_time>2024-12-01T18:05:02+08:00</record_start_time>
    </metadata>
    <d p="0.000,1,25,5816798,1733047466414,0,73c9f86f,-1189105972" uid="0" user="X***">?</d>
    <d p="0.000,1,25,5816798,1733047471983,0,73c9f86f,-1054085047" uid="0" user="X***">good</d>
  </i>
  ```

The XML file is comprised of main 2 elements:
- metadata: contains the information of the live room or video
- d: contains the danmaku information


### danmaku info
The general of <d> element is as follows:

```xml
<d p=" 0.000,     1,    25,5816798,1733047466414,   0,   73c9f86f,-1189105972" uid="0" user="X***">?</d>
<d p="{time},{type},{size},{color},{timestamp},{pool},{uid_crc32},{row_id}" uid="{uid}" user="{user}">{text}</d>
```

- time: the time of the danmaku show up
- type: the type of the danmaku
- size: the size of the danmaku, 12 tiny，16 very small, 18 small, 25 middle, 36 large, 45 very large, 64 huge
- color: the **decimal** RGB color of the danmaku, eg hexadecimal: `#FFFFFF` -> decimal: `16777215`
- timestamp: the timestamp of the danmaku
- pool: the danmaku pool type
- uid_crc32: the crc32 hash of the danmaku sender's uid, designed for ignore specific user's danmaku
- row_id: the row id of the danmaku, designed for the history danmaku

The relationship of type and pool:

| pool\type | 1 | 4 | 5 | 6 | 7 | 9 |
| --------- | - | - | - | - | - | - |
| 0         | roll | bottom | top | reverse | special[^1] | / |
| 1         | / | / | / | / | precise[^2] | / |
| 2         | / | / | / | / | / | [bas](https://bilibili.github.io/bas/#/guide) |

[^1]:special means: `[{x1(0-1)|(px)},{y1},"{Aplha0(0-1)}-{Alpha1}",{Lifetime},"{Text}",{Z_Rotation},{Y_Rotation},{x2},{y2},{Move_Time(ms)},{Delay_Time(ms)},{Outline[01]},"{Fontname}",{Linear_Speedup[01]},["SVG_Path"]]`

[^2]:precise means: `[{x1(0-1)|(px)},{y1},"{Aplha0(0-1)}-{Alpha1}",{Lifetime},"{Text}",{Z_Rotation},{Y_Rotation},{x2},{y2},{Move_Time(ms)},{Delay_Time(ms)},{Outline[01]},"{Fontname}",{Linear_Speedup(Bool)}]`


## ASS File Structure

### SSA

The `SSA` is the abbreviation of `Sub Station Alpha`, which is a subtitle format used in many video players. It can implement more complex subtitle effects than `SRT`.

### ASS

The `ASS` is the abbreviation of `Advanced SubStation Alpha`, which is the V4 version of `SSA`.

The basic structure of ASS file[^ass] is as follows:

[^ass]:https://web.archive.org/web/20210604141133/https://www.douban.com/note/658520175/

```ass
[Script Info]
ScriptType: v4.00+
Collisions: Normal
PlayResX: 720
PlayResY: 1280
Timer: 100.0000
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding

Style: R2L,Microsoft YaHei,38,&H4BFFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,8,0,0,0,1
Style: L2R,Microsoft YaHei,38,&H4BFFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,8,0,0,0,1
Style: TOP,Microsoft YaHei,38,&H4BFFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,8,0,0,0,1
Style: BTM,Microsoft YaHei,38,&H4BFFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,8,0,0,0,1
Style: SP,Microsoft YaHei,38,&H00FFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,7,0,0,0,1
Style: message_box,Microsoft YaHei,28,&H00FFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,0.7,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:12.00,R2L,,0000,0000,0000,,{\move(735,1,-15,1)}{\c&HDEC158}?
Dialogue: 0,0:00:00.00,0:00:12.00,R2L,,0000,0000,0000,,{\move(751,39,-31,39)}{\c&HDEC158}good
```

From above we can find the ASS file is comprised of 3 parts:
- [Script Info]
- [V4+ Styles]
- [Events]

#### Script Info

```python
[Script Info]
ScriptType: v4.00+  # The ass is the v4 version of the ssa
Collisions: Normal  # The collisions type
PlayResX: 720 # The X resolution of the video
PlayResY: 1280 # The Y resolution of the video
Timer: 100.0000 # This is a percentage, above 100 means the danmaku will display faster and faster.
WrapStyle: 2 # Whether to change lines, due to the bilibili restrictions, this value is always 2.
ScaledBorderAndShadow: yes # Whether to scale the border and shadow of the video with the resolution
```

In the [Script Info] part, the key and changeable parameters are:
- PlayResX: the X resolution of the video, default is **1920**
- PlayResY: the Y resolution of the video, default is **1080**

#### V4+ Styles

This part is some predefined styles for the [Events] part.

```ass
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding

Style: R2L,Microsoft YaHei,38,&H4BFFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,8,0,0,0,1
Style: L2R,Microsoft YaHei,38,&H4BFFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,8,0,0,0,1
Style: TOP,Microsoft YaHei,38,&H4BFFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,8,0,0,0,1
Style: BTM,Microsoft YaHei,38,&H4BFFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,8,0,0,0,1
Style: SP,Microsoft YaHei,38,&H00FFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,1.0,7,0,0,0,1
Style: message_box,Microsoft YaHei,28,&H00FFFFFF,&H00FFFFFF,&H00000000,&H1E6A5149,0,0,0,0,100.00,100.00,0.00,0.00,1,0.0,0.7,7,0,0,0,1
```

Most of the styles can be easily understood.

In the [V4+ Styles] part, the key and changeable parameters are:
- Fontname: the font name, default is `Microsoft YaHei`
- Fontsize: the font size, default is `38`
- MarginL: the left margin, default is `0`
- MarginR: the right margin, default is `0`
- MarginV: the vertical margin, default is `0`

#### Events

```ass
[Events]
Format: Layer,   Start,       End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:12.00,   R2L,     ,    0000,    0000,    0000,       ,{\move(735,1,-15,1)}{\c&HDEC158}?
Dialogue: 0,0:00:00.00,0:00:12.00,   R2L,     ,    0000,    0000,    0000,       ,{\move(751,39,-31,39)}{\c&HDEC158}good
```

In the [Events] part, the key and changeable parameters are:
- Layer: the layer of the danmaku
- Start: the start time of the danmaku
- End: the end time of the danmaku
- Style: the style of the danmaku, 
- Name, MarginL, MarginR, MarginV, Effect: always empty

About the `Layer` parameter:
- The `R2L danmaku` and `Superchat danmaku` are in the layer `0`.
- The `BTM danmaku` and `gift danmaku` are in the layer `1`.


About the `Start` and `End` time:
- By default the scroll time is 12 seconds.
- The fix time of BTM danmaku is 5 seconds.

About the `Style` parameter:
- R2L: right to left, which is corresponding to the `1` danmaku `type` in the XML file.
- BTM: bottom to top, which is corresponding to the `4` danmaku `type` in the XML file.
- message_box: message box, which is corresponding to the `<sc>` or `<gift>` in the XML file.


## Convert

From above analysis, we should convert the danmaku from XML to ASS.

So next I will analyze the conversion in terms of specific danmaku.

### R2L and BTM danmaku(Normal danmaku)

The xml file is as follows:
```xml
<d p=" 0.000,     1,    25,5816798,1733047466414,   0,   73c9f86f,-1189105972" uid="0" user="X***">?</d>
<d p="837.163,    4,    25,5816798,1732882824163,   0,   f201ec3c,51587109" uid="0" user="S***">what？</d>
<d p="{time},{type},{size},{color},{timestamp},{pool},{uid_crc32},{row_id}" uid="{uid}" user="{user}">{text}</d>
```

The ass file is as follows:
```ass
Format: Layer,   Start,       End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:12.00,   R2L,     ,    0000,    0000,    0000,       ,{\move(735,1,-15,1)}{\c&HDEC158}?
Dialogue: 1,0:13:57.16,0:14:02.16,   BTM,     ,    0000,    0000,    0000,       ,{\pos(960,1043)}{\c&HDEC158}what？
```

For the normal R2L and BTM danmaku, the `Layer` is `0`. `Start` time is the `time` in the XML file. `End` time is the `time` in the XML file plus 12 seconds(which can be changed). `Style` is `R2L` or `BTM`. `Name` is empty. `MarginL` is `0000`. `MarginR` is `0000`. `MarginV` is `0000`. `Effect` is empty. 

Text is the `text` in the XML file. It contains three parts:
- `{\move(735,1,-15,1)}`: **the Move Effect** for the R2L danmaku, which is the position of the danmaku. The first and second number inside is the initial position(x, y) of the danmaku, and the third and fourth number is the final position(x, y) of the danmaku. The `y` should be the same. The algorithm I will analyze in the next section.
- `{\pos(960,1043)}`: **the Pos Effect** for the BTM danmaku, which is the position of the danmaku. The number inside is the position(x, y) of the danmaku. The algorithm I will analyze in the next section.
- `{\c&HDEC158}`: the color of the danmaku, which can be converted from the decimal `color` in the XML file.
- `text`: the text of the danmaku.

#### Move Effect

The `move` effect is the most important part of the R2L danmaku.

##### X Position movement

The basic algorithm is from the initial position and the final position of the danmaku. We should keep the `y` position the same. Let's talk about the `x` position first.

- Initial position: `(resolution.x + text_length/2, PositionY)`
- Final position: `(-1 * text_length / 2, PositionY)`

So how to get the `text_length`?

We should count `cnt` the every character's length in UTF-8 encoding. So we use the `0xC0` to judge whether the current byte is the start of a multi-byte character, because `110- ----` is `0xC0`, and `0x00` to `0x7F` is the ASCII character, which is a single-byte character. Therefore, the second judgment is that it must be less than `0x80`. If it is not UTF-8 encoding, we here directly use the `strlen` function.

So the `text_length` can be approximated by the following formula:

`text_length = cnt * int((fontSizeSet + (fontSizeInXml - 25)) / 1.2);`

The `fontSizeInXml` which is in the XML file is the `size` of the danmaku. So in the simple version, we can just use the formula below:

`text_length = cnt * int((fontSizeSet) / 1.2);`

##### Y Position movement

So how should we arrange the position of `y`? We should ensure that the next danmaku would not be overlapped with the previous one.

I think we can return to the problem of the distance between the current danmaku and the previous one. To avoid the situation of catching up, we only need to ensure that the next danmaku in the same track(eg. n) cannot catch up with the previous one(eg. n-1), thus will ensure it cannot catch up with the n-2 indirectly. If it can catch up, we should compare the next danmaku data in the next track.

First, the total distance of each danmaku is fixed, which is `text_length + resolution.X`. Then the scrolling time is fixed, I think the default time is 12s, so we can calculate the speed of each danmaku `V_i`, and each track only needs to store the start time of the last danmaku `start_time` and the length of the danmaku `length`.

Then we need to determine whether the next danmaku B can catch up with the previous danmaku A, first, we need to calculate the distance difference `Delta_X`. That is, `Delta_X = (start_time_B - start_time_A) × V_a - text_length_A / 2 - text_length_B / 2`. Of course, for aesthetic reasons, a certain margin distance can be reserved. Then, we judge whether this distance can be covered within the remaining time. The speed difference is `Delta_V = V_B - V_A`, and the approximate time required for catching up can be calculated as `Delta_T = Delta_X / Delta_V`. We just need to ensure that `Start_time_B - Start_time_A > Delta_T` to ensure that the two danmakus will not overlap.

So, in the end, actually only one array and one formula are needed. Of course, in the case of a large number of danmakus, overlapping may still occur. Therefore, a fallback strategy is also required. This fallback strategy is quite simple. We just need to add a flag during each comparison to save the track number with the largest negative time difference. In this way, even if there is a catch-up situation, the danmakus will meet at the far right of the danmaku area. In the case of a large number of danmakus, the viewing experience can still be guaranteed. This method can theoretically accommodate more non-overlapping danmakus in extreme situations.

```python
def get_position_y(font_size, appear_time, text_length, resolution_x, roll_time, array):
    velocity = (text_length + resolution_x) / roll_time
    best_row = 0
    best_bias = float("-inf")
    for i in range(array.rows):
        previous_appear_time = array.get_time(i)
        if previous_appear_time < 0:
            array.set_time_length(i, appear_time, text_length)
            return 1 + i * font_size
        previous_length = array.get_length(i)
        previous_velocity = (previous_length + resolution_x) / roll_time
        delta_velocity = velocity - previous_velocity
        # abs_velocity = abs(delta_velocity)
        # The initial difference length
        delta_x = (appear_time - previous_appear_time) * previous_velocity - (
            previous_length + text_length
        ) / 2
        # If the initial difference length is negative, which means overlapped. Skip.
        if delta_x < 0:
            continue
        if delta_velocity <= 0:
            array.set_time_length(i, appear_time, text_length)
            return 1 + i * font_size
        delta_time = delta_x / delta_velocity
        bias = appear_time - previous_appear_time - delta_time
        if bias > 0:
            array.set_time_length(i, appear_time, text_length)
            return 1 + i * font_size
        else:
            if bias > best_bias:
                best_bias = bias
                best_row = i
    return 1 + best_row * font_size
```

#### Pos Effect

The `pos` effect is the most important part of the BTM danmaku. Due to the display of every danmaku is around 5 seconds, so we should make sure this single danmaku would not be overlapped in this period. And if there are other danmaku in this period, we should move the new generated danmaku up. So our core algorithm is to get the `PositionY` of the danmaku is as belows:

```python
# Bottom danmaku algorithm
def get_fixed_y(font_size, appear_time, resolution_y, array):
    best_row = 0
    best_bias = -1 # record the best bias
    for i in range(array.rows):
        previous_appear_time = array.get_time(i)
        if previous_appear_time < 0:
            array.set_time_length(i, appear_time, 0)
            return resolution_y - font_size * (i + 1) + 1 # return the bottom line of the screen.
        else:
            delta_time = appear_time - previous_appear_time
            # if the time gap is larger than 5 seconds(the previous danmaku display time is over),
            if delta_time > 5:  
                # we can move the new danmaku to this line.
                array.set_time_length(i, appear_time, 0)
                return resolution_y - font_size * (i + 1) + 1
            else:
                # if the time gap is less than 5 seconds, we can record this bias and row num,
                # then continue to the next epoch.
                if delta_time > best_bias:
                    best_bias = delta_time
                    best_row = i
    return resolution_y - font_size * (best_row + 1) + 1 # return the best line in the screen.
```

### Superchat danmaku

#### File structure

The super chat xml format is as follows:

```xml
<sc ts="50.000" uid="the_user_id" user="the_user_name" price="30" time="60">This is a superchat</sc>
```

- `ts`: The superchat appears time.
- `uid`: The user id.
- `user`: The user name.
- `price`: The price of the superchat.
- `time`: The display time of the superchat.

Regarding the specific rules on Bilibili, super chats with different prices will have different display durations and word limitations. The details are as follows[^superchat_rules]:

[^superchat_rules]: https://live.bilibili.com/blackboard/live-superchat-intro-web.html

|price(¥)|price range|display duration|chinese characters limit|
| ---- | ---- | ---- | ---- |
|30|30≤ custom price ＜50|60s|40|
|50|50≤ custom price ＜100|2min|50|
|100|100≤ custom price ＜500|5min|60|
|500|500≤ custom price ＜1000|30min|80|
|1000|1000≤ custom price ＜2000|1h|90|
|2000|custom price ≥2000|2h|100| 

The ass file is as follows:

```ass
Dialogue: 0,0:00:59.20,0:01:10.00,message_box,,0000,0000,0000,,{\pos(20,826.0)\c&HFFF5ED\p1\bord0\shad0}m 0 19 b 0 9.5 9.5 0 19 0 l 481 0 b 490.5 0 500 9.5 500 19 l 500 78 l 0 78
Dialogue: 0,0:00:59.20,0:01:10.00,message_box,,0000,0000,0000,,{\pos(20,904.0)\p1\c&HB2602A\bord0\shad0}m 0 0 l 500 0 l 500 29 b 500 38.5 490.5 48 481 48 l 19 48 b 9.5 48 0  38.5 0 29 
Dialogue: 1,0:00:59.20,0:01:10.00,message_box,,0000,0000,0000,,{\pos(20,832.0)\c&H653617\b1\bord0\shad0}The user name
Dialogue: 1,0:00:59.20,0:01:10.00,message_box,,0000,0000,0000,,{\pos(20,870.0)\c&H313131\fs30\bord0\shad0}SuperChat CNY 30
Dialogue: 1,0:00:59.20,0:01:10.00,message_box,,0000,0000,0000,,{\pos(20,904.0)\c&HFFFFFF\bord0\shad0}The display time of the superchat.
```

Every superchat danmaku message box is comprised of 5 parts:
- the upper box
- the lower box
- the user name
- the price
- the superchat text

#### Postion Arrangement Algorithm

For the upper box and lower box paramaters, I will not show them here, if you are interested, you can refer to the function `draw_lower_box` and `draw_upper_box` in my repository for more details, and many drawing parameters are referenced from the **DanmakuFactory**[^danmaku_factory], very grateful to the author. Here I would like to talk about how to make the superchat message box move according to other superchats appear and disappear.

[^danmaku_factory]: https://github.com/hihkm/DanmakuFactory

As we can see, the superchat show up and disappear in chronological order, so how can we define the superchat position in a specific timespot?

My solution is: calculate the position of the superchat message box every time the superchat changes its position in its life cycle. The concrete algorithm is as follows:

```python
def render_superchat(ass_file, sc_font_size, resolution_y, data):
    """
    Render superchat events to the ass file.

    Args:
        ass_file (str): The path to the ass file.
        sc_font_size (int): The superchat font size, which is used to calculate some render parameters.
        resolution_y (int): The resolution y, which is used to calculate the initial y coordinate.
        data (list): The data to render, which is a list of superchat events.
    """
    # get all events
    events = []
    for i, (
        start,
        end,
        sc_height,
        user_name,
        price,
        text,
        btm_box_height,
        process_record,
    ) in enumerate(data):
        events.append((start, "start", i))
        events.append((end, "end", i))

    # sort events by time
    events.sort()

    # still alive
    active = []

    # process each event
    for time, event_type, index in events:
        current_start = data[index][0]
        current_end = data[index][1]
        # if it is a start event, new superchat appears
        if event_type == "start":
            for active_index in active:
                active_start = data[active_index][0]
                active_end = data[active_index][1]
                # if the current superchat appears in the duration of the active superchat
                if active_start <= current_start < active_end:
                    # then it will record the height change of the active superchat
                    data[active_index][7] += f"-{data[index][2]}@{time} "
            active.append(index)
        else:
            # the superchat will disappear, so remove it from the active list first
            active.remove(index)
            # then check if the current superchat appears in the duration of the active superchat
            for active_index in active:
                active_start = data[active_index][0]
                active_end = data[active_index][1]
                if active_start <= current_start < active_end and time < active_end:
                    # if the current superchat disappears in the duration of the active superchat
                    # then record the height change.
                    data[active_index][7] += f"+{data[index][2]}@{time} "

    # then parse the result, and write the superchat to the ass file according to the result
    for i, (
        start,
        end,
        sc_height,
        user_name,
        price,
        text,
        btm_box_height,
        result,
    ) in enumerate(data):
        # print(f"\nSC {i} ({start}-{end}):")
        # Initial y coordinate
        previous_y = resolution_y - sc_font_size * 2
        current_y = previous_y - sc_height
        current_time = start
        # print(f"Time {start}: y = {current_y}, previous_y = {previous_y}")

        # if the position has changed
        if result:
            changes = result.strip().split()
            for change in changes:
                delta_y, time = change.split("@")
                prev_time = current_time
                current_time = float(time)
                # the shift height
                height_change = float(delta_y[1:])
                SuperChat(
                    prev_time,
                    current_time,
                    user_name,
                    price,
                    btm_box_height,
                    current_y,
                    previous_y,
                    text,
                    sc_font_size,
                ).write_superchat(ass_file)
                previous_y = current_y
                if delta_y[0] == "-":
                    current_y -= height_change
                else:
                    current_y += height_change
                # print(f"Time {time}: y = {current_y}, previous_y = {previous_y}")
        prev_time = current_time
        current_time = end
        SuperChat(
            prev_time,
            current_time,
            user_name,
            price,
            btm_box_height,
            current_y,
            previous_y,
            text,
            sc_font_size,
        ).write_superchat(ass_file)
```

Here I uncommented the print test code, so you can see the parsed result of the `sample.xml`.

```
SC 0 (10.0-70.0):
Time 10.0: y = 1078, previous_y = 1204
Time 50.0: y = 952.0, previous_y = 1078
Time 59.0: y = 826.0, previous_y = 952.0

SC 1 (50.0-110.0):
Time 50.0: y = 1078, previous_y = 1204
Time 59.0: y = 952.0, previous_y = 1078

SC 2 (59.0-119.0):
Time 59.0: y = 1078, previous_y = 1204

SC 3 (185.0-245.0):
Time 185.0: y = 1040, previous_y = 1204
Time 217.0: y = 914.0, previous_y = 1040

SC 4 (217.0-337.0):
Time 217.0: y = 1078, previous_y = 1204
Time 269.0: y = 914.0, previous_y = 1078
Time 303.0: y = 712.0, previous_y = 914.0
Time 329.0: y = 876.0, previous_y = 712.0

SC 5 (269.0-329.0):
Time 269.0: y = 1040, previous_y = 1204
Time 303.0: y = 838.0, previous_y = 1040

SC 6 (303.0-363.0):
Time 303.0: y = 1002, previous_y = 1204
```

Then we have the danmaku position of every timespot, so we can render the super chat in the ass file easily.

#### Bubble Movement Effect Algorithm

But, are these the best display? I think not. If we only consider the position, the video will be too boring, so we should add some animation to the superchat appearance. Think about the superchat like a bubble, it will move up and down according to other superchat appearance and disappearance. The picture will be more suitable for the audience.

So now we can think about the algorithm of the bubble movement effect. As we talked above, this movement can be implemented by the `move` effect.

First of all, the new superchat will appear in the bottom of the screen, so the initial `y` position is the `resolution_y - font_size * 2` (We should reserve some space for the gift danmaku, I will introduce them in the next section). And the show up position will be the initial `y` + the message box height.

Then, how will the new superchat effect other still alive superchat? At the timespot, others will move up the new superchat height as well. So the move parameter will be like from `current_y` to `current_y - new_superchat_height`. 

And if there is a specific superchat disappear, the superchat eariler than it will move down the superchat height. So the move parameter will be like from `current_y` to `current_y + disappear_superchat_height`. Then everything makes sense.

Then we should think about, when should we start the movement? There will be many solutions, but I think add it at the change position time of the superchat is the best choice. And make the movement a specific duration, like 0.2 second. 

So the process will be:
- change position time + 0.2s: make the superchat move effect.
- change position time + 0.2s ~ next change position time: make the superchat pos effect.

You can check the `superchat.py` for more details.

### Gift and guard danmaku

#### File structure

The xml file is as follows:

```xml
    <!-->gift danmaku<-->
    <gift ts="11.00"    uid="0"      user="xxx"         giftname="情书"         giftcount="1" cointype="金瓜子" price="5200"/>
    <gift ts="13.00"    uid="0"      user="yyy"         giftname="小花花"       giftcount="1" cointype="金瓜子" price="100"/>
    <gift ts="{time}"   uid="{uid}"  user="{username}"  giftname="{giftname}"   giftcount="{count}" cointype="金瓜子" price="{price}"/>

    <!-->all guard danmaku<-->
    <guard ts="18.000" uid="873268" user="xxx" giftname="舰长" count="1" price="198000" level="3"/>
    <guard ts="18.000" uid="873268" user="yyy" giftname="提督" count="1" price="1998000" level="2"/>
    <guard ts="18.000" uid="873268" user="zzz" giftname="总督" count="1" price="19998000" level="1  "/>
    <guard ts="{time}" uid="{uid}" user="{username}" giftname="{giftname}" count="{count}" price="{price}" 
    level="{level}"/>
```

The ass file is as follows:

```ass
Format: Layer,     Start,       End,      Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue:   0,0:00:00.20,0:00:02.00,message_box,     ,    0000,    0000,    0000,,{\pos(0,1242)}{\c&H1C7795\b1}{username}:{\c&H1C7795\b0} 粉丝团灯牌 x1
```

Set Layer to 0, Start to `time` in xml, End `time` +  duration time, Style to `message_box`, Name to empty, MarginL to 0000, MarginR to 0000, MarginV to 0000, Effect to `\pos` or `\move`, Text to the gift message. `\move` and  `\pos` are same as above. `b1` and `b0` are the start and end of the font bold, `&H1C7795` is the font color.

#### Gift and Guard Danmaku Display Algorithm

Gift and guard danmaku will be displayed in a box range, the height of the box is two font sizes. Gift and guard danmaku will scroll from bottom to top, and the earliest danmaku will be removed when the number of danmaku exceeds the limit.

First, parse the xml, find the part that contains "gift" and "guard", and store the information in `gift_list`. Then, calculate the display time and position of the gift and output the ass file according to these information.

The key points to note are:

1. Merge adjacent same danmaku
   - Sort all `gift` by appearance time in ascending order. Then merge the adjacent same danmaku in `gift_list`.
   - The definition of adjacent same danmaku is: the same user, the same gift, and the adjacent time is not more than `mrege_interval`(default 5s, configurable). The start time of the merged danmaku is the start time of the earliest danmaku, and the end time is the end time of the latest danmaku.

2. Handle different danmaku with the same time
   - Since the start time of danmaku from different users may be the same, which will cause display conflicts, so we need to adjust the time of the danmaku to avoid conflicts.
   - Traverse all danmaku in chronological order. If the start time of a gift danmaku is the same as or earlier than the previous one, then delay the start time of the danmaku and the end time correspondingly. Delay until the maximum number of danmaku is reached.
   - Note that: since the minimum time interval of adjacent gift danmaku is 1s, so the number of delayed danmaku multiplied by the delay time cannot exceed 1s.

3. Handle the display time and position of gift danmaku
   - When outputting, the display time and position of gift danmaku need to be adjusted according to the end time of `\pos`, but if there is a new danmaku joining in the final end time, then `\pos` needs to end earlier.
   - To achieve this adjustment, we check whether there is a danmaku with a start time earlier than the end time of the current gift danmaku in the final end time. If there is, then we will advance the end time of the current gift danmaku to the start time of the next danmaku.
   - Use an active danmaku list `active_danmaku_list` to record the current danmaku that is being displayed. The length of the list should not exceed the maximum number of danmaku that is set. When the list length exceeds the limit, the earliest danmaku should be deleted.
  
4. Danmaku display and movement transition
   - Danmaku movement transition: leave a transition time before each `\pos()`, for smooth transition from the previous position to the current `\pos()` position. This transition time can be configured.
   - For danmaku that exceeds the display range, add a mask `\clip()` when it is removed, so that the danmaku only displays the content within the mask. The height of the mask should be equal to the display box height, or twice the font size.

## Reference

