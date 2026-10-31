---
name: keel-upgrade
description: "KEEL 2.0.0 migration and upgrade: brings an existing project's documentation up to the KEEL standard (inventory, currency, mapping, approval, migrate, archive), upgrades a project on an older KEEL or AI-PROJECT-DOCS-STANDARD version, or switches a project from the KEEL.md file to this skill. Use when the developer runs keel-upgrade (/keel:keel-upgrade or /keel-upgrade), says 'migrate the docs to KEEL', 'upgrade KEEL', or 'switch to the KEEL skill'."
disable-model-invocation: true
argument-hint: "[migrate | upgrade | switch]"
metadata:
  version: "2.0.0"
  source: "https://github.com/DominusFL/keel"
---
# KEEL 2.0.0: migrate, upgrade, or switch

Bring an existing project up to KEEL version 2.0.0 (October 31, 2026), https://github.com/DominusFL/keel. Three cases:

- **Migration:** the project has documentation in another form (a README, notes, rules files, an older wiki export). Follow *Migrating or upgrading an existing project* below, steps 1 to 9.
- **Upgrade:** the project follows an older version of this standard (the stamp in `AGENTS.md` is older than 2.0.0, or names *AI-PROJECT-DOCS-STANDARD*). Do steps 1, 8, and 9. `references/changelog.md` lists what changed in each version.
- **Switch to the skill:** the project has `KEEL.md` in its root folder and the developer wants this skill to be the reference instead. Follow the Switch to the skill path in the Initialization rules below.

If the developer gave instructions with the command, follow them: $ARGUMENTS

Whatever the case, change nothing until the developer approves the plan. Change only documentation, never code, configuration, or dependencies; the docs check script is the one exception. Use the templates in `templates/` (guidance: `templates/README.md`). When the work is complete, run `references/checklist.md`, report, and offer the as-built review (`keel-as-built`) and the SPEC interview (`keel-interview`).

The rest of this file holds the initialization rules, the migration and upgrade steps, and the parts of the standard they rely on.

## Initialization rules

- **Check first:** Before you create anything, check the project and choose 1 path:
  - **Upgrade:** `AGENTS.md` (or `CLAUDE.md` before 1.2.0) has a version stamp older than this skill's version, and there is no other documentation to bring in. A stamp that names *AI-PROJECT-DOCS-STANDARD* is an older version of this standard (KEEL 1.x). Follow the upgrade-only path in *Migrating or upgrading an existing project*.
  - **Migration:** the project has any file that the Inventory step would find, even a single `README.md` or rules file. Follow *Migrating or upgrading an existing project*.
  - **New setup:** the project has none of these. Create the files from the templates in `templates/` (guidance: `templates/README.md`).
  - **Switch to the skill:** the KEEL skill is running, `KEEL.md` is in the root folder, and the developer asked to switch. Run the Upgrade path first if the stamp is older than the skill's version. Then set the stamp to the skill's version and, only on the developer's explicit instruction, delete `KEEL.md` or move it where the developer says. Report what changed.

  If the root folder also holds `AI-PROJECT-DOCS-STANDARD.md`, it is an older version of this standard: follow this skill, and tell the developer. When the upgrade is complete, ask the developer once whether to delete the old file; do not delete, move, or archive it without that answer. Tell the developer which path you chose and why before you continue. When the path is complete, offer the as-built review if the project has code.
- **As-built review:** If the project has code, offer this review after the setup, migration, or upgrade is complete and reported. The developer may decline or choose only some areas. On approval, follow these steps in order:
  1. **Feature inventory.** List the features the code implements, each with its entry points (routes, commands, screens, jobs, public modules) and folders. Show the list. The developer confirms, renames, merges, or drops items. Do not read deeper until the list is confirmed.
  2. **Area map.** Fill the area map in `ARCHITECTURE.md` for the confirmed areas: code, entry points, tests, command, dependencies (from imports). Set Confidence to Inferred on every row, and mark the table "Inferred from code, needs developer review".
  3. **One area at a time, with a budget.** Read 1 area, write or update its `ARCHITECTURE.md` content (stack, folders, commands, data model, operations), then stop and report before the next. Use a subagent per area where the tool allows, so the main context stays small. If an area exceeds the budget, set its Confidence to Low and record where reading stopped.
  4. **SPEC from behavior.** For each area, write feature text and acceptance criteria that describe what the code does now. If `SPEC.md` is empty or holds only the template, seed it and mark the content "Inferred from code, needs developer review". If `SPEC.md` has content, write the differences as PROPOSED blocks (see *Proposed changes to SPEC and DESIGN*). The same applies to `DESIGN.md`. Never change accepted SPEC or DESIGN text from code.
  5. **Differences and health.** Report what is built but not specified, what is specified but not built, superseded approaches still in the code, areas with no tests, secrets found, and dependencies with known issues. Lasting findings go to `RESEARCH.md`; questions go to `HANDOFF.md` under Waiting. Set the Verified date in `ARCHITECTURE.md`, and in `SPEC.md` once the developer has reviewed it.
  6. **Stop conditions.** Change no code. Do not run tests unless the developer asks.
