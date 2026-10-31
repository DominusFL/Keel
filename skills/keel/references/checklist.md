# KEEL 2.0.0: checklist

Reference for the `keel` skill, generated from `KEEL.md` (https://github.com/DominusFL/keel). Do not edit by hand.

## Initialization checklist

After creating the initial files, confirm each item and report any that fail.

- [ ] `README.md`, `docs/SPEC.md`, `docs/ARCHITECTURE.md`, `docs/PLAN.md`, and `docs/RELEASE-CHECKLIST.md` exist, from the starter templates, unless the developer chose not to use one and it is on the `AGENTS.md` "Not used" line.
- [ ] Every SPEC acceptance criterion has an ID and a matching check in `RELEASE-CHECKLIST.md`. `SPEC.md` has the Glossary and Constraints headings.
- [ ] `ARCHITECTURE.md` has the Operations section and the area map with a Docs row. The docs check script exists, is listed in the map, and passes.
- [ ] `PLAN.md` has the Definition of ready, the Definition of done, and the work board.
- [ ] A project with a UI has `docs/DESIGN.md` and `docs/DESIGN-GUIDE.html`. A project without one has neither, and `AGENTS.md` does not list them.
- [ ] `AGENTS.md` is under about 120 lines and has the version stamp, the precedence line, and the Project documentation standard, Making changes, Testing, Reporting, Session handoff, Docs, and Skills sections.
- [ ] `CLAUDE.md` starts with `@AGENTS.md`, and `.github/copilot-instructions.md` (exact name) points to `AGENTS.md`. Neither copies rules from `AGENTS.md`.
- [ ] Every tracker header has the tracker name and `TICKET-# (name of project)` filled in, or keeps the placeholder for the developer.
- [ ] Every required section that does not apply says why (for example, no authentication in `ARCHITECTURE.md`).
- [ ] Optional files exist only where needed and are listed in `AGENTS.md`. `docs/HANDOFF.md` was not created, unless a migration or the as-built review wrote to it, and `docs/CHANGELOG.md` was not created, unless a migration moved release history into it.
- [ ] No PROPOSED blocks exist, unless a migration or the as-built review created them; those are listed in the report and in `HANDOFF.md` under Waiting.
- [ ] No file contains secrets or customer data, and `.gitignore` excludes `.env` and `test-results/` if the project uses version control.
- [ ] After a migration: no Superseded content was migrated, and `docs/archive/INDEX.md` lists every archived file.
- [ ] No existing file was overwritten without the developer's approval, and `KEEL.md` was not deleted, renamed, moved, or modified, except by a switch to the skill on the developer's explicit instruction.
