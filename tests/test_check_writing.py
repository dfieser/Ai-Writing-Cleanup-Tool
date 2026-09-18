"""Tests for the check_writing scanner.

Run them with:
    python3 -m unittest discover -s tests -v
"""

import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = REPO / "skills" / "ai-writing-cleanup" / "scripts" / "check_writing.py"


def load_module():
    spec = importlib.util.spec_from_file_location("check_writing", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cw = load_module()


class EmDashes(unittest.TestCase):
    def test_finds_em_dash(self):
        self.assertEqual(len(cw.find_em_dashes("The API is fast — it caches.")), 1)

    def test_finds_disguised_forms(self):
        spaced_en = cw.find_em_dashes("The API is fast – it caches.")
        double_hyphen = cw.find_em_dashes("The API is fast -- it caches.")
        self.assertEqual(len(spaced_en), 1)
        self.assertEqual(len(double_hyphen), 1)

    def test_keeps_real_hyphens(self):
        self.assertEqual(cw.find_em_dashes("Mount it read-only for end-to-end runs."), [])

    def test_reports_line_numbers(self):
        hits = cw.find_em_dashes("clean line\nsecond — line\n")
        self.assertEqual(hits[0][0], 2)


class CodeIsNotProse(unittest.TestCase):
    def test_fenced_block_is_stripped(self):
        text = "Prose here.\n\n```\nrun --flag -- utilize the thing\n```\n\nMore prose.\n"
        prose = cw.strip_code(text)
        self.assertNotIn("utilize", prose)
        self.assertIn("More prose.", prose)

    def test_inline_span_is_stripped(self):
        prose = cw.strip_code("Pass `--utilize` to the command.")
        self.assertNotIn("utilize", prose)

    def test_fenced_block_collapses_lines(self):
        """strip_code drops line structure, which is why the em dash check
        blanks code itself instead of calling it."""
        text = "one\n```\ntwo\n```\nfour\n"
        self.assertLess(len(cw.strip_code(text).split("\n")), len(text.split("\n")))


class EmDashesIgnoreCode(unittest.TestCase):
    """A command flag is not a dash. The checker promises to skip code."""

    def test_flag_in_fenced_block_is_not_a_dash(self):
        text = "Run the scan.\n\n```bash\ncheck_writing.py draft.md --quiet\n```\n"
        self.assertEqual(cw.find_em_dashes(text), [])

    def test_flag_in_inline_span_is_not_a_dash(self):
        self.assertEqual(cw.find_em_dashes("Pass `draft.md --quiet` to the script."), [])

    def test_flag_in_indented_block_is_not_a_dash(self):
        self.assertEqual(cw.find_em_dashes("Example:\n\n    run foo --quiet\n"), [])

    def test_real_dash_outside_code_still_caught(self):
        text = "```\nrun foo --quiet\n```\n\nThe build is fast \u2014 it caches.\n"
        hits = cw.find_em_dashes(text)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0][0], 5)

    def test_double_hyphen_in_prose_still_caught(self):
        hits = cw.find_em_dashes("The build is fast -- it caches.")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0][1], "double hyphen used as dash")

    def test_line_numbers_stay_accurate_past_a_fence(self):
        text = "intro\n```\na\nb\nc\n```\ntail \u2014 here\n"
        self.assertEqual(cw.find_em_dashes(text)[0][0], 7)


class Buzzwords(unittest.TestCase):
    def test_flags_and_suggests(self):
        counts = cw.find_buzzwords("We leverage a robust pipeline.")
        self.assertIn("leverage", counts)
        self.assertEqual(counts["leverage"][1], "use")

    def test_clean_text_is_clean(self):
        self.assertEqual(cw.find_buzzwords("The pipeline retries three times."), {})


class Quotes(unittest.TestCase):
    def test_scare_quotes_flagged(self):
        scare, _ = cw.find_scare_quotes('The scheduler enters a "safe" mode.')
        self.assertEqual(len(scare), 1)

    def test_attributed_quotation_passes(self):
        scare, _ = cw.find_scare_quotes('The RFC says "servers MUST retry" in section 4.')
        self.assertEqual(scare, [])


