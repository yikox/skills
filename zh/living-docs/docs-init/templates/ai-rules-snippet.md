<!-- living-docs v2 工作流规则（docs-init 写入，合并不覆盖） -->

## living-docs 工作流

- 会话开始：读 project.md（概况 + 当前焦点）和 architecture/main-design.md；跑一次漂移检测（docs-sync 的 `check_drift.py`），有漂移先告知用户。
- 顺带更新：改到哪个模块，顺手更新 architecture/modules/<module>.md；新模块 = 新文件 + main-design.md 模块表加一行。
- 值得记的变化（行为、接口、决策）在 project.md 变更日志追加一行：日期 + 一句话 + commit。
- 会话结束：更新"当前焦点"（1-5 行：在做什么、卡在哪、下一步）。
- 可复用知识（命令、坑、约定）合并进 project.md 知识区的对应主题，不追加流水账。
- 变更日志超 50 条或 project.md 超 15KB：用 $docs-sync 归档压缩；证据不删只移。
