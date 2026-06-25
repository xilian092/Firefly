"""查找正文中所有'掌握'出现的位置，包括在表格或标题里。"""
import re
from pathlib import Path

text = Path("src/content/posts/医学免疫学复习笔记/index.md").read_text(encoding="utf-8")

# 跳过 frontmatter
if text.startswith("---"):
    _, _, text = text.partition("---\n")
    text = text.partition("---\n")[2]

lines = text.split("\n")
in_table = False
for i, line in enumerate(lines, 1):
    if "掌握" in line:
        # 区分
        in_tbl = line.startswith("|")
        marker = "[T]" if in_tbl else ("[H]" if line.startswith("#") else "   ")
        print(f"{marker} {i:4d}: {line[:200]}")