- **Existing files:** Never overwrite a file or folder from this standard that already exists. Merge the new content in, or propose the change, and ask the developer first.
- **Missing information:** Before you create any file, ask the developer once, in 1 message, for: the tracker and ticket ID (or none); the project name and a short description; and whether the project has a UI. Never take the project name from the folder name. If the developer does not supply an item, leave its placeholder.
- **SPEC interview:** After you seed or migrate `SPEC.md`, offer to interview the developer about its gaps: edge cases, non-goals, trade-offs, constraints, glossary terms, and acceptance criteria. Ask a few questions at a time, and skip questions the docs already answer. Write the resulting SPEC changes as PROPOSED blocks for acceptance (rule 1). The developer may decline. If you offer an as-built review, offer the interview after it.

## Migrating or upgrading an existing project

Use this section when the project already has documentation: another format, a single notes file, or an older version of this standard. The other Initialization rules (existing files, missing information) still apply. Whatever the prompt, change nothing until the developer approves the plan in step 5. Change only documentation, never code, configuration, or dependencies; the docs check script is the one exception.

**Upgrade only:** If the project already follows an older version of this standard, do steps 1, 8, and 9. Step 8 says when to run other steps.

1. **Back up.** Confirm with the developer that a backup or version-control commit exists. If not, copy the existing documentation to a folder outside the project and tell the developer where it is.
2. **Inventory.** Scan the whole project, including subfolders, for `.md`, `.txt`, `.rst`, `.adoc`, and similar text files, plus `.docx` and `.pdf` files you can read. Include rules files (`CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`, `.github/instructions/`), decision records, test plans, QA or release checklists, user manuals or help pages, runbooks, wiki exports, TODO lists, changelogs, and release notes. Skip `docs/archive/` and dependency, build, and version-control folders (such as `node_modules`, `vendor`, `dist`, `bin`, `obj`, and `.git`). List any file you could not read and ask how to handle it.
3. **Resolve currency.** Group the inventory by topic. For each topic with two or more sources, find the current source. Use these signals, strongest first:
   1. A direct statement from the developer.
   2. An explicit marker: "superseded", "deprecated", "obsolete", "old", "replaced by", or a link from a newer file.
   3. Agreement with the current code (evidence only; code never changes SPEC or DESIGN by itself).
   4. Dates or version numbers in the content or the file name (such as `v2`, `final`, or `2025-03`).
   5. Version-control history, if it exists.

   Do not rely on file modification dates alone; copies and sync tools (such as OneDrive or SharePoint) change them. Give each file one status: **Current**, **Partly current** (list the current sections), or **Superseded** (name what replaced it). If the signals disagree or are weak, mark the topic **Unresolved**.
4. **Map.** Give each Current item, and each current section of a Partly current file, a target file and section (for example, "requirements in README → `docs/SPEC.md` Goals"). Superseded content gets no target; it stays in the archive. Flag content with no target, content that conflicts with this standard, and content you would have to infer. When a newer source changed a choice recorded in a Superseded file, propose 2 decision notes from the original wording: the old choice ("Superseded by NNNN") and the new one (Accepted). For evidence of the change, such as failed tests, propose a `docs/RESEARCH.md` entry with the old finding marked "Outdated (date)".
5. **Get approval.** Show the developer the inventory, the currency table below, the mapping, the proposed decision notes and research entries, and the draft archive index (step 7). Ask about every Unresolved topic and every Low-confidence row; do not guess. Wait for approval.

   | Topic | Sources | Current source | Evidence | Confidence |
   |---|---|---|---|---|
   | (Login method) | (`auth.md`, `auth-v2.md`, `new-login.md`) | (`new-login.md`) | (Matches the code; newest date) | (High / Medium / Low) |
6. **Migrate**, using the templates in `templates/` (guidance: `templates/README.md`):
   - Migrate only the content mapped in step 4. Reorganize its original wording; do not rewrite or drop it. Never invent content: if a section has no source, keep the heading and write "(Not documented yet.)" Mark content inferred from code "Inferred, needs developer review" in SPEC and DESIGN.
   - Give each acceptance criterion an ID, and create `RELEASE-CHECKLIST.md` with a matching check for each, carrying in existing test plans and release checklists.
   - Build the `ARCHITECTURE.md` area map from the existing code and tests, as its template says. If no command can run one area alone, write "(Full suite only)" and report it. Do not run the tests during the migration unless the developer asks. Write the docs check script and add its row.
   - Put user manuals or help content in `docs/USER-GUIDE.md`, and their images in `docs/images/`. Offer to convert the guide to Simplified Technical English. Put runbooks and operations notes in the `ARCHITECTURE.md` Operations section, or `docs/RUNBOOK.md` if they pass a page.
   - Copy decision records into `docs/decisions/` word for word, keeping their status (Accepted if none). Add the approved decision notes, using "(Not documented yet.)" for any part with no source, and number all notes together in date order. Link each approved research entry from its decision note.
   - Merge the rules files into `AGENTS.md`. Put project-specific rules under Conventions, Claude-only rules under Claude-only notes in `CLAUDE.md`, and Copilot-only rules under Copilot-only notes in `.github/copilot-instructions.md`. Report conflicts with this standard or between files. Then replace `CLAUDE.md` and `.github/copilot-instructions.md` with their templates, keeping those notes.
   - Move lasting content from handoff, session-note, or TODO files to its proper doc, and leftovers to `docs/HANDOFF.md` as dated bullets, with the routing printed.
   - Move changelogs and release notes to `docs/CHANGELOG.md`, newest first.
   - Update links to moved content. Point links to Superseded files at their replacements, not at the archive. Set the `AGENTS.md` version stamp to this skill's version.
