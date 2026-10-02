# anvil

一个 spec 驱动的 OpenSpec schema，驱动**测试驱动开发**和**对抗式评审门禁**，而无需从中提取的 crucible schema 的全部仪式。Crucible schema 目前正在重构中，将很快可用。

> **门禁的工作原理（先阅读此）。** OpenSpec 的 `requires:` 依赖关系仅强制 artifact *文件存在* — 不强制其内容。
> 此 schema 中的 REVISE 门禁、TDD 排序和"停止"先决条件是**对 agent 的指令**，而不是机械强制。
> 它们由遵循 schema 的编码 agent 遵守，而不是由 OpenSpec CLI 遵守。
> 要进行机械强制，请添加 CI/git-hook 检查（参见 [Enforcement](#enforcement)）。

## 流程

```
proposal → specs → design → review（对抗式门禁）→ test-plan → tasks → apply → verify
```

## 与默认 schema 的区别

| 方面 | OpenSpec 默认 | 此 schema (`anvil`) |
|--------|------------------------|------------------------------|
| 评审门禁 | 无 | 由独立上下文/模型进行的对抗式评审，指示 agent 阻断所有下游工作 |
| 测试规划 | 无 | 每个 spec 场景在 tasks 存在之前 1:1 映射到命名测试 |
| 任务结构 | 自由形式清单 | 每个场景的强制红绿重构排序 |
| Spec 严谨性 | 每个需求 ≥1 个场景 | 每个需求 ≥1 个 happy-path **和** ≥1 个失败/边缘场景 |
| Apply 纪律 | "处理任务" | 实现之前必须存在失败的测试；没有证据就没有完成 |
| 实施后 | 无 | 对 TDD 完整性、评审合规性和任务完成的正式验证 |

## Artifact

| Artifact | Generates | 目的 |
|----------|-----------|---------|
| `proposal` | proposal.md | 为什么需要此变更 |
| `specs` | specs/**/*.md | 系统应该做什么（可测试场景） |
| `design` | design.md | 如何实现（决策 + 理由） |
| `review` | review.md | 对抗式门禁 — 指示 agent 在 REVISE 上阻断下游工作 |
| `test-plan` | test-plan.md | 场景 → 测试映射（全部以 🔴 red 开始） |
| `tasks` | tasks.md | 红绿重构排序的清单 |
| `verify` | verify.md | TDD + 评审合规性的实施后证明 |

## 评审规则

- **永远不要**在编写 artifact 的同一上下文中进行自我评审
- 首选跨模型评审（第二个不同的模型评审工作）使用实际安装的任何 CLI — 不要假设特定的命令或标志
- 回退：相同模型、全新上下文子 agent（消除锚定）
- 如果生成的评审者出错或不可用，不要自我评审或捏造判定 — 回退到全新上下文子 agent，或**停止**并报告错误
- 评审者以只读方式检查所有内容（view/grep/glob），只能写自己的评审输出（`review.md`） — 永远不编辑评审下的 artifact、源代码或任何其他文件
- **数据局部性：** 跨模型评审者可能将 `proposal.md`/`design.md`/`specs/` 发送给外部提供者。仅使用你的团队已批准此代码库敏感度的模型；对于没有批准的外部模型的机密/受监管材料，请改为在本地评审（全新上下文子 agent）。如有疑问，请保持本地。
- 三个判定：**APPROVE**、**APPROVE WITH CHANGES**、**REVISE**
- REVISE 指示 agent 阻断所有内容，直到 artifact 修复并重新评审
- **严重性-判定一致性：** 任何未解决的 Critical 发现禁止 APPROVE — 具有 Critical 发现且 `VERDICT: APPROVE` 的评审本身就是无效的
- **陈旧性：** 判定仅涵盖评审的确切内容。之后编辑 `proposal.md`、`design.md` 或 `specs/`（除了应用列出的 Required Changes）会使判定无效并需要新的评审回合
- **反驳被裁决：** 作者对 Critical 或 Moderate 发现的反驳只有在评审者重新检查并接受后才算；只有 Suggestions 可由作者单独拒绝
- **有界循环：** 每次完整重新评审都会增加 `review.md` 中的回合计数器；在 2 次连续的 REVISE 回合后，agent 必须停止并上报给人类

## 强制

> [!IMPORTANT]
> **核心保证是建议性的，不是强制性的。** TDD 排序和对抗式评审门禁是*对 agent 的指令*，而不是仓库或 OpenSpec CLI 实质检查的内容。此捆绑包中**没有 CI、git hook 或验证脚本**。作者或 agent 可以在 `REVISE` 判定上生成 `test-plan.md`/`tasks.md`，在未应用的 `APPROVE_WITH_CHANGES` 上继续，跳过红绿重构，或在 `DECISION: FAIL` 上合并，此处没有任何东西会阻止他们。如果必须*保证*这些门禁，请添加机械检查。

要机械强制，请在你的 CI 或 pre-commit hook 中解析这些规范字段（而不是散文）：

- `review.md` — `VERDICT: APPROVE | APPROVE_WITH_CHANGES | REVISE`
- `review.md` — `CHANGES_APPLIED: yes | no | n/a`（`APPROVE_WITH_CHANGES` 的完成信号）
- `verify.md` — `DECISION: PASS | PASS_WITH_WARNINGS | FAIL`

**白名单成功，不要黑名单失败：** 仅在 `VERDICT: APPROVE`（或 `APPROVE_WITH_CHANGES` 且 `CHANGES_APPLIED: yes`）上继续，并且一旦 `tasks.md` 存在，则使用 `verify.md` 且 `DECISION: PASS`/`PASS_WITH_WARNINGS`。将缺失的文件或未填写的占位符视为阻断 — 没有批准不是批准。

最小示例（pre-commit hook 或 CI 步骤，从变更目录运行）：

```bash
#!/usr/bin/env bash
set -euo pipefail

verdict=$(grep -E '^VERDICT: ' review.md | tail -1 || true)
case "$verdict" in
  "VERDICT: APPROVE") ;;
  "VERDICT: APPROVE_WITH_CHANGES")
    grep -qx 'CHANGES_APPLIED: yes' review.md \
      || { echo "BLOCKED: required changes not applied"; exit 1; } ;;
  *) echo "BLOCKED: no approving verdict in review.md"; exit 1 ;;
esac

if [ -f tasks.md ]; then
  decision=$(grep -E '^DECISION: ' verify.md 2>/dev/null | tail -1 || true)
  case "$decision" in
    "DECISION: PASS"|"DECISION: PASS_WITH_WARNINGS") ;;
    *) echo "BLOCKED: no passing decision in verify.md"; exit 1 ;;
  esac
fi
```

此检查仅检查规范字段；它不会（也无法）验证评审实际上是对抗式的或测试实际上先运行红色 — 这些仍然由 agent 遵守。

## TDD 规则

- 每个 spec 场景映射到命名测试 — 下限，不是上限（额外的测试受欢迎，但永远不会替代场景的命名测试）
- 任务已排序：编写失败的测试 → 实现 → 重构
- 测试必须因正确的原因失败（不是导入/语法错误）
- `test-plan.md` 是实时覆盖率账本：行以 🔴 red 开始，在 apply 期间随其测试通过翻转为 🟢 green；`verify` 阻塞任何留下的红色行
- **Spec 漂移：** 如果实现揭示 spec 错误，agent 必须停止、修改 spec、重新运行评审（旧判定无效）、更新测试计划 — 永远不要静默编辑 spec 或削弱测试以匹配观察到的行为
- 没有任务在没有新的测试运行作为证据的情况下完成；最终的完整套件命令和结果摘要记录在 `verify.md` 中
- 验证检查：没有跳过的测试、没有削弱的断言、没有未经 REMOVED 需求删除的测试
- **不可执行的变更**（文档、config、纯 schema）免于代码测试：将每个场景映射到等效的机械检查（例如 `openspec schema validate`、linter、CI 作业）标记为 `N/A — non-executable`，并在 `verify` 中确认该检查通过。散文批准不合格。

## 使用

参见 [INSTALL.md](../../INSTALL.md) 将此 schema 安装到你的项目，然后使用 `openspec new change <name> --schema anvil` 选择它
（或在 `openspec/config.yaml` 中设置 `schema: anvil`）。

## 来源

从 crucible schema 提取。保留 TDD 纪律和对抗式评审；删除了 Superpowers 技能依赖、校验和固定、头脑风暴、棕地基线、回顾和 git 工作树编排。