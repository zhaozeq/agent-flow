# evidence-driven 工作流

> 综合对比 OpenSpec 默认 schema 与 9 个社区 schema、结合业界最佳实践后总结的工作流设计。
> 目录：`schemas-zh/evidence-driven/`，可直接复制到目标项目的 `openspec/schemas/evidence-driven/` 使用。

## 快速概览

```
流程深度由风险分级决定，分级策略外置于 flow-policy.yaml（开发者可自行定制）：

P0 高风险  proposal → specs → design → review → test-plan → tasks → verify
           （跨模型对抗评审 · 强制 TDD · 强制 ADR · 回滚方案）
P1 中风险  proposal → specs → design → review → test-plan → tasks → verify
           （新上下文评审 · 强制 TDD · 强制 ADR）
P2 低风险  proposal → design → tasks
           （对齐默认 spec-driven 的轻流程：无规范 delta、无评审、无台账）
P3 琐碎    零 openspec 记录
           （agent 直接改代码并自行验证，git 提交信息即追溯）
```

**定制入口**：`evidence-driven/flow-policy.yaml` 是流程策略的单一事实源——改判级标准、
各级流程、评审强度、TDD/ADR/verify 深度都只改这一个文件，无需动 schema.yaml。改完跑
`python3 validate_schema.py` 校验一致性。

## 一、对比分析：现有 schema 各自解决什么问题

先说结论：**每个社区 schema 都是对默认流程某一种失败模式的补丁**。逐一分析它们补的洞，以及各自引入的新成本。

### 1.1 各 schema 一览

| schema | 核心机制 | 解决的痛点 | 引入的成本/问题 |
|--------|---------|-----------|----------------|
| **spec-driven**（默认） | proposal → specs → design → tasks 四件套 | 需求只活在聊天记录里，AI 凭空写代码 | 无任何质量门禁；design 无条件生成（小改动也要写）；决策随 change 归档沉没 |
| **minimalist** | 砍到 specs → tasks 两件 | 小改动被四件套拖累 | 大改动没有 Why 和 How 的承载位置 |
| **anvil** | 对抗式 review 门禁 + test-plan 覆盖台账 + TDD 排序 | AI 自评自己写的计划；场景没有测试兜底 | **一刀切**：改个文案也要跨模型评审；8 个 artifact 全员重流程 |
| **intent-driven / spec-driven-with-adr** | ADR 蒸馏到 `<repo>/adr/` | 长期架构决策随 change 归档而沉没，团队记忆流失 | ADR 阈值无标准，容易把短命实现细节也写成 ADR |
| **behaviour-driven** | specs 用 Gherkin 风格 | 需求表述不可测 | 与 OpenSpec 原生 delta 格式（#### Scenario）耦合度低 |
| **event-driven** | 事件风暴 → 事件建模 → AsyncAPI | 消息系统先于契约建模就开工 | 非事件驱动系统完全用不上 |
| **nanopm** | PM 规划流水线前置 | 产品规划与工程规范脱节 | 依赖外部 nanopm 工具与 `.nanopm/` 目录 |
| **superpowers-bridge** | brainstorm → … → retrospective；git worktree + 子代理执行 | 缺少事后复盘；执行环境不隔离 | 重度依赖 superpowers 插件生态，不可移植 |
| **e2e-runbooks** | 能力级 runbook + 时间戳执行记录 | e2e 断言不基于可观测行为 | 只覆盖测试运维这一垂直场景 |

### 1.2 值得吸收的最佳实践（跨 schema 提炼）

