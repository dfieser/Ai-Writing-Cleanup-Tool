# AI Writing Cleanup

A Claude skill that edits technical writing so it reads like a knowledgeable
person wrote it rather than a language model. It strips the tells of machine
prose and applies ordinary technical-writing discipline. It changes no technical
fact.

> **Handing this to an agent?** Point it at [AGENTS.md](AGENTS.md), which holds
> the task recipes, the checker contract, and the rules it must not break. An
> agent needs no installation to use the skill. It reads
> `dist/ai-writing-cleanup.bundle.md`, edits against it, and verifies with
> `check_writing.py --fail-on mechanics`. To drop the repository into a workspace
> and let agents take over, unzip it there and run
> `bash install.sh --into /path/to/workspace`.

The repository ships three parts.

| Part | Job |
| --- | --- |
| `skills/ai-writing-cleanup/SKILL.md` | The 18 editing rules, with worked examples. Claude reads these and makes the judgment calls. |
| `skills/ai-writing-cleanup/scripts/check_writing.py` | A deterministic scan. It reports problems with line numbers and never rewrites. |
| `skills/ai-writing-cleanup/references/` | Longer reference material the skill opens when it needs detail. |

The split matters. Rewriting a sentence takes judgment, so Claude does that.
Counting em dashes takes none, so the script does it and hands you a number
before the edit and after. You can check the work instead of trusting it.

For a full pass, read `examples/before.md` and then `examples/after.md`.

## What it fixes

Part 1 of the skill removes the machine texture:

- em dashes, including a spaced en dash or a double hyphen standing in for one
- scare quotes, and quotation marks used for emphasis
- parentheses around asides that belong in the sentence
- sentences that all run the same length, and the habit of listing things in threes
- openers that delay the point to the end of the sentence
- buzzwords, filler, and the small summarizing flourish that closes each section

Part 2 applies technical-writing discipline:

- passive voice outside the genres that use it, such as a journal Methods section
- hidden verbs, such as `perform an inspection of` for `inspect`
- noun stacks such as `retry configuration file parser validation logic`
- `this` and `it` with no clear referent
- tense drift, and terminology that wanders between synonyms
- abbreviations that cost more to define than the short form ever saves
- vague cross-references, forward references, and pointers such as `see below`

One rule outranks the rest. Every number, command, file path, API name, version,
and part number survives the edit exactly as written. If a cleaner sentence would
change a technical meaning, the skill keeps the meaning and finds another
wording. If a sentence is ambiguous, the skill leaves it alone and says so in the
change list.

## Install

### For your user account

```bash
git clone https://github.com/dfieser/Ai-Writing-Cleanup-Tool.git
cd Ai-Writing-Cleanup-Tool
./install.sh
```

The installer copies the skill to `~/.claude/skills/ai-writing-cleanup`. Three
flags change what it does:

- `--link` symlinks the skill instead of copying it, so `git pull` updates the
  installed copy.
- `--project` installs to `.claude/skills` in the current directory, which
  commits the skill alongside the project that needs it.
- `--uninstall` removes an installed copy.

Start a new Claude session afterward, because skills load at startup.

### As a plugin

The repository doubles as a plugin marketplace. Run these inside Claude Code:

```
/plugin marketplace add dfieser/Ai-Writing-Cleanup-Tool
/plugin install ai-writing-cleanup@ai-writing-cleanup-tool
```

### By hand

Copy the `skills/ai-writing-cleanup` folder into one of two places:

- `~/.claude/skills/` to use the skill in every project
- `.claude/skills/` inside a repository, to share it with everyone who clones
  that repository

## Using it

Ask in plain language. The skill triggers on requests to clean up, tighten,
clarify, or humanize writing, and on the complaint that a draft reads like
ChatGPT.

> Clean up README.md. It reads like a machine wrote it.

> Tighten this procedure so it matches our style guide.

> This section sounds generic. Fix it, but do not touch any of the numbers.

Claude reads the whole document first, runs the checker, rewrites, runs the
checker again, then returns the clean text with a change list grouped by issue
type. That second scan is the part that matters. Models reintroduce these
patterns without noticing.

## Running the checker by itself

The script needs Python 3.9 or later. It imports only the standard library, so
you install nothing.

```bash
python3 skills/ai-writing-cleanup/scripts/check_writing.py draft.md
cat draft.md | python3 skills/ai-writing-cleanup/scripts/check_writing.py -
python3 skills/ai-writing-cleanup/scripts/check_writing.py draft.md --quiet
```

`--quiet` prints the summary line by itself. Here it is on `examples/before.md`:

```
SUMMARY: needs work.  em-dashes=3 scare-quotes=2 parentheses=1 buzzwords=5 wordy=3 filler=2
         front-loaded=3 passive=10 hidden-verbs=2 noun-stacks(4+)=2
         weak-abbrev=1 vague-pronouns=4 first-person=2
         xref-defects=2 section-refs=0
```

