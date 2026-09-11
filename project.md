# skills 仓库 项目文档

Last updated: 2026-09-11

## 概况

个人 agent skills 的源仓库。当前产品是 **living-docs v2 套件**(`zh/living-docs/`:docs-init / docs-sync / docs-acceptance)——用两份文档(项目文档 + 模块地图)加"顺带更新 + git 对账"维持项目可持续,取代已冻结的 modular-programming v1(见 `legacy/`,tag `modular-v1-frozen`)。另含六个独立 skill:`personal-style`、`git-commit`、`writing-plexus-notes` 与三个本地 CLI 调度 skill(`using-cursor-cli` / `using-claude-cli` / `using-codex-cli`)。中文单源,不维护英文镜像。

- 安装:`./install.sh zh`(默认目标 `~/.agents|.codex|.claude` 的 skills 目录;预演加 `--dry-run`)
- 套件自测:`python3 zh/living-docs/docs-sync/tests/test_check_sync.py`
- 同步预检:`python3 zh/living-docs/docs-sync/scripts/check_sync.py --arch-dir architecture`(push main 时本仓库已装 pre-push hook 自动跑)

## 当前焦点

- 仓库整体优化已落地(见本次变更日志):过程产物清理、AI 规则收敛为 `AGENTS.md` 单一源、README 补齐、installer 清理 `auto-ai-coauthor`、同步门改自包含并修掉几处实质缺陷。
- 同步机制 v2.1 试用期,毕业计数 1/5;本次对套件的改动按"使用证据"原则记入 acceptance-log 后再评估是否需要重跑验收。
- 下步:运行 `./install.sh zh` 清掉 `~/.agents/skills/auto-ai-coauthor`,再在真实 `git.mtlab.meitu.com` 仓库验证 git-commit 的动态签名与去重行为。

## 知识

### 构建与测试

- 无构建;安装验证靠 `./install.sh zh --dry-run`。仅 Python 3 标准库 + bash,不引入第三方包。
- 同步门的回归测试在 `zh/living-docs/docs-sync/tests/test_check_sync.py`(10 条用例,临时仓库里跑,不触网)。改 `check_sync.py` 必须先跑它。
- `install.sh` 必须兼容 bash 3.2(macOS 自带):不用 `readarray`、关联数组、globstar。

### 环境坑

- EnterWorktree 建出的 worktree 可能缺本地未推送 commit(baseRef 默认 origin/main);worktree 内 `git merge --ff-only main` 补齐(2026-07-03 实证)。
- ExitWorktree remove 会误报"N commits 将丢失":先 `git merge-base --is-ancestor <tip> main` 确认已包含,再 discard。
- 在 `legacy/` 里跑 Python 会生成 `__pycache__`,同步门把它算作 legacy-v1 的变更而误报 DRIFT;已加进 `.gitignore`。
- 对同一个文件并行发多个编辑会互相覆盖(各自基于同一份原始内容写回,后写者胜),只有最后一个生效。同一文件的多处改动必须串行,或合并成一次整体写入。

### 约定

- commit 末尾加 `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`;主题行按 `$git-commit` 用 `[tag] 中文摘要`。
- 设计/PM 文档与 skill 正文均用中文(v2 起中文单源;v1 时代的 en 主 zh 镜像约定随冻结作废)。
- 请求用户确认 L3 级决策时,必须先给 3-8 条要点摘要(修改重点、歧义点、风险),让用户不读全文也能决策。
- 对 living-docs 套件本身的修改,唯一合法输入是 acceptance-log.md 中的记录(反面教训:v1 的 30 次提交全部由"看着不对劲"驱动,永不收敛)。用户当场提出的明确指令同样成立,但要照实记入日志。
- AI 协作规则只在 `AGENTS.md` 一处:AGENTS.md 入库为正文,CLAUDE.md 用 `@AGENTS.md` 引入。两份都写会分叉,`.gitignore` 不再屏蔽 AGENTS.md。

## 变更日志

<!-- append-only,一条一行:日期 + 一句话 + commit。超 50 条或本文件超 15KB 时归档。 -->

- 2026-09-11 仓库整体优化:清理 v1 过程产物与编译残留、AI 规则收敛为 AGENTS.md 单一源、README 补全 9 个 skill、installer 清理 auto-ai-coauthor 并兼容 bash 3.2、同步门改自包含(脚本随 hook 落 .git/hooks)并修掉退出码恒为 1/漏报跨模块移动两个缺陷、补 ORPHAN 一次性出口与 10 条回归测试、本仓库自身启用同步门 (本次 commit)
- 2026-08-08 修正 git-commit skill 的动态 AI 身份、仓库规则优先级、远端识别与签名去重，并移除会丢失正文的 shell 模板 (本次 commit)
- 2026-08-07 新增 git-commit skill（中文提交、[tag] 前缀、仓库特化 AI 追加规则），并补齐 architecture module 与主设计地图 (本次 commit)
- 2026-08-06 personal-style 增加不保留兼容层、最简实现、最小端到端闭环、成熟依赖与已验证模式等约定 (本次 commit)
- 2026-08-03 三个 using-*-cli skill 改为仅在用户显式调用或明确指定对应 CLI 时触发 (本次 commit)
- 2026-07-28 基于 using-cursor-cli 新增 using-claude-cli 与 using-codex-cli,统一低带宽调度并分别落实原生/调用方 worktree 隔离 (本次 commit)
- 2026-07-28 using-cursor-cli 取消默认定时轮询,改为等待完成唤醒;仅按用户要求或诊断失联时做窄检查 (本次 commit)
- 2026-07-27 using-cursor-cli 改为低带宽调度,禁止回传原始 stream-json,只提取最终摘要并执行窄验收 (本次 commit)
- 2026-07-27 personal-style 新增下载前测速、低速换可信来源及内容一致性校验约定 (本次 commit)
- 2026-07-27 新增 writing-plexus-notes 独立 skill:记录 Plexus 路径自配置、知识节点结构与安全写入规则 (本次 commit)
- 2026-07-25 新增 using-cursor-cli 独立 skill:统一 Cursor Agent CLI 的只读、结构化输出、会话和隔离写入契约 (本次 commit)
- 2026-07-09 同步机制 v2.1:废除 .last-sync 锚点,check_drift.py 重写为 check_sync.py(range 门模式,sync_branches/Arch-Sync skip),docs-init 装 pre-push hook;依据 acceptance-log 2026-07-09 存疑条目 (本次 commit)
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