class Parentheses(unittest.TestCase):
    def test_prose_aside_flagged(self):
        self.assertEqual(len(cw.find_parentheses("The cache is warm (it loads at boot).")), 1)

    def test_definition_is_exempt(self):
        self.assertEqual(cw.find_parentheses("We used high entropy alloys (HEA) throughout."), [])

    def test_reverse_definition_is_exempt(self):
        self.assertEqual(cw.find_parentheses("We used HEA (high entropy alloy) throughout."), [])


class Voice(unittest.TestCase):
    def test_passive_flagged(self):
        self.assertEqual(len(cw.find_passive(["The seal was replaced by the technician."])), 1)

    def test_active_passes(self):
        self.assertEqual(cw.find_passive(["The technician replaced the seal."]), [])


class HiddenVerbs(unittest.TestCase):
    def test_nominalization_flagged(self):
        self.assertTrue(cw.find_hidden_verbs("Perform an inspection of the housing."))


class Pronouns(unittest.TestCase):
    def test_expletive_opener_flagged(self):
        sentences = ["It was decided that the job would run nightly."]
        vague, _, _ = cw.find_pronoun_issues(sentences, " ".join(sentences))
        self.assertEqual(len(vague), 1)


class Sentences(unittest.TestCase):
    def test_split_and_count(self):
        sentences = cw.split_sentences("One short line. Another one here.")
        self.assertEqual(len(sentences), 2)
        self.assertEqual(cw.word_count("Another one here"), 3)


class CommandLine(unittest.TestCase):
    def run_checker(self, text, *flags):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "-", *flags],
            input=text, capture_output=True, text=True, check=True,
        ).stdout

    def test_reads_stdin_and_reports(self):
        out = self.run_checker("The build is fast — it caches.\n")
        self.assertIn("EM DASHES", out)
        self.assertIn("found: 1", out)

    def test_quiet_prints_summary_only(self):
        out = self.run_checker("The build is fast — it caches.\n", "--quiet")
        self.assertIn("em-dashes=1", out)
        self.assertNotIn("WRITING CHECK", out)

    def test_reads_a_file(self):
        out = subprocess.run(
            [sys.executable, str(SCRIPT), str(REPO / "README.md")],
            capture_output=True, text=True, check=True,
        ).stdout
        self.assertIn("SUMMARY", out)

    def test_empty_input_is_handled(self):
        self.assertIn("No text to check", self.run_checker("\n"))

    def test_help_flag(self):
        out = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True, check=True,
        ).stdout
        self.assertIn("Usage", out)


class PublicDocs(unittest.TestCase):
    """The repository's own docs follow the rules the skill teaches."""

    def docs(self):
        names = ["README.md", "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md",
                 "CHANGELOG.md", "examples/after.md", "wiki/Home.md",
                 "wiki/Checker-Reference.md", "wiki/Editing-Workflow.md",
                 "wiki/FAQ.md"]
        return [REPO / n for n in names]

    def test_no_em_dashes_in_public_docs(self):
        for path in self.docs():
            with self.subTest(doc=path.name):
                hits = cw.find_em_dashes(path.read_text(encoding="utf-8"))
                self.assertEqual(hits, [], f"{path.name} has em dashes: {hits}")


class MarkdownLinks(unittest.TestCase):
    """Link syntax is not a prose aside, or every README fails its own gate."""

    def test_link_target_not_flagged(self):
        self.assertEqual(
            cw.find_parentheses("See [the wiki](https://example.com/w) for more."), [])

    def test_relative_link_not_flagged(self):
        self.assertEqual(cw.find_parentheses("Read [the rules](./SKILL.md) first."), [])

    def test_real_aside_still_flagged(self):
        self.assertEqual(len(cw.find_parentheses("The cache is warm (it loads at boot).")), 1)


def run_checker(*args, stdin=None):
    """Run the CLI and hand back the finished process, whatever the exit code."""
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        input=stdin if stdin is not None else "",
        capture_output=True, text=True,
    )


