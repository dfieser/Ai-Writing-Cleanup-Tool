# AI Writing Cleanup: complete ruleset

Version 1.5.0.

One file holding every rule from the ai-writing-cleanup skill. It exists for an
agent that cannot load a skill directory and needs the whole ruleset in a single
read.

**How to use this file.** Read all of it, then edit the target document against
it. Rules 1 through 8 remove the texture of machine writing. Rules 9 through 18
apply technical-writing discipline. The reference sections at the end hold the
detail behind each rule.

**The rule that outranks every other one.** Preserve technical truth. Every
number, name, version, command, API, file path, code snippet, config value, and
part number stays exactly as the author meant it. If a rewrite for style would
change a technical meaning, keep the meaning and find other wording. If you
cannot tell whether a change preserves a fact, leave the text alone and say so
in the change list. Never touch text inside code blocks, command examples,
config samples, or literal output.

**Verify your work.** The repository ships a checker that counts what judgment
cannot. Run it before and after your edit:

```bash
python3 skills/ai-writing-cleanup/scripts/check_writing.py DRAFT --json
python3 skills/ai-writing-cleanup/scripts/check_writing.py DRAFT --fail-on mechanics
```

**Output format.** Return the rewrite, then a short change list grouped by issue
type. Say which items you left alone to protect a technical meaning. That line is
usually the most useful one.

This file is generated. Edit the sources under `skills/ai-writing-cleanup/` and
run `python3 tools/build_bundle.py`.



---

# Part A: the skill

Source: `SKILL.md`

## AI Writing Cleanup

### What this is for

Machine-generated prose has a recognizable texture. Every sentence runs the same
length, the vocabulary stays safe and predictable, lists come in threes, and each
section ends with a small summarizing flourish. Separately, weak technical writing
has its own failure modes: passive constructions, verbs buried inside nouns, long
strings of nouns jammed together, pronouns with no clear referent, and
abbreviations invented for no reason.

This skill fixes both. The goal is prose a working technical writer would sign:
short, direct, active, specific, and easy for a reader to follow on the first
pass. You are editing style and structure, never facts.

### The one rule you cannot break: preserve technical truth

Do not change what the document says. Keep every number, name, version, command,
API, file path, code snippet, config value, part number, defined term, and causal
claim exactly as the author meant it. If a rewrite for style would alter a
technical meaning, keep the meaning and find another wording. When a sentence is
ambiguous and you cannot tell whether a change preserves the fact, leave it and
note it in the fix list rather than guessing. A cleaner sentence that says the
wrong thing is a failure, not an improvement.

Never touch text inside code blocks, command examples, config samples, or literal
output. Those are data, not prose.

### Scope is settled before the edit starts

Every rule in Part 1 and Part 2 is in scope. Apply all of them. Do not open a
debate with the user about whether a defect counts as machine writing, and do not
skip a rule because the pattern also turns up in human prose. Four rules attract
that argument, so the grounds are stated here.

**Sentence length and uniformity, rule 4.** The length distribution is the most
measurable signature of generated text. A model samples near the center of its
distribution, so lengths cluster and the rhythm flattens. The checker reports a
coefficient of variation because that number is the evidence.

**Front-loaded sentences, rule 5.** Generated prose stacks conditions and
qualifiers ahead of the subject, so the main clause lands last. The habit is
common in model output, and it slows every reader.

**Passive voice, rule 9.** Agentless passive is heavy in the formal writing
models train on, and passive lets a sentence avoid naming an actor that the model
has no stake in naming. In a procedure it is a safety defect on its own terms,
because nobody is told who acts. Rule 9 is also the one rule a genre can
overrule. A journal Methods section is passive by convention and stays that way,
which is a call made once from the document type rather than a defect argued
sentence by sentence.

**Noun stacks and hidden verbs, rules 10 and 11.** Models compress clauses into
noun phrases. That produces long premodifier chains and verbs buried inside
nouns, which is why both patterns cluster in generated technical text.

These four are weaker fingerprints than an em dash or a scare quote, and each one
also appears in human writing. None of that changes the edit. Whether a sentence
came from a model cannot be recovered from the text, the fix is identical either
way, and the goal is prose that reads well and reads human. If the user asks
which patterns are the strongest evidence of machine authorship, answer
accurately, then apply every rule anyway. Never tell a user that a flagged item
falls outside this skill, and never drop a rule to win a point about taxonomy.

### Workflow

1. **Read the whole document first.** Understand what it is, who reads it, which
   field it belongs to, and what each section does. Style edits made sentence by sentence without the
   whole picture tend to flatten a document's structure.

2. **Run the checker.** Use `scripts/check_writing.py` on the source to get a
   fast, objective map of the mechanical problems. It catches what the eye skips.
   See "Using the checker" below.

3. **Rewrite for clarity.** Apply Part 1 and Part 2 below. You have latitude to
   restructure sentences and reorder within a paragraph, as long as meaning holds.
   Do not merely find and replace; sounding human is a whole-sentence judgment.

4. **Run the checker again on your rewrite.** Confirm zero em dashes and that the
   other counts dropped. If em dashes remain, you are not done. This second pass
   is not optional, because models reintroduce these patterns without noticing.

5. **Return two things:** the clean rewrite, then a short **What changed** list
   grouped by issue type.

---

## Part 1: Remove the machine texture

These describe symptoms of machine writing and why each hurts a technical
document. Treat them as a trained editor's instincts, not a checklist to satisfy
mechanically. When a rule and plain clarity conflict, clarity wins.

#### 1. No em dashes. None.

The em dash (—) is the most recognizable machine-writing tell, and the finished
document should contain zero. Remove every one. Depending on the job the dash was
doing, use a period for two independent thoughts, a comma for a light aside, or a
colon when the second half explains the first. Often the cleanest fix is two
sentences. Do not swap an em dash for parentheses, which rule 3 restricts just as
tightly.