7. **Archive.** Move the originals into `docs/archive/` under their original paths, so files with the same name do not collide (`notes/auth.md` becomes `docs/archive/notes/auth.md`). For files that keep their path, such as `README.md` and the rules files, save a copy there before editing. Create `docs/archive/INDEX.md` from its template, or add to it, with one row per archived file. Never delete the originals or the backup.
8. **Upgrade.** The version stamp is in `AGENTS.md` (in `CLAUDE.md` before 1.2.0). If it is older than this skill's version, apply only the changes since that version, in order, using the Changelog and the blocks below. Show the developer the planned changes and wait for approval, as in step 5. Then apply them and update the stamp.
   - **1.1.0 or earlier to 1.2.0:** Handle the rules files as in steps 6 and 7. Add the Session handoff section and the `docs/HANDOFF.md` Docs entry to `AGENTS.md`. Change `CLAUDE.md` references to `AGENTS.md` in `README.md` and the PLAN.md Definition of done. Do not create `docs/HANDOFF.md` unless the developer asks.
   - **1.2.0 to 1.3.0:** Propose acceptance-criterion IDs in `SPEC.md`, with test cases grouped by feature or milestone, then create `docs/RELEASE-CHECKLIST.md` with one check per ID. Add its Docs entry and the release-check Never rule to `AGENTS.md`, and the two new Definition of done lines to `PLAN.md`. If the project has end users, offer to create `docs/USER-GUIDE.md`.
   - **1.3.0 to 1.4.0:** Add the `docs/archive/` Docs entry and the two new Never rules to `AGENTS.md`. If `docs/archive/` exists, propose a `docs/archive/INDEX.md` with one row per file; ask the developer for any status you cannot tell. Do not move or rename files already in the archive. If current docs still have superseded copies beside them (such as `SPEC-v2.md`), run steps 3 to 7 for them.
   - **1.4.0 to 1.5.0:** In `AGENTS.md`, replace the template sections with their 1.5.0 versions (the Making changes and Testing sections are new, and most others are shorter), and keep the project's own lines, such as Conventions and the Skills list. Keep only the Docs entries for files that exist, plus the always-listed ones, and add the "Not used" line. Add the Testing lines, including How to run tests and the results file, to `ARCHITECTURE.md`, and build its test map from the existing tests as in step 6. Update the PLAN.md Definition of done and the release steps in `RELEASE-CHECKLIST.md`. Add `test-results/` to `.gitignore` if the project uses version control. Change Jira headers to `> Jira: PROJ-# (name of project)`. Add the compaction note to the Claude-only notes in `CLAUDE.md`. Propose cuts to `AGENTS.md` under rule 8, and wait for approval. Offer the SPEC interview, and propose the new SPEC template guidance as SPEC changes.
   - **1.5.0 to 1.5.1:** In `AGENTS.md`, add the 2 new Making changes lines and the new Never rule. Extend the evidence line in the PLAN.md Definition of done with the two docs lines.
   - **1.5.1 to 2.0.0:** The standard is now KEEL. New headings and template lines are structure: add them directly once the developer approves the plan, with "(Not documented yet.)" as content. Only changes to accepted SPEC or DESIGN text go through PROPOSED blocks. Headers keep their `> Jira:` form; the standard now accepts any tracker name.
     1. Root: during this version the root may hold `AI-PROJECT-DOCS-STANDARD.md` beside or instead of `KEEL.md`; follow `KEEL.md`. Set the stamp to `Aligned to KEEL 2.0.0 (https://github.com/DominusFL/keel)`. An existing stamp `Aligned to KEEL v2.0.0` is the same version in its earlier form: update it to the new form, and the `KEEL.md` line after it, the next time you edit `AGENTS.md`.
     2. `AGENTS.md`: replace every template section with its 2.0.0 version (all changed; Reporting and the precedence line are new; the cap is about 120 lines), keep the project's own lines, and add the Conventions lines for ask-before-touching paths and area owners. Propose cuts under rule 8 and wait for approval.
     3. `ARCHITECTURE.md`: convert the test map to the area map (add Code, Entry points, ACs, and Confidence; mark rows Inferred); add `Verified: (not yet verified)` under the header; add the Operations section with Known traps, the data lifecycle line, and the Testing lines for the docs check, the AC citation, and the results files; write the docs check script and add its row.
     4. `SPEC.md`: add `Verified: (not yet verified)`, the Glossary and Constraints headings, and the Area name on each feature group. Convert each proposed SPEC or DESIGN change waiting in the old `HANDOFF.md` Open questions into a PROPOSED block.
     5. `PLAN.md`: add the Definition of ready, replace the Definition of done, and convert Current / Next to the work board.
     6. `RELEASE-CHECKLIST.md`: replace the Release steps and the Result values.
     7. `README.md`: add Owners and support.
     8. `CLAUDE.md`: extend the compaction note.
     9. `HANDOFF.md`: run the close routine on it: route each item, move lasting gotchas to Known traps or `RESEARCH.md`, and rewrite it with the dated sections. If more than 1 developer works on the project, create `docs/handoff/<developer>.md` per developer and retire `docs/HANDOFF.md`.
     10. Offer the as-built review; it sets the Verified dates.
