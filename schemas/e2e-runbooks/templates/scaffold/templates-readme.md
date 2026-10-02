# e2e 运行记录模板

每个 spec 一个 `<N>-<capability>-tasks.template.md`。每个都是运行器在每次执行开始时复制到 `../runs/` 中的**复选框模板**。

## 与 spec 的关系

Spec 本身（`../<N>-<capability>-test.md`）位于上一级目录，直接在 `testing/` 下。
此 `templates/` 目录仅保存镜像它们的运行记录模板 — 每个 spec 一个模板，共享相同的 `{N}` 前缀和 `{capability}` 名称。

## 契约

1. 模板在运行之间**不可变**。运行器从不就地编辑它们。
2. 每个模板将其 spec 的 Prerequisites、Reset、Run 和 Expected 项镜像为复选框，加上 Verdict 复选框、Result summary 块（Input tokens、Output tokens、Start (UTC)、End (UTC)、Duration）和一个"Additional tasks I did"章节。
3. 要运行测试，请将匹配的模板复制到 `../runs/` 并带有 UTC 时间戳前缀
   （`<UTC-timestamp>_<N>-<capability>-tasks.md`），然后在该副本中勾选框并填写结果 — 而不是此处。

完整的运行器契约见 [../runs/README.md](../runs/README.md)。