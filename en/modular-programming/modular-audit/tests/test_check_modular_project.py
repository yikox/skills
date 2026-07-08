import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_modular_project.py"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")


class CheckModularProjectGraphTests(unittest.TestCase):
    def make_pm(self, graph: dict) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        pm = Path(tmp.name) / "pm"

        write(
            pm / "project-management.md",
            """
            # Test PM

            ## Active Tasks

            | Date | Task | Primary Module | Impacted Modules | Level | Status | Next Step / Notes |
            | --- | --- | --- | --- | --- | --- | --- |

            ## Modular Design Index

            | Type | Path | Status | Review | Notes |
            | --- | --- | --- | --- | --- |
            """,
        )
        write(pm / "knowledge-summary.md", "# Test Knowledge\n")
        write(
            pm / "architecture/main-design.md",
            """
            ---
            name: Test Architecture
            status: implemented
            review_status: reviewed
            ---

            # Test Architecture
            """,
        )
        for slug in ["api", "runtime", "worker"]:
            write(
                pm / f"architecture/modules/{slug}.md",
                f"""
                ---
                name: {slug}
                described: Test {slug} module
                module_form: atomic
                module_kind: function-flow
                main_subject: {slug}
                code_paths: ["src/{slug}.py"]
                status: implemented
                review_status: reviewed
                ---

                # {slug}

                ## Responsibility

                Test module.

                ## Public Contract

                No external contract.

                ## Dependencies

                | Dependency | Direction | Reason |
                | --- | --- | --- |
                """,
            )
        write(
            pm / "architecture/graphs/current-project.arch.json",
            json.dumps(graph, ensure_ascii=False, indent=2),
        )
        return pm

    def run_checker(self, pm: Path, *extra_args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(pm), *extra_args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_graph_file_is_optional_for_lightweight_baseline(self) -> None:
        pm = self.make_pm(
            {
                "format": "arch-graph/v0.3",
                "name": "Temporary graph",
                "described": "Removed to test optional graph baseline",
                "objects": [],
                "groups": [],
                "relations": [],
            }
        )
        (pm / "architecture/graphs/current-project.arch.json").unlink()

        result = self.run_checker(pm)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error, 0 warning", result.stdout)

    def test_group_interface_provider_must_be_inside_group_subtree(self) -> None:
        pm = self.make_pm(
            {
                "format": "arch-graph/v0.3",
                "name": "Bad provider graph",
                "described": "Provider points outside the group subtree",
                "objects": [
                    {"id": "api", "ref": "../modules/api.md"},
                    {"id": "worker", "ref": "../modules/worker.md"},
                ],
                "groups": [
                    {
                        "id": "runtime",
                        "ref": "../modules/runtime.md",
                        "contains": ["worker"],
                        "interfaces": [
                            {
                                "id": "service",
                                "name": "Service",
                                "described": "Runtime service",
                                "provided_by": ["api"],
                            }
                        ],
                    }
                ],
                "relations": [
                    {
                        "from": "api",
                        "to": "runtime.service",
                        "kind": "uses",
                        "described": "Calls the runtime service",
                    }
                ],
            }
        )

        result = self.run_checker(pm)

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("provider api", result.stdout)
        self.assertIn("contains", result.stdout)

    def test_shared_paths_are_documented_non_owner_exceptions(self) -> None:
        pm = self.make_pm(
            {
                "format": "arch-graph/v0.3",
                "name": "Ownership graph",
                "described": "Ownership fixture",
                "objects": [],
                "groups": [],
                "relations": [],
            }
        )
        repo = pm.parent / "repo"
        for slug in ["api", "runtime", "worker"]:
            write(repo / f"src/{slug}.py", "# owned\n")
        write(repo / "src/shared.py", "# shared\n")
        api_doc = pm / "architecture/modules/api.md"
        api_doc.write_text(
            api_doc.read_text(encoding="utf-8").replace(
                'code_paths: ["src/api.py"]',
                'code_paths: ["src/api.py"]\nshared_paths: ["src/shared.py"]',
            ),
            encoding="utf-8",
        )

        result = self.run_checker(pm, "--repo-root", str(repo), "--exclude", "pm/**")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error, 0 warning", result.stdout)

    def test_ghost_exception_globs_are_warned(self) -> None:
        pm = self.make_pm(
            {
                "format": "arch-graph/v0.3",
                "name": "Ownership graph",
                "described": "Ownership fixture",
                "objects": [],
                "groups": [],
                "relations": [],
            }
        )
        repo = pm.parent / "repo"
        for slug in ["api", "runtime", "worker"]:
            write(repo / f"src/{slug}.py", "# owned\n")
        api_doc = pm / "architecture/modules/api.md"
        api_doc.write_text(
            api_doc.read_text(encoding="utf-8").replace(
                'code_paths: ["src/api.py"]',
                'code_paths: ["src/api.py"]\nignored_paths: ["vendor/**"]',
            ),
            encoding="utf-8",
        )

        result = self.run_checker(pm, "--repo-root", str(repo), "--exclude", "pm/**")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("幽灵例外 glob", result.stdout)
        self.assertIn("vendor/**", result.stdout)

    def test_old_format_graph_downgrades_structural_errors_to_warnings(self) -> None:
        pm = self.make_pm(
            {
                "format": "arch-graph/v0.1",
                "name": "Legacy graph",
                "described": "v0.1 graph without contains forest",
                "objects": [
                    {"id": "api", "ref": "../modules/api.md"},
                    {"id": "worker", "ref": "../modules/worker.md"},
                ],
                "groups": [
                    {
                        "id": "runtime",
                        "ref": "../modules/runtime.md",
                        "interfaces": [
                            {
                                "id": "service",
                                "name": "Service",
                                "described": "Runtime service",
                                "provided_by": ["worker"],
                            }
                        ],
                    }
                ],
                "relations": [
                    {
                        "from": "api",
                        "to": "runtime.service",
                        "kind": "uses",
                        "described": "Calls the runtime service",
                    }
                ],
            }
        )

        result = self.run_checker(pm)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error", result.stdout)
        self.assertIn("缺少有效 contains", result.stdout)

    def test_relations_must_connect_endpoints_in_the_same_scope(self) -> None:
        pm = self.make_pm(
            {
                "format": "arch-graph/v0.3",
                "name": "Cross scope graph",
                "described": "Top-level object directly calls a child object",
                "objects": [
                    {"id": "api", "ref": "../modules/api.md"},
                    {"id": "worker", "ref": "../modules/worker.md"},
                ],
                "groups": [
                    {"id": "runtime", "ref": "../modules/runtime.md", "contains": ["worker"]}
                ],
                "relations": [
                    {
                        "from": "api",
                        "to": "worker",
                        "kind": "uses",
                        "described": "Invalid direct dependency across scopes",
                    }
                ],
            }
        )

        result = self.run_checker(pm)

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("跨 scope", result.stdout)

    def test_group_interface_relation_at_parent_scope_is_valid(self) -> None:
        pm = self.make_pm(
            {
                "format": "arch-graph/v0.3",
                "name": "Valid interface graph",
                "described": "Top-level object connects to a group interface",
                "objects": [
                    {"id": "api", "ref": "../modules/api.md"},
                    {"id": "worker", "ref": "../modules/worker.md"},
                ],
                "groups": [
                    {
                        "id": "runtime",
                        "ref": "../modules/runtime.md",
                        "contains": ["worker"],
                        "interfaces": [
                            {
                                "id": "service",
                                "name": "Service",
                                "described": "Runtime service",
                                "provided_by": ["worker"],
                            }
                        ],
                    }
                ],
                "relations": [
                    {
                        "from": "api",
                        "to": "runtime.service",
                        "kind": "uses",
                        "described": "Calls the runtime service",
                    }
                ],
            }
        )

        result = self.run_checker(pm)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error", result.stdout)

    def test_plan_may_reference_branch_architecture_patch_commit(self) -> None:
        pm = self.make_pm(
            {
                "format": "arch-graph/v0.3",
                "name": "Patch plan graph",
                "described": "Plan source patch fixture",
                "objects": [],
                "groups": [],
                "relations": [],
            }
        )
        write(
            pm / "architecture/plans/2026-07-08-branch-patch-plan.md",
            """
            ---
            source_patch: bd19dfa
            level: L3
            ---

            # Branch Patch Plan
            """,
        )

        result = self.run_checker(pm)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error, 0 warning", result.stdout)


class VocabSingleSourceTests(unittest.TestCase):
    """受控词表以 _shared/references/vocab.md 为单一事实源，缺失时回退内置默认。"""

    def load_module(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location("chk_vocab", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_real_manifest_matches_builtin_fallback(self) -> None:
        # 仓库内真实 vocab.md 解析结果必须与内置 fallback 完全一致，
        # 否则说明清单与 checker 已漂移。
        m = self.load_module()
        v = m.load_vocab(m.VOCAB_PATH)
        for name, expected in m._FALLBACK_VOCAB.items():
            self.assertEqual(v[name], expected, f"vocab.md 的 {name} 与内置默认不一致")

    def test_manifest_drives_vocabulary(self) -> None:
        # 证明校验词表来自清单而非硬编码：清单里加入假词即被采纳。
        m = self.load_module()
        tmp = Path(tempfile.mktemp(suffix=".md"))
        self.addCleanup(lambda: tmp.exists() and tmp.unlink())
        tmp.write_text("## module_kind\n`fake-kind`, `function-flow`\n", encoding="utf-8")
        v = m.load_vocab(tmp)
        self.assertIn("fake-kind", v["module_kind"])
        # 清单未列出的词表回退默认值
        self.assertEqual(v["review_status"], m._FALLBACK_VOCAB["review_status"])

    def test_missing_manifest_falls_back_and_warns(self) -> None:
        m = self.load_module()
        before = len(m.warnings)
        v = m.load_vocab(Path("/no/such/vocab.md"))
        self.assertEqual(v["module_form"], m._FALLBACK_VOCAB["module_form"])
        self.assertGreater(len(m.warnings), before)


if __name__ == "__main__":
    unittest.main()
