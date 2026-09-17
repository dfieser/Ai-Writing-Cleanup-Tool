# FAQ

## Will it change my technical facts?

No. That is the one rule the skill cannot break. Every number, name, version,
command, API, file path, code snippet, config value, part number, and defined
term stays as the author meant it. When a rewrite for style would alter a
technical meaning, the skill keeps the meaning and finds other wording. When a
sentence is ambiguous, the skill leaves it alone and says so in the change list.

Review the diff anyway. Facts come first, style second.

## Why zero em dashes? Some of mine are correct.

The em dash is the most recognizable tell of machine writing, and a document
with none reads as human even when nothing else changes. Every job an em dash
does has a replacement: a period for two independent thoughts, a comma for a
light aside, a colon when the second half explains the first.

If you want to keep them, say so in the request. The skill follows your
instruction over its default. The checker still counts them, so use `--quiet`
and ignore the first number.

## Does it work on writing that is not technical?

It works, though it targets technical documents. The buzzword tables, the
abbreviation rules, the cross-reference checks, and the terminology discipline
all assume a manual, a spec, a paper, or a README. Fiction and marketing copy
get worse advice, because rules such as no parentheses and short declarative
sentences are style choices there rather than defects.

## Why does the checker flag a sentence that is correct?

Checks 10, 12, 15, and 16 are heuristic. No regular expression can pin down passive
voice, noun stacks, tense, or cross-references without parsing meaning, so they
misfire on verb phrases and established terms. Markdown link syntax reads as a
parenthetical aside for the same reason.

Read each flag and judge it. Rewriting everything the script lists makes writing
worse, not better. [Checker Reference](Checker-Reference) covers which checks
guess and why.

## The summary says `needs work` on a document I already cleaned. Why?

The verdict turns on the total across every category, including the heuristic
ones. A document can hold zero em dashes, zero scare quotes, and zero buzzwords
and still read `needs work` because of three noun stack candidates that are not
noun stacks.

Read the numbered categories rather than the verdict. The mechanical counts are
the ones that mean something: em dashes, scare quotes, parentheses, buzzwords,
wordy phrases, and filler.

## Can I run it in CI?

Yes. The script always exits 0, so gate on the summary line instead:

```bash
python3 skills/ai-writing-cleanup/scripts/check_writing.py doc.md --quiet \
  | grep -q 'em-dashes=0' || { echo "em dashes in doc.md"; exit 1; }
```

The repository runs exactly this against its own documentation. See
`.github/workflows/checks.yml`.

Gate on the mechanical counts only. Gating on passive voice or noun stacks
produces a build that fails for correct prose.

## What does it need installed?

Python 3.9 or later. The script imports only the standard library, so there is
nothing to install and nothing to update.

## Which file formats does it read?

Any plain text. It understands Markdown fences and inline code spans, and it
recognizes both Markdown and LaTeX numbered headings for the forward-reference
check. It does not read `.docx` or PDF. Export to text first.

## Can I add my own buzzwords?

Yes. The vocabulary tables sit at the top of `check_writing.py`, keyed by the
word with the plain replacement as the value. Add an entry and the check picks it
up. Adding the same guidance to `SKILL.md` keeps Claude and the script in
agreement, which matters more than either one alone.

## Where does the skill folder go?

Claude Code reads two paths: `~/.claude/skills/` for every project, and
`.claude/skills/` inside one repository, which shares the skill with anyone who
clones it. `./install.sh` writes to the first, and `./install.sh --project`
writes to the second.

For any other Claude surface, follow its own instructions for adding a skill. The
folder holds Markdown and one Python file, so nothing in it is specific to
Claude Code.

## Why did it leave a sentence unchanged?

Two reasons, and the change list names which one. Either the sentence was
ambiguous enough that no rewrite was provably safe, or the flagged phrase is an
established technical term rather than a defect. `Fuel pump housing` is a name,
not a noun stack.

A third case looks similar. When a draft claims better performance and gives no
measurement, the skill flags the sentence and leaves it, because inventing a
number would break the rule that outranks every other. Go find the number.

## Does the skill replace an editor?

No. It fixes mechanics and structure. It does not check whether the document is
correct, complete, or worth reading, and a clean report says nothing about
whether the content is right.
