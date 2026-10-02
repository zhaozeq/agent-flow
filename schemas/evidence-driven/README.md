# evidence-driven：默认主干，按需增加护栏

以 `spec-driven` 为基线，分别评估**需求复杂度**与**变更风险**，取更严格的一档。
常规需求保持短流程，复杂需求在形成 tasks 前挑战完整方案，高风险需求再增加
覆盖台账与正式验证报告。所有档位都要验证；ADR 只为长期决策生成，不凑文件。

## 1. 四档流程

| Tier | 定位 | artifact 流程 | schema |
|------|------|---------------|--------|
| P0 | 高风险 | proposal → specs → design → review → test-plan → tasks → **apply** → verify | `evidence-driven` |
| P1 | 复杂需求 | proposal → specs → design → review → tasks → **apply + 验证** | `evidence-driven-p1` |
| P2 | 常规需求 | proposal → specs → design → tasks → **apply + 验证** | `evidence-driven-p2` |
| P3 | 琐碎修改 | **直接修改 + 相关验证**，不创建 change | 无 |

apply 是实施阶段，不是 artifact，因此 P0/P1/P2 分别有 **7/5/4 个 artifact**。

- **复杂度**：需求不确定性、跨模块协作、方案选择与验证难度。复杂但低风险的
  功能通常是 P1，需要独立规划评审，不必生成完整交付审计文档。
- **风险**：安全、数据、兼容性、故障影响与恢复能力。即使修改很小，权限或
  数据删除行为也可能是 P0。涉及文件数量不再直接决定最高风险档。
- **P3**：只允许不改变行为契约或交互语义的琐碎修改。单文件、有测试的小修复
  并非充分判据；有行为变化至少 P2，触及高风险判据则升级。
- **不确定就升级**。创建 change 前判级，proposal 记录两个维度的依据，Tier
  与实际 schema 一致。不能仅改 Tier 文本来跳过环节。

具体判据与强度以共享源码 `flow-policy.yaml` 为准。

## 2. 一份共享定义，三个真实依赖图

OpenSpec 的 `requires` 是静态依赖，不能让同一 artifact 在 P2 跳过 review，
又在 P1/P0 把 review 作为 tasks 的强制前置。用文字说「本级别跳过」也不会
改变 CLI 的 ready/blocked 状态、下一步推荐或 artifact 完成统计。

因此只维护一份共享定义与模板，通过 `build_profiles.py` 生成三个可独立安装的
schema 包。生成时保留本档启用的 artifact，并从共享 `requires` 中保留本档的
真实依赖；不通过空文件或 N/A artifact 假装完成被跳过的阶段。

关键依赖：

| 环节 | 前置 |
|------|------|
| specs | proposal |
| design | proposal、specs |
| review（P0/P1） | proposal、specs、design |
| test-plan（P0） | specs、review |
| tasks（P0） | specs、design、review、test-plan |
| tasks（P1） | specs、design、review |
| tasks（P2） | specs、design |
| verify（P0） | tasks；内容指令另要求 apply 已完成 |

所以 P0/P1 在 design 后只有 review 就绪，tasks 尚未就绪。P2 的图中根本没有
review/test-plan/verify，不会卡在不需要的文件上。主干 artifact 与默认流程一致，
但这里刻意让 design 等待 specs，以便先定行为契约再形成方案。

本仓库共享目录的 `schema.yaml` 同时是共享定义和可直接安装的 **P0 完整档**，保留现有名称
`evidence-driven`。不能只复制它再写 `Tier: P2` 来获取轻流程。

## 3. design 后的一次规划评审

先形成 proposal、specs、design，再独立审查三者的一致性和可实施性，批准后
才写 tasks。没有 S1/S2/S3 分阶段评审，也不单独增加 brainstorm、ADR 阶段。

评审覆盖问题真实性、范围/定级、更便宜的替代方案、未言明假设、失败/边界、
安全信任边界、可测试性及迁移/恢复能力。design 的 **Validation Strategy**
先说明关键行为怎么验证，不必在评审前展开完整台账。

- P1：独立新上下文评审；P0：保留同样独立性，加强安全、数据与故障攻击面。
- 跨模型是可选增强，只使用获准处理仓库数据的服务；工具不可用时不静默
  降成作者自查，必要时请人类评审。
- 记录输入文件集合与 SHA-256，评审期间冻结输入。裁决后变更必须复核并
  更新快照；需求/关键设计变化重审受影响部分，影响不清则完整重审。
- `VERDICT: APPROVE`，或 `APPROVE_WITH_CHANGES` 且 `CHANGES_APPLIED: yes` 才能
  进入下游；后者必须由独立评审者复核全部必改项后确认。
- 未关闭的 Critical/Moderate 是阻断项。连续两轮 REVISE 后上报人类。

**这是规划门禁，不替代实施后的代码 review。** CLI 只识别文件存在，裁决与
快照门禁需要 agent 或 CI 检查。仅 grep 一行 APPROVE 不能验证评审有效性。

## 4. 验证与证据按档缩放

