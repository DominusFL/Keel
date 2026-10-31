# KEEL 2.0.0: starter templates

Generated from `KEEL.md` (https://github.com/DominusFL/keel). Do not edit by hand. Each template is a file in this folder at the path it takes in the project, with `.template` before its extension: copy `docs/SPEC.template.md` to `docs/SPEC.md`.

Copy these into each new project. Replace the placeholders (`Tracker`, `TICKET-#`, name, and web link if available), and follow or delete the guidance in parentheses. The `AGENTS.md` template is a maximum: at setup, delete the optional lines that do not apply (teams, area owners, `docs/plans/`, `RUNBOOK`), and in its Docs list keep only the files that exist in the project, plus `docs/decisions/`, `docs/RESEARCH.md`, `docs/HANDOFF.md`, and `docs/CHANGELOG.md`, which stay listed even before they exist so the AI knows to create and use them. Keep the "Not used" line, with "(none)" until the developer removes a file.

## `README.md`

Template: `templates/README.template.md`

## `docs/SPEC.md`

Template: `templates/docs/SPEC.template.md`

## `docs/ARCHITECTURE.md`

Template: `templates/docs/ARCHITECTURE.template.md`

## `docs/PLAN.md`

Template: `templates/docs/PLAN.template.md`

## `AGENTS.md`

Template: `templates/AGENTS.template.md`

## `CLAUDE.md`

Template: `templates/CLAUDE.template.md`

Keep the `@AGENTS.md` line first and on its own line. Do not copy rules from `AGENTS.md` into this file. A session-start hook that prints `docs/HANDOFF.md` is allowed as a Claude-only convenience; the rules do not depend on it.

## `.github/copilot-instructions.md`

Template: `templates/.github/copilot-instructions.template.md`

Keep the pointer lines first. Do not copy rules from `AGENTS.md` into this file.

## `docs/decisions/0001-short-title.md` *(recommended; create when the first decision is recorded)*

Template: `templates/docs/decisions/0001-short-title.template.md`

## `docs/RELEASE-CHECKLIST.md`

Template: `templates/docs/RELEASE-CHECKLIST.template.md`

The release gate. Create it at setup with one check per acceptance criterion in `SPEC.md`, and keep it in step as the criteria change. Before each release, have a fresh-context review against the acceptance criteria and the docs, write the drift report, run a full regression, including every check, and replace the Latest release section. Example prompt: *"Prepare release 1.0: run the release checklist and record the results."*

## `docs/HANDOFF.md` *(recommended; create when first needed)*

Template: `templates/docs/HANDOFF.template.md`

A short session handoff so the next session (same tool, a different tool, or a different developer) can pick up without guessing. It is not created at initialization. Create it at the first session close, or earlier if something important must be recorded right away. Every bullet is dated, and the file stays under about 40 lines. Example closing prompt: *"I'm closing this session. Run the close routine: route each item, write it to its doc, then rewrite docs/HANDOFF.md."* On a team, each developer keeps `docs/handoff/<developer>.md` from the same template, and `docs/HANDOFF.md` is not used.

## `docs/plans/M<n>.md` *(optional; create when the work board in `PLAN.md` passes about 15 open rows)*

Template: `templates/docs/plans/M-n.template.md`

## `docs/CHANGELOG.md` *(recommended; create at the first release)*

Template: `templates/docs/CHANGELOG.template.md`

The release history, for testers, support staff, and other readers. It is not created at initialization. At each release, add one entry at the top, so the AI reads only the newest entries. Keep each entry short. Do not rewrite old entries.

## `docs/DESIGN.md` *(optional; required if the project has a UI)*

Template: `templates/docs/DESIGN.template.md`

Create this file for every project with a UI. Skip it for a project with no UI. The AI proposes changes as PROPOSED blocks (rule 1).

`docs/DESIGN-GUIDE.html` has no template. It is a human-readable, visual version of `DESIGN.md`, so graphic designers have an easy reference. Regenerate it from `DESIGN.md` every time `DESIGN.md` changes, in the same task. Never edit it by hand. Make it one self-contained HTML file that opens in a browser with no other files or build step. Follow the `DESIGN.md` headings, and show the values visually, such as color swatches, type samples, and spacing examples. Start it with a comment saying it is generated from `DESIGN.md` and must not be edited by hand.

## `docs/USER-GUIDE.md` *(optional; for projects with end users)*

Template: `templates/docs/USER-GUIDE.template.md`

Create this file once the product has a working feature that end users will use. End users are people who use the product but do not develop or maintain it. Write it for them, not for developers, in ASD-STE100 Simplified Technical English (STE): short sentences, active voice, one instruction per step, and approved words. Use the terms from the SPEC Glossary. Describe how the product works now, not planned features. Put screenshots in `docs/images/` and link them with relative paths.

## `docs/RUNBOOK.md` *(optional; create when the `ARCHITECTURE.md` Operations section passes a page)*

Template: `templates/docs/RUNBOOK.template.md`

For the people who run and support the product. Move the Operations content here and leave a link in `ARCHITECTURE.md`. Update it directly when operations change.

## `docs/MOCKUP.md` *(optional)*

Template: `templates/docs/MOCKUP.template.md`

Create this file only when the project will include mockups or prototypes. Use it for mockup guidance, temporary sample data, and mockup-specific decisions that do not belong in the production requirements or design documents.

## `docs/RESEARCH.md` *(optional)*

Template: `templates/docs/RESEARCH.template.md`

Create this file only when development produces research results or data that do not belong in the plan, specs, architecture, or decisions. Record research worth keeping for a future session, such as options tried but not chosen, and lasting findings from the as-built review or a drift report. Skip trivial lookups. Record the choice itself in `docs/decisions/`, and keep the supporting results here.

## `docs/archive/INDEX.md` *(optional; create during migration)*

Template: `templates/docs/archive/INDEX.template.md`

Lists every file moved into `docs/archive/` and what replaced it, so no session mistakes an old file for a current one. If the index already exists, add new rows to it.
