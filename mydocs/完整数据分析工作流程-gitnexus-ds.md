# 📊 完整数据分析工作流：阶段、子阶段与处理选项总览

基于对仓库 **45 个技能 (skills)** 的深入探索，以下是完整的数据分析工作流程图。每个阶段列出了可用的子阶段和具体的处理选项。

---

## 🧹 一、数据清洗与预处理 (Data Cleaning & Preprocessing)

### 1.1 数据加载与格式检测
| 选项                                                                             | 来源                                                                   |
| -------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| 200+ 科学文件格式自动检测                                                        | `exploratory-data-analysis/scripts/eda_analyzer.py:detect_file_type()` |
| **通用科学格式**: CSV, TSV, XLSX, JSON, HDF5, Parquet, NPY, NPZ, MAT, FITS, Zarr | `analyze_general_scientific()`                                         |
| **生物信息学格式**: FASTA, FASTQ, SAM/BAM, VCF, BED, GFF/GTF, H5AD               | `analyze_bioinformatics()`                                             |
| **化学/分子格式**: PDB, CIF, MOL, SDF, XYZ, SMI                                  | `detect_file_type()`                                                   |
| **显微成像格式**: TIFF, ND2, LIF, CZI, DCM/NIfTI                                 | `analyze_imaging()`                                                    |
| **光谱/分析化学格式**: mzML, mzXML, FID, JCAMP-DX                                | `detect_file_type()`                                                   |
| pandas/polars 通用读取                                                           | `scikit-learn`, `polars` skill                                         |

### 1.2 缺失值处理
| 选项                                          | 来源                                                                      |
| --------------------------------------------- | ------------------------------------------------------------------------- |
| **SimpleImputer** — 均值/中位数/众数/常量填充 | `sklearn.preprocessing.SimpleImputer`, `classification_pipeline.py:42-48` |
| **KNNImputer** — K近邻插补                    | `sklearn.impute.KNNImputer`                                               |
| **IterativeImputer** — 多变量迭代插补         | `sklearn.impute.IterativeImputer`                                         |
| PyMC 贝叶斯缺失数据处理（将缺失值作为参数）   | `pymc` SKILL.md                                                           |
| 缺失值统计报告                                | `eda_analyzer.py:290-291`, `missing_values` 统计                          |

### 1.3 异常值检测与处理
| 选项                                                  | 来源                                                    |
| ----------------------------------------------------- | ------------------------------------------------------- |
| **IQR 方法** — 四分位距异常值检测 (threshold=1.5/3.0) | `assumption_checks.py:detect_outliers(method='iqr')`    |
| **Z-Score 方法** — 标准差异常值检测 (threshold=3.0)   | `assumption_checks.py:detect_outliers(method='zscore')` |
| **RobustScaler** — 用中位数/IQR替代均值/标准差缩放    | `sklearn.preprocessing.RobustScaler`                    |
| **Winsorizing** / 删除 / 保留（按建议处理）           | `assumption_checks.py:401-405` 建议                     |
| TimesFM 上下文异常检测（时序数据）                    | `timesfm-forecasting/examples/anomaly-detection/`       |

### 1.4 数据标准化/归一化 (Feature Scaling)
| 选项                                       | 何时使用                                | 来源                     |
| ------------------------------------------ | --------------------------------------- | ------------------------ |
| **StandardScaler** (z = (x-μ)/σ)           | SVM, KNN, 神经网络, PCA, 正则化线性模型 | `preprocessing.md:11-17` |
| **MinMaxScaler** ([0, 1]或自定义范围)      | 需要边界值, 非正态分布数据              | `preprocessing.md:30-46` |
| **RobustScaler** (中位数/IQR)              | 含异常值数据                            | `preprocessing.md:49-61` |
| **MaxAbsScaler** ([-1, 1])                 | 稀疏数据, 已中心化数据                  | `preprocessing.md:78-90` |
| **Normalizer** (L1/L2/max)                 | 样本级归一化 (文本特征)                 | `preprocessing.md:64-76` |
| **QuantileTransformer**                    | 强制正态分布或均匀分布                  | sklearn                  |
| **PowerTransformer** (Box-Cox/Yeo-Johnson) | 使数据更接近正态分布                    | sklearn                  |

