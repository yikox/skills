---
name: installer
code_paths:
  - install.sh
---

# installer

## 职责

把 `zh/` 下全部 skill(按 `find -name SKILL.md` 发现)平铺复制到目标 skills 目录,并清理 deprecated 旧 skill 名(含 v1 的 10 个 modular-* 与 _shared)。

## 对外接口

- `./install.sh zh [--dry-run] [target_dir ...]`:语言参数必填且仅接受 zh;`en` 报错并指向 tag `modular-v1-frozen`;缺参退出码 2。默认目标 `~/.agents/skills`、`~/.codex/skills`、`~/.claude/skills`。
- rsync `-a --delete`:目标目录内同名 skill 完全镜像源。

## 依赖

- bash、rsync、find;无其他依赖。

## 注意点

- 平铺布局是 living-docs-suite 跨 skill 相对引用(`../docs-init/templates/`)的前提,不要改成嵌套安装。
- deprecated 列表含 `_shared`:任何想恢复共享层的改动都会被安装时清理,先改这里。
