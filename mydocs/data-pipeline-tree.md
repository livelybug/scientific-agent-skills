3 级树(主阶段 → 子阶段 → 所有调用的 skill + 一句话功能 + 数据流)。

---

## 🌳 数据分析 7 阶段 × Skill 串接树

### ① 数据获取与接入 (Data Acquisition)
```
├── 1.1 科学数据库/外部数据源(查询型,产出 → 结构化 DataFrame)
│   ├── database-lookup ── 78个公共数据库统一REST入口(PubChem/ChEMBL/UniProt/ClinVar/COSMIC/ClinicalTrials.gov/FRED/USPTO…),含分页、限流、溯源
│   ├── depmap ── 癌症细胞系CRISPR Chronos依赖性 + 药敏数据
│   ├── imaging-data-commons ── NCI 影像数据(CT/MR/PET/病理)下载
│   ├── primekg ── 精准医学知识图谱(基因-药物-疾病-表型)
│   ├── usfiscaldata ── 美国财政部54数据集/179表(国债、TGA、拍卖、CPI…)
│   ├── hugging-science ── 17个科学领域HF数据集/模型/Spaces目录
│   ├── gget ── 20+组学数据库一行命令查询(Ensembl/UniProt/BLAST/CELLxGENE…)
│   ├── bioservices ── 40+生物信息服务(KEGG/UniProt/ChEBI/Reactome/IntAct…)
│   └── biopython ── Entrez编程接口访问PubMed/GenBank/BLAST/分类/PDB/Phylo
│
├── 1.2 实验室/云平台接入(API型,产出 → 项目/记录ID)
│   ├── benchling-integration ── LIMS(DNA/蛋白registry + 库存 + ELN + 任务)
│   ├── dnanexus-integration ── 基因组云平台(FASTQ/BAM/VCF处理 + 流水线)
│   ├── latchbio-integration ── 生信serverless工作流(Nextflow + Registry)
│   ├── omero-integration ── 显微镜数据(ROI/批处理/OMERO.tables)
│   ├── labarchive-integration ── ELN REST API(条目/附件 + OAuth)
│   ├── ginkgo-cloud-lab ── 蛋白表达/纯化/IVT/SPR/DoE云实验
│   ├── opentrons-integration ── Opentrons Python Protocol API v2
│   ├── pylabrobot ── 跨硬件实验室SDK(Hamilton/Opentrons/Tecan + 读板机)
│   └── open-notebook ── 自托管NotebookLM(PDF/音/视频 + 16+AI提供商)
│
├── 1.3 文献/网页情报(产出 → 引用/元数据)
│   ├── paper-lookup ── 10个学术库检索(PubMed/bioRxiv/arXiv/OpenAlex…)
│   ├── bgpt-paper-search ── 全文25+字段结构化抽取(方法/结果/样本量)
│   ├── research-lookup ── 60条去重学术证据 + 证据矩阵 + 共识/冲突综合
│   ├── paperzilla ── 项目-论文匹配/推荐/分类
│   ├── exa-search / parallel-web ── 高质量网页搜索 + URL内容提取
│   └── literature-review ── PRISMA系统综述 + 多引文样式
│
└── 1.4 协议/方案管理
    └── protocolsio-integration ── 协议发布(DOI) + 协作 + 物料管理
```