**来源**: `scikit-learn/references/preprocessing.md`

### 1.5 数据验证与质量控制
| 选项                    | 来源                                                      |
| ----------------------- | --------------------------------------------------------- |
| 文件大小/格式/结构检测  | `eda_analyzer.py:136-148`                                 |
| 样本表验证 (生物信息学) | `bulk-rnaseq/scripts/validate_samplesheet.py`             |
| SMILES 化学结构验证     | `diffdock/scripts/prepare_batch_csv.py:validate_smiles()` |
| 去标识化检查 (临床报告) | `clinical-reports/scripts/validate_case_report.py`        |
| 词数/引用检查           | 临床报告技能                                              |

---

## 🔍 二、探索性数据分析 (EDA)

### 2.1 基本数据概览
| 选项                                                 | 来源                                 |
| ---------------------------------------------------- | ------------------------------------ |
| 数据形状/维度/大小                                   | `eda_analyzer.py:258-263`            |
| 列名/数据类型/缺失值统计                             | `eda_analyzer.py:288-289`            |
| 数据类别检测 (6大类)                                 | `eda_analyzer.py:detect_file_type()` |
| 序列统计 (生物信息学): 序列数/总长度/平均长度/GC含量 | `analyze_bioinformatics()`           |
| 图像统计 (显微成像): 尺寸/通道/位深度/强度范围       | `analyze_imaging()`                  |
| HDF5 层级结构浏览                                    | `eda_analyzer.py:304-324`            |

### 2.2 统计摘要
| 选项                                                | 来源                            |
| --------------------------------------------------- | ------------------------------- |
| **describe()** — 均值/标准差/最小值/四分位数/最大值 | `eda_analyzer.py:291`           |
| 分组统计：每组 N/均值/SD/中位数                     | `statistical-analysis` SKILL.md |
| **Pingouin** 统计报告                               | `statistical-analysis` SKILL.md |
| ArviZ 贝叶斯摘要 (默认89% HDI; `ci_prob=0.95`得95%) | `pymc` SKILL.md                 |

### 2.3 分布分析
| 选项                            | 来源                                                 |
| ------------------------------- | ---------------------------------------------------- |
| **直方图 + 正态分布曲线**       | `assumption_checks.py:68-76`, `seaborn` `histplot()` |
| **Q-Q 图 (Quantile-Quantile)**  | `assumption_checks.py:62-65`                         |
| **Shapiro-Wilk 正态性检验**     | `assumption_checks.py:check_normality()`             |
| 按组正态性检验 (ANOVA/t-test前) | `check_normality_per_group()`                        |
| **KDE 密度估计**                | `seaborn` `kdeplot()`                                |
| **小提琴图 (Violin Plot)**      | `seaborn` `violinplot()`                             |
| **箱线图 (Box Plot)**           | `assumption_checks.py:200-208`, `seaborn`            |

### 2.4 相关性分析
| 选项                                 | 来源                                                    |
| ------------------------------------ | ------------------------------------------------------- |
| **Pearson 相关系数** (线性, 正态)    | `statistical-analysis`                                  |
| **Spearman 秩相关** (非线性, 非正态) | `statistical-analysis`                                  |
| **相关性热图 (Heatmap)**             | `seaborn` `heatmap()`                                   |
| **散点图 + 回归线**                  | `assumption_checks.py:275-292`                          |
| **Pairplot 成对关系图**              | `seaborn` `pairplot()`                                  |
| 临床生物标志物-结局相关性            | `biomarker_classifier.py:correlate_biomarker_outcome()` |

### 2.5 可视化选项概览
| 图表类型                   | 来源技能                                       |
| -------------------------- | ---------------------------------------------- |
| 散点图 / 气泡图            | `matplotlib`, `seaborn`                        |
| 折线图 / 时间序列图        | `matplotlib`, `seaborn`                        |
| 柱状图 / 条形图            | `matplotlib`, `seaborn`                        |
| 直方图 / 核密度估计        | `matplotlib`, `seaborn`                        |
| 箱线图 / 小提琴图 / 蜂群图 | `seaborn`                                      |
| 热图 / 聚类热图            | `seaborn`, `matplotlib`                        |
| 分面网格 (FacetGrid)       | `seaborn`                                      |
| PCA/t-SNE/UMAP 降维图      | `scikit-learn`, `umap-learn`                   |
| Kaplan-Meier 生存曲线      | `clinical-decision-support`, `scikit-survival` |
| 堆叠面积图 / 流图          | `matplotlib`                                   |

