---
name: living-docs-suite
code_paths:
  - zh/living-docs/**
---

# living-docs-suite

## 职责

v2 套件本体:教 agent 建立并维护两份文档(project.md + architecture/ 模块地图)。三个 skill:docs-init(初始化 + 安装 pre-push 同步门,持有全部模板与 hook 模板)、docs-sync(门后对齐、历史抽查、归档压缩、旧体系一次性迁移,持有 check_sync.py)、docs-acceptance(临时验收员,持有验收清单,毕业后拆除)。

## 对外接口

- `$docs-init` / `$docs-sync` / `$docs-acceptance`:SKILL.md 协议触发。
- `docs-sync/scripts/check_sync.py [--arch-dir <dir>] [--repo <root>] [--branch <name>] [--remote origin] [--range A..B]`:同步门 CLI。默认查 `<remote>/<branch>` 与工作区的差异(含未提交);`--range` 查指定段(hook/抽查用)。读 main-design frontmatter 的 `sync_branches`(默认 [main],不受管分支直接放行)与 `ignored_paths`、模块文档 frontmatter 的 `code_paths`;放行出口为 commit message 的 `Arch-Sync: skip <module> <理由>`。退出码 0 同步/不受管 / 1 漂移 / 2 配置错。
- `docs-init/templates/pre-push-hook.sh`:hook 模板,装入 `.git/hooks/pre-push` 时替换 ARCH_DIR 与 CHECK_SYNC_PATH。
- `docs-init/templates/*.md`:project / main-design / module 模板与 ai-rules-snippet;docs-sync 迁移时按 `../docs-init/templates/` 相对路径引用(安装后为同级目录,依赖 installer 平铺布局)。

## 依赖

- installer:平铺复制,保证 docs-sync → docs-init 的同级相对引用成立。
- 目标项目的 git:同步门的唯一数据源;非 git 项目该能力不可用。

## 注意点

- 与设计文档的偏差:无 _shared 层,每个 skill 自包含(installer 平铺 + _shared 在清理列表,共享层装上即被删)。
- docs-init/docs-sync 的 SKILL.md 末尾强制调用 docs-acceptance;拆除 acceptance 时须同步删掉这两处调用要求。
- 修改本套件的唯一合法输入是使用中产生的 acceptance-log.md 记录。
