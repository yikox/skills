# skills 仓库 项目文档

Last updated: 2026-07-09

## 概况

个人 agent skills 的源仓库。当前产品是 **living-docs v2 套件**(`zh/living-docs/`:docs-init / docs-sync / docs-acceptance)——用两份文档(项目文档 + 模块地图)加"顺带更新 + git 对账"维持项目可持续,取代已冻结的 modular-programming v1(见 `legacy/`,tag `modular-v1-frozen`)。另含独立 skill `personal-style`。中文单源,不维护英文镜像。

- 安装:`./install.sh zh`(默认目标 `~/.agents|.codex|.claude` 的 skills 目录;预演加 `--dry-run`)
- 漂移检测:`python3 zh/living-docs/docs-sync/scripts/check_drift.py --arch-dir architecture`

## 当前焦点

- v2 落地全部完成并经用户验收确认(2026-07-09),套件进入试用期;毕业计数 1/5。
- 待办:acceptance-log 已有一条套件改进证据(.last-sync 锚点入库导致落后 HEAD 一颗 commit),下次修改套件时处理。

## 知识

### 构建与测试

- 无构建;验证靠 `./install.sh zh --dry-run` 与 `check_drift.py` 直跑。仅 Python 3 标准库 + bash,不引入第三方包。

### 环境坑

- EnterWorktree 建出的 worktree 可能缺本地未推送 commit(baseRef 默认 origin/main);worktree 内 `git merge --ff-only main` 补齐(2026-07-03 实证)。
- ExitWorktree remove 会误报"N commits 将丢失":先 `git merge-base --is-ancestor <tip> main` 确认已包含,再 discard。

### 约定

- commit 末尾加 `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`。
- 设计/PM 文档与 skill 正文均用中文(v2 起中文单源;v1 时代的 en 主 zh 镜像约定随冻结作废)。
- 请求用户确认 L3 级决策时,必须先给 3-8 条要点摘要(修改重点、歧义点、风险),让用户不读全文也能决策。
- 对 living-docs 套件本身的修改,唯一合法输入是 acceptance-log.md 中的记录(反面教训:v1 的 30 次提交全部由"看着不对劲"驱动,永不收敛)。
- CLAUDE.md 自 v2 起入库(规则仅含仓库相对路径;v1 时代因含机器路径不入库的决定 0fa8ba2 不再适用)。

## 变更日志

<!-- append-only,一条一行:日期 + 一句话 + commit。超 50 条或本文件超 15KB 时归档。 -->

- 2026-07-09 文档迁至标准位置项目根,PM/ 与全部 v1 记账产物按用户指示丢弃(git 历史/tag 可回溯);清理 ~/.codex 残留 project-management-docs 并补进 installer 清理列表 (本次 commit)
- 2026-07-09 本仓库 PM 迁移至 living-docs 格式,v1 记账文档移入 archives/(v1- 前缀),README 重写 (f447354)
- 2026-07-09 living-docs v2 套件实现:三 skill + 模板 + check_drift.py,中文单源、无 _shared 层(与设计的偏差:skill 自包含,原因是 installer 平铺布局与 _shared 清理冲突) (a229eb8)
- 2026-07-09 v1 套件冻结入 legacy/,installer 仅支持 zh 并清理旧 skill,tag modular-v1-frozen (283337b)
- 2026-07-09 living-docs v2 重设计提案落盘并经用户评审通过 (d6cee0f)
- 2026-07-08 默认 L2/L3 改为 branch-carried architecture patch;证据单一居所 + PM 压缩 (bd19dfa, ca17459, 1bfa33a)
- 2026-07-05/06 中英双语结构层与 zh 散文翻译;新增 modular-narrator;architect 改名 advisor (7cf18d3, 03d55f3, a537db2, 265aa52)
- 2026-07-04 轻量默认工作流、vocab 单一事实源、module-kind 拆分、modular-architect 角色 (22c98e8 等)
- 2026-07-03 初始化项目记忆;modular-autopilot 合入 main (7e55bf5..77b70c2)

v1 时代记账文档已按用户指示丢弃;需要时从 git 历史或 tag `modular-v1-frozen` 取回。
