# Instructions for agents

This repository holds a writing-editing skill. You are most likely here for one
of four reasons. Find yours, run the steps, and ignore the rest of this file.

Paths below are relative to this repository's root, which is the directory
holding this file. If someone unzipped the repository inside a larger workspace,
that root is a subdirectory, so prefix the paths accordingly.

## 1. Edit a document so it stops reading like a machine

You need no installation for this.

1. Get the current rules, because the copy you loaded may be old:

   ```bash
   python3 skills/ai-writing-cleanup/scripts/update.py
   ```

   It prints the path to the current ruleset and checker, fetched from the
   repository and cached for an hour. Read the rules file it names and use the
   checker it names. It exits 0 even when the fetch fails, falling back to its
   cache and then to the shipped files, so never treat a failure as a blocker.

   Working from a clone, or told to stay offline? Read
   `dist/ai-writing-cleanup.bundle.md` directly. It holds every rule in one file.
   If your harness loads skills from a directory, read
   `skills/ai-writing-cleanup/SKILL.md` instead and open the files under
   `skills/ai-writing-cleanup/references/` when you need the detail.
2. Scan the target document and keep the output:

   ```bash
   python3 skills/ai-writing-cleanup/scripts/check_writing.py TARGET --json
   ```

3. Rewrite the document against the rules. Work on whole sentences. A find and
   replace pass produces worse writing than no pass at all.
4. Scan your rewrite and compare. Em dashes must reach zero and the other
   mechanical counts must drop:

   ```bash
   python3 skills/ai-writing-cleanup/scripts/check_writing.py TARGET \
     --fail-on mechanics
   ```

   Exit 0 means the mechanical categories are clear. Exit 1 lists what remains
   on stderr. Step 4 is not optional, because models reintroduce these patterns
   without noticing.
5. Return the rewrite and a short change list grouped by issue type. Name
   anything you left alone to protect a technical meaning.

## 2. Install the skill into a workspace

One command, run from anywhere:

```bash
bash install.sh --into /path/to/workspace
```

The skill lands at `/path/to/workspace/.claude/skills/ai-writing-cleanup`, where
Claude Code picks it up on the next session. The last two lines of output are
`SKILL_PATH=` and `CHECKER=`, so parse those rather than rebuilding the paths.

Other forms:

| Command | Result |
| --- | --- |
| `bash install.sh` | Installs to `~/.claude/skills`, for every project |
| `bash install.sh --project` | Installs to `.claude/skills` under the current directory |
| `bash install.sh --link` | Symlinks rather than copies, so a pull updates it |
| `bash install.sh --uninstall` | Removes an installed copy |

If the workspace uses Claude Code plugins instead, the repository is also a
marketplace. The human runs `/plugin marketplace add dfieser/Ai-Writing-Cleanup-Tool`
and then `/plugin install ai-writing-cleanup@ai-writing-cleanup-tool`.

## 3. Check a document without editing it

```bash
python3 skills/ai-writing-cleanup/scripts/check_writing.py TARGET --json
```

The script needs Python 3.9 or later and imports only the standard library.
`TARGET` can be `-` to read standard input. Parse `counts` for the numbers and
`findings` for line-level detail. See the JSON contract below.

## 4. Gate a build or a commit on writing quality

```bash
python3 skills/ai-writing-cleanup/scripts/check_writing.py doc.md \
  --quiet --fail-on mechanics
```

Gate on `mechanics` only. The `heuristics` group fails on correct prose, so a
build that gates on it will block good writing. `.github/workflows/checks.yml`
runs this pattern against this repository's own documentation.

## The checker contract

```
python3 skills/ai-writing-cleanup/scripts/check_writing.py TARGET [options]
```

| Option | Effect |
| --- | --- |
| `--json` | Machine-readable report on stdout |
| `--quiet` | Summary line only |
| `--fail-on GROUP` | Exit 1 when a selected category is above zero |
| `--version` | Which copy of the skill this is |
| `--help` | Usage text |

Exit codes: 0 means it finished and found nothing in the categories
`--fail-on` selected, 1 means a selected category is above zero, and 2 means bad usage such as an
unknown option. Without `--fail-on` the exit code is always 0, so the scan
reports without gating.

`--fail-on` takes `mechanics`, `heuristics`, `any`, or a comma separated list of
category names such as `em-dashes,buzzwords`.

The JSON report carries these top-level keys:

| Key | Holds |
| --- | --- |
| `verdict` | `clean` or `needs-work` |
| `counts` | Every category name mapped to its count |
| `totals` | Summed `mechanics` and `heuristics` |
| `gate` | What `--fail-on` requested, what failed, and the exit code |
| `sentences` | Count, mean words, longest, variation, and long-sentence tallies |
| `findings` | Line-level detail per category, with a suggestion where one exists |
| `abbreviations` | Short forms sorted into wasteful, spell out, and introduce |
| `tense` | Present, past, and future counts |
| `notes` | Which categories guess, and the caveat that goes with them |
| `version` | The skill version that produced the report |

## Rules you must not break

**Preserve technical truth.** Every number, name, version, command, API, file
path, code snippet, config value, and part number stays exactly as the author
meant it. If a cleaner sentence would change a technical meaning, keep the
meaning and find other wording. If you cannot tell whether a change preserves a
fact, leave the text alone and say so. A cleaner sentence that says the wrong
thing is a failure, not an improvement.

**Never invent a number.** When a draft claims better performance and gives no
measurement, flag the sentence and leave it. Do not supply a figure.

**Never edit inside code.** Code blocks, command examples, config samples, and
literal output are data. The checker already skips them.

**Judge each heuristic finding, but never drop a rule.** Checks for passive
voice, noun stacks, tense, and cross-references produce false positives on verb
phrases and established terms, so decide case by case whether a given flag is a
true hit. That judgment applies to one flag, never to a rule. Every rule in the
skill is in scope, and hidden verbs, noun stacks, front-loaded sentences, and
uniform sentence length are all part of the cleanup. Do not skip one because the
pattern also turns up in human writing.

Voice is the one exception, and it turns on genre rather than on the sentence.
Active is the default for procedures, manuals, specs, READMEs, and reports. A
journal Methods section, and most of Results, is passive by the field's
convention, so its passive hits are not defects. Settle the document type first,
then edit. A clean report is a floor, not proof the prose is good.

## Working on this repository rather than with it

Run the tests before you change anything:

```bash
python3 -m unittest discover -s tests -v
```

If you edit `skills/ai-writing-cleanup/SKILL.md` or either file under
`references/`, rebuild the single-file bundle, because CI checks that it matches:

```bash
python3 tools/build_bundle.py
```

Documentation here follows the skill. `CONTRIBUTING.md` covers the bar for a new
check and the house style.
