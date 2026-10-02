# 行为驱动 OpenSpec Schema

`behaviour-driven` 是一个从 proposal 到 tasks 的工作流，适用于在实施前应捕获贡献者意图、可观察行为和技术设计的变更。

它通过生成 `specs/<capability>/spec.md` 文件使 spec 默认情况下可通过默认 OpenSpec archive 合并。
Markdown 标题是 OpenSpec 包装器；每个需求和场景内部的内容应该用 Gherkin 风格编写，使用 `GIVEN`、`WHEN` 和 `THEN` 步骤。

- 良好场景：具有重要可观察行为的产品或平台变更，最好在构建之前进行规范。
- 不适合的场景：小幅战术修复、纯文档变更或依赖升级。
- 还需要持久的架构决策？请使用 [`intent-driven`](../intent-driven/README.md) — 相同的工作流加上每变更 ADR 审查 artifact 和持久的仓库级 ADR 文件。

## 激活

在 `openspec/config.yaml` 中设置：

```yaml
schema: behaviour-driven
```

激活 schema 不需要其他键。

## 阶段门

Artifact 顺序：

```text
proposal -> (specs, design) -> tasks
```

`specs` 和 `design` 都仅依赖于 proposal，可以并行进行；`tasks` 需要两者。

门控期望：

- `proposal` 说明变更为何重要，并列出需要行为 spec 的 capability。
- `specs` 在 `specs/<capability>/spec.md` 为每个 capability 创建一个 OpenSpec Markdown delta 文件。
- `design` 解释实现方法。
- `tasks` 仅在 proposal、specs 和 design 完成后才规划。

## Spec 格式

使用 OpenSpec Markdown delta 头部以便 archive 可以合并变更：

```md
## ADDED Requirements

### Requirement: 用户数据导出
系统 SHALL 允许用户导出他们自己的已保存数据。

#### Scenario: 成功 CSV 导出
- **GIVEN** 用户有已保存数据
- **WHEN** 用户将其数据导出为 CSV
- **THEN** 系统提供一个包含用户数据的 CSV 文件
```

需求使用 `### Requirement:` 配合 SHALL/MUST 描述；场景使用恰好四个井号（`#### Scenario:`）配合 `GIVEN`/`WHEN`/`THEN` 步骤。
每个需求至少需要一个场景。`MODIFIED` 条目在编辑前从 `openspec/specs/<capability>/spec.md` 复制整个现有需求块，这样在归档时不会丢失任何细节。

这与 `intent-driven` schema 使用的 spec 格式相同。

## 可执行 Spec 由技能提供

此 schema 仅描述 artifact 工作流。它不定义围栏 Gherkin 格式、不抽取 `.feature` 文件、不运行验收套件、不强制 spec/代码区域隔离。
所有这些都是由可选的
[`spec-as-source`](https://github.com/intent-driven-dev/skills/tree/main/.agents/skills/spec-as-source)
技能提供的，它将 `spec.md` 视为可执行的真相来源，并在激活时用其自己的引用覆盖此 schema 的 `spec.md` 和 `tasks.md` 模板。
该技能还拥有过去在此声明的两条规则——验收测试始终通过、spec 和代码永远不会在同一工作单元中一起修改（`tasks.md` 豁免）。

`spec-as-source` 需要 `gherkin-authoring` 和
[`acceptance-test-authoring`](https://github.com/intent-driven-dev/skills/tree/main/.agents/skills/acceptance-test-authoring)
技能，后者负责运行器设置、抽取、检查、报告和它们需要的 `stack:` 键。

当希望 spec 作为验收测试运行时采用该技能；当仅希望在没有测试 harness 的情况下获得 artifact 纪律时单独使用 schema。

## 校验

```bash
openspec schema validate behaviour-driven
```

## 关联技能

此 schema 在 `skills.txt` 中声明其伴随技能；它们由 `AGENT_INSTALL.md` 的第 6 步自动安装到 `.agents/skills/`，来源是 [intent-driven-dev/skills](https://github.com/intent-driven-dev/skills)。

- `acceptance-test-authoring` — 验收套件设置：Gherkin 抽取、有效 spec 组合、两个栈的运行器、检查和报告。
- `gherkin-authoring` — 编写和审查 Gherkin/BDD 场景。
- `glossary` — 在 artifact 之间保持领域/技术术语的一致性。
- `openspec-git-discipline` — OpenSpec propose/apply/archive 工作流的 git 卫生。
- `spec-as-source` — 可选工作流，使 `spec.md` 成为可执行的真相来源：围栏 Gherkin 编写、验收优先的任务排序，以及 spec/代码区域隔离。

更多 schema，请参考 https://github.com/intent-driven-dev/openspec-schemas。