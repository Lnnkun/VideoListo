[中文](README.md) | **English** | [Español](README.es.md)

# VideoListo V1.0

Automatically generate subtitles (`.srt`), a title, description, chapter timestamps and tags for Spanish-language videos.

## Prerequisites

- Python and [ffmpeg](https://ffmpeg.org/) (Whisper needs it to read videos)
- An [OpenRouter](https://openrouter.ai/) account and API key

## Installation

```powershell
git clone https://github.com/Lnnkun/VideoListo.git
cd VideoListo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and fill in your own `OPENROUTER_API_KEY`.

> The `torch` entry in `requirements.txt` is the CUDA build (`+cu128`). If you don't have an NVIDIA GPU, change it to plain `torch` first.

## Usage

```powershell
python main.py video.mp4
```

This produces `video.srt` (subtitles) and `video_meta.md` (titles, description, chapters, tags), and prints the AI cost of the run.

## Performance

Tested on an RTX 4060 (8 GB) with the Whisper small model.

Batch-transcribing 19 Spanish explainer videos (4 to 50 minutes each, about 336 minutes of audio in total) took roughly 20 minutes, or about **16.6× real time** (a 10-minute video in about 36 seconds). Timings include loading the model on each run.

## Cost

Placeholder figures (Video_1, about 4 minutes): about $0.0018; about $0.0045 for a 10-minute video. To be replaced after Video 4.

## Screenshots

To be added.