### 2.6 EDA 报告生成
| 选项                   | 来源                                         |
| ---------------------- | -------------------------------------------- |
| 自动 Markdown 报告     | `eda_analyzer.py:generate_markdown_report()` |
| 下游分析推荐           | `eda_analyzer.py:474-497`                    |
| 6 大格式类别的参考文件 | `exploratory-data-analysis/references/`      |

---

## 🔧 三、特征工程 (Feature Engineering)

### 3.1 类别变量编码
| 选项                        | 何时使用                    | 来源                            |
| --------------------------- | --------------------------- | ------------------------------- |
| **OneHotEncoder**           | 名义型类别 (无序), 线性模型 | `preprocessing.md:94-100`       |
| **OrdinalEncoder**          | 有序类别                    | `preprocessing.md`              |
| **LabelEncoder**            | 目标变量编码                | `scikit-learn` SKILL.md         |
| **TargetEncoder**           | 高基数类别变量              | sklearn                         |
| **handle_unknown='ignore'** | 测试集中出现未知类别        | `classification_pipeline.py:48` |

### 3.2 特征缩放 (详见 1.4)
- StandardScaler / MinMaxScaler / RobustScaler / MaxAbsScaler / Normalizer

### 3.3 特征变换
| 选项                                       | 来源                                 |
| ------------------------------------------ | ------------------------------------ |
| **PolynomialFeatures** — 多项式/交互项     | `scikit-learn` `PolynomialFeatures`  |
| **KBinsDiscretizer** — 离散化/分箱         | `scikit-learn` `KBinsDiscretizer`    |
| **PowerTransformer** (Box-Cox/Yeo-Johnson) | sklearn                              |
| **QuantileTransformer**                    | sklearn                              |
| **FunctionTransformer** — 自定义变换       | sklearn                              |
| **log1p 对数变换** (如基因表达数据)        | `scanpy/scripts/preprocess.py:56-59` |

### 3.4 特征选择
| 选项                                                    | 来源                                 |
| ------------------------------------------------------- | ------------------------------------ |
| **SelectKBest** (f_classif, mutual_info, chi2)          | `scikit-learn`                       |
| **RFE (递归特征消除)**                                  | `scikit-learn` `RFE`                 |
| **SelectFromModel** (基于 L1/Lasso, 树模型重要性)       | `scikit-learn`                       |
| **VarianceThreshold** (移除低方差特征)                  | `scikit-learn`                       |
| Lasso L1 正则化自动选择                                 | `supervised_learning.md:37-49`       |
| **高可变基因选择 (HVG)** — Seurat/Cell Ranger/Seurat_v3 | `scanpy/scripts/preprocess.py:53-61` |

### 3.5 降维
| 选项                                                  | 来源                                                 |
| ----------------------------------------------------- | ---------------------------------------------------- |
| **PCA** (主成分分析)                                  | `scikit-learn` `PCA`, `clustering_analysis.py:43-46` |
| **TruncatedSVD** (稀疏数据)                           | `scikit-learn`                                       |
| **t-SNE** (可视化)                                    | `scikit-learn` `TSNE`                                |
| **UMAP** (统一流形逼近与投影)                         | `umap-learn` skill                                   |
| **NMF** (非负矩阵分解)                                | `scikit-learn`                                       |
| **FastICA** (独立成分分析)                            | `scikit-learn`                                       |
| **Isomap / LLE / MDS / ClassicalMDS**                 | `scikit-learn`                                       |
| 有监督 UMAP / DensMAP / AlignedUMAP / Parametric UMAP | `umap-learn`                                         |
| Scanpy 降维 (PCA + UMAP + t-SNE)                      | `scanpy/scripts/reduce_dimensions.py`                |

