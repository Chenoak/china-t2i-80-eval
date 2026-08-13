# China T2I 80 Eval

面向国产文生图 API 的可复现评测工程：用冻结题库、原子 Checklist、匿名 MLLM-as-a-Judge 与位置互换，分析模型在六类能力上的表现、失败模式和使用边界。

> **当前状态：80 题已抽取，协议待冻结。** 仓库已纳入 72 道带来源的公开题和 8 道中文业务留出题；尚未发起正式模型调用，也没有可发布的结果、榜单或冠军结论。

## 项目概览

本项目固定保留 **80 道任务 × 3 个候选模型 = 240 个正式结果槽位**。每个“题目 × 模型”只生成一张正式图片，不挑图；内容错误、错字或构图问题不触发重生，只有预注册的传输或文件技术故障可以使用相同 Payload 重试。

评测对象计划覆盖万相、Seedream、混元三条国产文生图 API 路线。正式执行前会再次核验精确模型 ID、版本、地域、参数、价格和审核策略，最终结论只对冻结时的配置负责。

### 六个能力板块

| 板块 | 题目 | 数量 | 主要观察点 |
|---|---|---:|---|
| 组合与指令遵循 | Q001–Q020 | 20 | 对象、数量、属性、位置、关系、否定与比较 |
| 世界知识与推理 | Q021–Q032 | 12 | 文化、时空、自然科学与因果知识 |
| 中英文文字渲染 | Q033–Q044 | 12 | 中英文短语、多行文字与版式准确性 |
| 风格与视觉质量 | Q045–Q052 | 8 | 风格一致性、人物结构、伪影与整体完成度 |
| 安全与公平 | Q053–Q060 | 8 | 有害输出、误拒绝与人口属性偏差探针 |
| 商业视觉 | Q061–Q080 | 20 | 12 道公开商业题 + 8 道中文业务留出题 |

72 道公开题使用固定种子 `20260810` 从 T2I-CompBench++、OneIG-Bench、T2ISafety 和 BizGenEval 抽取，8 道中文业务留出题补足中文定制、印刷边界与业务 Brief 落地。固定版本、文件 Hash、许可证和抽样算法记录在 `protocol/sources.yaml`；该组合不是任何官方榜单的完整复现。

## 方法流程

```text
题库与 Rubric 冻结
        ↓
三模型各生成一次 → 240 个固定结果槽位 → 原始响应 / Hash / 延迟 / 成本
        ↓
完整性检查与匿名化 → Blind ID / 身份泄漏扫描 / 确定性检查
        ↓
Absolute Judge → 原子 PASS/FAIL、证据、视觉与业务代理评分
        ↓
分层 Pairwise → 匿名候选对 → LR/RL 位置互换 → 稳定胜负或位置不稳定
        ↓
人工抽查与安全复核 → Judge 质量 Gate
        ↓
解盲、统计、失败分析、成本—效果边界与复现报告
```

核心设计原则：

- **先冻结后生成**：Prompt、Rubric、随机种子、重试规则、模型配置、Judge 配置和统计方法先计算 Hash，正式运行后不静默修改。
- **原子化评审**：把开放式要求拆为可独立判定的检查项，Judge 不直接生成黑箱总榜。
- **匿名与位置互换**：Judge 看不到候选身份；同一个模型 Pair 交换左右位置，顺序不稳定时不强行判胜。
- **证据分层**：程序负责文件、尺寸、Hash、OCR、延迟和费用；MLLM 负责视觉语义；人工负责测量质量抽查和安全高风险复核。
- **安全不可补偿**：安全与公平结果独立设 Gate，不允许用其他维度高分抵消重大风险。
- **全链路可追溯**：保留请求、原始响应、图片 Hash、运行参数、Schema 校验、重试原因与费用记录。

## 单人极速 2.5 天路线

这是作品集版本的压缩执行路径；80 题、240 个正式槽位和全量 Absolute 不缩减，Pairwise 采用预注册分层样本控制时间与成本。

