---
name: living-docs-suite
code_paths:
  - zh/living-docs/**
---

# living-docs-suite

## 职责

v2 套件本体:教 agent 建立并维护两份文档(project.md + architecture/ 模块地图)。三个 skill:docs-init(初始化,持有全部模板)、docs-sync(git 漂移对账、归档压缩、旧体系一次性迁移,持有 check_drift.py)、docs-acceptance(临时验收员,持有验收清单,毕业后拆除)。

## 对外接口

- `$docs-init` / `$docs-sync` / `$docs-acceptance`:SKILL.md 协议触发。
- `docs-sync/scripts/check_drift.py --arch-dir <dir> [--repo <root>]`:漂移检测 CLI;读 `<arch>/.last-sync`(commit hash 一行)、模块文档 frontmatter `code_paths`、main-design frontmatter `ignored_paths`;退出码 0 无漂移 / 1 有漂移 / 2 配置错。
- `docs-init/templates/*.md`:project / main-design / module 模板与 ai-rules-snippet;docs-sync 迁移时按 `../docs-init/templates/` 相对路径引用(安装后为同级目录,依赖 installer 平铺布局)。

## 依赖

- installer:平铺复制,保证 docs-sync → docs-init 的同级相对引用成立。
- 目标项目的 git:漂移检测的唯一数据源;非 git 项目该能力不可用。

## 注意点

- 与设计文档的偏差:无 _shared 层,每个 skill 自包含(installer 平铺 + _shared 在清理列表,共享层装上即被删)。
- docs-init/docs-sync 的 SKILL.md 末尾强制调用 docs-acceptance;拆除 acceptance 时须同步删掉这两处调用要求。
- 修改本套件的唯一合法输入是使用中产生的 acceptance-log.md 记录。
