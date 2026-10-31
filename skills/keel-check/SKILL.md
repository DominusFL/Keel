---
name: keel-check
description: "KEEL 2.0.0 docs check and drift report. Writes or runs the project's docs check script (AGENTS.md size and stamp, handoff size, AC coverage in the release checklist, broken paths and links, unlisted docs, headers, stray doc versions, stale PROPOSED blocks, secrets) and writes the read-only drift report (SPEC with no code, code with no SPEC, ACs with no test, stale doc sections). Use in a KEEL project when the developer runs keel-check (/keel:keel-check or /keel-check), says 'run the docs check', 'run a drift report', or before a release."
argument-hint: "[docs | drift | both]"
metadata:
  version: "2.0.0"
  source: "https://github.com/rickflashman/keel"
---
# KEEL 2.0.0: docs check and drift report

Run the 2 documentation checks of KEEL version 2.0.0 (October 31, 2026), https://github.com/rickflashman/keel. Both are defined below.

If the developer gave instructions with the command, follow them: $ARGUMENTS

## Steps

1. **Confirm the project uses KEEL.** `AGENTS.md` has an `Aligned to KEEL` stamp (or an older *AI-PROJECT-DOCS-STANDARD* stamp). If not, stop and tell the developer to run `keel` first.
2. **Docs check.** Find the script in the area map row *Docs* in `docs/ARCHITECTURE.md`. If it does not exist, write it as the definition below says (the project's own language, no new dependency, the list of checks in its header comment, results to `test-results/docs.md`), add its row to the area map and its command to the Testing section, then run it. If it exists, run it and compare its header comment with the list below; propose any missing check to the developer before you add it. Report the result from `test-results/docs.md`, with the exit code. Never weaken a check to make it pass.
3. **Drift report.** Write it as the definition below says: each finding with its certainty, never averaged. It changes nothing. Put it in the task summary; lasting findings go to `docs/RESEARCH.md` (create it from the standard if needed).
4. **Report** with the task summary from the `docs/PLAN.md` Definition of done. A check you could not run is "Not run: reason", never passed.

When the developer asked for only 1 of the 2 checks, do that one. Before a release, both run (rule 6 in `references/standard.md`).

## Docs check and drift report

**Docs check** is a saved script in the project's own language, with no new runtime or dependency. When the project has no language yet, check which runtimes are installed on the developer's machine and use one of them; if none fits, write a shell script (`sh` on macOS and Linux, PowerShell on Windows). Port the script when the stack is chosen, and record that in `ARCHITECTURE.md`. It is the one script this standard asks for. It is listed in the area map as area *Docs* and runs with the targeted tests of every change; a red check is a failing test. The AI writes it at setup or upgrade and keeps the list of checks, with these definitions, in the script's header comment, so the list survives without this skill. It writes its results to `test-results/docs.md`, so the area test results in `test-results/latest.md` survive the same task. It checks:

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

This skill is generated from `KEEL.md` in https://github.com/rickflashman/keel. Do not edit it by hand; change `KEEL.md` and run `python3 build/build.py`.
