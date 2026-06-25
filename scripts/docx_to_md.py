"""Convert medical immunology DOCX files to Markdown."""
import re
import os
from docx import Document
from docx.oxml.ns import qn

SRC_DIR = "医学免疫学"

# 匹配"第X章"、"第X章 第Y章"、"第X章、"等章节标题
CHAPTER_RE = re.compile(r"^第[一二三四五六七八九十百零0-9]+章[、\s]")
# 匹配"一、"、"二、"等章节小节标题
SECTION_RE = re.compile(r"^[一二三四五六七八九十]+、")
# 匹配"（一）"、"(1)"等
LIST_PAREN_RE = re.compile(r"^[（(][一二三四五六七八九十0-9]+[）)]")


def cell_text_to_md(text: str) -> str:
    lines = [l.strip() for l in text.split("\n")]
    lines = [l for l in lines if l != ""]
    return "<br>".join(lines)


def table_to_md(table) -> str:
    rows = []
    for row in table.rows:
        cells = [cell_text_to_md(cell.text) for cell in row.cells]
        cells = [c.replace("|", "\\|") for c in cells]
        rows.append(cells)
    if not rows:
        return ""
    ncols = max(len(r) for r in rows)
    for r in rows:
        while len(r) < ncols:
            r.append("")
    out = []
    out.append("| " + " | ".join(rows[0]) + " |")
    out.append("| " + " | ".join("---" for _ in rows[0]) + " |")
    for r in rows[1:]:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def list_paragraph_level(paragraph):
    pPr = paragraph._p.find(qn("w:pPr"))
    if pPr is None:
        return None
    numPr = pPr.find(qn("w:numPr"))
    if numPr is None:
        return None
    ilvl = numPr.find(qn("w:ilvl"))
    lvl = int(ilvl.get(qn("w:val"))) if ilvl is not None else 0
    return lvl


def normalize_heading(text: str, style: str) -> str:
    """将 Normal 样式但匹配章节模式的段落转成标题。"""
    t = text.strip()
    if not t:
        return t
    if style in ("Title", "Heading 1"):
        return t
    if CHAPTER_RE.match(t):
        return t
    if SECTION_RE.match(t):
        return t
    return t


def convert_paragraph(paragraph) -> str:
    text = paragraph.text.rstrip()
    style = paragraph.style.name
    if not text.strip():
        return ""

    t = text.strip()

    if style == "Title" or style == "Heading 1":
        return f"# {t}"
    if style == "Heading 2":
        return f"## {t}"
    if style == "Heading 3":
        return f"### {t}"
    if style == "Heading 4":
        return f"#### {t}"

    # Normal 样式但匹配章节模式
    if CHAPTER_RE.match(t):
        return f"# {t}"
    if SECTION_RE.match(t):
        return f"## {t}"

    # 列表
    lvl = list_paragraph_level(paragraph)
    if lvl is not None:
        indent = "  " * lvl
        return f"{indent}- {t}"

    return t


def iter_block_items(parent):
    from docx.document import Document as _Document
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    else:
        parent_elm = parent

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def merge_paragraph_runs_to_md(paragraph) -> str:
    """完整保留加粗、斜体等内联格式。"""
    parts = []
    for run in paragraph.runs:
        t = run.text
        if not t:
            continue
        if run.bold and run.italic:
            t = f"***{t}***"
        elif run.bold:
            t = f"**{t}**"
        elif run.italic:
            t = f"*{t}*"
        parts.append(t)
    return "".join(parts) if parts else paragraph.text


def convert_paragraph_v2(paragraph, is_first_normal: bool = False) -> str:
    """保留内联格式的版本。"""
    text = paragraph.text.rstrip()
    style = paragraph.style.name
    if not text.strip():
        return ""

    t = text.strip()

    if style == "Title" or style == "Heading 1":
        return f"# {t}"
    if style == "Heading 2":
        return f"### {t}"
    if style == "Heading 3":
        return f"#### {t}"
    if style == "Heading 4":
        return f"##### {t}"

    if CHAPTER_RE.match(t):
        return f"## {t}"
    if SECTION_RE.match(t):
        return f"### {t}"

    # 文档首段 Normal 样式视为 H1（仅当长度适中，避免与章节标题冲突）
    if is_first_normal and len(t) <= 30:
        return f"# {t}"
    if is_first_normal and len(t) > 30:
        # 长段落视为引言，保留为正文
        pass

    # 列表
    lvl = list_paragraph_level(paragraph)
    if lvl is not None:
        # 对列表项使用内联格式（保留加粗等）
        inline = merge_paragraph_runs_to_md(paragraph).strip()
        indent = "  " * lvl
        return f"{indent}- {inline}"

    return t


def convert_docx_to_md(src_path: str, out_path: str, use_inline_format: bool = True):
    doc = Document(src_path)
    out_lines = []
    fn = convert_paragraph_v2 if use_inline_format else convert_paragraph

    first_normal_seen = False
    for block in iter_block_items(doc):
        if hasattr(block, "text") and not hasattr(block, "rows"):
            is_first = False
            if not first_normal_seen and block.text.strip() and block.style.name == "Normal":
                is_first = True
                first_normal_seen = True
            line = fn(block, is_first_normal=is_first)
            if line:
                out_lines.append(line)
        else:
            md = table_to_md(block)
            if md:
                out_lines.append("")
                out_lines.append(md)
                out_lines.append("")

    text = "\n".join(out_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip() + "\n"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Written: {out_path} ({len(text)} chars, {len(out_lines)} lines)")


if __name__ == "__main__":
    convert_docx_to_md(
        os.path.join(SRC_DIR, "免疫学复习笔记.docx"),
        "src/content/posts/医学免疫学复习笔记/_raw.md",
    )
    convert_docx_to_md(
        os.path.join(SRC_DIR, "免疫学名词解释.docx"),
        "src/content/posts/医学免疫学名词解释/_raw.md",
    )
