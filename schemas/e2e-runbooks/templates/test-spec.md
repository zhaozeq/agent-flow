# {capability}：e2e 测试

## What this verifies

<!-- 项目符号列表。从 proposal 原样复制。仅行为断言。 -->

-
-

## Prerequisites

<!-- 运行器在开始之前执行的具体检查命令。每个命令在自己的围栏块中。
围绕块的散文说明成功是什么样。 -->

检查 API client 工具已安装。

```bash
<command>
```

期望 <success criterion>。

<每个先决条件重复>

## Reset state

<!-- 每个代码块一个命令，按顺序，以擦除状态使测试可重现。
如果不适用，使用 "None. This test does not write persisted state."。 -->

```bash
<command>
```

## Run

<!-- 一个或多个带编号的 API 客户端 CLI 调用。多步骤测试指示运行器
在继续之前等待成功响应（HTTP 200 或等效）。 -->

发送请求并在移至 Expected 部分之前等待响应。

```bash
<command>
```

## Expected

<!-- 仅可观察断言。HTTP 状态、响应体内容、后台服务中的持久化状态。不要日志子串。 -->

输出显示 HTTP 200。

响应体的 `<field>` 包含 <expected content>。

## Fixtures

<!-- 测试读取的本地文件路径。每个必须具有模型无法记住的独特金丝雀内容。如果没有则为 "None."。 -->

- `<path>` — <金丝雀内容的一行描述>

## Concurrency

- **Mutates:** <从 proposal 的 Concurrency profile 原样复制 Mutates 行。>
- **Conflicts with:** <从 proposal 的 Concurrency profile 原样复制 Conflicts with 行。>
- **Serial:** <从 proposal 的 Concurrency profile 原样复制 Serial 值。>