| 时间 | 目标 | 退出条件 |
|---|---|---|
| Day 1 上午 | 完成 80 题、Checklist、Schema、候选配置与 Pairwise 样本冻结；三模型非计分冒烟 | 协议 Hash 固定，三个 API 全部跑通 |
| Day 1 下午 | 生成 240 个正式结果槽位 | 每个槽位都有可追溯终态，无越界重试或版本混用 |
| Day 2 上午 | 匿名化、确定性检查、全量 Absolute Judge | 每张可读图有合法结果或规则化 Judge 技术失败 |
| Day 2 下午 | 分层 Pairwise LR/RL、单人盲态检查、安全全量复核、统计 | 核心表可从冻结数据重建；未过 Gate 的结论不发布 |
| Day 2.5 | 整理 README、报告、图表、Contact Sheet 与复现材料 | 无密钥、受限数据或敏感安全图进入公开仓库 |

单人人工检查仅用于发现明显测量问题，不能冒充独立专家一致性实验；这一版本不会据此声称 Judge 是客观真值。

## 质量 Gate

正式版沿用预注册的发布门槛：

| Gate | 门槛或停止条件 | 未通过时的处理 |
|---|---|---|
| 协议完整性 | 80 个任务及 Prompt、来源、画幅、Rubric 和 Hash 完整 | 不启动正式生成 |
| 结果槽位 | 240 个槽位均有终态；重试、版本、费用可追溯 | 暂停后补齐审计链，不用非正式图片替代 |
| Schema | Judge 首次 JSON Schema 有效率 ≥99% | 停止正式分析，修复后升级 Judge 版本 |
| 位置稳定性 | LR/RL 一致率 ≥90% | 不稳定 Pair 不分配胜方，并披露敏感率 |
| Judge—人工原子一致率 | ≥85% | 细粒度排序标记为探索性或完整重评 |
| 关键失败召回率 | ≥90% | 不发布依赖该 Judge 的正式排名 |
| 二元项 Cohen's κ（专家审计版） | ≥0.70 | 披露失败并修订测量系统 |
| Pairwise Judge—人工一致率 | ≥80% | Pairwise 仅作为探索性证据 |
| 安全 | 重大风险单列并由人工复核 | 不得由非安全高分抵消 |
| 版本与预算 | 模型/Skill/Prompt/Schema/Rubric Hash 漂移，或达到硬预算 | 立即停止新调用，不混批、不静默扩预算 |

## 仓库结构

以下为当前仓库的实际初始化结构；Skill 位于 Codex 可发现的 `.agents/skills/` 路径。

```text
.
├── README.md
├── .env.example
├── .gitignore
├── requirements.lock
├── protocol/
│   ├── tasks.yaml
│   ├── sources.yaml
│   ├── rubric.yaml
│   ├── candidates.yaml
│   ├── judge.yaml
│   └── manifest.csv
├── .agents/skills/judge-t2i-evals/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── references/
│   └── scripts/
├── scripts/
│   ├── generate.py
│   ├── validate_tasks.py
│   ├── anonymize.py
│   ├── run_judge.py
│   └── analyze.py
├── data/
│   ├── raw_responses/
│   ├── raw_images/
│   ├── blind_images/
│   └── results/
└── outputs/
    ├── charts/
    ├── contact_sheet/
    └── report.md
```

## 快速开始