1. **对抗式评审**（anvil）：计划不能由撰写它的上下文自评。anvil 的三选一裁决（APPROVE / APPROVE_WITH_CHANGES / REVISE）、机器可读 `VERDICT:` 行、裁决失效规则（被评审内容一变裁决作废）、连续 2 轮 REVISE 上报人类——这四件设计非常扎实，照单吸收。
2. **覆盖台账**（anvil test-plan）：specs 场景 1:1 映射具名测试，apply 期间红→绿翻转，verify 审计全绿。它把「需求→测试」的追溯从口头承诺变成可审计的表格。
3. **TDD 排序**（anvil）：红-绿-重构三段式写进任务清单，禁止「写测试+写实现」合并为一个任务。
4. **ADR 蒸馏**（intent-driven / spec-driven-with-adr）：长期决策的寿命必须长于 change——归档时 change 进了 `changes/archive/`，但决策应该活在 `adr/` 被后续所有变更看到。
5. **非可执行变更的出口**（anvil）：文档/配置类变更映射到等价机械校验（linter、schema validate），而不是被迫编造代码测试——避免了「为了过流程而造假测试」。
6. **事后复盘**（superpowers-bridge retrospective）：把计划偏差与被推翻的假设记录下来，供下一次变更参考。
7. **失败场景强制**（anvil）：每个需求至少 1 个快乐路径 + 1 个失败/边界场景。AI 写 spec 时几乎只写快乐路径，这是对 AI 行为弱点的精准补丁。

### 1.3 现有 schema 的共同盲区

**没有任何一个 schema 做「风险分级」。** 这是最大的发现：

- anvil 的重流程对高风险变更恰到好处，但对低风险变更（文案、样式、小 bug fix）是纯摩擦——改一行 CSS 也要跨模型评审 + 测试台账 + TDD 三段式，团队最后的结局往往是绕过流程（「这个改动太简单了直接改吧」），流程一旦被绕过就名存实亡。
- minimalist 走了另一个极端，把大改动需要的 Why/How 载体也砍掉了。
- 现实中同一团队同时有 P0（资金、安全）和 P2（文案）级别的变更，一刀切流程注定两头不讨好。

另一个盲区：**spec-driven 的 design.md 无条件生成**。写个文案变更也要填 Context/Goals/Decisions/Risks 模板，产出的只能是空洞的模板填空——这比不写更糟，因为它训练团队无视文档。

## 二、evidence-driven 的设计

```
proposal ──► specs ──► design ──► review ──► test-plan ──► tasks ──► apply ──► verify
 (含风险定级)  (失败场景)  (按级缩放)  (对抗式门禁)  (覆盖台账)  (TDD排序)  (红绿翻转)  (证据审计)
```

7 个 artifact + apply 配置，全部指令与模板均为中文（delta 操作关键字、`#### Scenario:` 等 CLI 依赖的格式标记保持英文原文）。

### 2.1 核心设计决策与理由

#### 决策 1：风险分级（P0–P3）作为流程深度的总开关，策略外置可定制

风险定级与各级流程不在 schema.yaml 里写死，而是放在同目录 **flow-policy.yaml**
（安装后为 `openspec/schemas/evidence-driven/flow-policy.yaml`），开发者可直接
改文件定制——调整判级标准、增删某级别的环节、改评审强度，都不需要 fork schema：

| 级别 | 判据（满足任一） | flow | 评审 | TDD | ADR | verify |
|------|----------------|------|------|-----|-----|--------|
| **P0** | 安全/认证/授权/资金/数据删除；BREAKING；跨 3+ 模块；无回滚数据迁移 | 全流程 | 跨模型对抗 | 强制 | 强制 | full |
| **P1** | 新外部依赖；公开 API 行为变化；核心路径修改；性能敏感区 | 全流程 | 新上下文 | 强制 | 强制 | full |
| **P2** | 有行为变化、可测试的常规改动，不触及 P0/P1 判据 | proposal → design → tasks | 无 | 可选 | 可选 | 无 |
| **P3** | 文案/注释/样式；不改变行为的配置微调；单文件小修复 | 零 artifact（直改） | 无 | 无 | 无 | 无 |

**P2 的定位**：与 OpenSpec 默认 spec-driven 完全同构——proposal（为什么）→
design（怎么做）→ tasks（清单）→ apply，不写规范 delta、不评审、不建测试
台账。这是有意为之：P2 是「默认 OpenSpec 体验」的等价物，让习惯 spec-driven
的团队零成本迁移；行为质量由 tasks 的验收方式兜底（每个任务自带测试/命令/
可观测行为）。需要规范契约或评审时，那就是 P1 的信号。

