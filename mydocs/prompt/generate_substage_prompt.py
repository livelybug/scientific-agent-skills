#!/usr/bin/env python3
"""Generate a sub-stage extraction prompt from the CSV catalog.

Usage:
    python generate_substage_prompt.py "1.5 数据标准化/归一化 (Feature Scaling)"

CSV format (wide): the first column is the sub_stage key; remaining columns are
source file names (relative to project root, no path prefix). Empty cells mean
that file does not cover the sub-stage. Column order in the CSV determines
the order of file references in the generated prompt.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

# Prepended to every column-name to form the project-relative file path
MYDOCS_PREFIX = "mydocs/"

# Sub-stage key regex: "X.Y " (digit dot digit space)
SUB_STAGE_KEY_RE = re.compile(r"^(\d+)\.(\d+)\s")
SUB_STAGE_LINE_RE = re.compile(r'^\s*"(\d+)\.(\d+)\s+([^"]+)":\s*\{')

# Prompt template (mirrors mydocs/prompt/prompts.md "通用模板")
PROMPT_TEMPLATE = """* @mydocs/json/data-pipeline-tree.json#L{insert_line}  现在要做这个子阶段。

* 这一阶段的子阶段是 `{sub_stage_key}`（请从下方源文件中提取这个子阶段的内容）。
以下是相关的资料，有点乱，请根据  @mydocs/json/data-pipeline-tree.schema.json#L38-94  整理成json ， 插入 @mydocs/json/data-pipeline-tree.json#L{insert_line} :

* {file_refs}

要求（「方法清单型」子阶段 — Skill 归属作为上一级 key,方法/工具作为下一级 key）：
- 结构：`<skill>: {{ <option>: <description> }}`（skill 作为父 key，option 作为子 key，value 只写方法简述，不带 `| skill`）
- skill_count = 父 key 数；data_options_estimate = 子 key 总数

value 格式示例：
```json
"statistical-analysis": {{
  "z-score-method": "Z-Score 方法 — 标准差异常值检测 (threshold=3.0)"
}},
"scikit-learn": {{
  "robust-scaler": "RobustScaler — 用中位数/IQR 替代均值/标准差缩放",
  "isolation-forest": "Isolation Forest — 树基隔离异常 (contamination 参数)",
  "one-class-svm": "One-class SVM — 边界学习异常 (RBF/linear 核)"
}}
```

