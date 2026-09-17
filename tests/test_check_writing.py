"""Tests for the check_writing scanner.

Run them with:
    python3 -m unittest discover -s tests -v
"""

import importlib.util
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
        return [REPO / "README.md", REPO / "CONTRIBUTING.md", REPO / "CHANGELOG.md",
                REPO / "examples" / "after.md"]

    def test_no_em_dashes_in_public_docs(self):
        for path in self.docs():
            with self.subTest(doc=path.name):
                hits = cw.find_em_dashes(path.read_text(encoding="utf-8"))
                self.assertEqual(hits, [], f"{path.name} has em dashes: {hits}")


if __name__ == "__main__":
    unittest.main()
