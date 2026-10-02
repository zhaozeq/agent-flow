# 带有 ADR 的 Spec-Driven OpenSpec Schema

`spec-driven-with-adr` 适用于需要标准的从 proposal 到 tasks OpenSpec 流程加上持久架构决策记录的变更。

主要参考：
- 文章：https://intent-driven.dev/blog/2026/04/29/spec-driven-development-with-adr/

[![Spec-Driven Development with ADR](https://img.youtube.com/vi/y5oemaPsmOA/hqdefault.jpg)](https://youtu.be/y5oemaPsmOA)

- 良好场景：架构变更、平台决策、跨模块工作、新服务边界、技术选择，或未来贡献者需要持久决策记录的变更。
- 不适合的场景：小幅战术修复、纯内容编辑、简单 UI 变更，或 `specs -> tasks` 就足够的工作。

## 安装（复制/粘贴）

对根 `README.md` 单行安装命令使用：
- `SCHEMA="spec-driven-with-adr"`

## 激活

在 `openspec/config.yaml` 中设置：

```yaml
schema: spec-driven-with-adr
```

## 阶段门

Artifact 顺序：
`proposal -> specs -> design -> adr -> tasks`

门控期望：
- `specs` 必须基于 `proposal.md` 中识别的 capabilities。
- `design` 必须考虑 proposal、specs 和当前生效的 ADR。
- `adr` 通过编写 `openspec/changes/<change>/adr.md` 完成——这是在 design 之后、任务规划之前创建的简洁 ADR 审查清单。
- `tasks` 仅在 proposal、specs、design 和 ADR artifact 完成后才规划。

## ADR 持久化

`openspec/changes/<change>/adr.md` 是用于 OpenSpec artifact 完成的每变更 ADR 审查 artifact。
它记录 ADR 审查的发生，列出已审查的现行生效 ADR 上下文，并引用为该变更创建的任何持久 ADR 文件。

持久 ADR 文件在目标仓库的顶级 `adr/` 文件夹下生成，而不是在 OpenSpec 变更文件夹内。
仅当变更引入了一个重大的持久架构决策时才创建 `adr/NNNN-kebab-title.md`。
已接受的 ADR 不可变。如果未来决策更改了先前的 ADR，请创建一个取代旧 ADR 的新 ADR，并保持原文件不变。

## 关联技能

此 schema 在 `skills.txt` 中声明其伴随技能；它们由 `AGENT_INSTALL.md` 的第 6 步自动安装到 `.agents/skills/`，来源是 [intent-driven-dev/skills](https://github.com/intent-driven-dev/skills)。

- [`architectural-decision-records`](https://github.com/intent-driven-dev/skills/tree/main/.agents/skills/architectural-decision-records) — 起草/审查 ADR；包括 MADR、Nygard 和 Y-statement 模板，并负责选择此 schema 使用的 ADR 样式/模板。
- `openspec-git-discipline` — OpenSpec propose/apply/archive 工作流的 git 卫生。

更多 schema，请参考 https://github.com/intent-driven-dev/openspec-schemas。