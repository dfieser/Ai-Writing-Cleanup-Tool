# Contributing

## Run the tests first

```bash
python3 -m unittest discover -s tests -v
```

The suite covers the checker and also scans this file, `README.md`, and
`examples/after.md` for em dashes. A repository about clean writing that ships
dirty writing has an obvious problem, so the check runs on every change.

## Which file to change

Decide what kind of change you have, then edit one place.

| Change | File |
| --- | --- |
| A rule, or how Claude should apply one | `skills/ai-writing-cleanup/SKILL.md` |
| Detail behind a rule, with more examples | `skills/ai-writing-cleanup/references/` |
| What the scan detects or reports | `skills/ai-writing-cleanup/scripts/check_writing.py` |
| A buzzword, wordy phrase, or filler entry | The vocabulary tables at the top of `check_writing.py` |

The rules and the script have to agree. If you add a rule that the script can
detect without guessing, add the detection too. If you add detection, say in
`SKILL.md` what a writer should do about the finding.

## The bar for a new check

The script reports and never rewrites, so a noisy check costs a reader more than
a missing one. Before you add a check, answer three questions:

1. Does it fire on real writing and stay quiet on clean writing? Run it over
   `examples/before.md` and `examples/after.md` to find out.
2. Can a writer act on the message? A flag that says something is wrong without
   naming the fix wastes the reader's time.
3. Is it deterministic? Anything that needs judgment belongs in `SKILL.md`, where
   Claude applies it, not in a regular expression.

Sort findings by confidence when they vary. The quotation and parenthesis checks
already split defects from cases a house style decides, and that split is what
keeps them usable.

## Reporting a false positive

Passive voice, noun stacks, tense, and cross-references are heuristic, and they
misfire. Open an issue with the sentence that tripped the flag, the check that
fired, and what the correct reading is. A failing test case in
`tests/test_check_writing.py` helps more than a description.

Some false positives are worth keeping. The noun stack check flags
`bullet claims better performance`, which is a verb phrase, and tightening the
pattern enough to clear it would hide real four-noun stacks. Say why the tradeoff
should change, not only that the flag is wrong.

## Writing style in this repository

Documentation here follows the skill. No em dashes, no scare quotes, no
parentheses around asides, active voice, and short sentences of varying length.
Put literal strings and command flags in backticks. The scan skips code, so
`--quiet` never registers as a dash.

Check your prose before you open a pull request:

```bash
python3 skills/ai-writing-cleanup/scripts/check_writing.py README.md
```

Judge the heuristic flags rather than clearing them. A clean report is a floor.

## Commits and pull requests

Write a subject line that says what changed and why it matters. Keep unrelated
changes in separate commits. If you change the checker, note the effect on
`examples/before.md` counts in the pull request body, because that is the fastest
way for a reviewer to see the blast radius.
