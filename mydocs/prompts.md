* 能用子agent就尽量用子agent.
* 在任何时候，有任何不明白，先用用 gitnexus mcp的 pure-k-dense-skill 索引查询， 还是不明白再用 AskUserQuestion tool 提问，直到完全明白才能继续。

* @mydocs/data-pipeline-tree.md#43  现在要做这个阶段。

这一阶段的子阶段是文件格式识别，文件加载与转化。以下是相关的资料，有点乱，请根据 @mydocs/json/data-pipeline-tree.schema.json#38-94 整理成json 插入 @mydocs/data-pipeline-tree.json#92: 
 
@mydocs/data-pipeline-tree.md#58-68，  @mydocs/EDA-workflow-skill.md#32-117  ， @mydocs/完整数据分析工作流程-gitnexus-ds.md#12-19  ， @mydocs/完整数据分析工作流程02.md#36-44 

要求（「方法清单型」子阶段 — Skill 归属作为上一级 key,方法/工具作为下一级 key）：
- 结构：`<skill>: { <option>: <description> }`（skill 作为父 key，option 作为子 key，value 只写方法简述，不带 `| skill`）
- skill_count = 父 key 数；data_options_estimate = 子 key 总数

value 格式示例：
```json
"statistical-analysis": {
  "z-score-method": "Z-Score 方法 — 标准差异常值检测 (threshold=3.0)"
},
"scikit-learn": {
  "robust-scaler": "RobustScaler — 用中位数/IQR 替代均值/标准差缩放",
  "isolation-forest": "Isolation Forest — 树基隔离异常 (contamination 参数)",
  "one-class-svm": "One-class SVM — 边界学习异常 (RBF/linear 核)"
}
```

最后同步更新Stage级别的Summary与顶层的Summary。

---

### 通用模板（替换占位符后即可复用）

* @mydocs/json/data-pipeline-tree.json#<LINE>  现在要做这个子阶段。

* 这一阶段的子阶段是 `<SUB_STAGE_KEY> <SUB_STAGE_NAME>`（<一句话描述>）。
以下是相关的资料，有点乱，请根据  @mydocs/json/data-pipeline-tree.schema.json#L<SCHEMA_LINE_RANGE>  整理成json ， 插入 @mydocs/json/data-pipeline-tree.json#L<INSERT_LINE> :

* @mydocs/完整数据分析工作流程-gitnexus-ds.md#L<LINE_RANGE>  ， @mydocs/完整数据分析工作流程-gitnexus-mm.md#L<LINE_RANGE>  ， <其他资料源>  

- 最后同步更新 Stage 级别 Summary 与顶层 Summary（`sub_stage_count` / `skill_count` / `data_options_estimate`）

