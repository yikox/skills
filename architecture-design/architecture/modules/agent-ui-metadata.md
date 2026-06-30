---
format: arch-module/v0.1
name: Agent UI Metadata
described: 定义 skill 在 Codex UI 中的展示名称、短描述和默认提示
module_form: atomic
module_kind: config-rule
main_subject: agents/openai.yaml
status: implemented
---

# Agent UI Metadata

## 模块定位

Agent UI Metadata 是 Codex 桌面端和 skill 列表读取的界面元数据。它不定义架构设计流程本身，只负责让用户能识别并快速调用 `architecture-design` skill。

## 配置结构

当前实现位于 `agents/openai.yaml`：

- `interface.display_name`：UI 展示名。
- `interface.short_description`：技能列表里的短描述。
- `interface.default_prompt`：默认调用提示，显式包含 `$architecture-design`。

## 合并与优先级

该文件是 skill 包内的 UI 元数据来源。流程规则仍以 `SKILL.md` 为准；当两者描述不一致时，应更新 `agents/openai.yaml` 以匹配 `SKILL.md`。

## 生效时机

Codex 枚举本地 skills、展示 skill chip 或插入默认提示时读取该元数据。

## 扩展方式

如果后续需要图标、品牌色或额外依赖声明，应通过 skill-creator 的 `generate_openai_yaml.py` 生成，避免手写字段格式漂移。

## 验证方式

使用 skill-creator 的 `quick_validate.py` 校验 skill 目录；更新 UI 元数据后检查 `agents/openai.yaml` 是否仍与 `SKILL.md` 的能力边界一致。
