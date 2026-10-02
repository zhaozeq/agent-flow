# e2e-runbooks

OpenSpec schema，用于 spec 驱动、AI 或人类可执行的、仅行为的 e2e 能力测试。

## 功能

你添加的每个能力测试都获得一个**不可变 spec**，描述它要验证的内容；一个配对的**不可变 tasks-template**，带有镜像 spec 的复选框；以及每个执行一次的**运行记录**。运行记录带有开始/结束 UTC、计算出的持续时间，以及最佳的 LLM token 消耗估算。

断言仅是可观察行为：HTTP 状态码、响应体内容、MinIO / Qdrant / Postgres 等中的持久化状态。永远不要记录日志子串；它们跨版本变化，并非在每个运行器的 shell 中都可见。

## Artifact DAG

```text
proposal ─► test-spec ─► tasks-template ─► run（每次执行）
```

- **proposal** — 仅在添加新的能力测试时必需。命名行为、设置成本类别、fixtures、API 客户端调用、所选的 N 前缀。
- **test-spec** — 不可变 spec，按七个固定章节（What this verifies、Prerequisites、Reset state、Run、Expected、Fixtures、Concurrency）描述一个能力。
- **tasks-template** — 镜像 spec 的不可变清单。
- **run** — 执行记录。每次执行时填写。

## 并发配置文件

每个 proposal（以及从中生成的 test-spec）都带有一个三行的**并发配置文件**，声明测试如何与扫描中的其他测试交互：

- **Mutates:** 测试写入、删除或使其失效的后台服务资源。命名存储和 collection / table / bucket；当测试仅触及一个时添加分区（user id、tenant id）。只读探测不计入——写 `none`。
- **Conflicts with:** 即使 `Mutates:` 列表不重叠也无法与之并行运行的其他测试。典型条目：`"any test that restarts the stack"`、`"any test that talks to the license server"`。如果唯一冲突来自 `Mutates:` 重叠则留空。
- **Serial:** 字面量 `true` 或 `false`。`true` 意味着测试必须单独运行——模式迁移、全栈重启、任何触及全局配置的内容。默认 `false`。

驱动扫描的主 agent 在生成运行器之前从每个 spec 读取这三个字段。它询问用户希望并行运行多少个测试，然后调度它们，使得没有两个并行测试的 `Mutates:` 列表重叠，没有一个在 `Conflicts with:` 下命名另一个，任何 `Serial: true` 的测试单独运行。完整的调度规则见 [`INTEGRATION.md`](./INTEGRATION.md)。

## 文件落地

OpenSpec 在变更目录（`openspec/changes/<change-id>/`）内起草每个 artifact。对于此 schema，四个 artifact 中的三个在消费者项目的 `e2e/` 树中也有永久归宿。agent 在两个位置都写入，因为 OpenSpec 的 `archive` 命令仅自动提升 `openspec/specs/` 中的内容；其他所有内容都需要显式双重写入：

| Artifact         | 变更目录路径（OpenSpec 审计跟踪）              | 最终归宿（工作资产）                                                |
| ---------------- | ---------------------------------------------- | ------------------------------------------------------------------- |
| `proposal`       | `openspec/changes/<id>/proposal.md`            | _无 — proposal 保留在变更目录中_                                    |
| `test-spec`      | `openspec/changes/<id>/test-spec.md`           | `e2e/testing/{N}-{capability}-test.md`                              |
| `tasks-template` | `openspec/changes/<id>/tasks-template.md`      | `e2e/testing/templates/{N}-{capability}-tasks.template.md`          |
| `run`            | `openspec/changes/<id>/run.md`                 | `e2e/testing/runs/{utc-timestamp}_{N}-{capability}-tasks.md`（被 gitignore）|

每个 artifact 的 `instruction:` 在 [`schema.yaml`](./schema.yaml) 中告诉 agent 执行双重写入。`{N}`、`{capability}` 和 `{utc-timestamp}` 由 agent 从 proposal 的内容中填充——OpenSpec 本身不会在 `generates:` 路径中替换 schema 占位符。

## 安装

此 schema 位于源仓库的 `openspec/schemas/e2e-runbooks/` 中——你的消费者项目中所需的同一路径。安装是从项目内部执行 `git fetch` + `git checkout`；仅写入 schema 的目录，树中的其他内容不受影响。

你的消费者项目必须是 git 仓库，并且必须已初始化 OpenSpec（`openspec init`）。从项目根运行：

```bash
git fetch --depth 1 https://github.com/Lukk17/openspec-schemas v0.1.0
```

```bash
git checkout FETCH_HEAD -- openspec/schemas/e2e-runbooks
```

同样的两条命令在 PowerShell 中也适用。文件落在你的工作树中并且已暂存——用 `git diff --staged` 审查并在准备好时提交。要稍后升级，使用新标签重新运行。

然后按变更调用（需要 `change` 子命令；`--schema` 是其上的一个选项）：

```bash
openspec new change "add-weather-mcp-test" --schema e2e-runbooks
```

或者在项目的 `openspec/config.yaml` 中将其设置为默认值，并使用 `/opsx:propose` 驱动它：

```yaml
default_schema: e2e-runbooks
```

## 伴随技能和子 agent

此 schema 是由 [Lukk17/agent-standards](https://github.com/Lukk17/agent-standards) 一起提供的三件套之一：

- **技能** 在 `.agents/skills/e2e-runbooks/SKILL.md` — 方法论真相来源。行为断言、金丝雀 fixtures、API 客户端替代方案（Bruno、hurl、REST Client、curl、httpie）、runs 目录契约、通用工作示例。
- **子 agent** 在 `.claude/agents/e2e-runner.md` 和 `.opencode/agents/e2e-runner.md` — 端到端扫描时的推荐委托。拥有运行器契约（Start/End UTC、Duration、tokens、Verdict）和变更目录/`e2e/testing/runs/` 双重写入。schema 和技能也可以在没有它的情况下工作；运行可以从主会话或通用运行器驱动。
- **Schema**（此文件夹）— 通过上述 artifact DAG 为 OpenSpec 用户实现方法论。

每个部分都可以独立安装：技能在没有 OpenSpec 的项目中工作，schema 在没有 agent-standards 的项目中工作。它们一起相互强化。

## 需要了解的 OpenSpec 限制

此 schema 是围绕两个已知的 OpenSpec 限制设计的：

- [Fission-AI/OpenSpec#777](https://github.com/Fission-AI/OpenSpec/issues/777) — schema 的 `instruction` 字段可以命名外部技能，但 `openspec-continue-change` 不能可靠地委托。我们将运行器契约直接嵌入到 `run` artifact 的 instruction 散文里，没有中段 DAG 技能委托。
- [Fission-AI/OpenSpec#666](https://github.com/Fission-AI/OpenSpec/issues/666) — OpenSpec 的 spec 格式部分硬编码在包代码中。我们将 spec artifact 命名为 `test-spec`（而不是 `spec`）以避开硬编码格式。

## 许可证

MIT。