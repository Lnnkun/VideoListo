import os
import sys
from core import transcribe, generate_srt

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python main.py 视频文件.mp4")
        sys.exit(1)

    video = sys.argv[1]
    if not os.path.exists(video):
        print(f"找不到文件：{video}")
        sys.exit(1)

    segments = transcribe(video)
    srt_file = os.path.splitext(video)[0] + ".srt"
    generate_srt(segments, srt_file)
    print(f"✅ 完成：{srt_file}")