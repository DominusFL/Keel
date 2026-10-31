# KEEL 2.0.0: starter templates

Generated from `KEEL.md` (https://github.com/rickflashman/keel). Do not edit by hand. Each template is a file in this folder at the path it takes in the project, with `.template` before its extension: copy `docs/SPEC.template.md` to `docs/SPEC.md`.

Copy these into each new project. Replace the placeholders (`Tracker`, `TICKET-#`, name, and web link if available), and follow or delete the guidance in parentheses. The `AGENTS.md` template is a maximum: at setup, delete the optional lines that do not apply (teams, area owners, `docs/plans/`, `RUNBOOK`), and in its Docs list keep only the files that exist in the project, plus `docs/decisions/`, `docs/RESEARCH.md`, `docs/HANDOFF.md`, and `docs/CHANGELOG.md`, which stay listed even before they exist so the AI knows to create and use them. Keep the "Not used" line, with "(none)" until the developer removes a file.

## `docs/ARCHITECTURE.md`

Template: `templates/docs/ARCHITECTURE.template.md`

## `docs/RESEARCH.md` *(optional)*

Template: `templates/docs/RESEARCH.template.md`

Create this file only when development produces research results or data that do not belong in the plan, specs, architecture, or decisions. Record research worth keeping for a future session, such as options tried but not chosen, and lasting findings from the as-built review or a drift report. Skip trivial lookups. Record the choice itself in `docs/decisions/`, and keep the supporting results here.