9. **Report** what moved where, what was inferred, which Superseded content was not migrated and what replaced it, what was left unmapped, and any conflicts. Also list, with file names, each superseded approach that the code still appears to use (possible dead code or an unfinished change). Run the Initialization checklist and mark any item that does not pass. Then offer the as-built review.

## Authority and file handling

When `KEEL.md` is in the project root, it is the authoritative reference for project structure, documentation standards, naming conventions, required, recommended, and optional artifacts, and templates and seed content, including for documentation created later. Direct developer instructions and explicit project-specific requirements override it. When project docs disagree with each other, the Precedence list in `AGENTS.md` says which one wins.

AI assistants may read and use the file, but must not delete, rename, move, modify, archive, or otherwise manage it without direct, explicit developer instruction. The developer controls its location and lifecycle, and may ask an AI assistant to update it.

When `KEEL.md` is absent and the KEEL skill is installed, the skill is the reference for the same things. When both are present, `KEEL.md` wins; if their versions differ, tell the developer before you continue.

## Folder layout

```
project/
├── KEEL.md                 (the standard as a file, or this skill in its place; retained at the developer's discretion)
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── .github/
│   └── copilot-instructions.md
├── .claude/                (optional)
│   └── skills/
│       └── <skill-name>/
│           └── SKILL.md
├── .env.example            (optional)
├── test-results/           (written by test runs; latest.md; excluded from version control)
└── docs/
    ├── SPEC.md
    ├── ARCHITECTURE.md
    ├── PLAN.md
    ├── RELEASE-CHECKLIST.md
    ├── decisions/             (recommended)
    ├── HANDOFF.md             (recommended; created when first needed)
    ├── handoff/               (teams only; one <developer>.md per developer, in place of HANDOFF.md)
    ├── plans/                 (optional; one M<n>.md per milestone when the work board grows)
    ├── CHANGELOG.md           (recommended; created at the first release)
    ├── DESIGN.md              (optional; required if the project has a UI)
    ├── DESIGN-GUIDE.html      (optional; required if the project has a UI)
    ├── USER-GUIDE.md          (optional; for projects with end users)
    ├── RUNBOOK.md             (optional; split from the ARCHITECTURE.md Operations section)
    ├── images/                (optional; screenshots and images for the docs)
    ├── MOCKUP.md              (optional)
    ├── RESEARCH.md            (optional)
    └── archive/               (optional; migration only)
        └── INDEX.md           (lists each archived file and its status)
```

The docs check script (see *Docs check and drift report*) lives where the project keeps its tests, or in `scripts/` if the project has no test folder.

## The documentation files

| # | File | Status | Purpose | Seeded from the ticket |
|---|---|---|---|---|
| 1 | `README.md` | Required | For humans: what the project is, how to run it, owners and support, links | Full description + link |
| 2 | `docs/SPEC.md` | Required | What and why: goals, users, glossary, features, user stories, constraints, acceptance criteria, non-goals | Requirements |
| 3 | `docs/ARCHITECTURE.md` | Required | How: stack, folders, commands, data model, APIs, auth, hosting, deployment, operations, testing, the area map, diagrams | Approach, deployment notes |
| 4 | `docs/PLAN.md` | Required | Execution: milestones, the work board, Definition of ready, Definition of done | Rarely |
| 5 | `AGENTS.md` | Required | AI working rules, precedence, and lists of the docs and skills, shared by all AI coding tools | n/a |
| 6 | `CLAUDE.md` | Required | Loads `AGENTS.md` into Claude Code with an import line, plus optional Claude-only notes | n/a |
| 7 | `.github/copilot-instructions.md` | Required | Points GitHub Copilot to `AGENTS.md` and its listed skills, plus optional Copilot-only notes | n/a |
| 8 | `docs/RELEASE-CHECKLIST.md` | Required | Release gate: one check per SPEC acceptance criterion, the non-test release steps, and the latest release result | n/a |
| - | `docs/decisions/` | Recommended | One short note per major decision, numbered in order. Create the folder with the first decision. | n/a |
| - | `docs/HANDOFF.md` | Recommended | Short handoff to the next session: next action, open items, traps. About 40 lines, dated bullets. Create it at the first session close, or earlier to record something important. | n/a |
| - | `docs/handoff/<developer>.md` | Teams only | One handoff per developer, same template and rules as `HANDOFF.md`. Used in place of `HANDOFF.md` when more than 1 developer works on the project. | n/a |
| - | `docs/CHANGELOG.md` | Recommended | Release history, newest first: what was added, changed, and fixed in each release. Create it at the first release. | n/a |
| - | `docs/plans/M<n>.md` | Optional | One work board per milestone, used when the board in `PLAN.md` passes about 15 open rows | n/a |
| - | `docs/DESIGN.md` | Optional (required if the project has a UI) | UI/UX: colors, type, spacing, components, layout, accessibility, wireframe links | UI/UX or design notes |
| - | `docs/DESIGN-GUIDE.html` | Optional (required if the project has a UI) | Human-readable, visual version of `DESIGN.md`, so graphic designers have an easy reference. Regenerated from `DESIGN.md` every time `DESIGN.md` changes; never edited by hand. | n/a |
| - | `docs/USER-GUIDE.md` | Optional (for projects with end users) | Task-based guide for the people who use the product but do not develop or maintain it | n/a |
| - | `docs/RUNBOOK.md` | Optional | Operations guide for support staff: services, logs, common failures and fixes, backups, contacts. Split from the `ARCHITECTURE.md` Operations section when it passes a page. | n/a |
| - | `docs/images/` | Optional | Screenshots and images used by the docs, such as the user guide | n/a |
| - | `docs/MOCKUP.md` | Optional | Mockup-only instructions, temporary sample data, and project-specific mockup decisions | n/a |
| - | `docs/RESEARCH.md` | Optional | Results of research and comparisons, including options not chosen, kept for later sessions | n/a |
| - | `docs/archive/` | Optional | Original documentation files moved by a migration, kept for history only, with `INDEX.md` giving each file's status. Never delete them, and never use them as a source of current information. | n/a |
| - | `.claude/skills/<skill-name>/SKILL.md` | Optional | Project-specific skills, one folder per skill | n/a |
| - | `.env.example` | Optional | Names of the required environment variables, with no real values. Required if the project uses environment variables. | n/a |

