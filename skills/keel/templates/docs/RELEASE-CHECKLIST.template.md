> Tracker: TICKET-# (name of project)

# Release checklist
Never mark a check passed without running it. Record how each one was verified. A human gives the final approval.

## Requirement checks
(One line per acceptance criterion in SPEC.md. Method: automated test, manual check, or both. For automated checks, the results file from the full regression is the evidence.)
| ID | Check | Method | Result |
|---|---|---|---|
| AC-1 | (Short description from SPEC.md) | (Automated / Manual) | (Pass / Fail / Not run: reason) |

## Release steps
- [ ] Fresh-context review done: code against the SPEC acceptance criteria, each command in README Run it and ARCHITECTURE Commands run, README and USER-GUIDE read against the code; each gap fixed or accepted by the developer
- [ ] Drift report written (SPEC with no code: Evidence; code with no SPEC: Evidence; AC with no test or test with no AC: Certain; broken path, link, or command: Certain; doc older than its code: Inference); each finding fixed or accepted by the developer
- [ ] Full regression passes: the whole test suite and the docs check, using the full regression command in ARCHITECTURE.md (results in test-results/latest.md and test-results/docs.md)
- [ ] No PROPOSED blocks remain in SPEC.md or DESIGN.md
- [ ] New or upgraded dependencies reviewed: license, maintenance, known vulnerabilities
- [ ] CHANGELOG.md has an entry for this release (create the file at the first release)
- [ ] Version number updated (if the project uses one)
- [ ] README.md, ARCHITECTURE.md, and USER-GUIDE.md (if used) match the release; Verified dates set in SPEC.md and ARCHITECTURE.md
- [ ] DESIGN-GUIDE.html regenerated if DESIGN.md changed
- [ ] .env.example is current; no secrets or customer data in code or docs
- [ ] Open items in the handoff file(s) resolved or accepted for this release
- [ ] (Project-specific steps, such as deployment or accessibility checks)

## Latest release
(Replaced at each release.)
- Release: (version), YYYY-MM-DD
- Checked by: (tool or developer)
- Result: (All checks passed, or each failed, not-run, or skipped check and why)
- Approved by: (developer name)