### ② 数据清洗与预处理 (Data Cleaning)
```
├── 2.1 文档/格式规范化(产出 → Markdown/JSON/CSV)
│   ├── liteparse ── 本地PDF/Office解析,带bbox + 可选Tesseract OCR
│   ├── markitdown ── 20+格式→Markdown(Office/音/视频/HTML/EPUB)
│   ├── pdf / docx / pptx / xlsx ── 原生Office/PDF读写/合并/拆分
│   └── anndata ── 单细胞h5ad标准化结构(obs/var/obsm/layers)
│
├── 2.2 表格/数组清洗(产出 → 干净DataFrame/ndarray)
│   ├── polars ── Rust内核高性能DataFrame(惰性查询 + Arrow)
│   ├── dask ── 超内存DataFrame/Array并行 + 集群扩展
│   ├── vaex ── 十亿行级out-of-core + 内存映射
│   ├── zarr-python ── 分块压缩N维数组(本地/S3/GCS)
│   └── lamindb ── 生物学lakehouse(沿袭追踪 + schema验证 + FAIR)
│
├── 2.3 领域数据标准化
│   ├── bids ── 神经影像BIDS标准(DICOM→BIDS + PyBIDS查询)
│   ├── pydicom ── DICOM读/写/匿名化/窗位/3D重建
│   ├── histolab / pathml ── 全幅病理切片(SVS/TIFF/NDPI)组织检测+tile抽取
│   ├── flowio ── 流式FCS文件(2.0/3.0/3.1)→DataFrame
│   ├── matchms ── 质谱(MGF/MSP/mzML)相似性匹配 + 40+滤波器
│   ├── pyopenms ── LC-MS/MS处理 + 搜库(Comet/Mascot/MSGF+)
│   ├── pysam ── SAM/BAM/CRAM/VCF/FASTA/FASTQ读写 + pileup
│   └── tiledbvcf ── 高性能VCF湖(增量样本 + 并行区域查询 + 云存储)
│
└── 2.4 流水线/调度框架
    ├── nextflow ── DSL2工作流 + nf-core + HPC/云执行
    ├── pacsomatic ── nf-core/pacsomatic肿瘤-正常体细胞变异调用
    └── modal ── Serverless GPU/CPU云函数(uv构建 + 自动扩缩)
```

### ③ 探索性数据分析 (EDA)
```
├── 3.1 自动化EDA
│   └── exploratory-data-analysis ── 统计概览+可视化+洞察一键式
│
├── 3.2 统计可视化(产出 → 出版级图表)
│   ├── matplotlib ── 出版级2D/3D静态/动画图
│   ├── seaborn ── 分布/相关/回归统计图 + 调色板
│   └── scientific-visualization ── 多面板/热图/CI自动/色盲安全 + 期刊样式
│
├── 3.3 网络/图结构探索
│   ├── networkx ── 100+图算法 + 50+生成器 + 8种布局
│   └── torch-geometric ── 图神经网络(PyG 2.7 + 60+卷积层)
│
├── 3.4 空间/地理探索
│   ├── geopandas ── 矢量空间(shapefile/GeoJSON + 空间连接 + 重投影)
│   └── geomaster ── 30+领域遥感/GIS(STAC/COG/Planetary Computer + 500+示例)
│
├── 3.5 时序/信号探索
│   ├── neurokit2 ── 生理信号(ECG/EEG/EDA/RSP/PPG)处理 + HRV/熵
│   ├── astropy ── 天文坐标/单位/FITS表/宇宙学计算/时间尺度
│   └── aeon ── 时序ML(分类/聚类/预测/分割/相似性 + 40+距离)
│
└── 3.6 假设/批判/方法论(产出 → 研究问题/证据)
    ├── hypothesis-generation ── 结构化科学假设生成/评估
    ├── scientific-brainstorming ── 对话式头脑风暴
    ├── scientific-critical-thinking ── 严谨科学推理工具
    ├── peer-review ── 方法学/统计学/可复现性/伦理结构化评审
    └── what-if-oracle ── 4-6分支场景推演(最佳/可能/最差/野牌)
```

