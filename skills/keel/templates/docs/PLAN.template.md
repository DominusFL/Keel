> Tracker: TICKET-# (name of project)
(Milestones and the work board. Every Shared or multi-file change gets a board row; a Small one-file change needs none. Track smaller tasks in the tracker.)

## Definition of ready
A Shared change, a change that touches several files, or a change whose approach is unclear starts only after the developer approves this card (classes: AGENTS.md Making changes):

    Change: (name, one line)
    Class: (Small / Shared / Release, and why)
    ACs: (added or changed; each written now as a PROPOSED block in SPEC.md or DESIGN.md, named by file and AC ID or heading)
    Files: (paths, with their areas from the area map in ARCHITECTURE.md)
    Tests: (to add or run, and the affected areas)
    Docs: (to update)
    Out of scope: (what this change will not do)

## Definition of done
Before calling a task done:
- Tests added/updated; targeted tests and the docs check pass, plus affected areas if other code uses the changed code (see the AGENTS.md Testing section; no full regression unless it calls for one)
- Shared change: fresh-context review of the diff against the ACs done; findings fixed or listed
- Area map in ARCHITECTURE.md updated if code, tests, or areas changed
- Task summary in this shape, every line present ("none" if empty):

      Changed: (files)
      Class: (Small / Shared / Release)
      Tested: (command -> pass/fail counts; results file)
      Reviewed: (fresh-context result for a Shared change, or n/a)
      Docs updated: (files) | Docs checked, no change: (files; search terms used)
      Proposed: (PROPOSED blocks by file and AC ID or heading)
      Decided without asking: (one line each)
      Skipped: (step and why)
      Next: (one action)

- Result matches the ready card, if there was one; anything outside it is reported, not done
- Code is readable and documented per the AGENTS.md rules
- Affected docs updated, as listed in the AGENTS.md Docs list (SPEC and DESIGN changes written as PROPOSED blocks; all other docs updated directly)
- DESIGN-GUIDE.html, if it exists, regenerated if DESIGN.md changed
- USER-GUIDE.md, if it exists, updated if user-facing behavior changed
- RELEASE-CHECKLIST.md updated if acceptance criteria changed
- `.env.example` updated if environment variables changed
- AGENTS.md Docs and Skills lists updated if files or skills changed
- Work board row updated, if the change has one (Status; Done when finished)

## Milestones
- [ ] M1: (name; owner; status)
- [ ] M2:

## Work board
(One row per work item in the current milestone. Claim an item by setting Owner and Status before you start. Two In progress rows may not list the same file; if another row holds a file you need, do not start: add the dependency and pick another item or ask. Mark Done; delete nothing. When open rows pass about 15, move this table to docs/plans/M<n>.md and keep only the milestones here. A solo developer keeps the board too; it stays short.)
| Item | Owner | Areas | Files | Status | Branch or ticket | Started |
|---|---|---|---|---|---|---|
| (Guest signup) | (Rick / Claude Code) | (Signup) | (src/forms/signup.js) | (Ready / In progress / Blocked / Review / Done) | (TICKET-12) | (YYYY-MM-DD) |
