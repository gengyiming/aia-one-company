#!/usr/bin/env python3
"""Export full PDF text (page-by-page) to a structured Markdown file."""

from __future__ import annotations

import argparse
import hashlib
from datetime import date
from pathlib import Path

import pdfplumber


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a PDF to full page-by-page markdown."
    )
    parser.add_argument("--pdf", required=True, help="Absolute path to source PDF")
    parser.add_argument("--output", required=True, help="Absolute path to output .md")
    parser.add_argument("--source-link", required=True, help="Obsidian [[...]] link")
    parser.add_argument("--task-link", required=True, help="Obsidian [[...]] link")
    parser.add_argument("--title", required=True, help="Document title for markdown")
    parser.add_argument(
        "--tags",
        default="输入处理,全量提取,PDF",
        help="Comma separated tags in frontmatter",
    )
    return parser.parse_args()


def build_markdown(
    pdf_path: Path,
    source_link: str,
    task_link: str,
    title: str,
    tags: list[str],
) -> str:
    today = date.today().isoformat()
    digest = sha256_file(pdf_path)

    page_blocks: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        page_count = len(pdf.pages)
        for idx, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            text = text.strip()
            if not text:
                text = "[本页未提取到可读文本，可能为扫描图像页]"

            page_blocks.append(
                "\n".join(
                    [
                        f"### 第 {idx} 页",
                        "",
                        "```text",
                        text,
                        "```",
                    ]
                )
            )

    fm_lines = [
        "---",
        "source_type: pdf",
        f'source_file: "{source_link}"',
        "parse_status: complete",
        "full_coverage: true",
        f"page_count: {page_count}",
        "parsed_by: ceo",
        f"parsed_date: {today}",
        f'source_task: "{task_link}"',
        f'sha256: "{digest}"',
        "tags: [" + ", ".join(tags) + "]",
        "---",
        "",
    ]

    body_lines = [
        f"# PDF 全量结构化：{title}",
        "",
        "## 文档信息",
        f"- 源文件：{source_link}",
        f"- 任务：{task_link}",
        f"- 页数：{page_count}",
        f"- SHA256：`{digest}`",
        f"- 生成日期：{today}",
        "",
        "## 全文（逐页）",
        "",
        "\n\n".join(page_blocks),
        "",
    ]

    return "\n".join(fm_lines + body_lines)


def main() -> int:
    args = parse_args()
    pdf_path = Path(args.pdf).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    content = build_markdown(
        pdf_path=pdf_path,
        source_link=args.source_link.strip(),
        task_link=args.task_link.strip(),
        title=args.title.strip(),
        tags=tags,
    )
    output_path.write_text(content, encoding="utf-8")
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