This covers em dashes in disguise: a spaced en dash used as a break ( – ) and a
double hyphen (--) standing in for one. Real hyphens in compounds ("read-only,"
"end-to-end") are correct and stay.

Input: The API is fast — it returns in under 50ms — but it has no caching.
Output: The API is fast. It returns in under 50ms, but it has no caching.

Input: There is one hard requirement — every request must be authenticated.
Output: There is one hard requirement: every request must be authenticated.

#### 2. Use quotation marks only for real quotations.

Quotation marks wrapped around ordinary words are a strong machine tell. The
quotes signal that the writer does not fully mean the word, or wants to stress
it, or is holding it at arm's length. A technical reader cannot tell which, so
the sentence turns evasive. Is the mode actually safe, or only "safe"?

Delete scare quotes. If the word is right, write it bare. If the word is wrong,
find the right word.

Input: The scheduler enters a "safe" mode when the queue fills up.
Output: The scheduler stops accepting jobs when the queue fills up.

Input: This is the "secret sauce" behind the ranking model.
Output: The ranking model weights recency three times as heavily as relevance.

Never use quotes for emphasis. They read as sarcasm and reverse the meaning.
A sign that says Do not remove the "cover" suggests the cover is not really a
cover. Use bold, or restructure the sentence so the important word lands last.

Cut "so-called" along with the quotes it drags in. Either the term is standard,
in which case use it, or it is wrong, in which case say why in plain words.

Quotation marks are correct for four jobs: quoting speech or text from a named
source, showing the exact string a reader types or sees returned, defining a term
on first use, and naming a titled section or document in a cross-reference.

For literal values, commands, filenames, parameters, and returned strings, code
formatting beats quotes. It survives copy and paste, and no reader mistakes it
for irony. For interface labels, follow the house style, which is usually bold.
Pick one convention and hold it through the document.

Input: Type "admin" in the "Username" field, then click "Save".
Output: Type `admin` in the **Username** field, then click **Save**.

#### 3. Use parentheses only where they are required.

The default is no parentheses. Use them only when no other construction works,
and rewrite whenever a rewrite is possible.

Parentheses tell the reader the material is optional, so a reader scanning a
procedure skips it. Anything a reader can skip and still do the job correctly did
not need writing. Anything they cannot skip does not belong in parentheses.

Before you keep any parenthesis, try three rewrites in this order:

1. Fold the material into the sentence, usually as a comma clause or an
   appositive.
2. Promote it to its own sentence, if it carries a subject and verb.
3. Delete it, if the sentence loses nothing without it.

Keep the brackets only when all three rewrites read worse, and be ready to say
which rewrite you rejected and why. "It is conventional" is not a reason. Neither
is "it is short."

Input: The service retries three times (this is configurable in the settings
file).
Output: The service retries three times. Change the retry count in the settings
file.

Input: The valve opens at 40 psi (which is the factory default) and closes at
20 psi.
Output: The valve opens at 40 psi and closes at 20 psi. Both values are factory
defaults.

Input: Set the timeout to 30 seconds (or longer for slow links).
Output: Set the timeout to 30 seconds, or longer for slow links.

Four uses are required, because the parentheses are part of a notation rather
than a way of demoting prose. Leave these alone:

- Math and equation terms: `(a + b) / c`.
- List and label markers the document already uses: (a), (b), (1), (2).
- A citation format the house style mandates: (Smith et al., 2019).
- A nomenclature definition, in either order. The parentheses are how a field
  binds a term to its short form, and no rewrite does the job as cleanly.

The nomenclature case is the one place where a bracketed aside carries real
information, so it is exempt without argument. Both orders are correct, and the
spelled-out term does not need to be capitalized:

Correct and unchanged: High entropy alloys (HEA) resist softening at high
temperature. The two-temperature model (TTM) treats electrons and the lattice
separately. HEA (high entropy alloy) powders were milled for 4 h.

The exemption covers the definition itself, not the decision to abbreviate.
Rule 14 still governs whether the abbreviation earns its place at all. Established
field nomenclature usually does, because a reader who knows the field expects the
short form and a reader who does not needs the binding. An abbreviation you
invented and then used twice does not, and deleting it also deletes its brackets.

One further use is allowed when the rewrite reads worse: a unit conversion or
tolerance sitting immediately after its value. "Torque the bolts to 12 Nm
(106 in-lb)" beats "Torque the bolts to 12 Nm, or 106 in-lb," because a technician
reads the value, not the sentence. This is the only routine exception, and it does
not extend to anything else that happens to be short.

Everything else gets rewritten, including cases a style guide would tolerate:

Input: Replace the pressure sensor (P/N 4471-A).
Output: Replace pressure sensor P/N 4471-A.

Input: Remove the retaining bolt(s).
Output: Remove the retaining bolts.
Write the plural. If the count matters, say it: "Remove the two retaining bolts."
If it genuinely varies, say that: "Remove the retaining bolt or bolts, depending
on the variant."

Input: The link is down (again).
Output: [deleted]

Figure, table, section, and equation callouts get the same treatment. Work the
reference into the sentence instead of bracketing it at the end. A bracketed
callout tells the reader to look somewhere else after the sentence is over, and
they have already stopped reading. Make the figure the subject, or name it in the
clause that needs it.

Input: The XRD pattern shows a single FCC phase (Figure 3).
Output: Figure 3 shows a single FCC phase in the XRD pattern.

Input: See the wiring diagram (Figure 4).
Output: See Figure 4 for the wiring diagram.

Input: The alarm sounds (see Section 4.2).
Output: Section 4.2 describes the response when the alarm sounds.

