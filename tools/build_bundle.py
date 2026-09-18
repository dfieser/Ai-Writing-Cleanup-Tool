#!/usr/bin/env python3
"""Build dist/ai-writing-cleanup.bundle.md from the skill sources.

The bundle is one file holding every rule, for an agent that has no skill
system and just needs to read the whole ruleset in a single fetch.

    python3 tools/build_bundle.py           # write the bundle
    python3 tools/build_bundle.py --check   # exit 1 if the bundle is stale

Stdlib only.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
SKILL = REPO / "skills" / "ai-writing-cleanup"
OUT = REPO / "dist" / "ai-writing-cleanup.bundle.md"


def version():
    import json
    return json.loads((REPO / ".claude-plugin" / "plugin.json")
                      .read_text(encoding="utf-8"))["version"]


HEADER = """# AI Writing Cleanup: complete ruleset

Version {version}.

One file holding every rule from the ai-writing-cleanup skill. It exists for an
agent that cannot load a skill directory and needs the whole ruleset in a single
read.

**How to use this file.** Read all of it, then edit the target document against
it. Rules 1 through 8 remove the texture of machine writing. Rules 9 through 18
apply technical-writing discipline. The reference sections at the end hold the
detail behind each rule.

**The rule that outranks every other one.** Preserve technical truth. Every
number, name, version, command, API, file path, code snippet, config value, and
part number stays exactly as the author meant it. If a rewrite for style would
change a technical meaning, keep the meaning and find other wording. If you
cannot tell whether a change preserves a fact, leave the text alone and say so
in the change list. Never touch text inside code blocks, command examples,
config samples, or literal output.

**Verify your work.** The repository ships a checker that counts what judgment
cannot. Run it before and after your edit:

```bash
python3 skills/ai-writing-cleanup/scripts/check_writing.py DRAFT --json
python3 skills/ai-writing-cleanup/scripts/check_writing.py DRAFT --fail-on mechanics
```

**Output format.** Return the rewrite, then a short change list grouped by issue
type. Say which items you left alone to protect a technical meaning. That line is
usually the most useful one.

This file is generated. Edit the sources under `skills/ai-writing-cleanup/` and
run `python3 tools/build_bundle.py`.

"""

PARTS = [
    ("SKILL.md", "Part A: the skill", SKILL / "SKILL.md"),
    ("references/ai-tells.md", "Part B: catalog of machine-writing tells",
     SKILL / "references" / "ai-tells.md"),
    ("references/tech-pub-rules.md", "Part C: technical publication rules",
     SKILL / "references" / "tech-pub-rules.md"),
]


def strip_frontmatter(text):
    """Drop a leading YAML frontmatter block."""
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    return text[end + 4:].lstrip("\n")


def demote(text, levels=1):
    """Push every ATX heading down so the bundle keeps one heading tree."""
    out = []
    in_fence = False
    for line in text.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
        elif not in_fence and stripped.startswith("#"):
            line = "#" * levels + line
        out.append(line)
    return "\n".join(out)


def build():
    chunks = [HEADER.replace("{version}", version())]
    for rel, title, path in PARTS:
        body = demote(strip_frontmatter(path.read_text(encoding="utf-8")))
        chunks.append(
            "\n---\n\n# {title}\n\nSource: `{rel}`\n\n{body}\n".format(
                title=title, rel=rel, body=body.strip()))
    return "\n".join(chunks).rstrip() + "\n"


def main():
    text = build()
    if "--check" in sys.argv[1:]:
        if not OUT.is_file():
            print("dist bundle is missing. Run python3 tools/build_bundle.py")
            return 1
        if OUT.read_text(encoding="utf-8") != text:
            print("dist bundle is stale. Run python3 tools/build_bundle.py")
            return 1
        print("bundle is current")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print("wrote {} ({:,} bytes)".format(
        OUT.relative_to(REPO), len(text.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
