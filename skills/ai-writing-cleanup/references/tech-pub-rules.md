# Technical publication rules: detailed reference

Deeper treatment of Part 2 in SKILL.md. Read a section when a case in the main
skill is not clear-cut, or when you need the longer conversion tables.

## Table of contents

1. Active and passive voice
2. Hidden verbs (nominalizations)
3. Noun stacks
4. Pronouns and referents
5. Tense conventions
6. Terminology consistency
7. Abbreviations and acronyms
8. Chunking and information design
9. Coordinate and cumulative adjectives
10. Quotation marks
11. Parentheses
12. Plain word substitutions

---

## 1. Active and passive voice

Active voice puts the actor first: subject, verb, object. "The loader reads the
file." Passive reverses it and makes the actor optional: "The file is read by the
loader," or worse, "The file is read."

The cost of passive in technical documentation is the dropped actor. A procedure
that says "the circuit breaker must be opened" leaves a technician wondering
whether they open it, another team opens it, or the system opens it
automatically. Ambiguity in a procedure is a safety problem, not a style problem.

### Genre decides the default

Voice is the one rule in this skill that the document type can overrule, so
settle the type before editing any verbs.

| Document | Default voice |
|---|---|
| Procedures, work instructions, manuals | Active, imperative for every step |
| Specs, READMEs, release notes, runbooks | Active |
| Reports and proposals | Active |
| Journal paper: Methods, most of Results | Passive, by the field's convention |
| Journal paper: Introduction, Discussion, Conclusions | Active |

Academic engineering and science write Methods in the passive. "The specimens
were annealed at 800 C for 2 h, then quenched in water." The actor is the
authors, the reader knows it, and the sentence belongs to the specimens. That is
not a defect to fix, and several journals will send back a Methods section
rewritten into the first person. Leave it.

The same paper turns active where the authors make their own claims. An
Introduction saying "This paper presents a coating that resists spalling" and a
Discussion saying "We attribute the loss to thermal cycling" are both correct.
Edit toward active in those sections, and leave Methods alone.

Three things stay defects in any genre, a journal paper included:

1. Passive that hides an actor the reader has to act on.
2. Passive stacked deep enough that the sentence loses its subject.
3. Expletive passive such as "It was determined that" or "It was observed that",
   which is a nominalization wearing a passive coat. Section 2 covers those.

When the document type is not obvious, ask. A lab report and a work instruction
want opposite answers, and guessing wrong damages the document either way.

### How to spot it

Look for a form of "to be" (is, are, was, were, be, been, being) or "get"
followed by a past participle: "is configured," "was replaced," "must be
verified," "gets triggered." If you can append "by the ..." and the sentence still
works, it is passive.

### How to convert it

This applies where active is the default. In a journal Methods section, skip it.

Find the real actor and make it the subject. If the actor is missing entirely,
recover it from context. If the sentence is an instruction, use the imperative,
which is the most direct form available.

| Passive | Active |
|---|---|
| The file is read by the loader. | The loader reads the file. |
| The bolts must be torqued to 12 Nm. | Torque the bolts to 12 Nm. |
| Errors are logged to /var/log/app. | The service logs errors to /var/log/app. |
| The request was rejected by the gateway. | The gateway rejected the request. |
| Configuration is validated at startup. | The service validates configuration at startup. |
| It is required that the seal be inspected. | Inspect the seal. |

### When passive is correct

Keep passive in four situations. First, when the field writes that way, which
covers Methods and most of Results in an academic engineering or science paper.
Second, when the actor is genuinely unknown: "The connector was damaged in
shipping." Third, when the actor is irrelevant to the reader and naming it adds
noise: "The unit is manufactured in Ohio." Fourth, when the affected object is
the real topic of the sentence and the paragraph follows that object: "The filter
is replaced every 500 hours. It is then discarded."

Two tests, in order. Does the genre call for passive here? If yes, keep it. If
no, does the reader need to know who acts? If yes, use active.

---

## 2. Hidden verbs (nominalizations)

A nominalization turns a verb into a noun. The sentence then needs a weak helper
verb (perform, conduct, make, provide, carry out, give, take, effect, achieve) to
carry the grammar, and the real action sits inert in the middle.

### Giveaway endings

-tion, -sion, -ment, -ance, -ence, -ity, -al, -ure, and -ing used as a noun.

