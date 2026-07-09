---
name: docs-acceptance
description: living-docs 临时验收员。docs-init 或 docs-sync 完成后必须调用：按验收清单逐条自查、请用户确认，结果追加进 acceptance-log.md。套件毕业（连续 5 次全过）后拆除本 skill。
---

# docs-acceptance（临时脚手架）

living-docs 套件的验收员。存在的理由：**对套件本身的任何修改，唯一合法的输入是本 skill 产出的 acceptance-log.md 中的记录**——不允许基于"看着不对劲"改套件。

## 流程

1. 确认被验收对象：本次完成的是 docs-init 还是 docs-sync。
2. 按下方对应清单逐条自查，每条给出 `通过` 或 `存疑`，各附一行证据（文件路径、行数、耗时等可核事实）。
3. 把结果呈现给用户，请其确认或否决；否决必须让用户说出原因（原因就是套件的修改依据）。
4. 把记录追加到 acceptance-log.md（与 project.md 同目录，无则创建）。
5. 统计日志：若已连续 5 次全过且无新问题，提醒用户套件可毕业——拆除本 skill，并从 docs-init / docs-sync 中删去调用要求。

## docs-init 验收清单

1. 产物齐全：project.md 四章齐全；architecture/main-design.md 存在（frontmatter 含 sync_branches）；每个模块有 modules/<name>.md；git 项目已装 pre-push 同步门（`.git/hooks/pre-push` 可执行且指向 check_sync.py）。
2. 可读性：project.md 各章开头一屏内；main-design.md 不超过两屏；每个模块文档不超过 80 行。
3. 模块划分在用户确认之后才落盘，未经确认不得写入。
4. AI 规则合并不覆盖既有内容，首次创建或修改 CLAUDE.md/AGENTS.md 前经过确认。
5. 向用户提问不超过 3 个。
6. 终检：用户能不看代码回答——系统有哪些模块、各管什么、"改 X"应落在哪个模块。

## docs-sync 验收清单

1. 点名清单与实际 git diff 相符（抽查至少一个被点名模块核对）。
2. 处理完成后，受影响 range 复跑 check_sync 通过（exit 0）；全程未用 `--no-verify`，所有 skip 出口都以 `Arch-Sync: skip` 带理由写进 commit message。
3. 每个被点名模块有明确结论：已更新文档，或 Arch-Sync skip（两者都算对齐）。
4. 归档/压缩后证据仍可追溯：日期、commit、结论没有被删除，只被移动或以链接摘要保留。
5. 全程不超过 10 分钟；超时记录原因（漂移积累量、模块数）。
6. project.md 四章仍符合写法规则（当前焦点 1-5 行、变更日志一条一行、知识按主题合并）。

## acceptance-log.md 记录格式（追加式）

```markdown
## YYYY-MM-DD <docs-init|docs-sync> — <全过|有存疑|用户否决>

- 清单：n 通过 / m 存疑（存疑项编号及一行原因）
- 用户结论：确认 / 否决（原因）
- 用户备注：…
```

## 硬规则

- 自查证据必须可核（路径、数字、命令输出），不接受"看起来没问题"。
- 用户否决时不当场修套件；先记日志，修改另行发起并引用日志条目。
- 本 skill 是脚手架：毕业后删除，不要长期保留。
