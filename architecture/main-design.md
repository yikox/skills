---
ignored_paths:
  - README.md
  - README_EN.md
  - CLAUDE.md
  - project.md
  - acceptance-log.md
  - archives/**
---

# skills 仓库 设计文档

本仓库产出并分发 agent skills:living-docs v2 套件(三个 SKILL.md 技能,教 agent 用两份文档维持项目可持续)、独立的 personal-style,以及把它们复制到各 agent skills 目录的安装脚本。v1 套件整体冻结在 legacy/,只读。运行环境:支持 SKILL.md 协议的 agent + Python 3 标准库 + bash。

## 模块表

| 模块 | 职责 | 入口 |
| --- | --- | --- |
| living-docs-suite | v2 套件:docs-init(建文档)、docs-sync(对账/压缩/迁移)、docs-acceptance(临时验收员),含模板与漂移检测脚本 | zh/living-docs/*/SKILL.md |
| personal-style | 个人编码风格约定,独立 skill | zh/personal-style/SKILL.md |
| installer | 按语言参数把 zh/ 下全部 skill 平铺复制到目标目录,清理旧 skill 名 | install.sh |
| legacy-v1 | modular-programming v1 冻结存档(en+zh),契约冻结只读 | legacy/README.md |

## 模块协作

安装流:installer 用 `find zh/ -name SKILL.md` 发现技能,按目录名平铺 rsync 到各目标,再删除 deprecated 列表中的旧 skill(含 v1 的 modular-* 与 _shared)。运行流:agent 加载 living-docs-suite 的某个 skill;docs-sync 在目标项目里调用自带的 check_drift.py;docs-init 与 docs-sync 结束时强制调用 docs-acceptance。legacy-v1 不参与任何流,出现变更即违反冻结契约(漂移检测会点名它)。