### 3.6 领域特定特征工程
| 领域           | 选项                                                                                                                                                                | 来源                           |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| **化学信息学** | Circular Fingerprint (ECFP), RDKit Descriptors, Mordred Descriptors, MACCS Keys, MolGraphConvFeaturizer, DMPNNFeaturizer, CoulombMatrix, SmilesToImage, SmilesToSeq | `deepchem` SKILL.md:67-93      |
| **化学信息学** | GroverFeaturizer, ChemBERTa, MolFormer (预训练)                                                                                                                     | `deepchem`                     |
| **单细胞**     | 批次校正/回归 (`regress_out`), 高可变基因选择, 标准化                                                                                                               | `scanpy/scripts/preprocess.py` |
| **图神经网络** | 节点特征/边特征/边索引构建                                                                                                                                          | `torch-geometric`              |
| **时序数据**   | 滞后特征, 外部回归变量 (xreg)                                                                                                                                       | `timesfm-forecasting`          |

---

## 🤖 四、建模与算法选择 (Modeling & Algorithm Selection)

### 4.1 监督学习 — 分类
| 算法                              | 何时使用                         | 来源                                                           |
| --------------------------------- | -------------------------------- | -------------------------------------------------------------- |
| **Logistic Regression**           | 可解释性, 概率输出, 二/多分类    | `supervised_learning.md:65-78`                                 |
| **Random Forest**                 | 基准模型, 抗过拟合, 特征重要性   | `supervised_learning.md`, `classification_pipeline.py:105-107` |
| **Gradient Boosting**             | 高性能, 表格数据                 | `classification_pipeline.py:108-111`                           |
| **XGBoost / LightGBM / CatBoost** | 工业级梯度提升                   | `shap` (解释了所有树模型)                                      |
| **SVC (支持向量机)**              | 小中数据集, 复杂决策边界, 核方法 | `supervised_learning.md:93-100`                                |
| **SGDClassifier**                 | 大规模数据集 (>10^4)             | `supervised_learning.md:81-91`                                 |
| **K-Nearest Neighbors**           | 简单基准                         | `scikit-learn`                                                 |
| **Naive Bayes**                   | 文本分类, 高维数据               | `scikit-learn`                                                 |
| **MLPClassifier**                 | 非线性, 中等规模                 | `scikit-learn`                                                 |

### 4.2 监督学习 — 回归
| 算法                                  | 何时使用             | 来源                           |
| ------------------------------------- | -------------------- | ------------------------------ |
| **Linear Regression** (OLS)           | 线性关系, 可解释性   | `supervised_learning.md:11-22` |
| **Ridge** (L2 正则化)                 | 多重共线性           | `supervised_learning.md:24-34` |
| **Lasso** (L1 正则化)                 | 特征选择+稀疏模型    | `supervised_learning.md:37-49` |
| **ElasticNet** (L1+L2)                | 两者兼顾             | `supervised_learning.md:52-61` |
| **Random Forest / Gradient Boosting** | 非线性回归           | `scikit-learn`                 |
| **SVR**                               | 中小数据集非线性回归 | `scikit-learn`                 |

### 4.3 无监督学习 — 聚类
| 算法                                       | 何时使用             | 来源                             |
| ------------------------------------------ | -------------------- | -------------------------------- |
| **K-Means**                                | 球形簇, 快速/可扩展  | `clustering_analysis.py:132`     |
| **DBSCAN**                                 | 任意形状簇, 噪声检测 | `clustering_analysis.py:139-140` |
| **HDBSCAN / OPTICS**                       | DBSCAN 改进版        | `scikit-learn`                   |
| **Agglomerative Clustering**               | 层次聚类             | `clustering_analysis.py:133`     |
| **Gaussian Mixture Models**                | 概率聚类, 软分配     | `clustering_analysis.py:134`     |
| **MeanShift / SpectralClustering / BIRCH** | 特殊用途             | `scikit-learn`                   |
| **MiniBatchKMeans**                        | 大规模数据           | `scikit-learn`                   |

**最佳 K 值选择**: Elbow Method + Silhouette Score | `clustering_analysis.py:51-108`