Input: Ablation depth scales with pulse energy (Fig. 5b) up to 40 uJ.
Output: Up to 40 uJ, ablation depth scales with pulse energy, as Figure 5b shows.

Rewrite it even when the reference is the whole point of the sentence, because
that is the easiest case: "Figure 6 compares the two coatings" needs no brackets
at all. Keep the bracketed form only where a house style mandates it, and say so
in the change list. Rule 17 decides whether the reference belongs at all.

Two hard defects, regardless of content: nested parentheses, and a parenthetical
longer than the clause holding it. Rewrite the sentence in both cases.

#### 4. Keep sentences short. Vary their length.

Two things are true at once, and they are not in conflict.

Short sentences win in technical writing. One idea per sentence. A reader
tracking a procedure or a failure mode should not have to hold three clauses in
memory. Aim for an average near 15 to 20 words. Treat anything past 25 words as a
candidate for splitting, and anything past 30 as a defect.

Uniform sentences read as machine output. Machine prose defaults to medium-long
sentences of near-identical length stitched together with "and," "but," "which,"
and semicolons. Read three in a row and the rhythm turns mechanical.

So: shorten overall, and vary within that shorter band. A five-word sentence lands
a point. A twenty-word sentence carries a chain of reasoning. Both belong. What
does not belong is ten sentences that all run eighteen words.

The usual offenders are the compound sentence that should be two sentences, and
the reflexive list of three ("fast, reliable, and easy to maintain"). Split
compounds when each half stands alone. Break the rule-of-three habit, because
sometimes one precise item beats three vague ones and sometimes the list belongs
as real bullet points.

Input: The service handles authentication, and it also manages sessions, and it
logs every request, which makes it a central point of failure.
Output: The service handles authentication, sessions, and request logging. That
makes it a central point of failure.

#### 5. Get to the point early. Do not front-load the sentence.

A sentence that stacks detail and conditions at the front makes the reader wait.
The main clause, the actual point, arrives only at the end. The reader must hold
every qualifier in suspension and cannot tell where the sentence is going until
the last word.

English reads most easily when the main clause comes first and supporting detail
follows. Lead with the subject and verb. Name the thing, say what it does, then
add conditions, reasons, and exceptions. The reader learns the direction in the
first few words and takes the rest as elaboration.

Short scene-setting openers are fine ("In production, ...", "On startup, ..."),
because they reach the subject in two or three words. The problem is the long
wind-up: a chain of clauses the reader crosses before reaching the subject. When
you find one, move the main clause to the front and split off the trailing detail.

Input: Because the authentication token had expired after its 60-minute window
and the retry logic had already used all three attempts, the request failed.
Output: The request failed because its authentication token had expired. The
token lasts 60 minutes, and the retry logic had already used its three attempts.

Input: In the event that the primary database is unavailable and the failover
replica has not yet caught up to the latest committed transaction, writes are
rejected.
Output: Writes are rejected when the primary database is down and the failover
replica has not caught up to the latest committed transaction.

#### 6. Raise specificity. Kill predictable phrasing.

Machine prose reaches for the most probable next word, which makes it generic and
low-signal. The fix in technical writing is not fancier vocabulary. It is
concreteness. Name the actual thing, the actual number, the actual mechanism.
Specific and plain beats generic and inflated, and it reads as less machine-made
because it is less predictable.

Replace vague quantifiers ("various," "numerous," "a range of," "several") with
the real count or the real items. Replace abstract claims ("improves performance")
with the concrete effect ("cuts p99 latency from 800ms to 120ms").

Input: We leverage a range of robust techniques to significantly improve system
performance across the board.
Output: Caching query results and batching writes cut average response time from
400ms to 90ms.

#### 7. Cut buzzwords and flowery language. Use simple words.

Prefer the shortest everyday word that is precise. Technical readers are not
impressed by elevated vocabulary; they are slowed by it. "Use" beats "utilize."
"Help" beats "facilitate." "Before" beats "prior to." "About" beats "regarding."

Cut the buzzword vocabulary: leverage, utilize, facilitate, robust, seamless,
cutting-edge, state-of-the-art, best-in-class, synergy, holistic, streamline,
empower, unlock, foster, delve, dive into, realm, landscape, tapestry, paradigm,
and journey.

Delete throat-clearing outright: "it's important to note that," "it's worth
mentioning," "needless to say," "at the end of the day," "in today's fast-paced
world," "when it comes to." These add length and no information.

Keep necessary technical terms. Simplifying vocabulary never means replacing a
precise term with a vague one. "Torque the fastener to 12 Nm" does not become
"tighten the thing." The full catalog is in `references/ai-tells.md`.

Input: It's important to note that our robust, cutting-edge platform empowers
teams to seamlessly streamline their workflows.
Output: The platform automates three manual steps in the release process: tagging,
changelog generation, and deployment.

#### 8. Every sentence earns its place. Cut the flourish.

Machine writing pads. It opens sections with a general preamble before reaching
the point, and closes them with a summarizing sentence that broadens into
significance ("This demonstrates the importance of...", "In conclusion..."). Cut
both. Start each section on its actual content and stop when the content stops.

Delete tacked-on asides and fun facts that do not serve the topic. If a sentence
would not be missed, it should not be there. Signposts like "Furthermore,"
"Moreover," and "Additionally" at the head of a sentence are usually deletable.
Keep a transition only where the logic actually turns.

Input: In conclusion, proper error handling is an essential cornerstone of any
robust application, and mastering it is a journey well worth taking.
Output: [deleted]

---

## Part 2: Technical writing discipline

Part 1 makes the prose sound human. Part 2 makes it work as technical
documentation. The split is a way to organize the rules, not a ranking of which
ones matter. Everything in Part 2 is part of the cleanup. These rules come from technical publication practice, where a
reader is often following a procedure under time pressure and any ambiguity costs
real money. `references/tech-pub-rules.md` holds the detailed treatment, longer
conversion tables, and edge cases; read it when a case here is not clear-cut.

