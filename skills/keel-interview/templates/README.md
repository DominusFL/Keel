# KEEL 2.0.0: starter templates

Generated from `KEEL.md` (https://github.com/rickflashman/keel). Do not edit by hand. Each template is a file in this folder at the path it takes in the project, with `.template` before its extension: copy `docs/SPEC.template.md` to `docs/SPEC.md`.

Copy these into each new project. Replace the placeholders (`Tracker`, `TICKET-#`, name, and web link if available), and follow or delete the guidance in parentheses. The `AGENTS.md` template is a maximum: at setup, delete the optional lines that do not apply (teams, area owners, `docs/plans/`, `RUNBOOK`), and in its Docs list keep only the files that exist in the project, plus `docs/decisions/`, `docs/RESEARCH.md`, `docs/HANDOFF.md`, and `docs/CHANGELOG.md`, which stay listed even before they exist so the AI knows to create and use them. Keep the "Not used" line, with "(none)" until the developer removes a file.

## `docs/SPEC.md`

Template: `templates/docs/SPEC.template.md`

## `docs/RELEASE-CHECKLIST.md`

Template: `templates/docs/RELEASE-CHECKLIST.template.md`

The release gate. Create it at setup with one check per acceptance criterion in `SPEC.md`, and keep it in step as the criteria change. Before each release, have a fresh-context review against the acceptance criteria and the docs, write the drift report, run a full regression, including every check, and replace the Latest release section. Example prompt: *"Prepare release 1.0: run the release checklist and record the results."*

## `docs/HANDOFF.md` *(recommended; create when first needed)*

Template: `templates/docs/HANDOFF.template.md`

A short session handoff so the next session (same tool, a different tool, or a different developer) can pick up without guessing. It is not created at initialization. Create it at the first session close, or earlier if something important must be recorded right away. Every bullet is dated, and the file stays under about 40 lines. Example closing prompt: *"I'm closing this session. Run the close routine: route each item, write it to its doc, then rewrite docs/HANDOFF.md."* On a team, each developer keeps `docs/handoff/<developer>.md` from the same template, and `docs/HANDOFF.md` is not used.