### 4.4 深度学习
| 框架/范式                                                               | 来源                                    |
| ----------------------------------------------------------------------- | --------------------------------------- |
| **MLPClassifier/MLPRegressor** (scikit-learn 级别)                      | `scikit-learn`                          |
| **PyTorch Lightning** — LightningModule + Trainer + DataModule          | `pytorch-lightning`                     |
| **Transformers** (Hugging Face) — NLP/CV/Audio/多模态 (v5 PyTorch-only) | `transformers`                          |
| **图神经网络** (GCN, GAT, GraphSAGE, GIN)                               | `torch-geometric`                       |
| **DeepChem GNNs** — GCNModel, GATModel, AttentiveFPModel, DMPNNModel    | `deepchem`                              |
| **迁移学习** — ChemBERTa, GROVER, MolFormer                             | `deepchem/scripts/transfer_learning.py` |
| **TimesFM** — 基础时序预测模型                                          | `timesfm-forecasting`                   |
| **Stable-Baselines3** — 强化学习 (PPO, SAC, TD3, A2C, DQN)              | `stable-baselines3`                     |
| **PyTorch Lightning 分布式** — DDP, FSDP, DeepSpeed, 多GPU/TPU          | `pytorch-lightning`                     |

### 4.5 统计建模
| 模型类型                                               | 来源                   |
| ------------------------------------------------------ | ---------------------- |
| **OLS 线性回归**                                       | `statsmodels` `sm.OLS` |
| **GLM** (Logistic/Poisson/Gamma)                       | `statsmodels`          |
| **Mixed Models** (混合效应模型)                        | `statsmodels`          |
| **ARIMA / SARIMAX / VAR** (时序分析)                   | `statsmodels`          |
| **贝叶斯建模** — 线性/逻辑/层次/时序/缺失数据/测量误差 | `pymc`                 |
| **MCMC 采样** — NUTS, NumPyro, BlackJAX 采样器         | `pymc`                 |
| **变分推断 (VI)**                                      | `pymc`                 |
| **多元优化 (多目标)** — NSGA-II, MOEA/D                | `pymoo`                |

### 4.6 生存分析
| 模型                                                      | 来源              |
| --------------------------------------------------------- | ----------------- |
| **Cox Proportional Hazards** (标准 + 弹性网惩罚)          | `scikit-survival` |
| **Random Survival Forest**                                | `scikit-survival` |
| **Gradient Boosting Survival Analysis**                   | `scikit-survival` |
| **Survival SVM** (FastSurvivalSVM, FastKernelSurvivalSVM) | `scikit-survival` |
| **Kaplan-Meier 估计**                                     | `scikit-survival` |
| **Nelson-Aalen 估计**                                     | `scikit-survival` |

### 4.7 算法选择决策参考
| 条件                         | 推荐                                      |
| ---------------------------- | ----------------------------------------- |
| 小数据集 (<1K), 可解释性优先 | Logistic/Linear Regression, Random Forest |
| 表格数据, 高性能             | Gradient Boosting (XGBoost/LightGBM)      |
| 高维数据 (p > n)             | CoxnetSurvivalAnalysis, Lasso/ElasticNet  |
| 大规模数据 (>10K)            | SGD, MiniBatchKMeans, GNN                 |
| 序列/文本/图像               | Transformers, PyTorch Lightning           |
| 图结构数据                   | GCN, GAT, GraphSAGE (torch-geometric)     |
| 因果推断                     | statsmodels, Bayesian (pymc)              |
| 时间序列预测                 | ARIMA/SARIMAX, TimesFM                    |
| 不确定性量化                 | PyMC (贝叶斯)                             |

---

## 📊 五、评估与解读 (Evaluation & Interpretation)

### 5.1 统计假设检验
| 检验                                         | 用途                                                    | 来源                                                   |
| -------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------ |
| **Shapiro-Wilk**                             | 正态性                                                  | `assumption_checks.py:check_normality()`               |
| **Levene**                                   | 方差齐性                                                | `assumption_checks.py:check_homogeneity_of_variance()` |
| **Breusch-Pagan**                            | 异方差性                                                | `assumption_checks.py:check_regression_diagnostics()`  |
| **Durbin-Watson**                            | 自相关                                                  | `assumption_checks.py:453-454`                         |
| **VIF**                                      | 多重共线性                                              | `assumption_checks.py:462-465`                         |
| 4-面板诊断图 (残差/QQ/Scale-Location/直方图) | `assumption_checks.py:467-494`                          |                                                        |
| 综合性假设检查                               | `assumption_checks.py:comprehensive_assumption_check()` |                                                        |

