# 事件驱动 OpenSpec Schema

`event-driven` 适用于通过事件通信并在实现规划之前需要清晰的发现到 spec 工作流的系统。

主要参考：
- AsyncAPI: https://www.asyncapi.com/
- Event Storming: https://en.wikipedia.org/wiki/Event_storming

- 良好场景：以事件为中心的域、异步集成、pub/sub 系统，以及在编码前需要经验证的 AsyncAPI 契约的团队。
- 不适合的场景：`specs -> tasks` 就足够了的小型低风险变更，且不需要事件架构决策。

## 安装（复制/粘贴）

对根 `README.md` 单行安装命令使用：
- `SCHEMA="event-driven"`

## 激活

在 `openspec/config.yaml` 中设置：

```yaml
schema: event-driven
```

## 阶段门

Artifact 顺序：
`event-storming -> event-modeling -> specs -> design -> asyncapi -> tasks`

门控期望：
- `event-modeling` 必须使用来自 `event-storming` 的输出。
- `specs` 和 `design` 必须在 `asyncapi` 之前完成。
- `tasks` 仅在已审查的 `specs`、已审查的 `design` 和经验证的 AsyncAPI 文档（`asyncapi-cli validate asyncapi.yaml`）之后才规划。

## Mermaid 颜色图例

在 Mermaid 模板中使用显式的 `classDef` 和 `class` 赋值，以便颜色语义在渲染器之间保持稳定。

Event-storming 标准基线：
- 域事件：橙色（`event`）
- 命令：蓝色（`command`）
- 参与者/用户：黄色（`actor`）
- 策略/自动化：紫色家族（`policy`）
- 读模型/投影：绿色（`readModel`）

事件驱动 schema 映射说明：
- `event-modeling` 中的 `Trigger` 被视为 actor/user 泳道，应使用 `actor` 颜色映射。
- 在 event-modeling artifact 中首选 `Read Model` 节点标签，在 event-storming artifact 中使用 `Read Model/Projection` 标签；两者都映射到 `readModel`（绿色）。

## 关联技能

此 schema 在 `skills.txt` 中声明其伴随技能；它们由 `AGENT_INSTALL.md` 的第 6 步自动安装到 `.agents/skills/`，来源是 [intent-driven-dev/skills](https://github.com/intent-driven-dev/skills)。

- `c4-diagrams` — 使用 ASCII 或 Mermaid 的 C4 风格架构图。
- `glossary` — 在 artifact 之间保持领域/技术术语的一致性。
- `openspec-git-discipline` — OpenSpec propose/apply/archive 工作流的 git 卫生。

更多 schema，请参考 https://github.com/intent-driven-dev/openspec-schemas。