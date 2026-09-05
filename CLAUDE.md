# skills 仓库约定

本仓库把技能直接维护在 `.claude/skills/`(Claude Code 项目技能目录)——在本仓库内打开
Claude Code,技能即被加载;带 `disable-model-invocation: true` 的技能以 `/技能名` 手动触发,
其余技能由模型按描述自动调用。

- 技能目录结构:`<name>/SKILL.md`(frontmatter:`name`、`description` 必填)+ 附属
  `scripts/`、`references/` 等。技能应自包含(仅 Python 内置库、无联网),目录可整体复制。
- 其他项目/全局使用:把技能目录整体复制到目标项目的 `.claude/skills/`,或 `~/.claude/skills/`
  (Windows 上注意提交真实文件、勿用符号链接)。
- README 技能表由 `tools/update_readme.py` 生成(数据源 `.claude/skills`,直接运行
  `python tools/update_readme.py` 重生成两份 README):
  - 标记区间 `skills-table` 内勿手改。
  - 中文表用 `tools/skill-desc-zh.json` 映射(新增技能须补一条中文说明;缺失回退英文,提交前补齐)。
  - 手动触发技能行序由 `MANUAL_ORDER` 决定(工作流顺序);新增手动技能想插到指定位置,先把名字加入该列表。
  - 标记区间之外正文若有修改,须同步更新两份 README。

## 发布规则(必须遵守)

1. **发布须经用户同意**:`git push` 共享远端、推 tag、建 Release、`gh` 发 PR/issue 等对外操作,执行前先列明将对外可见的内容并等待明确同意;本地 `git commit` 不受此限。
2. **许可证**:复制第三方技能前确认其许可允许再分发(须 MIT/Apache 类);自带 LICENSE/LICENSE.txt 保持原样入库;README「许可」节不做逐来源版权声明。
3. **符号链接禁令**:提交内容一律为真实文件;`.claude/skills` 出现 npx 等工具创建的 junction/符号链接时,先替换为真实副本再提交(Windows 上链接目标为绝对路径,对他人无效)。
4. **约定文件随仓库提交**:`tools/` 与本文件的改动一并提交,确保其他机器 clone 后规则仍生效。
