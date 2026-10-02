## Why

<!-- 解释本次变更的动机。它解决了什么问题？为什么是现在？ -->

## What Changes

<!-- 描述将要变更的内容。要具体说明新增能力、修改或删除。 -->

## Capabilities

### New Capabilities
<!-- 正在引入的新能力。对你新增的路径段使用 kebab-case
     （例如 user-auth 或 identity/user-auth），遵循项目已有的
     spec 组织方式。每个都会创建 specs/<capability-path>/spec.md。 -->
- `<capability-path>`：<该 capability 涵盖内容的简短描述>

### Modified Capabilities
<!-- 现有能力中正在发生 REQUIREMENTS 变更的（不仅仅是实现）。
     仅在 spec 级别行为发生变化时才在此列出。每个都需要一个 delta spec 文件。
     使用 openspec/specs/ 下的精确现有路径。如果没有需求变更则留空。
     完全没有任何 capability 的变更（纯重构、工具、文档）
     必须在它的 .openspec.yaml 中设置 `skip_specs: true` - openspec validate 拒绝
     没有该标记的零 delta 变更。不要为了满足校验而虚构需求。 -->
- `<existing-capability-path>`：<正在变更的需求>

## Impact

<!-- 受影响的代码、API、依赖、系统 -->