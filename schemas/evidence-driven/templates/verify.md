# Verify: <变更名称>

<!-- P0 正式审计；P1/P2 的证据留在 tasks，不生成本文件 -->
<!-- apply 完成后产出；没有记录测试运行的 verify 不可能 PASS -->

## Task Completion

- tasks.md 全部勾选：<!-- 是/否 -->
- 遗留 `- [ ]` 项及原因：<!-- 无则填「无」 -->

## Coverage Audit（阻断项）

- test-plan/tasks 的覆盖记录对应真实测试或登记 N/A 且机械校验已跑：<!-- 是/否 -->
- 从 specs 反向核对台账/内联映射或逐任务验收，无遗漏/过期场景，移除/改名也有验证：<!-- 是/否 -->
- changed 有 red→green；baseline/N/A 最终重跑通过，无 pending：<!-- 是/否 -->
- 相关回归及项目约定的完整检查通过，无本次新增的无理由跳过：<!-- 是/否；记录既有 skip 基线 -->
- 无缺少 REMOVED 需求的测试削弱/删除：<!-- 是/否 -->

## Review Integrity

<!-- 仅当本级别 flow 含 review；否则删除本节 -->
- VERDICT 为 APPROVE（或 APPROVE_WITH_CHANGES 且 CHANGES_APPLIED: yes）：<!-- 是/否 -->
- 输入文件集合与 SHA-256 匹配最新经复核的快照：<!-- 是/否 -->
- 所有发现已修复或经复核申诉：<!-- 是/否 -->

## Decision Distillation

<!-- 长期决策均有仓库级 ADR，design 对应一致；无长期决策写明不适用理由 -->

## Evidence

<!-- 最终运行：时间、环境/工作树状态、确切命令、退出码、通过/失败/跳过计数及必要日志 -->

```
$ <命令>
<结果摘要>
```

## Delivery Status

<!-- 已提交：commit 范围 首SHA..尾SHA；未提交：当前状态 + 谁将提交。不得为满足本节强行提交 -->

## Lessons Learned

<!-- 3-5 条：计划偏差、意外难点、被推翻的假设、做得好的；没有就删除本节 -->

## Decision

<!-- 输出唯一机器可读行；阻断问题不能降成 warning；agent/CI 负责内容检查 -->

DECISION: <!-- PASS | PASS_WITH_WARNINGS | FAIL -->
