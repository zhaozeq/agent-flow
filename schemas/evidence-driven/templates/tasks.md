# Tasks: <变更名称>

<!-- 机器可读行，必须保留：无 proposal 的级别这是唯一级别记录，CI 与 apply 均读取 -->
Tier: <!-- P0|P1|P2 -->

<!-- 前置（仅当本级别 flow 含 review）：review VERDICT 为 APPROVE，或 APPROVE_WITH_CHANGES 且 CHANGES_APPLIED: yes -->
<!-- 必须严格遵循复选框格式：`## 数字` 分组 + `- [ ] X.Y 描述`，apply 按此解析进度 -->
<!-- 每个任务自带验收方式（测试/命令/可观测行为/交付物）；排序深度按 flow-policy 的 tdd（mandatory/optional/none） -->

## 1. <分组名称>

<!-- P0/P1 的每组任务遵循 TDD 三段式：
- [ ] 1.1 编写失败测试 <test-plan 条目>（确认以正确原因失败）
- [ ] 1.2 实现 <行为> 使 1.1 通过
- [ ] 1.3 重构；全量测试保持绿色
-->

- [ ] 1.1 <任务描述；验收方式：…>
- [ ] 1.2 <任务描述；验收方式：…>

## 2. <分组名称>

- [ ] 2.1 <任务描述；验收方式：…>
