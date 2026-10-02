# e2e 测试指南

独立的演练，AI agent（或人类）可以针对实时栈端到端执行。
此目录中的每个 `<N>-<capability>-test.md` spec 都通过其 API 客户端调用驱动一项能力，
具有明确的先决条件检查、重置命令、运行步骤和预期结果。
配对的运行记录模板位于 `templates/` 子目录中；已执行的运行记录落在 `runs/` 中。

## 格式

每个 `<N>-<capability>-test.md` 文件是一个测试的**不可变 spec**，并使用相同的固定模板。

1. **What this verifies.** 行为列表。
2. **Prerequisites.** 运行器在开始之前执行的具体检查命令。每个命令是它自己的代码块；围绕它的散文说明成功是什么样。
3. **Reset state.** 每个代码块一个命令，按顺序执行，以擦除状态使测试可重现。如果适用，使用 "None. This test does not write persisted state."。
5. **Run.** 一个或多个带编号的步骤。每个步骤是一次 API 客户端调用。步骤在继续之前等待成功响应。
5. **Expected.** 在每个步骤之后验证的可观察行为断言：HTTP 状态码、响应体形状和内容、持久化状态。**不是**日志子串。
6. **Fixtures.** 测试读取的本地文件路径。

每个 spec 在 `templates/` 子目录中都有一个匹配的 `<N>-<capability>-tasks.template.md` — 一个运行的**复选框模板**。运行器从不直接编辑 spec 或模板。在开始运行之前，它将模板从 `templates/` 复制到 `runs/` 中并带有带时间戳的文件名，在进行过程中勾选框，填写 Result summary 和 Verdict，并在"Additional tasks I did"下记录在 spec 之外所做的任何事情。完整的运行器契约见 [runs/README.md](runs/README.md)。

## 测试顺序

按设置成本编号（最低优先）。逐步执行时先运行最早的；每个都是独立的，因此任何一个都可以单独运行。

## 横切约定

通过标准仅是可观察行为：HTTP 状态、响应体内容、后台服务中的持久化状态。日志是诊断性的，不是权威的。日志行跨版本变化，并非在每个运行器的 shell 中都可见。如果行为断言失败，则服务日志的尾部是下一个诊断步骤，而不是通过标准。

## 添加新测试

如果设置了 OpenSpec，请运行 `openspec new change "add-<capability>-test" --schema e2e-runbooks`（或当配置了 `default_schema: e2e-runbooks` 时使用 `/opsx:propose`）。否则按照伴随技能中的方法论手动编写 spec + tasks-template 对。