### Conversion table

| Buried | Freed |
|---|---|
| perform an inspection of | inspect |
| perform maintenance on | maintain |
| conduct an analysis of | analyze |
| conduct an evaluation of | evaluate |
| carry out a review of | review |
| make a determination | determine |
| make an adjustment to | adjust |
| make a recommendation | recommend |
| provide a description of | describe |
| provide assistance to | help |
| give consideration to | consider |
| give approval for | approve |
| take into account | account for |
| effect a reduction in | reduce |
| achieve compliance with | comply with |
| is indicative of | indicates |
| is reflective of | reflects |
| is in agreement with | agrees with |
| has the ability to | can |
| is able to | can |
| has a requirement for | requires |
| the installation of the pump | installing the pump |
| the verification of the seal | verifying the seal |
| the utilization of the tool | using the tool |
| for the purpose of testing | to test |
| in order to complete | to complete |
| it is necessary to verify | verify |
| it is possible to configure | you can configure |
| there is a need for calibration | calibrate it |

### The "the ___ of" pattern

"The <noun> of <thing>" is the most common hidden verb in specifications. "The
removal of the panel requires two technicians" becomes "Removing the panel
requires two technicians," or better, "Two technicians remove the panel."

### Worked example

Before: Verification of the seal integrity shall be performed by the technician
prior to the commencement of pressurization operations.

Three problems compound here: "verification" hides "verify," "be performed" is
passive, and "commencement of pressurization operations" is both a hidden verb
and a noun stack.

After: Before pressurizing the system, the technician verifies that the seal is
intact.

Word count drops from 17 to 12 and the actor becomes explicit.

---

## 3. Noun stacks

A noun stack (also called a noun cluster or noun string) is three or more nouns in
sequence, each modifying the next. English lets you do this, but the reader gets
no grammatical signal about which noun attaches to which, so they must resolve the
ambiguity from domain knowledge.

Two nouns are normal ("fuel pump"). Three is a warning sign. Four or more is
almost always a defect.

### How to unstack

The head noun is the last one in the string. Everything before it is a modifier.
To unstack, make the head noun the subject or object, then reattach the modifiers
with prepositions and verbs, working backward from the head.

Example: "system configuration parameter validation failure"

Head noun: failure. Working backward: failure of validation, validation of a
parameter, parameter of configuration, configuration of the system.

Result: "the system failed to validate a configuration parameter."

### More examples

| Stacked | Unstacked |
|---|---|
| aircraft fuel system pressure sensor calibration procedure | procedure for calibrating the pressure sensor in the fuel system |
| user account password reset request form | form for requesting a password reset |
| database connection pool exhaustion error | error raised when the database connection pool is exhausted |
| network interface configuration file syntax check | syntax check of the network interface configuration file |
| engine oil temperature warning indicator | engine oil temperature warning indicator (established term; leave it) |

### The established term exception

An accepted multi-word term is a name, not a stack. "Transport layer security,"
"fuel pump housing," "line replaceable unit," and "engine oil temperature
warning indicator" are what those things are called. Breaking a real term to
satisfy the noun stack rule creates a worse problem, because terminology
consistency (Section 6) outranks this rule.

The distinguishing question: would a subject matter expert recognize this exact
string as the name of a specific thing? If yes, keep it. If it is an ad hoc
description assembled by the writer, unstack it.

When a genuine term is itself long, keep the term intact and simplify the words
around it rather than the term itself.

---

## 4. Pronouns and referents

Every pronoun asks the reader to search backward. Technical documentation is read
in fragments, out of order, and under time pressure, so that search often fails.

### Vague demonstratives

The worst case is a sentence-initial "This," "That," "These," or "Those" followed
directly by a verb. The pronoun could point at the previous noun, the previous
clause, or the entire previous paragraph.

Before: The controller polls the sensor every 200ms and writes the reading to the
log. This can saturate the disk on high-frequency channels.

What saturates the disk: the polling, the writing, or both? Name it.

After: The controller polls the sensor every 200ms and writes the reading to the
log. The log writes can saturate the disk on high-frequency channels.

If you keep a demonstrative, attach it to a noun: "this valve," "these
conditions," "that reading." A bare demonstrative is the defect, not the word
itself.

### Ambiguous "it," "they," and "which"

