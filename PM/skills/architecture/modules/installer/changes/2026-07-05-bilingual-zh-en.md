---
title: 中英双语版本（语言分层 + install 语言参数）
level: L2
status: implemented
review_status: reviewed
primary_module: installer
impacted_modules: [workflow-skills, shared-references, shared-assets, audit-checker, graph-tooling]
---

# 中英双语版本（语言分层 + install 语言参数）

## Request

用户观察到 skill 用中文时表现更好，希望在保留英文版的同时扩充一份中文版：

- 目录按语言分层为 `<lang>/modular-programming/`（语言在最外层，因为 skills 仓库未来可能不止 modular-programming 一个套件，外层分语言便于记住"两种语言要同步"）。
- 安装时用 `./install.sh zh` 或 `./install.sh en` 选择语言。
- 保持中文 `README.md` 为主，补一份英文 `README_EN.md`，双向引用。

用户初判 L1，讨论后确认为 **L2**：本次实质是目录结构重构 + install 对外契约变化，翻译内容本身才是轻量部分。

## Current Module State

- `install.sh` 扫描 `$repo_dir` 下所有 `SKILL.md`，把每个技能目录与 `modular-programming/_shared` 平铺复制到目标 skills 目录；契约为 `./install.sh [--dry-run] [target_dir ...]`。
- 技能套件位于单一目录 `modular-programming/`（10 个技能 + `_shared`）。
- `README.md` 为中文；无英文版。
- 本仓库自审计、渲染、验证命令均以 `modular-programming/...` 为路径前缀（见 PM Testing and Validation）。

## Target Module Design

### 目录结构

```text
skills/                              # 仓库根（已叫 skills）
├── en/
│   └── modular-programming/         # = 现有 modular-programming/ 整体 git mv 进来（英文，主/源）
├── zh/
│   └── modular-programming/         # en 的中文翻译镜像，结构逐目录对等
├── install.sh                       # 加语言参数
├── README.md                        # 中文（主，不动语言）
├── README_EN.md                     # 新增英文
├── PM/                              # 本仓库自身项目记忆（元层，不分语言）
└── docs/                            # superpowers 流程存档（不分语言）
```

安装产物结构不变：`./install.sh <lang>` 仍把选定语言下的技能目录 + `_shared` **平铺**到目标 skills 目录，保证安装后 `../_shared/` 相对引用成立。目标目录本身不出现语言层——用户装哪个语言，目标就是那个语言的单份。

### install.sh 新契约

```text
./install.sh <lang> [--dry-run] [target_dir ...]
  <lang>        必填，zh | en。第一个非选项位置参数解释为语言。
  target_dir    其余位置参数为目标目录，默认 ~/.agents/skills ~/.codex/skills ~/.claude/skills
```

- `shared_dir` 与 SKILL.md 扫描根从 `$repo_dir` 改为 `$repo_dir/<lang>/modular-programming`。
- 缺 `<lang>` 或值非 zh/en → 打印 usage 并以非零码退出（**不设隐式默认语言**：语言是本次核心语义，隐式默认会让人不知道装了哪个语言）。
- `--dry-run`、deprecated 清理列表、rsync `-a --delete` 语义不变。

### 翻译边界（对"全量双份"的务实细化）

**翻译（zh 与 en 各一份散文）**：

- 10 个 `SKILL.md` 正文与 front matter 的 `description`（保留其中的英文触发关键词，以免降低触发准确率）。
- 各技能 `agents/` 下的 agent 定义散文。
- `_shared/references/*.md`、`_shared/assets/*.md`（模板散文）、`_shared/examples/*` 的说明性散文。
- `_shared/references/vocab.md` 的**说明性散文**。

**保持英文单源（zh 目录内物理相同，不翻译）**：

- 全部 `*.py`（`check_modular_project.py`、`render_modular_graph.py`、`serve_modular_graph.py`、`tests/`）——是代码不是文案。
- `vocab.md` 的**词表 token**（`atomic`、`function-flow`、`uses`、`reviewed` 等）。
- 所有模块/设计/ADR front matter 的**机器字段值 token**（`module_form`、`module_kind`、`status`、`review_status`、`relation_kind` 等的取值）。
- 架构图 JSON 的关系 token。

理由：这些 token 是 audit-checker 的解析契约。若在 zh 版翻成中文，则 zh 版所有模块文档 front matter 也须用中文 token 并需另一套 checker，两语言数据格式分叉、checker 失效。翻译词表 token 有害无益。

## Contract Impact

**契约变化（破坏性，需在 README/PM 同步）**：

- `install.sh` 从"无位置参数即安装"变为"首参必须是 zh|en"。旧的 `./install.sh`（无参）将报 usage 退出。这是有意的破坏——本次的核心就是让语言显式化。
- 已安装到 `~/.claude/skills` 等目标的产物结构不变，因此**已安装端无需适配**，重装即覆盖为选定语言。

**路径引用连锁更新（不改行为，但会误导未来工作）**：

- `README.md` / 新 `README_EN.md` 的安装与命令示例。
- PM `Testing and Validation` 与模块文档中以 `modular-programming/...` 为前缀的自审计/渲染命令 → 统一改用 `en/modular-programming/...`（en 为主/源，代码与 zh 相同）。
- `architecture/main-design.md` 的 Scope 描述 + 各模块 `code_paths` 前缀（改为 `en/modular-programming/...`），并在 Scope 说明 `zh/` 为 en 的中文翻译镜像、结构对等、baseline 以 en 为准（**baseline 不双份**，它是本仓库元层记忆）。

