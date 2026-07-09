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
