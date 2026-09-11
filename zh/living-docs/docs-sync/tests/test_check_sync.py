#!/usr/bin/env python3
"""check_sync.py 回归测试。仅标准库。

用法: python3 tests/test_check_sync.py

在临时目录建最小 git 仓库,覆盖同步门的各条路径:

  1. 同步——代码与文档同 commit                    -> 0
  2. DRIFT——代码动了、文档没动                     -> 1
  3. ORPHAN——变更路径不属于任何模块                -> 1
  4. ORPHAN 用 Arch-Sync: skip <路径> 放行          -> 0
  5. ignored_paths 内的变更不报 ORPHAN             -> 0
  6. 不受管分支放行                                -> 0
  7. Arch-Sync: skip <模块> 放行                   -> 0
  8. 文件跨模块移动,源模块同样被点名               -> 1
  9. --arch-dir 越出仓库                           -> 2
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECK_SYNC = HERE.parent / "scripts" / "check_sync.py"

MAIN_DESIGN = """---
sync_branches:
  - main
ignored_paths:
  - README.md
---

# demo
"""

MODULE_DOC = """---
name: {name}
code_paths:
  - src/{name}/**
---

# {name}
"""


def git(repo, *args):
    proc = subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} 失败: {proc.stderr.strip()}")


def git_out(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True).stdout


class CheckSyncTest(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="check-sync-"))
        git(self.repo, "init", "-q")
        git(self.repo, "symbolic-ref", "HEAD", "refs/heads/main")
        git(self.repo, "config", "user.email", "test@example.com")
        git(self.repo, "config", "user.name", "test")

        (self.repo / "architecture" / "modules").mkdir(parents=True)
        (self.repo / "architecture" / "main-design.md").write_text(MAIN_DESIGN)
        for name in ("alpha", "beta"):
            (self.repo / "architecture" / "modules" / f"{name}.md").write_text(
                MODULE_DOC.format(name=name))
            (self.repo / "src" / name).mkdir(parents=True)
            (self.repo / "src" / name / f"{name}.py").write_text("x = 1\n")
        (self.repo / "README.md").write_text("demo\n")

        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-qm", "base")
        self.base = git_out(self.repo, "rev-parse", "HEAD").strip()

    def tearDown(self):
        shutil.rmtree(self.repo, ignore_errors=True)

    def commit(self, message):
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-qm", message)

    def run_check(self, *extra):
        proc = subprocess.run(
            [sys.executable, str(CHECK_SYNC), "--repo", str(self.repo),
             "--range", f"{self.base}..HEAD", *extra],
            capture_output=True, text=True)
        return proc.returncode, proc.stdout + proc.stderr

    def test_synced(self):
        (self.repo / "src" / "alpha" / "alpha.py").write_text("x = 2\n")
        (self.repo / "architecture" / "modules" / "alpha.md").write_text(
            MODULE_DOC.format(name="alpha") + "\n改过了\n")
        self.commit("同步改动")
        rc, out = self.run_check()
        self.assertEqual(rc, 0, out)

    def test_drift(self):
        (self.repo / "src" / "alpha" / "alpha.py").write_text("x = 2\n")
        self.commit("只改代码")
        rc, out = self.run_check()
        self.assertEqual(rc, 1, out)
        self.assertIn("DRIFT alpha", out)

    def test_orphan(self):
        (self.repo / "notes.txt").write_text("hello\n")
        self.commit("无人认领的路径")
        rc, out = self.run_check()
        self.assertEqual(rc, 1, out)
        self.assertIn("ORPHAN notes.txt", out)

    def test_orphan_skip_exact_path(self):
        (self.repo / "notes.txt").write_text("hello\n")
        self.commit("清理临时文件\n\nArch-Sync: skip notes.txt 一次性清理")
        rc, out = self.run_check()
        self.assertEqual(rc, 0, out)

    def test_orphan_skip_glob(self):
        (self.repo / "scratch").mkdir()
        (self.repo / "scratch" / "a.txt").write_text("x\n")
        (self.repo / "scratch" / "b.txt").write_text("y\n")
        self.commit("清理草稿\n\nArch-Sync: skip scratch/** 一次性清理")
        rc, out = self.run_check()
        self.assertEqual(rc, 0, out)

    def test_ignored_path(self):
        (self.repo / "README.md").write_text("demo v2\n")
        self.commit("只改被忽略的路径")
        rc, out = self.run_check()
        self.assertEqual(rc, 0, out)

    def test_unmanaged_branch_passes(self):
        (self.repo / "src" / "alpha" / "alpha.py").write_text("x = 2\n")
        self.commit("开发分支上的漂移")
        rc, out = self.run_check("--branch", "dev")
        self.assertEqual(rc, 0, out)
        self.assertIn("不受管", out)

    def test_skip_escape(self):
        (self.repo / "src" / "alpha" / "alpha.py").write_text("x = 2\n")
        self.commit("只改代码\n\nArch-Sync: skip alpha 改动只是格式化")
        rc, out = self.run_check()
        self.assertEqual(rc, 0, out)
        self.assertIn("alpha", out)

    def test_rename_across_modules(self):
        git(self.repo, "mv", "src/alpha/alpha.py", "src/beta/alpha.py")
        self.commit("把实现搬到 beta")
        rc, out = self.run_check()
        self.assertEqual(rc, 1, out)
        self.assertIn("DRIFT alpha", out)
        self.assertIn("DRIFT beta", out)

    def test_arch_dir_outside_repo(self):
        outside = Path(tempfile.mkdtemp(prefix="check-sync-outside-"))
        self.addCleanup(shutil.rmtree, outside, True)
        (outside / "main-design.md").write_text(MAIN_DESIGN)
        rc, out = self.run_check("--arch-dir", str(outside))
        self.assertEqual(rc, 2, out)
        self.assertIn("必须位于仓库内", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
