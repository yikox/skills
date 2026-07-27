---
sync_branches:
  - main
ignored_paths:
  - README.md
  - README_EN.md
  - CLAUDE.md
  - .gitignore
  - project.md
  - acceptance-log.md
  - archives/**
---

# skills 仓库 设计文档

本仓库产出并分发 agent skills:living-docs v2 套件(三个 SKILL.md 技能,教 agent 用两份文档维持项目可持续)、独立的 personal-style、using-cursor-cli 与 writing-plexus-notes,以及把它们复制到各 agent skills 目录的安装脚本。v1 套件整体冻结在 legacy/,只读。运行环境:支持 SKILL.md 协议的 agent + Python 3 标准库 + bash。

## 模块表

| 模块 | 职责 | 入口 |
| --- | --- | --- |
| living-docs-suite | v2 套件:docs-init(建文档+装同步门)、docs-sync(门后对齐/抽查/压缩/迁移)、docs-acceptance(临时验收员),含模板、hook 与 check_sync.py | zh/living-docs/*/SKILL.md |
| personal-style | 个人编码风格约定,独立 skill | zh/personal-style/SKILL.md |
| using-cursor-cli | 通过本地 Cursor Agent CLI 做只读分析、规划、结构化自动化与隔离代码修改,约束权限、工作区、会话和验收 | zh/using-cursor-cli/SKILL.md |
| writing-plexus-notes | 把笔记安全写入 Plexus Markdown 工作区,约定路径自配置、知识节点双面结构、草稿箱与冲突处理 | zh/writing-plexus-notes/SKILL.md |
| installer | 按语言参数把 zh/ 下全部 skill 平铺复制到目标目录,清理旧 skill 名 | install.sh |
| legacy-v1 | modular-programming v1 冻结存档(en+zh),契约冻结只读 | legacy/README.md |

## 模块协作

安装流:installer 用 `find zh/ -name SKILL.md` 发现技能,按目录名平铺 rsync 到各目标,再删除 deprecated 列表中的旧 skill(含 v1 的 modular-* 与 _shared)。运行流:agent 可独立加载 personal-style、using-cursor-cli 或 writing-plexus-notes;using-cursor-cli 直接调用外部 `cursor-agent`,writing-plexus-notes 直接读写本机 Plexus Markdown 工作区,均不依赖其他仓库 skill。living-docs-suite 中,docs-init 在目标项目装 pre-push 同步门(调 docs-sync 自带的 check_sync.py),docs-init 与 docs-sync 结束时强制调用 docs-acceptance。legacy-v1 不参与任何流,出现变更即违反冻结契约(同步门会点名它)。
