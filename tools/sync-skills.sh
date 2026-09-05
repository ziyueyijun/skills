#!/usr/bin/env bash
# 将 .agents/skills 中的安装态技能镜像到发布目录 skills/ 与本地 agent 目录 .claude/skills(只增不删)。
# 用法:bash tools/sync-skills.sh   (须在仓库根目录运行)
set -euo pipefail
cd "$(dirname "$0")/.."

INSTALL_DIR=".agents/skills"
PUBLISH_DIR="skills"
CLAUDE_DIR=".claude/skills"

if [ ! -d "$INSTALL_DIR" ]; then
  echo "未找到 $INSTALL_DIR,跳过镜像。"
  exit 0
fi

count=0
for skill in "$INSTALL_DIR"/*/; do
  name=$(basename "$skill")
  [ -f "$skill/SKILL.md" ] || continue  # 只镜像含 SKILL.md 的技能
  for dest in "$PUBLISH_DIR" "$CLAUDE_DIR"; do
    mkdir -p "$dest"
    rm -rf "$dest/$name"
    cp -r "$skill" "$dest/$name"
  done
  count=$((count+1))
done

echo "已镜像 $count 个技能到 skills/ 与 .claude/skills/"
python tools/update_readme.py
echo "README.md 技能表已更新"
