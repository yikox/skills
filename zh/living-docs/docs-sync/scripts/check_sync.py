#!/usr/bin/env python3
"""living-docs 同步门:检查一段 commit range 内"代码动了、文档没动"的模块。

用法:
    check_sync.py [--arch-dir architecture] [--repo .]
                  [--branch <name>] [--remote origin] [--range A..B]

- 默认(不带 --range):branch 取当前分支,检查 <remote>/<branch> 与工作区的
  全部差异(含未提交、未跟踪)——push/commit 前的预检。
- --range A..B:检查指定 commit 段——pre-push hook 与历史抽查用。
- 仅当 branch 在 main-design.md frontmatter 的 sync_branches(默认 [main])
  中才检查,否则直接放行(开发分支不受管,合入受管分支时再查)。
- 跳过出口:range 内任一 commit message 含 "Arch-Sync: skip <module> <理由>"。

退出码: 0 同步/不受管, 1 有漂移, 2 配置错误。仅 Python 标准库。
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"git {' '.join(args)} 失败: {r.stderr.strip()}")
    return r.stdout


def parse_frontmatter_list(text, key):
    """从 frontmatter 中取 'key:' 下的 '- item' 列表(不依赖 yaml 库)。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    items, in_key = [], False
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.strip().startswith("#"):
            continue
        if not line.startswith(" ") and line.rstrip().endswith(":"):
            in_key = line.strip() == f"{key}:"
            continue
        if in_key and line.strip().startswith("- "):
            items.append(line.strip()[2:].strip().strip("'\""))
    return items


def glob_match(path, pattern):
    """仓库相对路径 glob 匹配,支持尾部 /** 与普通 fnmatch。"""
    import fnmatch
    if pattern.endswith("/**"):
        return path == pattern[:-3] or path.startswith(pattern[:-3] + "/")
    return fnmatch.fnmatch(path, pattern)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arch-dir", default="architecture",
                    help="设计文档目录(仓库相对)")
    ap.add_argument("--repo", default=".", help="仓库根")
    ap.add_argument("--branch", default=None,
                    help="目标分支(默认当前分支;hook 传 push 的远程分支名)")
    ap.add_argument("--remote", default="origin", help="默认模式的对比远程")
    ap.add_argument("--range", dest="rev_range", default=None,
                    help="显式 commit range(A..B);hook 与历史抽查用")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    arch = repo / args.arch_dir
    main_design = arch / "main-design.md"
    modules_dir = arch / "modules"
    if not main_design.is_file():
        sys.exit(f"缺 {main_design}。退出码 2。")

    md_text = main_design.read_text()
    managed = parse_frontmatter_list(md_text, "sync_branches") or ["main"]
    ignored = parse_frontmatter_list(md_text, "ignored_paths")

    branch = args.branch or git(
        repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    if branch not in managed:
        print(f"分支 {branch} 不受管(sync_branches: {managed}),放行;合入受管分支时再检查。")
        return 0

    if args.rev_range:
        changed = set(git(repo, "diff", "--name-only",
                          args.rev_range).splitlines())
        log_range = args.rev_range
    else:
        base = f"{args.remote}/{branch}"
        if subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify",
                           base], capture_output=True).returncode:
            sys.exit(f"找不到 {base};指定 --range 或先 fetch。退出码 2。")
        changed = set(git(repo, "diff", "--name-only", base).splitlines())
        changed |= set(git(repo, "ls-files", "--others",
                           "--exclude-standard").splitlines())
        log_range = f"{base}..HEAD"
    changed = {p for p in changed if p}

    skips = set(re.findall(r"^Arch-Sync:\s*skip\s+(\S+)", git(
        repo, "log", "--format=%B", log_range, check=False), re.M))

    modules = {}  # name -> (doc_rel_path, [globs])
    if modules_dir.is_dir():
        for doc in sorted(modules_dir.glob("*.md")):
            globs = parse_frontmatter_list(doc.read_text(), "code_paths")
            modules[doc.stem] = (str(doc.relative_to(repo)), globs)
    if not modules:
        sys.exit(f"{modules_dir} 下没有模块文档。退出码 2。")

    arch_rel = str(arch.relative_to(repo))
    drifted, claimed = [], set()
    for name, (doc_rel, globs) in modules.items():
        hits = sorted(p for p in changed
                      for g in globs if glob_match(p, g))
        claimed.update(hits)
        if hits and doc_rel not in changed and name not in skips:
            drifted.append((name, hits))

    orphans = sorted(
        p for p in changed - claimed
        if not p.startswith(arch_rel + "/")
        and not any(glob_match(p, g) for g in ignored))

    if not drifted and not orphans:
        skipped = f",跳过 {sorted(skips)}" if skips else ""
        print(f"同步: {log_range} 变更 {len(changed)} 个路径均已覆盖{skipped}。")
        return 0
    for name, hits in drifted:
        print(f"DRIFT {name}: 代码 {len(hits)} 个路径变更,文档未更新"
              f"(更新 {modules[name][0]},或 commit message 加"
              f" 'Arch-Sync: skip {name} <理由>')")
        for p in hits[:5]:
            print(f"    {p}")
        if len(hits) > 5:
            print(f"    … 共 {len(hits)} 个")
    for p in orphans:
        print(f"ORPHAN {p}  (不属于任何模块; 补 code_paths / 建模块 / 加 ignored_paths)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