### ④ 特征工程 (Feature Engineering)
```
├── 4.1 分子/化学特征化(产出 → 分子描述符/指纹/图)
│   ├── rdkit ── 200+描述符 + 指纹(Morgan/RDKit/MACCS) + 3D坐标 + 反应
│   ├── datamol ── 标准化/互变异构/立体异构 + RDKit增强
│   ├── molfeat ── 100+分子特征器(ECFP/描述符/图 + MolBERT/ChemBERTa/Uni-Mol)
│   ├── medchem ── Lipinski/Veber/PAINS规则 + 结构告警 + 多准则过滤
│   ├── pytdc ── ADMET/药物-靶点/药物-药物/生成基准数据集
│   ├── esm ── 蛋白语言模型(ESM3/ESMC + Forge云 + ESMFold2)
│   └── glycoengineering ── N/O糖基化位点预测 + 治疗性抗体优化
│
├── 4.2 组学特征(产出 → 区间/GRN/轨迹特征)
│   ├── arboreto ── GRN推断(GRNBoost2 + GENIE3 + Dask)
│   ├── geniml ── BED文件无监督ML(Region2Vec/BEDspace/scEmbed)
│   ├── gtars ── 高性能区间/IGD索引/TreeTokenizer + fragsplit
│   ├── polars-bio ── BED/VCF/BAM/GFF区间运算 + 云原生流式
│   ├── deeptools ── BAM→bigWig + 相关性/PCA + 热图矩阵
│   └── scvelo ── RNA速度(剪接/未剪接mRNA) + 潜时 + 驱动基因
│
├── 4.3 数值特征工程(产出 → 缩放/降维/特征集)
│   ├── scikit-learn ── 缩放/编码/插补/多项式/分箱 + Pipeline
│   ├── umap-learn ── 非线性降维(监督/非监督)保留局部+全局
│   ├── scikit-bio ── 多样性指数(α/β) + 距离/系统发育 + 序列比对
│   ├── pymatgen ── 晶体结构/相图/电子结构 + Materials Project
│   ├── cobrapy ── 代谢网络FBA/FVA/基因敲除 + SBML
│   └── astropy ── 物理单位/坐标变换/时间尺度
│
└── 4.4 信号/复杂系统特征
    ├── neurokit2 ── HRV谱/熵/分形维 + 多导联整合
    ├── matchms ── 谱相似性 + 分子指纹比较
    └── molecular-dynamics ── MD模拟(RMSD/RMSF/接触图/自由能面)
```

### ⑤ 建模与算法选择 (Modeling)
```
├── 5.1 经典ML(产出 → 训练好的模型)
│   ├── scikit-learn ── 分类/回归/聚类/降维/异常检测 + Pipeline/调参
│   ├── statsmodels ── OLS/GLM/ARIMA/时间序列 + 诊断
│   ├── scikit-survival ── CoxPH/随机生存森林/SVM-S + C-index/Brier
│   └── aeon ── 时序分类/聚类/预测/异常(ROCKET/InceptionTime/TCN)
│
├── 5.2 深度学习
│   ├── pytorch-lightning ── LightningModule/Trainer + DDP/FSDP/混合精度
│   ├── transformers ── HF 100万+预训练模型 + Trainer + 文本/视觉/多模态
│   ├── torch-geometric ── 60+卷积层(GCN/GAT/SAGE/GIN) + 邻居采样
│   ├── scvi-tools ── 30+单细胞VAE(scVI/scANVI/totalVI/MultiVI/DestVI…)
│   ├── stable-baselines3 ── 可靠RL实现(PPO/SAC/DQN/TD3/DDPG/A2C)
│   ├── pufferlib ── 1M-4M步/秒高性能RL(Ocean环境 + PuffeRL)
│   ├── deepchem ── 分子GNN(GCN/GAT/MPNN/AttentiveFP) + MoleculeNet
│   └── torchdrug ── 20+GNN + 40+数据集 + 知识图谱/逆合成
│
├── 5.3 贝叶斯/概率
│   └── pymc ── MCMC(NUTS/MH) + VI(ADVI/SVGD) + 高斯过程 + 留一法
│
├── 5.4 优化与仿真
│   ├── pymoo ── 多目标进化算法(NSGA-II/III/MOEA/D/SPEA2)
│   ├── simpy ── 离散事件仿真(资源/队列/优先级/实时)
│   └── what-if-oracle ── 决策分支仿真(场景/敏感性)
│
├── 5.5 量子计算
│   ├── qiskit ── IBM量子(VQE/QAOA/QML) + 13M下载 + 83x优化
│   ├── cirq ── Google量子AI硬件(噪声感知电路)
│   ├── pennylane ── 跨平台量子ML(IBM/Braket/Rigetti/IonQ + Catalyst)
│   └── qutip ── 量子动力学(薛定谔/Lindblad/蒙特卡洛)
│
├── 5.6 领域专用模型
│   ├── bulk-rnaseq ★ ── 端到端RNA-seq编排:FASTQ→FastQC→STAR/Salmon→counts→pydeseq2→pathway-enrichment→scientific-visualization
│   ├── pydeseq2 ── 负二项GLM差异表达(尺寸因子/离散度/FDR)
│   ├── scanpy ★ ── 端到端单细胞:h5ad→QC→normalize→HVG→PCA→UMAP→Leiden→markers(内置 run_pipeline.py)
│   ├── pathway-enrichment ── ORA/GSEA/ssGSEA(Enrichr/gseapy/g:Profiler) + GO/KEGG/Reactome/MSigDB
│   ├── phylogenetics / etetoolkit ── MAFFT/IQ-TREE2/FastTree系统发育
│   ├── diffdock / rowan ── 分子对接 + pKa/共折叠(Chai-1/Boltz)
│   ├── molecular-dynamics ── OpenMM/MDAnalysis MD模拟
│   ├── pymatgen / cobrapy ── 材料/代谢
│   ├── matlab / sympy / fluidsim / astropy ── 数值/符号/CFD/天文
│   ├── timesfm-forecasting ── Google零样本单变量时序预训练
│   └── adaptyv / tamarind ── 云实验验证/云GPU结构设计
│
└── 5.7 实验设计与样本量(建模前)
    ├── experimental-design ── 随机化/区组/因子/响应面/序贯/混合
    └── statistical-power ── 样本量/MDE/功效曲线(闭式 + 蒙特卡洛)
```

