---
name: keel-interview
description: "KEEL 2.0.0 SPEC interview: asks the developer a few questions at a time about the gaps in docs/SPEC.md (edge cases, non-goals, trade-offs, constraints, glossary terms, acceptance criteria) and writes the answers as PROPOSED blocks for acceptance. Use in a KEEL project when the developer runs keel-interview (/keel:keel-interview or /keel-interview), asks to interview them about the spec, or wants to fill the gaps in SPEC.md."
argument-hint: "[feature or area to focus on]"
metadata:
  version: "2.0.0"
  source: "https://github.com/DominusFL/keel"
---
# KEEL 2.0.0: SPEC interview

Fill the gaps in `docs/SPEC.md` by interviewing the developer, under KEEL version 2.0.0 (October 31, 2026), https://github.com/DominusFL/keel.

If the developer gave instructions with the command, such as a feature to focus on, follow them: $ARGUMENTS

## Steps

1. **Confirm the project uses KEEL** (`AGENTS.md` has an `Aligned to KEEL` stamp and `docs/SPEC.md` exists). If not, stop and tell the developer to run `keel` first.
2. **Read `docs/SPEC.md`** and the area map in `docs/ARCHITECTURE.md`. List the gaps by section: Goals, Users, Glossary, Features & user stories, Constraints, Acceptance criteria & test cases, Non-goals, Open questions. The SPEC template is in `templates/docs/SPEC.md`.
3. **Interview.** Ask a few questions at a time, and skip questions the docs already answer. Cover edge cases, non-goals, trade-offs, constraints, glossary terms, and acceptance criteria. The developer may stop at any time.
4. **Write the answers as PROPOSED blocks** in `docs/SPEC.md`, next to the text they change, never only in chat (the rule and the block format are below). Give each new acceptance criterion the next `AC-n` ID and its test cases, and note that `docs/RELEASE-CHECKLIST.md` needs a matching row once the block is accepted.
5. **Report** the PROPOSED blocks by file and AC ID or heading, and list them in `docs/HANDOFF.md` under Waiting at the next session close.

Never edit accepted SPEC text. The standard is in `references/standard.md`.

## The interview rule

**SPEC interview:** After you seed or migrate `SPEC.md`, offer to interview the developer about its gaps: edge cases, non-goals, trade-offs, constraints, glossary terms, and acceptance criteria. Ask a few questions at a time, and skip questions the docs already answer. Write the resulting SPEC changes as PROPOSED blocks for acceptance (rule 1). The developer may decline. If you offer an as-built review, offer the interview after it.

**Proposed changes to SPEC and DESIGN:** The AI never edits accepted text in `SPEC.md` or `DESIGN.md` (rule 1). It writes each proposal in the file, next to the text it changes, as a PROPOSED block, never only in chat:

```md
> PROPOSED 2026-10-31 (Claude Code): change AC-3 to allow an empty email.
> Reason: the form now has a guest path. Code: src/forms/signup.js.
```

A PROPOSED block is not a requirement and not a design. The developer accepts it by applying the edit and deleting the marker, rejects it by deleting the block, or tells the AI to do either. A block is named by its file and the AC ID or heading it changes (`SPEC.md AC-3`). The AI lists pending blocks in its task summary and, at the next close, in `HANDOFF.md` under Waiting. No block may remain at a release (rule 6).

---

This skill is generated from `KEEL.md` in https://github.com/DominusFL/keel. Do not edit it by hand; change `KEEL.md` and run `python3 build/build.py`.
