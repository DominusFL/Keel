#!/usr/bin/env python3
"""Generate the KEEL skills from KEEL.md.

KEEL.md is the single source of truth. This script reads it and writes:

- skills/<name>/SKILL.md for the 6 skills (keel, keel-init, keel-upgrade,
  keel-check, keel-as-built, keel-interview)
- skills/<name>/references/*.md: sections of KEEL.md that a skill reads on demand
- skills/<name>/templates/*: the starter templates, 1 file per template, plus
  templates/README.md with the guidance for each one
- .claude-plugin/plugin.json and .claude-plugin/marketplace.json, with the
  version taken from KEEL.md
- the version badge in README.md, set to the same version

Usage:
    python3 build/build.py          # write the files
    python3 build/build.py --check  # exit 1 if the files on disk differ

Inputs: KEEL.md. Outputs: the files above. No dependencies beyond Python 3.8+.
Change the skill text by changing KEEL.md or the SKILL_INTROS below, then run
the script again.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "KEEL.md"
SKILLS_DIR = ROOT / "skills"
PLUGIN_DIR = ROOT / ".claude-plugin"
REPO_URL = "https://github.com/DominusFL/keel"
SKILL_NAMES = ["keel", "keel-init", "keel-upgrade", "keel-check", "keel-as-built", "keel-interview"]


# --------------------------------------------------------------------------
# Parsing KEEL.md
# --------------------------------------------------------------------------

def read_version(text: str) -> tuple[str, str]:
    """Return (version, date) from the 'Version X.Y.Z (date)' line."""
    m = re.search(r"^Version (\d+\.\d+\.\d+) \(([^)]+)\)", text, re.M)
    if not m:
        sys.exit("build: no 'Version X.Y.Z (date)' line in KEEL.md")
    return m.group(1), m.group(2)


def split_sections(text: str) -> dict[str, str]:
    """Split the document into its level-2 sections, ignoring headings inside code fences.

    Returns {title: body}; the body excludes the heading line and is stripped of
    leading and trailing blank lines.
    """
    sections: dict[str, str] = {}
    title = None
    buf: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## "):
            if title is not None:
                sections[title] = "\n".join(buf).strip("\n")
            title = line[3:].strip()
            buf = []
            continue
        if title is not None:
            buf.append(line)
    if title is not None:
        sections[title] = "\n".join(buf).strip("\n")
    return sections


def top_bullet(section: str, label: str) -> str:
    """Return the top-level bullet '- **label:** ...' with its indented continuation lines."""
    lines = section.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith(f"- **{label}:**"):
            start = i
            break
    if start is None:
        sys.exit(f"build: bullet '{label}' not found")
    out = [lines[start]]
    for line in lines[start + 1:]:
        if line.startswith("- ") or line.startswith("**") or line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out).rstrip()


def bold_paragraph(section: str, label: str) -> str:
    """Return the paragraph that starts with '**label:**' up to the next bold label at column 0."""
    lines = section.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith(f"**{label}:**"):
            start = i
            break
    if start is None:
        sys.exit(f"build: paragraph '{label}' not found")
    out = [lines[start]]
    in_fence = False
    for line in lines[start + 1:]:
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("**") and line != lines[start]:
            break
        out.append(line)
    return "\n".join(out).rstrip()


TEMPLATE_RE = re.compile(r"^\*\*([^*]+)\*\*(?:\s+\*\(([^)]*)\)\*)?\s*$")


def parse_templates(section: str) -> tuple[str, list[dict]]:
    """Parse the Starter templates section.

    Returns (intro, templates). Each template is {path, note, guidance, body}.
    """
    lines = section.splitlines()
    intro: list[str] = []
    templates: list[dict] = []
    current: dict | None = None
    in_fence = False
    fence: list[str] = []
    for line in lines:
        if in_fence:
            if line.startswith("```"):
                in_fence = False
                current["body"] = "\n".join(fence).rstrip() + "\n"
                fence = []
            else:
                fence.append(line)
            continue
        m = TEMPLATE_RE.match(line)
        if m and (m.group(1).endswith((".md", ".html")) or "/" in m.group(1)):
            current = {"path": m.group(1), "note": m.group(2) or "", "guidance": [], "body": ""}
            templates.append(current)
            continue
        if line.startswith("```"):
            if current is None:
                sys.exit("build: code fence before the first template label")
            in_fence = True
            continue
        if current is None:
            intro.append(line)
        else:
            current["guidance"].append(line)
    for t in templates:
        t["guidance"] = "\n".join(t["guidance"]).strip("\n")
        if not t["body"]:
            sys.exit(f"build: template {t['path']} has no code block")
    return "\n".join(intro).strip("\n"), templates


def template_file_name(path: str) -> str:
    """Map a template label to a file path under templates/.

    Angle brackets are removed, and '.template' is inserted before the extension,
    so no tool mistakes a template (CLAUDE.md, AGENTS.md, README.md) for a real
    instruction file, and the README template does not collide with templates/README.md.
    """
    clean = path.replace("<n>", "-n").replace("<", "").replace(">", "")
    stem, dot, ext = clean.rpartition(".")
    return f"{stem}.template.{ext}" if dot else f"{clean}.template"


# --------------------------------------------------------------------------
# Text adaptation: KEEL.md speaks as a file; the skills speak as a skill
# --------------------------------------------------------------------------

def adapt(text: str, section_files: dict[str, str]) -> str:
    """Rewrite self-references and cross-references for a skill.

    section_files maps a section title to where the skill holds it:
    'inline' (in SKILL.md) or a relative file path such as 'references/migration.md'.
    """
    out = text
    out = out.replace("this document's version", "this skill's version")
    out = out.replace("it is an older version of this document: follow this file", "it is an older version of this standard: follow this skill")
    out = out.replace("so the list survives without this file", "so the list survives without this skill")
    out = out.replace("this document", "this standard")
    out = out.replace("(this file, or the KEEL skill in its place;", "(the standard as a file, or this skill in its place;")
    out = out.replace(" (near the end of this standard)", "")
    out = out.replace("Create the files from the templates.", "Create the files from the templates in `templates/` (guidance: `templates/README.md`).")
    out = out.replace("using the starter templates", "using the templates in `templates/` (guidance: `templates/README.md`)")
    out = out.replace("(see *Proposed changes*)", "(see *Proposed changes to SPEC and DESIGN*)")

    def ref(m: re.Match) -> str:
        title = m.group(1)
        where = section_files.get(title)
        if where is None or where == "inline":
            return m.group(0)
        return f"(see `{where}`)"

    out = re.sub(r"\(see \*([^*]+)\*\)", ref, out)
    out = re.sub(r"\bin \*Migrating or upgrading an existing project\*", lambda m: _in_ref("Migrating or upgrading an existing project", section_files, m), out)
    out = re.sub(r"\bFollow \*Migrating or upgrading an existing project\*", lambda m: _follow_ref("Migrating or upgrading an existing project", section_files, m), out)
    return out


def _in_ref(title: str, section_files: dict[str, str], m: re.Match) -> str:
    where = section_files.get(title)
    if where is None or where == "inline":
        return m.group(0)
    return f"in `{where}`"


def _follow_ref(title: str, section_files: dict[str, str], m: re.Match) -> str:
    where = section_files.get(title)
    if where is None or where == "inline":
        return m.group(0)
    return f"Follow `{where}`"


# --------------------------------------------------------------------------
# Skill definitions
# --------------------------------------------------------------------------

STANDARD_SECTIONS = [
    "Authority and file handling",
    "Folder layout",
    "The documentation files",
    "Project skills",
    "Linking to the project tracker",
    "Risk classes",
    "Rules",
    "Docs check and drift report",
]

COMMON_NOTE = (
    "This skill is generated from `KEEL.md` in {repo}. Do not edit it by hand; "
    "change `KEEL.md` and run `python3 build/build.py`.\n"
)

SKILL_INTROS: dict[str, dict] = {
    "keel": {
        "description": (
            "KEEL {version}, the documentation and working standard for AI-developed projects. "
            "Sets up, migrates, or upgrades a project's docs (README, SPEC, ARCHITECTURE, PLAN, "
            "RELEASE-CHECKLIST, AGENTS.md) and chooses the right path on its own. Use when the "
            "developer runs the keel skill (/keel:keel or /keel), says 'apply KEEL', 'set up KEEL', or 'upgrade to the latest KEEL', "
            "or is not sure which KEEL task they need. Task skills: keel-init, keel-upgrade, "
            "keel-check, keel-as-built, keel-interview."
        ),
        "explicit": True,
        "argument_hint": "[init | upgrade | switch | check | as-built | interview | free text]",
        "intro": """# KEEL {version}

