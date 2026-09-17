# Checker Reference

`check_writing.py` is a deterministic scan. It reports and never rewrites, so
you can target an edit and then verify it. Run it on the source to plan, and on
the rewrite to confirm the counts dropped.

```bash
python3 skills/ai-writing-cleanup/scripts/check_writing.py draft.md
cat draft.md | python3 skills/ai-writing-cleanup/scripts/check_writing.py -
python3 skills/ai-writing-cleanup/scripts/check_writing.py draft.md --quiet
```

The script needs Python 3.9 or later and imports only the standard library.
`--quiet` prints the summary line by itself, which suits a pre-commit hook.
`-h` and `--help` print the usage text.

The script always exits 0, so a build gate has to read the summary:

```bash
python3 .../check_writing.py doc.md --quiet | grep -q 'em-dashes=0' || exit 1
```

## What the report covers

| # | Check | Flags |
| --- | --- | --- |
| 1 | Em dashes | The em dash, a spaced en dash, and a double hyphen used as a break |
| 2 | Quotation marks | Scare quotes, split from literal strings and interface labels |
| 3 | Parentheses | Prose asides and callouts, split from cases a style guide tolerates |
| 4 | Buzzwords | Single words with a plain replacement, and the replacement to use |
| 5 | Wordy phrases | Multi-word phrases one word says better |
| 6 | Filler phrases | Throat-clearing openers that carry no content |
| 7 | Sentence length | Mean, longest, and the coefficient of variation |
| 8 | Comma lists | Sentences heavy with commas, and rule-of-three lists |
| 9 | Front-loaded sentences | The point delayed behind a long opening clause |
| 10 | Passive voice | A passive construction where an actor exists |
| 11 | Hidden verbs | An action buried in a noun with a weak helper verb |
| 12 | Noun stacks | Three or more nouns in a row, with four or more called likely defects |
| 13 | Abbreviations | Short forms that cost more than they save |
| 14 | Pronouns | Vague demonstratives, expletive openers, first and second person |
| 15 | Tense | The mix of present, past, and future |
| 16 | Cross-references | Forward references and vague pointers |

## The checks that rank their findings

Four checks separate real defects from cases that need a decision. That split is
what keeps the report usable.

**Quotation marks.** Scare quotes have no attribution and no literal-string cue,
and those are defects to delete. Literal strings and interface labels go on a
review list, because house style decides whether they take quotes, code
formatting, or bold. A real quotation with an attributing verb is not flagged.

**Parentheses.** The remove list holds prose asides, with full clauses marked
separately from short qualifiers, plus every figure, table, section, and equation
callout, because those belong in the sentence. The review list holds what a style
guide tolerates and this skill does not accept by default: unit conversions and
tolerances, part and model numbers, and the plural marker `(s)`. Rewrite each one
unless you can name the rewrite you rejected.

Never reported: math, list markers, author-year citations, and nomenclature
definitions in either order. Both `high entropy alloys (HEA)` and
`HEA (high entropy alloy)` pass in silence, because the check matches the
initials against the short form beside them. The check still flags an ordinary lowercase
aside.

**Abbreviations.** Three cases, ranked. A short form defined in parentheses and
then used once or twice is the real defect, because the definition cost more than
the short form saved. An undefined short form coined once usually reads better
written out. A widely known abbreviation used once appears for information only
and needs no action.

**Cross-references.** The report lists every section reference for review,
because each one has to justify itself. Three are defects: a reference pointing past the
current section, a pointer such as `see below` or `as discussed above`, and a
mention of `supporting information`, `supplementary material`, or `the appendix`
that names no specific item.

Forward detection needs numbered headings, either Markdown headings starting with
a number or LaTeX sectioning commands. Without them the report says it skipped
the forward check. A backward pointer followed by a citation, such as
`as shown previously [12]`, counts as a literature reference and passes.

## Where it guesses

The script skips fenced code blocks, indented blocks, and inline code spans, so
command examples and config samples produce no false hits. A flag such as
`--quiet` in a code block does not register as a dash.

Checks 10, 12, 15, and 16 are heuristic, and they misfire. Scanning
`examples/after.md`, a document the skill already cleaned, still flags
`bullet claims better performance` as a four-noun stack. `claims` is the verb there, so the phrase is not a
stack. Markdown link syntax can read as a parenthetical aside for
the same reason.

Two habits keep the report honest:

1. Read each flag and judge it. Do not rewrite everything the script lists.
2. Treat a clean report as a floor, not as proof that the prose is good. Nothing
   here measures whether the document says the right thing.

## A page about defects looks like a defective page

A document that quotes bad writing to teach it, such as
[The Rules](The-Rules) or `examples/before.md`, reports high counts. The checker
cannot tell a quoted example from the author's own prose. Scan the sections you
wrote, and expect the teaching material to stay red.
