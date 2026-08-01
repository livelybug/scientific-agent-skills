# 调研结论：当前项目如何把 skill 串起来做端到端数据分析

## 关键发现（先说结论）

**这个仓库里没有写死的 pipeline/orchestrator/main.py。是 170+ 个相互独立、可单独调用的 skill。

- `autoskill` 不是数据流水线，而是"工作流观测→生成 composition recipe"的元工具

## 串起来的机制：不是代码，是"运行时由 LLM 代理调度"

### 2) Skill 描述层：frontmatter 互相 cross-reference
每个 skill 的 frontmatter `description` 字段互相点名，作为"什么时候用我 / 什么时候换我"的软链接。例如：
- `statistical-analysis/SKILL.md` → "For low-level model APIs, see the **statsmodels and pymc** skills"
- `pi-agent/SKILL.md` → 提到 `pi-subagents` 负责"delegation/orchestration"
- `autoskill/SKILL.md` → 提到 `scientific-writing / literature-review / citation-management` 这一类组合

LLM agent 读这些 description 后，会按需求自主选择调用顺序——这就是"链"的真实形态。

### 3) 元工具层：`autoskill` 自动生成"composition recipe"
`skills/autoskill/` 是这个体系里**唯一显式做"skill 串接"**的组件，路径在 [autoskill/SKILL.md:117-134](skills/autoskill/SKILL.md#L117-L134)：

```
screenpipe 记录用户屏幕操作
  → fetch_window.py  → redact.py  → cluster.py
  → match_skills.py （把聚类跟现有 170 个 skill 做 embedding 匹配）
  → synthesize.py   （LLM 判定：reuse / compose / novel）
  → 输出到 ~/.autoskill/proposed/<ts>/
       ├── composition-recipes/<name>/SKILL.md   ← 把已有 skill 串成新 skill
       └── new-skills/<name>/SKILL.md
  → promote.py                                      ← 用户审核后落进 skills/
```

也就是说，**composed（组合）型 recipe 的 SKILL.md 里就只写一节"Workflow"，按顺序 `Invoke the X skill → invoke the Y skill → invoke the Z skill`**，所以 agent 运行时只要读这个 recipe 就自动按序执行。

`autoskill/scripts/run.py:122-127` 是分流的代码位置：
```python
kind = "new-skills" if decision["verdict"] == "novel" else "composition-recipes"
...
(draft_dir / "SKILL.md").write_text(decision["skill_body"])
```


> 注：[exploratory-data-analysis](skills/exploratory-data-analysis) 的 SKILL.md 第 156-244 行明确写了"5 步 Workflow"：authorize → manifest → bounded inspect → add context → scaffold report。其它几个核心 skill（[statistical-analysis](skills/statistical-analysis)、[scientific-writing](skills/scientific-writing)）的 SKILL.md 也都是同样结构："Workflow" 章节按编号小节给出操作步骤，但**步骤之间是自然语言指引，不是 Python 调用**。

## 所以"完整数据分析"在这个项目里的运行形态

1. **没有静态流水线**——agent 在收到任务后，根据每个 skill 的 frontmatter description 决定调谁、什么时候调。
2. **没有共享的中间数据格式**——EDA、特征工程、建模各自把产物写到 `--output` 指定的文件，下一个 skill 通过 `read_csv` / 共享工作区来接力。
3. **想固化一条流水线只有两种办法**：
   - (a) 手写一个 `composition-recipes/<your-recipe>/SKILL.md`，里面把 skill A→B→C 写进 "Workflow"；
   - (b) 跑 `python skills/autoskill/scripts/autoskill.py run --start … --end …`，让 autoskill 监听你做几次分析后自动 draft 出 recipe（需要本机跑 [screenpipe](https://github.com/screenpipe/screenpipe) daemon）。

---

## 附录 A：何时不要用这条通用链路

- **单点问题**：用户只问"画个分布图"或"跑个 t 检验"——直接调对应单 skill，不要拉全套。
- **强领域**：用户明确说"做单细胞"、"做临床报告"、"做化合物筛选"——用 [`scvi-tools`](../skills/scvi-tools) / [`clinical-reports`](../skills/clinical-reports) / [`medchem`](../skills/medchem) 等领域 skill 替换通用阶段 4-7 的对应节点。
- **生产级重跑**：如果同一份数据要反复跑、跨人协作、要求可审计——把 `end-to-end-analysis` 升级为 [`nextflow`](../skills/nextflow) / [`dnalnexus`](../skills/dnanexus-integration) / [`latchbio-integration`](../skills/latchbio-integration) 这类管道层 skill，由它们来调度上方 7 步。

## 附录 B：如何让 agent 持续发现新链路

仓库自带的 [`autoskill`](../skills/autoskill) 会：
1. 通过 [screenpipe](https://github.com/screenpipe/screenpipe) 记录你跑分析时实际打开的窗口、命令、文件；
2. 把重复 ≥2 次的模式聚类；
3. 跟现有 170+ skill 做 embedding 匹配；
4. LLM 判定 → 输出 `composition-recipes/<name>/SKILL.md` 草案；
5. 你审过之后 `promote.py` 落进 `skills/`，从此成为正式 skill。

跑一次：

```bash
export SCREENPIPE_TOKEN=$(screenpipe auth token)
python skills/autoskill/scripts/autoskill.py run \
    --start "2026-08-01T00:00:00Z" \
    --end   "2026-08-01T23:59:59Z" \
    --config skills/autoskill/config.yaml \
    --skills-dir skills
```

新发现的链路会出现在 `~/.autoskill/proposed/<ts>/composition-recipes/`。

---

# 7 个阶段的 skill 就是把机制

下面 7 个阶段的 skill 选择，就是把机制 (2) 显式列出来——既可以由 agent 自主调度，也可以照搬到一份 composition-recipe 里硬编码。

---

## 1. 数据获取与接入

**主用 skill**：[`hugging-science`](../skills/hugging-science)（HuggingFace Hub 通用数据源）, [`bioservices`](../skills/bioservices)（生命科学 API 聚合）, [`cellxgene-census`](../skills/cellxgene-census)（单细胞）, [`primekg`](../skills/primekg)（医学知识图谱）, [`depmap`](../skills/depmap)（癌症依赖图谱）

**通用备选**：`gget`, `pysam`, `onekgpd`, `scvi-tools`, `database-lookup`, `usfiscaldata`, `hugging-science`

**示例命令**（通用 Hub 拉取）：

```bash
# 从 HuggingFace Hub 拉取一个 CSV 数据集到本地
python skills/hugging-science/scripts/fetch_catalog.py \
    --repo-id <org>/<dataset> \
    --revision refs/convert/parquet \
    --output data/raw/
```

```python
# 走 bioservices 风格的 API 聚合
from bioservices import BioMart
bm = BioMart(verbose=False)
df = bm.query(dataset="hsapiens_gene_ensembl",
              attributes=["ensembl_gene_id", "external_gene_name"])
df.to_parquet("data/raw/genes.parquet")
```

**输入 / 输出契约**

- 输入：URL / dataset ID / API 凭证（环境变量）
- 输出：`data/raw/<source>.<ext>`，**只读**，禁止就地修改
- 交接物：一个或多个原始文件 + 简短 provenance（来源、版本、抓取时间）

---

## 2. 数据清洗与预处理

**主用 skill**：[`polars`](../skills/polars)（懒求值、快、列式）或 [`dask`](../skills/dask)（超内存并行）

**数据形状相关**：

| 形态 | skill |
|---|---|
| 表格 (CSV/Parquet/JSON) | [`polars`](../skills/polars), [`dask`](../skills/dask), [`vaex`](../skills/vaex) |
| 分子 / 化学式 | [`datamol`](../skills/datamol), [`rdkit`](../skills/rdkit) |
| 单细胞矩阵 | [`anndata`](../skills/anndata), [`scanpy`](../skills/scanpy) |
| 轨迹 / 实验序列 | [`nextflow`](../skills/nextflow)（管道层） |
| 地理 / 空间 | [`geopandas`](../skills/geopandas) |
| 基因组区间 | [`genomic-coordinates`](../skills/genomic-coordinates), [`pysam`](../skills/pysam) |

**示例命令**（polars 通用清洗）：

```python
import polars as pl

df = (
    pl.scan_parquet("data/raw/*.parquet")
      .with_columns(pl.col("timestamp").str.to_datetime())
      .filter(pl.col("value").is_finite())
      .with_columns(pl.col("category").cast(pl.Categorical))
      .collect()
)
df.write_parquet("data/interim/clean.parquet")
```

**输入 / 输出契约**

- 输入：`data/raw/`
- 输出：`data/interim/clean.<ext>` + 配套 `cleaning_log.md`（记录：去重规则、缺失处理、过滤阈值、版本差异）
- 强约束：**永远不要覆盖 raw**；所有变换记录在日志里，可回放

---

## 3. 探索性数据分析 (EDA)

**主用 skill**：[`exploratory-data-analysis`](../skills/exploratory-data-analysis) —— 仓库里最贴近"通用 EDA"的 skill，自带 capability manifest + 受限的本地分析器。

**配套 skill**：[`matplotlib`](../skills/matplotlib), [`seaborn`](../skills/seaborn), [`scientific-visualization`](../skills/scientific-visualization), [`datamol`](../skills/datamol), [`uncertainty-and-units`](../skills/uncertainty-and-units)（单位 / 不确定度）

**示例命令**（来自 [`exploratory-data-analysis/SKILL.md`](../skills/exploratory-data-analysis/SKILL.md) 第 156-244 行的 5 步 Workflow）：

```bash
# Step 2: 写 manifest（边界审计）
python skills/exploratory-data-analysis/scripts/capability_manifest.py inspect \
    data/interim/clean.parquet \
    --root /approved/project \
    --output data/processed/clean.manifest.json

# Step 3: 跑最窄的有界分析
python skills/exploratory-data-analysis/scripts/eda_analyzer.py \
    data/interim/clean.parquet \
    --root /approved/project \
    --max-rows 100000 \
    --output data/processed/clean.eda.json

# 可选：分布/异常/变换敏感性
python skills/exploratory-data-analysis/scripts/distribution_sensitivity.py \
    data/interim/clean.parquet \
    --root /approved/project \
    --column value

# Step 5: 出报告脚手架
python skills/exploratory-data-analysis/scripts/report_scaffold.py \
    --input data/interim/clean.parquet \
    --root /approved/project \
    --output reports/eda.md
```

**输入 / 输出契约**

- 输入：`data/interim/clean.<ext>`
- 输出：`data/processed/<name>.eda.json`（机器可读聚合）+ `reports/eda.md`（人读叙事）
- 强约束：EDA 阶段**只读**，不做缺失填补 / 离群点删除 / 标准化；只输出"flag"和建议

---

## 4. 特征工程

**主用 skill**：[`scikit-learn`](../skills/scikit-learn) —— 自带 `Pipeline` / `ColumnTransformer`，把变换写成一个可序列化的对象，是这一阶段的事实标准。

**备选**：纯表操作 [`polars`](../skills/polars)；显式特征选择 [`shap`](../skills/shap)（事后归因 / 排序用）；时序特征 [`aeon`](../skills/aeon)；NLP/Embedding [`transformers`](../skills/transformers)。

**示例命令**（来自 [`scikit-learn/SKILL.md`](../skills/scikit-learn/SKILL.md) Quick Start）：

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# 1) 切分 —— 必须在拟合任何变换之前
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 2) 数值 vs 类别列分别走不同变换；用 fit_transform(train) / transform(test)
numeric_features     = ["age", "income"]
categorical_features = ["city", "plan"]
preprocess = ColumnTransformer([
    ("num", StandardScaler(), numeric_features),
    ("cat", "passthrough",   categorical_features),  # 实际可用 OneHotEncoder
])

# 3) 整条管线和模型绑在一起
pipe = Pipeline([("prep", preprocess), ("clf", RandomForestClassifier(random_state=42))])
pipe.fit(X_train, y_train)

# 4) 落盘供下游复用
import joblib
joblib.dump(pipe, "data/processed/feature_pipeline.joblib")
```

**输入 / 输出契约**

- 输入：`data/processed/clean.eda.json` + `data/interim/clean.<ext>`
- 输出：`data/processed/features.parquet`（训练后的特征矩阵）+ `data/processed/feature_pipeline.joblib`（可重放的变换对象）
- 强约束：所有 fit 类步骤只用 train 子集；test 只做 transform。这一步错了，下游评估全部泄露。

---

## 5. 建模与算法选择

**主用 skill**：按数据形态分流（无单一"主" skill）

| 任务 | skill |
|---|---|
| 经典分类 / 回归 / 聚类 / 降维 | [`scikit-learn`](../skills/scikit-learn) |
| 频率派统计建模 (GLM / ARIMA / Panel) | [`statsmodels`](../skills/statsmodels) |
| 贝叶斯层级模型 | [`pymc`](../skills/pymc) |
| 深度学习 (CV / NLP / 多模态) | [`pytorch-lightning`](../skills/pytorch-lightning), [`transformers`](../skills/transformers) |
| 时序预测 | [`timesfm-forecasting`](../skills/timesfm-forecasting), [`aeon`](../skills/aeon) |
| 图神经网络 | [`torch-geometric`](../skills/torch-geometric) |
| 强化学习 | [`stable-baselines3`](../skills/stable-baselines3), [`pufferlib`](../skills/pufferlib) |
| 多目标优化 | [`pymoo`](../skills/pymoo) |
| 生存分析 | [`scikit-survival`](../skills/scikit-survival) |

**示例命令**（承接阶段 4 的 `pipe`）：

```python
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

candidates = {
    "rf":  RandomForestClassifier(n_estimators=300, random_state=42),
    "lr":  LogisticRegression(max_iter=1000),
}
# 注意：cross_val_score 仍要求 pipeline 在内层，特征变换不会泄露
scores = {name: cross_val_score(pipe.set_params(clf=model), X_train, y_train, cv=5)
          for name, model in candidates.items()}
# 选 cv 最高者；落盘整条 pipeline + 模型 + 训练元数据
```

**输入 / 输出契约**

- 输入：`data/processed/features.parquet` + `feature_pipeline.joblib`
- 输出：`models/<algo>/<run-id>/` 含 `model.joblib` / `model.pt` / 训练日志 / 超参表 / CV 分数
- 强约束：训练脚本确定 `random_state`；记录所有超参；落盘版本化的 pip-freeze

---

## 6. 评估与解读

**主用 skill**：[`statistical-analysis`](../skills/statistical-analysis)（假设检验 + 效应量 + APA 报告） + [`shap`](../skills/shap)（特征归因）

**配套**：[`statistical-power`](../skills/statistical-power)（先验 / 事后功效）、[`analytical-method-validation`](../skills/analytical-method-validation)（方法学验证）、[`scientific-critical-thinking`](../skills/scientific-critical-thinking)（GRADE / Cochrane 偏倚评估）、[`what-if-oracle`](../skills/what-if-oracle)（假设探索）

**示例命令**：

```bash
# 假设检验（来自 statistical-analysis 的 Quick Reference）
python skills/statistical-analysis/scripts/assumption_checks.py \
    --input data/processed/features.parquet \
    --group condition --outcome value \
    --output reports/assumptions.json

# SHAP 归因（来自 shap skill frontmatter，Python ≥3.12 + uv）
uv pip install "shap==0.52.0"
```

```python
import shap, joblib
pipe = joblib.load("data/processed/feature_pipeline.joblib")
model = pipe.named_steps["clf"]
explainer = shap.Explainer(model, pipe[:-1].transform(X_train.sample(500, random_state=42)))
shap_values = explainer(pipe[:-1].transform(X_test))
shap.plots.beeswarm(shap_values, show=False)  # → reports/figures/shap_beeswarm.png
```

**输入 / 输出契约**

- 输入：`models/<algo>/<run-id>/` + holdout / test 集
- 输出：`reports/evaluation.md`（效应量 + 置信区间 + 假设 + 假设违背的敏感性分析）+ `reports/figures/`
- 强约束：探索性结果标注 post-hoc；不把关联说成因果；不把非显著说成等价

---

## 7. 结果输出与报告

**主用 skill**：[`scientific-writing`](../skills/scientific-writing)（带 evidence-binding 强约束，禁止幻觉，强制引用 `source_manifest.json` + `claims.csv`）

**格式分发**：

| 媒介 | skill |
|---|---|
| 论文 / 报告 (Markdown + 引用) | [`scientific-writing`](../skills/scientific-writing) |
| 海报 / 大幅 | [`latex-posters`](../skills/latex-posters), [`pptx-posters`](../skills/pptx-posters) |
| 演示幻灯 | [`scientific-slides`](../skills/scientific-slides), [`pptx`](../skills/pptx) |
| 文档 (Word) | [`docx`](../skills/docx) |
| 表格 (Excel) | [`xlsx`](../skills/xlsx) |
| 通用文档转换 | [`markitdown`](../skills/markitdown) |
| 引用 / 文献管理 | [`citation-management`](../skills/citation-management), [`pyzotero`](../skills/pyzotero) |
| 同行评审 | [`peer-review`](../skills/peer-review) |

**示例命令**（写作 intake，来自 [`scientific-writing/SKILL.md`](../skills/scientific-writing/SKILL.md) "Intake" 章节）：

```bash
# 1) 把上游 evaluation.md 当 claims 源，先建 source_manifest.json
python skills/scientific-writing/scripts/build_source_manifest.py \
    --reports reports/evaluation.md \
    --output reports/source_manifest.json

# 2) 渲染最终文档
python skills/scientific-writing/scripts/render_paper.py \
    --manifest reports/source_manifest.json \
    --template assets/paper_template.md \
    --output reports/final.md
```

**输入 / 输出契约**

- 输入：`reports/evaluation.md` + `reports/figures/` + `source_manifest.json`
- 输出：人读最终稿 + 可分发的多格式（PDF/PPTX/DOCX/海报）
- 强约束：不创造任何不能溯源到 `source_manifest.json` 的数字、人名、年份、URL

---

## 端到端 Composition Recipe 示例

下面是一份"把这 7 步固化进一个 skill"的 SKILL.md 模板。把这段内容保存为 `skills/end-to-end-analysis/SKILL.md`，下一次 agent 看到时，会按 Workflow 章节顺序逐项调用。

```markdown
---
allowed-tools: Read Write Edit Bash
description: Run a complete data analysis pipeline from raw data acquisition to final report. Use when the user provides a dataset and asks for a full end-to-end analysis without naming a specific skill. Composes seven existing skills in fixed order. For per-stage depth, invoke the named skill directly instead.
license: MIT
metadata:
    github-path: skills/end-to-end-analysis
    skill-author: K-Dense Inc.
    version: "0.1"
name: end-to-end-analysis
---
# End-to-End Data Analysis

## When to Use

- User supplies data (path, URL, or dataset ID) and asks for "a full analysis", "analyze this dataset", "take it from raw to report".
- User does **not** name a specific algorithm or domain.

Do **not** invoke when:
- User names a single stage (e.g., "do EDA only") — call that skill directly.
- User names a domain (e.g., "single-cell") — domain skill outranks this recipe.

## Workflow

1. **Acquire** — Invoke the [`hugging-science`](../hugging-science) or [`bioservices`](../bioservices) skill. Provide source URL / dataset ID; obtain `data/raw/`. Record provenance.

2. **Clean** — Invoke the [`polars`](../polars) skill (or [`dask`](../dask) if dataset > RAM). Read `data/raw/`, write `data/interim/clean.parquet` + `cleaning_log.md`. **Never overwrite raw.**

3. **EDA** — Invoke the [`exploratory-data-analysis`](../exploratory-data-analysis) skill. Run `capability_manifest.py inspect` → `eda_analyzer.py` → `distribution_sensitivity.py` → `report_scaffold.py`. Output `reports/eda.md` + `<name>.eda.json`. **Read-only**; flag issues, do not modify data.

4. **Features** — Invoke the [`scikit-learn`](../scikit-learn) skill. Build a `Pipeline` with `ColumnTransformer`; split before any fit; save `feature_pipeline.joblib` + `features.parquet`.

5. **Model** — Pick one of [`scikit-learn`](../scikit-learn) (default), [`statsmodels`](../statsmodels) (inference), [`pymc`](../pymc) (Bayesian), or [`pytorch-lightning`](../pytorch-lightning) (DL) based on data shape. Set `random_state`; log to `models/<algo>/<run-id>/`.

6. **Evaluate** — Invoke the [`statistical-analysis`](../statistical-analysis) + [`shap`](../shap) skills. Produce `reports/evaluation.md` with effect sizes + CIs + assumption diagnostics + SHAP. Do not claim causation.

7. **Report** — Invoke the [`scientific-writing`](../scientific-writing) skill. Build `source_manifest.json` from stage 6 outputs; render final document. Do not fabricate any number not traceable to the manifest.

## Stop Conditions

Stop and ask the user if:
- Stage 1 produces no data after two retries.
- Stage 3 reveals data quality issues that block stage 4.
- Stage 6 finds the chosen stage 5 model violates its core assumptions.

## Outputs

```
data/raw/                      # immutable inputs
data/interim/clean.parquet     # stage 2
data/processed/features.parquet # stage 4
data/processed/feature_pipeline.joblib
models/<algo>/<run-id>/        # stage 5
reports/eda.md                 # stage 3
reports/evaluation.md          # stage 6
reports/final.md               # stage 7
reports/figures/               # stages 3, 6, 7
```

## Permissions

This recipe inherits `allowed-tools` from each invoked skill. If a downstream skill requires a tool not in this skill's frontmatter, the agent will surface a permission request.
```

> 把这份 SKILL.md 落盘到 `skills/` 后，agent runtime 只要看到 `end-to-end-analysis` 这个 skill，就会按 Workflow 7 步串行执行——这就是"把 170 个 skill 串成一条链路"的最直接做法。

