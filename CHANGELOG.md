# Changelog

## 1.0.0

First packaged release. The skill lived in a local Claude skills folder before
this. The repository is now its home.

### Added

- `install.sh`, which installs the skill for one user or into a single project,
  by copy or by symlink, and removes it again.
- Plugin and marketplace manifests under `.claude-plugin/`, so Claude Code can
  install the skill straight from the repository.
- A test suite in `tests/`, covering the checker and scanning the public
  documents for em dashes.
- A GitHub Actions workflow that runs the tests on three Python versions, scans
  every public document, and validates the manifests.
- `examples/before.md` and `examples/after.md`, a full editing pass with the
  change list the skill produces.
- Wiki pages under `wiki/`, covering the rules, the checker, the editing
  workflow, and a FAQ. `publish-wiki.sh` pushes them to the GitHub wiki, which
  git treats as a separate repository.

### Fixed in `check_writing.py`

Running the checker on this repository's own documentation exposed three gaps
between what `SKILL.md` documents and what the script did.

- The em dash check read raw text, so a command flag such as `--quiet` inside a
  fenced block reported as a dash. Any document about a command-line tool failed
  its own check. The check now blanks code line by line, which keeps the
  reported line numbers exact. `strip_code` cannot do this job, because it
  collapses a fenced block to a single space and loses the line count.
- `--help` hung. The option filter removed it before the help branch ran, so the
  script fell through to reading standard input and blocked there. Only `-h`
  worked. Both work now.
- A reverse nomenclature definition such as `HEA (high entropy alloy)` reported
  as a prose aside, though `SKILL.md` documents both orders as exempt. The check
  now matches the initials of the parenthetical against the short form in front
  of it, and it handles the plural. The check still flags an ordinary lowercase
  aside.

No rule changed, and no wording in `SKILL.md` or the reference files changed.
