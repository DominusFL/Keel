---
name: keel-as-built
description: "KEEL 2.0.0 as-built review of existing code: feature inventory, area map in ARCHITECTURE.md, SPEC acceptance criteria inferred from the code as PROPOSED blocks, and a differences and health report (built but not specified, specified but not built, no tests, secrets, risky dependencies). Changes no code. Use in a KEEL project when the developer runs keel-as-built (/keel:keel-as-built or /keel-as-built) or asks for an as-built review, to document existing code, or to set the Verified dates."
argument-hint: "[area names to review, or 'all']"
metadata:
  version: "2.0.0"
  source: "https://github.com/rickflashman/keel"
---
# KEEL 2.0.0: as-built review

Document what the code does now, under KEEL version 2.0.0 (October 31, 2026), https://github.com/rickflashman/keel. Change no code. Do not run tests unless the developer asks.

If the developer gave instructions with the command, such as the areas to review, follow them: $ARGUMENTS

## Before you start

- The project follows KEEL: `AGENTS.md` has an `Aligned to KEEL` stamp and `docs/ARCHITECTURE.md` and `docs/SPEC.md` exist. If not, stop and tell the developer to run `keel` first.
- The developer may choose only some areas. Confirm the scope before step 1.
- Use a subagent per area where the tool allows, so the main context stays small.
- The templates for the files you write are in `templates/`; the standard, including the rules on PROPOSED blocks and the area map, is in `references/standard.md`.

## The review

**As-built review:** If the project has code, offer this review after the setup, migration, or upgrade is complete and reported. The developer may decline or choose only some areas. On approval, follow these steps in order:
1. **Feature inventory.** List the features the code implements, each with its entry points (routes, commands, screens, jobs, public modules) and folders. Show the list. The developer confirms, renames, merges, or drops items. Do not read deeper until the list is confirmed.
2. **Area map.** Fill the area map in `ARCHITECTURE.md` for the confirmed areas: code, entry points, tests, command, dependencies (from imports). Set Confidence to Inferred on every row, and mark the table "Inferred from code, needs developer review".
3. **One area at a time, with a budget.** Read 1 area, write or update its `ARCHITECTURE.md` content (stack, folders, commands, data model, operations), then stop and report before the next. Use a subagent per area where the tool allows, so the main context stays small. If an area exceeds the budget, set its Confidence to Low and record where reading stopped.
4. **SPEC from behavior.** For each area, write feature text and acceptance criteria that describe what the code does now. If `SPEC.md` is empty or holds only the template, seed it and mark the content "Inferred from code, needs developer review". If `SPEC.md` has content, write the differences as PROPOSED blocks (see *Proposed changes to SPEC and DESIGN*). The same applies to `DESIGN.md`. Never change accepted SPEC or DESIGN text from code.
5. **Differences and health.** Report what is built but not specified, what is specified but not built, superseded approaches still in the code, areas with no tests, secrets found, and dependencies with known issues. Lasting findings go to `RESEARCH.md`; questions go to `HANDOFF.md` under Waiting. Set the Verified date in `ARCHITECTURE.md`, and in `SPEC.md` once the developer has reviewed it.
6. **Stop conditions.** Change no code. Do not run tests unless the developer asks.

**Proposed changes to SPEC and DESIGN:** The AI never edits accepted text in `SPEC.md` or `DESIGN.md` (rule 1). It writes each proposal in the file, next to the text it changes, as a PROPOSED block, never only in chat:

```md
> PROPOSED 2026-10-31 (Claude Code): change AC-3 to allow an empty email.
> Reason: the form now has a guest path. Code: src/forms/signup.js.
```

A PROPOSED block is not a requirement and not a design. The developer accepts it by applying the edit and deleting the marker, rejects it by deleting the block, or tells the AI to do either. A block is named by its file and the AC ID or heading it changes (`SPEC.md AC-3`). The AI lists pending blocks in its task summary and, at the next close, in `HANDOFF.md` under Waiting. No block may remain at a release (rule 6).

---

This skill is generated from `KEEL.md` in https://github.com/rickflashman/keel. Do not edit it by hand; change `KEEL.md` and run `python3 build/build.py`.
