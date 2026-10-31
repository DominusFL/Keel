# Project rules
AI working rules for every AI coding tool on this project. CLAUDE.md and .github/copilot-instructions.md only point here. Keep this file under about 120 lines; cut any line whose removal would not cause mistakes.

## Project documentation standard
- Aligned to KEEL 2.0.0 (https://github.com/DominusFL/keel). Update when the docs are realigned.
- If `KEEL.md` is in the project root, read it before creating docs or changing the doc structure; it is the authority. Never delete, rename, move, modify, or archive it without explicit developer instruction. If it is absent, follow the KEEL skill when it is installed, else the existing docs, and keep this section. Developer instructions override both.
- Precedence, highest first: developer instruction > docs/decisions/ > SPEC.md and DESIGN.md (accepted text, not PROPOSED blocks) > ARCHITECTURE.md and PLAN.md > HANDOFF.md and RESEARCH.md > the code (evidence only) > docs/archive/ (never a source).

## Commands
- In README.md (from the ticket) and docs/ARCHITECTURE.md. Record new commands in ARCHITECTURE.md only.

## Conventions
- (Project-specific code style, naming, folder rules)
- Ask before touching: (paths that need a ready card and approval regardless of size, such as auth, data migrations, build config, CI; "(none)" if none)
- Area owners: (optional: area, owner, review required; delete if unused)

## Code
- No clever or compressed code; if performance needs it, comment why.
- Header comment on every file; doc comment on every function/component (what, inputs, outputs); inside, comment only the *why* of non-obvious logic.

## Making changes
- Classify first, then act by class:
  - Small (1 area, no shared code): change directly; targeted tests.
  - Shared (shared code, data model, auth, build config, dependency upgrade, cross-area refactor, or an ask-before-touching path): ready card and approval first; affected tests; then a fresh-context review of the diff against the ACs.
  - Release: docs/RELEASE-CHECKLIST.md.
- Ready card, for a Shared change, a multi-file change, or an unclear approach: the Definition of ready in docs/PLAN.md.
- Bug fix: reproduce first with a failing test or captured error output, and save the test; no repro, no fix. Never guess a version pin. If the same fix fails twice, stop, report, and ask.
- Update the affected docs in the same task, never deferred to the handoff file or a later task. Before you finish, search docs/ for each path, name, label, and behavior you changed (names: area map, SPEC Glossary) and update each hit.
- SPEC and DESIGN: never edit accepted text. Write a PROPOSED block next to the text it changes, never only in chat: `> PROPOSED YYYY-MM-DD (tool): the edit. Reason: ... Code: path.` Name it by file and AC ID or heading. The developer accepts by applying the edit and deleting the marker, or rejects by deleting the block.

## Testing
- Read the Testing section and area map in docs/ARCHITECTURE.md before you read code or run or write a test; read only the areas you change. Each test names the AC it covers.
- Run only what the change needs: new and updated tests, the changed area's tests, the docs check, and the tests of areas that use the changed code. If a failure points outside the changed area, run those areas too. Do not retest unchanged areas.
- Full regression only before a release or when the developer asks; otherwise ask first and say why.
- Never weaken, skip, or delete a test to make it pass; report the failure and its cause. After 3 test-fix rounds, stop and report.

## Reporting
- Lead with the result. No preamble, recap, or effort estimates; lists of at most 5 items. Full content for errors, failing tests, and confirmations.
- Before reporting done, re-read the Definition of done in docs/PLAN.md and your ready card, and end with the task summary it defines, every line present.
- A check you could not run is "Not run: reason", never passed. A pass claim cites test-results/latest.md. To dismiss a review finding, cite the file and line that shows it is wrong.

## Decisions
- Before a structural or technology choice, check docs/decisions/. Never reverse a decision; supersede it: write a new note, then set the old note's Status to "Superseded by NNNN", the only edit allowed.
- Note choices that are hard to reverse or affect multiple files (stack, data model, auth, hosting, major dependencies); skip routine ones. File: docs/decisions/NNNN-short-title.md, next number, no ticket ID, same format as the newest note (first note: `# NNNN: Title`, Status, Context, Decision, Why). On a number collision, the later merge renumbers. Mention new notes in your summary.

## Session handoff
- Handoff file: docs/HANDOFF.md (teams: docs/handoff/<developer>.md, one per developer). At session start, read it if it exists, and the work board in docs/PLAN.md.
- Close routine, when the developer closes the session, before any compact or clear, or when most of the context is used: (1) Route: print one line per item: a choice -> docs/decisions/; evidence or results -> docs/RESEARCH.md; milestones -> docs/PLAN.md; commands, structure, lasting traps -> docs/ARCHITECTURE.md; release results -> docs/RELEASE-CHECKLIST.md; requirement or UI changes -> PROPOSED block; leftovers -> the handoff file (Next | Waiting | Assumed | Decided without asking | Traps). (2) Write the routed items into their docs. (3) Rewrite the handoff file (never append; if missing, create it with Where we left off and those 5 sections) with only what step 1 routed there; print the line count. After a close at the context limit, tell the developer to start a new session from the handoff file; do not continue on a compacted context.
- Handoff file: about 40 lines; every bullet dated; anything older than one session is moved or deleted, never copied forward. Not rewritten after every change; if something important would be lost before the close, record it now in its proper doc or in the handoff file. It never overrides other docs; on a conflict, they win: flag it.

## Always / Never
- Always: mention the ticket ID when describing work; meet the Definition of done before finishing; claim a work board row before a Shared or multi-file change.
- Never: put secrets in code or docs; mark a release check passed without running it; create a new version of a doc (such as SPEC-v2.md) beside the old one; edit docs/archive/ or use it as a source.

## Docs (read the one that matches your task)
- docs/SPEC.md: requirements, glossary, constraints. PROPOSED blocks only.
- docs/ARCHITECTURE.md: area map, structure, commands, operations. Read before structural changes. Update directly.
- docs/PLAN.md: work board, Definition of ready and done. Update directly. (docs/plans/M<n>.md: per-milestone boards, when used.)
- docs/RELEASE-CHECKLIST.md: release gate; follow it before every release. A human approves.
- docs/decisions/: past decisions.
- docs/HANDOFF.md (teams: docs/handoff/<developer>.md): read at session start.
- docs/CHANGELOG.md: entry at each release (create at the first); read only the top entries.
- docs/DESIGN.md: read before touching UI. PROPOSED blocks only. docs/DESIGN-GUIDE.html: generated from it; never edit by hand; regenerate when DESIGN.md changes.
- docs/USER-GUIDE.md: end-user guide in STE; update directly for current user-facing behavior.
- docs/RUNBOOK.md: operations for support staff. Update directly.
- docs/images/: images used by the docs.
- docs/MOCKUP.md: read before mockups; update directly; never redefines production requirements.
- docs/RESEARCH.md: check before researching again; save research worth keeping (create if needed).
- docs/archive/: migration originals, history only; INDEX.md says what replaced each.
- Not used (developer decision; do not recreate or report missing): (none)

## Skills (.claude/skills/<skill-name>/SKILL.md)
- When a task matches a skill listed here, read and follow its SKILL.md (some tools do not scan this folder).
- (`<skill-name>`: one-line purpose. Leave empty if none.)
