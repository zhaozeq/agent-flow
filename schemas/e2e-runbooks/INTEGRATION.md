# `e2e-runbooks` 的集成说明

## 生命周期：变更目录加 `e2e/` 树

OpenSpec 假设在 proposal 周期中每个 artifact 都位于 `openspec/changes/<change-id>/` 下，并且
`archive` 将完成的内容提升到 `openspec/specs/`。此 schema 的 artifact 有不同的最终归宿——
spec 在 `e2e/testing/` 下，它们的运行记录模板在 `e2e/testing/templates/` 下，执行记录在
`e2e/testing/runs/` 下——所以 schema 指示**双重写入**，而不是依赖 archive。

```text
变更目录 artifact                         副本种类          工作树目的地
─────────────────────────────────────────────────────────────────────────────────────────────────
openspec/changes/<id>/proposal.md           (无)              保留在变更目录中
openspec/changes/<id>/test-spec.md          相同         ──►  e2e/testing/{N}-{capability}-test.md
openspec/changes/<id>/tasks-template.md     相同         ──►  e2e/testing/templates/{N}-{capability}-tasks.template.md
openspec/changes/<id>/run.md                带时间戳   ──►  e2e/testing/runs/<UTC-ts>_{N}-{capability}-tasks.md  (被 gitignore)
```

消费者项目中的结果 `e2e/` 树：

```text
e2e/
├── fixtures/
└── testing/
    ├── {N}-{capability}-test.md              # spec
    ├── templates/
    │   └── {N}-{capability}-tasks.template.md
    └── runs/
        └── <UTC-ts>_{N}-{capability}-tasks.md   # 被 gitignore
```

为什么需要两个副本：

- **变更目录副本** 是 proposal 的审计跟踪。它将 artifact 固定到引入（或修改）它的变更，并在审查和归档过程中随之移动。
- **`e2e/testing/` 副本** 是运行消耗的工作资产。`e2e/testing/runs/` 中的记录指向的就是它。扫描遍历 `e2e/testing/*-test.md`，而不是变更目录。

两个副本之间的漂移是最可能的缺陷类别。当你修改 spec 时，在同一个提交中对变更目录副本进行相同的编辑——永远不要让它们静默分歧。

Proposal 仅保留在变更目录中。没有 `e2e/proposals/` 镜像。

## 与 agent-standards 技能和子 agent 配对

