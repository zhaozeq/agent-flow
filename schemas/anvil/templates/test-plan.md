## Test Plan

<!-- specs/ 中的每个场景映射到具体测试。映射是 -->
<!-- 下限，不是上限：额外的测试受欢迎，但此处不需要条目。 -->
<!-- 实时账本：在 apply 期间，每行在其测试通过时从 🔴 red 翻转为 🟢 green。 -->
<!-- verify 在任何留下的红色行上阻塞。 -->

| Requirement | Scenario | Test File | Test Name | Initial State |
|-------------|----------|-----------|-----------|---------------|
| specs/<cap>/spec.md → <Requirement Name> | <Scenario Name> | src/tests/... | test_<name> | 🔴 red |
<!-- 不可执行的变更（docs/config/schema）：映射到机械检查。 -->
<!-- | specs/<cap>/spec.md → <Requirement Name> | <Scenario Name> | openspec schema validate anvil | schema-validates | N/A — non-executable | -->

## Coverage Notes

<!-- 有关测试基础设施、共享 fixture 或所需测试实用程序的任何备注。 -->
<!-- 对于 N/A — non-executable 条目，解释为什么不存在代码测试并命名门禁变更的检查。 -->