class ExitCodes(unittest.TestCase):
    """Agents branch on exit codes, so these are a contract."""

    def test_no_gate_always_succeeds(self):
        self.assertEqual(run_checker(str(REPO / "examples" / "before.md")).returncode, 0)

    def test_gate_fails_on_a_dirty_document(self):
        done = run_checker(str(REPO / "examples" / "before.md"), "--quiet",
                           "--fail-on", "mechanics")
        self.assertEqual(done.returncode, 1)
        self.assertIn("FAILED on:", done.stderr)

    def test_gate_passes_on_a_clean_document(self):
        done = run_checker(str(REPO / "AGENTS.md"), "--quiet", "--fail-on", "mechanics")
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_equals_form_of_the_flag(self):
        self.assertEqual(
            run_checker(str(REPO / "AGENTS.md"), "--quiet", "--fail-on=mechanics").returncode, 0)

    def test_single_category_gate(self):
        done = run_checker(str(REPO / "examples" / "before.md"), "--quiet",
                           "--fail-on", "em-dashes")
        self.assertEqual(done.returncode, 1)

    def test_unknown_category_is_a_usage_error(self):
        done = run_checker(str(REPO / "AGENTS.md"), "--fail-on", "nonsense")
        self.assertEqual(done.returncode, 2)
        self.assertIn("unknown --fail-on category", done.stderr)

    def test_unknown_option_is_a_usage_error(self):
        done = run_checker(str(REPO / "AGENTS.md"), "--bogus")
        self.assertEqual(done.returncode, 2)
        self.assertIn("unknown option", done.stderr)

    def test_missing_fail_on_value(self):
        self.assertEqual(run_checker(str(REPO / "AGENTS.md"), "--fail-on").returncode, 2)


class JsonReport(unittest.TestCase):
    """The JSON shape is what an agent parses, so pin it down."""

    def report(self, path=None):
        target = str(path or (REPO / "examples" / "before.md"))
        done = run_checker(target, "--json")
        self.assertEqual(done.returncode, 0, done.stderr)
        return json.loads(done.stdout)

    def test_top_level_keys(self):
        d = self.report()
        for key in ("file", "verdict", "counts", "totals", "gate", "sentences",
                    "tense", "abbreviations", "findings", "notes"):
            self.assertIn(key, d)

    def test_every_category_is_counted(self):
        counts = self.report()["counts"]
        for name in cw.COUNT_KEYS:
            self.assertIn(name, counts)
            self.assertIsInstance(counts[name], int)

    def test_counts_match_the_findings(self):
        d = self.report()
        self.assertEqual(d["counts"]["em-dashes"], len(d["findings"]["em-dashes"]))
        self.assertEqual(d["counts"]["scare-quotes"], len(d["findings"]["scare-quotes"]))

    def test_findings_carry_line_numbers(self):
        for hit in self.report()["findings"]["em-dashes"]:
            self.assertIsInstance(hit["line"], int)
            self.assertIn("text", hit)

    def test_buzzwords_carry_a_suggestion(self):
        for hit in self.report()["findings"]["buzzwords"]:
            self.assertTrue(hit["suggestion"])

    def test_verdict_values(self):
        self.assertEqual(self.report()["verdict"], "needs-work")
        self.assertEqual(self.report(REPO / "AGENTS.md")["verdict"],
                         self.report(REPO / "AGENTS.md")["verdict"])

    def test_gate_block_reports_the_failure(self):
        done = run_checker(str(REPO / "examples" / "before.md"), "--json",
                           "--fail-on", "mechanics")
        self.assertEqual(done.returncode, 1)
        gate = json.loads(done.stdout)["gate"]
        self.assertEqual(gate["exit_code"], 1)
        self.assertIn("em-dashes", gate["failed"])

    def test_empty_input_is_still_json(self):
        done = run_checker("-", "--json", stdin="\n")
        self.assertEqual(done.returncode, 0)
        self.assertEqual(json.loads(done.stdout)["verdict"], "empty")


