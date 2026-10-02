# e2e 测试运行

每个 e2e 测试运行在此处放置匹配的 `*-tasks.template.md` 的已填写副本，命名为
`<UTC-timestamp>_<N>-<capability>-tasks.md`。此 README 被跟踪；运行文件本身默认被 gitignore。

## 契约

1. Spec（`../<N>-<capability>-test.md`）在运行之间**不可变**。运行器从不编辑它们。
2. 模板（`../templates/<N>-<capability>-tasks.template.md`）也**不可变**。它们为该测试定义了复选框列表。
3. 每个运行通过将相关模板从 `../templates/` 复制到此目录并带有 UTC 时间戳前缀来开始。
   运行器在完成每个步骤时勾选框，并在最后填写 **Result summary** 和 **Additional tasks I did**。

## 命名

```text
2026-05-12T18-15-00_1-<capability>-tasks.md
2026-05-12T18-15-00_2-<capability>-tasks.md
2026-05-12T18-15-00_3-<capability>-tasks.md
```

使用 ISO-8601 UTC，冒号替换为连字符，以便文件名在 Windows / macOS / Linux 上对文件系统安全。
将一次扫描中的所有测试分组在同一时间戳下；一个时间戳 = 一次完整的 e2e 扫描。

## 运行器步骤

1. 读取测试的 spec。
2. 将模板从 `../templates/` 复制到此目录，并带有带时间戳的文件名。
3. **记录 `Start (UTC)`** 作为第一个动作。在先决条件检查开始之前的实际瞬间。
4. 按顺序执行每个任务。成功时勾选框；失败时记录出了什么问题。
5. 在 **Verdict** 行确定之后，**记录 `End (UTC)`**。在最后一个验证步骤之后的实际瞬间。
6. 计算 `Duration = End - Start` 并将其记录为 `HH:MM:SS`。
   是**整个测试**的实际耗时（先决条件 + reset + run + verify），
   而不仅仅是 API 客户端调用。
7. 用你对运行中消耗的 LLM API tokens 的最佳估算填写 **Input tokens** 和 **Output tokens**。
   如果无法获得确切数字则留空。不要凭空捏造。
8. 编写 **Result summary** 段落和 **Verdict**（PASS 或 FAIL）。
9. 如果在 spec 之外完成了任何步骤（额外的诊断、重试、手动检查），请在
   **Additional tasks I did** 下记录。

## Gitignore 策略

运行记录文件默认是短暂的（被 gitignore）。此 README 保持被跟踪。
通过将单个运行移到 `runs/<YYYY-MM>/` 子文件夹下并调整 .gitignore 例外，将单个运行提升为已提交的审计跟踪。