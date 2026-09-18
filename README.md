# skills

个人 agent skills 的源仓库。`install.sh` 把 `zh/` 下的 skill 平铺安装到各 agent 的 skills 目录。

## 安装

```sh
./install.sh zh                      # 装到 ~/.agents、~/.codex、~/.claude 的 skills 目录
./install.sh zh --dry-run            # 预演,不落盘
./install.sh zh ~/my-agent/skills    # 指定目标目录
```

按目录名平铺复制,目标目录内同名 skill 被完全镜像;更名或移除的 skill 由脚本内的清理列表删除。

## Skills

| Skill | 什么时候用 |
| --- | --- |
| `personal-style` | 处理开发请求时遵循个人编码风格约定 |
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
zh/         # 全部 skill 源码,每个子目录一个 SKILL.md
install.sh  # 安装脚本
```

改动前先读 `AGENTS.md`。中文单源,不维护英文镜像。

## 这里不放治理流程

试过两次都删了(v1 `modular-programming`、v2 `living-docs`),同一个理由:机制体量超过实际收益。理由和内容都在 git 历史里,tag `modular-v1-frozen` 指向 v1 冻结点。
