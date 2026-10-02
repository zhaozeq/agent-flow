## Why

<!--
解释本次变更的动机。它解决了什么问题？为什么是现在？

硬限制：50 ≤ 字符数 ≤ 1000（OpenSpec zod schema 会 validate）
- 太短：会收到 `Why section must be at least 50 characters` error
- 太长：会收到 `Why section should not exceed 1000 characters` error

建议结构：现状痛点 → 为什么现在处理 → 预期收益（各 1-2 句）
-->

## What Changes

<!--
描述将要变更的内容。要具体说明新增能力、修改或删除。

对于有明确前后对比的行为变更，使用 From/To 格式（markdown 无 inline diff）：

**<Section or Behavior Name>**
- From: <当前状态/需求>
- To: <未来状态/需求>
- Reason: <为什么需要此变更>
- Impact: <breaking / non-breaking，谁受影响>

多个变更可重复此 block；纯新增或纯删除可用简单列表描述。
-->

## Capabilities

### New Capabilities
<!--
正在引入的新能力。将 <name> 替换为 kebab-case 标识符。
命名规则见 openspec/specs/README.md：使用复合名词（至少 2 个 word），
例如 `user-auth`、`data-export`、`api-rate-limiting`，不用纯单词。
Each creates specs/<name>/spec.md
-->
- `<name>`: <该 capability 涵盖内容的简短描述>

### Modified Capabilities
<!--
现有能力中 REQUIREMENTS 正在变更的（不仅仅是实现）。
仅在 spec 级别行为发生变化时才在此列出。每个都需要一个 delta spec 文件。
使用 openspec/specs/ 中的现有 spec 名称。如果没有需求变更则留空。
-->
- `<existing-name>`: <正在变更的需求>

## Impact

<!-- 受影响的代码、API、依赖、系统 -->