A documentation and working standard for AI-developed projects. Version {version} ({date}), {repo}.

Like the keel of a ship, it keeps a project steady and on course when the AI tool, the AI model, or the developer changes. It keeps the AI's work organized, supportable, and token-efficient. This is the general skill: it looks at the project, chooses the right path, and does it. The developer may also call 1 task directly:

| Skill | Task |
|---|---|
| `keel-init` | New setup from the templates, for a project with no docs yet |
| `keel-upgrade` | Migrate existing docs, upgrade an older KEEL version, or switch a `KEEL.md` project to this skill |
| `keel-check` | Write or run the docs check script, and write a drift report |
| `keel-as-built` | The as-built review: area map, SPEC from code, differences and health |
| `keel-interview` | The SPEC interview: fill the gaps in `SPEC.md` as PROPOSED blocks |

If the developer gave extra instructions with the command, follow them: $ARGUMENTS

## How to use this skill

1. Read *Initialization rules* below and choose 1 path: Upgrade, Migration, New setup, or Switch to the skill. Tell the developer which path you chose and why before you continue.
2. For a Migration or an Upgrade, read `references/migration.md` and follow it. `references/changelog.md` lists the changes in each version.
3. For a New setup, create the files from `templates/` (guidance: `templates/README.md`), in the numbered order of the documentation files table.
4. When the path is complete, run `references/checklist.md` and report. Then offer the as-built review (if the project has code) and the SPEC interview.
5. The developer approves before any existing file changes. Never delete, rename, move, or modify `KEEL.md` without the developer's explicit instruction.

