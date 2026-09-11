# living-docs 验收日志

<!-- docs-acceptance 追加式记录。对套件本身的修改,唯一合法输入是本日志。 -->

## 2026-07-09 docs-sync(本仓库 v1→v2 一次性迁移)— 全过

- 清单:6 通过 / 0 存疑
  1. 漂移清单与 diff 相符:三分支实测——对齐(exit 0)、DRIFT(改 docs-sync/SKILL.md 后点名 living-docs-suite,exit 1)、ORPHAN(orphan-test.txt 被点名,exit 1)。
  2. .last-sync == 迁移完成时 HEAD(f447354);其后仅记账文件(PM/**,在 ignored_paths)变更。
  3. 漂移模块结论明确:迁移重建了全部 4 份模块文档 + main-design(v1 的 6 模块地图随冻结整体替换)。
  4. 证据可追溯:v1 记账文档以 v1- 前缀移入 archives/(project-management、knowledge-summary、v1-baseline/),commit 链完整保留在 project.md 变更日志。
  5. 耗时:迁移 + 验证约 8 分钟,达标。
  6. project.md 四章合规:当前焦点 2 行、变更日志一条一行、知识按主题四小节。
- 用户结论:确认(2026-07-09,与迁根条目一并确认)。计入连续全过:1/5。
- 备注:与设计文档的一处偏差已记录(无 _shared 层,skill 自包含;原因:installer 平铺布局 + _shared 在清理列表)。计数规则:本条在用户确认前不计入"连续 5 次全过"。

## 2026-07-09 docs-sync(文档迁至项目根 + 丢弃 v1 产物 + 装机清理)— 有存疑

- 清单:5 通过 / 1 存疑
  1. 通过——漂移清单与 diff 相符:检测报"对齐,变更 1 路径已覆盖";锚前的 install.sh 变更(+1 行,deprecated 补 project-management-docs)人工核对,不改 installer 契约,确认无需更新文档。
  2. **存疑**——.last-sync(11b10f05)≠ HEAD(79b47553):锚点自身入库导致永远落后一颗 commit(写锚→提交→HEAD 前移)。语义上对齐成立(锚后仅 .last-sync 与本日志变更,均被排除/忽略),但清单条文与机制有出入。**套件待改进项:锚点语义应定义为"锚后仅允许 ignored/arch 路径变更",或锚改为 gitignore 的本地文件。**
  3. 通过——漂移模块结论明确:installer 确认无需更新(见第 1 条)。
  4. 通过——用户明示"老的东西都可以丢弃",覆盖"不删只移"默认:v1 记账产物删除,变更日志保留全部 commit 指针,tag modular-v1-frozen 可整体回溯。
  5. 通过——全程约 5 分钟。
  6. 通过——四章合规:当前焦点 2 行、变更日志一条一行、知识按主题小节;project.md 3.6KB;模块文档 19-28 行,main-design 26 行。
- 用户结论:确认(存疑项认可语义对齐解释,作为改进证据留存,未当场修改套件)。本条非全过,不计入连续计数。
- 用户备注:无

## 2026-07-09 套件修改 v2.1(变更记录,非 init/sync 运行)

- 依据:本日志 2026-07-09 存疑条目(锚点入库永远落后 HEAD 一颗 commit)+ 用户提议的合入时检查设计。
- 变更:废除 .last-sync 锚点;check_drift.py → check_sync.py(range 门模式,sync_branches 默认 [main],Arch-Sync: skip 放行出口);docs-init 安装 pre-push hook;docs-sync 改为门后对齐/抽查/压缩/迁移;验收清单第 1/2 条改为门语义。
- 验证:同步(exit 0)/不受管分支放行/DRIFT 点名/skip 放行/hook 随 push --dry-run 触发,五条路径实测通过;commit ac5bbfe、0071b8a。
- 状态:待试用期检验;存疑条目就此关闭。

## 2026-09-11 套件修改(变更记录,非 init/sync 运行)

- 依据:① 用户当场指令"整体调整优化,使架构更合理、职责更清晰、功能更完整";② 本次真实使用中观察到的失败(见下)。两者都属日志允许的输入,不是"看着不对劲"。
- 观察到的失败:
  1. 同步门核心脚本的绝对路径被烧进 hook 模板,而脚本只存在于用户的全局 skill 目录 → 换机器或未装 skill 时门静默失效。
  2. `check_sync.py` 的配置类错误一律 `sys.exit("文本")`,退出码恒为 1,与文档承诺的"2=配置错误"不符,会把配置问题混进"有漂移"。
  3. `git diff --name-only` 对重命名只报新路径,文件跨模块移动时源模块被漏点名。
  4. 一次性删除无归属文件时 ORPHAN 无法通过,而当时唯一出口是永久改 ignored_paths 配置。
  5. docs-init / module-template / docs-sync 三处对"四节还是五节"表述不一致。
  6. docs-sync 的抽查命令写相对路径 `scripts/check_sync.py`,在目标项目里不成立。
- 变更:pre-push hook 改为自包含(与 check_sync.py 成对装到 `.git/hooks/`,用自身目录定位);新增 `die()` 显式传退出码;diff 加 `--no-renames`;新增 `Arch-Sync: skip <路径 glob>` 一次性放行 ORPHAN;统一模块文档为"frontmatter code_paths + 正文四节";抽查命令改用 `.git/hooks/` 里的副本;新增 `tests/test_check_sync.py`;docs-init 验收清单第 1 条改为核对两份 hook 文件。
- 验证:`test_check_sync.py` 10/10 通过;另在本地 bare 仓库端到端跑通四路径——首次 push 放行、DRIFT 拦截、补文档后放行、`Arch-Sync: skip` 放行;本仓库自身已装同步门并实跑通过。
- 状态:待试用期检验。本次未改动验收清单的判定标准,故不重置"连续全过"计数。
