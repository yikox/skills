---
name: writing-plexus-notes
code_paths:
  - zh/writing-plexus-notes/**
---

# writing-plexus-notes

## 职责

指导 agent 把 Markdown 笔记安全写入 Plexus 工作区，记录笔记库路径自配置、知识节点双面结构、草稿箱和同名冲突处理规则。

## 对外接口

- `$writing-plexus-notes`：SKILL.md 协议触发。
- `notes_root`：写在 skill 自身文档中的本机 Plexus 笔记库绝对路径。

## 依赖

- Plexus 的 `~/.plexus/config.json` 提供 `activeWorkspace`。
- 笔记库是可读写的本地 Markdown 文件树。

## 注意点

- 同层 `<名称>.md` 与 `<名称>/` 是同一个知识节点的正文和子节点容器。
- 未指定归属时写入 `inbox/`，不擅自发明知识分类。
- 已有文件必须先读再合并，不能盲目覆盖。
