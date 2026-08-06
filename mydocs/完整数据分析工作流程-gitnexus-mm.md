# 数据分析工作流程阶段分析

我从这个仓库（scientific-agent-skills，47541 个符号、279 个执行流）的 SKILL.md 脚本、参考文档和功能模块中提取了完整数据分析工作流的 5 个主要阶段、各自的子阶段以及每个子阶段的数据处理可选项数量。

## 一、总体概览

| 主要阶段                | 关键技能 (skills)                                                                                                    | 子阶段数 | 数据处理可选项总数 |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------- | -------- | ------------------ |
| 1. 数据清洗与预处理     | scikit-learn, scanpy, dask, polars, vaex, neuropixels-analysis, datamol, bulk-rnaseq                                 | 6        | 28+                |
| 2. 探索性数据分析 (EDA) | exploratory-data-analysis, scanpy, statistical-analysis, seaborn, matplotlib, scientific-visualization               | 5        | 35+                |
| 3. 特征工程             | scikit-learn, datamol, molfeat, pymatgen, geniml, umap-learn, scanpy                                                 | 5        | 22+                |
| 4. 建模与算法选择       | scikit-learn, pymc, pytorch-lightning, transformers, torch-geometric, timesfm-forecasting, stable-baselines3, scanpy | 4        | 35+                |
| 5. 评估与解读           | scikit-learn, statistical-analysis, shap, statistical-power, scientific-critical-thinking, peer-review               | 5        | 30+                |

---

## 二、阶段 1：数据清洗与预处理

包含 6 个子阶段，可选项约 28+ 种。

### 子阶段 1.1：缺失值处理 (Missing Value Imputation)
可选项：
1. SimpleImputer (mean/median/most_frequent/constant)
2. KNNImputer
3. IterativeImputer

### 子阶段 1.2：异常值检测与处理 (Outlier Detection & Handling)
可选项：
1. IQR Method
2. Z-score
3. Winsorization
4. Isolation Forest / One-class SVM

### 子阶段 1.3：缩放与归一化 (Scaling & Normalization)
可选项：
1. StandardScaler
2. MinMaxScaler
3. RobustScaler
4. MaxAbsScaler
5. Normalizer (l1/l2/max)
6. Power Transform
7. Quantile Transformation

### 子阶段 1.4：分类变量编码 (Categorical Encoding)
可选项：
1. OneHotEncoder
2. OrdinalEncoder
3. LabelEncoder
4. Target Encoding

### 子阶段 1.5：格式转换与数据加载 (Format Conversion & Loading)
可选项（按数据域）：
- 通用: CSV / TSV / Excel / JSON / Parquet / HDF5 / zarr / .npy
- 单细胞: 10X (mtx/h5) / loom / h5ad / Seurat RDS
- 化学: SDF / SMILES / mol2
- 组学: fastq / bam / vcf / counts
- 神经科学: NWB
- 约 30+ 文件格式

### 子阶段 1.6：领域特异预处理 (Domain-Specific Preprocessing)
- scRNA-seq: QC（基因/细胞/线粒体）+ 归一化（normalize_total）+ log1p + HVG
- 化学分子: standardize_mol + sanitize
- 神经像素: preprocess_recording
- 共计 6+ 选项


### 子阶段 1.7：数据验证与质量控制

