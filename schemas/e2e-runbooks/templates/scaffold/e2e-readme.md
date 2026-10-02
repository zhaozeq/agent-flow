# 端到端能力测试

本项目的手动/AI 可运行 e2e 套件。每个测试针对实时栈端到端地执行一项能力，并仅断言**可观察行为**：HTTP 状态码、响应体内容、后台服务（数据库、对象存储、向量存储、缓存）中的持久化状态。日志是诊断性的，不是通过标准。

## 这里有什么

```text
e2e/
├── README.md                            # 此文件
├── fixtures/                            # 测试上传的金丝雀输入
│   └── README.md
└── testing/                             # 编号的 spec + templates/ + runs/
    ├── README.md
    ├── 1-<capability>-test.md           # 不可变 spec
    ├── 2-<capability>-test.md
    ├── templates/                       # 不可变运行记录模板，每个 spec 一个
    │   ├── README.md
    │   ├── 1-<capability>-tasks.template.md
    │   └── 2-<capability>-tasks.template.md
    └── runs/
        ├── README.md
        └── <UTC-timestamp>_<N>-<capability>-tasks.md   # 每个执行的测试一个（被 gitignore）
```

测试按设置成本编号前缀。`1` 需要的最少，较大的数字需要更多。此目录中 `testing/` 下的每个 spec 在 `testing/templates/` 中都有一个配对的 tasks-template，运行器将其复制到 `testing/runs/` 中，并带有扫描时间戳，在执行时逐个勾选复选框，并填充结果、token 使用和实际耗时。

## 流程

1. 读取位于 `testing/{N}-<capability>-test.md` 的 spec。
2. 将 `testing/templates/{N}-<capability>-tasks.template.md` 复制到
   `testing/runs/<UTC-timestamp>_{N}-<capability>-tasks.md`。
3. 将 `Start (UTC)` 记录为第一个动作。
4. 执行先决条件 → 重置状态 → 运行 → 期望。边走边勾选框。
5. 记录 `End (UTC)`，将 Duration 计算为 HH:MM:SS。
6. 填写 Result summary、Verdict 以及 "Additional tasks I did" 下任何 spec 外的操作。

完整方法论见 [Lukk17/agent-standards](https://github.com/Lukk17/agent-standards/tree/master/.agents/skills/e2e-runbooks) 中的 `e2e-runbooks` 技能。

## API 客户端

每个项目选择一个客户端并一致地用于所有测试。推荐的默认值：Bruno CLI、hurl 或最简单情况下的纯 curl。在项目的主 README 中记录项目的选择；此文件是通用的。

## 任何测试之前的先决条件

每个单独的 spec 列出其自己的具体先决条件检查。所有测试共同的是：

1. 被测服务在其绑定的端口上可达。
2. 后台服务（DB、缓存、向量存储、对象存储、MCP 服务器如适用）已启动。
3. 选择的 API 客户端已安装。

如果服务发出启动就绪横幅（参见 `coding-standards` 技能的规范约定），请在扫描开始时检查一次横幅。
外部依赖项下任何 `[FAILED]` 行都会阻止扫描。

## 添加新测试

使用 e2e-runbooks schema 创建变更：

```bash
openspec new change "add-<capability>-test" --schema e2e-runbooks
```

然后用 `/opsx:propose` 驱动它（如果 `openspec/config.yaml` 中设置了 `default_schema: e2e-runbooks`）。
该 schema 指导 proposal → test-spec → tasks-template → run。
或者，不使用 OpenSpec，按照 `e2e-runbooks` 技能中的方法论手动以常规形式编写三个文件。