- **P2**：每个任务附验收方式，最终证据放在 tasks 的 Completion Evidence。
- **P1**：tasks 内联场景→具名测试/机械检查映射，不另建 test-plan/verify。
- **P0**：独立 test-plan 活台账，apply 后的 verify 从 specs 反向核对覆盖集合，
  检查真实运行、评审快照、ADR、交付状态与遗留问题。

所有档位都运行相关回归/机械检查，记录确切命令、退出码与结果，不把“不生成
verify”理解成“不验证”。P0 的正式报告还记录环境、工作树状态与必要日志。

TDD 不一刀切：P0 的新增/变更可执行行为必须 red→green；未变化场景复用并
重跑 baseline；非可执行项运行对应机械校验，不造无意义失败。计划尚未运行
标 pending，不能把计划写成运行证据。P1/P2 可选测试优先，但行为变化仍须测试。

既有跳过测试记录基线与理由；本次新增的无理由 skip、覆盖遗漏、失败验证、
过期裁决都不能包装成 PASS_WITH_WARNINGS。不为流程强制 commit。

## 5. ADR 的生命周期

```text
design 标记长期决策候选
        ↓
review 批准（P0/P1）或方案确认（P2）
        ↓
tasks 安排固化仓库级 ADR
        ↓
实现发生实质偏离时更新或取代 ADR
```

架构边界、数据模型、协议、关键技术选型适合 ADR；短期实现细节留在 design。
先遵循仓库现有目录/编号约定，无约定用 `adr/NNNN-<slug>.md`，包含 Status、
Context、Decision、Consequences。只在方案确认后 accepted；被取代的记录
标 superseded，不覆写历史。没有长期决策就说明不适用。

固化后登记 design 的 ADR 对应；有 review 的档位需复核登记并刷新快照。
强制的是长期决策不遗漏，不是每个 change 都要生成 ADR。

## 6. 安装与使用

在本仓库执行，需要 Python 3 与 PyYAML（缺失时 `python3 -m pip install PyYAML`）：

```bash
python3 schemas/validate_schema.py
python3 schemas/evidence-driven/build_profiles.py \
  --output <项目>/openspec/schemas
python3 schemas/validate_schema.py --installed <项目>/openspec/schemas
```

三个输出目录各自包含完整 schema、所需模板、策略快照与本文档，不依赖相邻
schema 的模板路径。生成包不包含源码构建工具，修改应在本仓库共享源码完成。

在目标项目先判级，再选择 schema：

```bash
openspec new change routine-feature --schema evidence-driven-p2
openspec new change complex-feature --schema evidence-driven-p1
openspec new change sensitive-feature --schema evidence-driven
```

不确定档位时不要默认绕过评审；先澄清或选择更严格档。P3 不调用 new change。
项目 `config.yaml` 可保持严格的 `schema: evidence-driven`；已判级的 P1/P2 用
`--schema` 指定。路由是创建 change 前的 agent/人工判断，不宣称 CLI 自动判级。

定制判据、模式或已有环节组合后，先校验再重新生成安装：

```bash
python3 schemas/validate_schema.py
python3 schemas/evidence-driven/build_profiles.py \
  --output <项目>/openspec/schemas --force
python3 schemas/validate_schema.py --installed <项目>/openspec/schemas
```

`--force` 更新生成文件，不删除其他文件。生成器禁止覆盖本仓库共享源码目录。
环节配置必须与模式一致且符合真实依赖顺序；P0 保留完整定义，P1/P2 可按团队
需要增加已有护栏。新增 artifact 或改变依赖关系要修改共享 schema，而非只改
策略。**修改已安装策略副本不会改变 CLI 依赖图，必须重新生成。**

## 7. 实施中升级与现有 change 迁移

1. 停止相关实施，在 proposal 记录原/新档位和理由。
2. 将当前 change 的 `.openspec.yaml` 中 `schema` 改为新档名称，保留其他元数据；
   只在命令行用 `--schema` 临时覆盖不会持久化档位。
3. 同步 proposal/tasks Tier，重新核对 specs/design，重开受影响的已完成任务。
4. P2→P1 补独立 review；P1→P0 补 test-plan，并把已有实现如实记录为 baseline，
   不编造历史 red。既有 review 若内容/档位变化须重审。
5. 检查 `openspec status --change <name> --json`，补齐门禁再继续；不在收尾时补写
   文档假装流程曾经执行。实施中不自动降级，需要人类确认才能减少护栏。

旧版所有档位都用 `evidence-driven`；更新后此名称固定为 P0。旧 P1/P2 change
需要显式切换元数据，再按新档图检查；不要仅因现有文件存在就认为裁决有效。

## 8. 源码结构

```text
schemas/
├── validate_schema.py
└── evidence-driven/
    ├── README.md
    ├── schema.yaml         # 共享定义 + P0 完整图
    ├── flow-policy.yaml    # 判级、档名、flow 与模式
    ├── build_profiles.py  # 生成 P0/P1/P2 安装包
    └── templates/         # 只维护一套中文模板
```

借鉴默认 spec-driven 的主干、anvil 的独立评审与覆盖台账、intent-driven 的
长期决策留存、superpowers-bridge 的证据优先收尾，但不绑定外部技能或执行环境。
