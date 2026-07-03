# skills 仓库 Knowledge Summary

Last updated: 2026-07-03

## Verified Commands

| Command | Purpose | Notes |
| --- | --- | --- |
| `python3 modular-programming/modular-audit/scripts/check_modular_project.py PM/skills` | 项目记忆一致性检查 | 退出码 1 = 有 error；`--repo-root . --exclude 'docs/**' --exclude 'PM/**'` 启用代码所有权检查 |
| `python3 modular-programming/_shared/scripts/render_modular_graph.py <in.arch.json> -o <out.html> --svg-output <out.svg>` | 渲染架构图 | stdlib-only |
| `./install.sh --dry-run` | 预演技能安装 | 默认目标 ~/.agents、~/.codex、~/.claude 的 skills 目录 |

## Architecture Facts

- 图是模块关系的权威来源；模块文档 Dependencies 表必须是图关系子集（checker 强制）。
- 计划文件存 `plans/`（L3）或 `modules/<slug>/plans/`（L2），front matter 须含 `source_design` 与 `level`；归档移入旁边 `archive/` 子目录（checker 有意跳过）。
- modular-autopilot 是主会话技能：subagent 不能再派发 subagent，任何"监督者"类角色都必须坐在主会话。

## Conventions

- commit 末尾加 `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`。
- CLAUDE.md / AGENTS.md 不入库（机器相关路径，见 0fa8ba2），保留本地副本。
- 设计/PM 文档用中文，技能正文用英文（description 含中文触发词）。

## Troubleshooting

| Symptom | Cause | Fix / Evidence |
| --- | --- | --- |
| EnterWorktree 建出的 worktree 缺本地最新提交 | baseRef 默认 fresh（origin/main），不含未推送的本地 commit | worktree 内 `git merge --ff-only main`（2026-07-03 实证） |
| ExitWorktree remove 误报"N commits 将丢失" | 工具以 origin/main 为基准，未识别已 ff 合并进本地 main | 先 `git merge-base --is-ancestor <tip> main` 确认包含，再 discard_changes: true |

## Reusable Lessons

- 把设计中的契约约束逐字注入 writing-plans 的 Global Constraints，SDD 会转交每个任务评审者，自动获得模块边界守门。
- 转录型任务（计划内嵌全文）用最便宜模型跑 implementer 足够，评审用中档模型核对零漂移。
