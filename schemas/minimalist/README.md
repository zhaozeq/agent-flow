# 极简 OpenSpec Schema

`minimalist` 用于通过直接的 `specs -> tasks` 流快速构建。

- 良好场景：登陆页面和具有太多技术设计决策的简单应用。
- 不适合的场景：具有多层、数据库工作和更广泛架构关注的完整应用。

## 安装（复制/粘贴）

对根 `README.md` 单行安装命令使用：
- `SCHEMA="minimalist"`

## 激活

在 `openspec/config.yaml` 中设置：

```yaml
schema: minimalist
```

## Spec 格式

在此 schema 中编写 `specs` artifact 时：
- 将每个需求编写为用户故事：
  `As a <role>, I want <capability>, so that <benefit>.`
- 使用 Gherkin 结构编写验收标准：
  `Given ...`、`When ...`、`Then ...`

## 关联技能

此 schema 在 `skills.txt` 中声明其伴随技能；它们由 `AGENT_INSTALL.md` 的第 6 步自动安装到 `.agents/skills/`，来源是 [intent-driven-dev/skills](https://github.com/intent-driven-dev/skills)。

- `openspec-git-discipline` — OpenSpec propose/apply/archive 工作流的 git 卫生。

更多 schema，请参考 https://github.com/intent-driven-dev/openspec-schemas。