<div align="center">

# ⚓ KEEL

**A documentation and working standard for AI-developed projects.**

Like the keel of a ship, it keeps a project steady and on course when the AI tool, the AI model, or the developer changes.

[![Version](https://img.shields.io/badge/version-2.0.0-0b5fff)](https://github.com/DominusFL/keel/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Works with](https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex%20%7C%20Cursor%20%7C%20Copilot-6f42c1)](#-install)

</div>

---

**Contents:** [Why KEEL](#-why-keel) · [Quick start](#-quick-start) · [What you get](#-what-you-get) · [The 6 skills](#-the-6-skills) · [Install](#-install) · [Updates](#-updates) · [File or skill?](#-file-or-skill) · [Repository layout](#-repository-layout) · [Releasing](#-releasing-a-new-version) · [License](#-license)

## 🧭 Why KEEL

AI coding tools are fast, but they forget. Each new session, model, or tool starts without the context of the last one. The result is familiar:

- Requirements drift to match whatever the code does.
- Decisions get reversed because no one wrote them down.
- The handoff note becomes a long memory dump that nobody reads.
- Tests get skipped, and "done" means different things on different days.

A ship's keel is the long beam along the bottom of the hull. Every other part is built on it. It is the backbone of the ship: it holds the structure together and keeps the ship on course. KEEL is the backbone of an AI-developed project. It is a small set of documents and working rules that every AI coding tool can follow, and everything else is built on it. The rules live in `AGENTS.md`, a shared format that Claude Code, GitHub Copilot, Codex, and Cursor all read. The documents hold the truth. The AI keeps them current in the same task, proposes changes to requirements instead of rewriting them, tests only what changed, and ends every task with evidence.

The full standard is one file: [`KEEL.md`](KEEL.md). It is both a guide for developers and a setup prompt for AI coding assistants.

## 🚀 Quick start

**Option A. Put the file in your project.** Copy `KEEL.md` into the project root and tell your AI coding agent:

> *Read KEEL.md and do what it says.*

**Option B. Install the skills once, use them everywhere.** In Claude Code:

```
/plugin marketplace add DominusFL/keel
```

```
/plugin install keel@keel
```

Then open any project and run `/keel:keel`. For other tools, see [Install](#-install).

Both options work for new and existing projects. The AI asks for your approval before it changes any existing file.

## 📦 What you get

KEEL sets up a small, fixed set of files. Each one has a job.

| File | Job |
|---|---|
| `README.md` | For humans: what the project is, how to run it, owners and support |
| `docs/SPEC.md` | What and why: goals, users, glossary, features, constraints, acceptance criteria with IDs |
| `docs/ARCHITECTURE.md` | How: stack, folders, commands, data model, operations, and the area map that tells the AI what to read and test |
| `docs/PLAN.md` | Execution: milestones, the work board, Definition of ready, Definition of done |
| `docs/RELEASE-CHECKLIST.md` | Release gate: one check per acceptance criterion, and the release steps |
| `AGENTS.md` | The AI working rules, shared by every tool, under about 120 lines |
| `CLAUDE.md`, `.github/copilot-instructions.md` | Pointers to `AGENTS.md`, plus tool-only notes |
| `docs/decisions/`, `docs/HANDOFF.md`, `docs/CHANGELOG.md` | Decisions that are never rewritten, a 40-line session handoff, and the release history |

And a few habits the rules enforce:

- 🔒 **Humans own the requirements.** The AI proposes SPEC and DESIGN changes as `PROPOSED` blocks in the file. You accept or reject them.
- 🧪 **Test progressively.** Targeted tests by default, a full regression only before a release. A docs check script runs with every change.
- 📋 **Every claim carries evidence.** Each task ends with a fixed summary: what changed, what ran, what was proposed, what was skipped.
- 🤝 **Clean handoffs.** A close routine routes each item to its proper document and rewrites the handoff file. Nothing is copied forward.

## 🧩 The 6 skills

The same standard, packaged as skills you install once at user level. They work in every project without the file.

| Skill | Task |
|---|---|
| `keel` | General: looks at the project, chooses the path (new setup, migration, upgrade, or switch), and does it |
| `keel-init` | New setup from the templates, for a project with no docs yet |
| `keel-upgrade` | Migrate existing docs, upgrade an older KEEL version, or switch a `KEEL.md` project to the skill |
| `keel-check` | Write or run the docs check script, and write a drift report |
| `keel-as-built` | The as-built review of existing code: area map, SPEC from code, differences and health |
| `keel-interview` | The SPEC interview: fill the gaps in `SPEC.md` as PROPOSED blocks |

`keel`, `keel-init`, and `keel-upgrade` run only when you call them, because they create or change many files. The other 3 may also start on their own in a KEEL project when a request matches, for example "run a drift report".

A few prompts to try in a KEEL project:

> *Run a drift report.*
> *Interview me about the gaps in the spec.*
> *I'm closing this session. Run the close routine.*
> *Prepare release 1.0: run the release checklist and record the results.*

## 🔧 Install

### Claude Code (plugin, with updates)

This repository is a Claude Code plugin marketplace. Install once at user level:

```
/plugin marketplace add DominusFL/keel
```

```
/plugin install keel@keel
```

Then call the skills as `/keel:keel`, `/keel:keel-init`, `/keel:keel-upgrade`, `/keel:keel-check`, `/keel:keel-as-built`, and `/keel:keel-interview`.

### Codex, Cursor, GitHub Copilot, or Claude Code without the plugin

The 6 skills follow the Agent Skills format (`SKILL.md` with `name` and `description`), which these tools read from their own skills folders. Two ways to install, both at user level, both able to update later:

**With the skills CLI** (needs Node):

```bash
npx skills add DominusFL/keel -g
```

It finds the 6 skills in `skills/`, asks which tools to install into, and copies them there.

**With the install script** (needs only `git`):

```bash
curl -fsSL https://raw.githubusercontent.com/DominusFL/keel/main/install.sh | sh
```

It clones this repository into `~/.keel/src`, then copies the skills into the folder of every tool whose config folder exists on your machine. Options: `--agents claude,codex,cursor,copilot` to choose the tools, `--project` to install into the current project instead, `--ref v2.0.0` for a release tag, and `--remove` to uninstall. From a clone, run `sh install.sh --source .`.

Skills folders, user level: Claude Code `~/.claude/skills/`, Codex `~/.agents/skills/`, Cursor `~/.cursor/skills/`, GitHub Copilot `~/.copilot/skills/`. Project level: `.agents/skills/` for Codex, Cursor, and Copilot, and `.claude/skills/` for Claude Code.

Call a skill by its name, for example `/keel-init`, or ask for it in words. Note: `disable-model-invocation` (explicit only) is a Claude Code setting; other tools may start any of the 6 skills on their own when a request matches its description.

## 🔄 Updates

Each release of KEEL bumps the version in `KEEL.md` and in the plugin.

| Installed with | Update command |
|---|---|
| Claude Code plugin | `/plugin marketplace update keel`, then update the plugin from the Installed tab of `/plugin`, or `claude plugin update keel@keel` in a shell |
| Skills CLI | `npx skills update -g` |
| Install script | Run the same `curl ... \| sh` command again |

To update on your own in Claude Code, open `/plugin`, choose Marketplaces, choose keel, and turn on auto-update. Auto-update is off by default for a marketplace that is not an official one.

Inside a project, `/keel:keel-upgrade` then brings the project's docs to the new version.

## ⚖️ File or skill?

Both forms carry the same version and the same rules.

| Form | How it works | Best for |
|---|---|---|
| **File** | Put `KEEL.md` in the project root and tell the AI: *"Read KEEL.md and do what it says."* | A single project, or a team that wants the standard in the repository |
| **Skill** | Install the 6 KEEL skills once at user level. They work in every project without the file. | A developer who applies KEEL to many projects and wants updates from this repository |

When `KEEL.md` is in the project root, it is the authority. A project can switch from the file to the skill at any time (see *Switch to the skill* in `KEEL.md`), and a project set up by the skill can add the file later.

## 🗂️ Repository layout

```
KEEL.md                      The standard: the single source of truth
KEEL.html, KEEL.pdf          Renderings of KEEL.md
build/build.py               Generates skills/ and .claude-plugin/ from KEEL.md
skills/<name>/SKILL.md       The 6 skills (generated; do not edit by hand)
skills/<name>/references/    Sections of KEEL.md a skill reads on demand (generated)
skills/<name>/templates/     The starter templates, 1 file each (generated)
.claude-plugin/              Plugin and marketplace manifests (generated)
install.sh                   Installs or updates the skills for other tools
```

## 🏷️ Releasing a new version

1. Edit `KEEL.md`: change the version line at the top and add the changelog entry.
2. Run `python3 build/build.py`. It regenerates the skills and the manifests with the new version, and updates the version badge in this README.
3. Commit, then tag the release: `git tag v<version>` and `git push --tags`.

`python3 build/build.py --check` fails when the generated files do not match `KEEL.md`. The GitHub Actions workflow runs it on every push.

## 📄 License

MIT. See [`LICENSE`](LICENSE).
