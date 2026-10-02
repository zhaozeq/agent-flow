# Review: <变更名称>

<!-- design 后统一评审 proposal/specs/design，批准前不形成 tasks；P2 不生成本文件 -->
<!-- 独立新上下文；P0 加强攻击面，跨模型仅为获准时的可选增强；仅允许写本文件 -->

## Review Metadata

- **Round**: 1
- **Reviewer**: <fresh-context | cross-model:<cli>>
- **Schema**: <实际 schema 名称>
Tier: <P0|P1|P2>
- **Timing**: once
- **上轮裁决摘要**: <!-- 首轮省略 -->

## Reviewed Snapshot

<!-- 所有 proposal/design/specs 输入的相对路径与 SHA-256；检查 specs 文件集合无新增/删除 -->
<!-- 裁决后修改须复核并刷新快照；包括应用必改项、文字修正与 ADR 对应登记 -->

| File | SHA-256 |
|------|---------|
| proposal.md | <hash> |
| design.md | <hash> |
| specs/<capability>/spec.md | <hash> |

## Findings

<!-- 每条发现标级别：🔴 Critical / 🟠 Moderate / 💡 Suggestion -->
<!-- 攻击面：未言明假设、缺失失败场景、范围蔓延、更廉价替代、设计与规范矛盾、
     不可断言的 THEN、安全（信任边界/鉴权/注入） -->

### F1 — <Critical/Moderate/Suggestion>: <发现标题>

<证据 + 影响 + 建议修法 + 处置/复核状态>

## Required Changes

<!-- APPROVE_WITH_CHANGES 时逐条列出必改项；其他裁决留空 -->

## Rebuttals

<!-- Critical/Moderate 申诉必须经评审者认可；未关闭的阻断项禁止进入 tasks -->

## Verdict

<!-- 输出唯一机器可读行；文件存在不代表门禁通过，内容检查由 agent/CI 执行 -->

VERDICT: <!-- APPROVE | APPROVE_WITH_CHANGES | REVISE -->

CHANGES_APPLIED: <!-- APPROVE_WITH_CHANGES 时输出 no/yes；其余填 n/a -->