### ⑥ 评估与解读 (Evaluation & Interpretation)
```
├── 6.1 模型可解释性(产出 → 特征重要性/归因)
│   ├── shap ── TreeExplainer/DeepExplainer/Kernel + 水fall/beeswarm
│   ├── statsmodels ── 系数/置信区间/诊断 + 影响点
│   └── pymc ── 后验分布/预测区间/LOO-CV模型比较
│
├── 6.2 统计评估
│   ├── statistical-analysis ── 假设检验/效应量/APA报告(Pingouin/SciPy)
│   ├── peer-review / scholar-evaluation ── 方法/统计/可复现性/伦理评审
│   └── consciousness-council ── 多视角审议(专家/魔鬼辩护/权衡)
│
├── 6.3 临床/决策支持
│   ├── clinical-decision-support ── GRADE证据分级 + HR/生存/瀑布图
│   ├── what-if-oracle ── 4-6分支情景压测
│   └── consciousness-council ── 复杂决策多视角审议
│
├── 6.4 性能/扩展(模型已训后加速)
│   ├── optimize-for-gpu ── RAPIDS生态(CuPy/cuDF/cuML/cuGraph/cuCIM/cuVS)
│   ├── modal ── Serverless GPU(T4→B200) + 持久卷 + Sandboxes
│   ├── dask ── 多核/集群并行
│   ├── get-available-resources ── 启动时检测CPU/GPU/内存/磁盘 → 推荐策略
│   └── lamindb ── 沿袭追踪(ln.track/flow) + 复现性
│
└── 6.5 自主迭代优化
    ├── arbor ── Hypothesis Tree Refinement(Obs→Ideate→Select→Dispatch→Backprop→Decide)
    ├── autoskill ── 屏幕观察自动发现重复工作流 → 推荐/起草新skill
    └── hypogenic ── 数据驱动+文献混合假设生成(Redis缓存 + 14.19%提升)
```