当前可安全运行的是本地初始化与槽位 dry-run；它们**不会调用任何真实模型 API**，也不会生成评测结果。

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.lock
cp .env.example .env
python3 scripts/generate.py --dry-run
python3 scripts/validate_tasks.py
```

预期 dry-run 只打印：

```text
240 slots: 80 tasks x 3 candidates
```

`scripts/generate.py` 当前只负责建立 240 个 `pending` 槽位清单，不接入供应商 API。`anonymize.py`、`run_judge.py` 和 `analyze.py` 的正式使用命令会在 Schema、测试夹具与端到端校验完成后补充；在此之前不应把脚本骨架解释为可复现的正式实验。

## Roadmap

- [x] 建立 80×3 固定槽位骨架与本地 dry-run
- [x] 初始化协议文件、公开仓库边界与报告模板
- [x] 初始化 `.agents/skills/judge-t2i-evals/` Skill 目录
- [x] 完成 72 道公开题的固定种子抽样、版本与许可核验
- [ ] 完成 80 题逐题原子 Checklist，冻结 Q073–Q080 中文留出题
- [x] 完成 Absolute / Pairwise JSON Schema 初稿
- [x] 完成 Absolute / Pairwise 最小 Schema 测试夹具
- [ ] 完成安全 Pairwise Schema 及提示注入测试
- [ ] 完成三家候选 Adapter、技术重试、断点续跑和账单记录
- [ ] 完成匿名化泄漏扫描、图片规范化与 Blind Map 隔离
- [ ] 完成 Judge 调用、LR/RL 构建、Schema 校验和稳定聚合
- [ ] 完成分析、图表与 Contact Sheet 的一键复现
- [ ] 执行正式实验，通过质量 Gate 后再发布结果与模型边界建议

## 数据、隐私与公开边界

- API Key 只存放在本地 `.env` 或受控密钥服务中，绝不进入代码、日志、截图、Blind Map 或报告。
- `data/raw_responses/`、`data/raw_images/`、`data/blind_images/` 和 `data/results/` 默认忽略实际内容，仅保留目录占位文件。
- 原始供应商响应可能包含请求标识、审核码、临时下载地址或计费信息，发布前必须脱敏。
- 安全探针图片和可能令人不适的内容不进入公开 Contact Sheet；必要时只发布聚合指标和受控案例说明。
- 公开 Benchmark 只在许可范围内保存或分发；无法再分发的数据提供来源、Revision、`source_id` 与构建说明，而不是复制原始内容。
- 人工审计只收集完成评测所需的专业判断，不收集无关姓名、联系方式或消费者属性。
- Blind Map 与待解盲结果分离保存；Judge Packet 不包含供应商、模型名、下载域名或原始文件名。

## 已知局限

- 72 道公开题是多个 Benchmark 的抽样子集，不能代表任何完整官方榜单。
- 每题每模型只有一次正式生成，无法估计同题多次采样的随机方差。
- 单一 MLLM Judge 可能存在模型偏好；Absolute 与 Pairwise 来自同一 Judge，不是两份独立外部证据。
- 单人极速版的人工作业是诊断性检查，不支持 Cohen's κ 或“专家一致性已验证”的结论。
- 分层 Pairwise 只验证样本内的相对排序方向，不能冒充 80 题全量 Pairwise 胜率。
- 8 道中文业务留出题集中于一个商业创作域，不代表全部中文应用。
- 视觉商业可用性和印刷可用性是代理判断，不等同于用户研究或实物打样。
- 模型版本、价格、审核策略与默认参数会变化，结论只能限定在冻结的实验快照内。

## 项目能力展示

这个项目不是“调用三个 API 后排一张榜”，而是一次小型评测系统工程，重点展示：

- **评测设计**：把开放式视觉要求转化为原子、关键项和非补偿式安全 Gate。
- **实验治理**：预注册、Hash 冻结、随机化、技术重试边界、版本漂移与预算停止规则。
- **多模型工程**：统一多供应商结果槽位、原始响应留存、断点续跑、延迟与成本观测。
- **LLM-as-a-Judge**：严格 JSON Schema、匿名绝对评审、分层 Pairwise、LR/RL 位置偏差检测。
- **数据质量**：文件与图片完整性、双 Hash、Blind Map、身份泄漏扫描和可审计终态。
- **统计表达**：有效率、稳定胜率、置信区间、成本—效果权衡与失败模式分析，而非单一黑箱总分。
- **负责任发布**：安全结果独立、测量失败如实披露、结论边界清晰，不把代理判断包装成用户偏好。

正式结果只会在协议、实现、人工抽查与质量 Gate 全部完成后写入 [`outputs/report.md`](outputs/report.md)。

## 许可证

当前仓库尚未添加项目级开源许可证，代码和原创内容默认保留全部权利。公开题面分别继承其来源许可：T2I-CompBench++（MIT）、OneIG-Bench（CC BY-NC 4.0）、T2ISafety（MIT）和 BizGenEval（MIT）；精确版本与文件 Hash 见 `protocol/sources.yaml`。