最后同步更新 Stage 级别 Summary 与顶层 Summary（`sub_stage_count` / `skill_count` / `data_options_estimate`）。
"""


def read_header(csv_path: Path) -> list[str]:
    """Read the first row of the CSV and return the column names (stripped)."""
    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return []
    return [h.strip() for h in header]


def find_row(csv_path: Path, sub_stage_key: str) -> dict[str, str] | None:
    """Return the row whose first-column value matches sub_stage_key, or None.

    The returned dict preserves CSV column order (Python 3.7+ dict insertion order).
    Cells and header names are stripped of surrounding whitespace defensively.
    Extra cells past the header length are kept under the empty-string key "".
    """
    header = read_header(csv_path)
    if not header:
        return None
    key_col = header[0]
    target = sub_stage_key.strip()

    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for raw_row in reader:
            if not raw_row:
                continue
            row: dict[str, str] = {}
            for i, cell in enumerate(raw_row):
                col = header[i] if i < len(header) else ""
                row[col] = cell.strip()
            if row.get(key_col, "") == target:
                return row
    return None


def build_file_refs(row: dict[str, str], key_col: str) -> tuple[str, list[str]]:
    """Return (joined_refs_string, list_of_skipped_column_names).

    Walks the row in column order. For every column except the key column,
    if the cell is non-empty, emit `@mydocs/<column>.<range>`. Empty or
    unnamed columns are skipped.
    """
    refs: list[str] = []
    skipped: list[str] = []
    for col, val in row.items():
        if col == key_col:
            continue
        if not col:  # unnamed column (e.g. trailing comma)
            continue
        if not val:
            skipped.append(col)
            continue
        refs.append(f"@{MYDOCS_PREFIX}{col}#{val}")
    return "  ， ".join(refs), skipped


def find_insertion_line(json_path: Path, sub_stage_key: str) -> tuple[int, int, str]:
    """Find the insertion line for the new sub_stage in the JSON.

    Returns (insert_after_line, insert_before_line, note) where:
      - insert_after_line: line of the predecessor sub_stage's closing },
                         i.e. the new content goes immediately AFTER this line
      - insert_before_line: insert_after_line + 1 (the new key's expected line)
      - note: explanation when stage doesn't exist yet
    """
    with json_path.open(encoding="utf-8") as f:
        text_lines = f.readlines()

    m = SUB_STAGE_KEY_RE.match(sub_stage_key)
    if not m:
        raise ValueError(
            f"sub_stage_key must start with 'X.Y ' (digit dot digit space): got {sub_stage_key!r}"
        )
    stage_num = m.group(1)
    sub_num = int(m.group(2))

    # Collect all sub_stage keys in this stage (line numbers + sub_num)
    stage_pat = re.compile(rf'^\s*"({re.escape(stage_num)})\.(\d+)\s+([^"]+)":\s*\{{')
    candidates: list[tuple[int, int]] = []  # (sub_num, key_line)
    existing_target_line: int | None = None
    for i, line in enumerate(text_lines, start=1):
        mm = stage_pat.match(line)
        if mm:
            n = int(mm.group(2))
            if n == sub_num and existing_target_line is None:
                existing_target_line = i
            candidates.append((n, i))

    if existing_target_line is not None:
        # Sub-stage already exists — don't pretend to insert
        return (
            existing_target_line,
            existing_target_line,
            f"[warn] 子阶段 {sub_stage_key!r} 已存在于第 {existing_target_line} 行 — 不需要插入",
        )

    if not candidates:
        # No sub_stages in this stage yet — find the "sub_stage": { line
        for i, line in enumerate(text_lines, start=1):
            if '"sub_stage":' in line and "{" in line:
                return (i, i + 1, f"stage_{stage_num} 还没有任何子阶段 — 在 sub_stage 的 {{ 内插入第一行")
        return (len(text_lines), len(text_lines) + 1, "找不到 sub_stage 块；请手动确认")

    candidates.sort()

    # Find predecessor (largest sub_num < target)
    predecessor = None
    for n, key_line in candidates:
        if n < sub_num:
            predecessor = (n, key_line)
        else:
            break

    if predecessor is None:
        # New is the first sub_stage; insert right after "sub_stage": {
        for i, line in enumerate(text_lines, start=1):
            if '"sub_stage":' in line and "{" in line:
                return (i, i + 1, "这是该 stage 的第一个子阶段 — 在 sub_stage 的 { 后插入")
        return (1, 2, "")

    pred_key_line = predecessor[1]
    # Walk forward from pred_key_line counting braces; the first line where depth
    # returns to 0 closes the predecessor's block.
    depth = 0
    end_line = None
    for i in range(pred_key_line - 1, len(text_lines)):
        line = text_lines[i]
        depth += line.count("{") - line.count("}")
        if depth == 0:
            end_line = i + 1  # 1-indexed
            break

    if end_line is None:
        return (pred_key_line, pred_key_line + 1, "[warn] 找不到前一个子阶段的闭合 }，返回近似行号")

    return (end_line, end_line + 1, "")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a sub-stage extraction prompt from the CSV catalog."
    )
    parser.add_argument(
        "sub_stage_key",
        help='JSON sub-stage key, e.g. "1.5 数据标准化/归一化 (Feature Scaling)"',
    )
    parser.add_argument(
        "--csv",
        default="mydocs/prompt/sub_stage_sources.csv",
        help="CSV catalog path (relative to project root)",
    )
    parser.add_argument(
        "--json",
        default="mydocs/json/data-pipeline-tree.json",
        help="Target JSON path (relative to project root)",
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root (default: current directory)",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    csv_path = project_root / args.csv
    json_path = project_root / args.json

    if not csv_path.exists():
        print(f"ERROR: CSV not found: {csv_path}", file=sys.stderr)
        return 2

    header = read_header(csv_path)
    if not header:
        print(f"ERROR: CSV is empty: {csv_path}", file=sys.stderr)
        return 2
    key_col = header[0]

    row = find_row(csv_path, args.sub_stage_key)
    if row is None:
        print(
            f"ERROR: No row in {csv_path} for sub_stage_key={args.sub_stage_key!r}",
            file=sys.stderr,
        )
        return 1

    file_refs, skipped = build_file_refs(row, key_col)
    if skipped:
        print(
            f"# Note: column(s) with empty cell (skipped): {', '.join(skipped)}",
            file=sys.stderr,
        )

    if not json_path.exists():
        print(f"ERROR: JSON not found: {json_path}", file=sys.stderr)
        return 2
    insert_after, insert_before, note = find_insertion_line(json_path, args.sub_stage_key)
    if note:
        print(f"# Insertion note: {note}", file=sys.stderr)

    insert_line = insert_before
    prompt = PROMPT_TEMPLATE.format(
        insert_line=insert_line,
        sub_stage_key=args.sub_stage_key,
        file_refs=file_refs,
    )
    print(prompt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
