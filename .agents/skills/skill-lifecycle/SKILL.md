---
name: skill-lifecycle
description: >-
  Skill lifecycle advisor: judge whether a hard-won solution deserves to become
  a reusable skill, and keep existing skills from going stale as requirements
  drift. Use whenever a task wraps up after solving a genuinely difficult
  problem — long debugging detours, surprising failure modes, multi-step
  procedures with non-obvious pitfalls — or when the user hints they will hit
  the same problem again ("we'll run into this again", "save this workflow"),
  even if the user never mentions skills. Also use when an existing skill's
  steps conflict with the current requirement, or the user corrects a procedure
  a skill prescribes. Evaluate skill-worthiness against explicit criteria and,
  when warranted, propose the skill with a concrete scope and pitfalls list —
  or propose a concrete update to the existing skill. Proposes only: creating
  or editing skill files is the user's call; point to the skill-creator
  workflow for full creation.
---

# 技能生命周期顾问(只提议,不代劳)

一份复杂的解法如果只留在会话里,下周就蒸发;一份过期的技能如果没人指出,会持续误导以后的每次执行。你的价值是在**恰当的时机用一句提议把它捞住**——提议本身几秒钟,决定权永远在用户。

判断要克制:提议泛滥比从不提议更糟,它会让用户学会无视你。拿不准时,偏向沉默,而非打扰。

## 何时进入本流程

- 任务收尾、汇报成果时:刚解决了一个困难问题。
- 用户话里有"以后还会遇到""下次怎么办""这流程值得留下来"之类的暗示。
- 用户纠正了某个技能的执行步骤,或当前需求与某技能流程冲突(执行时绕开了技能步骤也算)。
- 用户直接问"这个问题值得做成技能吗""技能要不要更新"。

无人值守(定时任务、后台 agent)绝不主动提议——那是打扰。

## 流程 A:复杂问题解决后,评估是否值得沉淀

先过三条判据,**全部满足才提议**:

1. **有可复现的复杂度**:多步骤(大致 >5 步)或绕了远路(调试兜圈子、意外失败模式、多次重试),且解法里含**非显然的坑或顺序敏感步骤**——坑一旦写下来,下次就是现成的跳坑板,这是技能最有价值的部分。步骤多但无坑的纯体力活,优先级低。
2. **预期会再遇到**:用户明说还会遇到、该领域是长期工作、或过往记忆里已有同类问题。若只是本次项目的一次性事件 → 不提议建技能;若其中有值得留存的偏好或事实,该进的是记忆,不是技能——记忆存"事实与偏好",技能存"可重复执行的过程"。
3. **现有技能未覆盖**:快速查重——本次会话的可用技能列表、`~/.claude/skills`、项目 `.claude/skills` 与 `.agents/skills`。有近似技能 → 不新建,改走流程 B,提议"并入/补进现有技能"。

**不值得的典型信号**(此时闭嘴或一句话带过,不啰嗦):一次性排查(如"环境变量拼写错"、某个报错查出来即改)、纯事实问答、步骤简单且无坑、已有技能覆盖。

满足判据 → 把提议放在任务汇报的末尾,压在一两屏内,不打断主流程:

```text
💡 建议沉淀成技能 `候选名`(值得:命中判据①多步骤含坑 / ②还会再遇到 / ③现有技能无覆盖)
- 触发场景:什么时候会用到(用户会怎么说)
- 范围:技能做什么、不做什么——保持通用,剔掉本项目特定细节
- 关键步骤:3–6 条主干
- 最容易踩的坑:2–4 条,从这次经历提炼
- 重叠检查:与现有技能无重叠(若有,改为"建议并入 X 技能")
- 下一步:同意的话运行 /skill-creator 起草并迭代;本技能不代写文件
```

用户拒绝 → 尊重,不再坚持。同类提议连续被拒 ≥2 次 → 这个方向不值得反复打扰,停止提议。

## 流程 B:技能与需求脱节 → 提议更新(或退役)

触发情境:用户纠正执行步骤、需求变化使技能流程与实际做法冲突、执行时发现技能步骤已过时。

先判断是**一次性变通还是长期变化**——这是更新与否的闸门:

- **一次性的**(这次环境/项目特有)→ 说明差异即可,**不改技能**。把单次特例写进技能是技能腐化的主因:技能应保持通用层,新变体最多作为示例沉淀,而不是写死进流程。
- **长期变化**(会复现、是该领域的新常态)→ 提议更新,写清三点:差异(技能哪一段与现状冲突,引用到小节)、建议(改成什么、为什么)、出路(优先"更新本技能"或"并入其他技能"而非新建——技能碎片化比技能缺失更难收拾)。
- **已被完全取代或无法修复** → 提议删除或归档,理由一句话。

提议同样放在汇报末尾、用会话当前语言,格式从简:

```text
💡 技能 `名字` 需要更新(原因:××已变化,照旧步骤会做错)
- 过时处:××节(第×步)
- 改为:××
- 判断依据:这是长期变化(会复现),非一次性变通;已查无重叠技能
- 执行:确认后我再改 SKILL.md;若在本仓库还须跑同步脚本镜像
```

用户明确说"改"才动文件;修改遵守技能所在仓库的发布约定。用户没表态,只汇报、不动笔。

## 为什么只提议、不直接做

建技能是一种约定,归属权在用户:反复替用户拍板会让他烦,草率的半成品入库存下去只会变成下一个"待更新的旧技能"。完整工程化(起草、测试用例、迭代)已由 skill-creator 承担,本技能不与它重复——它的工作是发现时机、讲清理由,把选择权和执行权都留在用户手里。

提案输出语言跟随当次会话语言。
