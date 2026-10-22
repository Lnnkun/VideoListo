# VideoListo

西班牙语视频后期助手：给一个西语视频，自动生成字幕文件，以及可直接粘贴到 YouTube 的标题、简介、章节时间戳和标签。

## 解决什么问题

发布视频前要做的杂活：听写字幕、想标题、写简介、整理章节、挑标签。VideoListo 把这些一次跑完：

1. 用 [Whisper](https://github.com/openai/whisper) 识别西班牙语语音，生成 `.srt` 字幕
2. 把字幕交给大模型（通过 OpenRouter），生成标题备选、简介、章节、标签
3. 检查章节时间戳是否合法，调用失败时自动重试，并打印本次 AI 调用的费用

## 前置条件

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/)（Whisper 读取视频需要，须已加入 `PATH`）
- [OpenRouter](https://openrouter.ai/) 账号和 API Key
- 有 NVIDIA 显卡会快很多（可选，没有则用 CPU 识别）

## 安装

```powershell
git clone https://github.com/<用户名>/videolisto.git
cd videolisto
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

然后编辑 `.env`，填入你自己的 Key：

```
OPENROUTER_API_KEY=你的OpenRouter密钥
MODEL=deepseek/deepseek-v4.1-flash-1017
```

> `.env` 已被 `.gitignore` 忽略，请不要提交它。

> `requirements.txt` 里的 `torch` 是 CUDA 12.8 版本（`+cu128`）。没有 NVIDIA 显卡的话，请先改成普通的 `torch` 再安装。

## 运行

```powershell
python main.py 视频.mp4
```

会在视频同目录下生成：

| 文件 | 内容 |
| --- | --- |
| `视频.srt` | 西语字幕 |
| `视频_meta.md` | 标题备选、简介、章节时间戳、标签（逗号分隔，可直接粘贴到 YouTube） |

终端末尾会打印本次 AI 调用的 token 数和费用。

## 费用

> 以下为占位数据，来自 Video_1，等 Video 4 录好后替换为真实数据。

- 视频长度约 4 分钟
- token 用量：输入 1211 + 输出 3525
- 费用约 **$0.0018**；按此推算，10 分钟视频约 **$0.0045**

Whisper 在本地运行，不产生费用。

## 效果截图

> 占位：等 Video 4 跑完补上。

## 项目结构

| 文件 | 作用 |
| --- | --- |
| `main.py` | 入口，串起整个流程 |
| `core.py` | Whisper 识别与字幕生成 |
| `ai.py` | AI 调用、章节检查、费用计算 |
