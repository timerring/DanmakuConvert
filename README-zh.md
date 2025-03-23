# DanmakuConvert

将XML弹幕转换为ASS弹幕。

这是 [DanmakuFactory](https://github.com/hihkm/DanmakuFactory) 的Python实现。

## 功能特性

- 将XML弹幕转换为ASS弹幕。
- 更高效的弹幕排列方式。详见 [问题讨论](https://github.com/hihkm/DanmakuFactory/issues/104#issuecomment-2716857788)。
- 移除那些 [FFmpeg无法渲染的多余表情符号](https://trac.ffmpeg.org/ticket/5777)。
- 支持不同操作系统，通过Python实现跨平台。
- 不需要任何第三方库。
- 支持不同分辨率。
- 支持不同字体大小。
- 支持不同颜色。
- 支持一些持久化预设参数集（进行中）。
- 未来将添加更多功能，如果您有任何建议，欢迎 [提交问题](https://github.com/timerring/DanmakuConvert/issues)。

## 转换结果展示

![示例图片](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-03-23-15-38-54.jpg)

## 安装

```bash
pip install dmconvert
```

## 使用方法

### 命令行版本