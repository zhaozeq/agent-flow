# {capability}：e2e 能力测试 proposal

## Why

<!-- 50-1000 个字符。需要端到端断言什么行为？它填补了当前测试套件中的什么空白？
如果有的话，锚定到一个真实风险或最近的事件。 -->

## What this will verify

<!-- 项目符号列表。仅可观察行为：HTTP 状态码、响应体内容、后台服务中的持久化状态。不要日志子串。 -->

-
-

## Setup cost class

<!-- 选择一个。较低的数字在扫描中先运行。决定 spec 文件名中的 {N} 前缀。 -->

- [ ] 1：无状态要重置，无 fixtures，命中单个端点或 MCP 工具。
- [ ] 2：单个 fixture 上传或视觉能力模型或 PDF 解析。
- [ ] 3：单服务重置（例如仅 Redis）。
- [ ] 4：多服务重置（DB + Redis + Qdrant + MinIO）。
- [ ] 5：种子状态 + 观察异步后台进程。

## Fixtures needed

<!-- 列出此测试将读取的金丝雀文件。每个必须包含足够独特的内容，
使得通过测试证明的是检索而非记忆。如果没有则留空。 -->

-

## Concurrency profile

<!-- 声明此测试变更哪些后台服务状态，以便编排者可以决定什么并行运行。
有关字段语义，请参阅 agent-standards 中 e2e-runbooks 技能的 Concurrency-constraints 章节。 -->

- **Mutates:** <测试写入/删除/失效的每个资源：存储 + collection/table/bucket + 分区（user/tenant id）（如适用）。只读探测不计入。如果真的是只读，则使用 `none`。>
- **Conflicts with:** <通常是"变更相同资源的任何其他测试"；当从 Mutates 重叠不明显时命名明确的冲突。>
- **Serial:** <`true` 如果测试无法与任何其他测试并行运行（迁移、全栈重启、许可证服务器交互）。默认 `false`。>

## API client invocation

<!-- 命名确切的请求文件。Bruno YAML、hurl 文件、REST Client .http 或 curl 调用。 -->

-

## Number assignment

<!-- 选择与上述设置成本类别匹配的最低未使用的 {N}。 -->

N:

## Next steps

在批准此 proposal 后：

- 从 `test-spec` artifact 生成 `e2e/testing/{N}-{capability}-test.md`。
- 从 `tasks-template` artifact 生成 `e2e/testing/templates/{N}-{capability}-tasks.template.md`。
- 每次执行在 `e2e/testing/runs/` 下生成一个 `run` 记录。