`--json` prints the same findings as a parseable report, with line numbers and a
suggestion wherever one exists. Agents should read that rather than the text.

`--fail-on` turns a count into an exit code, which is what a build or an agent
branches on:

```bash
python3 skills/ai-writing-cleanup/scripts/check_writing.py doc.md \
  --quiet --fail-on mechanics
```

Exit 0 means the selected categories are clear, 1 means at least one is above
zero and stderr names which, and 2 means bad usage. Without `--fail-on` the exit
code is always 0, so a plain scan reports without gating.

Gate on `mechanics`. The `heuristics` group fails on correct prose, so a build
that gates on it blocks good writing.

### What the report covers

The full report prints 16 numbered sections with line numbers: em dashes,
quotation marks, parentheses, buzzwords, wordy phrases, filler, sentence length
statistics, comma pileups, front-loaded sentences, passive voice, hidden verbs,
noun stacks, abbreviations, pronouns, tense mix, and cross-references.

Several sections rank findings instead of lumping them together. Scare quotes
are defects to delete, while literal strings and interface labels go on a review
list, because house style decides whether those take quotes, code formatting, or
bold. Parentheses split the same way. Prose asides and figure callouts come out,
while unit conversions and part numbers go on the review list. The script never flags math,
citations, list markers, or nomenclature definitions, so
`high entropy alloys (HEA)` passes in silence.

### Where it guesses

The script skips fenced code blocks and inline code spans, so command examples
and config samples produce no false hits. Passive voice, noun stacks, tense, and
cross-references are still heuristic, and they misfire. Scan `examples/after.md`,
a document the skill already cleaned, and it flags `bullet claims better
performance` as a four-noun stack. That is not a noun stack, because `claims` is
the verb.

Read each flag and judge it. Do not rewrite everything the script lists. A clean
report is a floor, not proof that the prose is good.

## Documentation

The [wiki](https://github.com/dfieser/Ai-Writing-Cleanup-Tool/wiki) goes deeper
than this page:

- **The Rules** lists all 18 rules and maps each one to the check that finds it.
- **Checker Reference** explains all 16 checks and where the heuristics guess.
- **Editing Workflow** covers how to ask, what comes back, and how to review it.
- **FAQ** answers the questions that come up first.

Those pages live in `wiki/` here, so they get reviewed and scanned with the rest
of the documentation. The GitHub wiki is a separate git repository, and the
`publish wiki` workflow copies them across. It runs on GitHub, so it needs no
local clone. Push a change under `wiki/` to the default branch, or start the
workflow by hand from the Actions tab.

With a clone, `./publish-wiki.sh` does the same thing from a terminal, and
`--dry-run` shows the diff first.

## Repository layout

```
AGENTS.md             entry point for an agent, with task recipes
CLAUDE.md             notes for Claude Code working inside this repository
.claude-plugin/       plugin and marketplace manifests
dist/                 the whole ruleset as one generated file
examples/             a before and after pair, with the change list
skills/
  ai-writing-cleanup/
    SKILL.md          the 18 rules
    references/       detailed reference material
    scripts/          check_writing.py
tests/                unit tests for the checker
tools/build_bundle.py regenerates the one-file ruleset
tools/build_release.py builds the zip you upload to an account
tools/sync_version.py  stamps the version into the skill
wiki/                 source for the GitHub wiki pages
install.sh            installer
publish-wiki.sh       pushes wiki/ to the GitHub wiki from a terminal
.github/workflows/    tests, the documentation gate, and the wiki publisher
```

## Updating an account copy

A skill uploaded to a Claude account is the copy that follows you into other
workspaces, and uploading is the only way to change it. Nothing in a clone
reaches it.

Build the package:

```bash
python3 tools/build_release.py
```

That writes `dist/ai-writing-cleanup-<version>.zip` holding the skill and
nothing else. Upload it at claude.ai under Settings, Capabilities, Skills. Every
CI run also attaches the same zip, so you can download it from the Actions tab
without a clone.

The version lives in `.claude-plugin/plugin.json`. `tools/sync_version.py`
stamps it into the SKILL.md frontmatter and into `check_writing.py`, so a copy
that has travelled somewhere can still say what it is:

```bash
python3 skills/ai-writing-cleanup/scripts/check_writing.py --version
```

CI fails when those drift apart, and the release build refuses to package an
unstamped skill.

## Contributing

Run the tests before you send a change:

```bash
python3 -m unittest discover -s tests -v
```

The suite scans this README, `CONTRIBUTING.md`, and `examples/after.md` for em
dashes, which holds the repository to the standard its own skill teaches.
`CONTRIBUTING.md` covers the rest.

## License

MIT. See `LICENSE`.