### 5.2 交叉验证策略
| 策略                           | 何时使用                           | 来源                          |
| ------------------------------ | ---------------------------------- | ----------------------------- |
| **KFold** (k=5/10)             | 标准 CV                            | `model_evaluation.md:32-41`   |
| **StratifiedKFold**            | 不平衡分类                         | `model_evaluation.md:43-53`   |
| **TimeSeriesSplit**            | 时序数据                           | `model_evaluation.md:55-66`   |
| **GroupKFold**                 | 样本不独立 (按组)                  | `model_evaluation.md:67-77`   |
| **LeaveOneOut**                | 极小数据集                         | `model_evaluation.md:80-90`   |
| **Scaffold Split**             | 化学分子 (防止结构泄漏)            | `deepchem` `ScaffoldSplitter` |
| **Butina Split**               | 分子聚类分割                       | `deepchem`                    |
| 留一法/留组法交叉验证 (LOO-CV) | `pymc/scripts/model_comparison.py` |                               |

### 5.3 超参数调优
| 方法                               | 来源                                                        |
| ---------------------------------- | ----------------------------------------------------------- |
| **GridSearchCV** (穷举搜索)        | `model_evaluation.md`, `classification_pipeline.py:155-163` |
| **RandomizedSearchCV** (随机搜索)  | `model_evaluation.md`                                       |
| **HalvingGridSearchCV** (连续减半) | `model_evaluation.md`                                       |
| **Optuna / Hyperopt**              | 第三方工具                                                  |

### 5.4 模型评估指标
#### 分类指标
| 指标                                                     | 来源                                 |
| -------------------------------------------------------- | ------------------------------------ |
| **Accuracy**                                             | `classification_pipeline.py:175`     |
| **Precision / Recall / F1-Score** (macro/micro/weighted) | `classification_pipeline.py:176-178` |
| **ROC AUC** (二分类)                                     | `classification_pipeline.py:186-188` |
| **Confusion Matrix**                                     | `classification_pipeline.py:198`     |
| **Classification Report**                                | `classification_pipeline.py:193`     |
| **Balanced Accuracy** (不平衡)                           | `deepchem`                           |
| **Log Loss**                                             | sklearn                              |

#### 回归指标
| 指标                 | 来源                  |
| -------------------- | --------------------- |
| **MSE / RMSE / MAE** | `deepchem`, sklearn   |
| **R²**               | `model_evaluation.md` |
| **MAPE**             | sklearn               |

#### 聚类指标
| 指标                                   | 来源                              |
| -------------------------------------- | --------------------------------- |
| **Silhouette Score** (越高越好)        | `clustering_analysis.py:148,163`  |
| **Calinski-Harabasz Index** (越高越好) | `clustering_analysis.py:149,163`  |
| **Davies-Bouldin Index** (越低越好)    | `clustering_analysis.py:150,163`  |
| **Inertia / Elbow Method**             | `clustering_analysis.py:74,80-85` |

#### 贝叶斯模型比较
| 指标                                               | 来源                               |
| -------------------------------------------------- | ---------------------------------- |
| **LOO (Leave-One-Out Cross-Validation)**           | `pymc/scripts/model_comparison.py` |
| **WAIC (Widely Applicable Information Criterion)** | `pymc`                             |
| **Bayes Factor (BF10)**                            | `statistical-analysis`             |
| **Posterior Predictive Checks**                    | `pymc`                             |
| **R-hat / ESS (诊断收敛)**                         | `pymc`                             |

