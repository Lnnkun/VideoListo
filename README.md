# VideoListo

给西班牙语视频自动生成字幕（`.srt`），以及标题、简介、章节时间戳和标签。

## 前置条件

- Python、[ffmpeg](https://ffmpeg.org/)（Whisper 读取视频需要）
- [OpenRouter](https://openrouter.ai/) 账号和 API Key

## 安装

```powershell
git clone https://github.com/Lnnkun/VideoListo.git
cd VideoListo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

编辑 `.env`，填入自己的 `OPENROUTER_API_KEY`。

> `requirements.txt` 里的 `torch` 是 CUDA 版（`+cu128`），没有 NVIDIA 显卡请先改成普通 `torch`。

## 运行

```powershell
python main.py 视频.mp4
```

生成 `视频.srt`（字幕）和 `视频_meta.md`（标题、简介、章节、标签），并打印本次 AI 费用。

## 费用

占位数据（Video_1，约 4 分钟）：约 $0.0018，10 分钟约 $0.0045。Video 4 跑完后替换。

## 效果截图

待补充。
