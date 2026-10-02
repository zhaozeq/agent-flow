# {capability}：运行任务模板

Spec: [`{N}-{capability}-test.md`]({N}-{capability}-test.md)

在开始运行之前将此文件复制到 `runs/<UTC-timestamp>_{N}-{capability}-tasks.md`。
边走边勾选框。在 **Additional tasks I did** 下添加你在 spec 之外所做的任何事情。

## Tasks

### Prerequisites

<!-- 镜像 spec 的 Prerequisites 章节，每个检查一个复选框。 -->

- [ ]
- [ ]

### Reset state

<!-- 镜像 Reset state 章节，每个命令一个复选框。
如果 spec 写"None"，则跳过。 -->

- [ ]

### Run

<!-- 镜像 Run 章节，每个带编号的步骤一个复选框。 -->

- [ ]

### Expected

<!-- 镜像 Expected 章节，每个断言一个复选框。 -->

- [ ]
- [ ]

### Verdict

- [ ] Verdict: PASS / FAIL（删除错误的那个）

## Result summary

<!-- 一段关于此次运行期间发生的事情的叙述。锚定到 Expected 断言。
将此摘要写在此行上方，然后填写下面的字段。 -->

Input tokens:

Output tokens:

Start (UTC):

End (UTC):

Duration:

---

## Additional tasks I did

<!-- 可选。列出 spec 之外的任何内容，例如诊断 curl、手动日志检查、使用不同输入的重试。
如果没有额外内容则留空。 -->