### 5.5 模型解释性
| 方法                                                                                                   | 来源                                 |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------ |
| **特征重要性** (树模型 `.feature_importances_`)                                                        | `classification_pipeline.py:201-214` |
| **SHAP Values** — 全局/局部解释                                                                        | `shap` skill                         |
| **SHAP Explainer 选择** — TreeExplainer → DeepExplainer → LinearExplainer → KernelExplainer → 自动选择 | `shap` SKILL.md:41-56                |
| **SHAP 可视化** — Waterfall, Beeswarm, Bar, Scatter, Force, Heatmap                                    | `shap`                               |
| **系数解释** (线性模型)                                                                                | `statsmodels` `summary()`            |
| **Lasso 系数归零** (特征选择)                                                                          | `supervised_learning.md:48-49`       |
| **PDP/ICE 图**                                                                                         | sklearn                              |

### 5.6 统计效应量
| 统计量                          | 来源                                           |
| ------------------------------- | ---------------------------------------------- |
| **Cohen's d**                   | `statistical-analysis`                         |
| **Partial Eta-squared** (ANOVA) | Pingouin                                       |
| **Cramér's V** (卡方)           | Pingouin                                       |
| **Odds Ratio / Hazard Ratio**   | `scikit-survival`, `clinical-decision-support` |

### 5.7 统计检验选择 (快速参考)
#### 比较两组
| 条件                 | 检验                        |
| -------------------- | --------------------------- |
| 独立 + 连续 + 正态   | Independent t-test          |
| 独立 + 连续 + 非正态 | Mann-Whitney U              |
| 配对 + 连续 + 正态   | Paired t-test               |
| 配对 + 连续 + 非正态 | Wilcoxon signed-rank        |
| 二分类结果           | Chi-square / Fisher's exact |

#### 比较 3+ 组
| 条件                 | 检验                    |
| -------------------- | ----------------------- |
| 独立 + 连续 + 正态   | One-way ANOVA           |
| 独立 + 连续 + 非正态 | Kruskal-Wallis          |
| 配对 + 连续 + 正态   | Repeated measures ANOVA |
| 配对 + 连续 + 非正态 | Friedman test           |

#### 关系分析
| 条件          | 检验                               |
| ------------- | ---------------------------------- |
| 双连续变量    | Pearson (正态) / Spearman (非正态) |
| 连续 + 预测   | Linear Regression                  |
| 二分类 + 预测 | Logistic Regression                |

**来源**: `statistical-analysis/SKILL.md:67-91`

### 5.8 证据质量评估
| 框架                         | 来源                           |
| ---------------------------- | ------------------------------ |
| **GRADE** 证据分级           | `scientific-critical-thinking` |
| **Cochrane Risk of Bias**    | `scientific-critical-thinking` |
| 方法学批评 (内部/外部有效性) | `scientific-critical-thinking` |
| 系统综述与Meta分析           | `scientific-critical-thinking` |

### 5.9 报告与输出
| 选项                             | 来源                                                                |
| -------------------------------- | ------------------------------------------------------------------- |
| **APA 格式统计报告**             | `statistical-analysis`                                              |
| Markdown 分析报告                | `exploratory-data-analysis`                                         |
| 综合诊断报告 (贝叶斯)            | `pymc/scripts/model_diagnostics.py`                                 |
| 决策树/治疗时间线可视化          | `clinical-decision-support`, `treatment-plans`                      |
| 生存分析报告 (含 KM 图 + 风险表) | `clinical-decision-support/generate_survival_analysis.py`           |
| 科研图示/信息图                  | `scientific-schematics`, `infographics`, `scientific-visualization` |
| PPTX/LaTeX 海报                  | `pptx-posters`, `latex-posters`                                     |

---

## 📋 流程全景总结图

