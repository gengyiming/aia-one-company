#!/usr/bin/env python3
"""Pre-commit checks for intake workflow compliance."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


ROOT = Path(run(["git", "rev-parse", "--show-toplevel"]))


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1].strip()
    return value


def parse_inline_list(raw: str) -> list[str]:
    inner = raw[1:-1].strip()
    if not inner:
        return []
    return [strip_quotes(part.strip()) for part in inner.split(",") if part.strip()]


def parse_value(raw: str) -> Any:
    raw = raw.strip()
    if raw == "":
        return ""
    if raw.lower() in {"true", "false"}:
        return raw.lower() == "true"
    if raw.startswith("[") and raw.endswith("]"):
        return parse_inline_list(raw)
    return strip_quotes(raw)


def parse_frontmatter(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        return {}

    fm_lines = lines[1:end]
    data: dict[str, Any] = {}
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        if not line.strip():
            i += 1
            continue
        match = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if not match:
            i += 1
            continue
        key = match.group(1).strip()
        raw_value = match.group(2).strip()
        if raw_value:
            data[key] = parse_value(raw_value)
            i += 1
            continue

        # Possible multiline list
        items: list[str] = []
        j = i + 1
        while j < len(fm_lines):
            item_line = fm_lines[j]
            item_match = re.match(r"^\s*-\s+(.*)$", item_line)
            if item_match:
                items.append(strip_quotes(item_match.group(1).strip()))
                j += 1
                continue
            if not item_line.strip():
                j += 1
                continue
            break
        data[key] = items if items else ""
        i = j
    return data


def staged_files() -> list[Path]:
    out = run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"])
    files = [line.strip() for line in out.splitlines() if line.strip()]
    return [ROOT / rel for rel in files]


def obsidian_link_target(raw: Any) -> str:
    if raw is None:
        return ""
    text = strip_quotes(str(raw).strip())
    match = re.match(r"^\[\[([^\]]+)\]\]$", text)
    if not match:
        return ""
    return match.group(1).split("|", 1)[0].strip()


def resolve_note_path(raw: Any) -> Path | None:
    target = obsidian_link_target(raw)
    if not target:
        return None
    candidate = ROOT / target
    if candidate.exists():
        return candidate
    if candidate.suffix == "":
        md_candidate = ROOT / f"{target}.md"
        if md_candidate.exists():
            return md_candidate
        return md_candidate
    return candidate


def to_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value).strip()
    if not text:
        return []
    if text.startswith("[") and text.endswith("]"):
        return parse_inline_list(text)
    return [text]


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def looks_like_product_file(raw_source_file: Any) -> bool:
    text = str(raw_source_file).lower()
    keywords = [
        "product",
        "产品",
        "產品",
        "产品资料",
        "資料冊",
        "资料册",
        "小冊子",
        "小册子",
        "一页精华",
        "一頁精華",
        "计划ppt",
        "計劃ppt",
    ]
    return any(keyword in text for keyword in keywords)


def check_staged_tasks() -> list[str]:
    errors: list[str] = []
    task_files = [
        f
        for f in staged_files()
        if f.suffix.lower() == ".md"
        and "_agent-system/tasks/" in f.as_posix()
        and f.exists()
    ]
    if not task_files:
        return errors

    for task_file in task_files:
        task_fm = parse_frontmatter(task_file)
        status = str(task_fm.get("status", "")).strip().lower()
        input_type = str(task_fm.get("input_type", "")).strip().lower()

        if status != "done" or not input_type:
            continue

        structured_output = task_fm.get("structured_output", "")
        structured_path = resolve_note_path(structured_output)
        rel_task = task_file.relative_to(ROOT).as_posix()

        if not structured_output:
            errors.append(f"{rel_task}: status=done 但缺少 structured_output 字段")
            continue
        if structured_path is None:
            errors.append(f"{rel_task}: structured_output 不是有效 [[链接]]")
            continue
        if not structured_path.exists():
            errors.append(
                f"{rel_task}: structured_output 指向文件不存在 -> "
                f"{structured_path.relative_to(ROOT).as_posix()}"
            )
            continue

        structured_fm = parse_frontmatter(structured_path)
        parse_status = str(structured_fm.get("parse_status", "")).strip().lower()
        if parse_status not in {"complete", "partial"}:
            errors.append(
                f"{rel_task}: 结构化文件 parse_status 非法或缺失（需 complete/partial）"
            )

        if not structured_fm.get("source_file"):
            errors.append(f"{rel_task}: 结构化文件缺少 source_file")

        if input_type == "pdf":
            is_product = boolish(task_fm.get("is_product_file")) or boolish(
                structured_fm.get("is_product_file")
            )
            if not is_product:
                is_product = looks_like_product_file(
                    task_fm.get("source_file", structured_fm.get("source_file", ""))
                )
            if not is_product:
                continue

            raw_card_paths = (
                to_list(task_fm.get("product_card_paths"))
                + to_list(structured_fm.get("product_card_paths"))
            )
            card_paths: list[Path] = []
            for item in raw_card_paths:
                resolved = resolve_note_path(item)
                if resolved is not None:
                    card_paths.append(resolved)
                else:
                    tentative = ROOT / item
                    if tentative.exists():
                        card_paths.append(tentative)
                    elif tentative.suffix == "":
                        card_paths.append(ROOT / f"{item}.md")
                    else:
                        card_paths.append(tentative)

            unique_cards: list[Path] = []
            seen = set()
            for card in card_paths:
                key = card.as_posix()
                if key in seen:
                    continue
                seen.add(key)
                unique_cards.append(card)

            if not unique_cards:
                errors.append(
                    f"{rel_task}: 产品文件任务需填写 product_card_paths 并指向至少1个产品卡"
                )
                continue

            required_keys = ["official_name", "category", "status", "tags"]
            for card in unique_cards:
                rel_card = card.relative_to(ROOT).as_posix()
                if not card.exists():
                    errors.append(f"{rel_task}: product_card_paths 文件不存在 -> {rel_card}")
                    continue
                card_fm = parse_frontmatter(card)
                for key in required_keys:
                    value = card_fm.get(key)
                    if value in {None, "", []}:
                        errors.append(
                            f"{rel_task}: 产品卡 {rel_card} 缺少 Dataview 关键字段 `{key}`"
                        )

    return errors


def main() -> int:
    errors = check_staged_tasks()
    if errors:
        print("✗ pre-commit 检查失败：检测到不合规输入任务。")
        for err in errors:
            print(f"  - {err}")
        print(
            "\n请先补齐结构化输出/产品卡回写字段，再重新 git add 并提交。"
        )
        return 1
    print("✓ pre-commit 检查通过（输入任务结构化与产品卡规则）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
