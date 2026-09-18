# Editing Workflow

## How to ask

The skill triggers on plain requests. It does not need the word AI.

> Clean up README.md. It reads like ChatGPT.

> Tighten this procedure and make it match the style guide.

> This section sounds generic. Fix it, but do not touch any of the numbers.

> Give the release notes an editing pass before I publish them.

Requests to clarify, tighten, humanize, or cut wordiness all reach it, as do
complaints that a draft sounds robotic or formulaic.

## What Claude does

Six steps, in order:

1. **Gets the current rules.** The skill folder loaded into a session can be
   months old, so step 1 runs `scripts/update.py`, which fetches the current
   ruleset and checker from the repository and caches them for an hour. Claude
   then follows the fetched rules in preference to the copy it loaded. A failed
   fetch falls back to the cache and then to the shipped files, so this never
   blocks an edit.

2. **Reads the whole document.** Style edits made sentence by sentence flatten
   the structure of a document, so the first pass is about what the document is,
   who reads it, and what each section does.
3. **Runs the checker** on the source, which maps the mechanical problems and
   catches what an eye skips.
4. **Rewrites for clarity**, with latitude to restructure sentences and reorder
   within a paragraph. Sounding human is a whole-sentence judgment, so this is
   not a find and replace.
5. **Runs the checker again** on the rewrite. Models reintroduce these patterns
   without noticing, so this step is not optional. Em dashes at zero is the
   floor.
6. **Returns the rewrite and a change list** grouped by issue type.

## What comes back

```
## Cleaned version

[the full rewritten text]

## What changed

- Em dashes: removed 4, split into separate sentences or replaced with colons.
- Voice: converted 7 passive constructions to active.
- Hidden verbs: "perform an inspection of" to inspect, and 3 similar.
- Abbreviations: dropped ECS and LRU, each used only once.
- Left as-is: latency figures, API names, and the term fuel pump housing,
  which is an established term rather than a noun stack.
```

The change list stays short and grouped rather than listing every edit. The most
useful line is usually the last one. When the skill leaves something alone to
protect a technical meaning, it says so.

See [examples/after.md](https://github.com/dfieser/Ai-Writing-Cleanup-Tool/blob/HEAD/examples/after.md)
for a full pass, next to the draft it started from.

## Reviewing the result

Check three things, in this order.

**Facts first.** Diff the rewrite against the source and confirm every number,
command, file path, API name, version, and part number survived. This matters
more than any style question. A cleaner sentence that says the wrong thing is a
failure.

**Then the flagged items.** The change list names what the skill left alone and
why. Those lines need your judgment, because they are the places where style and
meaning pulled in different directions.

**Then the counts.** Run the checker yourself on the result:

```bash
python3 skills/ai-writing-cleanup/scripts/check_writing.py rewritten.md --quiet
```

Em dashes should read zero. The heuristic counts should drop, not vanish.
[Checker Reference](Checker-Reference) explains which checks guess.

## Scoping a large document

Feed one section at a time when a document runs long. The skill reads for whole
structure, and a 40-page manual exceeds what fits comfortably in one pass. Name
the section and keep the surrounding context in the request:

> Clean up the Installation chapter. The rest of the manual uses present tense
> and calls the product the controller, so match that.

Terminology consistency is the piece that suffers when you split a document.
Tell the skill which term is standard, or check the terminology line in the
change list for each section.

## When to stop

The skill edits style and structure. It does not verify that the document is
correct, complete, or useful, and it never invents a number to replace a vague
claim. When a draft says performance improved and gives no measurement, the
skill flags the sentence and leaves it for you. That flag is the signal to go
find the number, not to rewrite the sentence again.
