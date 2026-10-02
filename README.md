# agent-flow

面向 [OpenSpec](https://github.com/Fission-AI/OpenSpec) 的 schema 集合与工作流设计。

收录 OpenSpec 默认 schema、10 个社区 schema，以及本项目自研的 **`evidence-driven`**——
一个按**需求复杂度与变更风险**缩放流程长度的通用工作流。全部 schema 的指令与模板均为中文。

---

## 快速开始

```bash
# 1. 校验共享定义，生成三个可独立安装的档位（需要 Python 3 + PyYAML）
python3 schemas/validate_schema.py
python3 schemas/evidence-driven/build_profiles.py --output <项目>/openspec/schemas

# 2. 严格默认档（<项目>/openspec/config.yaml）；创建前先判级
#    schema: evidence-driven

# 3. 按复杂度/风险选择；P3 不创建 change
openspec new change routine-feature --schema evidence-driven-p2
openspec new change complex-feature --schema evidence-driven-p1
openspec new change sensitive-feature --schema evidence-driven

# 4. 定制共享策略后重新生成（可选；不要只改已安装的策略副本）
# vim schemas/evidence-driven/flow-policy.yaml
# python3 schemas/evidence-driven/build_profiles.py --output <项目>/openspec/schemas --force
```

---

## Schema 一览

| schema | artifact 数 | 适合场景 |
|--------|------------|---------|
| `spec-driven` | 4 | OpenSpec 默认内置，通用基线 |
| `minimalist` | 2 | 小改动、低风险 |
| `behaviour-driven` | 4 | BDD / Gherkin 团队 |
| `intent-driven` | 5 | 强调意图与架构决策留存 |
| `spec-driven-with-adr` | 5 | 默认流程 + ADR 归档 |
| `event-driven` | 6 | 事件溯源 / 消息驱动系统 |
| `nanopm` | 4 | 产品规划先行 |
| `anvil` | 7 | TDD + 独立评审门禁 |
| `superpowers-bridge` | 8 | 深度集成 superpowers 技能集 |
| `e2e-runbooks` | 4 | 端到端测试运维手册 |
| **`evidence-driven` 系列** | **P0/P1/P2 为 7/5/4；P3 为 0** | **按需求复杂度与风险选择流程（本项目自研）** |

每个 schema 的详细说明与来源见 [`schemas/README.md`](schemas/README.md)。

---

## evidence-driven

现有 11 个 schema 有个共同盲区：**没有一个做风险分级**。

- `anvil` 的重流程对高风险变更恰到好处，但改一行 CSS 也要跨模型评审 + 测试台账 +
  TDD 三段式——团队最终会绕过流程，流程名存实亡。
- `minimalist` 走了另一个极端，把大改动需要的 Why/How 载体也砍掉了。
- 现实中同一团队同时有 P0（资金、安全）和 P3（文案）级别的变更，一刀切注定两头不讨好。

`evidence-driven` 的设计是：**复杂度与风险取更严格档，保留默认主干，按需增加护栏**。

| 级别 | 判据 | 流程 | 评审 | TDD | ADR |
|------|------|------|------|-----|-----|
| **P0** 高风险 | 安全/资金/敏感数据；BREAKING；不可逆迁移或重大故障影响 | 主干 + review/test-plan/verify | 独立对抗，可选跨模型 | 变更行为强制 | 有长期决策才做 |
| **P1** 复杂需求 | 跨模块协作、显著取舍、不确定性、核心路径或验证难点 | 主干 + review | 独立新上下文 | 可选 | 有长期决策才做 |
| **P2** 常规需求 | 边界清晰、方案成熟、可测试，不触及更高档判据 | 默认主干 | 无 | 可选 | 有长期决策才做 |
| **P3** 琐碎 | 不改变行为契约的文案/注释/纯展示或配置微调 | 直改 + 验证 | 无 | 无 | 无 |

- **P0/P1** 都在 design 后、tasks 前统一对抗评审；只有 P0 额外生成覆盖台账与正式验证报告。
- **P2** 保留 proposal → specs → design → tasks 的主干，任务自带验收方式。
- **所有档位都验证**；P1/P2 收尾证据留在 tasks，ADR 不作为固定阶段。
- **P3** 不创建 change；单文件、有测试不是零流程的充分理由，也不为流程强制 commit。

分别判断复杂度与风险，`rules.on_doubt: escalate`——存疑就往严的一级靠。

### 策略外置

`flow-policy.yaml` 管判级、档名、环节与强度，`schema.yaml` 管共享定义与依赖。
生成器从同一套模板生成 `evidence-driven`（P0）、`evidence-driven-p1`、
`evidence-driven-p2` 三个真实静态图。修改策略后必须重新生成，不靠指令跳过 CLI 依赖。

改完跑一次一致性校验：

```bash
python3 schemas/validate_schema.py
python3 schemas/validate_schema.py --installed <项目>/openspec/schemas
```

它从实际 `requires` 校验依赖顺序、模式与 flow 一致性、模板和依赖环；可额外
检查已安装图/策略/模板是否与共享源码一致。裁决、快照与测试证据仍需 agent/CI 检查。

完整设计说明、对比分析与决策理由见
[`schemas/evidence-driven/README.md`](schemas/evidence-driven/README.md)。

---

## 目录结构

```
agent-flow/
├── README.md
├── docs/
│   └── openspec-使用指南.md      # OpenSpec 中文使用文档（安装 / 命令 / config / schema 体系）
└── schemas/
    ├── README.md                 # schema 汇总与对照表
    ├── validate_schema.py        # 结构 + flow-policy 一致性校验器
    ├── spec-driven/              # OpenSpec 默认内置
    ├── minimalist/ behaviour-driven/ intent-driven/
    ├── spec-driven-with-adr/ event-driven/ nanopm/
    ├── anvil/ superpowers-bridge/ e2e-runbooks/
    └── evidence-driven/          # 本项目自研
        ├── schema.yaml           # 共享定义 + P0 完整图（7 artifact + apply）
        ├── flow-policy.yaml      # 判级、档名、环节与强度
        ├── build_profiles.py     # 生成 P0/P1/P2 安装包
        └── templates/            # 各 artifact 的中文模板
```

每个 schema 包结构统一：`schema.yaml`（工作流定义）+ `templates/`（模板）+ `README.md`。
`evidence-driven/` 额外含 `flow-policy.yaml` 与 `build_profiles.py`。

---

## 使用 schema 包

把子目录复制到目标项目的 `openspec/schemas/<name>/`，然后在 `openspec/config.yaml`
里设 `schema: <name>`，或命令行 `--schema <name>`。`evidence-driven` 系列建议用
上述生成器安装三个档位；直接复制共享目录只得到 P0。名称解析顺序见使用指南第 8 节。

---

## 文档

- [OpenSpec 开发使用文档](docs/openspec-使用指南.md) — 安装、`/opsx` 命令、config.yaml
  可配置项、schema 体系、CLI 参考、常见问题
- [Schema 汇总](schemas/README.md) — 各 schema 的 artifact 流与来源
- [evidence-driven 设计说明](schemas/evidence-driven/README.md) — 四档流程、评审、ADR、
  证据规则、生成安装与现有 change 升级迁移

---

## 来源

社区 schema 来自 [intent-driven-dev/openspec-schemas](https://github.com/intent-driven-dev/openspec-schemas)、
[jikkujoyce/openspec-schemas](https://github.com/jikkujoyce/openspec-schemas)、
[JiangWay/openspec-schemas](https://github.com/JiangWay/openspec-schemas)、
[Lukk17/openspec-schemas](https://github.com/Lukk17/openspec-schemas)、[nmrtn/nanopm](https://github.com/nmrtn/nanopm)，
版权归各自作者，本项目仅做中文整理与收录。
