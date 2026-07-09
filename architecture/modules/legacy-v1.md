---
name: legacy-v1
code_paths:
  - legacy/**
---

# legacy-v1

## 职责

modular-programming v1 套件(en+zh,10 skill + 共享层 + 审计脚本 + 图渲染器)的冻结存档。只读参考,冻结语义见 legacy/README.md,取回用 tag `modular-v1-frozen`。

## 对外接口

- 无。不被安装、不被引用、不接需求。

## 依赖

- 无。

## 注意点

- 契约冻结:本模块出现任何代码变更都是违规,同步门点名它时应当回退变更而不是更新文档。