The rest of this file is the standard itself: authority, initialization rules, folder layout, the documentation files, project skills, the tracker link, risk classes, the rules, and the docs check.
""",
        "inline": ["Authority and file handling", "Initialization rules"] + STANDARD_SECTIONS[1:],
        "references": {
            "migration.md": ["Migrating or upgrading an existing project"],
            "checklist.md": ["Initialization checklist"],
            "changelog.md": ["Changelog"],
        },
        "templates": "all",
    },
    "keel-init": {
        "description": (
            "KEEL {version} new setup: creates the baseline docs for a project that has no "
            "documentation yet (README, docs/SPEC, ARCHITECTURE, PLAN, RELEASE-CHECKLIST, AGENTS.md, "
            "CLAUDE.md, copilot-instructions) from the KEEL templates, then runs the initialization "
            "checklist. Use when the developer runs keel-init (/keel:keel-init or /keel-init) or asks to initialize a new project "
            "with KEEL. For a project that already has docs, use keel-upgrade."
        ),
        "explicit": True,
        "argument_hint": "[ticket ID or project description]",
        "intro": """# KEEL {version}: new setup

Create the baseline documentation for a project that has no documentation yet. Version {version} ({date}), {repo}.

If the developer gave the ticket ID, the project description, or other instructions with the command, use them: $ARGUMENTS

## Steps

1. **Check first.** Follow the Check first rule below. If the path is not *New setup*, stop and tell the developer to run `keel-upgrade` (migration or upgrade) or `keel` (any path). Do not continue with a project that already has docs.
2. **Ask before you create any file.** Send this message, with all 3 questions, as plain chat text, and wait for the answer. Do not use a question tool or form: the answers are free text. Skip only a question the developer already answered with the command. Never take the project name from the folder name. If the developer does not answer an item, leave its placeholder (see *Linking to the project tracker*).

       Before I create the files, 3 questions:
       1. Tracker and ticket ID, with the ticket link if you have one (or "none"):
       2. Project name and a short description:
       3. Does the project have a user interface (yes or no)?

3. **Create the required files** in numbered order from `templates/` (guidance for each file: `templates/README.md`). Create optional files only where the table says they are needed now, such as `docs/DESIGN.md` for a project with a UI. Follow the folder layout exactly.
4. **Write the docs check script** and add its row to the area map (see *Docs check and drift report*).
5. **Run the Initialization checklist** at the end of this file and report any item that fails.
6. **Offer** the as-built review (`keel-as-built`) if the project has code, then the SPEC interview (`keel-interview`).