```

## 一、方法学级验证（Analytical Method Validation）

### 1. [skills/analytical-method-validation](skills/analytical-method-validation/SKILL.md) — 分析方法验证
> 适用：ICH Q2(R2)/Q14、USP <1220>/<1225>/<1226>、ICH M10、CLSI EP、ISO/IEC 17025；HPLC、LC-MS/MS、GC、CE、ICP-MS、qNMR、qPCR、IR 等。

| 脚本                          | 验证/QC 方法                                                                                                        |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `plan_validation.py`          | 框架选型 (`ich-q2r2 / ich-m10 / usp-1220 / usp-1225 / usp-1226 / clsi / iso-17025`)；按框架生成 study layout 与协议 |
| `check_response.py`           | 校准模型（线性 / 非线性 / 加权）在整个范围内是否成立；Q2(R2) §3.2.2 *response*                                      |
| `check_accuracy_precision.py` | 回收率、重复性、中间精密度、批内/批间方差分解                                                                       |
| `check_detection_limits.py`   | DL / QL：基于信噪比法、标准差外推法、斜率法；与报告阈值对齐                                                         |
| `check_bioanalytical_run.py`  | ICH M10 单次 run 接受准则（calibrator tolerance、QC accuracy、ISR 复算）                                            |
| `compare_methods.py`          | 方法转移 / 等效性：Deming、Passing–Bablok、Bland–Altman、TOST 等效检验                                              |

**方法亮点**：先定框架再定 acceptance criteria；ICH Q2(R1)→Q2(R2) 重组（Range 为父特征，包含 Response 与 Lower Range Limits），多变量方法（2.5/3.2.2.3）有 Annex 2 worked examples；exit code 可作 CI gate。

### 2. [skills/iso-standards-readiness](skills/iso-standards-readiness/SKILL.md) — ISO 标准就绪证据
> 适用：ISO 13485（医疗器械 QMS）、ISO 14971（风险管理）、ISO/IEC 17025（实验室）、ISO 15189（医学实验室）。

| 脚本                            | 验证/QC 方法                                                            |
| ------------------------------- | ----------------------------------------------------------------------- |
| `validate_scope_intake.py`      | 范围声明（scope intake）的结构、必填字段、命名一致性                    |
| `validate_evidence_manifest.py` | evidence manifest 的 JSON Schema 校验、引用闭合、未解析项标记为 blocker |
| `audit_document_records.py`     | 受控文件/记录的版本、日期、审批链（controlled_item + Review.date）      |
| `check_capa.py`                 | CAPA 闭环（纠正 / 预防措施）的要素齐备性、有效性证据                    |
| `check_supplier_controls.py`    | 外部供方控制：评价、监视、再评价的记录                                  |
| `check_traceability.py`         | 计量学溯源链：参考物质 → 测量程序 → 结果                                |
| `check_qmsr_transition.py`      | FDA QMSR（2026-02-02 生效）迁移检查                                     |
| `gap_analyzer.py`               | 框架 → 必需要素 → 现有证据三段差距分析，输出 blocker 列表               |

**方法亮点**：以"draft evidence-preparation material for authorized human review" 自约束，**不**判定合规 / 出证 / 颁照；保留未决项为 blocker。ISO / IEC 文本受版权保护，本地只存 designation + scope + 取证路径。

---

## 二、数据级 QC（Profiling · Missingness · Leakage · Outliers）

### 3. [skills/exploratory-data-analysis](skills/exploratory-data-analysis/SKILL.md) — 探索性数据分析（核心数据 QC）
> 适用：CSV/TSV/JSON、NumPy NPY/NPZ、HDF5、FASTA/FASTQ、PNG/JPEG/TIFF/OME-TIFF 元数据。

| 脚本                                           | 验证/QC 方法                                                                                             |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `capability_manifest.py`                       | 能力矩阵：按扩展名分级（Automated core / optional / reference-only / unsupported），未知格式 fail closed |
| `tabular_profile.py`                           | 矩形 schema 剖析：列数、行数、UTF-8 校验、字段类型、唯一性                                               |
| `missingness_leakage_audit.py`                 | 缺失率（per-column / per-row）、组间缺失模式、train↔test 泄漏（共享样本 ID、重叠记录、目标泄漏）         |
| `distribution_sensitivity.py`                  | 离群点（IQR / MAD / z-score）、变换敏感性（log / sqrt / Box–Cox）                                        |
| `eda_analyzer.py`                              | 端到端 `build_report` / `markdown_report`；仅产出 bounded aggregate，**不**自动删除 / 填补 / 归一化      |
| `report_scaffold.py`                           | 严格的 EDA 报告骨架（无断言式结论）                                                                      |
| `image_inspector.py` / `sequence_inspector.py` | 容器元数据 / 序列前缀 only（Phred+33 aggregate screen）；不读像素或值                                    |

**方法亮点**：Safe I/O 契约——拒绝 URL/管道/symlink/`..`/outside-root；默认 64 MiB 上限，硬顶 512 MiB；tokenized identifier（不是 anonymization）；--reveal-identifiers 仅暴露 basenames/字段名。

### 4. [skills/statistical-analysis](skills/statistical-analysis/SKILL.md) — 统计分析假设检查
| 脚本                   | 验证/QC 方法                                                                                                                                                                                                                                    |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `assumption_checks.py` | `check_normality`（Shapiro–Wilk / D'Agostino / Anderson–Darling）、`check_normality_per_group`、`detect_outliers`（IQR/MAD/Grubbs）、`check_regression_diagnostics`（残差正态、同方差性、多重共线性、自相关）、`comprehensive_assumption_check` |

**方法亮点**：方法选型 + 假设检查 + 效应量 + APA 报告的完整链；假设失败自动给 remedial test。

### 5. [skills/aeon](skills/aeon/) — 时间序列 QC（异常检测/分割）
时间序列的 anomaly detection、change point、segmentation——即对时序数据做数据级 QC。

---

## 三、组学 / 实验数据的领域 QC

### 6. [skills/scanpy](skills/scanpy/SKILL.md) — 单细胞 RNA-seq QC
| 脚本             | QC 方法                                                                                                                                                  |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `qc_analysis.py` | per-cell / per-gene 指标：counts、genes、% mito、% ribo；`make_qc_plots` 前后对比；可选 Scrublet 双体检测；filtering；`run_pipeline.py` 在加载后立即调用 |

### 7. [skills/deeptools](skills/deeptools/SKILL.md) — NGS QC
| 脚本                                                  | QC 方法                                                                                 |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `validate_files.py`                                   | BAM/bigWig/BED 存在性、index（.bai/.csi）、格式正确性                                   |
| `workflow_generator.py::generate_chipseq_qc_workflow` | plotFingerprint、plotCorrelation、plotPCA、plotCoverage；用于 ChIP-seq 富集与样本一致性 |

### 8. [skills/bulk-rnaseq](skills/bulk-rnaseq/) — Bulk RNA-seq QC gate
- `validate_samplesheet.py` — RNA-seq 样本表（FASTQ 路径、strandedness、library layout、replicate 关系）的列与引用闭合
- 内置 **FastQC + fastp/Trim Galore** QC 门，并按 QC gate 决定是否进入 STAR/Salmon 量化。

### 9. [skills/neuropixels-analysis](skills/neuropixels-analysis/) — 神经电生理 QC
- `compute_metrics.py` — SpikeInterface 质量指标（ISI violation、presence ratio、amplitude、SNR、drift）
- `neuropixels_pipeline.py` — 阈值 + 模型（UnitRefine）+ 视觉 AI 协同的 unit curation

### 10. [skills/pacsomatic](skills/pacsomatic/) — 体细胞变异调用前置验证
- `run_pacsomatic.py::parse_args` / `build_nextflow_command` — 输入 BAM、配对样本（tumor/normal）、samplesheet 合规性、参考基因组一致性 dry-run 验证。

### 11. [skills/pydeseq2](skills/pydeseq2/scripts/run_deseq2_analysis.py) — DESeq2 差异分析
- `create_plots` — MA / volcano / dispersion / sample-distance（QC 性质的诊断图）

### 12. [skills/matchms](skills/matchms/scripts/library_search.py) — 质谱数据质量
- `create_processor` — 可插拔的谱图处理管道：归一化、去噪、peak 选取、metadata 校验；用于谱库匹配前 QC。

### 13. [skills/lamindb](skills/lamindb/) — 生物数据湖 + 验证
- Bionty ontology-backed 校验；artifact 注册、lineage 跟踪；为下游每个使用阶段提供 schema 校验入口。

### 14. [skills/fluidsim](skills/fluidsim/) — 数值模拟 QC
- 求解器选择、参数审查、FFT/MPI 配置、restart 兼容性、数值有效性（NaN/Inf/CFL）显式检查；HPC 提交安全门。

### 15. [skills/hypogenic](skills/hypogenic/scripts/audit_dataset.py) — LLM 假设生成数据审计
- `audit_dataset.py::audit` — 标签分布、leakage、schema 闭合；`evaluate_local.py::classification_metrics` 评估数据集质量。

### 16. [skills/pytdc](skills/pytdc/scripts/load_and_split_data.py) — 药效/ADMET 数据
- `validate_request`、`_audit_cold_columns`、`execute_split`（scaffold / random / scaffold+random 的泄漏检查）

---

## 四、元数据 / 标识符 / 坐标级验证

### 17. [skills/ontology-term-resolution](skills/ontology-term-resolution/SKILL.md)
- OLS4 上解析自由文本 → ontology ID；CURIEs（`UBERON:`、`CL:`、`MONDO:`、`HPO:`、`EFO:`、`ChEBI:`、`NCBITaxon:`、`GO:`、`PATO:`）有效性、废弃项检查、替代项推荐。用于 GEO/ENA/BioSamples/CELLxGENE 提交前的 metadata QC。

### 18. [skills/genomic-coordinates](skills/genomic-coordinates/)
- `bed_validator.py::validate`（在 `gtars` 与 `geniml` 中都有）— BED/VCF/GTF 坐标约定审计（0-based vs 1-based）、左右对齐、组装识别（hg19 vs GRCh37 vs GRCh38 vs T2T）、chr-prefix 一致性。

### 19. [skills/geniml](skills/geniml/) — 基因组区间语料 QC
- `bed_validator.py::validate`、`corpus_auditor.py::audit` — BED 与 universe 契约、Region2Vec/scEmbed 兼容性的输入 QC。

### 20. [skills/dnanexus-integration](skills/dnanexus-integration/)
- `validate_dxapp.py::Validator.validate` — `dxapp.json` 必填字段、文件路径闭合；
- `inspect_dxpy.py::missing_required_methods` — API surface drift detection（自动检查 SDK 调用是否仍然存在）。

### 21. [skills/labarchive-integration](skills/labarchive-integration/)
- `entry_operations.py::validate_eln_component` — ELN 条目 schema；
- `command_self_test` — SDK 自身连通性 QC。

### 22. [skills/benchling-integration](skills/benchling-integration/) — Benchling
- Registry entity、inventory、ELN entry、Data Warehouse 查询的 schema 与字段必填校验；Benchling Apps manifest 验证。

### 23. [skills/latchbio-integration](skills/latchbio-integration/) — Latch
- workflow 注册、Registry schema、interface 配置的合规性验证；运行前参数检查。

### 24. [skills/omero-integration](skills/omero-integration/) — OMERO 显微数据
- 容器、annotation、ROI、tables 的 inventory 与 metadata 校验；write 路径强制"先读后写"。

### 25. [skills/opentrons-integration](skills/opentrons-integration/) — 自动化移液
- 协议解析、deck/labware/pipette/module 一致性、runtime parameter、liquid class 验证；`Opentrons App analysis` 作为外部 QC 门。

### 26. [skills/protocolsio-integration](skills/protocolsio-integration/)
- protocols.io REST/MCP 响应 schema 校验；mutation 计划只生成、不执行。

### 27. [skills/geopandas](skills/geopandas/scripts/spatial_join_audit.py) — 空间连接审计
- `audit` — 空间连接前的 CRS 一致性、几何有效性、attribute 泄漏检查。

---

## 五、报告 / 文档 / 临床层面的 QC

### 28. [skills/clinical-decision-support](skills/clinical-decision-support/)
- `deidentification_checklist.py::check_documentation` — PHI/隐私脱敏文档；
- evidence profile、cohort、survival、biomarker 产物的结构化验证。

### 29. [skills/clinical-reports](skills/clinical-reports/)
- case / diagnostic / trial / safety / aggregate 报告草稿的结构化校验；仅合成/去标识/聚合输入。

### 30. [skills/hypothesis-generation](skills/hypothesis-generation/)
| 脚本                              | 验证/QC 方法                                               |
| --------------------------------- | ---------------------------------------------------------- |
| `validate_hypothesis_schema.py`   | 假设 JSON 模式、controls / analysis_plan / AI use sections |
| `validate_prediction_matrix.py`   | 预测矩阵元素齐全、互相可区分                               |
| `check_falsification_controls.py` | 反证控制：nulls、controls、pre-registered outcomes         |
| `check_operationalization.py`     | 操作化（变量 → 测量）                                      |
| `audit_evidence_ledger.py`        | 证据账本：每条声明 ↔ 来源 ↔ 强度                           |
| `lint_causal_claims.py`           | 因果语言层级（associational / causal / mechanistic）lint   |

### 31. [skills/scientific-writing](skills/scientific-writing/scripts/check_consistency.py)
- `validate_methods_results` — 论文方法部分与结果部分的数字 / 端点一致性；
- `check_consistency.py::cli` — 引用、表格、图注的闭合检查。

### 32. [skills/peer-review](skills/peer-review/)
- `audit_citations.py` — 引用真实性、DOI 解析、过度自引；
- `audit_statistics_reproducibility.py` — 统计可复现性：方法-结果数字对齐。

### 33. [skills/scholar-evaluation](skills/scholar-evaluation/scripts/check_process.py)
- `check_process` — scholar 评估的流程合规（数据 / 方法 / 报告三段闭合）。

### 34. [skills/market-research-reports](skills/market-research-reports/scripts/audit_claim_citations.py)
- `audit` — 市场报告声明的引用 / 数字追溯。

### 35. [skills/literature-review](skills/literature-review/)
- 多库（PubMed/arXiv/bioRxiv/Semantic Scholar）系统综述的检索策略与纳入/排除清单 QC。

### 36. [skills/database-lookup](skills/database-lookup/)
- 公共数据库 API 端点的参数、过滤、分页、provenance 显式记录——确保每次查询可复现。

### 37. [skills/experimental-design](skills/experimental-design/)
- 收集数据 *之前* 的设计 QC：随机化、区组、析因设计、统计功效样本量计算（与 statistical-analysis 的 power analysis 对接）。

### 38. [skills/bgpt-paper-search](skills/bgpt-paper-search/)
- 全文论文字段抽取的 25+ 字段（含 sample size、quality scores、methods）——论文级 metadata QC。

### 39. [skills/citation-management](skills/citation-management/)
- 引用元数据准确性、DOI 解析、BibTeX 生成前的 schema 校验。

### 40. [skills/pptx-posters](skills/pptx-posters/scripts/_manifest.py) & [skills/scientific-slides](skills/scientific-slides/scripts/validate_presentation.py)
- `validate_manifest_document`、`_validate_quality`、`PresentationValidator.validate` — 演示 / 海报 manifest 的字段闭合、引用 token 化、文件路径闭合。

### 41. [skills/pptx](skills/pptx/scripts/office/validators/) / [skills/docx](skills/docx/scripts/office/validators/) / [skills/xlsx](skills/xlsx/scripts/office/validators/) — Office 文档 schema 验证
- `BaseSchemaValidator`、`DOCXSchemaValidator`、`PPTXSchemaValidator`、`RedliningValidator` — Office XML schema 校验；redlining 合规。

### 42. [skills/pydicom](skills/pydicom/scripts/deidentification_audit.py) — DICOM 脱敏审计
- `build_report` — PHI 字段在 DICOM header 中的剩余暴露度。

### 43. [skills/neurokit2](skills/neurokit2/scripts/validate_multimodal.py) — 多模态生理信号
- `validate_manifest` — 多模态信号的对齐、采样率、通道命名一致性。

---

## 跨 skill 的共性方法（方法学横向）

把上面四类的具体方法抽象出来，本项目内的"数据验证与质量控制"反复使用以下 5 种工程方法：

| 方法                                                                | 出处脚本举例                                                                                                          |
| ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **JSON Schema / 结构化必填字段校验**                                | `iso-standards-readiness/validate_evidence_manifest.py`、所有 `_manifest.py`、所有 `office/validators/*.py`           |
| **Tokenized / bounded 输出**                                        | `exploratory-data-analysis` 全套（`--reveal-identifiers` 仅暴露 basename）                                            |
| **Exit-code gating**                                                | `analytical-method-validation`（0 无 / 1 发现 / 2 错误输入）、`iso-standards-readiness`                               |
| **Bounded deterministic preflight**（行/列/字段/字节/对象深度封顶） | `exploratory-data-analysis` 64 MiB / 512 MiB 硬顶；`deeptools/validate_files.py`；`pydicom/deidentification_audit.py` |
| **Audit ledger / evidence manifest**（每条结论 ↔ 来源 ↔ 强度）      | `hypothesis-generation/audit_evidence_ledger.py`、`iso-standards-readiness/gap_analyzer.py`、`peer-review/audit_*.py` |

---

## 如何挑选合适的 skill

| 你的场景                                                                            | 用哪个 skill                                                                                                      |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 一个 HPLC / LC-MS / qPCR 方法到底能不能用？                                         | `analytical-method-validation`                                                                                    |
| 整理 ISO 13485/14971/17025/15189 的审计证据                                         | `iso-standards-readiness`                                                                                         |
| 拿到一份 CSV / TSV / JSON，先扫一遍质量                                             | `exploratory-data-analysis`                                                                                       |
| 选 t 检验 / ANOVA 之前先检查正态/方差/离群                                          | `statistical-analysis`（`assumption_checks.py`）                                                                  |
| 单细胞 / Bulk / ChIP-seq / 神经像素 / 体细胞变异                                    | `scanpy` / `bulk-rnaseq` / `deeptools` / `neuropixels-analysis` / `pacsomatic`                                    |
| GEO / ENA / BioSamples 提交前 metadata                                              | `ontology-term-resolution` + `genomic-coordinates`                                                                |
| Benchling / LabArchives / Latch / OMERO / Opentrons / protocols.io 的接入与写前检查 | 对应 `*-integration` 系列                                                                                         |
| 报告 / 论文 / 假设的内部一致性                                                      | `scientific-writing` / `peer-review` / `hypothesis-generation` / `clinical-decision-support` / `clinical-reports` |
| 市场报告 / 文献综述 / 参考文献核查                                                  | `market-research-reports` / `literature-review` / `citation-management` / `bgpt-paper-search`                     |

```
---

## 三、阶段 2：探索性数据分析 (EDA)

包含 5 个子阶段，可选项约 35+ 种。

### 子阶段 2.1：文件类型检测与基础结构 (File Detection & Structure)
- 200+ 科学文件格式的自动检测
- 形状、维度、数据类型识别

### 子阶段 2.2：数据质量评估 (Data Quality Assessment)
可选项：
1. 缺失值模式分析
2. 重复检测
3. 异常值检测
4. 格式合规性检查
5. 元数据一致性验证

### 子阶段 2.3：描述性统计 (Descriptive Statistics)
- mean / median / SD / 分位数 / IQR / skew / kurtosis

### 子阶段 2.4：分布与可视化探索 (Distribution & Visualization)
可选项：
1. Histograms / KDE
2. Box plots
3. Violin plots
4. Scatter / pair plots
5. Correlation matrix / heatmap
6. UMAP / t-SNE / PCA 投影
7. 期刊出版级图（Nature / Science / Cell 风格）

### 子阶段 2.5：领域特异 EDA (Domain-Specific EDA)
- 生物信息: GC 含量、序列长度分布、FASTQ 质量分数
- 成像: 通道/时间/空间校准
- 单细胞: 高变异基因、批次效应初步检测
- 分子: 描述符分布、Lipinski 过滤
- 共计 6+ 选项

---

## 四、阶段 3：特征工程

包含 5 个子阶段，可选项约 22+ 种。

### 子阶段 3.1：特征缩放（复用 1.3）

### 子阶段 3.2：特征构造 (Feature Construction)
可选项：
1. PolynomialFeatures
2. KBinsDiscretizer
3. Spline Features
4. 算术组合（加减乘除）
5. 时间/日期特征提取
6. 文本特征（CountVectorizer / TfidfVectorizer / HashingVectorizer）

### 子阶段 3.3：特征提取 (Feature Extraction)
- 线性: PCA, TruncatedSVD, NMF, FastICA
- 流形: t-SNE, Isomap, LLE, MDS
- UMAP（含 ParametricUMAP / DensMAP / AlignedUMAP）
- 化学: ECFP4/ECFP6/MACCS/拓扑指纹（datamol + molfeat）
- 分子描述符: 200+ RDKit 描述符

### 子阶段 3.4：特征选择 (Feature Selection)
可选项：
1. Filter Methods (SelectKBest, variance threshold)
2. Wrapper Methods (RFE)
3. Embedded Methods (SelectFromModel, L1）
4. 基于树的重要性
5. SHAP-based 重要性

### 子阶段 3.5：特征变换 (Feature Transformation)
- Log / Box-Cox / Yeo-Johnson
- 分箱 / 二值化

---

## 五、阶段 4：建模与算法选择

包含 4 个子阶段，可选项约 35+ 种。

### 子阶段 4.1：有监督学习 (Supervised)
可选项：
1. 线性: Linear/Logistic/Ridge/Lasso/ElasticNet
2. SVM: SVC/SVR（多种 kernel）
3. 树: Decision Tree, Random Forest, Gradient Boosting
4. 集成: AdaBoost, Voting, Stacking
5. 神经网络: MLP
6. KNN / Naive Bayes

### 子阶段 4.2：无监督学习 (Unsupervised)
聚类可选项：
1. K-Means / MiniBatchKMeans
2. DBSCAN / HDBSCAN / OPTICS
3. Agglomerative
4. Gaussian Mixture
5. MeanShift / Spectral / BIRCH
6. Butina (化学)

降维可选项：见 3.3

### 子阶段 4.3：高级建模范式 (Advanced Paradigms)
可选项：
1. 贝叶斯建模 (pymc + arviz)
2. 深度学习 (pytorch-lightning, transformers, torch-geometric)
3. 时间序列 (timesfm-forecasting, ARIMA, Prophet)
4. 强化学习 (stable-baselines3, pufferlib)
5. 图神经网络 (torch-geometric)
6. 单细胞概率模型 (scvi-tools)
7. 域特化（dhdna-profiler, depmap, pydeseq2, pathway-enrichment）

### 子阶段 4.4：超参数优化 (Hyperparameter Tuning)
可选项：
1. GridSearchCV
2. RandomizedSearchCV
3. HalvingGridSearchCV
4. Optuna / Hyperopt

---

## 六、阶段 5：评估与解读

包含 5 个子阶段，可选项约 30+ 种。

### 子阶段 5.1：交叉验证与数据划分 (Validation Strategy)
可选项：
1. KFold
2. StratifiedKFold
3. TimeSeriesSplit
4. GroupKFold
5. Leave-One-Out
6. Nested Cross-Validation

### 子阶段 5.2：性能指标 (Performance Metrics)
分类：
- accuracy / precision / recall / F1 / ROC AUC / log loss / 混淆矩阵 / PR curve
回归：
- MSE / RMSE / MAE / R² / MAPE
聚类：
- Silhouette / Calinski-Harabasz / Davies-Bouldin
总计 10+ 选项

### 子阶段 5.3：统计推断 (Statistical Inference)
可选项：
1. 假设检验（t-test / ANOVA / χ² / 非参数）
2. 效应量（Cohen's d / η² / Cramér's V / R²）
3. 置信区间
4. 多重比较校正（Tukey HSD / Holm / BH-FDR）
5. 贝叶斯（BF₁₀ + 可信区间 + 后验概率）
6. 功效分析（先验 / 灵敏度）

### 子阶段 5.4：模型可解释性 (Interpretability)
可选项：
1. SHAP（Tree/Deep/Linear/Kernel/Permutation）
2. 特征重要性
3. 部分依赖图 (PDP)
4. LIME
5. 水fall / beeswarm / force / heatmap 可视化
6. 公平性与偏差分析

### 子阶段 5.5：报告与可重复性 (Reporting & Reproducibility)
可选项：
1. APA 格式报告
2. 模型持久化（pickle / joblib）
3. MLflow 跟踪
4. 实验笔记本 (open-notebook)
5. 同行评审 (peer-review)
6. 关键性思考 (scientific-critical-thinking)

---

## 七、跨阶段横向能力

存在一些贯穿所有阶段的可选项：

| 横向能力        | 可选项                                              | 涉及技能                                                |
| --------------- | --------------------------------------------------- | ------------------------------------------------------- |
| 并行/分布式计算 | Dask, Spark, joblib, n_jobs                         | dask, vaex, polars, datamol                             |
| 大数据访问      | memory-map, chunking, lazy                          | vaex, polars, dask, zarr-python                         |
| 工作流编排      | pipelines, scripts                                  | scikit-learn Pipeline, scanpy scripts (15 个), nextflow |
| 资源/工具获取   | get-available-resources, database-lookup            | 工具定位                                                |
| 假设生成        | scientific-critical-thinking, hypothesis-generation | 科研规划                                                |

---

## 八、关键发现

1. 仓库共有 1459 个文件、47541 个符号、279 个执行流
2. 主要阶段都是高度模块化的
3. scanpy 提供了 15 个 CLI 脚本（run_pipeline / qc_analysis / preprocess / reduce_dimensions / batch_correct / cluster / find_markers / annotate / score_genes / pseudobulk / subset / plot / convert / inspect_data / run_pipeline），把整个工作流串成一条命令
4. scikit-learn 在每个阶段都提供相应能力：预处理（预处理参考）、特征工程（多项式/分箱/特征选择）、建模（监督+无监督）、评估（CV+网格搜索+多种指标）
5. 可解释性是独立阶段，有 SHAP + LIME + 部分依赖图 + 公平性分析等 6+ 种可选项
6. 阶段并非线性，许多选项可以并行或重复使用（如特征缩放既属于 1.3 也属于 3.1）