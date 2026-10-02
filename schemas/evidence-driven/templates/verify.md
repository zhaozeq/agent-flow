# Verify: <变更名称>

<!-- 深度按 flow-policy 的 verify_depth：minimal 只做 1/5 + Evidence + DECISION；full 全查 -->
<!-- apply 完成后产出；没有记录测试运行的 verify 不可能 PASS -->

## Task Completion

- tasks.md 全部勾选：<!-- 是/否 -->
- 遗留 `- [ ]` 项及原因：<!-- 无则填「无」 -->

## Coverage Audit（阻断项）

- test-plan 每条目对应真实测试或登记 N/A 且机械校验已跑：<!-- 是/否 -->
- 台账全绿（无 🔴 red）：<!-- 是/否 -->
- 全量测试套件通过、零跳过/挂起/注释测试：<!-- 是/否 -->
- 无缺少 REMOVED 需求的测试削弱/删除：<!-- 是/否 -->

## Review Integrity

<!-- 仅当本级别 flow 含 review；否则删除本节 -->
- VERDICT 为 APPROVE（或 APPROVE_WITH_CHANGES 且 CHANGES_APPLIED: yes）：<!-- 是/否 -->
- 裁决未失效（被评审文件在裁决后未变更）：<!-- 是/否 -->
- 所有发现已修复或经复核申诉：<!-- 是/否 -->

## Decision Distillation

<!-- 仅当本级别 adr 为 mandatory：design 中标注的长期决策 → adr/ 文件编号对应一致；否则删除或填「不适用」 -->

## Evidence

<!-- 最终全量测试运行：确切命令 + 结果摘要（通过/失败计数） -->

```
$ <命令>
<结果摘要>
```

## Delivery Status

<!-- 已提交：commit 范围 首SHA..尾SHA；未提交：当前状态 + 谁将提交。不得为满足本节强行提交 -->

## Lessons Learned

<!-- 3-5 条：计划偏差、意外难点、被推翻的假设、做得好的；没有就删除本节 -->

## Decision

<!-- 机器可读行必须逐字输出，CI 据此强制 -->

DECISION: <!-- PASS | PASS_WITH_WARNINGS | FAIL -->
