#!/usr/bin/env python3
"""living-docs 漂移检测：git diff <.last-sync>..工作区 ∩ 模块 code_paths。

用法:
    python3 check_drift.py --arch-dir architecture [--repo .]

输出"代码动了、文档没动"的模块清单与孤儿路径。退出码: 0 无漂移, 1 有漂移, 2 配置错误。
仅用 Python 标准库。
"""
import argparse
import subprocess
import sys
from pathlib import Path


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True)
    if r.returncode != 0:
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
    """仓库相对路径 glob 匹配，支持尾部 /** 与普通 fnmatch。"""
    import fnmatch
    if pattern.endswith("/**"):
        return path == pattern[:-3] or path.startswith(pattern[:-3] + "/")
    return fnmatch.fnmatch(path, pattern)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arch-dir", default="architecture",
                    help="设计文档目录(仓库相对)")
    ap.add_argument("--repo", default=".", help="仓库根")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    arch = repo / args.arch_dir
    sync_file = arch / ".last-sync"
    modules_dir = arch / "modules"

    if not sync_file.is_file():
        sys.exit(f"缺 {sync_file}(docs-init 初始化，对账后 bump)。退出码 2。")
    anchor = sync_file.read_text().strip()
    if subprocess.run(["git", "-C", str(repo), "cat-file", "-e",
                       f"{anchor}^{{commit}}"], capture_output=True).returncode:
        sys.exit(f".last-sync 指向未知 commit: {anchor}")

    # anchor 与工作区的差异(含已提交+未提交) + 未跟踪文件
    changed = set(git(repo, "diff", "--name-only", anchor).splitlines())
    changed |= set(git(repo, "ls-files", "--others",
                       "--exclude-standard").splitlines())
    changed = {p for p in changed if p}

    main_design = arch / "main-design.md"
    ignored = parse_frontmatter_list(
        main_design.read_text(), "ignored_paths") if main_design.is_file() else []
    arch_rel = str(arch.relative_to(repo))

    modules = {}  # name -> (doc_rel_path, [globs])
    if modules_dir.is_dir():
        for doc in sorted(modules_dir.glob("*.md")):
            globs = parse_frontmatter_list(doc.read_text(), "code_paths")
            modules[doc.stem] = (str(doc.relative_to(repo)), globs)
    if not modules:
        sys.exit(f"{modules_dir} 下没有模块文档。退出码 2。")

    drifted, claimed = [], set()
    for name, (doc_rel, globs) in modules.items():
        hits = sorted(p for p in changed
                      for g in globs if glob_match(p, g))
        claimed.update(hits)
        if hits and doc_rel not in changed:
            drifted.append((name, hits))

    orphans = sorted(
        p for p in changed - claimed
        if not p.startswith(arch_rel + "/")
        and not any(glob_match(p, g) for g in ignored))

    if not drifted and not orphans:
        print(f"对齐: {anchor[:12]} 以来无漂移(变更 {len(changed)} 个路径均已覆盖)。")
        return 0
    for name, hits in drifted:
        print(f"DRIFT {name}: 代码 {len(hits)} 个路径变更，文档未更新")
        for p in hits[:5]:
            print(f"    {p}")
        if len(hits) > 5:
            print(f"    … 共 {len(hits)} 个")
    for p in orphans:
        print(f"ORPHAN {p}  (不属于任何模块; 补 code_paths / 建模块 / 加 ignored_paths)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
