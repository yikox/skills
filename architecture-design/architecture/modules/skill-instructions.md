---
format: arch-module/v0.1
name: Skill Instructions
described: 定义 architecture-design skill 的触发条件、工作流和质量检查
module_form: atomic
module_kind: config-rule
main_subject: SKILL.md
status: implemented
---

# Skill Instructions

## 模块定位

Skill Instructions 是 Codex 使用本项目能力的主入口。它把架构设计流程固化为 skill 规则，覆盖老项目架构基线生成、新项目模块设计讨论、已有架构文档的模块级修改。

## 配置结构

- front matter `name` 和 `description` 负责触发 skill。
- Core Model 规定 Markdown 模块文档、`*.arch.json` 图结构、HTML/SVG 渲染产物三层分工。
- Workflow Decision 根据项目状态选择老项目、新项目或已有文档修改流程。
- Quality Checklist 规定输出前必须检查的文档、关系、渲染和链接完整性。

## 校验规则

Skill Instructions 明确废弃 `.mdx` 图源，要求图结构只使用 `*.arch.json`。它还要求模块分类读取 Module Kind Taxonomy，图结构书写读取 Format Spec，渲染后检查 warnings。

## 生效时机

当用户请求架构设计、架构修改、生成当前项目模块架构、讨论新项目模块边界或更新现有模块设计时生效。

## 扩展方式

新增工作流时优先扩展 `SKILL.md` 的流程段落；新增格式细节时优先扩展 `docs/` 下的参考文档，避免把所有细节塞进 skill 主体。

## 验证方式

使用 skill-creator 的 `quick_validate.py` 校验 skill 结构；使用渲染器校验架构图引用和 HTML/SVG 输出。
