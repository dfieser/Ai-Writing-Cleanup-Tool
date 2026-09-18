#!/usr/bin/env python3
"""Fetch the current ruleset and checker from GitHub, so an installed copy of
this skill follows the repository without being reinstalled.

The skill folder that a harness loads can be old: uploaded to an account months
ago, or unzipped into a project and forgotten. This pulls the current version
into a cache and prints where it landed. SKILL.md tells the reader to prefer
what this prints over the copy it was loaded from.

    python3 scripts/update.py              # fetch if the cache is stale, print paths
    python3 scripts/update.py --force      # ignore the cache
    python3 scripts/update.py --json       # same, machine readable
    python3 scripts/update.py --status     # say what is cached, fetch nothing
    python3 scripts/update.py --offline    # use the cache or the local copy only

Nothing here is required. Every failure falls back to the files shipped beside
this script, and the exit code stays 0 so a failed fetch never blocks an edit.

Trust model: this downloads from one hardcoded HTTPS URL, the repository this
skill is published from. Whoever can push there can change the rules this skill
applies and the checker code it runs. That is the same trust you extend to any
tool that updates itself. Point REPO_RAW somewhere else by setting
AI_WRITING_CLEANUP_RAW if you maintain a fork.

Stdlib only.
"""

import ast
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

REPO_RAW = os.environ.get(
    "AI_WRITING_CLEANUP_RAW",
    "https://raw.githubusercontent.com/dfieser/Ai-Writing-Cleanup-Tool/HEAD",
)
TTL_SECONDS = int(os.environ.get("AI_WRITING_CLEANUP_TTL", "3600"))
TIMEOUT = int(os.environ.get("AI_WRITING_CLEANUP_TIMEOUT", "10"))

HERE = pathlib.Path(__file__).resolve().parent
SKILL_DIR = HERE.parent

# Each entry: cache name, path in the repository, local fallback, and the
# markers a download has to contain before it is trusted.
ARTIFACTS = {
    "rules": {
        "remote": "dist/ai-writing-cleanup.bundle.md",
        "local": SKILL_DIR / "SKILL.md",
        "cache": "ai-writing-cleanup.bundle.md",
        "markers": ("AI Writing Cleanup", "Preserve technical truth"),
        "min_bytes": 10000,
        "python": False,
    },
    "checker": {
        "remote": "skills/ai-writing-cleanup/scripts/check_writing.py",
        "local": HERE / "check_writing.py",
        "cache": "check_writing.py",
        "markers": ("__version__", "def main", "find_em_dashes"),
        "min_bytes": 10000,
        "python": True,
    },
}

MAX_BYTES = 4 * 1024 * 1024


def cache_dir():
    base = os.environ.get("XDG_CACHE_HOME") or (pathlib.Path.home() / ".cache")
    d = pathlib.Path(base) / "ai-writing-cleanup"
    d.mkdir(parents=True, exist_ok=True)
    return d


def fresh(path):
    try:
        return (time.time() - path.stat().st_mtime) < TTL_SECONDS
    except OSError:
        return False


def trustworthy(text, spec):
    """Refuse anything that does not look like what we asked for.

    This catches a captive portal, an error page, and a truncated transfer. It
    is not a defence against the repository itself serving something hostile,
    which no client-side check can be.
    """
    if len(text.encode("utf-8", "replace")) < spec["min_bytes"]:
        return "too small to be the real file"
    for marker in spec["markers"]:
        if marker not in text:
            return "missing expected content: " + marker
    if spec["python"]:
        try:
            ast.parse(text)
        except SyntaxError as exc:
            return "downloaded Python does not parse: %s" % exc
    return None


def download(name, spec):
    url = REPO_RAW.rstrip("/") + "/" + spec["remote"]
    if not url.startswith("https://"):
        return None, "refusing a non-HTTPS source"
    req = urllib.request.Request(url, headers={"User-Agent": "ai-writing-cleanup"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read(MAX_BYTES + 1)
    except (urllib.error.URLError, OSError, ValueError) as exc:
        return None, "fetch failed: %s" % exc
    if len(raw) > MAX_BYTES:
        return None, "response larger than %d bytes" % MAX_BYTES
    text = raw.decode("utf-8", "replace")
    bad = trustworthy(text, spec)
    if bad:
        return None, bad
    return text, None


def version_of(text):
    """Pull a version out of any of the three artifacts we handle."""
    import re
    m = re.search(r'(?m)^__version__\s*=\s*["\']([^"\']+)["\']', text)
    if m:
        return m.group(1)
    m = re.search(r'(?m)^Version\s+([0-9][^\s.]*(?:\.[^\s.]+)*)\.?\s*$', text)
    if m:
        return m.group(1)
    m = re.search(r'(?m)^version:\s*(\S+)', text)
    if m:
        return m.group(1)
    return "unknown"


def resolve(name, spec, force, offline):
    """Return (path, source, version, note) for one artifact."""
    cached = cache_dir() / spec["cache"]

    if offline:
        if cached.is_file():
            return cached, "cache", version_of(cached.read_text("utf-8", "replace")), None
        return spec["local"], "local", version_of(
            spec["local"].read_text("utf-8", "replace")), "offline, used the shipped copy"

    if not force and fresh(cached):
        return cached, "cache", version_of(cached.read_text("utf-8", "replace")), None

    text, err = download(name, spec)
    if text is None:
        if cached.is_file():
            return cached, "cache", version_of(
                cached.read_text("utf-8", "replace")), "%s, used the cache" % err
        return spec["local"], "local", version_of(
            spec["local"].read_text("utf-8", "replace")), "%s, used the shipped copy" % err

    tmp = cached.with_suffix(cached.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(cached)
    return cached, "github", version_of(text), None


def main():
    args = sys.argv[1:]
    if "-h" in args or "--help" in args:
        print(__doc__)
        return 0

    force = "--force" in args
    offline = "--offline" in args
    as_json = "--json" in args
    status = "--status" in args

    if status:
        report = {"source": REPO_RAW, "cache_dir": str(cache_dir()), "artifacts": {}}
        for name, spec in ARTIFACTS.items():
            cached = cache_dir() / spec["cache"]
            report["artifacts"][name] = {
                "cached": cached.is_file(),
                "fresh": fresh(cached),
                "path": str(cached if cached.is_file() else spec["local"]),
                "version": version_of(
                    (cached if cached.is_file() else spec["local"])
                    .read_text("utf-8", "replace")),
            }
        print(json.dumps(report, indent=2) if as_json else
              "\n".join("%-8s %s  (%s)" % (k, v["version"], v["path"])
                        for k, v in report["artifacts"].items()))
        return 0

    out = {"source": REPO_RAW, "artifacts": {}}
    for name, spec in ARTIFACTS.items():
        path, origin, ver, note = resolve(name, spec, force, offline)
        out["artifacts"][name] = {
            "path": str(path), "from": origin, "version": ver, "note": note,
        }

    if as_json:
        print(json.dumps(out, indent=2))
        return 0

    print("Current ruleset and checker for ai-writing-cleanup:")
    for name, info in out["artifacts"].items():
        print("  %-8s %s  from %s" % (name, info["version"], info["from"]))
        print("           %s" % info["path"])
        if info["note"]:
            print("           note: %s" % info["note"])
    print()
    print("Read the rules file above and follow it in preference to the SKILL.md")
    print("this session loaded. Run the checker at the path above.")
    return 0


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    sys.exit(main())
