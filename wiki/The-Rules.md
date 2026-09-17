# The Rules

`SKILL.md` holds 18 rules in two parts. Part 1 removes the texture that marks
machine writing. Part 2 applies the discipline any technical editor would apply.
Claude reads them as an editor's instincts, not as a checklist to satisfy. When
a rule and plain clarity conflict, clarity wins.

The last column names the check in `check_writing.py` that finds the problem.
Rules with no check need judgment, so no regular expression can catch them.

## Part 1: remove the machine texture

| # | Rule | Check |
| --- | --- | --- |
| 1 | No em dashes. None. | 1 |
| 2 | Use quotation marks only for real quotations. | 2 |
| 3 | Use parentheses only where they are required. | 3 |
| 4 | Keep sentences short. Vary their length. | 7, 8 |
| 5 | Get to the point early. Do not front-load the sentence. | 9 |
| 6 | Raise specificity. Kill predictable phrasing. | none |
| 7 | Cut buzzwords and flowery language. Use simple words. | 4, 5, 6 |
| 8 | Every sentence earns its place. Cut the flourish. | none |

## Part 2: technical writing discipline

| # | Rule | Check |
| --- | --- | --- |
| 9 | Use active voice unless passive earns its place. | 10 |
| 10 | Free the hidden verbs. | 11 |
| 11 | Break up noun stacks. | 12 |
| 12 | Name the thing instead of using a pronoun. | 14 |
| 13 | Keep tense and terminology consistent and standard. | 15 |
| 14 | Make abbreviations earn their place. | 13 |
| 15 | Break long content into small pieces. | 7 |
| 16 | Punctuate adjectives correctly. | none |
| 17 | Make cross-references exact, and use them only when essential. | 16 |
| 18 | Write at the level of the field. | none |

## The rules that need the most explaining

### 1. No em dashes

The finished document contains zero. Use a period for two independent thoughts,
a comma for a light aside, or a colon when the second half explains the first.
Often two sentences is the cleanest fix. Do not swap an em dash for parentheses,
because rule 3 restricts those just as tightly.

This covers the disguises: a spaced en dash and a double hyphen standing in for
one. Real hyphens in compounds such as `read-only` and `end-to-end` stay.

> Input: The API is fast — it returns in under 50ms — but it has no caching.
>
> Output: The API is fast. It returns in under 50ms, but it has no caching.

> Input: There is one hard requirement — every request must be authenticated.
>
> Output: There is one hard requirement: every request must be authenticated.

### 2. Quotation marks

Quotes around an ordinary word signal that the writer does not fully mean it.
A technical reader cannot tell which meaning applies, so the sentence turns
evasive. Is the mode actually safe, or only `safe`?

> Input: The scheduler enters a "safe" mode when the queue fills up.
>
> Output: The scheduler stops accepting jobs when the queue fills up.

Never use quotes for emphasis. They read as sarcasm and reverse the meaning. A
sign reading `Do not remove the "cover"` suggests the cover is not really a
cover.

Four jobs still take quotes: quoting a named source, showing the exact string a
reader types or sees, defining a term, and marking a title.

### 10. Free the hidden verbs

A hidden verb is an action turned into a noun that needs a weak helper verb.
Find the action and make it the verb.

| Buried | Freed |
| --- | --- |
| perform an inspection of | inspect |
| conduct an analysis of | analyze |
| provide a description of | describe |
| make a determination | determine |
| is indicative of | indicates |
| has the ability to | can |
| it is necessary to verify | verify |

### 11. Break up noun stacks

Three or more nouns in a row modifying each other force the reader to work out
which noun modifies which. Two are usually fine. Three is a warning. Four or more
is almost always broken. Unstack by adding prepositions and verbs, working from
the last noun backward. The head noun is the last one, so make it the subject.

> Input: system configuration parameter validation failure
>
> Output: the system failed to validate a configuration parameter

> Input: The aircraft fuel system pressure sensor calibration procedure is
> documented in Section 4.
>
> Output: Section 4 describes how to calibrate the pressure sensor in the fuel
> system.

One exception matters. An established multi-word technical term is a name, not a
stack. `Fuel pump housing` and `transport layer security` stay intact.

### 12. Name the thing instead of using a pronoun

Repeating the noun is correct in technical documentation, not inelegant.
Three offenders come up most:

- **Vague demonstratives.** A sentence opening `This causes` sends the reader
  hunting. Name it: the pressure drop causes. Keep a demonstrative only when a
  noun follows it, such as this valve.
- **Expletive openers.** `It is necessary to check the seal` and `There are
  three conditions that trigger a rollback` bury the subject behind a
  placeholder. Write: check the seal, and three conditions trigger a rollback.
- **First person.** Drop we, our, and I. The document speaks for the system, not
  for its authors. `We recommend closing the valve` becomes: close the valve.

## Full text

Every rule carries worked examples in
[SKILL.md](https://github.com/dfieser/Ai-Writing-Cleanup-Tool/blob/HEAD/skills/ai-writing-cleanup/SKILL.md).
Two reference files go deeper:

- [ai-tells.md](https://github.com/dfieser/Ai-Writing-Cleanup-Tool/blob/HEAD/skills/ai-writing-cleanup/references/ai-tells.md)
  catalogs machine-writing tells, with plain-word swaps.
- [tech-pub-rules.md](https://github.com/dfieser/Ai-Writing-Cleanup-Tool/blob/HEAD/skills/ai-writing-cleanup/references/tech-pub-rules.md)
  covers voice, nominalizations, noun stacks, referents, tense, terminology,
  abbreviations, chunking, adjective punctuation, quotes, and parentheses.