When a sentence contains two candidate antecedents, "it" is guaranteed trouble.

Before: When the service connects to the proxy, it logs the handshake.

Which one logs it? Rewrite: "When the service connects to the proxy, the service
logs the handshake."

The same applies to a trailing "which," which often points at a whole clause:
"The pump ran dry, which damaged the seal" is acceptable in prose but better as
"Running dry damaged the pump seal."

### Expletive constructions

"It is" and "there is/are" at the start of a sentence are placeholders that push
the real subject to the back and often hide a passive or a hidden verb.

| Expletive | Direct |
|---|---|
| It is necessary to check the seal. | Check the seal. |
| It is recommended that you restart the service. | Restart the service. |
| There are three conditions that trigger a rollback. | Three conditions trigger a rollback. |
| There is a requirement for annual calibration. | Calibrate the unit annually. |

### First and second person

First person (we, our, us, I, my) does not belong in technical publications. The
document describes a system, not the authors' opinions. "We recommend closing the
valve" becomes "Close the valve" or "Closing the valve prevents backflow."

Second person (you, your) is a house style decision. Most software documentation
style guides accept and even prefer "you" in procedures. Many aerospace, defense,
and industrial technical publication standards bar it, using the imperative
instead. The imperative is shorter and unambiguous either way, so default to it:
"Check the seal" rather than "You should check the seal."

Follow whatever convention the document already uses. If the document mixes both,
standardize on the imperative and flag the change.

---

## 5. Tense conventions

Pick a convention and hold it. Drift makes a reader wonder whether a described
behavior changed between versions.

- **Present tense** for how a system behaves, always. "The valve opens at 40
  psi." "The parser rejects malformed headers."
- **Imperative** for instructions. "Open the valve." "Restart the service."
- **Past tense** only for events that actually happened. "The outage began at
  02:14." "Revision C removed the bracket."
- **Future tense** almost never. "The system will send a confirmation" describes a
  promise; "the system sends a confirmation" describes how it works. Reserve
  "will" for genuinely future events, such as a planned deprecation.

Conditional statements stay in present tense on both sides: "If the token
expires, the gateway rejects the request." Not "if the token expires, the gateway
will reject the request."

---

## 6. Terminology consistency

One thing gets one name, everywhere in the document.

This rule is where technical writing diverges hardest from general prose. Essay
writers vary word choice to avoid monotony, a habit sometimes called elegant
variation. In technical documentation it is a defect, because a reader who sees
"relief valve" in Section 2 and "pressure release mechanism" in Section 5
reasonably assumes those are two different parts.

The same applies to actions and states: pick "restart" or "reboot," "abort" or
"cancel," "error" or "fault," and stay with it.

When you find inconsistent naming during a cleanup:

1. Identify every variant used for the thing.
2. Choose the term the document formally defines, or failing that, the one used
   most often and most precisely.
3. Standardize on it everywhere.
4. List the change in your summary so the author can confirm the choice, since
   only they know for certain whether two names really meant one thing.

Never merge two terms because they look similar without checking. If the document
distinguishes a "fault" from an "error" deliberately, collapsing them destroys
meaning. When you are not sure, leave both and flag the inconsistency instead of
resolving it.

Rhythm and sentence structure should vary. Terminology should not.

---

## 7. Abbreviations and acronyms

An abbreviation is a trade: the reader spends effort learning a token now to save
effort later. The trade only pays off with repetition.

### The single-use rule

Never define an abbreviation you use once. "The Environmental Control System
(ECS) regulates cabin temperature," with no later mention of ECS, costs the reader
a definition and returns nothing. Delete the parenthetical and let the spelled-out
term stand alone.

### When to introduce one

Introduce an abbreviation when either condition holds:

- The term appears at least three or four more times after the definition.
- The abbreviation is more familiar to the audience than the expansion. Most
  readers know USB, HTTP, PDF, and RAM better than the words behind them.
  Expanding these can hurt readability rather than help it.

### Mechanics

Define on first use in the body text, spelled-out term first, abbreviation in
parentheses: "line replaceable unit (LRU)." Use the abbreviation consistently
afterward; do not alternate.

Spell out terms in headings, titles, table captions, and figure captions. Readers
land on those without having read the body, and a heading full of unfamiliar
acronyms is unreadable.

