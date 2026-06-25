"""为医学免疫学复习笔记中的掌握/熟悉/了解知识点加标记。"""
import re
from pathlib import Path

PATH = Path("src/content/posts/医学免疫学复习笔记/index.md")

# 视觉标记
MARKERS = {
    "掌握": "⭐ **【掌握】**",
    "熟悉": "▫️ **【熟悉】**",
    "了解": "· **【了解】**",
}
KEYWORDS = "|".join(MARKERS.keys())

# 行首匹配："（1）掌握" / "(1) 掌握"
LEADING_RE = re.compile(r"^([ \t]*[（(]\s*[0-9一二三四五六七八九十]+\s*[）)]\s*)(" + KEYWORDS + r")")

# 行内匹配：在中文标点后的"掌握/熟悉/了解"
INLINE_RE = re.compile(r"(?<=[；。,，；])\s*(" + KEYWORDS + r")")


def process_line(line: str) -> str:
    # 行首处理
    m = LEADING_RE.match(line)
    if m:
        prefix = m.group(1)
        kw = m.group(2)
        rest = line[m.end():]
        line = prefix + MARKERS[kw] + rest

    # 行内处理（多次替换）
    def repl(match: re.Match) -> str:
        return MARKERS[match.group(1)]

    line = INLINE_RE.sub(repl, line)
    return line


def main():
    text = PATH.read_text(encoding="utf-8")
    lines = text.split("\n")
    changed = 0
    for i, line in enumerate(lines):
        # 跳过 frontmatter 与空行
        if not line.strip():
            continue
        new_line = process_line(line)
        if new_line != line:
            lines[i] = new_line
            changed += 1
    new_text = "\n".join(lines)
    PATH.write_text(new_text, encoding="utf-8")
    print(f"修改行数: {changed}")


if __name__ == "__main__":
    main()
