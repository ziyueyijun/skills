# skills 仓库约定

本仓库是技能的**发布源与完整镜像**:`skills/` 为发布布局(供 `npx skills add ziyueyijun/skills` 发现),`.agents/skills` 与 `.claude/skills` 为可直接使用的安装态(全部真实文件,入库共享)。任何人(含本会话 Claude)在本仓库执行 `npx skills add/update` 后,**必须运行同步脚本**:

```bash
bash tools/sync-skills.sh
```

`tools/sync-skills.sh` 将 `.agents/skills/`(源)镜像到 `skills/` 与 `.claude/skills/`(只增不删;`skills/` 中不在 `.agents/skills` 的目录,如 frontend-design,原样保留),并自动调用 `tools/update_readme.py` 重生成两份 README 的技能表:

- 标记区间 `skills-table` 内勿手改;英文表用技能原版描述、中文表用 `tools/skill-desc-zh.json` 映射(新增技能须补一条中文说明;缺失回退英文,提交前补齐)。
- 手动触发技能行序由脚本内 `MANUAL_ORDER` 决定(工作流顺序);新增手动技能想插到指定位置,先把名字加入该列表。
- 标记区间之外正文若有修改,须同步更新两份 README。

## 发布规则(必须遵守)

1. **发布须经用户同意**:`git push` 共享远端、推 tag、建 Release、`gh` 发 PR/issue 等对外操作,执行前先列明将对外可见的内容并等待明确同意;本地 `git commit` 不受此限。
2. **许可证**:复制第三方技能前确认其许可允许再分发(须 MIT/Apache 类);自带 LICENSE/LICENSE.txt 保持原样入库;README「许可」节不做逐来源版权声明。
3. **符号链接禁令**:提交内容一律为真实文件;`.claude/skills` 出现 npx 创建的 junction/符号链接时,先替换为真实副本再提交(Windows 上链接目标为绝对路径,对他人无效)。
4. **约定文件随仓库提交**:`tools/` 与本文件的改动一并提交,确保其他机器 clone 后规则仍生效。