Never overwrite a file that already exists; merge or ask. The rest of this file is the part of the standard that a new setup needs.
""",
        "inline": ["Initialization rules", "Folder layout", "The documentation files", "Project skills", "Linking to the project tracker", "Risk classes", "Rules", "Docs check and drift report", "Initialization checklist"],
        "references": {},
        "templates": "all",
    },
    "keel-upgrade": {
        "description": (
            "KEEL {version} migration and upgrade: brings an existing project's documentation up to "
            "the KEEL standard (inventory, currency, mapping, approval, migrate, archive), upgrades a "
            "project on an older KEEL or AI-PROJECT-DOCS-STANDARD version, or switches a project from "
            "the KEEL.md file to this skill. Use when the developer runs keel-upgrade (/keel:keel-upgrade or /keel-upgrade), says 'migrate "
            "the docs to KEEL', 'upgrade KEEL', or 'switch to the KEEL skill'."
        ),
        "explicit": True,
        "argument_hint": "[migrate | upgrade | switch]",
        "intro": """# KEEL {version}: migrate, upgrade, or switch

Bring an existing project up to KEEL version {version} ({date}), {repo}. Three cases:

- **Migration:** the project has documentation in another form (a README, notes, rules files, an older wiki export). Follow *Migrating or upgrading an existing project* below, steps 1 to 9.
- **Upgrade:** the project follows an older version of this standard (the stamp in `AGENTS.md` is older than {version}, or names *AI-PROJECT-DOCS-STANDARD*). Do steps 1, 8, and 9. `references/changelog.md` lists what changed in each version.
- **Switch to the skill:** the project has `KEEL.md` in its root folder and the developer wants this skill to be the reference instead. Follow the Switch to the skill path in the Initialization rules below.

If the developer gave instructions with the command, follow them: $ARGUMENTS

Whatever the case, change nothing until the developer approves the plan. Change only documentation, never code, configuration, or dependencies; the docs check script is the one exception. Use the templates in `templates/` (guidance: `templates/README.md`). When the work is complete, run `references/checklist.md`, report, and offer the as-built review (`keel-as-built`) and the SPEC interview (`keel-interview`).

The rest of this file holds the initialization rules, the migration and upgrade steps, and the parts of the standard they rely on.
""",
        "inline": ["Initialization rules", "Migrating or upgrading an existing project", "Authority and file handling", "Folder layout", "The documentation files", "Project skills", "Linking to the project tracker", "Risk classes", "Rules", "Docs check and drift report"],
        "references": {
            "checklist.md": ["Initialization checklist"],
            "changelog.md": ["Changelog"],
        },
        "templates": "all",
    },
    "keel-check": {
        "description": (
            "KEEL {version} docs check and drift report. Writes or runs the project's docs check "
            "script (AGENTS.md size and stamp, handoff size, AC coverage in the release checklist, "
            "broken paths and links, unlisted docs, headers, stray doc versions, stale PROPOSED "
            "blocks, secrets) and writes the read-only drift report (SPEC with no code, code with no "
            "SPEC, ACs with no test, stale doc sections). Use in a KEEL project when the developer "
            "runs keel-check (/keel:keel-check or /keel-check), says 'run the docs check', 'run a drift report', or before a release."
        ),
        "explicit": False,
        "argument_hint": "[docs | drift | both]",
        "intro": """# KEEL {version}: docs check and drift report

Run the 2 documentation checks of KEEL version {version} ({date}), {repo}. Both are defined below.

If the developer gave instructions with the command, follow them: $ARGUMENTS

## Steps

