---
name: docs-init
description: 为项目建立 living-docs 两份文档——项目文档 project.md 与设计文档 architecture/（模块地图），并把"顺带更新"规则写入项目 AI 文档。新项目接入、空白项目初始化时使用；已有旧文档体系的项目迁移改用 docs-sync。
---

# docs-init

living-docs 的产品是两份文档，不是流程。init 只做一件事：让这两份文档以正确结构落盘，并把维护习惯（一条规则）写进项目 AI 文档。

## 两份文档

1. **project.md（项目文档）**：概况 / 当前焦点 / 知识 / 变更日志，四章固定。
2. **architecture/（设计文档）**：main-design.md（系统一段话 + 模块表 + 协作描述）+ modules/<name>.md（每模块五节：职责 / 对外接口 / code_paths / 依赖 / 注意点）。

模板在 `templates/`，各章的读者与写法/压缩规则以 `templates/project-template.md` 内注释为准。

## 流程

1. **定位置**：默认项目根放 project.md 与 architecture/；用户另有偏好则遵守。
2. **收集最少信息**：项目目标、怎么跑起来。有代码先扫代码推断（入口、目录结构、构建/测试命令），只问推断不出的。**向用户提问不超过 3 个。**
3. **起草**：
   - project.md：概况按已知信息填写；当前焦点写接入时的状态；变更日志首条记 init。
   - architecture/：从代码结构推断模块划分，顶层模块建议 3-9 个；每模块一份文档。不确定的边界如实标注"(不确定)"，不假装明确。
4. **确认后落盘**：给用户看草稿要点——模块清单 + 每模块一句话职责 + 你不确定的点。**模块划分必须经用户确认才写入。**
5. **安装同步门**：git 项目把 `templates/pre-push-hook.sh` 装到 `.git/hooks/pre-push`（替换其中 ARCH_DIR 与 CHECK_SYNC_PATH 为实际路径，`chmod +x`；已有 pre-push hook 则追加调用，先确认）；main-design.md frontmatter 写 `sync_branches`（默认 main）。非 git 项目跳过并告知同步门不可用。
6. **写入规则**：把 `templates/ai-rules-snippet.md` 合并进项目的 CLAUDE.md / AGENTS.md（合并不覆盖既有内容；首次创建或修改前先向用户确认）。
7. **验收**：完成后必须调用 $docs-acceptance 验收本次 init。

## 硬规则

- 可读性第一：project.md 各章开头一屏内；main-design.md 一到两屏；模块文档 ≤80 行——超限说明模块该拆，或文档在复述代码。
- project.md 不写实现细节叙述（那属于 commit message 和模块文档）。
- code_paths 用仓库相对 glob，每个承载行为的路径归属一个模块；这是同步门的映射表。文档准确性靠提交纪律（文档与代码同一颗 commit）加 push 时的同步门保证，日常没有别的流程。