#### 9. Match voice to the genre. Active by default, passive where the field writes that way.

Identify what the document is before you touch a single verb. Voice is the one
rule here that a genre can overrule, and getting it backwards damages the
document in either direction.

**Default to active.** Active names the actor, so the reader knows who does what,
and it runs shorter. Use it in manuals, procedures, work instructions, specs,
READMEs, release notes, reports, and proposals. In a procedure a dropped actor is
a safety defect rather than a style problem, because "the valve must be closed"
never says who closes it. Write steps as imperatives.

**Keep passive in academic engineering and science papers.** A journal Methods
section is written in the passive by convention, and much of Results with it. Take
"The specimens were annealed at 800 C for 2 h." The actor is the authors, every
reader already knows that, and the sentence belongs to the specimens rather than
to the people handling them. Rewriting it as "We annealed the specimens" fights
the field, and some journals send it back. Leave it.

The convention is sectional, not blanket. Introductions, Discussions, and
Conclusions carry the authors' own claims, and those read active in most
engineering journals. "This paper presents" and "We show that the coating fails
by spalling" are correct there. Edit toward active in those sections.

**What stays a defect in any genre.** Passive that hides an actor the reader has
to act on. Passive stacked deep enough that the sentence loses its subject.
Expletive passive such as "It was determined that", which is a hidden verb from
rule 10 wearing a passive coat. Fix those anywhere they appear, a journal paper
included.

If the document type is not obvious, ask rather than guess. A lab report and a
work instruction want opposite answers.

Input: The configuration file is read by the loader at startup, and any invalid
fields are logged.
Output: The loader reads the configuration file at startup and logs any invalid
fields.

Input: The bolts must be torqued to 12 Nm.
Output: Torque the bolts to 12 Nm.

Input, from a journal Methods section: The samples were sectioned, mounted in
epoxy, and polished to 1 um.
Output: unchanged. This is the field's convention and the samples are the subject.

Input, from a journal Discussion: It was determined by the authors that the
coating failed by spalling.
Output: The coating failed by spalling.

#### 10. Free the hidden verbs.

A hidden verb, or nominalization, is an action turned into a noun that needs
a weak helper verb to function: "perform an inspection of" instead of "inspect."
The real action disappears into a noun, the sentence gets longer, and the reader
works harder for the same meaning.

Find the action in the sentence and make it the verb.

| Buried | Freed |
|---|---|
| perform an inspection of | inspect |
| conduct an analysis of | analyze |
| provide a description of | describe |
| make a determination | determine |
| give consideration to | consider |
| is indicative of | indicates |
| effect a reduction in | reduce |
| the installation of the pump | installing the pump |
| has the ability to | can |
| it is necessary to verify | verify |

Watch for the giveaway endings: -tion, -sion, -ment, -ance, -ence, -ity, and -ing
sitting after "perform," "conduct," "make," "provide," "carry out," "give," or
"take."

Input: Verification of the seal integrity shall be performed by the technician
prior to the commencement of pressurization.
Output: Before pressurizing the system, the technician verifies that the seal is
intact.

#### 11. Break up noun stacks.

A noun stack is three or more nouns in a row modifying each other: "system
configuration parameter validation failure." The reader cannot tell which noun
modifies which, and has to re-read to find the head noun. Two nouns are usually
fine. Three is a warning. Four or more is almost always broken.

Unstack by adding prepositions and verbs, working from the last noun backward.
The head noun is the last one; make it the subject and let the rest describe it.

Input: system configuration parameter validation failure
Output: the system failed to validate a configuration parameter

Input: The aircraft fuel system pressure sensor calibration procedure is
documented in Section 4.
Output: Section 4 describes how to calibrate the pressure sensor in the fuel
system.

One exception matters: an established multi-word technical term is a name, not a
stack. "Fuel pump housing" or "transport layer security" should stay intact if
that is what the part or concept is actually called. Breaking a real term to
satisfy this rule creates a worse problem than the stack did. When in doubt, keep
the term and unstack the words around it.

#### 12. Name the thing instead of using a pronoun.

Pronouns force the reader to look backward for a referent. In technical
documentation the referent is often ambiguous, and the reader guesses. Replace
pronouns with the noun. Repeating the noun is not inelegant here; it is correct.

Three specific offenders:

Vague demonstratives. A sentence starting "This causes..." or "These prevent..."
makes the reader hunt for what "this" points to. Name it: "The pressure drop
causes..." If you keep the demonstrative, always attach it to a noun ("This valve,"
"These conditions"), never leave it bare.

Expletive openers. "It is necessary to check the seal" and "There are three
conditions that trigger a rollback" bury the subject behind a placeholder. Write
"Check the seal" and "Three conditions trigger a rollback."

First person. Drop "we," "our," and "I" from technical publications. The document
speaks for the system, not for its authors. "We recommend closing the valve"
becomes "Close the valve" or "Closing the valve prevents backflow."

Second person is a judgment call by house style. Most software documentation
accepts "you" in procedures, while many technical publication standards bar it in
favor of the imperative. The imperative is usually better regardless, because it
is shorter and unambiguous: "Check the seal" beats "You should check the seal."
Follow the document's existing convention, and flag it if the document is
inconsistent.

Input: When the controller detects an overpressure event, it opens the relief
valve. This prevents damage to the downstream components.
Output: When the controller detects an overpressure event, the controller opens
the relief valve. The open valve prevents damage to downstream components.

#### 13. Keep tense and terminology consistent and standard.

Tense drift makes a reader wonder whether something changed. Pick the convention
and hold it across the whole document:

