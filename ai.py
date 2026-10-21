# ai.py
import os
import openai
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ConfigDict, ValidationError

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# 价格：美元 / 百万 token，以 OpenRouter 模型页为准，换模型要同步改
PRICE_IN = 0.07
PRICE_OUT = 0.50

class Chapter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    time: str   # 格式 "00:00" 或 "1:23:45"
    title: str

class VideoMeta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    titles: list[str]       # 3 个标题备选
    description: str        # YouTube 简介
    chapters: list[Chapter] # 章节时间戳
    tags: list[str]         # 10–15 个标签

PROMPT = """你是一个西班牙语 YouTube 频道的助手，频道记录普通人自学 AI 和编程的真实过程。
下面是一期视频的字幕，每行开头是时间。请根据字幕生成：
1. 3 个西语标题备选：真实、具体，不夸张；三个要从不同角度切入（比如一个讲内容、一个讲收获、一个用提问），不要互相只是换词
2. 西语简介：用第一人称（我）写，像频道主自述。第一句不超过 25 个词，说清这期讲什么；之后分 2–3 个短段落，不要写成一整段；全文不超过 200 词。字幕内容不够就写短，不要凑字数
3. 章节：第一个必须是 00:00，至少 3 个，每个标题不超过 6 个词，章节之间至少间隔 30 秒
4. 10–15 个标签：西语为主，可以有少量英文技术词；标签不要带 # 号
所有西语使用性别中立的表达。

重要：
- 标题、简介、章节、标签都只能依据字幕里明确出现过的内容。字幕里没提到的概念、工具、品牌（比如没说过 Arduino 就不能出现 Arduino），一律不要写，标签也一样。
- 西语统一用拉美拼写（video，不是 vídeo）。

字幕：
{transcript}"""

def segments_to_text(segments):
    """把 Whisper 的片段变成「[时:分:秒] 文字」，方便 AI 找时间点"""
    lines = []
    for s in segments:
        total = int(s["start"])
        h, rem = divmod(total, 3600)
        m, sec = divmod(rem, 60)
        stamp = f"{h}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"
        lines.append(f"[{stamp}] {s['text'].strip()}")
    return "\n".join(lines)

def _to_seconds(t):
    """'03:11' 或 '1:03:11' 转成秒数，格式不对返回 None"""
    try:
        parts = [int(x) for x in t.split(":")]
    except ValueError:
        return None
    sec = 0
    for p in parts:
        sec = sec * 60 + p
    return sec

def check_chapters(meta, min_gap=10):
    """检查章节是否符合 YouTube 要求，返回警告列表（空列表表示没问题）"""
    warnings = []
    chapters = meta.chapters
    if len(chapters) < 3:
        warnings.append(f"章节只有 {len(chapters)} 个，YouTube 要求至少 3 个")
    if not chapters or _to_seconds(chapters[0].time) != 0:
        warnings.append("第一个章节不是 00:00，YouTube 不会识别章节")
    prev = None
    for c in chapters:
        sec = _to_seconds(c.time)
        if sec is None:
            warnings.append(f"时间格式不对：{c.time}")
            continue
        if prev is not None and sec - prev < min_gap:
            warnings.append(f"章节「{c.title}」距上一个不足 {min_gap} 秒")
        prev = sec
    return warnings

def generate_meta(segments):
    """返回 (VideoMeta, 本次费用美元)"""
    print("[3/3] 正在让 AI 写简介和时间戳...")
    prompt = PROMPT.format(transcript=segments_to_text(segments))
    total_in = total_out = 0

    for attempt in range(2):  # 最多试 2 次：第一次 + 重试 1 次
        try:
            response = client.chat.completions.create(
                model=os.getenv("MODEL"),
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "video_meta",
                        "strict": True,
                        "schema": VideoMeta.model_json_schema(),
                    },
                },
                extra_body={"provider": {"require_parameters": True}},
            )
        except openai.APIError as e:
            # Key 错、余额不足、网络断了：重试也没用，直接报清楚
            raise RuntimeError(f"调用 AI 失败：{e}") from e

        if response.usage:
            total_in += response.usage.prompt_tokens
            total_out += response.usage.completion_tokens

        try:
            meta = VideoMeta.model_validate_json(response.choices[0].message.content)
            break
        except ValidationError:
            if attempt == 0:
                print("AI 返回的 JSON 不合格，自动重试 1 次...")
            else:
                raise RuntimeError("AI 连续两次返回不合格的 JSON，请换模型或加大 max_tokens")

    cost = (total_in * PRICE_IN + total_out * PRICE_OUT) / 1_000_000
    print(f"    用了 token：{total_in} + {total_out}")
    return meta, cost