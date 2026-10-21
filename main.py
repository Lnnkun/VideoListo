import os
import sys
from core import transcribe, generate_srt
from ai import generate_meta, check_chapters

# Windows 终端默认是 GBK 编码，强制用 UTF-8 输出，避免特殊字符导致崩溃
sys.stdout.reconfigure(encoding="utf-8")


def write_meta_md(meta, output_path):
    """把 AI 生成的内容写成方便复制到 YouTube 的 .md 文件"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 标题备选\n\n")
        for i, t in enumerate(meta.titles, 1):
            f.write(f"{i}. {t}\n")
        f.write("\n# 简介\n\n")
        f.write(meta.description.strip() + "\n\n")
        # 章节放在简介最后，格式和 YouTube 要求一致：时间 + 空格 + 标题
        f.write("章节：\n")
        for c in meta.chapters:
            f.write(f"{c.time} {c.title}\n")
        f.write("\n# 标签（逗号分隔，可直接粘贴到 YouTube）\n\n")
        f.write(", ".join(t.lstrip("#") for t in meta.tags) + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python main.py 视频文件.mp4")
        sys.exit(1)

    video = sys.argv[1]
    if not os.path.exists(video):
        print(f"找不到文件：{video}")
        sys.exit(1)

    base = os.path.splitext(video)[0]

    segments = transcribe(video)
    srt_file = base + ".srt"
    generate_srt(segments, srt_file)
    print(f"[完成] 字幕：{srt_file}")

    # AI 这一步放在字幕之后，即使它失败了，字幕也已经保存好了
    try:
        meta, cost = generate_meta(segments)
    except Exception as e:
        print(f"[失败] AI 生成失败：{e}")
        print("字幕已保存，可以稍后重试。")
        sys.exit(1)

    meta_file = base + "_meta.md"
    write_meta_md(meta, meta_file)
    print(f"[完成] 简介和时间戳：{meta_file}")

    # 检查章节是否符合 YouTube 要求，并显示本次费用
    for w in check_chapters(meta):
        print(f"[警告] {w}")
    print(f"[费用] 本次 AI 费用约 ${cost:.4f}")