# {capability}：运行记录

Spec: [`../{N}-{capability}-test.md`](../{N}-{capability}-test.md)

<!--
此文件是通过将 `../templates/{N}-{capability}-tasks.template.md`
复制到此位置并填写而创建的。文件名使用 ISO-8601 UTC，冒号替换为连字符：
`runs/2026-05-12T17-23-36_{N}-{capability}-tasks.md`。

上面的 Spec 反向链接（`../{N}-{capability}-test.md`）是为
`e2e/testing/runs/` 下的规范归宿编写的，spec 位于上一级目录。
变更目录中的审计跟踪副本（`openspec/changes/<id>/run.md`）是扁平的，
因此在编写该副本时，将链接指向同级 `test-spec.md`。
两个副本共享相同的主体和任务；只有此反向链接因位置而异。

运行器契约：

1. 在运行任何先决条件检查之前记录 `Start (UTC)`。它是第一个动作。
2. 按 spec 顺序执行每个任务。成功时勾选框；失败时记录出了什么问题。
3. 在 Verdict 行确定之后，记录 `End (UTC)`。
4. 计算 `Duration = End - Start`，格式为 HH:MM:SS。
   是整个测试的实际耗时（先决条件 + reset + run + verify），而不仅仅是 API 客户端调用。
5. 用对 LLM API tokens 消耗的最佳估算填写 `Input tokens` 和 `Output tokens`。
   如果无法获得确切数字则留空。不要凭空捏造。
6. 编写 Result 摘要段落和 Verdict（PASS 或 FAIL）。
7. 在"Additional tasks I did"下记录在 spec 之外所做的任何事情。

此模板在结构上镜像 tasks-template.md（相同的章节和字段）；
两者一起漂移，因此在同一个变更中编辑匹配的 tasks-template。
spec 反向链接深度是唯一的故意差异。
-->

## Tasks

### Prerequisites

- [ ]

### Reset state

- [ ]

### Run

- [ ]

### Expected

- [ ]

### Verdict

- [ ] Verdict: PASS / FAIL（删除错误的那个）

## Result summary

<!-- 一段锚定到 Expected 断言的叙述。在此行上方编写；填写下面的指标。 -->

Input tokens:

Output tokens:

Start (UTC):

End (UTC):

Duration:

---

## Additional tasks I did