- Present tense for how a system behaves: "the valve opens at 40 psi."
- Imperative for instructions: "Open the valve."
- Past tense only for events that actually happened: "the outage began at 02:14."

Avoid "will" for routine behavior. "The system will send a confirmation" describes
a future promise; "the system sends a confirmation" describes how it works.

Terminology consistency is stricter than tense, and it overrides style variety.
One thing gets one name, every time. If it is a "relief valve" in Section 2, it is
not a "pressure valve" or "the release mechanism" in Section 5. Elegant variation
is a virtue in essays and a defect in technical documentation, because a reader
reasonably assumes two different names mean two different parts. When you find
inconsistent naming, standardize on the term the document defines or uses most,
and list the change so the author can confirm you picked the right one.

Consistent is not enough. The name must also be the one the field uses. Use the
nomenclature found in the field's journals, standards, and textbooks, not a
coined label or a near synonym. A reader who searches for the standard term
should find it in the document. The same holds for symbols and units. Where the
field has competing conventions, pick one, define it on first use, and hold it.
If a term looks nonstandard but you cannot confirm the convention, keep it and
flag it in the change list rather than swap in a guess.

Input: The laser-liquid ablation route produced smaller particles than the
gas-phase laser route.
Output: Laser ablation in liquid produced smaller particles than laser ablation
in gas.

Vary rhythm freely. Never vary terminology.

#### 14. Make abbreviations earn their place.

An abbreviation is a trade: the reader learns a token now to save reading later.
If the saving never comes, the trade was a loss.

Do not abbreviate a term you use only once. "The Environmental Control System
(ECS) regulates cabin temperature" followed by no further mention of ECS is pure
overhead. Delete the parenthetical and let the spelled-out term stand.

Introduce an abbreviation only when the term appears at least three or four times
after the definition, or when the abbreviation is more familiar to the audience
than the expansion. USB, HTTP, and PDF need no introduction in most documents.
Established field nomenclature also qualifies on the first count, because terms
like HEA, TTM, and XRD carry the load of a paper and a reader expects the binding
on first use.

Other rules that keep abbreviations usable: define on first use in the body, with
the spelled-out term first and the abbreviation in parentheses. Spell out terms in
headings and titles, where a reader may land without having read the definition.
Never invent an abbreviation for convenience. Use one expansion for a given
abbreviation throughout.

Input: The Line Replaceable Unit (LRU) must be grounded before removal.
Output: The line replaceable unit must be grounded before removal.
Used once, so the abbreviation is dropped.

#### 15. Break long content into small pieces.

Dense blocks of text hide their structure. A reader scanning for one step or one
condition should find it without parsing a paragraph. Chunking is often a bigger
readability win than any sentence-level edit.

Convert as the content warrants: sequential prose becomes numbered steps, one
action per step. A paragraph comparing options becomes a table. A run of
conditions becomes a bulleted list. A section past roughly five paragraphs gets
subheadings. Keep paragraphs to one topic and roughly three to five sentences.

In procedures, one instruction per step is the rule. A step that says "Remove the
cover, disconnect the harness, and extract the module" is three steps wearing a
disguise, and a technician who stops halfway through loses their place.

Input: To replace the filter, first shut off the supply valve, then wait for
pressure to drop below 5 psi, and after that remove the four retaining bolts
before lifting out the filter housing.
Output:
1. Shut off the supply valve.
2. Wait for pressure to drop below 5 psi.
3. Remove the four retaining bolts.
4. Lift out the filter housing.

#### 16. Punctuate adjectives correctly.

Comma errors between adjectives are common and change how the phrase reads. The
distinction is structural, not stylistic.

Coordinate adjectives modify the noun independently and take a comma. Test them
two ways: insert "and" between them, or reverse their order. If the phrase still
works both ways, they are coordinate, so use a comma. "A small, red valve" passes
both tests ("small and red valve," "red, small valve").