该方法论存在于通过 [Lukk17/agent-standards](https://github.com/Lukk17/agent-standards) 一起提供的三个地方：

- `.agents/skills/e2e-runbooks/SKILL.md` 是方法论真相来源。
- `.claude/agents/e2e-runner.md` 和 `.opencode/agents/e2e-runner.md` 是运行器子 agent — 驱动扫描时的推荐委托。它强制执行运行器契约（Start/End UTC、Duration、tokens、Verdict）以及对 `e2e/testing/runs/` 的双重写入。
- 此 schema 是 OpenSpec 用户的操作形态。

当你编辑其中一个时，请在同一个变更中审查其他两个。方法论、子 agent 行为和 schema 模板之间的漂移是最可能的缺陷类别。

每个部分都可以独立安装。单独使用技能时无需 OpenSpec。单独使用 schema 时无需 agent-standards。它们一起相互强化。

## 扫描编排

主 agent 拥有扫描，而不是运行器。它按数字顺序读取 `e2e/testing/*-test.md`，选择一个所有运行器共享的 UTC 时间戳，然后为每个测试生成一个 `e2e-runner` 子 agent。在生成之前，主 agent 询问用户希望并行生成多少个运行器——没有预设上限。正确的数字取决于测试环境（专用栈比共享开发栈能容忍更多并行，许可证服务器或付费 API 等外部依赖可能要求较低的数字）。

随着每个运行器返回其判定，主 agent 生成下一个待定测试，直到每个 spec 都已运行。然后它聚合：通过/失败计数、总 token 使用、总实际耗时（最长单个运行，而非总和）以及带有从每个失败的运行器报告复制的一行原因的简短失败列表。

用户选择的并行数量可以作为 `e2e-runner-max-parallel: <N>` 保存在消费者项目的 `AGENTS.md` 中，以便未来的扫描重用同一数字而无需重新询问。

## 并发分析

每个 spec 的 `Concurrency` 部分告诉主 agent 哪些测试可以同时与哪些其他测试一起运行。
主 agent 在生成之前读取每个 spec，然后按它们触及的资源对测试进行分组：

- 两个 `Mutates:` 列表不重叠的测试可以在同一批次中运行。
- 两个 `Mutates:` 列表重叠的测试（同一存储、同一 collection/table/bucket、同一分区）必须一个接一个运行。
- 标记为 `Serial: true` 的测试等待所有正在运行的运行器完成，单独运行，然后恢复其余队列。

用户选择的并行数字是上限；`Concurrency` 规则只能将并行降低到它之下，永远不能超过它。八个具有完全不相交的 `Mutates:` 列表的测试和用户选择的限制为三个，仍然会一次运行三个。

字段语义（agent-standards 技能具有权威定义；这里是快速参考）：

- `Mutates:` — 测试写入、删除或使其失效的每个后台服务资源。命名存储和 collection / table / bucket；当测试仅触及一个时添加分区（user id、tenant id）。只读探测不计入——写 `none`。
- `Conflicts with:` — 即使 `Mutates:` 列表不重叠，此测试也无法与之并行运行的其他测试。典型条目："任何重启栈的测试"、"任何与许可证服务器通信的测试"。如果唯一冲突明显来自 `Mutates:` 重叠则留空。
- `Serial:` — 字面量 `true` 或 `false`。`true` 意味着模式迁移、全栈重启、许可证服务器交互、任何触及全局配置的内容。默认 `false`。

一个单独运行时通过但在扫描中失败的测试几乎总是某个 spec 的 `Mutates:` 列表中缺少一个条目。修复方法是将缺失的资源添加到 spec 中，而不是插入 sleep。

## API 客户端选择

schema 不绑定客户端。每个项目选择一个并一致地用于所有测试。推荐的默认值：

| 客户端 | 何时使用 | 备注 |
| --- | --- | --- |
| [Bruno CLI](https://www.usebruno.com/) | REST API、多步骤流程、成熟的集合 | API 真相的单一来源；请求文件 = 测试 fixture。将请求固定到 `X-User-Id` 或类似的每项目标头。 |
| [Hurl](https://hurl.dev/) | 纯文本 HTTP、请求文件中嵌入的断言 | 比 Bruno 更轻；断言与请求相邻。 |
| `curl` | 单次健康检查、MCP HTTP 探测 | 用于 spec 内的先决条件探测；除非测试极其简单，否则不用于主 Run 步骤。 |
| [httpie](https://httpie.io/) | 交互式调试 | 避免用于存储的测试定义；它是符合人体工程学的 CLI，而不是 fixture 格式。 |
| VS Code REST Client | 非 CLI 工作流 | `.http` 文件；适合仅人类执行的路径。 |

对于 MCP 工具测试，通过 agent 驱动（而不是直接通过 MCP 服务器），这样你断言的是端到端发现和路由，而不仅仅是 MCP 协议机制。

## CI 集成草图

```yaml
# .github/workflows/e2e-sweep.yml
name: e2e-sweep
on:
  workflow_dispatch:
  schedule:
    - cron: "0 6 * * *"   # 每日扫描
jobs:
  sweep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker compose up -d --build
      - run: npm install -g @usebruno/cli   # 或 hurl / 等等
      - run: |
          for spec in e2e/testing/*-test.md; do
            N="${spec##*/}"
            # 从模板打开匹配的运行记录，通过 API 客户端驱动，
            # 根据 CI 输出勾选框，将记录提交到 runs/
          done
```

无论是人类还是 AI 执行，运行器契约都是一样的。CI 只是自动化运行器角色。

## 在 git 中记录运行

默认假设 `e2e/testing/runs/` 被 gitignore — 运行是短暂的，在审查时作为审计有用，提交时成为噪音。
对于审计跟踪，提交到 `runs/<YYYY-MM>/` 子文件夹下，以便一次扫描的记录聚集在一起。