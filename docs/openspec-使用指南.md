# OpenSpec 开发使用文档

> 本文档基于 `参考/OpenSpec` 源码（Fission-AI/OpenSpec，`@fission-ai/openspec`）整理，面向在本仓库中使用/借鉴 OpenSpec 的开发者。
> 文中所有配置项、默认行为均对照源码 `src/core/project-config.ts`、`src/core/config-schema.ts`、`src/core/global-config.ts`、`src/core/profiles.ts`、`src/core/artifact-graph/resolver.ts` 核实。

---

## 目录

1. [项目简介](#1-项目简介)
2. [核心概念](#2-核心概念)
3. [安装与初始化](#3-安装与初始化)
4. [目录结构](#4-目录结构)
5. [日常工作流（/opsx 命令）](#5-日常工作流opsx-命令)
6. [config.yaml 可配置项详解（重点）](#6-configyaml-可配置项详解重点)
7. [全局配置（~/.config/openspec/config.json）](#7-全局配置configopenspecconfigjson)
8. [Schema 体系与解析顺序](#8-schema-体系与解析顺序)
9. [CLI 命令参考](#9-cli-命令参考)
10. [环境变量](#10-环境变量)
11. [常见问题排查](#11-常见问题排查)

---

## 1. 项目简介

OpenSpec 是一个「规范驱动开发（Spec-Driven Development）」的轻量框架，定位在你与 AI 编码助手之间的**协议层**：在写任何代码之前，先和 AI 就"要构建什么"达成书面一致，然后才动手。

核心主张：

- **先约定，后构建** —— 人与 AI 先对齐规范，再写代码
- **流动而非僵化** —— artifact 顺序是"使能者"而非"关卡"，随时可回头修改
- **面向存量项目（brownfield）** —— 增量 delta 规范，不需要先给 5 万行代码补全文档
- **工具无关** —— 通过斜杠命令支持 30+ AI 助手（Claude Code、Cursor、Codex、Gemini CLI 等）

完整闭环（默认 core profile）：

```
/opsx:explore ──► /opsx:propose ──► /opsx:apply ──► /opsx:sync ──► /opsx:archive
   (可选：先想清楚)    (AI 起草计划)     (AI 按任务实现)   (可选：合并规范)   (归档收尾)
```

环境要求：**Node.js ≥ 20.19.0**。

---

## 2. 核心概念

| 概念 | 说明 |
|------|------|
| **specs/** | 真相之源。描述系统**当前**行为，按领域组织（`specs/auth/`、`specs/payments/`）。由 Requirement（`### Requirement: xxx`，使用 SHALL/MUST）和 Scenario（`#### Scenario: xxx`，WHEN/THEN）构成 |
| **change** | 一个工作单元。`openspec/changes/<change-name>/` 下一个文件夹装下该次变更的全部内容 |
| **delta specs** | 变更内的增量规范，只写"改了什么"：`## ADDED Requirements` / `## MODIFIED Requirements` / `## REMOVED Requirements` / `## RENAMED Requirements`。归档时合并回主规范 |
| **artifact** | 变更内的文档产物，按依赖链组织：`proposal`（为什么）→ `specs`（做什么）→ `design`（怎么做）→ `tasks`（步骤清单）。依赖是"使能"不是"门禁" |
| **schema** | 工作流定义（artifact 集合 + 依赖关系 + 模板 + AI 指令）。内置默认为 `spec-driven` |
| **archive** | 归档：delta 合并进主 specs，change 目录移入 `changes/archive/YYYY-MM-DD-<name>/` |
| **store**（beta） | 独立仓库形式的规划空间，可跨仓库/跨团队共享 specs 与 changes |
| **profile** | 全局工作流档位：`core`（精简，默认）/ `custom`（自选命令集） |

Delta spec 格式示例：

```markdown
## ADDED Requirements

### Requirement: 主题切换
系统 SHALL 允许用户在亮色/暗色主题间切换。

#### Scenario: 手动切换
- **WHEN** 用户点击主题切换按钮
- **THEN** 主题立即切换并跨会话持久化
```

> 注意：Scenario 必须用 **4 个 `#`**（`####`），用 3 个 `#` 或列表符号会静默失败；每个 Requirement 必须至少有一个 Scenario，否则 `openspec validate` 报错。

---

## 3. 安装与初始化

```bash
# 终端：全局安装
npm install -g @fission-ai/openspec@latest

# 终端：进入项目目录初始化
cd your-project
openspec init
```

`openspec init` 交互式完成：

1. 选择要集成的 AI 工具（claude、cursor、codex、gemini、opencode 等 30+，可用 `--tools` 指定）
2. 是否创建项目配置 `openspec/config.yaml`（可选但推荐）
3. 是否生成 GitHub Copilot 云端 coding-agent 文件
4. 在项目里生成对应工具的 skills / 斜杠命令文件（如 `.claude/skills/opsx-*`）

常用 init 参数：

| 参数 | 说明 |
|------|------|
| `--tools <ids>` | 非交互指定工具，逗号分隔 |
| `--language <lang>` | 以指定语言撰写新生成的 OpenSpec artifact（多语言支持） |
| `--profile <p>` | 覆盖全局 profile（core/custom） |
| `--force` | 跳过提示自动清理遗留文件 |
| `--copilot-cloud` / `--no-copilot-cloud` | 直接启用/跳过 Copilot 云端 agent 文件生成 |

升级 CLI 后，需要在**每个项目**里重跑 `openspec update` 刷新 AI 指令与斜杠命令。

---

## 4. 目录结构

`openspec init` 之后的项目结构：

```
openspec/
├── config.yaml          # 项目配置（可选，见第 6 节）
├── specs/               # 真相之源：系统当前行为
│   └── <domain>/
│       └── spec.md
├── changes/             # 进行中的变更（一变更一文件夹）
│   ├── <change-name>/
│   │   ├── .openspec.yaml   # change 元数据（schema、skip_specs 等）
│   │   ├── proposal.md      # 为什么、改什么
│   │   ├── design.md        # 技术方案（可选生成）
│   │   ├── tasks.md         # 实现清单（- [ ] 复选框，apply 阶段解析进度）
│   │   └── specs/           # delta specs（与主 specs 同构）
│   │       └── <domain>/spec.md
│   └── archive/             # 已归档变更
│       └── YYYY-MM-DD-<name>/
└── schemas/             # 项目自定义 schema（可选）
    └── <my-workflow>/
        ├── schema.yaml
        └── templates/
```

命名规范：change 名称必须是小写 kebab-case（小写字母、数字、单个连字符，无下划线/大写/连续连字符；允许数字开头如 `100-add-feature`）。

---

## 5. 日常工作流（/opsx 命令）

斜杠命令在 **AI 助手聊天框**里输入（不是终端）；`openspec ...` CLI 在**终端**执行。这是新手最常混淆的点。

默认 core profile 提供的命令：

| 命令 | 作用 | 阶段产出 |
|------|------|---------|
| `/opsx:explore` | 零成本思考伙伴：读代码、权衡方案、把模糊想法打磨成明确计划，**不产生任何 artifact** | 无（纯讨论，可交接给 propose） |
| `/opsx:propose <name>` | 一步创建 change 并生成全部规划 artifact（proposal、specs、design、tasks） | `changes/<name>/` 全套文档 |
| `/opsx:apply` | 按 tasks.md 逐项实现代码，勾选复选框；期间可回头改 artifact | 源码变更 + tasks 勾选 |
| `/opsx:update` | 修订既有 change 的规划 artifact 并保持一致性 | 更新后的文档 |
| `/opsx:sync` | （可选）把 delta specs 合并进主 specs，不移动 change 目录 | 主 specs 更新 |
| `/opsx:archive` | 校验 → 合并 delta → change 目录移入 archive | 归档完成 |

扩展 profile 额外提供的命令（需 `openspec config profile` 开启后 `openspec update` 生效）：

| 命令 | 作用 |
|------|------|
| `/opsx:new` | 仅创建 change 脚手架（轻量起步） |
| `/opsx:continue` | 按依赖链生成下一个 artifact（渐进式） |
| `/opsx:ff` | fast-forward，快速跑完规划 artifact |
| `/opsx:verify` | 对照 artifact 校验实现结果 |
| `/opsx:bulk-archive` | 批量归档多个已完成变更 |
| `/opsx:onboard` | 引导式走完一个端到端变更（新手教程） |

> 不同工具拼写可能不同：Claude Code 用 `/opsx:propose`，Cursor/Copilot 用 `/opsx-propose`，Amazon Q 用 `@opsx-propose`，Codex 用 `$openspec-propose`。

---

## 6. config.yaml 可配置项详解（重点）

OpenSpec 有**两层配置**，注意区分：

| 层级 | 文件 | 格式 | 作用域 |
|------|------|------|--------|
| **项目级** | `<项目根>/openspec/config.yaml`（也接受 `config.yml`，`.yaml` 优先） | YAML | 单个项目：默认 schema、注入上下文与规则 |
| **全局级** | `~/.config/openspec/config.json`（XDG 规范；Windows 为 `%APPDATA%/openspec/`） | **JSON** | 机器级：profile、delivery、遥测等 |

本节讲**项目级 config.yaml**（即大家通常说的"openspec 中的 config.yaml"），全局配置见第 7 节。

### 6.1 完整可配置项一览

```yaml
# openspec/config.yaml —— 全部字段均为可选
schema: spec-driven            # ① 默认工作流 schema
context: |                     # ② 项目上下文（注入所有 artifact 指令）
  Tech stack: TypeScript, React, Node.js
  Testing: Vitest + Playwright
rules:                         # ③ 按 artifact 的附加规则
  proposal:
    - Include rollback plan
  specs:
    - Use Given/When/Then format
  design:
    - Include sequence diagrams
operations:                    # ④ 按操作（apply/archive）的咨询性指引
  apply:
    guidance:
      - Run focused tests before the full suite
  archive:
    guidance:
      - Keep the completion summary concise
references:                    # ⑤ 声明引用的外部 store（beta）
  - team-plans
  - id: another-store
    remote: git@github.com:org/another-store.git
store: team-plans              # ⑥ 声明默认 store（仅 config-only 目录生效）
githubCopilot:                 # ⑦ GitHub Copilot 集成偏好
  cloudAgent: false
```

### 6.2 逐项说明与默认行为

#### ① `schema`（string，非空）

- **作用**：本项目新 change 使用的默认工作流 schema 名称。
- **取值**：内置 `spec-driven`，或项目本地 `openspec/schemas/<name>/`、用户目录、包内置中的任一 schema 名（见第 8 节）。
- **默认行为**：
  - 文件缺失或字段缺失/非法（空字符串、非字符串）→ 回退到内置 **`spec-driven`**（源码 `DEFAULT_OPENSPEC_SCHEMA = 'spec-driven'`，`src/core/openspec-root.ts:17`）。
  - 名称非法时 CLI 会做模糊匹配（Levenshtein 距离 ≤ 3）给出"是不是想说 xxx"的提示，并列出内置/项目本地可用 schema。
- schema 名不允许包含路径分隔符、`.`、`..` 等（防路径穿越）。

#### ② `context`（string，上限 50KB）

- **作用**：项目上下文，注入到**每一个** artifact 的 AI 生成指令中，让 AI 了解技术栈、约定、约束。
- **注入格式**：以 `<context>...</context>` 包裹，位于指令最前部（后面依次是 `<rules>`、`<template>`）。
- **默认行为**：未设置或为空白 → 不注入。超过 **50KB**（`MAX_CONTEXT_SIZE = 50 * 1024`）→ 整个字段被忽略并打印警告（不是截断）。
- 典型内容：技术栈、API 风格、测试框架、兼容性承诺等。

#### ③ `rules`（map：artifact ID → string[]）

- **作用**：按 artifact 附加的规则，**只**注入到 artifact ID 匹配的那个 artifact 的指令中（以 `<rules>...</rules>` 包裹，位于 context 之后、template 之前）。
- **key 约定**：artifact ID 取决于 schema。默认 `spec-driven` 有四个：`proposal`、`specs`、`design`、`tasks`。自定义 schema 的 artifact ID 不受内置命名约束。
- **默认行为**：
  - 未设置 → 不注入。
  - 值不是字符串数组 → 该 artifact 的规则被忽略并告警；空字符串条目被剔除。
  - key 在**所有**可用 schema 中都找不到对应 artifact → 校验时产生警告（`Unknown artifact ID in rules`），但不阻断。
- 与 `context` 的区别：context 全 artifact 生效，rules 仅对应 artifact 生效。

#### ④ `operations`（object，key 仅限 `apply` / `archive`）

- **作用**：给 apply / archive 这两个**操作**（而非 artifact 内容）附加的咨询性指引，数组 `guidance: string[]`。
- **默认行为**：
  - 未设置 → 不注入。
  - 未知的操作 ID（既不是 apply 也不是 archive）→ 警告并忽略；`guidance` 内只支持字符串数组，其他字段告警忽略；空字符串剔除。
  - 工作流在执行时通过 `openspec instructions apply --change <name> --json` / `openspec instructions archive --change <name> --json` 现场拉取最新快照（含 `context` 与 `operationGuidance` 两个独立字段）。
- **语义边界**（源码注释与文档反复强调）：
  - operation guidance **不约束 artifact 内容**，artifact 的 `rules` 也**不会被当作** operation guidance —— 两者严格分离。
  - 它是**建议性**的：工作流会考虑每一条，遵循适用且与内置流程兼容的条目；遇到不适用/冲突的指引会解释原因，不盲从。
  - 使用 `--store <id>` 时，change、context、guidance 均来自该 store 而非当前仓库。
  - 若 instructions 返回非零或非法 JSON，归档/sync 流程视为"查询失败"（而非空输入），**在写任何主 spec 或移动 change 之前停止**。

#### ⑤ `references`（数组：字符串 或 `{id, remote}` 对象）

- **作用**：声明本项目引用的外部 store（独立 OpenSpec 仓库，beta 特性），供跨仓库共享规划。
- **默认行为**：
  - 未设置 → 无引用。
  - 字符串条目 → `{id: <字符串>}`；对象条目需含字符串 `id`，可选非空字符串 `remote`（克隆来源，用于 onboarding 修复提示）。
  - 非法条目（无 id 等）→ 剔除并告警；按 id 去重保留首个位置，后到的重复项仅可补缺 `remote`，不会覆盖。
  - 归一化后为空 → 视同未设置。

#### ⑥ `store`（string）

- **作用**：声明默认 store 作为 OpenSpec 根。
- **默认行为（重要且很窄）**：**只有当该 `openspec/` 目录是"纯配置目录"**（既没有 `openspec/specs/` 也没有 `openspec/changes/` 目录）时，才作为根解析的**回退**；它是 fallback，**永远不会覆盖**本地已有的规划结构、`--store` 标志或上级解析结果。
- 取值必须是单个 store id 字符串，否则警告忽略。root 解析用的是独立的 `readStorePointer()`：config 读不出来（YAML 损坏）或 `store` 键存在但不是字符串时会**报错**而不是静默丢弃——因为"指针被丢弃"会静默改变工作落点。

#### ⑦ `githubCopilot`（object）

- **作用**：GitHub Copilot 集成偏好。目前唯一子键 `cloudAgent: boolean`。
- **默认行为**：字段缺失 = "尚未决定"；由 `openspec init` 在你选择（或拒绝）Copilot 云端 coding-agent 时写入。控制 `init`/`update` 是否生成其文件（GitHub Actions workflow + agent 文件）。类型非法 → 警告忽略。

### 6.3 文件级默认行为与解析规则

| 情形 | 行为 |
|------|------|
| 文件不存在 | 完全正常，返回 null，一切走默认（schema 回退 `spec-driven`，无注入） |
| 文件是 `config.yml` 而非 `.yaml` | 同样支持，`.yaml` 优先 |
| YAML 语法错误 | 整体忽略 + 警告（store 指针读取除外，见 ⑥） |
| 单个字段非法 | **弹性解析**：仅该字段被忽略并告警，其余字段照常生效，不会整体失败 |
| 修改后生效 | 即时生效，每次命令现读（无缓存），无需重启/刷新 |
| 安全防护 | 拒绝 `__proto__`/`constructor`/`prototype` 等原型链键名（CLI set 路径校验 + 解析双保险） |

### 6.4 注入顺序（AI 实际收到的指令结构）

生成任意 artifact 时，AI 收到的指令按以下顺序拼装：

```xml
<context>        ← config.yaml 的 context（若有）
项目技术栈……
</context>

<rules>          ← config.yaml 中该 artifact 的 rules（若有）
- Include rollback plan
</rules>

<template>       ← schema 的内置模板
（schema.yaml 对应 artifact 的 template 内容）
</template>
```

`operations.*.guidance` 不进入这里，而是 apply/archive 执行时单独拉取。

---

## 7. 全局配置（~/.config/openspec/config.json）

注意：全局配置是 **JSON** 文件，不是 YAML。路径遵循 XDG：`$XDG_CONFIG_HOME/openspec/config.json`，默认 `~/.config/openspec/config.json`；Windows 为 `%APPDATA%/openspec/config.json`。

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `featureFlags` | `Record<string, boolean>` | `{}` | 功能开关，无用户可用的公开开关 |
| `profile` | `'core' \| 'custom'` | `'core'` | 工作流档位（决定装哪些 /opsx 命令） |
| `delivery` | `'both' \| 'skills' \| 'commands'` | `'both'` | 命令投递形态：skills、斜杠命令，或两者 |
| `workflows` | `string[]`（可选） | 未设置 | `profile: custom` 时自选的工作流列表 |
| `defaultStore` | `string`（可选） | 未设置 | 机器级兜底 store：仅当无 `--store`、无本地根、无项目级 `store:` 指针时才用 |
| `telemetry.enabled` | `boolean`（可选） | **未设置 = 开启（opt-out 模型）** | 匿名遥测（只采集命令名与版本，无参数/路径/内容/PII，CI 自动关） |
| `telemetry.anonymousId` / `telemetry.noticeSeen` / `completionTipSeen` | 运行时管理 | — | CLI 自动维护，不要手工设置 |

### profile 与 workflows

- **core profile 固定包含**：`propose`、`explore`、`apply`、`update`、`sync`、`archive`（源码 `CORE_WORKFLOWS`，`src/core/profiles.ts:14`）。
- **全部可选工作流**：`propose`、`explore`、`new`、`continue`、`apply`、`update`、`ff`、`sync`、`archive`、`bulk-archive`、`verify`、`onboard`。
- **custom profile**：按 `workflows` 列表安装；若选了 `archive` 或 `bulk-archive` 而没选 `sync`，会自动补上 `sync`（归档依赖规范同步）。
- 切换后需在项目内跑 `openspec update` 才会刷新实际安装的命令文件。

### `openspec config` 子命令

```bash
openspec config path                  # 显示配置文件位置
openspec config list                  # 列出全部设置
openspec config get telemetry.enabled # 读取某项
openspec config set telemetry.enabled false   # 写入某项（自动做类型转换）
openspec config set user.name "Tom" --string  # 强制按字符串写入
openspec config unset user.name       # 删除某项
openspec config reset --all --yes     # 恢复默认
openspec config edit                  # 在 $EDITOR 中打开
openspec config profile               # 交互式向导（delivery + workflows）
openspec config profile core          # 快速切回 core 档（保留 delivery）
```

CLI `set` 支持的键路径白名单：顶层 `featureFlags`、`profile`、`delivery`、`workflows`、`defaultStore`、`telemetry`；`telemetry` 下仅允许 `telemetry.enabled`。未知顶层键会被拒绝。

---

## 8. Schema 体系与解析顺序

### 8.1 schema 是什么

`schema.yaml` 定义一个工作流：包含哪些 artifact、各自生成什么文件、依赖谁、用什么模板、给 AI 什么指令。

> **本仓库已收录全部 schema**：默认内置 + 5 个 intent-driven 系列 + 4 个其他社区 schema，位于工作区根目录 **`schemas/`**，索引见 `schemas/README.md`。

### 8.2 默认 schema（spec-driven）完整内容

源文件：`参考/OpenSpec/schemas/spec-driven/schema.yaml`（副本在 `schemas/spec-driven/`），共 220 行。头部：

```yaml
name: spec-driven
version: 1
description: Default OpenSpec workflow - proposal → specs → design → tasks
```

#### artifact 1：`proposal`（生成 `proposal.md`，无前置）

AI 指令要求按以下小节撰写：

- **Why**：1–2 句说明问题或机会，为什么是现在做
- **What Changes**：变更清单，破坏性变更标注 **BREAKING**
- **Capabilities**（关键小节，构成 proposal 与 specs 阶段的契约）：
  - *New Capabilities*：新增能力，每个对应一个新的 `specs/<capability>/spec.md`，路径段用 kebab-case
  - *Modified Capabilities*：需求发生变化 的既有能力，需产出 delta 文件，使用 `openspec/specs/` 下的**既有确切路径**
- **Impact**：受影响的代码、API、依赖、系统

硬性规则：每个 change 必须声明至少一个能力（新增或修改），或在 `.openspec.yaml` 里显式 `skip_specs: true`，否则 `openspec validate` 拒绝零 delta 的变更——但不要为过校验而编造 requirement。

#### artifact 2：`specs`（生成 `specs/**/*.md`，requires: proposal）

核心规范：**spec 是行为契约，不是实现计划**。

- 应写：可观测行为、输入/输出/错误条件、外部约束（安全/隐私/可靠性/兼容）、可测试的场景
- 不写：内部类/函数名、库选型、实现步骤（属于 design.md / tasks.md）
- 快速判别：若实现可以换而外部可见行为不变，那它就不该出现在 spec 里

Delta 操作（`##` 级标题）：`ADDED` / `MODIFIED`（**必须包含更新后的完整内容**，部分内容会在归档时丢失细节）/ `REMOVED`（必须带 **Reason** 和 **Migration**）/ `RENAMED`（仅改名，FROM:/TO: 格式）。

格式硬约束：Requirement 用 `### Requirement: <名称>` + SHALL/MUST 措辞；Scenario 用 `#### Scenario: <名称>` + WHEN/THEN，**必须恰好 4 个 `#`**（3 个或列表符号会静默失败）；每个 Requirement 至少 1 个 Scenario。

新能力的 delta 必须以 `## Purpose` 开头（≥50 字符，`--strict` 会检查），归档时会复制进主 spec；既有能力不要加 Purpose。

#### artifact 3：`design`（生成 `design.md`，requires: proposal，**条件生成**）

仅在以下情形创建：跨模块/跨服务的横切变更、新外部依赖或重大数据模型变更、安全/性能/迁移复杂度、存在值得先定的技术决策。

小节：Context（只写现状与约束）/ Goals & Non-Goals / Decisions（含备选方案与取舍理由）/ Risks & Trade-offs（格式：[风险] → 缓解）/ Migration Plan / Open Questions（仅放真正可延后的未知项，会改变方案的问题必须现在解决——问用户，别猜）。

#### artifact 4：`tasks`（生成 `tasks.md`，requires: specs + design）

**必须严格遵循模板**：apply 阶段按 `- [ ]` 复选框格式解析进度，不符合的 任务不被追踪。

规则：相关任务归入 `## 数字` 分组；每个任务必须是 `- [ ] X.Y 描述` 复选框；粒度控制在一次会话可完成；按依赖排序；**每个任务必须自带验收方式**（测试、命令、可观测行为或交付物，写进该任务的描述里）。

#### `apply` 配置块

```yaml
apply:
  requires: [tasks]     # apply 前置条件：tasks 必须完成
  tracks: tasks.md      # 进度追踪文件
  instruction: |
    Read context files, work through pending tasks, mark complete as you go.
    Pause if you hit blockers or need clarification.
```

#### templates/

四个模板（`proposal.md`、`spec.md`、`design.md`、`tasks.md`）是注入 AI 提示的骨架，与 artifact 一一对应（见 6.4 节注入顺序）。

### 8.2 名称解析顺序（谁生效）

当 OpenSpec 需要确定用哪个 schema 时，按优先级：

1. **CLI 标志**：`--schema <name>`
2. **change 元数据**：`changes/<name>/.openspec.yaml` 里的 `schema:`
3. **项目配置**：`openspec/config.yaml` 的 `schema:`
4. **默认**：`spec-driven`

### 8.3 目录查找顺序（同名 schema 从哪读）

对同一个名字，按以下顺序找第一个命中（`src/core/artifact-graph/resolver.ts:127`）：

1. **项目本地**：`<项目根>/openspec/schemas/<name>/schema.yaml`
2. **用户级覆盖**：`$XDG_DATA_HOME/openspec/schemas/<name>/`（macOS/Linux 默认 `~/.local/share/openspec/schemas/`；Windows `%LOCALAPPDATA%/openspec/schemas/`）
3. **包内置**：`<openspec 包>/schemas/<name>/schema.yaml`

即项目本地可覆盖同名内置 schema；推荐项目级（随代码入库、随 git 协作）。

### 8.4 自定义 schema

```bash
# 从内置 fork 一份（最快）
openspec schema fork spec-driven my-workflow   # → openspec/schemas/my-workflow/

# 从零创建（交互式）
openspec schema init research-first
# 非交互
openspec schema init rapid --description "..." --artifacts "proposal,tasks" --default

# 校验（语法、模板存在性、无循环依赖、ID 合法性）
openspec schema validate my-workflow

# 查询某 schema 实际解析自哪里 / 列出全部
openspec schema which my-workflow
openspec schema which --all
```

自定义 `schema.yaml` 骨架：

```yaml
name: my-workflow
version: 1
description: 我的团队工作流
artifacts:
  - id: proposal
    generates: proposal.md        # 支持 glob，如 specs/**/*.md
    description: 提案
    template: proposal.md         # templates/ 下的模板文件
    instruction: |                # 给 AI 的生成指令
      说明这个 artifact 怎么写……
    requires: []                  # 前置 artifact
apply:
  requires: [tasks]
  tracks: tasks.md
```

社区 schema 以独立仓库分发，官方目录页见 `参考/OpenSpec/docs/customization.md` 的 Community Schemas 一节。**本仓库已将全部社区 schema 收录至根目录 `schemas/`**（intent-driven 系列含 behaviour-driven、event-driven、minimalist、spec-driven-with-adr 共 5 个，另有 superpowers-bridge、anvil、nanopm、e2e-runbooks），每个的定位与 artifact 流见 `schemas/README.md`。使用时把对应子目录复制进目标项目的 `openspec/schemas/<name>/` 即可。

---

## 9. CLI 命令参考

### 初始化与维护

| 命令 | 说明 |
|------|------|
| `openspec init [path]` | 初始化项目（选工具、建 config、生成 skills） |
| `openspec update [path]` | 升级后刷新 AI 指令文件与斜杠命令 |

### 浏览与查看

| 命令 | 说明 |
|------|------|
| `openspec list` | 列出进行中的 changes / specs（`--json` 供脚本） |
| `openspec view` | 交互式 dashboard |
| `openspec show [name]` | 查看 change 或 spec 详情（`--json`） |
| `openspec status --change <name>` | artifact 完成度（done/ready/blocked，`--json` 供 agent 判断下一步） |

### 校验与生命周期

| 命令 | 说明 |
|------|------|
| `openspec validate [name]` | 校验 change/spec 格式（`--all`、`--strict`、`--json`） |
| `openspec new change <name>` | 创建 change 脚手架（`--description`、`--goal`、`--schema`、`--store`） |
| `openspec archive [name]` | 归档：校验 → 合并 delta → 移入 archive（`--yes` 免确认供 CI/agent；`--skip-specs` 跳过规范合并；`--no-validate`） |

### Agent 专用（供 AI 调用，多为 `--json` 输出）

| 命令 | 说明 |
|------|------|
| `openspec instructions [artifact]` | 获取某个 artifact 的增强生成指令（context+rules+template 拼装结果）；参数也可以是 `apply` / `archive` 这两个操作面 |
| `openspec templates` | 查看某 schema 各 artifact 的模板路径 |
| `openspec schemas` | 列出可用 schema 及 artifact 流 |

### Schema 管理

| 命令 | 说明 |
|------|------|
| `openspec schema init / fork / validate / which` | 见第 8.4 节 |

### Store（beta，跨仓库规划）

| 命令 | 说明 |
|------|------|
| `openspec store setup / register / unregister / remove / list / doctor` | 建立、注册、注销、移除、列出、体检独立规划仓库 |

### 其他

| 命令 | 说明 |
|------|------|
| `openspec config ...` | 全局配置管理（见第 7 节） |
| `openspec doctor` | 仓库关系健康检查 |
| `openspec context` | 查看当前组装的工作上下文 |
| `openspec workset` | 个人工作集（hand-edited openers） |
| `openspec feedback <msg>` / `openspec completion [shell]` | 反馈 / shell 补全安装 |

### change 元数据（`.openspec.yaml`）

每个 change 可携带元数据，与 config.yaml 互补：

```yaml
schema: spec-driven        # 必填：本 change 使用的 schema
created: 2025-01-24        # 可选
goal: 支持 SSO 登录         # 可选
skip_specs: true           # 可选：声明本变更无规范级变化（纯重构/工具/文档），
                           # validate 允许零 delta；specs artifact 视为完成（状态显示 skipped）
retire_capabilities: true  # 可选：允许归档时"退役"能力——当 REMOVED 删光某能力
                           # 最后一条 requirement 时删除其主 spec 文件（不可从工作区恢复，需作者显式声明）
```

---

## 10. 环境变量

| 变量 | 说明 |
|------|------|
| `OPENSPEC_TELEMETRY=0` | 关闭遥测与 update 版本检查（覆盖全局配置） |
| `DO_NOT_TRACK=1` | 同上（标准 DNT 信号，覆盖配置） |
| （`CI` 为真值，如 `true`/`1`/`yes`） | 无论配置如何，始终禁用遥测 |
| `OPENSPEC_CONCURRENCY` | 批量校验并发数（默认 6） |
| `EDITOR` / `VISUAL` | `openspec config edit` 使用的编辑器 |
| `NO_COLOR` | 禁用彩色输出 |
| `OPENSPEC_NO_ANIMATION` | 禁用 init 欢迎动画 |
| `OPENSPEC_NO_COMPLETIONS=1` | 屏蔽 shell 补全的一次性提示 |
| `OPENSPEC_NO_UPDATE_CHECK` | 禁用 CLI 新版本检查（任何值；`CI` 或 `NODE_ENV=test` 时自动跳过） |
| `npm_config_registry` | 版本检查使用的 npm registry（须为 http(s) URL，否则回退官方源） |

优先级：**环境变量 > 全局 config.json > 默认值**。

---

## 11. 常见问题排查

**"Unknown artifact ID in rules: X"**
`rules` 的 key 必须匹配某个 schema 的 artifact ID。用 `openspec schemas --json` 查看各 schema 的 artifact ID；默认 `spec-driven` 是 `proposal`/`specs`/`design`/`tasks`。

**config 没生效**
- 确认文件在 `openspec/config.yaml`（`.yml` 也支持但 `.yaml` 优先），且 YAML 语法正确；
- 配置即时生效、无缓存，改完即用；
- 注意区分项目级 config.yaml 与全局 config.json——profile/delivery/telemetry 在全局层，schema/context/rules 在项目层。

**Context 被忽略**
超过 50KB 会被整体丢弃（不截断）并告警；精简内容或改为链接外部文档。

**`/opsx:xxx` 命令不存在**
默认 core profile 只有 6 个命令；`new`/`continue`/`ff`/`verify`/`bulk-archive`/`onboard` 属扩展集，需 `openspec config profile` 开启后 `openspec update` 应用。

**归档在 CI/无终端环境直接失败退出 1**
archive 默认需要交互确认；stdin 关闭时无法应答会中止并提示。改用 `openspec archive <name> --yes`。

**不知道当前生效的 schema 是哪个**
`openspec schema which <name>` 看来源（project/user/package），`openspec status --change <name>` 看 change 实际解析到的 schema；解析顺序：`--schema` 标志 > change 的 `.openspec.yaml` > 项目 config.yaml > 默认 `spec-driven`。

**Scenario 校验老不通过**
Scenario 标题必须恰好 4 个 `#`（`####`）；每个 Requirement 至少 1 个 Scenario；新能力的 delta 必须以 `## Purpose` 开头（≥50 字符，否则 `--strict` 报过于简短）。

---

## 附：与本项目（agent-flow）的关系

OpenSpec 的可借鉴点：

1. **配置双分层**：项目级 YAML（团队可入库共享）+ 全局级 JSON（个人偏好），弹性解析（坏字段只降级不崩溃）。
2. **多级回退链**：CLI 标志 > change 元数据 > 项目配置 > 内置默认，每层都有明确默认值。
3. **指令注入模型**：`context`（全局）+ `rules`（按 artifact）+ `template`（schema）三段式拼装给 AI，操作级 guidance（`operations`）单独通道。
4. **schema 即工作流**：用声明式 YAML 定义 artifact 图（依赖、模板、指令），fork 机制支持团队定制而不 fork 代码。