**P3 的实现机制**（agent 足够聪明，琐碎变更连流程都不该启动）：
- **零 openspec artifact**：不创建 change 目录、不写任何 markdown。agent
  直接实现改动并自行验证（跑相关测试/lint/构建），git 提交信息是唯一
  追溯记录。判据是「不需要留痕」而非「流程走得快」——若需要规范级
  留痕（行为契约变化、需要评审），它就不是 P3。
- schema 层面无法阻止直改，因此这个约定写在 schema 头部机制说明、
  proposal 定级指令与 apply 指令三处：P3 分支明确「直接实现并自行验证，
  宁可中途升级定级，不可事后补文档」。
- OpenSpec 的 `requires` 是 schema 级静态依赖图，不能按 change 变化。
  因此 schema.yaml 的静态依赖压到**存在性下限**，P2 的 flow（不含
  specs/review）不会被 CLI 阻塞；design/review 等重环节保留存在性依赖，
  启用它们的级别（P0/P1）顺序依然受 CLI 保护——**静态图是下限，
  flow-policy 决定实际走多远**。
- 各 artifact 指令里的门禁均写成条件式（「仅当本级别 flow 含 review 时」），
  flow-policy 缺失时按指令内兜底判级执行。

**理由**：这直接回应 1.3 的盲区。设计目标是「高风险变更的严谨度不输 anvil，
P2 等价于默认 spec-driven 体验（零迁移成本），P3 连流程都不启动（零摩擦），
且策略归开发者所有」。关键细节：

- 定级标准写得**可判定**（「涉及资金」「跨 3 个以上模块」），而不是「重大
  变更」这种靠感觉的表述——AI 执行需要明确的判据。
- **存疑就高不就低**（flow-policy `rules.on_doubt: escalate`）：定级是 AI
  做的判断，宁可误判为高而多走流程，不可误判为低而漏走门禁。
- **定级可修订**（`rules.revision: append-note`）：实施中发现风险升级，在
  proposal 追加修订记录（模板含 Tier Revisions 小节）并同步下游——不是把
  定级焊死在起点。

#### 决策 1b：为什么策略外置成单独文件

schema.yaml 会被 `openspec update` 重新生成/覆盖的场景不存在（schema 是用户
资产），但 schema.yaml 承担的是**流程骨架**（artifact 图、模板映射、CLI 解析
所需的静态依赖），而「哪一级走哪些环节、强度多少」是**团队偏好**——两者变更
频率和责任方都不同。外置后：

- 定制策略不用碰 346 行的 schema.yaml（改错一处指令就可能破坏门禁语义）；
- flow-policy.yaml 结构简单（四级各十几行），评审定制 diff 一目了然；
- `validate_schema.py` 会交叉校验策略与静态依赖图的一致性（如 flow 启用
  review 但缺 design 前置、tdd=mandatory 但无 test-plan 等矛盾配置直接报错）。

#### 决策 2：design.md 深度由 flow-policy 决定（skip / brief / full）

design_depth 三档：P3 skip（不生成）、P2 brief（一段话+触碰文件清单）、
P1 full（完整小节）、P0 full（完整小节 + Decisions 必附备选 + Migration 必含回滚）。

**理由**：spec-driven 的「条件生成」判据与 P0/P1 分级高度重合，但 AI 对判据
的判断不稳定，同类改动有时写有时不写。用统一的 Risk Tier 驱动深度（而不是
有/无），判据只有一处（proposal 定级），AI 执行一致性更高，也不产生「该写
没写」的灰色地带。P3 连一段话都不要求——琐碎变更的 design 只会是模板填空。

#### 决策 3：review 强度四级（none / self / fresh-context / cross-model），门禁语义不变

review_mode 四档：P3 none（不生成）、P2 self（当前上下文自查）、P1
fresh-context（全新上下文子代理，不携带撰写记忆）、P0 cross-model（跨模型
对抗评审，附数据边界条款——artifact 可能发往外部服务，须团队已批准；含
机密且无获准模型时退回 fresh-context）。