### ⑦ 结果输出与报告 (Output & Reporting)
```
├── 7.1 文档生成(产出 → 论文/报告文件)
│   ├── scientific-writing ── IMRAD + CONSORT/STROBE/PRISMA + 多引文样式
│   ├── docx / pdf / pptx / xlsx ── 原生Office输出
│   ├── markdown-mermaid-writing ── 24种Mermaid图 + 9个文档模板
│   ├── clinical-reports ── CARE/ICH-E3/SOAP/H&P + HIPAA/FDA合规
│   ├── treatment-plans ── 3-4页LaTeX/PDF临床方案(SMART目标)
│   ├── venue-templates ── Nature/Science/PLOS/IEEE/ACM/NSF/NIH模板
│   └── market-research-reports ── 50+页McKinsey/BCG风格咨询报告
│
├── 7.2 演示/海报/演讲
│   ├── scientific-slides ── Beamer/PPT + 视觉驱动叙事 + 引用
│   ├── latex-posters ── beamerposter/tikzposter/baposter(A0/A1/36×48)
│   └── pptx-posters ── PowerPoint海报(WYSIWYG + 协作)
│
├── 7.3 示意图/插图/信息图
│   ├── scientific-schematics ── AI示意图(Nano Banana + Gemini 3.6 Flash质量门)
│   ├── generate-image ── AI配图(Flux.2 Pro + Gemini 3.6 Flash)
│   ├── infographics ── 10种信息图 + 8种风格 + 色盲安全调色板
│   └── markdown-mermaid-writing ── 文本图表默认
│
├── 7.4 引用管理
│   ├── citation-management ── BibTeX生成/查重 + Google Scholar/PubMed
│   └── pyzotero ── Zotero API v3(Web库/群组/本地 + BibTeX/CSL-JSON)
│
├── 7.5 监管/合规
│   └── iso-13485-certification ── 31份强制程序模板 + QMSR→EU MDR过渡
│
├── 7.6 工作流/复现性/平台
│   ├── nextflow ── DSL2流水线 + nf-core + 容器
│   ├── pacsomatic ── nf-core/pacsomatic封装
│   ├── lamindb ── 沿袭追踪 + schema验证 + 跨工具集成
│   ├── pi-agent ── Pi编码harness + SDK + RPC + 扩展/包/主题
│   ├── modal ── 云端托管 + 端点部署 + 定时任务
│   └── autoskill ── 从使用模式自动生成skill配方
│
└── 7.7 跨阶段支撑(任一阶段可调)
    ├── get-available-resources ── 资源探测 + 战略建议
    └── primekg / hugging-science ── 知识图谱/资源目录
```

---

## ⭐ 三个核心洞察(可作为架构图说明)

1. **没有"中心"orchestrator**:GitNexus 索引里没有 `main → skill_a → skill_b` 这种中心节点。串接是**声明式**的 —— 在 prompt 文本或 `SKILL.md` 描述里写 "use X when Y" 或 "hand off to Z"。
2. **两个显式"准 orchestrator"** 用代码级方式锁定了部分流水线:[bulk-rnaseq](skills/bulk-rnaseq/SKILL.md) 和 [scanpy](skills/scanpy/SKILL.md)。其他都靠 agent 的语义选择。
   * [bulk-rnaseq/skills/bulk-rnaseq/SKILL.md:42](skills/bulk-rnaseq/SKILL.md#L42) 显式声明自己是 "end-to-end bulk RNA-seq orchestrator",画了完整 mermaid 流程图(FASTQ → FastQC → STAR/Salmon → counts → pydeseq2 → pathway-enrichment → scientific-visualization)。
   * [scanpy/skills/scanpy/SKILL.md:56](skills/scanpy/SKILL.md#L56) 通过 `scripts/run_pipeline.py` 一行命令串接 QC→normalize→HVG→PCA→UMAP→Leiden→markers。
3. **跨阶段横切关注点**:`lamindb`(复现性)、`get-available-resources`(环境)、`arbor`(自主优化)、`autoskill`(自我扩展)可以在任意阶段被插入。