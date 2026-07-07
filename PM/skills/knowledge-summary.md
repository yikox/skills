# skills 仓库 Knowledge Summary

Last updated: 2026-07-04

## Verified Commands

| Command | Purpose | Notes |
| --- | --- | --- |
| `python3 en/modular-programming/modular-audit/scripts/check_modular_project.py PM/skills --repo-root . --exclude 'docs/**' --exclude 'PM/**' --exclude 'zh/**'` | 项目记忆一致性检查（自审计标准命令） | 退出码 1 = 有 error；须豁免 zh 镜像 |
| `python3 en/modular-programming/_shared/scripts/render_modular_graph.py <in.arch.json> -o <out.html> --svg-output <out.svg>` | 渲染高级架构图 | stdlib-only；图是给人看的高级可视化，不是默认 AI baseline |
| `python3 -m unittest discover -s en/modular-programming/modular-audit/tests` | checker 单元测试 | 含 vocab drift-guard |
| `./install.sh <zh\|en> --dry-run` | 预演技能安装 | 语言参数必填；默认目标 ~/.agents、~/.codex、~/.claude 的 skills 目录 |

## Architecture Facts

- 默认 AI-readable baseline 是 `architecture/main-design.md` + `architecture/modules/*.md`；图是高级可视化能力，只有项目维护图时才作为关系的权威可视化来源。
- `architecture/graphs/*.arch.json` 可缺省；checker 仅在图文件存在时校验图端点、关系词表、group/interface/scope 与 Dependencies 子集。
- 计划文件存 `plans/`（L3）或 `modules/<slug>/plans/`（L2），front matter 须含 `source_design` 与 `level`；归档移入旁边 `archive/` 子目录（checker 有意跳过）。
- modular-autopilot 是主会话技能：subagent 不能再派发 subagent，任何"监督者"类角色都必须坐在主会话。

## Conventions

- commit 末尾加 `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`。
- CLAUDE.md / AGENTS.md 不入库（机器相关路径，见 0fa8ba2），保留本地副本。
- 设计/PM 文档用中文，技能正文用英文（description 含中文触发词）。
- en/zh 双语散文修改：先写 zh 再产出 en 对应版（用户观察 zh 散文效果更好），两语言同一提交落地；机器 token 不动。
- 证据单一居所（写入时规则，2026-07-08 起）：证据只写进设计文档或 Recent Updates 单行，PM 其余节只放一行指针；见 pm-maintenance-rules。

## Troubleshooting

| Symptom | Cause | Fix / Evidence |
| --- | --- | --- |
| EnterWorktree 建出的 worktree 缺本地最新提交 | baseRef 默认 fresh（origin/main），不含未推送的本地 commit | worktree 内 `git merge --ff-only main`（2026-07-03 实证） |
| ExitWorktree remove 误报"N commits 将丢失" | 工具以 origin/main 为基准，未识别已 ff 合并进本地 main | 先 `git merge-base --is-ancestor <tip> main` 确认包含，再 discard_changes: true |

## Reusable Lessons

- 把设计中的契约约束逐字注入 writing-plans 的 Global Constraints，SDD 会转交每个任务评审者，自动获得模块边界守门。
- 转录型任务（计划内嵌全文）用最便宜模型跑 implementer 足够，评审用中档模型核对零漂移。
- 模块化工作流默认应轻量：L1 不默认进入 Active Tasks；只有跨会话、风险、发布证据、用户要求或已有 active task 才完整 PM。
