# skills

个人 agent skills 源仓库。6 个 skill,由 `install.sh` 平铺安装到各 agent 的 skills 目录。

## Skills

| Skill | 什么时候用 |
| --- | --- |
| `personal-style` | 处理开发请求时遵循个人编码风格约定 |
| `git-commit` | 生成、规范化或检查 Git 提交信息;用户明确要求时执行提交或推送 |
| `writing-plexus-notes` | 把笔记安全写入本机 Plexus Markdown 工作区 |
| `using-cursor-cli` | 低带宽调度本地 Cursor Agent CLI 做分析、规划、结构化自动化或隔离代码修改 |
| `using-claude-cli` | 低带宽调度本地 Claude Code CLI 做分析、规划、结构化自动化或隔离代码修改 |
| `using-codex-cli` | 低带宽调度本地 Codex CLI 做分析、规划、结构化自动化或隔离代码修改 |

三个 CLI 调度 skill 均为手动触发:只有显式调用 `$using-*-cli` 或明确点名对应 CLI 时才加载。

## 使用

```text
Use $git-commit 规范/检查我的提交信息。
Use $personal-style 按我的编码风格约束本次改动。
Use $writing-plexus-notes 把这段内容记进 Plexus。
Use $using-cursor-cli 通过 Cursor Agent CLI 复核当前改动。
Use $using-claude-cli 通过 Claude Code CLI 复核当前改动。
Use $using-codex-cli 通过 Codex CLI 复核当前改动。
```

## 安装

```sh
./install.sh zh                      # 安装(默认 ~/.agents、~/.codex、~/.claude 的 skills 目录)
./install.sh zh --dry-run            # 预演
./install.sh zh ~/my-agent/skills    # 指定目标目录
```

中文单源,不维护英文镜像。skill 按目录名平铺复制,目标目录内同名 skill 被完全镜像;安装时会一并清理早前版本遗留的旧 skill 名。

## 仓库结构

```text
AGENTS.md   # 本仓库约定(AI 协作规则唯一事实源)
CLAUDE.md   # @AGENTS.md 引入
zh/         # 全部 skill 源码,每个子目录一个 skill
install.sh  # 安装脚本
```

## 已移除的套件

- **v1 `modular-programming`**:双语 10 skill 治理套件(L0-L3 分级、模块门、review 流程)。
- **v2 `living-docs`**:三 skill 文档治理套件(docs-init / docs-sync / docs-acceptance),外加本仓库自己的 `project.md`、`architecture/` 模块地图与 pre-push 同步门。

两者均已移除,理由相同:机制体量超过实际收益,维护文档与绕过同步门反而成为开发负担。内容仍在 git 历史中,tag `modular-v1-frozen` 指向 v1 冻结点。