class Bundle(unittest.TestCase):
    """The single-file bundle is what an agent without a skill loader reads."""

    def test_bundle_exists_and_is_current(self):
        done = subprocess.run(
            [sys.executable, str(REPO / "tools" / "build_bundle.py"), "--check"],
            capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

    def test_bundle_holds_every_source(self):
        text = (REPO / "dist" / "ai-writing-cleanup.bundle.md").read_text(encoding="utf-8")
        for marker in ("Part A: the skill", "Part B: catalog of machine-writing tells",
                       "Part C: technical publication rules"):
            self.assertIn(marker, text)

    def test_bundle_states_the_overriding_rule(self):
        text = (REPO / "dist" / "ai-writing-cleanup.bundle.md").read_text(encoding="utf-8")
        self.assertIn("Preserve technical truth", text)


class AgentEntryPoints(unittest.TestCase):
    """A dropped-in copy has to be usable without a human reading anything."""

    def test_agents_file_exists(self):
        self.assertTrue((REPO / "AGENTS.md").is_file())
        self.assertTrue((REPO / "CLAUDE.md").is_file())

    def test_agents_file_names_the_checker_and_the_bundle(self):
        text = (REPO / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("skills/ai-writing-cleanup/scripts/check_writing.py", text)
        self.assertIn("dist/ai-writing-cleanup.bundle.md", text)
        self.assertIn("--fail-on mechanics", text)

    def test_installer_accepts_into(self):
        done = subprocess.run(["bash", str(REPO / "install.sh"), "--help"],
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0)
        self.assertIn("--into", done.stdout)


class Versioning(unittest.TestCase):
    """The skill folder travels alone, so it has to say which version it is."""

    def plugin_version(self):
        return json.loads((REPO / ".claude-plugin" / "plugin.json")
                          .read_text(encoding="utf-8"))["version"]

    def test_checker_reports_its_version(self):
        done = run_checker("--version")
        self.assertEqual(done.returncode, 0)
        self.assertIn(self.plugin_version(), done.stdout)

    def test_short_version_flag(self):
        self.assertEqual(run_checker("-V").stdout, run_checker("--version").stdout)

    def test_version_needs_no_input(self):
        """--version must not block on stdin the way --help once did."""
        done = subprocess.run([sys.executable, str(SCRIPT), "--version"],
                              stdin=subprocess.DEVNULL, capture_output=True,
                              text=True, timeout=10)
        self.assertEqual(done.returncode, 0)

    def test_skill_frontmatter_carries_the_version(self):
        head = (REPO / "skills" / "ai-writing-cleanup" / "SKILL.md").read_text(
            encoding="utf-8").split("---")[1]
        self.assertIn("version: " + self.plugin_version(), head)

    def test_json_report_carries_the_version(self):
        done = run_checker(str(REPO / "AGENTS.md"), "--json")
        self.assertEqual(json.loads(done.stdout)["version"], self.plugin_version())

    def test_everything_is_stamped_consistently(self):
        done = subprocess.run(
            [sys.executable, str(REPO / "tools" / "sync_version.py"), "--check"],
            capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)


class ReleasePackage(unittest.TestCase):
    """The zip is the only thing that can change an account's copy."""

    def test_release_builds(self):
        done = subprocess.run(
            [sys.executable, str(REPO / "tools" / "build_release.py"), "--check"],
            capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

    def test_release_holds_the_skill_and_nothing_else(self):
        done = subprocess.run(
            [sys.executable, str(REPO / "tools" / "build_release.py"), "--check"],
            capture_output=True, text=True)
        listed = [l.strip() for l in done.stdout.splitlines() if l.startswith("  ")]
        self.assertIn("ai-writing-cleanup/SKILL.md", listed)
        self.assertIn("ai-writing-cleanup/scripts/check_writing.py", listed)
        for entry in listed:
            self.assertNotIn("__pycache__", entry)
            self.assertFalse(entry.endswith(".pyc"))


UPDATER = REPO / "skills" / "ai-writing-cleanup" / "scripts" / "update.py"


def load_updater():
    spec = importlib.util.spec_from_file_location("aw_update", UPDATER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class UpdaterGuards(unittest.TestCase):
    """What comes off the network is checked before it is trusted."""

    def setUp(self):
        self.up = load_updater()
        self.rules = self.up.ARTIFACTS["rules"]
        self.checker = self.up.ARTIFACTS["checker"]

    def test_real_bundle_is_accepted(self):
        text = (REPO / "dist" / "ai-writing-cleanup.bundle.md").read_text(encoding="utf-8")
        self.assertIsNone(self.up.trustworthy(text, self.rules))

    def test_real_checker_is_accepted(self):
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIsNone(self.up.trustworthy(text, self.checker))

    def test_error_page_is_rejected(self):
        self.assertIsNotNone(self.up.trustworthy("<html>404 Not Found</html>", self.rules))

    def test_truncated_download_is_rejected(self):
        text = (REPO / "dist" / "ai-writing-cleanup.bundle.md").read_text(
            encoding="utf-8")[:500]
        self.assertIn("too small", self.up.trustworthy(text, self.rules))

    def test_right_size_wrong_content_is_rejected(self):
        self.assertIn("missing expected content",
                      self.up.trustworthy("x" * 20000, self.rules))

    def test_broken_python_is_rejected(self):
        text = SCRIPT.read_text(encoding="utf-8") + "\ndef (((:\n"
        self.assertIn("does not parse", self.up.trustworthy(text, self.checker))

    def test_non_https_source_is_refused(self):
        done = subprocess.run(
            [sys.executable, str(UPDATER), "--force"],
            env={**os.environ, "AI_WRITING_CLEANUP_RAW": "http://example.com"},
            capture_output=True, text=True, timeout=30)
        self.assertIn("non-HTTPS", done.stdout + done.stderr)

    def test_version_is_read_from_each_artifact(self):
        self.assertEqual(self.up.version_of('__version__ = "9.9.9"'), "9.9.9")
        self.assertEqual(self.up.version_of("# Title\n\nVersion 9.9.9.\n"), "9.9.9")
        self.assertEqual(self.up.version_of("---\nname: x\nversion: 9.9.9\n"), "9.9.9")
        self.assertEqual(self.up.version_of("nothing here"), "unknown")


class UpdaterNeverBlocks(unittest.TestCase):
    """A failed fetch must never stop an edit."""

    def run_updater(self, *args, **env):
        return subprocess.run(
            [sys.executable, str(UPDATER), *args],
            env={**os.environ, **env}, capture_output=True, text=True, timeout=60)

    def test_offline_succeeds_without_network(self):
        done = self.run_updater("--offline")
        self.assertEqual(done.returncode, 0)
        self.assertIn("rules", done.stdout)

    def test_unreachable_source_still_exits_zero(self):
        done = self.run_updater(
            "--force",
            AI_WRITING_CLEANUP_RAW="https://raw.githubusercontent.com/dfieser/no-such-repo-xyz/HEAD")
        self.assertEqual(done.returncode, 0)
        self.assertIn("shipped copy", done.stdout + done.stderr)

    def test_falls_back_to_a_real_readable_file(self):
        done = self.run_updater(
            "--force", "--json",
            AI_WRITING_CLEANUP_RAW="https://raw.githubusercontent.com/dfieser/no-such-repo-xyz/HEAD")
        for info in json.loads(done.stdout)["artifacts"].values():
            self.assertTrue(pathlib.Path(info["path"]).is_file(), info["path"])

    def test_status_reports_without_fetching(self):
        done = self.run_updater("--status", "--json")
        self.assertEqual(done.returncode, 0)
        self.assertIn("artifacts", json.loads(done.stdout))

    def test_help_does_not_hang(self):
        done = subprocess.run([sys.executable, str(UPDATER), "--help"],
                              stdin=subprocess.DEVNULL, capture_output=True,
                              text=True, timeout=10)
        self.assertEqual(done.returncode, 0)


class BundleAvoidsFetchLoop(unittest.TestCase):
    def test_bundle_tells_the_reader_the_fetch_is_done(self):
        text = (REPO / "dist" / "ai-writing-cleanup.bundle.md").read_text(encoding="utf-8")
        self.assertIn("do not run the updater again", text)

    def test_skill_names_the_updater_as_step_one(self):
        text = (REPO / "skills" / "ai-writing-cleanup" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("scripts/update.py", text)
        self.assertIn("Get the current rules", text)


if __name__ == "__main__":
    unittest.main()
