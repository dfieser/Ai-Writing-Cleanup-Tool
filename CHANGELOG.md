# Changelog

## 1.2.0

### Changed

- Rule 9 now turns on genre rather than treating every passive as a defect.
  Active stays the default for procedures, manuals, work instructions, specs,
  READMEs, release notes, reports, and proposals, where a dropped actor is a
  safety problem. Academic engineering and science papers write Methods, and most
  of Results, in the passive by convention, and the skill now leaves those alone.
  The convention is sectional: an Introduction, Discussion, or Conclusions
  section carries the authors' own claims and still reads active.
- Three things stay defects in any genre: passive that hides an actor the reader
  must act on, passive stacked until the sentence loses its subject, and
  expletive passive such as `It was determined that`, which is a hidden verb in a
  passive coat.
- `references/tech-pub-rules.md` section 1 gained a genre table and a reordered
  test. Ask the genre question first, then ask whether the reader needs to know
  who acts.
- The checker's advice for check 10 no longer says to convert every passive. It
  names the genre split, and the `--json` guidance note says the same to an agent.
- The frontmatter description, `README.md`, `AGENTS.md`, and the wiki rule table
  all state the rule the same way.

The detector itself is unchanged. It still reports every passive construction,
because whether one is a defect depends on the document, which is a judgment the
skill makes rather than a regular expression.

## 1.1.2

### Added

- A `publish wiki` workflow. It syncs `wiki/` to the GitHub wiki from GitHub
  itself, so publishing no longer needs a local clone or a terminal. A push to
  the default branch touching `wiki/` triggers it, and the Actions tab can start
  it by hand. It authenticates with the built-in `GITHUB_TOKEN` and falls back to
  a `WIKI_TOKEN` secret if this repository requires one for wiki writes.

### Changed

- `README.md` and `CLAUDE.md` now name the workflow as the way to publish the
  wiki, with `publish-wiki.sh` as the terminal alternative rather than the only
  route.

## 1.1.1

### Changed

- Synced `SKILL.md` from upstream. It gained a section titled "Scope is settled
  before the edit starts", which argues the grounds for rules 4, 5, 9, 10, and 11
  and bars dropping any of them, plus a reworked frontmatter description and a
  note that Part 1 and Part 2 are an organizing split rather than a ranking.
- `AGENTS.md` now separates judging a single heuristic flag from dropping a rule,
  so the agent guidance matches that new section.
- Regenerated `dist/ai-writing-cleanup.bundle.md`.

`check_writing.py` and both reference files are unchanged upstream, so the
checker keeps the fixes below.

## 1.1.0

Made the repository usable by an agent that arrives with nothing but the link,
or with the folder dropped into a workspace.

### Added

- `AGENTS.md`, the entry point. Four task recipes, the checker contract, the
  JSON keys, and the rules an agent must not break.
- `CLAUDE.md`, pointing at `AGENTS.md` and covering work inside the repository.
- `--json` on the checker, a parseable report carrying counts, per-category
  findings with line numbers, sentence statistics, and a suggestion wherever one
  exists.
- `--fail-on` on the checker, which turns counts into an exit code. It takes
  `mechanics`, `heuristics`, `any`, or a comma separated list of categories.
  Exit 1 means a selected category is above zero, and exit 2 means bad usage.
- `dist/ai-writing-cleanup.bundle.md`, the whole ruleset in one file for an agent
  with no skill loader. `tools/build_bundle.py` generates it, and CI fails when
  it drifts from the sources.
- `install.sh --into DIR`, which installs into any workspace from any working
  directory. The installer now ends with parseable `SKILL_PATH=` and `CHECKER=`
  lines.

### Changed

- The checker rejects an unknown option with exit 2 instead of ignoring it, so a
  mistyped flag fails loudly rather than scanning the wrong thing.
- CI gates with `--fail-on` rather than by grepping the summary line.

### Fixed

- Markdown link syntax, `[label](url)`, reported as a parenthetical prose aside.
  Every document with a link failed its own parenthesis check, which made
  `--fail-on mechanics` unusable on a README. Link targets are now exempt, and a
  real aside such as `(it loads at boot)` still gets flagged.

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
