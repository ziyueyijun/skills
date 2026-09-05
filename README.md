# skills

ziyueyijun 的 AI agent 技能合集,基于开放 agent skills 生态([skills.sh](https://skills.sh)),兼容 Claude Code、Codex、Cursor 等主流 agent。

## 一条命令安装全部技能

```bash
npx skills add ziyueyijun/skills
```

### 装到全局(所有项目可用)

```bash
npx skills add ziyueyijun/skills -g
```

### 只装单个技能

```bash
npx skills add ziyueyijun/skills@<技能名>
```

## 技能列表

<!-- skills-table:start -->
| 技能 | 说明 | 上游来源 |
|------|------|----------|
| `ask-matt` | 询问哪个技能或流程适合当前场景:本仓库技能的「路由器」。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `code-review` | 按两轴审查自某基点以来的变更:是否符合仓库规范(含 Fowler 坏味道基线)、是否忠实实现源 issue/spec。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `codebase-design` | 设计深模块(deep module)的共享词汇:设计或改进模块接口、寻找深化机会、确定接缝位置、提升可测试性与 AI 可导航性。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `diagnosing-bugs` | 硬 bug 与性能回退的诊断循环:建立可复现反馈环、最小化、假设、插桩、修复、回归测试。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `domain-modeling` | 构建并打磨项目领域模型:讨论代码库术语、编写或编辑 CONTEXT.md、记录 ADR 时使用。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `find-skills` | 帮助查找并安装开放 agent 技能生态中的技能:回答「有没有做 X 的技能」「帮我找 X 技能」等需求。 | [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| `frontend-design` | 为新建或重塑 UI 提供有辨识度、有意图的视觉设计指导:美学方向、排版,避免模板化默认样式。 | [anthropics/skills](https://github.com/anthropics/skills) |
| `git-guardrails-claude-code` | 为 Claude Code 配置 hooks,在危险 git 命令(push、reset --hard、clean、branch -D 等)执行… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `grill-me` | 用穷追不舍的提问把方案或设计想透彻(grill 系技能的手动入口)。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `grill-with-docs` | grill 式追问的同时沉淀文档:顺带生成 ADR 与术语表,共建项目领域语言。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `grilling` | 对方案、决策、想法穷追不舍地提问以压力测试思路;grill-me、triage、wayfinder 等共用的底层原语。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `handoff` | 把当前对话压缩成一份交接文档,供另一个 agent 接手继续。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `implement` | 按 spec 或一组 ticket 实现一块工作。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `improve-codebase-architecture` | 扫描代码库寻找「深化模块」机会并输出可视化 HTML 报告,再对选中项逐一 grill。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `prototype` | 做一次性原型回答设计问题:状态或逻辑用单个共享 HTML,UI 探索用可切换的多方案变体。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `research` | 以高信任一手来源调研问题,结论写成带引用的 Markdown 文件入库,可由后台 agent 执行。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `resolving-merge-conflicts` | 逐 hunk 解决进行中的 git merge/rebase 冲突,按意图回溯冲突双方源头,完成后收尾(不 abort)。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `setup-matt-pocock-skills` | 为工程技能配置仓库:issue 追踪器、triage 标签词表、领域文档布局;跑整套流程前先运行一次。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `setup-pre-commit` | 在仓库配置 Husky 预提交钩子:lint-staged(Prettier)+ 类型检查 + 测试。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `setup-ts-deep-modules` | 在 TS 仓库接入 dependency-cruiser,让每个包成为深模块:实现藏进子目录、仅能经接口访问。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `skill-creator` | 创建、修改与优化技能并评测性能:从零写技能、跑 eval 测试、方差分析基准、优化描述提升触发准确率。 | [anthropics/skills](https://github.com/anthropics/skills) |
| `tdd` | 测试驱动开发:先写失败测试再修复(red-green-refactor),一次一个垂直切片。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `to-spec` | 把当前对话综合成 spec 发布到项目 issue 追踪器:不追问,只整理已讨论的内容。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `to-tickets` | 把计划、spec 或当前对话拆成一组「曳光弹」式 ticket,声明各自阻塞边,落到本地文件或追踪器。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `triage` | 用状态机推动 issue 与外部 PR 走 triage 流程:分类、核验、必要时 grill、写出 agent 可执行的简报。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `wayfinder` | 把超出单会话容量的大工程规划成共享的「决策 ticket 地图」,逐个解决直到路径清晰。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `wizard` | 生成交互式 bash 向导,引导人类完成只有他们能做的步骤:基础设施、凭据、CI 机密、陌生后台或一次性迁移。 | [mattpocock/skills](https://github.com/mattpocock/skills) |
<!-- skills-table:end -->

> 技能表由 [tools/sync-skills.sh](tools/sync-skills.sh) 自动维护,请勿手改标记区间内内容。

## 目录结构

- `skills/<技能名>/SKILL.md` — 发布布局,`npx skills add ziyueyijun/skills` 可自动发现
- `.agents/skills/`、`.claude/skills/` — 安装态真实副本(clone 后开箱即用)
- `rules/AGENTS.zh.md` — 通用 agent 规则(证据诚实、安全底线、工作方式)
- `tools/sync-skills.sh` + `tools/update_readme.py` — 镜像同步与技能表自动更新
- `skills-lock.json` — 技能来源记录(README 表格的数据源)

## 通用规则

[rules/AGENTS.zh.md](rules/AGENTS.zh.md) 是一份可直接使用的 agent 通用规则(核心原则:不编造、先证据;含安全与破坏性操作底线、冲突裁决、运行模式等)。「底线」建议全盘保留,「偏好」可按需裁剪。

```bash
# Claude Code:全局生效
cp rules/AGENTS.zh.md ~/.claude/CLAUDE.md
# 或放入单个项目根目录,命名为 CLAUDE.md 或 AGENTS.md
```

## 许可

根目录 MIT License 适用于本仓库自有的编排内容;各技能目录保留各自上游的 LICENSE 文件。`skills/` 下的 mattpocock 系技能来自 [mattpocock/skills](https://github.com/mattpocock/skills),Copyright (c) 2026 Matt Pocock,MIT License 发布。
