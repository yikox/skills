---
name: writing-plexus-notes
description: Use when the user asks to save, capture, create, append, update, organize, or retrieve Markdown notes in Plexus, including the Plexus inbox and knowledge-node tree.
---

# 将笔记写入 Plexus

把 Plexus 笔记库当作本地 Markdown 文件树直接读写。

## 笔记库路径

当前配置：

```yaml
notes_root: /Users/zyc/notes
```

安装此 skill 时，安装者必须完成一次路径配置：

1. 读取 `~/.plexus/config.json` 的 `activeWorkspace`。
2. 确认它是存在的目录。
3. 直接改写本 `SKILL.md` 上面的 `notes_root`，把它替换为绝对路径。

每次使用先确认已配置路径仍存在。用户指出路径不对，或路径已失效时，重新执行上述步骤并改写本文件。不要扫描整个 home 目录，不要读取 `~/.plexus/secrets.json`；仍无法确定时再询问用户。

## Plexus 节点规则

- 文件就是数据，没有数据库；笔记正文是 `.md` 文件。
- 文件名就是节点标题，正文通常不再重复写同名一级标题。
- 一个节点由两个可以独立存在的部分组成：
  - `<路径>/<名称>.md`：节点自己的正文。
  - `<路径>/<名称>/`：节点的子节点容器。
- 同一层的同名 `.md` 文件和目录是同一个节点，不是两个条目。
- 只有正文、只有子节点容器、正文和容器同时存在，三种形态都合法。
- 给节点增加子节点时，只创建它的同名目录，不移动它的正文文件。

例如：

```text
机器学习.md             # “机器学习”节点的正文
机器学习/               # “机器学习”节点的子节点容器
机器学习/神经网络.md     # “神经网络”子节点的正文
```

`inbox/` 是草稿箱。用户只说“记一下”“随手记”，没有指定归属节点时，写到 `inbox/<YYYY-MM-DD HHmm>.md`；不要擅自发明知识分类。

## 写入步骤

1. 根据用户指定的节点或父节点确定相对路径；未指定时使用 `inbox/`。
2. 路径必须位于 `notes_root` 内，使用工作区相对路径，不接受绝对目标路径或 `..`。
3. 新笔记使用 `.md`；标题中的 `/\:*?"<>|` 要移除，避免产生非法路径。
4. 目标文件存在时先读取，再按用户意图追加或合并；绝不盲目覆盖。
5. 用户明确要新建独立笔记但同名文件已存在时，依次使用 `名称 2.md`、`名称 3.md`。
6. 写完后重新读取目标文件确认内容，并报告实际相对路径以及是新建还是更新。
