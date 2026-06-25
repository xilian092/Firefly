"""给'2. 重点内容'小节及其下的（1）（2）（3）项目加标记。"""
import re
from pathlib import Path

PATH = Path("src/content/posts/医学免疫学复习笔记/index.md")
text = PATH.read_text(encoding="utf-8")
lines = text.split("\n")

# 匹配 "2. 重点内容" 各种写法
KEYPOINT_HEADER_RE = re.compile(r"^[ \t]*2[\.．][ \t]*重点内容[：:]?[ \t]*$")
GENERAL_HEADER_RE = re.compile(r"^[ \t]*1[\.．][ \t]*一般内容")
CHAPTER_HEADER_RE = re.compile(r"^## 第[一二三四五六七八九十百零0-9]+章")
KEYPOINT_ITEM_RE = re.compile(r"^[ \t]*[（(]\s*([0-9]+)\s*[）)]\s*(.+)")  # 宽松匹配，不要求 $ 结尾

new_lines = []
in_keypoint = False

for line in lines:
    stripped = line.strip()

    if KEYPOINT_HEADER_RE.match(stripped):
        new_lines.append("##### 🔖 **重点内容**")
        in_keypoint = True
        continue

    if GENERAL_HEADER_RE.match(stripped):
        in_keypoint = False
        new_lines.append(line)
        continue

    if CHAPTER_HEADER_RE.match(stripped):
        in_keypoint = False
        new_lines.append(line)
        continue

    if in_keypoint:
        m = KEYPOINT_ITEM_RE.match(line)
        if m:
            num = m.group(1)
            content = m.group(2).strip()
            new_lines.append(f"  🔖 **（{num}）{content}**")
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

PATH.write_text("\n".join(new_lines), encoding="utf-8")
print("Done.")
