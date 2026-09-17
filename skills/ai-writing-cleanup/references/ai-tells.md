# Catalog of machine-writing tells

A reference for the cleanup pass. You do not need to memorize this. Read it when
you want the full list behind a category, or when a draft has a tell you can feel
but cannot name. Each entry says what to do instead.

## Table of contents

1. Punctuation tells (em dashes, scare quotes, parentheses)
2. Buzzwords (plain-word swaps)
3. Filler and throat-clearing
4. Formulaic sentence constructions
5. Structural tells
6. Hedging and vague quantifiers

---

## 1. Punctuation tells

The em dash is the headline. Remove every one; this document allows zero. Also
watch for its disguises.

- Em dash `—`: replace with a period, comma, colon, or parentheses, or split
  the sentence. Choose by the job the dash was doing.
- Spaced en dash used as a break ` – `: same treatment.
- Double hyphen `--` standing in for a dash: same treatment.
- Real hyphens in compounds (`read-only`, `end-to-end`, `well-tested`) are
  correct. Leave them.
- Overused semicolons joining two full clauses: usually better as two sentences.
- Overused colons introducing every list: vary the lead-in.

Scare quotes are the second big punctuation tell. Machine text wraps ordinary
words in quotation marks to signal emphasis, hedging, or ironic distance, and
the reader is left unsure whether the term is meant literally.

- Quotes for emphasis: `Do not remove the "cover"`. This reverses the meaning and
  reads as sarcasm. Use bold, or put the important word at the end of the
  sentence.
- Quotes for hedging: `enters a "safe" mode`, `a "solution" nobody asked for`,
  `the "secret sauce" behind the model`. Delete the quotes and commit to the
  word, or replace the word with an accurate one.
- `so-called` plus quotes: doubly hedged. Say whether the term is standard or say
  what is wrong with it.
- Quoting a term on first mention when nothing is being defined: usually just
  delete the quotes. If you are defining the term, italics read better.
- Legitimate uses: quoting a source, showing an exact string the reader types or
  sees returned, defining a term on first use, and naming a titled section in a
  cross-reference. For literal values, commands, filenames, and parameters, code
  formatting beats quotes. For interface labels, follow house style; bold is
  the common convention.

Parentheses around ordinary prose are the third punctuation tell. Machine text
hedges by demoting half a thought into an aside instead of committing it to the
sentence.

- A full clause in parentheses: `The service retries three times (this is
  configurable).` Promote it to its own sentence.
- A relative clause in parentheses: `opens at 40 psi (which is the factory
  default)`. Fold it in or split it out.
- A qualifier in parentheses: `30 seconds (or longer for slow links)`. Drop the
  parentheses and keep the words.
- Parentheses at the end of a sentence carrying an afterthought: usually the
  afterthought is either important, in which case write it properly, or filler,
  in which case delete it.
- Nested parentheses: always rewrite.
- Legitimate uses: abbreviation definitions and spelled-out terms, part and model
  numbers, units and tolerances, cross-references and citations, math and
  equation terms, list markers, and the optional plural marker `bolt(s)`.

## 2. Buzzwords (plain-word swaps)

Say the plain word. In technical writing the plain word is almost always clearer
and more precise.

| Buzzword | Plain version |
|---|---|
| leverage / utilize | use |
| facilitate | help |
| robust | reliable, tested, stable (pick the real one) |
| seamless / seamlessly | (drop it, or say how it is smooth) |
| cutting-edge / state-of-the-art | (drop it, or name the technology) |
| game-changer / game-changing | (say what it actually changes) |
| best-in-class / world-class | (drop it) |
| synergy | (name the concrete benefit) |
| holistic | (be specific about scope) |
| streamline | simplify |
| empower | let, enable |
| unlock | (say what it enables) |
| foster | encourage, support |
| delve / dive into | look at, cover |
| realm / landscape / space | area, field (or just name it) |
| tapestry | (drop it) |
| paradigm | model, approach |
| myriad | many |
| plethora | many, plenty |
| bespoke | custom |
| supercharge | speed up, improve |
| turnkey | ready-to-use |
| frictionless | (drop it, or say how) |
| impactful | (state the actual effect) |
| actionable | (usually deletable) |

## 3. Filler and throat-clearing

These phrases add words and no information. Delete them and keep the sentence
that follows.

- "It's important to note that ..."
- "It's worth mentioning that ..."
- "It should be noted that ..."
- "Needless to say ..."
- "At the end of the day ..."
- "In today's fast-paced world ..." / "In this day and age ..."
- "In the world of ..." / "When it comes to ..."
- "The fact of the matter is ..."
- "First and foremost ..." / "Last but not least ..."
- "As we all know ..."
- "That being said ..."
- Closing flourishes: "In conclusion ...", "In summary ...", "To sum up ...",
  "Ultimately, X represents ...", "This just goes to show ...", "... a journey
  worth taking."

## 4. Formulaic sentence constructions

Patterns a language model reaches for on autopilot. Rewrite into a plain
statement.

- Front-loaded (periodic) sentences: conditions and subordinate clauses piled at
  the start, so the main clause (the point) arrives only at the end and the
  reader cannot tell where the sentence is going until they finish it. Lead with
  the main clause instead; let the detail follow, and split the sentence if the
  trailing detail is heavy.
- "It's not just X, it's Y." / "It's not about X; it's about Y."
- "Not only ... but also ..."
- "From X to Y to Z, ..." (the sweeping tricolon opener)
- "Whether you're a X or a Y, ..."
- "X isn't just a Z, it's a way of life."
- "Think of it as ..." followed by a strained metaphor.
- "That's where X comes in."
- "But here's the thing: ..."
- "Let's dive in." / "Let's explore ..." / "Let's unpack ..."
- Rhetorical question then answer: "So what does this mean? It means ..."
- The rule of three everywhere: "fast, reliable, and scalable." Real writing
  does not list in threes on every line. Vary the count; sometimes one precise
  item beats three vague ones.

## 5. Structural tells

- Every section opens with a general preamble before the actual content. Cut the
  preamble; start on the content.
- Every section closes with a summary sentence that restates what was just said
  and gestures at significance. Cut it.
- Uniform paragraph length, uniform sentence length. Vary both.
- Bulleted lists where every item is a full grammatical sentence of the same
  shape, often starting with a bolded two-word label plus a colon. Fine in
  moderation; a tell when every list in the document looks identical.
- Heavy signposting: "Furthermore," "Moreover," "Additionally," "Notably" at the
  head of sentence after sentence. Keep a transition only where the logic
  actually turns.

## 6. Hedging and vague quantifiers

Machine text hedges and gestures at quantity instead of stating it.

- Vague quantifiers: "various," "numerous," "several," "a range of," "a variety
  of," "a number of." Give the real count or the real items when you know them.
- Hedges: "arguably," "generally," "in many cases," "to some extent," "it could
  be argued that." Keep a hedge only when the uncertainty is real and relevant.
- Empty intensifiers: "very," "really," "quite," "extremely," "incredibly."
  Usually the sentence is stronger without them.
- Nominalizations that hide a verb: "the utilization of," "the implementation
  of," "the optimization of." Prefer the verb: "using," "implementing,"
  "optimizing."

---

## The underlying goal

None of these are sins on their own. A single em dash or one "leverage" would not
give a document away. The tell is the accumulation: the same moves, over and
over, with no human variation. Your job is to make the writing read like a person
who knows the subject wrote it with care. Specific, direct, varied in rhythm, and
free of the filler that pads machine output. When a rule here would make the
prose worse or less clear, ignore the rule and keep the prose clear.