Redefine on first use in each major standalone section of a long document, since
readers rarely start at page one.

Never invent an abbreviation for writing convenience. If the field does not
already use it, the reader has to learn a token that exists nowhere else.

Use one expansion per abbreviation throughout. If "CM" means both "configuration
management" and "corrective maintenance," spell out at least one of them
everywhere.

Avoid stacking abbreviations into a single sentence. Three unfamiliar acronyms in
one sentence forces the reader to decode instead of read.

---

## 8. Chunking and information design

Chunking often improves readability more than any sentence-level edit, because it
exposes structure the prose was hiding.

### Conversions worth making

- Sequential prose becomes numbered steps, one action per step.
- A paragraph comparing two or more options becomes a table.
- A run of parallel conditions or requirements becomes a bulleted list.
- A long section gets subheadings a reader can scan.
- A paragraph carrying two topics becomes two paragraphs.

### Targets

Keep paragraphs to one topic and roughly three to five sentences. Keep procedures
to one instruction per step. A step reading "Remove the cover, disconnect the
harness, and extract the module" is three steps in disguise, and a technician
interrupted midway loses their place with no way to mark progress.

Put the condition before the action in a step, so the reader knows whether the
step applies before they perform it: "If the indicator is red, replace the
filter," not "Replace the filter if the indicator is red."

Front-load warnings. Safety information belongs before the step it applies to,
never after.

### Worked example

Before: To replace the filter, first shut off the supply valve, then wait for
pressure to drop below 5 psi, and after that remove the four retaining bolts
before lifting out the filter housing.

After:

To replace the filter:

1. Shut off the supply valve.
2. Wait for pressure to drop below 5 psi.
3. Remove the four retaining bolts.
4. Lift out the filter housing.

---

## 9. Coordinate and cumulative adjectives

Whether a comma belongs between two adjectives is a structural question with a
reliable test, not a matter of taste.

### Coordinate adjectives: use a comma

Coordinate adjectives each modify the noun independently. Two tests confirm it:

1. Insert "and" between them. Does it still read correctly?
2. Reverse their order. Does it still read correctly?

If both tests pass, the adjectives are coordinate and take a comma.

"A small, red valve" passes: "a small and red valve" works, and "a red, small
valve" works. Comma required.

### Cumulative adjectives: no comma

Cumulative adjectives build on one another. The adjective nearest the noun forms a
unit with it, and the earlier adjective modifies that whole unit.

"A red hydraulic valve" fails both tests: "a red and hydraulic valve" is wrong,
and "a hydraulic red valve" is wrong. No comma, because "hydraulic valve" is the
unit and "red" describes that unit.

### More examples

| Correct | Type |
|---|---|
| a small, red valve | coordinate |
| a durable, lightweight housing | coordinate |
| a red hydraulic valve | cumulative |
| a durable stainless steel fitting | cumulative ("stainless steel" is a unit) |
| three large steel brackets | cumulative |
| a clear, concise procedure | coordinate |
| the old aluminum bracket | cumulative |

### The rule that has no exceptions

Never put a comma between the final adjective and the noun. "A small, red, valve"
is always wrong.

### Common error pattern

Writers often place the comma by rhythm rather than structure, which yields "a
small red, hydraulic valve." Apply the tests: "small" and "red" are coordinate, so
the comma belongs between them, and "hydraulic valve" is a unit, so no comma
precedes it. Correct: "a small, red hydraulic valve."

---

## 10. Quotation marks

Quotation marks carry a specific meaning: the enclosed text is somebody else's
words, or a literal string, or a term under definition. Used for anything else,
they tell the reader the writer is distancing themselves from the word.

### Delete these

| Wrong | Why | Fix |
|---|---|---|
| enters a "safe" mode | hedge; is it safe or not? | enters a safe mode, or say what it does |
| the "secret sauce" of the design | evasive; hides the actual mechanism | name the mechanism |
| a "solution" that shipped late | sarcasm the writer may not intend | say what was wrong with it |
| Do not remove the "cover" | quotes as emphasis reverse the meaning | Do not remove the **cover** |
| the so-called "best practice" | doubly hedged | state whether it is standard, or why it is not |
| a "state-of-the-art" sensor | quoted buzzword is still a buzzword | give the specification |