1. **Confirm the project uses KEEL.** `AGENTS.md` has an `Aligned to KEEL` stamp (or an older *AI-PROJECT-DOCS-STANDARD* stamp). If not, stop and tell the developer to run `keel` first.
2. **Docs check.** Find the script in the area map row *Docs* in `docs/ARCHITECTURE.md`. If it does not exist, write it as the definition below says (the project's own language, no new dependency, the list of checks in its header comment, results to `test-results/docs.md`), add its row to the area map and its command to the Testing section, then run it. If it exists, run it and compare its header comment with the list below; propose any missing check to the developer before you add it. Report the result from `test-results/docs.md`, with the exit code. Never weaken a check to make it pass.
3. **Drift report.** Write it as the definition below says: each finding with its certainty, never averaged. It changes nothing. Put it in the task summary; lasting findings go to `docs/RESEARCH.md` (create it from the standard if needed).
4. **Report** with the task summary from the `docs/PLAN.md` Definition of done. A check you could not run is "Not run: reason", never passed.

When the developer asked for only 1 of the 2 checks, do that one. Before a release, both run (rule 6 in `references/standard.md`).
""",
        "inline": ["Docs check and drift report"],
        "references": {
            "standard.md": STANDARD_SECTIONS,
        },
        "templates": ["docs/ARCHITECTURE.md", "docs/RESEARCH.md"],
    },
    "keel-as-built": {
        "description": (
            "KEEL {version} as-built review of existing code: feature inventory, area map in "
            "ARCHITECTURE.md, SPEC acceptance criteria inferred from the code as PROPOSED blocks, "
            "and a differences and health report (built but not specified, specified but not built, "
            "no tests, secrets, risky dependencies). Changes no code. Use in a KEEL project when the "
            "developer runs keel-as-built (/keel:keel-as-built or /keel-as-built) or asks for an as-built review, to document existing code, "
            "or to set the Verified dates."
        ),
        "explicit": False,
        "argument_hint": "[area names to review, or 'all']",
        "intro": """# KEEL {version}: as-built review

Document what the code does now, under KEEL version {version} ({date}), {repo}. Change no code. Do not run tests unless the developer asks.

If the developer gave instructions with the command, such as the areas to review, follow them: $ARGUMENTS

## Before you start

- The project follows KEEL: `AGENTS.md` has an `Aligned to KEEL` stamp and `docs/ARCHITECTURE.md` and `docs/SPEC.md` exist. If not, stop and tell the developer to run `keel` first.
- The developer may choose only some areas. Confirm the scope before step 1.
- Use a subagent per area where the tool allows, so the main context stays small.
- The templates for the files you write are in `templates/`; the standard, including the rules on PROPOSED blocks and the area map, is in `references/standard.md`.

## The review
""",
        "inline_extra": [("Initialization rules", "bullet", "As-built review"), ("The documentation files", "paragraph", "Proposed changes to SPEC and DESIGN")],
        "inline": [],
        "references": {
            "standard.md": STANDARD_SECTIONS,
        },
        "templates": ["docs/SPEC.md", "docs/ARCHITECTURE.md", "docs/RESEARCH.md", "docs/HANDOFF.md"],
    },
    "keel-interview": {
        "description": (
            "KEEL {version} SPEC interview: asks the developer a few questions at a time about the "
            "gaps in docs/SPEC.md (edge cases, non-goals, trade-offs, constraints, glossary terms, "
            "acceptance criteria) and writes the answers as PROPOSED blocks for acceptance. Use in a "
            "KEEL project when the developer runs keel-interview (/keel:keel-interview or /keel-interview), asks to interview them about the "
            "spec, or wants to fill the gaps in SPEC.md."
        ),
        "explicit": False,
        "argument_hint": "[feature or area to focus on]",
        "intro": """# KEEL {version}: SPEC interview

Fill the gaps in `docs/SPEC.md` by interviewing the developer, under KEEL version {version} ({date}), {repo}.

If the developer gave instructions with the command, such as a feature to focus on, follow them: $ARGUMENTS

## Steps

1. **Confirm the project uses KEEL** (`AGENTS.md` has an `Aligned to KEEL` stamp and `docs/SPEC.md` exists). If not, stop and tell the developer to run `keel` first.
2. **Read `docs/SPEC.md`** and the area map in `docs/ARCHITECTURE.md`. List the gaps by section: Goals, Users, Glossary, Features & user stories, Constraints, Acceptance criteria & test cases, Non-goals, Open questions. The SPEC template is in `templates/docs/SPEC.md`.
3. **Interview.** Ask a few questions at a time, and skip questions the docs already answer. Cover edge cases, non-goals, trade-offs, constraints, glossary terms, and acceptance criteria. The developer may stop at any time.
4. **Write the answers as PROPOSED blocks** in `docs/SPEC.md`, next to the text they change, never only in chat (the rule and the block format are below). Give each new acceptance criterion the next `AC-n` ID and its test cases, and note that `docs/RELEASE-CHECKLIST.md` needs a matching row once the block is accepted.
5. **Report** the PROPOSED blocks by file and AC ID or heading, and list them in `docs/HANDOFF.md` under Waiting at the next session close.

Never edit accepted SPEC text. The standard is in `references/standard.md`.

## The interview rule
""",
        "inline_extra": [("Initialization rules", "bullet", "SPEC interview"), ("The documentation files", "paragraph", "Proposed changes to SPEC and DESIGN")],
        "inline": [],
        "references": {
            "standard.md": STANDARD_SECTIONS,
        },
        "templates": ["docs/SPEC.md", "docs/RELEASE-CHECKLIST.md", "docs/HANDOFF.md"],
    },
}


# --------------------------------------------------------------------------
# Generation
# --------------------------------------------------------------------------

def yaml_str(s: str) -> str:
    """Quote a string for the YAML frontmatter."""
    return json.dumps(s)


def build_skill(name: str, spec: dict, sections: dict[str, str], templates: list[dict], tintro: str, version: str, date: str) -> dict[str, str]:
    """Return {relative path: content} for one skill folder."""
    files: dict[str, str] = {}
    fmt = dict(version=version, date=date, repo=REPO_URL)

    # Where each section lives, for cross-references.
    section_files: dict[str, str] = {}
    for title in spec["inline"]:
        section_files[title] = "inline"
    for fname, titles in spec["references"].items():
        for title in titles:
            section_files.setdefault(title, f"references/{fname}")
    for title, kind, label in spec.get("inline_extra", []):
        pass  # extracts, not whole sections

    # Frontmatter.
    desc = spec["description"].format(**fmt)
    if len(desc) > 1024:
        sys.exit(f"build: description of {name} is longer than 1024 characters")
    fm = ["---", f"name: {name}", f"description: {yaml_str(desc)}"]
    if spec["explicit"]:
        fm.append("disable-model-invocation: true")
    if spec.get("argument_hint"):
        fm.append(f"argument-hint: {yaml_str(spec['argument_hint'])}")
    fm += ["metadata:", f"  version: {yaml_str(version)}", f"  source: {yaml_str(REPO_URL)}", "---", ""]

    body = [spec["intro"].format(**fmt).rstrip(), ""]
    for title, kind, label in spec.get("inline_extra", []):
        src = sections[title]
        text = top_bullet(src, label) if kind == "bullet" else bold_paragraph(src, label)
        if kind == "bullet":
            # Turn '- **Label:** ...' with 2-space continuation into a plain paragraph.
            lines = text.splitlines()
            lines = [lines[0][2:]] + [l[2:] if l.startswith("  ") else l for l in lines[1:]]
            text = "\n".join(lines)
        body += [adapt(text, section_files), ""]
    for title in spec["inline"]:
        body += [f"## {title}", "", adapt(sections[title], section_files), ""]
    body += ["---", "", COMMON_NOTE.format(repo=REPO_URL)]
    files["SKILL.md"] = "\n".join(fm) + "\n".join(body)

    # Reference files.
    for fname, titles in spec["references"].items():
        parts = [f"# KEEL {version}: {fname[:-3]}", "", f"Reference for the `{name}` skill, generated from `KEEL.md` ({REPO_URL}). Do not edit by hand.", ""]
        for title in titles:
            parts += [f"## {title}", "", adapt(sections[title], section_files), ""]
        files[f"references/{fname}"] = "\n".join(parts).rstrip() + "\n"

    # Templates.
    wanted = spec["templates"]
    chosen = templates if wanted == "all" else [t for t in templates if t["path"] in wanted]
    if wanted != "all" and len(chosen) != len(wanted):
        sys.exit(f"build: {name} asks for a template that does not exist: {wanted}")
    readme = [f"# KEEL {version}: starter templates", "", f"Generated from `KEEL.md` ({REPO_URL}). Do not edit by hand. Each template is a file in this folder at the path it takes in the project, with `.template` before its extension: copy `docs/SPEC.template.md` to `docs/SPEC.md`.", "", adapt(tintro, section_files), ""]
    for t in chosen:
        files[f"templates/{template_file_name(t['path'])}"] = t["body"]
        head = f"## `{t['path']}`" + (f" *({t['note']})*" if t["note"] else "")
        readme += [head, "", f"Template: `templates/{template_file_name(t['path'])}`", ""]
        if t["guidance"]:
            readme += [adapt(t["guidance"], section_files), ""]
    files["templates/README.md"] = "\n".join(readme).rstrip() + "\n"
    return files


def build_manifests(version: str) -> dict[str, str]:
    """Return the plugin and marketplace manifests as {relative path: content}."""
    description = "KEEL: a documentation and working standard for AI-developed projects. 6 skills: keel, keel-init, keel-upgrade, keel-check, keel-as-built, keel-interview."
    plugin = {
        "name": "keel",
        "displayName": "KEEL",
        "description": description,
        "version": version,
        "author": {"name": "Rick Flashman"},
        "homepage": REPO_URL,
        "repository": REPO_URL,
        "license": "MIT",
        "keywords": ["documentation", "standard", "agents-md", "spec", "handoff", "keel"],
    }
    marketplace = {
        "name": "keel",
        "owner": {"name": "Rick Flashman", "url": REPO_URL},
        "description": "Marketplace for the KEEL skills. Add with: /plugin marketplace add DominusFL/keel",
        "plugins": [
            {
                "name": "keel",
                "source": "./",
                "description": description,
                "category": "productivity",
                "tags": ["documentation", "standard", "keel"],
            }
        ],
    }
    return {
        ".claude-plugin/plugin.json": json.dumps(plugin, indent=2) + "\n",
        ".claude-plugin/marketplace.json": json.dumps(marketplace, indent=2) + "\n",
    }


BADGE_RE = re.compile(r"(https://img\.shields\.io/badge/version-)[0-9.]+(-[0-9a-fA-F]+\))")


def readme_with_badge(version: str) -> str:
    """Return README.md with its version badge set to the KEEL.md version."""
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    new, n = BADGE_RE.subn(lambda m: f"{m.group(1)}{version}{m.group(2)}", text, count=1)
    if n != 1:
        sys.exit("build: README.md has no version badge (img.shields.io/badge/version-X.Y.Z-color)")
    return new


def generate() -> dict[str, str]:
    """Build every output file in memory. Returns {path relative to ROOT: content}."""
    text = SOURCE.read_text(encoding="utf-8")
    version, date = read_version(text)
    sections = split_sections(text)
    missing = [t for t in STANDARD_SECTIONS + ["Initialization rules", "Starter templates", "Initialization checklist", "Migrating or upgrading an existing project", "Changelog"] if t not in sections]
    if missing:
        sys.exit(f"build: KEEL.md is missing the section(s) {missing}; update build.py if a heading changed")
    tintro, templates = parse_templates(sections["Starter templates"])
    out: dict[str, str] = {}
    for name in SKILL_NAMES:
        for rel, content in build_skill(name, SKILL_INTROS[name], sections, templates, tintro, version, date).items():
            out[f"skills/{name}/{rel}"] = content
    out.update(build_manifests(version))
    out["README.md"] = readme_with_badge(version)
    return out


def write(files: dict[str, str]) -> None:
    """Replace skills/ and the manifests with the generated files."""
    if SKILLS_DIR.exists():
        shutil.rmtree(SKILLS_DIR)
    for rel, content in files.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    print(f"build: wrote {len(files)} files for KEEL {read_version(SOURCE.read_text(encoding='utf-8'))[0]}")


def check(files: dict[str, str]) -> int:
    """Compare the generated files with the files on disk. Returns the exit code."""
    problems: list[str] = []
    for rel, content in files.items():
        path = ROOT / rel
        if not path.exists():
            problems.append(f"missing: {rel}")
        elif path.read_text(encoding="utf-8") != content:
            problems.append(f"differs: {rel}")
    if SKILLS_DIR.exists():
        for path in SKILLS_DIR.rglob("*"):
            if path.is_file():
                rel = path.relative_to(ROOT).as_posix()
                if rel not in files:
                    problems.append(f"stray: {rel}")
    if problems:
        print("build --check: the generated files are out of date. Run: python3 build/build.py")
        for p in problems:
            print("  " + p)
        return 1
    print("build --check: skills/, .claude-plugin/ and the README badge match KEEL.md")
    return 0


def main(argv: list[str]) -> int:
    files = generate()
    if "--check" in argv:
        return check(files)
    write(files)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