**Sections that do not apply:** Create every required file and keep all its headings. If a section does not apply, say why in the file. Example: the `ARCHITECTURE.md` Auth & security section says the project has no authentication.

**Files a developer removes:** A developer may decide not to use a file from this standard, even a required one. That decision overrides this standard. List each such file on the "Not used" line of the `AGENTS.md` Docs list. Never recreate a file on that line, and never report it as missing. If a file from this standard is missing and is not on that line, ask the developer once whether to recreate it, and record the answer there.

**Projects with no UI:** Do not create `DESIGN.md` or `DESIGN-GUIDE.html`, and leave them out of the `AGENTS.md` Docs list. If the project later gains a UI, create both from the templates.

**Projects with end users:** Create `USER-GUIDE.md` once end users have a working feature to use. Write it in ASD-STE100 Simplified Technical English (STE): short sentences, active voice, and approved words. Describe current behavior as tasks, and put screenshots in `docs/images/`.

**Projects with more than 1 developer:** Count developers, not tools: a solo developer who uses 2 AI tools is still 1 developer. The work board in `PLAN.md` holds the shared state: who holds which item, which files it touches, and its status. Each developer has a handoff file `docs/handoff/<developer>.md` (the developer's name in lowercase with no spaces, such as `rick.md`), rewritten only by that developer's sessions, and `docs/HANDOFF.md` is not used. The Handoff file line in `AGENTS.md` names the form the project uses. A board Owner is a developer name, with the tool after it when useful ("Rick / Claude Code").

Create other optional files only when needed, from their templates, and add them to the `AGENTS.md` Docs list.

**Research versus decisions:** Use `docs/RESEARCH.md` for research results or data that do not belong in the plan, specs, architecture, or decisions.

- **Decision note:** records *what* we chose and *why*, in a sentence or two. Example: "We chose A over B because it was faster." The AI must not reverse it.
- **Research entry:** records the *evidence* behind a choice, such as the actual test results for A and B. If A later fails, the entry shows whether B is a viable fallback. Research entries may be updated.

When a decision rests on research, the decision note links to the research entry.

**Acceptance criteria versus the release checklist:** `SPEC.md` defines correct behavior. Each acceptance criterion has an ID (`AC-1`, `AC-2`, and so on) and its test cases, grouped by feature or milestone, so development can test one part at a time. `RELEASE-CHECKLIST.md` proves a release meets all of them: one check per ID, plus non-test release steps such as updating the version and the docs (rule 6).

**Proposed changes to SPEC and DESIGN:** The AI never edits accepted text in `SPEC.md` or `DESIGN.md` (rule 1). It writes each proposal in the file, next to the text it changes, as a PROPOSED block, never only in chat:

```md
> PROPOSED 2026-10-31 (Claude Code): change AC-3 to allow an empty email.
> Reason: the form now has a guest path. Code: src/forms/signup.js.
```

A PROPOSED block is not a requirement and not a design. The developer accepts it by applying the edit and deleting the marker, rejects it by deleting the block, or tells the AI to do either. A block is named by its file and the AC ID or heading it changes (`SPEC.md AC-3`). The AI lists pending blocks in its task summary and, at the next close, in `HANDOFF.md` under Waiting. No block may remain at a release (rule 6).

**Session handoff versus lasting records:** `docs/HANDOFF.md` is a short, temporary handoff between sessions, tools, or developers, not a general record of what the AI remembers. Before writing to it, the AI routes each item to its proper home and prints the routing (rule 5):

| Content | Goes in |
|---|---|
| A choice and why it was made | `docs/decisions/` |
| Test results, options compared, fallbacks | `docs/RESEARCH.md` |
| Milestones and milestone-level next work | `docs/PLAN.md` |
| Commands, structure, stack, lasting traps | `docs/ARCHITECTURE.md` |
| Release check results | `docs/RELEASE-CHECKLIST.md` |
| Requirement or UI changes | PROPOSED block in `SPEC.md` or `DESIGN.md`; listed in `HANDOFF.md` under Waiting until accepted |

Only leftovers go in `HANDOFF.md`: the immediate next action, questions waiting on a person, unconfirmed assumptions, decisions made without asking, and traps found this session that have not yet moved. It never overrides the other docs. The same routing table sits at the top of the `HANDOFF.md` template, so the AI sees it each time it edits the file.

**AI instruction files:** `AGENTS.md` is a shared format that many AI coding tools read, including Claude Code and GitHub Copilot. It holds all the AI working rules, so a project keeps working as tools change. The other two files only point to it, plus optional notes for their own tool. Do not copy rules from `AGENTS.md` into either one.

- `CLAUDE.md` starts with the line `@AGENTS.md`, which imports `AGENTS.md` into Claude Code. The import works in every current Claude Code setup, including sessions that cannot read `AGENTS.md` directly, and never loads the rules twice. Do not replace it with a symbolic link (links need extra permissions on Windows).
- `.github/copilot-instructions.md` points GitHub Copilot to `AGENTS.md` for setups that do not read `AGENTS.md` directly. Only GitHub Copilot reads it; *Microsoft Copilot* and *Microsoft 365 Copilot* do not. Note the leading dot in `.github`, and use the exact file name. It needs no GitHub repository or version control. Create it even if you only use Claude Code, so others can use GitHub Copilot with the same rules.

## Project skills

Skills specific to one project live with that project, not in a developer's personal `~/.claude/skills/` folder, where they would apply to every project on that machine.

- **Location:** `.claude/skills/<skill-name>/SKILL.md`, one folder per skill. Create `.claude/skills/` if it does not exist (note the leading dot).
- **Naming:** Name the file exactly `SKILL.md`. The folder name must match the `name:` line inside it.
- **Using a skill:** Claude Code or GitHub Copilot can pick one up automatically when it is relevant, or a developer can call it by typing `/<skill-name>`.
- **Listing:** When you add, rename, or remove a skill, update the Skills list in `AGENTS.md`. Some tools do not scan `.claude/skills/` on their own, so that list points them there.

Starting point for a new skill:

```md
---
name: <skill-name>
description: One sentence on what it does and when to use it.
---

# Skill Name
Instructions for the AI go here.
```

## Linking to the project tracker

Most projects have a ticket, work item, or issue in a tracker such as Jira, Azure DevOps, GitHub Issues, or Linear, with a description of the project. Where the table lists a "Seeded from the ticket" section, copy ("seed") the file's first draft from the matching part of that description (for example, a Requirements or Approach section). Which tracker, and what its sections are called, is the project's choice; this standard does not depend on any product.

- `README.md` and every Markdown file in `docs/`, except decision notes and files in `docs/archive/`, start with a header line that names the tracker and the ticket: `> Tracker: TICKET-# (name of project)`, with the tracker's name in place of `Tracker` and the ticket ID in place of `TICKET-#`, for example `> Jira: BOOK-12 (Booking Portal)` or `> GitHub: #42 (Booking Portal)`. The README also links to the ticket and starts with the full ticket description. Projects set up under 1.x keep their `> Jira:` headers; they already follow this form.
- Include the ticket ID in the names of work items and in any notes or messages about the work. Decision notes carry no ticket ID.
- If no ticket ID has been assigned yet, leave the `TICKET-#` placeholder. The developer fills it in later, or gives it to the AI to replace every placeholder.
- If the project has no tracker, replace each header with `> Project: (name of project)`, omit the ticket link and ticket IDs, and ask the developer for a project description to use instead.

## Risk classes

Every change gets 1 class before work starts. The class is defined here once; rules 6, 9, and 10 and the `AGENTS.md` template cite it instead of repeating it. The AI names the class in the ready card or the task summary, so the developer can correct it.

| Class | Trigger | Tests (rule 9) | Review (rule 6) | Plan (rule 10) |
|---|---|---|---|---|
| **Small** | 1 area, no shared code, no ask-before-touching path | Targeted | None | Direct; a ready card if the change touches several files or its approach is unclear |
| **Shared** | Shared code (such as core utilities), the data model, auth, build configuration, a dependency upgrade, a refactor across areas, or a path on the ask-before-touching line in `AGENTS.md` | Affected; ask before a full regression | Fresh-context review of the diff against the acceptance criteria, before the task is done | Ready card, approved first |
| **Release** | A release | Full regression | Fresh-context review and drift report | Release checklist |

## Rules

1. **Humans own SPEC and DESIGN (when it exists),** including the acceptance criteria and their IDs. After the first draft is seeded at setup, the AI may only *propose* edits, as PROPOSED blocks in the file, and must wait for acceptance. Otherwise requirements quietly drift to match whatever the code does.
2. **The AI keeps the docs current.** Every time the application changes, the AI updates the affected files in place, in the same task, not afterward. To find them, it searches `docs/` for each path, name, label, and behavior it changed; the area map and the Glossary give the names. It writes SPEC and DESIGN edits as PROPOSED blocks in the same task, never skips them silently, and never defers doc updates to `HANDOFF.md`. Never create a new version of a doc (such as `SPEC-v2.md`) beside the old one; that leaves several conflicting versions. To change a decision, follow rule 3. How to handle each file:
   - **Update directly:** ARCHITECTURE (including the area map), PLAN (including the work board), the `AGENTS.md` Docs and Skills lists, `.env.example` (when environment variables change), and, when used, MOCKUP, RESEARCH, RUNBOOK, and USER-GUIDE (current user-facing behavior only).
   - **Propose:** SPEC and DESIGN, as PROPOSED blocks (rule 1).
   - **Regenerate:** `DESIGN-GUIDE.html` (when used) every time `DESIGN.md` changes.
   - **`RELEASE-CHECKLIST.md`:** keep one check per accepted acceptance criterion; record results only by running the checks (rule 6).
   - **`HANDOFF.md`** (when used): rewrite at session close through the close routine, or to record something important right away (rule 5), not after every change.
   - **`CHANGELOG.md`** (when used): add one entry at the top at each release (rule 6). Do not rewrite old entries.
3. **Decisions are never rewritten.** To change one, write a new note that supersedes it, then mark the old note's Status as Superseded (the only edit allowed). If 2 notes get the same number, the later merge renumbers its note and fixes the Superseded references.
4. **A task is not done until it meets the Definition of done in PLAN.md.** Test the task as rule 9 says; a task does not need a full regression unless rule 9 calls for one. The result must match the ready card, when there was one; anything outside the card is reported, not done.
5. **The session handoff is not a record.** Run the close routine when the developer says the session is closing, before any compact or clear (for example, `/compact` or `/clear`), or when the session has used most of its context:
   1. **Route.** For each item worth keeping, print 1 line: `item -> target doc`, or `item -> HANDOFF (Next | Waiting | Assumed | Decided | Trap)`. Use the routing table.
   2. **Write** the routed items into their docs (PROPOSED blocks for SPEC and DESIGN).
   3. **Rewrite** `HANDOFF.md` (never append) with only what step 1 routed there, and print the line count.

   A close with no routing report is incomplete. `HANDOFF.md` stays under about 40 lines. Every bullet is dated; an item older than 1 session is moved or deleted, never copied forward, and a lasting fact never stays more than 1 session. After a close at the context limit, tell the developer to start a new session from `HANDOFF.md`; do not continue on a compacted context. If something important would be lost sooner, record it right away in its proper doc or in `HANDOFF.md`, creating the file if needed. On a team, each developer's `docs/handoff/<developer>.md` follows the same rules.
6. **A release is not approved until the release checklist passes.** Before every release, in this order:
   1. A reviewer in a fresh context (a new session or a subagent, not the one that wrote the code) checks the code against the SPEC acceptance criteria, runs each command in `README.md` Run it and `ARCHITECTURE.md` Commands, and reads `README.md` and `USER-GUIDE.md` (if used) against the code. It reports only gaps that affect correctness, the requirements, or the docs. Fix each gap or list it for the developer.
   2. Write the drift report (see *Docs check and drift report*). The developer fixes or accepts each finding.
   3. Run a full regression (rule 9): the whole test suite, the docs check, and every check in `RELEASE-CHECKLIST.md`. Never mark a check passed without running it.
   4. Confirm that no PROPOSED block remains in `SPEC.md` or `DESIGN.md`. Review new or upgraded dependencies (license, maintenance, known vulnerabilities).
   5. Record how each check was verified, replace the Latest release section with the result, set the Verified date in `SPEC.md` and `ARCHITECTURE.md`, and add the release entry to `CHANGELOG.md` (create the file at the first release).
   6. A human gives the final approval.
7. **Never put secrets in code or docs.** If the project uses environment variables, list their names in `.env.example`. Do not paste secrets or customer data into docs or the tracker. If the project uses version control, make sure `.gitignore` excludes `.env` and the `test-results/` folder (rule 9), creating or updating it if needed. This is the only version-control step this standard covers.
8. **Keep docs skimmable.** Keep `AGENTS.md` under about 120 lines, because the AI loads it every session; the template is a maximum, so delete the optional lines that do not apply and list only the docs that exist. Keep `CLAUDE.md` and `copilot-instructions.md` to a few lines, and `HANDOFF.md` under about 40. Other docs have no line limit: if one is too long to skim, trim it or split it by topic, leaving a link in the original. `RESEARCH.md` grows by design; split it by topic if it becomes unwieldy. In `AGENTS.md`, for each line, ask whether removing it would cause mistakes; if not, cut it. Do not include what the AI can learn from the code or already does by default. Mark at most 1 or 2 lines "IMPORTANT"; if many lines are marked, none stands out. If the AI keeps breaking a rule, or asks a question that `AGENTS.md` already answers, flag to the developer that the file may be too long or unclear.
9. **Test progressively.** Run only the tests a change needs, as the risk class says. The area map in `ARCHITECTURE.md` lists each area, its code, its tests, its command, its acceptance criteria, and the areas it depends on. Read the map before you read code, and read only the code of the areas you change. An area that a change does not touch is not tested again; its last passing result still holds.
   - **Targeted (the default):** new and updated tests, plus the existing tests for the changed area, plus the docs check.
   - **Affected:** targeted, plus the tests for each area that uses the changed code. Run them for a Shared change. If a targeted test fails in a way that points outside the changed area, run the affected areas without asking.
   - **Full regression:** the whole test suite, the docs check, and every release check. Run it before every release (rule 6) and when the developer asks. For any other reason, ask the developer first and explain why; a Shared change with a wide reach is the typical reason.
   - **Scripted first:** run the saved test commands from the area map. Each run writes a short results file, `test-results/latest.md`: what ran, the pass and fail counts, and details for failures only. The docs check writes `test-results/docs.md` instead, so both results survive the same task. Attach screenshots only for failures or visual checks. Check the exit code and the counts, not only a "passed" line. Test interactively only to debug a failure, to explore a new check before you script it, or for visual checks.
   - **Saved scripts only:** use the project's test framework when it has one. Save each new test script in the project and add its command to the area map. Each test names the acceptance criterion it covers (`AC-n`) in its name or a comment. Do not write throwaway test scripts.
10. **Plan before code.** Classify the change (Risk classes). For a Shared change, a change that touches several files, or a change whose approach is unclear, write the ready card from the `PLAN.md` Definition of ready and wait for approval. Approval of the card approves the plan; its PROPOSED blocks still need acceptance, which the developer may give at the same time. A Small change with a clear approach goes ahead directly. Before a bug fix, reproduce the bug with a failing test or captured error output and save the test; no repro, no fix: ask. Never guess a version pin; read the lock file or ask. If the same fix fails twice, stop, report what you tried, and ask.
11. **Every claim carries evidence.** End every task with the task summary from the `PLAN.md` Definition of done, every line present ("none" if empty); the `AGENTS.md` Reporting section points to it. A test passed only if the results file shows it. A check the AI could not run is reported as "Not run: reason", never as passed. A Shared change is not done until its fresh-context review ran and its findings are fixed or listed. Never weaken, skip, or delete a test to make it pass; report the failure and its cause. After 3 test-fix rounds, stop and report. To dismiss a review finding, cite the file and line that shows it is wrong. Before reporting a task done, re-read the Definition of done and the ready card; this is the cheapest defense against a long context.

## Docs check and drift report

**Docs check** is a saved script in the project's own language, with no new runtime or dependency. It is the one script this standard asks for. It is listed in the area map as area *Docs* and runs with the targeted tests of every change; a red check is a failing test. The AI writes it at setup or upgrade and keeps the list of checks, with these definitions, in the script's header comment, so the list survives without this skill. It writes its results to `test-results/docs.md`, so the area test results in `test-results/latest.md` survive the same task. It checks:

1. `AGENTS.md` is under about 120 lines and has the version stamp.
2. `docs/HANDOFF.md` and each `docs/handoff/*.md` is under about 40 lines, and every bullet starts with a date.
3. Every `AC-n` in `SPEC.md` outside PROPOSED blocks (lines that start with `>`) has a row in `RELEASE-CHECKLIST.md`, and every row has such an AC.
4. Every relative path and link in `README.md` and `docs/` exists. For every command in the area map and in `ARCHITECTURE.md` Commands, the script file or first word it names exists; the check does not run it.
5. Every file in `docs/` is listed in `AGENTS.md` or on its Not used line (contents of `docs/decisions/`, `docs/images/`, `docs/plans/`, `docs/handoff/`, and `docs/archive/` are covered by their folder's entry).
6. Every doc, except decision notes and `docs/archive/`, starts with a header line of the form `> Name: text`.
7. No file in `docs/` has a standard doc name plus a suffix such as `-v2`, `-old`, `-new`, `-copy`, or `-final`.
8. PROPOSED blocks older than 14 days are listed (a warning, not a failure).
9. No assignment-shaped secret in docs: `password`, `secret`, `api_key`, or `token`, followed by `=` or `:` and a value, or a private key header.

**Drift report** is a read-only report the AI writes before every release (rule 6) and whenever the developer asks ("run a drift report"). It never blocks and changes nothing. Each finding carries a certainty, and findings are never averaged:

| Finding | Certainty | How found |
|---|---|---|
| A SPEC feature or AC with no code behind it | Evidence | Area map ACs column against the code |
| Code with no SPEC coverage | Evidence | Folders not in any area map row, or rows with no ACs |
| An AC with no test, or a test with no AC | Certain | Area map ACs column against tests that cite `AC-n` in a name or comment |
| A command, folder, file, or link in the docs that does not exist | Certain | The docs check (paths, links, commands); the reviewer for anything else |
| A doc section older than the code it describes | Inference | The Verified date against the change history: version-control history if any; else the work board Started dates and `CHANGELOG.md`; else "Not run: no change history". Compares dates, not behavior. |

The report goes in the task summary. Lasting findings go to `RESEARCH.md`. At a release, each finding is fixed or accepted by the developer.

---

This skill is generated from `KEEL.md` in https://github.com/DominusFL/keel. Do not edit it by hand; change `KEEL.md` and run `python3 build/build.py`.
