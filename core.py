import whisper

def transcribe(video_path, model_name="small"):
    """直接识别视频里的西语，返回带时间的片段"""
    print(f"[1/3] 加载 Whisper {model_name} 模型（第一次会自动下载）...")
    model = whisper.load_model(model_name)
    print(f"[1/3] 开始识别 {video_path} ...")
    result = model.transcribe(video_path, language="es")
    return result["segments"]

def format_time(seconds):
    """把秒数转成 SRT 时间格式 00:00:00,000"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generate_srt(segments, output_path):
    """把片段写成 .srt 字幕文件"""
    print(f"[2/3] 生成字幕 {output_path} ...")
    with open(output_path, "w", encoding="utf-8") as f:
        for i, s in enumerate(segments):
            f.write(f"{i + 1}\n")
            f.write(f"{format_time(s['start'])} --> {format_time(s['end'])}\n")
            f.write(f"{s['text'].strip()}\n\n")