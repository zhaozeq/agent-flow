# Test Plan: <变更名称>

<!-- 本档有 review 时，前置为有效 APPROVE 或 APPROVE_WITH_CHANGES 且 CHANGES_APPLIED: yes -->
<!-- specs/ 中每个 #### Scenario 必须映射到至少一个具名测试；未映射场景是阻断性缺陷 -->
<!-- 非可执行变更（文档/配置/schema）：映射到等价机械校验，状态 N/A — non-executable 并附理由 -->
<!-- 活台账：changed 记录 red→green，baseline 重跑，N/A 机械检查通过；未执行标 pending -->

## Coverage Ledger

| Requirement | Scenario / Delta | Test File / Command | Test Name / Check | 类型 | State | Evidence |
|-------------|------------------|---------------------|-------------------|------|-------|----------|
| specs/<cap>/spec.md → <需求名> | <场景/移除/改名> | <测试文件或相关机械命令> | <具名测试/检查项> | <changed/baseline/non-executable> | pending | <真实运行后填写> |

## Coverage Notes

<!-- baseline/N/A 理由、REMOVED/RENAMED 验证；额外测试可不登记，不能替代场景覆盖 -->