## Implementation Outline

1. `git mv modular-programming en/modular-programming`（保留历史）。
2. `cp -r en/modular-programming zh/modular-programming` 生成 zh 骨架（含相同 `*.py` 与 token）。
3. 翻译 zh 下散文：SKILL.md（正文 + description 散文，保留英文触发词）、agents/、references、assets、examples、vocab.md 散文。**不动** `*.py` 与词表/front-matter token。
4. 改 `install.sh`：解析首个位置参数为 lang（校验 zh|en），其余为 target；扫描根与 `shared_dir` 加 `<lang>/modular-programming` 前缀。
5. 新增 `README_EN.md`（现有中文 README 内容的英文版），`README.md` 顶部加语言切换链接指向 `README_EN.md`，反之亦然；更新两份 README 的 install 示例为 `./install.sh zh|en`。
6. 更新路径引用：PM Testing/Validation 命令前缀、模块文档 code_paths、main-design Scope。
7. 更新 architecture baseline（installer 模块公共契约、main-design Scope）。

## Validation

- `./install.sh en --dry-run` 与 `./install.sh zh --dry-run` 各列出 10 个技能目录 + `_shared`，退出码 0；`./install.sh`（缺 lang）报 usage 非零退出。
- 自审计（用 en 版 checker）：`python3 en/modular-programming/modular-audit/scripts/check_modular_project.py PM/skills --repo-root . --exclude 'docs/**' --exclude 'PM/**'` 0 error。
- checker 单测：`python3 -m unittest discover -s en/modular-programming/modular-audit/tests` 全绿。
- zh 版 checker 对 zh 自身内容的 sanity：`python3 zh/modular-programming/modular-audit/scripts/check_modular_project.py <zh 内一个含 PM 的样例或跳过>`（zh 内无 PM，主要验证脚本 py_compile 与词表解析不因散文翻译报错）。
- `git diff --check` 干净；`git mv` 后 en 目录 diff 为纯重命名（历史保留）。
- 抽查：zh 某模板/示例的 front matter token 与 en 完全一致（证明 token 未被翻译）。

## Risks

- **翻译漂移**：zh/en 散文双份，未来改一处忘另一处。缓解：语言置于最外层（用户主动诉求，便于记忆同步）；可在后续加一个"结构对等性"检查（en/zh 目录树与 token 一致性）作为独立 backlog，不在本次范围。
- **token 误翻**：若翻译时不慎翻了 vocab/front-matter token，checker 对 zh 失效。缓解：验证步骤含 token 抽查；zh 骨架用 `cp` 自 en 生成，token 天然一致，只改散文。
- **install 破坏性**：缺 lang 报错可能让沿用旧命令的人踩一下。缓解：usage 明确提示 zh|en；README 同步。
- **接近 L3**：本变更跨全部模块目录搬迁 + install 契约，逼近架构级。判定为 L2 的依据是各模块**职责与公共契约不变**，仅新增语言维度并整体搬迁；主模块单一为 installer。若评审认为动了模块边界语义，升级 L3。

## Open Questions

- README 语言切换：主 README 保持中文（已定）。README_EN 是否需要与中文逐节完全对齐，还是可精简？倾向逐节对齐以免英文用户信息缺失。
- 后续是否要一个 en↔zh 结构对等性校验脚本（防漂移）——建议记为独立 backlog，不阻塞本次。

## Review Notes

- Review status: reviewed（modular-review，2026-07-05）。无阻塞机械缺陷（补录了 PM Modular Design Index 索引行）。
- L2 判定核对通过：file organization 重构，模块数量/职责/边界不变，无 cross-module 契约变化；属接近 L3 的边界案例，已由用户确认 L2。
- 需人类接受的方向点（非阻塞）：install 破坏性契约、baseline 只描述 en（zh 为镜像不双份）、install 缺 lang 是否报错 vs 默认 en——均纳入决策摘要待用户确认。

## Decisions（2026-07-05 用户接受）

- 接受设计并开始实现（status: accepted）。
- install 缺 lang → 报 usage 非零退出（不设隐式默认）。
- 翻译边界：只翻散文；`*.py` 与 vocab/front-matter 机器 token 保持英文单源。

## Implementation（2026-07-05/06）

- 结构层 commit `7cf18d3`：git mv → en/、zh 骨架、install.sh 语言参数、README_EN、baseline 更新。
- 翻译 commit `03d55f3`：6 个并行 subagent 完成 zh 散文中文化（39 文件：9 SKILL + 10 openai.yaml + 20 _shared；narrator 等本已中文的文件跳过）。
- 意外发现（已记入 baseline Scope）：en/ 实为中英混合（历史 docs-language=zh），非纯英文源。若需 en/ 纯英文化，属后续独立工作。
- token 完整性验证全绿：机器 token 无中文污染；vocab.md 及全部 `*.py`/`*.arch.json` 在 en/zh 逐字一致；`install zh --dry-run` 10 技能；zh 渲染器可渲染示例；en 版 checker 自审计 0/0；`git diff --check` 干净。
- 未完成：实际 `./install.sh <lang>` 同步到 `~/.claude/skills` 等因权限/额度未运行（历史一贯 pending，dry-run 已验证）。
