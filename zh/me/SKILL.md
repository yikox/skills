---
name: me
description: 处理任何开发相关请求时必定加载的个人规则入口，包括写码、改码、接口设计、重构、评审、清理及开发资源下载；按任务情境读取对应专题文档。中文触发词：个人风格、编码风格、我的风格、风格约定。
---

# me：个人开发规则入口

每个开发相关请求都必须加载本技能。入口只负责少量通用约定和专题文档路由；符合多个场景时，读取全部匹配文档，并在对应工作开始前读取。

## 专题文档触发规则

- **设计新项目或模块、重构项目、进行大版本改动时**，在开始方案设计前读取 [`references/code-design.md`](references/code-design.md)。
- **代码改动进入收尾、交付或提交阶段，任务需要整理工作区或测试材料，或需要执行任何 Git / `gh` 操作时**，在收尾或首次 Git 操作前读取 [`references/code-delivery.md`](references/code-delivery.md)。
- **准备、配置或使用机器环境，或下载依赖、工具、数据、模型时**，在开始环境操作或下载前读取 [`references/machine-environment.md`](references/machine-environment.md)。
