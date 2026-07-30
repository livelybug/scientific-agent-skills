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