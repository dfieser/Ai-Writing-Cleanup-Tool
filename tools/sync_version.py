#!/usr/bin/env python3
"""Stamp the version from .claude-plugin/plugin.json into the skill.

plugin.json holds the one authoritative version. The skill folder needs its own
copy, because the folder travels on its own: uploaded to an account, copied into
`.claude/skills`, or unzipped somewhere. Without a stamp inside it, nobody can
tell which copy they are running, which is the whole problem this solves.

    python3 tools/sync_version.py           # write the version into the skill
    python3 tools/sync_version.py --check   # exit 1 if anything is out of step

Stdlib only.
"""

import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
PLUGIN = REPO / ".claude-plugin" / "plugin.json"
MARKETPLACE = REPO / ".claude-plugin" / "marketplace.json"
SKILL = REPO / "skills" / "ai-writing-cleanup" / "SKILL.md"
CHECKER = REPO / "skills" / "ai-writing-cleanup" / "scripts" / "check_writing.py"


def source_version():
    return json.loads(PLUGIN.read_text(encoding="utf-8"))["version"]


def stamp_skill(text, version):
    """Put `version:` in the frontmatter, right after `name:`."""
    if not text.startswith("---"):
        raise SystemExit("SKILL.md has no frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        raise SystemExit("SKILL.md frontmatter is not closed")
    head, rest = text[:end], text[end:]
    if re.search(r"(?m)^version:", head):
        head = re.sub(r"(?m)^version:.*$", "version: " + version, head, count=1)
    else:
        head = re.sub(r"(?m)^(name:.*)$", r"\1\nversion: " + version, head, count=1)
    return head + rest


def stamp_checker(text, version):
    if re.search(r'(?m)^__version__ = ', text):
        return re.sub(r'(?m)^__version__ = .*$',
                      '__version__ = "%s"' % version, text, count=1)
    raise SystemExit("check_writing.py has no __version__ line")


def marketplace_version():
    d = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    return d["plugins"][0].get("version")


def main():
    version = source_version()
    check = "--check" in sys.argv[1:]

    targets = [
        (SKILL, stamp_skill(SKILL.read_text(encoding="utf-8"), version)),
        (CHECKER, stamp_checker(CHECKER.read_text(encoding="utf-8"), version)),
    ]

    problems = []
    if marketplace_version() != version:
        problems.append("marketplace.json says %s, plugin.json says %s"
                        % (marketplace_version(), version))

    for path, wanted in targets:
        if path.read_text(encoding="utf-8") != wanted:
            problems.append("%s is not stamped %s"
                            % (path.relative_to(REPO), version))

    if check:
        for line in problems:
            print(line)
        if problems:
            print("run: python3 tools/sync_version.py")
            return 1
        print("version %s is consistent across plugin.json, marketplace.json, "
              "SKILL.md, and check_writing.py" % version)
        return 0

    if marketplace_version() != version:
        print("marketplace.json disagrees with plugin.json. Fix it by hand, "
              "since only you know which is right.")
        return 1

    for path, wanted in targets:
        if path.read_text(encoding="utf-8") != wanted:
            path.write_text(wanted, encoding="utf-8")
            print("stamped %s" % path.relative_to(REPO))
    print("version %s" % version)
    return 0


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    sys.exit(main())