Cumulative adjectives build on each other, with the one nearest the noun forming a
unit with it. They take no comma. "A red hydraulic valve" fails both tests ("red
and hydraulic valve" and "hydraulic red valve" are both wrong), because
"hydraulic valve" is the unit and "red" describes that unit.

Never place a comma between the final adjective and the noun.

Input: a small red, hydraulic valve
Output: a small, red hydraulic valve

Input: a durable, stainless steel fitting
Output: a durable stainless steel fitting
"Stainless steel" is a unit; "durable" describes the fitting, not the steel.

#### 17. Make cross-references exact, and use them only when essential.

A cross-reference asks the reader to stop, find another place, and come back.
Most readers will not make the trip. Each reference has to be worth that cost,
and it has to say exactly where to go and what the reader will find there. Never
invent a figure, table, equation, or section number to make a pointer specific.
If the source does not identify the target, flag it for the author.

**Supporting material.** A general pointer to the supporting information,
supplementary material, or an appendix tells the reader nothing. It sends them to
another long document that most will never open. If the content matters, the
reader needs to know what it is from the main text. Name the exact item and say
what it shows. When the finding itself carries the argument, state the finding in
the main text and cite the item as its source. When the item adds nothing the
reader needs, delete the pointer.

Input: Additional characterization details are provided in the Supporting
Information.
Output: Figure S4 shows the particle size distributions for all five
compositions.
The item number and its content come from the supporting file itself, never from
inference.

**Section references.** Keep them to a minimum. A section reference earns its
place only when the reader cannot follow the current passage without the other
one. Test each by deleting it. If the sentence still works, leave it deleted. A
document where every section points to three others reads as a maze.

A section reference that stays must follow reading order. The reader has only
read what came before. Evidence and claims cannot rest on a later section,
because the reader has not reached it. If an argument needs a later result, move
the result ahead of the argument or move the claim after the result. Backward
references are fine when they are exact. Name the section and the specific point
it established. "As discussed above" and "as mentioned earlier" make the reader
search, so replace them with the exact target or delete them.

Point at the object, not the container. If the reader needs an equation, figure,
or table, cite that item rather than the section that holds it. Often the better
fix restates the short result so the reader never leaves the sentence. All of
this applies only when the reference is essential. Otherwise, cut it.

Input: As will be shown in Section 5, the lattice temperature peaks within 10 ps,
which justifies the fixed-time comparison used here.
Output: [move the 10 ps result ahead of this comparison, or move the comparison
after the result]

Input: The electron temperature was computed with the model described in
Section 2.1.
Output: The electron temperature was computed with Equation 3.

Input: As discussed above, the coupling factor controls the heating rate.
Output: The coupling factor controls the heating rate.

#### 18. Write at the level of the field.

A technical paper should read as expert work and still be followable by a reader
anywhere in its field, not only by the few groups working on the exact problem.
Decide who that reader is from the topic before editing. A paper on femtosecond
laser processing of tungsten is read by laser processing and materials
researchers broadly, not only by ultrafast modelers. A software design document
is read by engineers across the product, not only by the team that wrote the
module.

Pitch the text at that reader. Do not explain what everyone in the field knows.
Defining X-ray diffraction for a materials audience wastes their time and reads
as padding. Do explain what only a subfield knows. A quantity, method, or term
that the broad field would not recognize gets a short definition on first use.
Never trade a precise term for a vague one to seem friendly. Accessibility comes
from defining terms and ordering ideas well, not from lowering the technical
level.

Hold that level through the whole document. A paper that explains basics in the
introduction and then drops undefined subfield terms in the results is written
for two audiences and serves neither. When the right level is unclear from the
topic, say so in the change list rather than guess.

Input: X-ray diffraction, a technique that uses X-rays to probe crystal
structure, showed a single FCC phase. The TTM was solved for the heated film.
Output: X-ray diffraction showed a single FCC phase. The two-temperature model,
which tracks electron and lattice temperatures as separate coupled fields, was
solved for the heated film.

---

### Using the checker

`scripts/check_writing.py` is a deterministic scan. It does not rewrite. It
reports, so you can target the rewrite and then verify it.

```bash
python3 scripts/check_writing.py path/to/document.md
cat draft.txt | python3 scripts/check_writing.py -
```

It reports em dashes with line numbers, unnecessary quotation marks and
parentheses, buzzwords and filler phrases, sentence length statistics,
comma-list pileups, front-loaded
sentences, passive voice, hidden verbs, noun stack candidates, abbreviations that
never earn their definition, vague pronouns, tense mixing, and weak
cross-references. It skips code blocks, so command examples do not create false
hits.

The quotation-mark section splits its findings in two. Scare quotes have no
attribution and no literal-string cue, and those are defects to delete. Literal
strings and interface labels are listed for review, since whether they take
quotes, code formatting, or bold is a house-style decision. Real quotations with
an attributing verb are not flagged.

The parenthesis section splits its findings in two. The remove list holds prose
asides, with full clauses marked separately from short qualifiers, plus every
figure, table, section, and equation callout, since those belong in the sentence.
The review list holds the cases a style guide would tolerate but this skill does
not accept by default: unit conversions and tolerances, part and model numbers,
and the "(s)" plural marker. Rewrite each one unless you can name the rewrite you
rejected. Exempt and never reported: math, list markers, author-year citations,
and nomenclature definitions in either order, so `high entropy alloys (HEA)` and
`HEA (high entropy alloy)` both pass silently. The definition check matches the
initials against the neighboring short form, so an ordinary lowercase aside is
still flagged.

The abbreviation section separates three cases. An abbreviation defined in
parentheses and then used once or twice is the real defect, because the
definition cost more than the short form saved. An undefined short form coined
once is usually better written out. A widely known abbreviation used once is
listed for information only and needs no action.

The cross-reference section lists every section reference for review, because
each one has to justify itself. It flags three defects. A section reference that
points past the current section is a forward reference. A pointer such as "see
below" or "as discussed above" is vague. A mention of supporting information,
supplementary material, or the appendix that names no specific item is vague
too. Forward detection needs numbered headings, either Markdown headings that
begin with a number or LaTeX sectioning commands. Without them, the report says
the forward check was skipped. A backward pointer followed by a citation, such as
"as shown previously [12]," counts as a literature reference and passes.

Run it on the source to plan the edit, then on your rewrite to confirm em dashes
are at zero and the other counts dropped. Some sections are heuristic and will
produce occasional false positives, especially noun stacks and passive voice. Read
each flag and judge it; do not blindly rewrite everything it lists. A clean report
is a floor, not proof that the prose is good.

### Output format

Return the rewrite, then the change summary:

```
## Cleaned version

[the full rewritten text]

## What changed

- Em dashes: removed 4 (split into separate sentences or replaced with colons).
- Quotation marks: removed 3 sets of scare quotes; moved 2 literal values to
  code formatting.
- Parentheses: folded 4 asides into their sentences, worked 3 figure callouts
  into the sentences that needed them, moved P/N 4471-A out of brackets, and
  wrote "bolts" for "bolt(s)". Kept two: the HEA definition and the 106 in-lb
  conversion.
- Voice: converted 7 passive constructions to active.
- Hidden verbs: "perform an inspection of" to "inspect," 3 similar.
- Noun stacks: broke up 2 four-noun strings.
- Pronouns: replaced 5 bare "this"/"it" with the actual noun.
- Abbreviations: dropped ECS and LRU, each used only once.
- Cross-references: named the item behind 3 vague Supporting Information
  pointers, cut 4 of 6 section references, and moved one result ahead of the
  claim that relied on it. Flagged one pointer whose target the source never
  names.
- Terminology: standardized "laser-liquid ablation" to "laser ablation in
  liquid." Confirm the choice.
- Sentences: split 6 running past 30 words; average is now 17 words.
- Cut: the closing summary in each section and two off-topic asides.
- Left as-is: latency figures, API names, and the term "fuel pump housing"
  (established term, not a noun stack).
```

Keep the summary short and grouped by issue type rather than listing every edit.
If you left something unchanged to protect a technical meaning, say so. That is
usually the most useful line in the list.


---

# Part B: catalog of machine-writing tells

Source: `references/ai-tells.md`

## Catalog of machine-writing tells

A reference for the cleanup pass. You do not need to memorize this. Read it when
you want the full list behind a category, or when a draft has a tell you can feel
but cannot name. Each entry says what to do instead.

### Table of contents

1. Punctuation tells (em dashes, scare quotes, parentheses)
2. Buzzwords (plain-word swaps)
3. Filler and throat-clearing
4. Formulaic sentence constructions
5. Structural tells
6. Hedging and vague quantifiers

---

### 1. Punctuation tells

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

### 2. Buzzwords (plain-word swaps)

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

### 3. Filler and throat-clearing

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

### 4. Formulaic sentence constructions

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

### 5. Structural tells

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

### 6. Hedging and vague quantifiers

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

### The underlying goal

None of these are sins on their own. A single em dash or one "leverage" would not
give a document away. The tell is the accumulation: the same moves, over and
over, with no human variation. Your job is to make the writing read like a person
who knows the subject wrote it with care. Specific, direct, varied in rhythm, and
free of the filler that pads machine output. When a rule here would make the
prose worse or less clear, ignore the rule and keep the prose clear.


---

# Part C: technical publication rules

Source: `references/tech-pub-rules.md`

## Technical publication rules: detailed reference

Deeper treatment of Part 2 in SKILL.md. Read a section when a case in the main
skill is not clear-cut, or when you need the longer conversion tables.

### Table of contents

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

### 1. Active and passive voice

Active voice puts the actor first: subject, verb, object. "The loader reads the
file." Passive reverses it and makes the actor optional: "The file is read by the
loader," or worse, "The file is read."

The cost of passive in technical documentation is the dropped actor. A procedure
that says "the circuit breaker must be opened" leaves a technician wondering
whether they open it, another team opens it, or the system opens it
automatically. Ambiguity in a procedure is a safety problem, not a style problem.

#### Genre decides the default

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

#### How to spot it

Look for a form of "to be" (is, are, was, were, be, been, being) or "get"
followed by a past participle: "is configured," "was replaced," "must be
verified," "gets triggered." If you can append "by the ..." and the sentence still
works, it is passive.

#### How to convert it

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

#### When passive is correct

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

### 2. Hidden verbs (nominalizations)

A nominalization turns a verb into a noun. The sentence then needs a weak helper
verb (perform, conduct, make, provide, carry out, give, take, effect, achieve) to
carry the grammar, and the real action sits inert in the middle.

#### Giveaway endings

-tion, -sion, -ment, -ance, -ence, -ity, -al, -ure, and -ing used as a noun.

#### Conversion table

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

#### The "the ___ of" pattern

"The <noun> of <thing>" is the most common hidden verb in specifications. "The
removal of the panel requires two technicians" becomes "Removing the panel
requires two technicians," or better, "Two technicians remove the panel."

#### Worked example

Before: Verification of the seal integrity shall be performed by the technician
prior to the commencement of pressurization operations.

Three problems compound here: "verification" hides "verify," "be performed" is
passive, and "commencement of pressurization operations" is both a hidden verb
and a noun stack.

After: Before pressurizing the system, the technician verifies that the seal is
intact.

Word count drops from 17 to 12 and the actor becomes explicit.

---

### 3. Noun stacks

A noun stack (also called a noun cluster or noun string) is three or more nouns in
sequence, each modifying the next. English lets you do this, but the reader gets
no grammatical signal about which noun attaches to which, so they must resolve the
ambiguity from domain knowledge.

Two nouns are normal ("fuel pump"). Three is a warning sign. Four or more is
almost always a defect.

#### How to unstack

The head noun is the last one in the string. Everything before it is a modifier.
To unstack, make the head noun the subject or object, then reattach the modifiers
with prepositions and verbs, working backward from the head.

Example: "system configuration parameter validation failure"

Head noun: failure. Working backward: failure of validation, validation of a
parameter, parameter of configuration, configuration of the system.

Result: "the system failed to validate a configuration parameter."

#### More examples

| Stacked | Unstacked |
|---|---|
| aircraft fuel system pressure sensor calibration procedure | procedure for calibrating the pressure sensor in the fuel system |
| user account password reset request form | form for requesting a password reset |
| database connection pool exhaustion error | error raised when the database connection pool is exhausted |
| network interface configuration file syntax check | syntax check of the network interface configuration file |
| engine oil temperature warning indicator | engine oil temperature warning indicator (established term; leave it) |

#### The established term exception

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

### 4. Pronouns and referents

Every pronoun asks the reader to search backward. Technical documentation is read
in fragments, out of order, and under time pressure, so that search often fails.

#### Vague demonstratives

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

#### Ambiguous "it," "they," and "which"

When a sentence contains two candidate antecedents, "it" is guaranteed trouble.

Before: When the service connects to the proxy, it logs the handshake.

Which one logs it? Rewrite: "When the service connects to the proxy, the service
logs the handshake."

The same applies to a trailing "which," which often points at a whole clause:
"The pump ran dry, which damaged the seal" is acceptable in prose but better as
"Running dry damaged the pump seal."

#### Expletive constructions

"It is" and "there is/are" at the start of a sentence are placeholders that push
the real subject to the back and often hide a passive or a hidden verb.

| Expletive | Direct |
|---|---|
| It is necessary to check the seal. | Check the seal. |
| It is recommended that you restart the service. | Restart the service. |
| There are three conditions that trigger a rollback. | Three conditions trigger a rollback. |
| There is a requirement for annual calibration. | Calibrate the unit annually. |

#### First and second person

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

### 5. Tense conventions

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

### 6. Terminology consistency

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

### 7. Abbreviations and acronyms

An abbreviation is a trade: the reader spends effort learning a token now to save
effort later. The trade only pays off with repetition.

#### The single-use rule

Never define an abbreviation you use once. "The Environmental Control System
(ECS) regulates cabin temperature," with no later mention of ECS, costs the reader
a definition and returns nothing. Delete the parenthetical and let the spelled-out
term stand alone.

#### When to introduce one

Introduce an abbreviation when either condition holds:

- The term appears at least three or four more times after the definition.
- The abbreviation is more familiar to the audience than the expansion. Most
  readers know USB, HTTP, PDF, and RAM better than the words behind them.
  Expanding these can hurt readability rather than help it.

#### Mechanics

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

### 8. Chunking and information design

Chunking often improves readability more than any sentence-level edit, because it
exposes structure the prose was hiding.

#### Conversions worth making

- Sequential prose becomes numbered steps, one action per step.
- A paragraph comparing two or more options becomes a table.
- A run of parallel conditions or requirements becomes a bulleted list.
- A long section gets subheadings a reader can scan.
- A paragraph carrying two topics becomes two paragraphs.

#### Targets

Keep paragraphs to one topic and roughly three to five sentences. Keep procedures
to one instruction per step. A step reading "Remove the cover, disconnect the
harness, and extract the module" is three steps in disguise, and a technician
interrupted midway loses their place with no way to mark progress.

Put the condition before the action in a step, so the reader knows whether the
step applies before they perform it: "If the indicator is red, replace the
filter," not "Replace the filter if the indicator is red."

Front-load warnings. Safety information belongs before the step it applies to,
never after.

#### Worked example

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

### 9. Coordinate and cumulative adjectives

Whether a comma belongs between two adjectives is a structural question with a
reliable test, not a matter of taste.

#### Coordinate adjectives: use a comma

Coordinate adjectives each modify the noun independently. Two tests confirm it:

1. Insert "and" between them. Does it still read correctly?
2. Reverse their order. Does it still read correctly?

If both tests pass, the adjectives are coordinate and take a comma.

"A small, red valve" passes: "a small and red valve" works, and "a red, small
valve" works. Comma required.

#### Cumulative adjectives: no comma

Cumulative adjectives build on one another. The adjective nearest the noun forms a
unit with it, and the earlier adjective modifies that whole unit.

"A red hydraulic valve" fails both tests: "a red and hydraulic valve" is wrong,
and "a hydraulic red valve" is wrong. No comma, because "hydraulic valve" is the
unit and "red" describes that unit.

#### More examples

| Correct | Type |
|---|---|
| a small, red valve | coordinate |
| a durable, lightweight housing | coordinate |
| a red hydraulic valve | cumulative |
| a durable stainless steel fitting | cumulative ("stainless steel" is a unit) |
| three large steel brackets | cumulative |
| a clear, concise procedure | coordinate |
| the old aluminum bracket | cumulative |

#### The rule that has no exceptions

Never put a comma between the final adjective and the noun. "A small, red, valve"
is always wrong.

#### Common error pattern

Writers often place the comma by rhythm rather than structure, which yields "a
small red, hydraulic valve." Apply the tests: "small" and "red" are coordinate, so
the comma belongs between them, and "hydraulic valve" is a unit, so no comma
precedes it. Correct: "a small, red hydraulic valve."

---

### 10. Quotation marks

Quotation marks carry a specific meaning: the enclosed text is somebody else's
words, or a literal string, or a term under definition. Used for anything else,
they tell the reader the writer is distancing themselves from the word.

#### Delete these

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

#### Keep these

Quotation marks are correct for quoted speech or text from an identified source,
the exact string a reader types or sees returned, a term being defined on first
use, and the title of a section or document in a cross-reference.

#### Preferred formatting in technical documents

| Content | Convention |
|---|---|
| command, filename, path, parameter, value, returned string | code formatting |
| interface label (button, field, menu, tab) | bold, per most house styles |
| section or document title in a cross-reference | quotes or italics, per house style |
| term being defined on first use | italics |
| quoted text from a source | quotation marks |

Code formatting beats quotes for literal values for two reasons. It survives copy
and paste, and it removes any chance the reader reads the quotes as irony.

#### Punctuation inside or outside

US convention places periods and commas inside the closing quotation mark. That
convention breaks for literal strings, because a period inside the quotes looks
like part of the string. When the quoted text is a value the reader must type or
match, put the punctuation outside, or better, use code formatting and sidestep
the question. `Set the level to "verbose".` is unambiguous; `Set the level to
"verbose."` suggests the trailing period is part of the value.

#### Consistency

Whatever the house style chooses, apply it to every instance in the document. A
document that bolds some button labels and quotes others reads as unedited.

---

### 11. Parentheses

Parentheses signal that the enclosed text is outside the sentence. In technical
documents readers act on that signal and skip what is bracketed. Anything a
reader can skip without consequence should not have been written; anything with
consequence should not be bracketed.

#### Fold it in or split it out

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

#### Keep the parentheses

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

#### Two hard limits

Nested parentheses are always a defect. A reader tracking two levels of aside has
lost the sentence. Rewrite.

A parenthetical that runs longer than the clause containing it is a defect for
the same reason. Promote it to its own sentence.

---

### 12. Plain word substitutions

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
