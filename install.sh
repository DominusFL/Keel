#!/usr/bin/env sh
# install.sh: install or update the KEEL skills for Codex, Cursor, GitHub Copilot, and Claude Code.
#
# What it does: clones or updates https://github.com/rickflashman/keel into a cache folder, then copies
# the 6 skill folders (skills/keel, skills/keel-init, ...) into each tool's skills folder.
# Run it again to update. Needs only git and a POSIX shell. No Node, no plugin system.
#
# Usage:
#   sh install.sh                     user level, every tool whose config folder exists
#   sh install.sh --agents codex,cursor,copilot,claude
#   sh install.sh --project           into the current project: .agents/skills and .claude/skills
#   sh install.sh --remove            remove the KEEL skills from the chosen folders
#   sh install.sh --source /path      use a local checkout instead of the cache (for development)
#   sh install.sh --ref v2.0.0        install a tag or branch instead of main
#
# From a clone, run: sh install.sh --source .
# Without a clone, run:
#   curl -fsSL https://raw.githubusercontent.com/rickflashman/keel/main/install.sh | sh
#
# Skill folders (user level), from the skills CLI agent list:
#   Claude Code  ~/.claude/skills/   Codex  ~/.agents/skills/
#   Cursor       ~/.cursor/skills/   GitHub Copilot  ~/.copilot/skills/
# Project level: .agents/skills/ (Codex, Cursor, Copilot) and .claude/skills/ (Claude Code).

set -eu

REPO_URL="https://github.com/rickflashman/keel"
CACHE="${KEEL_HOME:-$HOME/.keel}/src"
REF="main"
SOURCE=""
AGENTS=""
SCOPE="user"
ACTION="install"
SKILLS="keel keel-init keel-upgrade keel-check keel-as-built keel-interview"

while [ $# -gt 0 ]; do
  case "$1" in
    --agents) AGENTS="$2"; shift ;;
    --project) SCOPE="project" ;;
    --remove) ACTION="remove" ;;
    --source) SOURCE="$2"; shift ;;
    --ref) REF="$2"; shift ;;
    -h|--help) sed -n '2,24p' "$0"; exit 0 ;;
    *) echo "install.sh: unknown option $1" >&2; exit 2 ;;
  esac
  shift
done

# 1. Get the source: a local checkout, or the cache clone (updated on every run).
if [ -z "$SOURCE" ] && [ "$ACTION" = "install" ]; then
  if [ -d "$CACHE/.git" ]; then
    git -C "$CACHE" fetch --quiet --tags origin
  else
    mkdir -p "$(dirname "$CACHE")"
    git clone --quiet "$REPO_URL" "$CACHE"
  fi
  git -C "$CACHE" checkout --quiet "$REF" 2>/dev/null || git -C "$CACHE" checkout --quiet "origin/$REF"
  if git -C "$CACHE" symbolic-ref -q HEAD >/dev/null; then
    git -C "$CACHE" pull --quiet --ff-only origin "$REF"
  fi
  SOURCE="$CACHE"
fi
if [ "$ACTION" = "install" ] && [ ! -f "$SOURCE/skills/keel/SKILL.md" ]; then
  echo "install.sh: no skills/keel/SKILL.md in $SOURCE" >&2; exit 1
fi

# 2. Choose the target folders.
targets=""
add_target() { targets="$targets $1"; }
if [ "$SCOPE" = "project" ]; then
  add_target ".agents/skills"
  add_target ".claude/skills"
else
  if [ -z "$AGENTS" ]; then
    # Default: every tool whose config folder exists on this machine.
    [ -d "$HOME/.claude" ] && AGENTS="$AGENTS,claude"
    [ -d "$HOME/.codex" ] && AGENTS="$AGENTS,codex"
    [ -d "$HOME/.cursor" ] && AGENTS="$AGENTS,cursor"
    [ -d "$HOME/.copilot" ] && AGENTS="$AGENTS,copilot"
  fi
  for a in $(echo "$AGENTS" | tr ',' ' '); do
    case "$a" in
      claude|claude-code) add_target "$HOME/.claude/skills" ;;
      codex) add_target "$HOME/.agents/skills" ;;
      cursor) add_target "$HOME/.cursor/skills" ;;
      copilot|github-copilot) add_target "$HOME/.copilot/skills" ;;
      "") ;;
      *) echo "install.sh: unknown agent $a (use claude, codex, cursor, copilot)" >&2; exit 2 ;;
    esac
  done
fi
if [ -z "$targets" ]; then
  echo "install.sh: no tool found. Name one or more with --agents claude,codex,cursor,copilot" >&2; exit 1
fi

# 3. Copy or remove each skill folder.
for dir in $targets; do
  mkdir -p "$dir"
  for skill in $SKILLS; do
    rm -rf "$dir/$skill"
    if [ "$ACTION" = "install" ]; then
      cp -R "$SOURCE/skills/$skill" "$dir/$skill"
    fi
  done
  if [ "$ACTION" = "install" ]; then
    version=$(sed -n 's/^Version \([0-9.]*\).*/\1/p' "$SOURCE/KEEL.md" | head -n 1)
    echo "KEEL ${version:-?} skills installed in $dir"
  else
    echo "KEEL skills removed from $dir"
  fi
done
