# skills 仓库约定

本仓库是技能的**发布源与完整镜像**:`skills/` 为发布布局(供 `npx skills add ziyueyijun/skills` 发现),`.agents/skills` 与 `.claude/skills` 为可直接使用的安装态(全部真实文件,入库共享)。任何人(包括本会话 Claude)在本仓库执行 `npx skills add/update` 安装、更新技能后,**必须运行同步脚本**,保持三处一致:

```bash
bash tools/sync-skills.sh
```

## 发布规则(必须遵守)

1. **同步方向**:`.agents/skills/`(源) → `skills/`(发布镜像)与 `.claude/skills/`(本机使用镜像),只增不删;`skills/` 里不在 `.agents/skills` 中的目录(如插件来源的 frontend-design)原样保留。
2. **同步后**:README.md(英文默认)与 README.zh-CN.md(中文版)的技能表由 `tools/update_readme.py` 自动重生成(英文表用技能原版描述,中文表用中文映射;标记区间 `skills-table` 内勿手改);同步脚本会自动调用它。**技能表之外正文若修改,须同步更新两份 README 的对应内容。**
3. **来源标注**:脚本从 `skills-lock.json` 读取每个技能的上游来源;不在锁文件中的技能需在 `tools/update_readme.py` 的 `OVERRIDE` 表手动补来源。
4. **技能表说明必须为中文**:中文说明维护在 `tools/skill-desc-zh.json`(name → 说明);新增技能时须同步补一条中文说明(可让 Claude 翻译 frontmatter 描述后写入),缺失时脚本回退英文并在提交前补齐。
4. **许可证**:复制第三方技能前先确认其许可允许再分发(须 MIT/Apache 类);MIT 许可需在 README「许可」节保留原作者版权声明。
5. **符号链接禁令**:提交内容一律为真实文件。`.claude/skills` 若出现 npx 创建的 junction/符号链接,先替换为真实副本再提交(Windows 上链接目标为绝对路径,对他人无效)。
6. 同步脚本与约定文件(`tools/`、本文件)的改动需随仓库提交,确保其他机器 clone 后规则仍生效。
7. **插件清单人工维护**:`.claude-plugin/plugin.json` 与 `marketplace.json` 不在自动同步范围内;新增/移除技能或行为变化时,同步更新 manifest 的 description,并按需递增 `version`(或打 tag)。
