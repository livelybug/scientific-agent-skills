#!/usr/bin/env bash
# install-selected.sh — 安装 49 个选中的跨学科 skill 到 income-data-analyse/.agents/skills/
# 源：/home/burt/p2/src/AI/data-analyse/auto-data-analyse/scientific-agent-skills/skills/
# 目标：/home/burt/p2/src/AI/data-analyse/income-data-analyse/.agents/skills/
# 用法：bash install-selected.sh [--dry-run]

set -euo pipefail

SRC="/home/burt/p2/src/AI/data-analyse/auto-data-analyse/scientific-agent-skills/skills"
DST="/home/burt/p2/src/AI/data-analyse/income-data-analyse/.agents/skills"

DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

# 49 个用户选中（按 adoc 当前勾选状态）
SELECTED="aeon arbor autoskill bgpt-paper-search consciousness-council database-lookup exa-search experimental-design exploratory-data-analysis generate-image get-available-resources hypogenic infographics latex-posters liteparse markdown-mermaid-writing markitdown matlab matplotlib networkx nextflow paper-lookup paperzilla parallel-web pdf peer-review polars pptx-posters pymc pymoo research-lookup scientific-brainstorming scientific-critical-thinking scientific-visualization scikit-learn scikit-survival seaborn shap simpy statistical-analysis statistical-power statsmodels sympy timesfm-forecasting umap-learn vaex what-if-oracle xlsx zarr-python"

echo "==> 源: $SRC"
echo "==> 目标: $DST"
echo "==> 选中数: $(echo $SELECTED | wc -w)"
[[ $DRY_RUN == 1 ]] && echo "==> 模式: DRY RUN（不实际复制）" || echo "==> 模式: 实际安装"

# 1. 准备目标目录
if [[ $DRY_RUN == 0 ]]; then
  mkdir -p "$DST"
fi

# 2. 复制每个 skill
copied=0
skipped=0
failed=0
for s in $SELECTED; do
  src_dir="$SRC/$s"
  dst_dir="$DST/$s"
  if [[ ! -d "$src_dir" ]]; then
    echo "  ✗ 缺失: $s （源目录不存在）"
    failed=$((failed+1))
    continue
  fi
  if [[ -e "$dst_dir" ]]; then
    echo "  ⊘ 跳过: $s （目标已存在）"
    skipped=$((skipped+1))
    continue
  fi
  if [[ $DRY_RUN == 1 ]]; then
    echo "  → 将复制: $s"
  else
    cp -r "$src_dir" "$dst_dir"
    echo "  ✓ 已装: $s"
  fi
  copied=$((copied+1))
done

echo ""
echo "==> 完成：复制 $copied | 跳过 $skipped | 失败 $failed"

# 3. 写一个安装清单到目标目录
if [[ $DRY_RUN == 0 ]]; then
  cat > "$DST/INSTALLED.md" <<EOF
# Installed Scientific Agent Skills

**Date:** $(date -u +"%Y-%m-%d %H:%M UTC")
**Source:** $SRC
**Count:** 49 / 149 (跨学科子集，按用户 adoc 勾选)

## 分类概览

* 数据处理与可视化: 11
* 统计与实验设计: 4
* ML / AI / 统计建模: 9
* 通用计算 / 仿真: 3
* 科学写作与沟通: 18
* 数据访问: 2
* 基础设施: 2

## Skills (按字母序)

EOF
  for s in $SELECTED; do echo "- \`$s\`" >> "$DST/INSTALLED.md"; done
  echo ""
  echo "==> 清单已写入: $DST/INSTALLED.md"
fi
