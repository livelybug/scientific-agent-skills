# 完整数据分析工作流程

```mermaid
graph TD
    A["数据获取与接入"] --> B["数据清洗与预处理"]
    B --> C["探索性数据分析 (EDA)"]
    C --> D["特征工程"]
    D --> E["建模与算法选择"]
    E --> F["评估与解读"]
    F --> G["结果输出与报告"]
```

---

## 一、总体概览

| 主要阶段                  | 关键技能 (skills)                                                                                                                                                                                                                                                                                                                              | 子阶段数 | 数据处理可选项总数 |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------ |
| 0. 数据获取与接入         | database-lookup, bioservices, gget, biopython, benchling-integration, paper-lookup, bgpt-paper-search, paperzilla, exa-search, research-lookup, parallel-web, depmap, primekg, imaging-data-commons, usfiscaldata, cellxgene-census, onekgpd, tamarind, tiledbvcf, pydicom, bids, histolab, flowio, dnanexus-integration, lamindb, labarchive-integration, omero-integration, pyzotero | 5        | 180+               |
| 1. 数据清洗与预处理       | scikit-learn, scanpy, dask, polars, vaex, neuropixels-analysis, datamol, bulk-rnaseq                                                                                                                                                                                                                                                           | 6        | 28+                |
| 2. 探索性数据分析 (EDA)   | exploratory-data-analysis, scanpy, statistical-analysis, seaborn, matplotlib, scientific-visualization                                                                                                                                                                                                                                         | 5        | 35+                |
| 3. 特征工程               | scikit-learn, datamol, molfeat, pymatgen, geniml, umap-learn, scanpy                                                                                                                                                                                                                                                                           | 5        | 22+                |
| 4. 建模与算法选择         | scikit-learn, pymc, pytorch-lightning, transformers, torch-geometric, timesfm-forecasting, stable-baselines3, scanpy                                                                                                                                                                                                                          | 4        | 35+                |
| 5. 评估与解读             | scikit-learn, statistical-analysis, shap, statistical-power, scientific-critical-thinking, peer-review                                                                                                                                                                                                                                       | 5        | 30+                |
| 6. 结果输出与报告         | scientific-writing, venue-templates, clinical-reports, clinical-decision-support, treatment-plans, matplotlib, seaborn, plotly, scientific-visualization, scientific-schematics, scientific-slides, latex-posters, pptx-posters, paper-2-web, pdf, docx, pptx, xlsx, markitdown, markdown-mermaid-writing, liteparse, peer-review, market-research-reports, infographics, generate-image, scholar-evaluation, research-grants, citation-management, perplexity-search, literature-review, bgpt-paper-search | 8        | 34+                |
| 7. 其他                   | nextflow                                                                                                                                                                                                                                                                                                                                       | 1        | 1                  |

---

## 阶段 0：数据获取与接入

通过 `database-lookup` 统一网关访问 78+ 数据库，并按子领域扩展出多种数据获取与接入通路。 [1](#0-0) 

| 小阶段 | 可选项 | 代表 Skill |
|---|---|---|
| 0.1 公共数据库查询 | 130+ 数据库与生物信息服务 (PubChem, UniProt, KEGG, Ensembl, ENA, GEO, ChEMBL, ENCODE, AlphaFold, dbSNP, SRA, gnomAD, ExPASy...) | `database-lookup`, `bioservices`, `gget`, `biopython`, `benchling-integration` |
| 0.2 文献检索 | 15+ 学术与综合搜索后端 (PubMed, arXiv, OpenAlex, Semantic Scholar, Google Scholar, BGPT, Exa, Perplexity...) | `paper-lookup`, `bgpt-paper-search`, `paperzilla`, `exa-search`, `research-lookup`, `parallel-web` |
| 0.3 专项数据平台 | 8 个领域知识库 (DepMap, PrimeKG, IDC, US Fiscal Data, cellxgene-census, 1kG, Tamarind, TileDB-VCF) | `depmap`, `primekg`, `imaging-data-commons`, `usfiscaldata`, `cellxgene-census`, `onekgpd`, `tamarind`, `tiledbvcf` |
| 0.4 领域数据格式加载 | 5 种专业科学数据格式 (DICOM, BIDS, WSI, FCS, PACS) | `pydicom`, `bids`, `histolab`, `flowio`, `pacsomatic` |
| 0.5 云平台/实验室数据管理 | 8 个云端与实验室管理平台 (DNAnexus, LatchBio, Lamin, LabArchives, Omero, protocols.io, Ginkgo, Zotero) | `dnanexus-integration`, `latchbio-integration`, `lamindb`, `labarchive-integration`, `omero-integration`, `protocolsio-integration`, `ginkgo-cloud-lab`, `pyzotero` |

---

## 阶段 6：结果输出与报告

将分析结果转化为可交付的论文、报告、海报、幻灯片、临床文档或信息图，覆盖 8 个子阶段、31 个关键 skill、34+ 数据处理可选项。

| 小阶段 | 可选项 | 代表 Skill |
|---|---|---|
| 6.1 科学写作 | IMRAD 论文 + 50+ 期刊与会议模板 | `scientific-writing`, `venue-templates` |
| 6.2 临床报告 | 3 种报告类型 (CARE / 临床决策 / 治疗方案) | `clinical-reports`, `clinical-decision-support`, `treatment-plans` |
| 6.3 可视化图表 | 5 种可视化工具 / 40+ 图表类型 | `matplotlib`, `seaborn`, `plotly`, `scientific-visualization`, `scientific-schematics` |
| 6.4 演示文稿与海报 | 4 种格式 (Beamer / LaTeX Poster / PPTX / HTML 视频) | `scientific-slides`, `latex-posters`, `pptx-posters`, `paper-2-web` |
| 6.5 文档/格式转换 | 7 种格式 (PDF / DOCX / PPTX / XLSX / Markdown / Mermaid / LiteParse) | `pdf`, `docx`, `pptx`, `xlsx`, `markitdown`, `markdown-mermaid-writing`, `liteparse` |
| 6.6 同行评审与质量评估 | 2 类评估 (同行评审 / 学者评估) | `peer-review`, `scholar-evaluation` |
| 6.7 内容传播与资助 | 4 种工具 (咨询报告 / 信息图 / AI 图像 / 资助申请) | `market-research-reports`, `infographics`, `generate-image`, `research-grants` |
| 6.8 引用与文献管理 | 4 种工具 (引用 / Perplexity / 文献综述 / 论文检索) | `citation-management`, `perplexity-search`, `literature-review`, `bgpt-paper-search` |

---

## 阶段 7：其他

不属于数据获取或结果输出的横切型基础设施（工作流编排、跨阶段调度）。

| 小阶段 | 可选项 | 代表 Skill |
|---|---|---|
| 7.1 工作流编排 | 1 个流水线框架 (Nextflow DSL1/DSL2) | `nextflow` |

---

