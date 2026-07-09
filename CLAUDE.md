# skills 仓库

## living-docs 工作流

- 会话开始:读 project.md(概况 + 当前焦点)和 architecture/main-design.md。
- 顺带更新:改到哪个模块,**同一颗 commit** 里顺手更新 architecture/modules/<module>.md;新模块 = 新文件 + main-design.md 模块表加一行。
- 同步门:push main 前 pre-push hook 会跑 check_sync.py;被拦下时要么补文档,要么(确实无需更新时)commit message 加 `Arch-Sync: skip <module> <一句话理由>`。不用 `--no-verify` 绕过。
- 值得记的变化(行为、接口、决策)在 project.md 变更日志追加一行:日期 + 一句话 + commit。
- 会话结束:更新"当前焦点"(1-5 行:在做什么、卡在哪、下一步)。
- 可复用知识(命令、坑、约定)合并进 project.md 知识区的对应主题,不追加流水账。
- 变更日志超 50 条或 project.md 超 15KB:用 $docs-sync 归档压缩;证据不删只移。

## 本仓库特有约定

- `legacy/` 契约冻结:任何变更都是违规,同步门点名它时回退变更而不是更新文档。
- 对 living-docs 套件本身的修改,唯一合法输入是 acceptance-log.md 中的记录。
- commit 末尾加 `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`。