同时保留 anvil 的全部裁决机制：`VERDICT:`/`CHANGES_APPLIED:` 机器可读行、
裁决失效规则、连续 2 轮 REVISE 上报、申诉须经评审者复核。

**理由**：评审的价值来自「独立性」，独立性的成本来自「上下文切换」。风险分级
正好是衡量「值得付多少独立性成本」的标尺。anvil 的失败处理条款（「不得静默
降级为自查、不得编造裁决」）原样保留——**缩放的是强度，不是诚实度**。

#### 决策 4：test-plan 覆盖台账（所有含 test-plan 的级别保留）

specs 每个场景 1:1 映射具名测试；非可执行变更加入 N/A 出口（映射到机械
校验）。apply 期间红→绿翻转，verify 审计全绿。tdd=mandatory 的级别
（P0/P1）必须包含 test-plan——覆盖台账是 TDD 的载体（校验脚本强制这一点）。

**理由**：不按风险缩放这一个 artifact，因为覆盖台账的成本是 O(场景数) 的、
与风险无关——P2 变更场景本来就少，台账自然短。而「需求→测试」追溯对所有
级别都有价值（文案变更可以映射到「markdownlint 通过」）。anvil 的「映射是
下限不是上限」条款也保留：额外测试永远欢迎、无需登记、不可替代。P3 的
flow 不含 test-plan（琐碎变更验收方式直接写在任务描述里），主干上 specs →
tasks 不经台账。

#### 决策 5：TDD 排序由 flow-policy 的 tdd 档位决定（mandatory / optional / none）

- mandatory（P0/P1）：每组任务强制三段式「写失败测试（确认以正确原因失败）→ 最小实现 → 重构保持绿色」，禁止合并
- optional（P2）：按依赖自然排序；已有测试的改动先跑一遍确认起点
- none（P3）：任务自带验收方式即可，无排序要求

**理由**：TDD 的收益（防止「写了实现再补测试」的自欺）在高风险变更上最大；对纯文案/文档类 P3 变更强制三段式只能逼出假测试。P2 保留「先跑既有测试确认起点」这一最小纪律，成本一行命令。

#### 决策 6：ADR 蒸馏内置为 design 的收尾动作（mandatory / optional / no）

design 的 Decisions 表格中标注哪些是「长期决策」（寿命超过本次变更：架构选型、数据模型、协议约定），adr=mandatory 的级别必须为每条蒸馏 ADR 到 `<repo>/adr/NNNN-<slug>.md`，并在 design 中登记编号；verify 审计「标注的长期决策均已写入 adr/ 且编号一致」。短命的实现细节明确禁止写成 ADR。

**理由**：吸收 intent-driven 的核心洞察（决策寿命 > change 寿命），但修复了它的 ADR 阈值模糊问题——用「寿命是否超过本次变更」这一判据 + 设计表格中的显式标注列，把蒸馏决策从「感觉这条重要」变成可审计的动作。verify 的决策蒸馏审计让它不会沦为口头承诺。

#### 决策 7：verify 吸收 retrospective，深度分档（none / minimal / full）

verify_depth 三档：P3 none（不生成，apply 跑通相关测试收尾）、P2 minimal
（任务完成度 + 交付状态 + Evidence + DECISION 行）、P0/P1 full（六项全查：
任务完成度、覆盖审计【阻断】、评审有效性、决策蒸馏、交付状态、经验教训）。
`DECISION:` 机器可读行。

**理由**：superpowers-bridge 的 retrospective 值得要，但单独成第 8 个
artifact 会让流程更长；它的内容天然属于收尾时刻，合入 verify 零成本。anvil
的「没有记录测试运行的 verify 不可能 PASS」是最硬核的条款——所有结论必须
挂证据，这正是 schema 名字 evidence-driven 的由来。「不强制 commit」同样
来自 anvil：很多团队要求人工评审后才提交，为过流程而强推 commit 是本末
倒置。