```
┌─────────────────────────────────────────────────────────────────────┐
│                     完整数据分析工作流                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. 数据清洗与预处理                                                    │
│  ├─ 1.1 格式检测 ── 200+ 科学文件格式                                   │
│  ├─ 1.2 缺失值处理 ── Simple/KNN/Iterative/Bayesian Imputer           │
│  ├─ 1.3 异常值检测 ── IQR/Z-Score/RobustScaler/Winsorizing            │
│  ├─ 1.4 标准化/归一化 ── Standard/MinMax/Robust/MaxAbs/Normalizer      │
│  └─ 1.5 数据验证 ── 格式/结构/完整性/去标识化                             │
│        ↓                                                            │
│  2. 探索性数据分析 (EDA)                                                │
│  ├─ 2.1 数据概览 ── 维度/类型/缺失值/类别                                │
│  ├─ 2.2 统计摘要 ── describe()/分组统计/贝叶斯摘要                       │
│  ├─ 2.3 分布分析 ── 直方图/QQ图/Shapiro-Wilk/KDE/箱线图/小提琴图         │
│  ├─ 2.4 相关性 ── Pearson/Spearman/Heatmap/散点图/Pairplot             │
│  └─ 2.5 报告生成 ── Markdown + 推荐                                    │
│        ↓                                                            │
│  3. 特征工程                                                            │
│  ├─ 3.1 类别编码 ── OneHot/Ordinal/Label/Target                       │
│  ├─ 3.2 特征缩放 (同 1.4)                                              │
│  ├─ 3.3 特征变换 ── Polynomial/KBins/Power/Quantile/log1p             │
│  ├─ 3.4 特征选择 ── SelectKBest/RFE/L1/FromModel/VarianceThreshold    │
│  ├─ 3.5 降维 ── PCA/TruncatedSVD/t-SNE/UMAP/NMF/FastICA              │
│  └─ 3.6 领域特征 ── 化学指纹/图特征/单细胞/时序滞后                       │
│        ↓                                                            │
│  4. 建模与算法选择                                                        │
│  ├─ 4.1 分类 ── Logistic/RF/GBDT/XGBoost/SVM/KNN/NB/MLP              │
│  ├─ 4.2 回归 ── OLS/Ridge/Lasso/ElasticNet/RF/SVR                    │
│  ├─ 4.3 聚类 ── KMeans/DBSCAN/HDBSCAN/Agglomerative/GMM              │
│  ├─ 4.4 深度学习 ── Lightning/Transformers/GNN/DeepChem/TimesFM       │
│  ├─ 4.5 统计建模 ── OLS/GLM/ARIMA/Mixed Models/Bayesian (PyMC)        │
│  ├─ 4.6 生存分析 ── Cox/RandomSurvivalForest/GradientBoosting/SVM     │
│  └─ 4.7 强化学习 ── PPO/SAC/TD3/A2C/DQN (Stable-Baselines3)          │
│        ↓                                                            │
│  5. 评估与解读                                                           │
│  ├─ 5.1 假设检验 ── Shapiro/Levene/BP/DW/VIF/4-panel诊断               │
│  ├─ 5.2 交叉验证 ── KFold/Stratified/TimeSeries/Group/LOO/Scaffold    │
│  ├─ 5.3 超参调优 ── Grid/Randomized/Halving Search                    │
│  ├─ 5.4 评估指标 ── Accuracy/Precision/F1/ROC-AUC/R²/Silhouette       │
│  ├─ 5.5 模型解释 ── SHAP/Feature Importance/系数/PDP                   │
│  ├─ 5.6 效应量 ── Cohen's d/Eta²/Cramér's V/OR/HR                    │
│  ├─ 5.7 统计检验 ── t-test/ANOVA/Mann-Whitney/Kruskal-Wallis/Chi²     │
│  ├─ 5.8 证据质量 ── GRADE/Cochrane ROB                                │
│  └─ 5.9 报告输出 ── APA/Markdown/图示/海报/生存报告                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔑 涉及的核心技能清单

| 阶段             | 核心技能                                                                                                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 数据清洗与预处理 | `scikit-learn`, `exploratory-data-analysis`, `scanpy`, `polars`                                                                                                          |
| EDA              | `exploratory-data-analysis`, `seaborn`, `matplotlib`, `scientific-visualization`                                                                                         |
| 特征工程         | `scikit-learn`, `umap-learn`, `deepchem`, `scanpy`                                                                                                                       |
| 建模与算法       | `scikit-learn`, `pytorch-lightning`, `transformers`, `torch-geometric`, `pymc`, `statsmodels`, `scikit-survival`, `deepchem`, `timesfm-forecasting`, `stable-baselines3` |
| 评估与解读       | `statistical-analysis`, `shap`, `scientific-critical-thinking`, `experimental-design`, `statistical-power`, `pymc`                                                       |