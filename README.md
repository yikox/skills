# living-docs Skills

> v1(modular-programming,10 skill 治理套件)已于 2026-07-09 冻结,存档于 [`legacy/`](legacy/README.md),tag `modular-v1-frozen`。

让 AI agent 用**两份文档**维持项目的可持续,而不是用流程:

1. **项目文档 `project.md`**:概况 / 当前焦点 / 知识 / 变更日志,四章固定,每章有明确的读者、写法和压缩规则。解决"跨会话失忆"和"知识沉淀成流水账"。
2. **设计文档 `architecture/`**:main-design.md(一到两屏的模块地图)+ modules/*.md(每模块五节,≤80 行)。解决"越写越乱"和"改动无处定位"——可以直接说"我要改某某模块的 XX"。

准确性不靠流程门禁,靠两件事:**顺带更新**(改到哪个模块就顺手更新它的文档,写进项目 CLAUDE.md 的一条规则)+ **git 对账**(`.last-sync` 锚点,`git diff ∩ code_paths` 检测"代码动了、文档没动")。

## 三个 skill

| Skill | 什么时候用 |
| --- | --- |
| `docs-init` | 新项目接入:建两份文档 + 写入顺带更新规则 |
| `docs-sync` | 漂移对账、项目文档归档压缩、旧文档体系一次性迁移 |
| `docs-acceptance` | 临时验收员:init/sync 完成后自动调用,结果记入 acceptance-log.md;连续 5 次全过后拆除毕业 |

对套件本身的修改,唯一合法输入是 acceptance-log.md 里的使用证据——这是 v1 三十次"看着不对劲"式修改永不收敛的教训。

## 使用

```text
Use $docs-init 给这个项目接入 living-docs。
Use $docs-sync 对账/压缩项目文档/迁移旧文档体系。
```

## 安装

```sh
./install.sh zh              # 安装(默认 ~/.agents、~/.codex、~/.claude 的 skills 目录)
./install.sh zh --dry-run    # 预演
```

中文单源,不维护英文镜像。安装会顺带清理旧 v1 skill(`modular-*`、`_shared`)。另含独立 skill `personal-style`(个人编码风格约定)。

## 仓库结构

```text
project.md            # 本仓库自己的项目文档
architecture/         # 本仓库自己的模块地图
zh/living-docs/       # v2 套件:docs-init / docs-sync / docs-acceptance
zh/personal-style/    # 独立 skill
legacy/               # v1 冻结存档(只读)
install.sh
```

设计与决策沿革见 `architecture/changes/2026-07-09-living-docs-v2-redesign.md`。
