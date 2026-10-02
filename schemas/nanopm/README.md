# nanopm × OpenSpec schema

为 [OpenSpec](https://openspec.dev) 添加 nanopm 的 PM 流水线作为上游规划层的社区 schema。

## 安装

将此 schema 复制到你的项目：

```bash
mkdir -p openspec/schemas/nanopm
curl -fsSL https://raw.githubusercontent.com/nmrtn/nanopm/main/openspec-schema/schema.yaml \
  -o openspec/schemas/nanopm/schema.yaml
mkdir -p openspec/schemas/nanopm/templates
for f in proposal spec design tasks; do
  curl -fsSL https://raw.githubusercontent.com/nmrtn/nanopm/main/openspec-schema/templates/${f}.md \
    -o openspec/schemas/nanopm/templates/${f}.md
done
```

然后在 `openspec/config.yaml` 中将其设置为默认值：

```yaml
schema: nanopm
```

或按命令使用：

```bash
openspec new change my-feature --schema nanopm
```

## 这新增了什么

`nanopm` schema 了解 nanopm 的输出 artifact。在生成任何 artifact 时，如果存在 `.nanopm/` 则从中读取：

- `proposal.md` 从 `.nanopm/CHALLENGES.md` + `.nanopm/prds/<feature>.md` 读取
- `design.md` 从 `.nanopm/STRATEGY.md` 读取
- `tasks.md` 如果 `/pm-breakdown` 已运行，则从 `.nanopm/tasks/<feature>.md` 读取
- `specs/` 将 PRD 需求转换为 SHALL 声明

## 完整链路

```
/pm-challenge-me → 挑战产品思维
/pm-strategy     → 定义战略定位
/pm-roadmap      → 优先排序要构建的内容
/pm-prd          → 编写 PRD
/pm-breakdown    → 分解为任务（可选地写入 openspec/changes/<feature>/）

openspec new change <feature> --schema nanopm
/opsx:apply      → 实现
```

## 两层，一个工作流

| 层 | 工具 | 回答 |
|-------|------|---------|
| PM | nanopm | 为什么构建、构建什么、为谁构建、战略、路线图 |
| 工程 | OpenSpec | 如何构建、需求是什么、任务是什么 |