# skills

ziyueyijun 的 AI agent 技能合集。本仓库原创技能通过开放 agent skills 生态([skills.sh](https://skills.sh))发布,一条命令即可安装;在本仓库内,技能位于 `.claude/skills/`,打开 Claude Code 即自动加载。

**English version:** [README.md](README.md)

## 用 npx 安装技能

安装本仓库原创技能(当前为 `pbidea`、`powerbuilder`;[skills-lock.json](skills-lock.json) 中记录的上游技能按各自来源安装,不在此重复发布):

```bash
npx skills add ziyueyijun/skills
```

- 只列出可用技能不安装:`npx skills add ziyueyijun/skills -l`
- 只装单个技能:`npx skills add ziyueyijun/skills -s pbidea`
- 装到全局(所有项目可用):`npx skills add ziyueyijun/skills -g`

CLI 会把技能写入项目的 `.agents/skills/`,并为 Claude Code 及其支持的各 agent 建立符号链接。

## 更新技能

- 已安装技能想更新到最新版:在安装它的项目里运行 `npx skills update`(全局安装用 `npx skills update -g`);只更新某一个用 `npx skills update <技能名>`。
- 本仓库原创技能发布新版后,重新执行 `npx skills add ziyueyijun/skills`(或 `npx skills update`)即可拉到最新。

## 在本仓库内使用

- 在本目录打开 Claude Code:`.claude/skills/` 里的技能自动加载;手动触发技能(`disable-model-invocation`)以 `/技能名` 唤起。
- 未装 npx 的其他项目:把 `.claude/skills/<技能名>` 复制到目标项目的 `.claude/skills/`,或放入 `~/.claude/skills/`(所有项目可用)。技能自包含(仅 Python 内置库、无联网),复制目录即可。

## 技能列表

<!-- skills-table:start -->
### 手动触发(需 `/技能名` 或显式点名;不主动调用即零开销)

| 技能 | 说明 |
|------|------|
| `ask-matt` | 询问哪个技能或流程适合当前场景:本仓库技能的「路由器」。 |
| `setup-matt-pocock-skills` | 为工程技能配置仓库:issue 追踪器、triage 标签词表、领域文档布局;跑整套流程前先运行一次。 |
| `setup-ts-deep-modules` | 在 TS 仓库接入 dependency-cruiser,让每个包成为深模块:实现藏进子目录、仅能经接口访问。 |
| `wayfinder` | 把超出单会话容量的大工程规划成共享的「决策 ticket 地图」,逐个解决直到路径清晰。 |
| `grill-me` | 用穷追不舍的提问把方案或设计想透彻(grill 系技能的手动入口)。 |
| `grill-with-docs` | grill 式追问的同时沉淀文档:顺带生成 ADR 与术语表,共建项目领域语言。 |
| `to-spec` | 把当前对话综合成 spec 发布到项目 issue 追踪器:不追问,只整理已讨论的内容。 |
| `to-tickets` | 把计划、spec 或当前对话拆成一组「曳光弹」式 ticket,声明各自阻塞边,落到本地文件或追踪器。 |
| `implement` | 按 spec 或一组 ticket 实现一块工作。 |
| `handoff` | 把当前对话压缩成一份交接文档,供另一个 agent 接手继续。 |
| `triage` | 用状态机推动 issue 与外部 PR 走 triage 流程:分类、核验、必要时 grill、写出 agent 可执行的简报。 |
| `improve-codebase-architecture` | 扫描代码库寻找「深化模块」机会并输出可视化 HTML 报告,再对选中项逐一 grill。 |
| `pbidea` | PbIdea 框架 API 查询技能,由 /pbidea 手动触发:uo_json(JSON 解析/生成/与 DataWindow 互转)、uo… |
| `powerbuilder` | PowerBuilder 官方开发文档查询技能,由 /powerbuilder 手动触发:PowerScript 语言(语法/语句/事件/函数/… |
| `search` | research 的手动变体,由 /search 触发:只查一手官方资料,结论直接答在对话里、逐条附来源,不写任何文件;要落盘成 Markdow… |

### 自动触发(模型按需调用)

| 技能 | 说明 |
|------|------|
| `code-review` | 按两轴审查自某基点以来的变更:是否符合仓库规范(含 Fowler 坏味道基线)、是否忠实实现源 issue/spec。 |
| `codebase-design` | 设计深模块(deep module)的共享词汇:设计或改进模块接口、寻找深化机会、确定接缝位置、提升可测试性与 AI 可导航性。 |
| `diagnosing-bugs` | 硬 bug 与性能回退的诊断循环:建立可复现反馈环、最小化、假设、插桩、修复、回归测试。 |
| `domain-modeling` | 构建并打磨项目领域模型:讨论代码库术语、编写或编辑 CONTEXT.md、记录 ADR 时使用。 |
| `find-skills` | 帮助查找并安装开放 agent 技能生态中的技能:回答「有没有做 X 的技能」「帮我找 X 技能」等需求。 |
| `git-guardrails-claude-code` | 为 Claude Code 配置 hooks,在危险 git 命令(push、reset --hard、clean、branch -D 等)执行… |
| `grilling` | 对方案、决策、想法穷追不舍地提问以压力测试思路;grill-me、triage、wayfinder 等共用的底层原语。 |
| `prototype` | 做一次性原型回答设计问题:状态或逻辑用单个共享 HTML,UI 探索用可切换的多方案变体。 |
| `research` | 以高信任一手来源调研问题,结论写成带引用的 Markdown 文件入库,可由后台 agent 执行。 |
| `resolving-merge-conflicts` | 逐 hunk 解决进行中的 git merge/rebase 冲突,按意图回溯冲突双方源头,完成后收尾(不 abort)。 |
| `setup-pre-commit` | 在仓库配置 Husky 预提交钩子:lint-staged(Prettier)+ 类型检查 + 测试。 |
| `skill-creator` | 创建、修改与优化技能并评测性能:从零写技能、跑 eval 测试、方差分析基准、优化描述提升触发准确率。 |
| `tdd` | 测试驱动开发:先写失败测试再修复(red-green-refactor),一次一个垂直切片。 |
| `wizard` | 生成交互式 bash 向导,引导人类完成只有他们能做的步骤:基础设施、凭据、CI 机密、陌生后台或一次性迁移。 |
<!-- skills-table:end -->

> 技能表由 [tools/update_readme.py](tools/update_readme.py) 自动维护,请勿手改标记区间内内容。

## 目录结构

- `.claude/skills/<技能名>/SKILL.md` — 唯一的技能目录;在本仓库内打开 Claude Code 即从此加载
- `.mcp.json` — 本仓库开发用的 MCP 服务器配置(github / context7),凭据只以 `${VAR}` 占位、不存明文,见下节
- `tools/update_readme.py` + `tools/skill-desc-zh.json` — 技能表重新生成(中文说明映射)
- `rules/AGENTS.md` / `rules/AGENTS.zh.md` — 通用 agent 规则(English / 中文版)
- `skills-lock.json` — `npx skills` 安装记录(每个技能的来源与内容哈希)
- `settings.json` — 作者本人 Claude Code 用户配置的参考副本(Claude Code 不会加载它,见下节)

## Claude Code 配置参考

根目录的 [settings.json](settings.json) 是作者本人的 Claude Code 用户配置,作为参考副本留在仓库,供想了解如何配置 permissions、deny 规则与 env 覆盖项的读者借鉴。**Claude Code 不会读取仓库根目录的 `settings.json`** —— 它只从 `~/.claude/settings.json`(用户级,作用于所有项目)与 `<项目根>/.claude/settings.json`(项目级,须位于项目 `.claude/` 目录内)加载配置。文件中的 `env` 段是本机专属配置(本地代理端点与模型重映射),直接照抄在其他机器上不会生效,请按需裁剪。

## MCP 配置

[.mcp.json](.mcp.json) 为仓库开发提供两个 MCP 服务器:github(GitHub 操作)、context7(第三方库文档查询)。**凭据不以明文入库**:文件里只写 `${VAR}` 占位符,启动时由 Claude Code 从进程环境展开。

配置流程:

1. 项目里有 `.mcp.json` 即可(本仓库自带占位符版本,可直接提交,不含任何密钥)。
2. 准备各站点的 token:GitHub 的 fine-grained 或 classic PAT、context7 的 API key。
3. 把真实值写进 `~/.claude/settings.json`(用户级配置,不入库)的 `env` 段,例如:

   ```json
   {
     "env": {
       "GITHUB_PAT": "github_pat_真实token",
       "CONTEXT7_API_KEY": "ctx7sk-真实key"
     }
   }
   ```

   `env` 段由 Claude Code 启动时注入进程环境——与操作系统环境变量等效(优先级高于 shell 导出值,且只对 Claude Code 及其子进程可见),`.mcp.json` 里的 `${VAR}` 即从中展开;还支持默认值语法 `${VAR:-默认值}`。
4. 重启 Claude Code 使环境变量生效(在会话启动时注入);用 `claude mcp list` 可查看服务器状态与缺失变量告警。

要点:

- **无需 `.env` 文件**:Claude Code 不会自动加载项目根目录的 `.env`,变量只认进程环境(shell 导出或 settings 的 `env` 段)。
- 变量缺失不阻止加载:启动时告警,请求会携带字面 `${VAR}`(鉴权失败是「响亮」的,便于排查,不会静默出错)。
- 本仓库根目录 [settings.json](settings.json) 参考副本不含 token;真实值只存在于你的用户级 `~/.claude/settings.json`。
- token 若曾外泄(误提交、明文贴进对话等),去站点后台轮换后同步更新 settings 即可。

## 通用规则

[rules/AGENTS.zh.md](rules/AGENTS.zh.md)(中文版)/ [rules/AGENTS.md](rules/AGENTS.md)(English)是一份可直接使用的 agent 通用规则(核心原则:不编造、先证据;含安全与破坏性操作底线、冲突裁决、运行模式等)。「底线」建议全盘保留,「偏好」可按需裁剪。内容不依赖任何工具专属语法。

注意:规则文件本身通用,但**各工具读取的文件名不同**——Claude Code 只读 `CLAUDE.md`,Codex 只读 `AGENTS.md`(二者均不读取对方文件名,此差异已在官方文档/源码验证)。按目标工具放置:

| 目标 | 放置位置 | 命令 |
|---|---|---|
| Claude Code(全局) | `~/.claude/CLAUDE.md` | `cp rules/AGENTS.md ~/.claude/CLAUDE.md` |
| Claude Code(单个项目) | 项目根 `CLAUDE.md` | 把规则复制为项目根 `AGENTS.md`,再在 CLAUDE.md 顶部加一行 `@AGENTS.md` import(官方推荐,双工具共用一份) |
| Codex(全局) | `~/.codex/AGENTS.md` | `cp rules/AGENTS.md ~/.codex/AGENTS.md` |
| Codex(单个项目) | 项目根 `AGENTS.md` | 直接放入项目根即可 |

## 许可

根目录 MIT License 适用于本仓库自有的编排内容;各技能目录保留各自上游的 LICENSE 文件。
