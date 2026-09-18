# skills 仓库

个人 agent skills 的源仓库。只有 skill 源码与安装脚本,不含任何项目治理流程。

## 约定

- AI 协作规则只此一份;`CLAUDE.md` 通过 `@AGENTS.md` 引入,不要两边各写一份。
- 提交信息按 `$git-commit`:`[tag] 中文摘要` 主题行,末尾加 `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`。
- 文档与 skill 正文一律中文,不维护英文镜像。
- 独立 skill 之间不互相点名:边界靠描述任务自身的性质来划,不写「这种情况去用 X」。点名等于把对方的存在与命名写进自己的正文,对方改名或移除时这里就是死引用。同一套件内配套的 skill 不受此限,它们本来就要互相衔接。
- 请求用户确认重大决策(L3 级)前,先给 3-8 条要点摘要(修改重点、歧义点、风险),让用户不读全文也能决策。
- 删除、重写 git 历史、改动公共接口这类不可逆操作,先列清单再动手,不要边做边扩范围。
- `install.sh` 必须兼容 bash 3.2(macOS 自带):不用 `readarray`、关联数组、globstar。

## 环境坑

- EnterWorktree 建出的 worktree 可能缺本地未推送 commit(baseRef 默认 origin/main);worktree 内 `git merge --ff-only main` 补齐(2026-07-03 实证)。
- ExitWorktree remove 会误报"N commits 将丢失":先 `git merge-base --is-ancestor <tip> main` 确认已包含,再 discard。
- 对同一个文件并行发起多个编辑会互相覆盖(各自基于同一份原始内容写回,后写者胜),只有最后一个生效。同一文件的多处改动必须串行,或合并成一次整体写入。
- 在 skill 目录里跑 Python 会生成 `__pycache__`,已加进 `.gitignore`。
