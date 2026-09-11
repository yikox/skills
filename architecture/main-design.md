---
sync_branches:
  - main
ignored_paths:
  - README.md
  - README_EN.md
  - AGENTS.md
  - CLAUDE.md
  - .gitignore
  - project.md
  - acceptance-log.md
  - archives/**
---

# skills 仓库 设计文档

本仓库产出并分发 agent skills:living-docs v2 套件(三个 SKILL.md 技能,教 agent 用两份文档维持项目可持续)、六个独立 skill(personal-style、git-commit、writing-plexus-notes 与 using-cursor-cli / using-claude-cli / using-codex-cli),以及把它们复制到各 agent skills 目录的安装脚本。v1 套件整体冻结在 legacy/,只读。运行环境:支持 SKILL.md 协议的 agent + Python 3 标准库 + bash(install.sh 兼容 macOS 自带的 bash 3.2)。

## 模块表

| 模块 | 职责 | 入口 |
| --- | --- | --- |
| living-docs-suite | v2 套件:docs-init(建文档+装同步门)、docs-sync(门后对齐/抽查/压缩/迁移)、docs-acceptance(临时验收员),含模板、hook 与 check_sync.py | zh/living-docs/*/SKILL.md |
| git-commit | 统一 git 提交信息规范：中文提交、标签化主题，支持仓库特化签名规则 | zh/git-commit/SKILL.md |
| personal-style | 个人编码风格约定,独立 skill | zh/personal-style/SKILL.md |
| using-cursor-cli | 通过本地 Cursor Agent CLI 做事件驱动的低带宽调度:Cursor 承担主要推理与执行,调用方默认等待完成唤醒,只处理最终摘要与窄验收 | zh/using-cursor-cli/SKILL.md |
| using-claude-cli | 通过本地 Claude Code CLI 做低带宽调度:Plan 只读,原生 worktree + 最小工具白名单隔离写任务 | zh/using-claude-cli/SKILL.md |
| using-codex-cli | 通过本地 Codex CLI 做低带宽调度:显式审批与 sandbox,调用方创建 worktree 隔离写任务 | zh/using-codex-cli/SKILL.md |
| writing-plexus-notes | 把笔记安全写入 Plexus Markdown 工作区,约定路径自配置、知识节点双面结构、草稿箱与冲突处理 | zh/writing-plexus-notes/SKILL.md |
| installer | 按语言参数把 zh/ 下全部 skill 平铺复制到目标目录,清理旧 skill 名 | install.sh |
| legacy-v1 | modular-programming v1 冻结存档(en+zh),契约冻结只读 | legacy/README.md |

## 模块协作

安装流:installer 用 `find zh/ -name SKILL.md` 发现技能,按目录名平铺 rsync 到各目标,再删除 deprecated 列表中的旧 skill(含 v1 的 modular-*、`_shared` 与 `auto-ai-coauthor`)。运行流:agent 可独立加载 personal-style、git-commit、writing-plexus-notes 或三个 CLI 调度 skill;CLI 调度 skill 分别直接调用本机 `cursor-agent`、`claude`、`codex exec`,writing-plexus-notes 直接读写本机 Plexus Markdown 工作区,均不依赖其他仓库 skill。living-docs-suite 中,docs-init 在目标项目装同步门——把 hook 模板与 docs-sync 的 `check_sync.py` 成对落到目标项目的 `.git/hooks/`,使门不依赖 skill 安装路径;docs-init 与 docs-sync 结束时强制调用 docs-acceptance。legacy-v1 不参与任何流,出现变更即违反冻结契约(同步门会点名它)。
