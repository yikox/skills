# skills

个人 agent skills 的源仓库。`install.sh` 把 `zh/` 下的 skill 以软链接平铺安装到各 agent 的 skills 目录。

## 安装

```sh
./install.sh zh                      # 软链接装到 ~/.agents、~/.codex、~/.claude、~/.cursor、~/.workbuddy 的 skills 目录
./install.sh zh --dry-run            # 预演,不落盘
./install.sh zh ~/my-agent/skills    # 指定目标目录
```

按目录名建立指向本仓库源码的软链接（若目标已有同名物理目录则先替换为软链接）;更名或移除的 skill 由脚本内的清理列表删除。

## Skills

| Skill | 什么时候用 |
| --- | --- |
| `me` | 所有开发请求和个人任务管理请求必定加载；按具体任务触发条件读取个人规则专题文档 |
| `git-commit` | 生成、规范化或检查 Git 提交信息;用户明确要求时执行提交或推送 |
| `writing-good-docs` | 写或重写一份成形文档时,先判断体裁再按该体裁的写作逻辑组织 |
| `writing-plexus-notes` | 把笔记安全写入本机 Plexus Markdown 工作区 |
| `with-doc` | 为单次任务维护一份人读的工作记录 |
| `show-me` | 按真实执行顺序讲解仓库中的一个逻辑实现 |
| `using-cursor-cli` | 低带宽调度本地 Cursor Agent CLI 做分析、规划、结构化自动化或隔离代码修改 |
| `using-claude-cli` | 低带宽调度本地 Claude Code CLI 做分析、规划、结构化自动化或隔离代码修改 |
| `using-codex-cli` | 低带宽调度本地 Codex CLI 做分析、规划、结构化自动化或隔离代码修改 |

大多数 skill 由 agent 按 `description` 自行判断是否加载;三个 CLI 调度 skill 是手动触发,只有显式调用 `$using-*-cli` 或明确点名对应 CLI 时才加载。

## 仓库结构

```text
AGENTS.md   # 本仓库约定(AI 协作规则唯一事实源)
CLAUDE.md   # @AGENTS.md 引入
zh/         # 全部 skill 源码,每个 skill 子目录含 SKILL.md,可带按需读取的专题文档
install.sh  # 安装脚本
skill-hub/  # 本机 Skill 全盘扫描、软链去重与 AI 工具快捷启动台 (含 Skill Hub.app)
```

改动前先读 `AGENTS.md`。中文单源,不维护英文镜像。

## Skill Hub (本机管理与快捷启动台)

`skill-hub/` 提供零第三方依赖的本机 `SKILL.md` 全盘扫描、版本分叉对比、一键软链去重及 AI 工具快捷启动面板:

```sh
# 方式 1: 直接双击打开原生桌面窗口应用（含 Dock 图标与右上角状态栏 ⚡ Skill Hub 指示，关闭窗口即自动停止后台服务）
open "skill-hub/Skill Hub.app"

# 方式 2: 命令行启停服务 (http://127.0.0.1:8765)
./skill-hub/ctl.sh start
./skill-hub/ctl.sh stop
./skill-hub/ctl.sh status

# 方式 3: 独立执行全盘扫描或软链对齐脚本
python3 skill-hub/scan_skills.py
python3 skill-hub/sync_skills.py
```

## 这里不放治理流程

试过两次都删了(v1 `modular-programming`、v2 `living-docs`),同一个理由:机制体量超过实际收益。理由和内容都在 git 历史里,tag `modular-v1-frozen` 指向 v1 冻结点。
