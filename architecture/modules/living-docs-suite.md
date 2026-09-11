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
- `docs-sync/scripts/check_sync.py [--arch-dir <dir>] [--repo <root>] [--branch <name>] [--remote origin] [--range A..B]`:同步门 CLI。默认查 `<remote>/<branch>` 与工作区的差异(含未提交、未跟踪);`--range` 查指定段(hook/抽查用);`--no-renames` 保证跨模块移动文件时源模块同样被点名。读 main-design frontmatter 的 `sync_branches`(默认 [main],不受管分支直接放行)与 `ignored_paths`、模块文档 frontmatter 的 `code_paths`;放行出口为 commit message 的 `Arch-Sync: skip <模块名|路径 glob> <理由>`(模块名放行 DRIFT,路径 glob 放行 ORPHAN)。退出码 0 同步/不受管 / 1 漂移 / 2 配置错——退出码分流靠 `die()` 显式传码,不能用 `sys.exit("文本")`(那样恒为 1)。
- `docs-sync/tests/test_check_sync.py`:check_sync.py 的回归测试,在临时仓库里覆盖十条用例——同步 / DRIFT / ORPHAN / ORPHAN 的 skip 出口(精确路径与 glob) / ignored_paths / 不受管分支 / DRIFT 的 skip 出口 / 跨模块移动 / arch-dir 越界。`python3 tests/test_check_sync.py`。
- `docs-init/templates/pre-push-hook.sh`:hook 模板,装入 `.git/hooks/pre-push` 并改写 `ARCH_DIR`;它靠自身所在目录定位 `living-docs-check-sync.py`,故须与该脚本**成对安装**。
- `docs-init/templates/*.md`:project / main-design / module 模板与 ai-rules-snippet;docs-sync 迁移时按 `../docs-init/templates/` 相对路径引用(安装后为同级目录,依赖 installer 平铺布局)。

## 依赖

- installer:平铺复制,保证 docs-sync → docs-init 的同级相对引用成立。
- 目标项目的 git:同步门的唯一数据源;非 git 项目该能力不可用。

## 注意点

- 与设计文档的偏差:无 _shared 层,每个 skill 自包含(installer 平铺 + _shared 在清理列表,共享层装上即被删)。
- 同步门的核心脚本随 hook 落到目标项目的 `.git/hooks/`(命名 `living-docs-check-sync.py`),**不依赖 skill 安装路径**;docs-sync 的抽查因此也用 `.git/hooks/` 里的副本。两份文件拆开装会让门静默失效。
- hook 在缺 python3 或缺检查脚本时打印警告并放行(门是事后归纳工具,不是安全边界),因此"门没拦住"要先去 `.git/hooks/` 确认两份文件是否都在。
- 模块文档是 frontmatter 的 `code_paths` + 正文四节(职责/对外接口/依赖/注意点);docs-init、template、docs-sync 迁移表三处措辞必须一致。
- ORPHAN 的默认出口是改配置(补 code_paths / 建模块 / 加 ignored_paths),对"一次性删除无归属文件"都会永久留痕,故补了 `Arch-Sync: skip <路径 glob>` 这条一次性出口。
- docs-init/docs-sync 的 SKILL.md 末尾强制调用 docs-acceptance;拆除 acceptance 时须同步删掉这两处调用要求。
- 修改本套件的唯一合法输入是使用中产生的 acceptance-log.md 记录。
