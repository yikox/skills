---
source_design: architecture/modules/workflow-skills/changes/2026-07-05-modular-narrator.md
level: L2
---

# 项目讲述者（modular-narrator）实现计划

> 迁移说明：原路径 `docs/superpowers/plans/2026-07-05-modular-narrator.md`，2026-07-07 审计时随设计迁入并归档（设计已 implemented）。正文保留原貌，文中路径为改名/语言分层前的历史路径。

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 新增一个独立可用的高级"项目讲述者"技能，只读调查任意项目并用通俗中文讲解，帮用户理解项目而非实现细节。

**Architecture:** 一个自包含的 `SKILL.md`（中文、内联只读纪律、不引用 `_shared`）加配套 `agents/openai.yaml`，放在 `modular-programming/modular-narrator/`。`install.sh` 通过 `find SKILL.md` 自动发现新技能，无需改安装脚本。README 的技能表、安装列表、仓库结构树需同步登记新技能。

**Tech Stack:** Markdown（SKILL.md）、YAML（agents/openai.yaml）、Bash（安装脚本验证）。无代码运行时。

## Global Constraints

- 技能与文档内容一律用**中文**撰写（`SKILL.md`、README 新增行）。
- 讲述者**独立可用**：`SKILL.md` 自包含，运行时**不引用 `_shared`、不依赖任何模块化资产或工作流**。
- 讲述者**只读**：不改代码、不出提案、不写任何文件（纯对话讲解）。
- 每次讲解回复控制在 **500–1000 字符**。
- 物理位置固定为 `modular-programming/modular-narrator/`（`install.sh` 自动发现，不改安装脚本）。

---

### Task 1: 创建 modular-narrator 技能（SKILL.md + agents/openai.yaml）

**Files:**
- Create: `modular-programming/modular-narrator/SKILL.md`
- Create: `modular-programming/modular-narrator/agents/openai.yaml`

**Interfaces:**
- Produces: 一个可被 `install.sh`（`find ... -name SKILL.md`）发现的技能目录 `modular-programming/modular-narrator/`，技能名 `modular-narrator`。Task 2 依赖此技能名与目录名。

- [ ] **Step 1: 写 `SKILL.md`（完整内容）**

创建 `modular-programming/modular-narrator/SKILL.md`，内容如下（逐字）：

```markdown
---
name: modular-narrator
description: 项目讲述者——只读地调查一个项目并用通俗语言讲解，帮用户理解"这个项目是做什么的、为什么这么设计、怎么运作"，而不是实现细节。适用于任意代码库，独立可用，不依赖任何模块化工作流或资产；只讲解，不改代码、不出提案、不写文件。中文触发词：讲述者、项目讲解、讲讲这个项目、帮我理解、这块是做什么的、这里为什么这么设计、原理讲解。English triggers: narrator, explain this project, walk me through the codebase, help me understand this project.
---

# 项目讲述者（Modular Narrator）

在"一份陌生代码库"和"用户真正读懂它"之间工作：只调查、只讲解，帮用户建立对项目的心智模型。是 `modular-architect`（出提案）的讲解版兄弟——architect 出提案，narrator 讲理解。

本技能随模块化编程套件分发，但**运行时不依赖任何模块化资产**，可独立用于任意项目。不预设、也不要求项目接入任何工作流。

## 硬边界

- **只读**：读代码、目录、文档、测试、提交历史，收集证据后回答。绝不修改代码、不创建或编辑文件、不出提案、不改架构基线、不把任何东西标记为已实现。
- **纯对话**：讲解全部在对话中完成，不产出任何讲解文档或导读文件。用户想留存另行处理。
- **有理有据**：每个结论落到具体文件 / 模块 / 函数。证据不足时明说"未确认"，绝不臆测。

## 讲解风格

- **篇幅**：每次回复控制在 500–1000 字符，通俗易懂。
- **视角**：默认讲"是什么 / 为什么这么设计 / 怎么运作"——用比喻、轮廓、设计意图帮助理解，回避实现细节。
- **按需下探**：仅当用户主动追问实现时，才下探到代码级细节，但仍用通俗语言解释，而非罗列代码。
- **分层讲解**：先给整体轮廓，再随用户追问逐层深入，不一次倾倒。遇到大问题（如"讲讲整个架构"），先给概览，把深入留给后续追问，这也天然契合篇幅约束。

## 调查方式

读一切可得的证据，无差别对待：目录结构、源码、README 及各类文档、测试、提交历史。

项目里若存在架构或模块文档（如 `architecture/main-design.md`、模块文档、`knowledge-summary.md`），就当作普通文档一并读取——有则讲得更快更准，无则从代码与结构推断。这只是文档多寡的差别，不构成特殊模式，也不构成前提条件。

## 过程

1. **理解用户想弄懂什么**：整体是什么、某个模块的职责、某处为什么这么设计，还是某个流程怎么跑通。
2. **按需调查**：从最能回答该问题的证据入手（入口文件、相关模块、对应测试），只读不改。
3. **组织成一次讲解**：500–1000 字符，先给结论 / 轮廓，再用证据支撑，落到具体文件。
4. **邀请追问**：指出还能往哪深入，把控制权交给用户，按其追问分层展开。

## 不做

- 不做设计、评估、提案、重构——那是 `modular-architect` 及主入口 skill 的职责；用户若有此需要，建议其改用相应 skill。
- 不写任何文件、不改任何代码。
- 不引用 `_shared`、不要求模块化工作流。
```