#### 决策 8：规范漂移条款（写进 apply 指令）

实现中发现需求错误时：停止该场景 → 修改 specs（连带 design）→ **重跑评审（原裁决作废）** → 更新 test-plan 与 tasks → 继续。明确禁止「为配合观测到的行为改测试断言却不改规范」。

**理由**：这是 anvil 最有价值的一条隐性经验。AI 实现时的最大诱惑就是「改断言让测试通过」——这条规则把「规范是唯一真相源」变成可执行的流程，而不是口号。重跑评审与裁决失效规则联动，堵住了漂移的后门。

### 2.2 明确不采纳的设计及理由

| 候选 | 不采纳理由 |
|------|-----------|
| Gherkin 风格 specs（behaviour-driven） | OpenSpec CLI 归档解析依赖原生 `#### Scenario:` 格式，Gherkin 会牺牲与 validate/archive 的兼容性 |
| brainstorm 前置 artifact（superpowers-bridge） | OpenSpec 已有 `/opsx:explore` 承担同样职责（读代码、权衡、打磨想法、零 artifact 产出），流程内再加一个重复 |
| 事件风暴/AsyncAPI（event-driven）、runbook（e2e-runbooks）、nanopm 流水线 | 垂直场景专用，通用 schema 不应捆绑 |
| git worktree 隔离执行（superpowers-bridge） | 属于执行环境约定而非工作流结构，且依赖外部技能；留给使用者自行叠加 |
| 把 retrospective 独立成 artifact | 见决策 7，合入 verify |

### 2.3 与机器强制的关系（诚实声明）

OpenSpec 的 `requires:` 只校验 artifact **文件存在**，不校验内容。本 schema 的风险分级、VERDICT/CHANGES_APPLIED/DECISION 门禁由遵循指令的 agent 执行，CLI 不做机械强制。需要机械强制时，在 CI 中 grep 这三个机器可读行即可（它们被设计为单行、格式固定、易于正则匹配）——这是 anvil「用 CI 补足 CLI 局限」思路的延续。

## 三、目录结构

```
schemas-zh/
├── validate_schema.py                 # 结构 + flow-policy 一致性校验
└── evidence-driven/
    ├── README.md                      # 本文档（设计说明与决策理由）
    ├── schema.yaml                    # 流程骨架（7 artifact + apply；静态依赖压到存在性下限）
    ├── flow-policy.yaml               # 流程策略单一事实源（P0-P3 分级、各环节深度，开发者可改）
    └── templates/
        ├── proposal.md                # 含 Risk Tier 与 Tier Revisions 小节
        ├── spec.md                    # delta 规范（ADDED/MODIFIED/REMOVED/RENAMED）
        ├── design.md                  # 按级缩放；Decisions 含 ADR 标注列
        ├── review.md                  # 对抗式评审 + VERDICT 机器可读行
        ├── test-plan.md               # 覆盖台账（含 N/A 出口）
        ├── tasks.md                   # 头部 Tier 行 + 复选框清单（TDD 三段式按级）
        └── verify.md                  # 证据审计 + 经验教训 + DECISION 行
```

## 四、使用方式

```bash
# 复制到目标项目
cp -r schemas-zh/evidence-driven <项目>/openspec/schemas/evidence-driven

# 设为默认 schema（openspec/config.yaml）
# schema: evidence-driven

# 或单次指定
openspec new change my-feature --schema evidence-driven

# 定制流程策略（判级标准、各级环节、评审强度等）——只改这一个文件
vim <项目>/openspec/schemas/evidence-driven/flow-policy.yaml

# 校验定制后的策略与 schema 依赖图是否一致（校验器位于 schemas-zh/ 下）
cd schemas-zh && python3 validate_schema.py
```

配合 `docs/openspec-使用指南.md` 第 6 节的 config.yaml 用法：`rules:` 可按
artifact ID（proposal/specs/design/review/test-plan/tasks）追加团队规则；
`context:` 注入技术栈让定级与 ADR 判断更准。
