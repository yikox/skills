# living-docs Skills

> v1(modular-programming,10 skill 治理套件)已于 2026-07-09 冻结,存档于 [`legacy/`](legacy/README.md),tag `modular-v1-frozen`。

让 AI agent 用**两份文档**维持项目的可持续,而不是用流程:

1. **项目文档 `project.md`**:概况 / 当前焦点 / 知识 / 变更日志,四章固定,每章有明确的读者、写法和压缩规则。解决"跨会话失忆"和"知识沉淀成流水账"。
2. **设计文档 `architecture/`**:main-design.md(一到两屏的模块地图)+ modules/*.md(每模块五节,≤80 行)。解决"越写越乱"和"改动无处定位"——可以直接说"我要改某某模块的 XX"。

准确性不靠流程审批,靠两道保证:**提交纪律**(改到哪个模块,文档改动和代码同一颗 commit,写进项目 CLAUDE.md 的一条规则)+ **同步门**(pre-push hook 在变更进入受管分支前跑 `git diff ∩ code_paths`,"代码动了、文档没动"就拒绝;确实无需改文档时 commit message 加 `Arch-Sync: skip <module> <理由>` 放行,理由入历史可审计)。受管分支默认 main,开发分支自由。

## Skills

仓库内共 9 个 skill，安装时全部平铺到目标目录。套件三个有调用关系，其余六个彼此独立。

套件（`living-docs`）：

| Skill | 什么时候用 |
| --- | --- |
| `docs-init` | 新项目接入:建两份文档 + 写入顺带更新规则 |
| `docs-sync` | 漂移对账、项目文档归档压缩、旧文档体系一次性迁移 |
| `docs-acceptance` | 临时验收员:init/sync 完成后自动调用,结果记入 acceptance-log.md;连续 5 次全过后拆除毕业 |

独立 skill：

| Skill | 什么时候用 |
| --- | --- |
| `personal-style` | 处理开发请求时遵循个人编码风格约定 |
| `git-commit` | 生成、规范化或检查 Git 提交信息;用户明确要求时执行提交或推送 |
| `writing-plexus-notes` | 把笔记安全写入本机 Plexus Markdown 工作区 |
| `using-cursor-cli` | 低带宽调度本地 Cursor Agent CLI 做分析、规划、结构化自动化或隔离代码修改 |
| `using-claude-cli` | 低带宽调度本地 Claude Code CLI 做分析、规划、结构化自动化或隔离代码修改 |
| `using-codex-cli` | 低带宽调度本地 Codex CLI 做分析、规划、结构化自动化或隔离代码修改 |

三个 CLI 调度 skill 均为手动触发：只有显式调用 `$using-*-cli` 或明确点名对应 CLI 时才加载。

对套件本身的修改,唯一合法输入是 acceptance-log.md 里的使用证据——这是 v1 三十次"看着不对劲"式修改永不收敛的教训。

## 使用

```text
Use $docs-init 给这个项目接入 living-docs。
Use $docs-sync 对账/压缩项目文档/迁移旧文档体系。
Use $git-commit 规范/检查我的提交信息。
Use $personal-style 按我的编码风格约束本次改动。
Use $writing-plexus-notes 把这段内容记进 Plexus。
Use $using-cursor-cli 通过 Cursor Agent CLI 复核当前改动。
Use $using-claude-cli 通过 Claude Code CLI 复核当前改动。
Use $using-codex-cli 通过 Codex CLI 复核当前改动。
```

## 安装

```sh
./install.sh zh              # 安装(默认 ~/.agents、~/.codex、~/.claude 的 skills 目录)
./install.sh zh --dry-run    # 预演
./install.sh zh ~/my-agent/skills   # 指定目标目录
```

中文单源,不维护英文镜像。skill 按目录名平铺复制,目标目录内同名 skill 被完全镜像;安装时会一并清理早前版本遗留的旧 skill 名(`modular-*`、`_shared`、`pm-*`、`auto-ai-coauthor` 等)。

## 仓库结构

```text
project.md            # 本仓库自己的项目文档
architecture/         # 本仓库自己的模块地图(main-design + modules/*)
acceptance-log.md     # living-docs 套件的验收日志(套件修改的唯一合法输入)
zh/living-docs/       # v2 套件:docs-init / docs-sync / docs-acceptance
zh/personal-style/    # 独立 skill
zh/git-commit/        # 独立 skill
zh/writing-plexus-notes/  # 独立 skill
zh/using-cursor-cli/  # Cursor Agent CLI 调用 skill
zh/using-claude-cli/  # Claude Code CLI 调用 skill
zh/using-codex-cli/   # Codex CLI 调用 skill
legacy/               # v1 冻结存档(只读)
install.sh
```

设计与决策沿革见 `architecture/changes/2026-07-09-living-docs-v2-redesign.md`。
