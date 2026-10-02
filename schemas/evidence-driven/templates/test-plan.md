# Test Plan: <变更名称>

<!-- 前置：review VERDICT 为 APPROVE，或 APPROVE_WITH_CHANGES 且 CHANGES_APPLIED: yes -->
<!-- specs/ 中每个 #### Scenario 必须映射到至少一个具名测试；未映射场景是阻断性缺陷 -->
<!-- 非可执行变更（文档/配置/schema）：映射到等价机械校验，状态 N/A — non-executable 并附理由 -->
<!-- 活台账：apply 期间测试通过后把 State 从 🔴 翻转为 🟢；verify 审计全绿 -->

## Coverage Ledger

| Requirement | Scenario | Test File | Test Name | State |
|-------------|----------|-----------|-----------|-------|
| specs/<cap>/spec.md → <需求名> | <场景名> | <测试文件路径> | <测试函数名> | 🔴 red |
| specs/<cap>/spec.md → <需求名> | <场景名> | <!-- 如 `openspec schema validate <name>` --> | <检查项> | N/A — non-executable |

## Coverage Notes

<!-- N/A 项的一行理由；额外测试（参数化/回归/内部单测）无需登记，但不能替代场景的具名测试 -->