Quoting a word for emphasis is the most damaging version, because the convention
already means the opposite. A maintenance note reading `Torque to "12 Nm"` invites
the reader to wonder what the real figure is.

### Keep these

Quotation marks are correct for quoted speech or text from an identified source,
the exact string a reader types or sees returned, a term being defined on first
use, and the title of a section or document in a cross-reference.

### Preferred formatting in technical documents

| Content | Convention |
|---|---|
| command, filename, path, parameter, value, returned string | code formatting |
| interface label (button, field, menu, tab) | bold, per most house styles |
| section or document title in a cross-reference | quotes or italics, per house style |
| term being defined on first use | italics |
| quoted text from a source | quotation marks |

Code formatting beats quotes for literal values for two reasons. It survives copy
and paste, and it removes any chance the reader reads the quotes as irony.

### Punctuation inside or outside

US convention places periods and commas inside the closing quotation mark. That
convention breaks for literal strings, because a period inside the quotes looks
like part of the string. When the quoted text is a value the reader must type or
match, put the punctuation outside, or better, use code formatting and sidestep
the question. `Set the level to "verbose".` is unambiguous; `Set the level to
"verbose."` suggests the trailing period is part of the value.

### Consistency

Whatever the house style chooses, apply it to every instance in the document. A
document that bolds some button labels and quotes others reads as unedited.

---

## 11. Parentheses

Parentheses signal that the enclosed text is outside the sentence. In technical
documents readers act on that signal and skip what is bracketed. Anything a
reader can skip without consequence should not have been written; anything with
consequence should not be bracketed.

### Fold it in or split it out

| Wrong | Fix | Method |
|---|---|---|
| The service retries three times (this is configurable). | The service retries three times. Change the retry count in the settings file. | full clause becomes its own sentence |
| opens at 40 psi (which is the factory default) | opens at 40 psi, the factory default | relative clause folds in as an appositive |
| Set the timeout to 30 seconds (or longer for slow links). | Set the timeout to 30 seconds, or longer for slow links. | qualifier keeps the words, drops the brackets |
| Install the filter (a new one, not the old one). | Install a new filter. | aside was doing the sentence's job |
| The alarm sounds (see below). | The alarm sounds. Section 4.2 describes the response. | vague pointer becomes a real cross-reference |

The test: read the sentence without the bracketed text. If it now says something
incomplete or wrong, the material belongs in the sentence. If it reads fine, ask
whether the bracketed text earns its space at all.

### Keep the parentheses

| Content | Example |
|---|---|
| abbreviation definition | Environmental Control System (ECS) |
| spelled-out term after the short form | ECS (Environmental Control System) |
| part, model, or drawing number | the pressure sensor (P/N 4471-A) |
| unit conversion or tolerance | 12 Nm (106 in-lb), 0.5 mm (+/- 0.05) |
| cross-reference or citation | See the wiring diagram (Figure 4). |
| math and equation terms | (a + b) / c |
| list markers | (a), (b), (1), (2) |
| optional plural | Remove the retaining bolt(s). |

### Two hard limits

Nested parentheses are always a defect. A reader tracking two levels of aside has
lost the sentence. Rewrite.

A parenthetical that runs longer than the clause containing it is a defect for
the same reason. Promote it to its own sentence.

---

## 12. Plain word substitutions

Prefer the shortest everyday word that stays precise. This never means replacing a
technical term with a vague one.

| Inflated | Plain |
|---|---|
| utilize, leverage | use |
| facilitate | help |
| prior to | before |
| subsequent to, following | after |
| in the event that | if |
| in order to | to |
| for the purpose of | to, for |
| at this point in time | now |
| a large number of | many |
| the majority of | most |
| in close proximity to | near |
| with regard to, regarding | about |
| in the vicinity of | near |
| terminate | end, stop |
| initiate, commence | start, begin |
| endeavor | try |
| ascertain | find out, determine |
| demonstrate | show |
| sufficient | enough |
| additional | more, extra |
| approximately | about |
| component | part |
| assist | help |
| obtain | get |
| require | need |
| indicate | show |
| modify | change |
| construct | build |
| purchase | buy |

Apply judgment on the last several. Some are standard in a given field, and
"component," "modify," and "indicate" are often the accepted terms in engineering
documentation. Substituting a plain word for a term of art is a downgrade. The
target is the shortest precise word, not the shortest word.