- [ ] **Step 2: 写 `agents/openai.yaml`（完整内容）**

创建 `modular-programming/modular-narrator/agents/openai.yaml`，内容如下（逐字，格式对齐 `modular-architect/agents/openai.yaml`）：

```yaml
interface:
  display_name: "Modular Narrator"
  short_description: "Investigate a project read-only and explain it in plain language"
  default_prompt: "Use $modular-narrator to explain what this project does and how it works."
```

- [ ] **Step 3: 验证技能被安装脚本发现**

Run:
```bash
cd /Users/zyc/work/skills && ./install.sh --dry-run | grep modular-narrator
```
Expected: 输出包含 `modular-narrator -> ...`（每个默认 target 各一行），证明 `find SKILL.md` 已发现新技能，无需改 `install.sh`。

- [ ] **Step 4: 验证 SKILL.md 关键约束就位**

Run:
```bash
cd /Users/zyc/work/skills/modular-programming/modular-narrator && \
  grep -q "name: modular-narrator" SKILL.md && \
  grep -q "讲述者" SKILL.md && \
  grep -q "500–1000 字符" SKILL.md && \
  grep -q "只读" SKILL.md && \
  ! grep -q "_shared" SKILL.md && \
  echo "OK: name/触发词/篇幅/只读 就位且未引用 _shared"
```
Expected: 打印 `OK: name/触发词/篇幅/只读 就位且未引用 _shared`（`_shared` 未出现，证明自包含）。

- [ ] **Step 5: Commit**

```bash
cd /Users/zyc/work/skills && \
  git add modular-programming/modular-narrator/SKILL.md modular-programming/modular-narrator/agents/openai.yaml && \
  git commit -m "feat: add modular-narrator (project narrator) skill

Read-only advisory skill that investigates any project and explains it in
plain Chinese (500-1000 chars per reply), focused on understanding rather
than implementation. Self-contained, no _shared dependency.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: 在 README 登记 modular-narrator

**Files:**
- Modify: `README.md`（技能分工表约 67 行、安装列表约 321 行、仓库结构树约 343 行）

**Interfaces:**
- Consumes: Task 1 产出的技能名 `modular-narrator` 与目录 `modular-programming/modular-narrator/`。

- [ ] **Step 1: 在 Skills 分工表新增一行**

在 `README.md` 中 `modular-architect` 表格行（以 `| \`modular-architect\` |` 开头的行）之后，插入一行：

```markdown
| `modular-narrator` | 高级：只读调查项目并通俗讲解"是什么 / 为什么这么设计 / 怎么运作"，帮用户理解项目（独立可用，不依赖工作流） | 对话式讲解，每次 500–1000 字符（不产出文件） |
```

- [ ] **Step 2: 在安装列表新增一项**

在 README "安装脚本会安装" 代码块中，`modular-architect` 那一行之后新增一行：

```text
modular-narrator
```

（该代码块位于 `~/.claude/skills` 段落之后，以 `_shared` 开头、逐行列出各技能名。）

- [ ] **Step 3: 在仓库结构树新增一项**

在 README "仓库结构" 代码块中，`modular-architect/` 那一行之后新增一行（保持两空格缩进）：

```text
  modular-narrator/
```

- [ ] **Step 4: 验证三处登记齐全**

Run:
```bash
cd /Users/zyc/work/skills && grep -c "modular-narrator" README.md
```
Expected: `3`（技能表 1 处、安装列表 1 处、结构树 1 处）。

- [ ] **Step 5: Commit**

```bash
cd /Users/zyc/work/skills && git add README.md && \
  git commit -m "docs: register modular-narrator in README

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Self-Review

**1. Spec coverage**（对照 `architecture/modules/workflow-skills/changes/2026-07-05-modular-narrator.md`，迁移前路径 `docs/superpowers/specs/2026-07-05-modular-narrator-design.md`）：
- 角色定位 / 独立可用 → Task 1 Step 1（SKILL.md 正文 + description）。
- 硬边界（只读 / 纯对话 / 有理有据 / 只读纪律内联不引用 `_shared`）→ Task 1 Step 1 "硬边界" 段，Step 4 校验未引用 `_shared`。
- 讲解风格（500–1000 字符 / 默认高层 / 追问才下探 / 分层）→ Task 1 Step 1 "讲解风格" 段。
- 调查方式不分模式、模块文档当普通文档 → Task 1 Step 1 "调查方式" 段。
- 触发词（中文）→ Task 1 Step 1 description。
- 语言中文 → 全程中文内容 + Global Constraints。
- 落地形态 SKILL.md + agents/openai.yaml + 物理位置 → Task 1 Step 1/2，Step 3 校验发现。
- YAGNI（不落文件 / 不做提案 / 无双模式 / 无工作流依赖）→ Task 1 "不做" 段。
- 覆盖完整，无缺口。README 登记为落地所需的附带同步（spec"落地形态"隐含），已由 Task 2 承担。

**2. Placeholder scan：** 无 TBD/TODO/"稍后实现"；SKILL.md、openai.yaml、README 三处新增行均给出逐字完整内容。通过。

**3. Type consistency：** 全程技能名统一为 `modular-narrator`，目录 `modular-programming/modular-narrator/`，display_name `Modular Narrator`，前后一致。通过。
