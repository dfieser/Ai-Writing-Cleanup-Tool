# AI Writing Cleanup

A Claude skill that edits technical writing so it reads like a knowledgeable
person wrote it rather than a language model. It removes the tells of machine
prose, applies ordinary technical-writing discipline, and changes no technical
fact.

Two halves do the work. `SKILL.md` holds 18 rules that Claude applies with
judgment. `check_writing.py` runs 16 deterministic checks that count what
judgment cannot, so you get a number before the edit and after.

## Start here

```bash
git clone https://github.com/dfieser/Ai-Writing-Cleanup-Tool.git
cd Ai-Writing-Cleanup-Tool
./install.sh
```

Start a new Claude session, then ask for an editing pass:

> Clean up docs/install.md. It reads like a machine wrote it.

Scan a file without Claude:

```bash
python3 skills/ai-writing-cleanup/scripts/check_writing.py draft.md
```

## Pages

- [The Rules](The-Rules) lists all 18 rules with examples, and maps each one to
  the check that detects it.
- [Checker Reference](Checker-Reference) explains all 16 checks, what each one
  flags, and where each one guesses.
- [Editing Workflow](Editing-Workflow) covers how to ask, what comes back, and
  how to review it.
- [FAQ](FAQ) answers the questions that come up first.

## The rule that outranks the others

Every number, command, file path, API name, version, and part number survives
the edit exactly as written. If a cleaner sentence would change a technical
meaning, the skill keeps the meaning and finds other wording. If a sentence is
ambiguous, the skill leaves it alone and says so in the change list. A cleaner
sentence that says the wrong thing is a failure, not an improvement.

Text inside code blocks, command examples, config samples, and literal output is
data, not prose. The skill never touches it, and the checker skips it.

## Repository

Source, installer, tests, and examples live at
[dfieser/Ai-Writing-Cleanup-Tool](https://github.com/dfieser/Ai-Writing-Cleanup-Tool).
