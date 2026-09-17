# CLAUDE.md

Read `AGENTS.md` first. It holds the task recipes, the checker contract, and the
rules that cannot be broken. This file adds only what is specific to working
inside this repository.

## Layout

- `skills/ai-writing-cleanup/SKILL.md` holds the 18 rules. The two files under
  `references/` hold the detail behind them.
- `skills/ai-writing-cleanup/scripts/check_writing.py` is the checker. It reports
  and never rewrites. Stdlib only, Python 3.9 or later.
- `dist/ai-writing-cleanup.bundle.md` is the whole ruleset in one file, generated
  by `tools/build_bundle.py`.
- `wiki/` holds the GitHub wiki pages. The `publish wiki` workflow pushes them
  when a change under `wiki/` reaches the default branch, and the Actions tab
  can start it by hand. `publish-wiki.sh` does the same from a terminal.

## Before you commit

```bash
python3 -m unittest discover -s tests
python3 tools/build_bundle.py --check
```

Rebuild the bundle with `python3 tools/build_bundle.py` after editing `SKILL.md`
or either reference file. CI fails when the bundle is stale.

## House style

Documentation here follows the skill it ships. No em dashes, no scare quotes, no
parentheses around asides, active voice, and short sentences of varying length.
Put literal strings and command flags in backticks, because the checker skips
code and a flag such as `--quiet` would otherwise read as a dash.

Check any document you touch:

```bash
python3 skills/ai-writing-cleanup/scripts/check_writing.py FILE --fail-on mechanics
```

Two documents quote bad writing to teach it, so they report defects on
purpose and stay off that gate: `examples/before.md` and `wiki/The-Rules.md`.

Judge the heuristic findings rather than clearing them. Passive voice, noun
stacks, tense, and cross-references misfire on verb phrases and established
terms.
