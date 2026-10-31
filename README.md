# KEEL

A documentation and working standard for AI-developed projects. Like the keel of a ship, it keeps a project steady and on course when the AI tool, the AI model, or the developer changes.

The standard is `KEEL.md`. Read it for the full text. It comes in 2 forms with the same version:

| Form | How it works | Best for |
|---|---|---|
| **File** | Put `KEEL.md` in the project root and tell the AI: *"Read KEEL.md and do what it says."* | A single project, or a team that wants the standard in the repository |
| **Skill** | Install the 6 KEEL skills once at user level. They work in every project without the file. | A developer who applies KEEL to many projects and wants updates from this repository |

A project can switch from the file to the skill at any time (see *Switch to the skill* in `KEEL.md`).

## The skills

| Skill | Task |
|---|---|
| `keel` | General: looks at the project, chooses the path (new setup, migration, upgrade, or switch), and does it |
| `keel-init` | New setup from the templates, for a project with no docs yet |
| `keel-upgrade` | Migrate existing docs, upgrade an older KEEL version, or switch a `KEEL.md` project to the skill |
| `keel-check` | Write or run the docs check script, and write a drift report |
| `keel-as-built` | The as-built review of existing code: area map, SPEC from code, differences and health |
| `keel-interview` | The SPEC interview: fill the gaps in `SPEC.md` as PROPOSED blocks |

`keel`, `keel-init`, and `keel-upgrade` run only when you call them, because they create or change many files. The other 3 may also start on their own in a KEEL project when a request matches, for example "run a drift report".

## Install in Claude Code (plugin, with updates)

This repository is a Claude Code plugin marketplace. Install once at user level:

```
/plugin marketplace add DominusFL/keel
```

```
/plugin install keel@keel
```

Then call the skills as `/keel:keel`, `/keel:keel-init`, `/keel:keel-upgrade`, `/keel:keel-check`, `/keel:keel-as-built`, and `/keel:keel-interview`.

**Updates.** Each release of KEEL bumps the version in `KEEL.md` and in the plugin. To update, run `/plugin marketplace update keel` and then update the plugin from the Installed tab of `/plugin`, or run `claude plugin update keel@keel` in a shell. To update on your own, open `/plugin`, choose Marketplaces, choose keel, and turn on auto-update. Auto-update is off by default for a marketplace that is not an official one.

Inside a project, `/keel:keel-upgrade` then brings the project's docs to the new version.

## Install in Codex, Cursor, GitHub Copilot, or Claude Code without the plugin

The 6 skills follow the Agent Skills format (`SKILL.md` with `name` and `description`), which these tools read from their own skills folders. Two ways to install, both at user level, both able to update later:

**With the skills CLI** (needs Node):

```bash
npx skills add DominusFL/keel -g
```

It finds the 6 skills in `skills/`, asks which tools to install into, and copies them there. To update later:

```bash
npx skills update -g
```

**With the install script** (needs only `git`):

```bash
curl -fsSL https://raw.githubusercontent.com/DominusFL/keel/main/install.sh | sh
```

It clones this repository into `~/.keel/src`, then copies the skills into the folder of every tool whose config folder exists on your machine. Run the same command again to update. Options: `--agents claude,codex,cursor,copilot` to choose the tools, `--project` to install into the current project instead, `--ref v2.0.0` for a release tag, and `--remove` to uninstall. From a clone, run `sh install.sh --source .`.

Skills folders, user level: Claude Code `~/.claude/skills/`, Codex `~/.agents/skills/`, Cursor `~/.cursor/skills/`, GitHub Copilot `~/.copilot/skills/`. Project level: `.agents/skills/` for Codex, Cursor, and Copilot, and `.claude/skills/` for Claude Code.

Call a skill by its name, for example `/keel-init`, or ask for it in words. Note: `disable-model-invocation` (explicit only) is a Claude Code setting; other tools may start any of the 6 skills on their own when a request matches its description.

## Repository layout

```
KEEL.md                      The standard: the single source of truth
KEEL.html, KEEL.pdf          Renderings of KEEL.md
build/build.py               Generates skills/ and .claude-plugin/ from KEEL.md
skills/<name>/SKILL.md       The 6 skills (generated; do not edit by hand)
skills/<name>/reference/     Sections of KEEL.md a skill reads on demand (generated)
skills/<name>/templates/     The starter templates, 1 file each (generated)
.claude-plugin/              Plugin and marketplace manifests (generated)
install.sh                   Installs or updates the skills for other tools
```

## Releasing a new version

1. Edit `KEEL.md`: change the version line at the top and add the changelog entry.
2. Run `python3 build/build.py`. It regenerates the skills and the manifests with the new version.
3. Commit, then tag the release: `git tag v<version>` and `git push --tags`.

`python3 build/build.py --check` fails when the generated files do not match `KEEL.md`. The GitHub Actions workflow runs it on every push.

## License

MIT. See `LICENSE`.
