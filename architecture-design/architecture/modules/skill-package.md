---
format: arch-module/v0.1
name: Skill 包装层
described: 把架构设计规则、UI 元数据和项目资源封装为可发现的 Codex skill
module_form: composite
main_subject: SKILL.md + agents/openai.yaml
status: implemented
---

# Skill 包装层

## 模块定位

Skill 包装层让本项目不只是格式原型和渲染器，而是一个可以被 Codex 发现和复用的架构设计 skill。

## 子模块清单

| 子模块 | module_kind | 说明 |
| --- | --- | --- |
| Skill Instructions | `config-rule` | 定义触发条件、工作流、引用规则和质量检查 |
| Agent UI Metadata | `config-rule` | 定义 UI 展示名、短描述和默认提示 |

## 组合边界

包装层只负责 skill 入口和发现信息。具体图结构规则仍属于规则层，渲染执行仍属于渲染运行时，示例和输出仍属于示例与产物层。

## 内部关系

Agent UI Metadata 提供用户可见入口；Skill Instructions 提供实际执行流程。Skill Instructions 再引用 Format Spec、Module Kind Taxonomy 和渲染运行时。

## 对外入口

对外入口是 `$architecture-design` skill 调用。用户通过该入口要求生成、讨论或修改模块架构设计。

## 演进规则

当架构设计流程变更时更新 Skill Instructions；当 UI 展示、默认提示或依赖声明变更时更新 Agent UI Metadata；如果新增稳定自动化脚本，应在 Skill Instructions 中说明调用方式。

## 验证方式

验证 skill 目录结构、当前项目架构图和安装后的 skill 渲染器都能正常工作。
