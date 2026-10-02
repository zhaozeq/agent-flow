# OpenSpec Schema 汇总

本目录收录了 OpenSpec 的**默认内置 schema**、**全部社区 schema**，以及本项目**自研的
`evidence-driven`**（共 11 个），供本项目参考与复用。

每个子目录都是一个可直接使用的 schema 包，结构统一为：

```
<schema-name>/
├── schema.yaml      # 工作流定义（artifact 列表、依赖、生成物、AI 指令）
├── templates/       # 各 artifact 的 Markdown 模板
└── README.md        # 该 schema 的说明
```

例外：`evidence-driven/` 额外含 `flow-policy.yaml`（流程策略单一事实源），
本目录根部含 `validate_schema.py`（校验器）。

使用方式：把整个子目录复制到目标项目的 `openspec/schemas/<schema-name>/`，然后在 `openspec/config.yaml` 里设 `schema: <schema-name>`（或命令行 `--schema <schema-name>`）。

---

## 1. 默认内置 schema

| 目录 | 来源 |
|------|------|
| `spec-driven/` | OpenSpec 包内置（`@fission-ai/openspec/schemas/spec-driven`），从 `参考/OpenSpec/schemas/` 复制 |

**artifact 流**：`proposal` → `specs` → `design` → `tasks` → apply

- `proposal.md`：为什么改（Why / What Changes / Capabilities / Impact）
- `specs/**/*.md`：delta 规范（ADDED / MODIFIED / REMOVED / RENAMED Requirements + Scenario）
- `design.md`：技术方案（Context / Goals / Decisions / Risks / Migration / Open Questions，满足条件时才生成）
- `tasks.md`：`- [ ]` 复选框实现清单，apply 阶段解析进度
- `apply` 配置：`requires: [tasks]`、`tracks: tasks.md`

依赖关系：`specs` requires `proposal`；`design` requires `proposal`；`tasks` requires `specs + design`。

详细字段解读见 `docs/openspec-使用指南.md` 第 8 节。

## 2. intent-driven-dev 系列（5 个）

来源仓库：<https://github.com/intent-driven-dev/openspec-schemas>（`openspec/schemas/` 下）

| 目录 | 说明 | artifact 流 |
|------|------|-------------|
| `intent-driven/` | 捕获变更意图、可观测行为、技术设计与长期架构决策；变更内 ADR 评审清单，合格决策固化为可被取代的 ADR | proposal → specs → design → adr → tasks |
| `behaviour-driven/` | 行为驱动（BDD）变体，specs 采用 Gherkin 风格 | proposal → specs → design → tasks |
| `spec-driven-with-adr/` | 默认流程 + ADR 环节，ADR 持久化到 `<repo>/adr/` | proposal → specs → design → adr → tasks |
| `event-driven/` | 事件驱动工作流：从事件发现到 AsyncAPI 优先的实现规划 | proposal → event-storming → event-modeling → specs → design(asyncapi.yaml) → tasks |
| `minimalist/` | 极简 schema，适合范围明确、低风险的变更 | specs → tasks |

## 3. 其他社区 schema（4 个）

| 目录 | 来源仓库 | 说明 |
|------|---------|------|
| `superpowers-bridge/` | <https://github.com/JiangWay/openspec-schemas>（`superpowers-bridge/`） | 桥接 obra/superpowers 执行技能（头脑风暴、写计划、子代理 TDD、代码评审、收尾），增加证据优先的 `retrospective` 回顾 artifact |
| `anvil/` | <https://github.com/jikkujoyce/openspec-schemas>（`schemas/anvil/`） | 带 TDD 纪律与对抗式评审：proposal → specs → design → review → test-plan → tasks → apply → verify；`review` 由全新上下文的只读评审者撰写并给出 `VERDICT:` 门禁 |
| `nanopm/` | <https://github.com/nmrtn/nanopm>（`openspec-schema/`） | PM 优先工作流：先跑 nanopm 规划流水线（audit → strategy → roadmap → PRD），再衔接 spec-driven 工程；若存在 `.nanopm/` 则作为 artifact 输入源 |
| `e2e-runbooks/` | <https://github.com/Lukk17/openspec-schemas>（`openspec/schemas/e2e-runbooks/`） | 能力级端到端测试 runbook：断言只用可观测行为（HTTP 状态、响应体、落库状态），每次执行生成一条带 UTC 时间与 token 消耗的时间戳记录 |

> 官方社区 schema 目录页：OpenSpec 文档 `docs/customization.md` 的 Community Schemas 一节（见 `参考/OpenSpec/docs/customization.md`）。

## 4. 本项目自研 schema（1 个）

| 目录 | 说明 | artifact 流 |
|------|------|-------------|
| `evidence-driven/` | **本项目原创**，综合对比上述 10 个 schema 后设计：流程深度由 **P0–P3 风险分级**驱动，策略外置于 `flow-policy.yaml`，开发者可改判级标准与各级环节强度而无需 fork schema | P0/P1：proposal → specs → design → review → test-plan → tasks → verify；P2：proposal → design → tasks；P3：零 artifact 直改 |

核心设计：P0/P1 走全流程（跨模型对抗评审 / 新上下文评审、强制 TDD、强制 ADR 蒸馏），
P2 与默认 `spec-driven` 完全同构（零迁移成本），P3 连流程都不启动（零摩擦，
agent 直接改代码并自行验证）。它补的是**所有社区 schema 的共同盲区——风险分级**：
`anvil` 的重流程对高风险恰到好处但对改文案是纯摩擦（团队最后会绕过流程），
`minimalist` 则砍掉了大改动需要的 Why/How 载体。

配套 `validate_schema.py`（本目录根部）交叉校验 `flow-policy.yaml` 与 schema 静态
依赖图的一致性（如 `tdd: mandatory` 却缺 `test-plan`、flow 启用 `review` 却缺
`design` 前置等矛盾配置直接报错）。改完策略跑一次：

```bash
cd schemas-zh && python3 validate_schema.py
```

完整设计说明与决策理由见 `evidence-driven/README.md`。

---

## 汇总对照表

| schema | artifact 数 | 适合场景 |
|--------|------------|---------|
| `spec-driven` | 4 | 默认通用 |
| `minimalist` | 2 | 小改动、低风险 |
| `behaviour-driven` | 4 | BDD / Gherkin 团队 |
| `intent-driven` | 5 | 强调意图与架构决策留存 |
| `spec-driven-with-adr` | 5 | 默认流程 + ADR 归档 |
| `event-driven` | 6 | 事件溯源 / 消息驱动系统 |
| `nanopm` | 4 | 产品规划先行 |
| `anvil` | 7 | TDD + 独立评审门禁 |
| `superpowers-bridge` | 8 | 深度集成 superpowers 技能集 |
| `e2e-runbooks` | 4 | 端到端测试运维手册 |
| **`evidence-driven`** | **7（按 P0–P3 分级缩放）** | **任意风险级别的通用流程（本项目自研）** |