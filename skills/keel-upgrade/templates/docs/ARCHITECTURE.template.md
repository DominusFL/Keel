> Tracker: TICKET-# (name of project)
Verified: YYYY-MM-DD (last as-built review or release; the only date to trust)

## Stack
## Folder layout
## Commands
(Build, run, test, and lint commands added during development. Commands from the ticket stay in README.md.)
## Data model & APIs
(Include migrations, personal data, and retention, or say the project has none.)
## Auth & security
## Hosting & deployment
## Operations
(Logging, error handling, backups and retention, monitoring, and what to do when it fails. Split to docs/RUNBOOK.md when this passes a page.)
### Known traps
(Lasting surprises and workarounds, moved here from HANDOFF.md: what, why, and how to avoid it.)
## Testing
- What must be tested: (e.g., business logic, API endpoints, key user flows)
- Tools: (e.g., the project's test framework; a saved script only if there is no framework)
- Minimum bar: (e.g., new code ships with tests; targeted tests and the docs check pass for each change; a full regression passes before each release)
- How to run tests: run the saved commands from the area map. Save each new test script in the project and add its command to the map; no throwaway scripts. Each test names the acceptance criterion it covers (AC-n) in its name or a comment. Test interactively only to debug a failure, to explore a new check before you script it, or for visual checks.
- Results file: `test-results/latest.md`. Each saved command writes it itself, so every run produces it. Each run overwrites it with what ran, the pass and fail counts, and details for failures only. Attach screenshots only for failures or visual checks. Check the exit code and the counts, not only a "passed" line.
- Docs check: (`...`). The list of checks is in the script's header comment. Runs with every change; writes `test-results/docs.md`.
- Full regression command: (`...`)
### Area map
(One row per area. Use the feature groups from SPEC.md as the areas. Read this map before you read code, and read only the areas you change. Update the map when code, tests, or areas change. Confidence: High = the developer reviewed the row; Inferred = from code, not yet reviewed; Low = incomplete read, and the row says where reading stopped.)
| Area | Code (folders or files) | Entry points | Tests | Command (this area only) | ACs | Depends on | Confidence |
|---|---|---|---|---|---|---|---|
| (Login) | (src/auth/) | (src/auth/login.js) | (tests/login.test.js) | (`npm test -- login`) | (AC-1, AC-2) | (Data model, Auth) | (High) |
| Docs | (scripts/check-docs.js) | | | (`node scripts/check-docs.js`) | | | High |
## Links to diagrams
