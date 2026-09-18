#!/usr/bin/env python3
"""Build the upload package for the skill.

Produces a zip holding just the skill folder, which is what you upload to an
account at claude.ai under Settings, Capabilities, Skills. Uploading is the only
way to change the account copy, and the account copy is what follows you into
other workspaces.

    python3 tools/build_release.py            # write dist/<name>-<version>.zip
    python3 tools/build_release.py --check    # verify it would build, write nothing

The version comes from .claude-plugin/plugin.json and has to be stamped into the
skill first, so this refuses to build when tools/sync_version.py disagrees.

Stdlib only.
"""

import json
import pathlib
import subprocess
import sys
import zipfile

REPO = pathlib.Path(__file__).resolve().parents[1]
SKILL_DIR = REPO / "skills" / "ai-writing-cleanup"
DIST = REPO / "dist"
SKIP_DIRS = {"__pycache__", ".git", ".pytest_cache"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def version():
    return json.loads((REPO / ".claude-plugin" / "plugin.json")
                      .read_text(encoding="utf-8"))["version"]


def wanted_files():
    for path in sorted(SKILL_DIR.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix in SKIP_SUFFIXES:
            continue
        yield path


def main():
    check = "--check" in sys.argv[1:]

    synced = subprocess.run(
        [sys.executable, str(REPO / "tools" / "sync_version.py"), "--check"],
        capture_output=True, text=True)
    if synced.returncode != 0:
        print(synced.stdout.strip())
        print("refusing to build a package whose version is not stamped")
        return 1

    ver = version()
    files = list(wanted_files())
    if not any(f.name == "SKILL.md" for f in files):
        print("no SKILL.md in the skill folder")
        return 1

    out = DIST / ("ai-writing-cleanup-%s.zip" % ver)

    if check:
        print("would write %s" % out.relative_to(REPO))
        for f in files:
            print("  %s" % f.relative_to(SKILL_DIR.parent))
        return 0

    DIST.mkdir(parents=True, exist_ok=True)
    for stale in DIST.glob("ai-writing-cleanup-*.zip"):
        if stale != out:
            stale.unlink()
            print("removed stale %s" % stale.relative_to(REPO))

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(f, f.relative_to(SKILL_DIR.parent))

    print("wrote %s (%d files, %s bytes)"
          % (out.relative_to(REPO), len(files), format(out.stat().st_size, ",")))
    print("upload it at claude.ai, Settings, Capabilities, Skills")
    return 0


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    sys.exit(main())
