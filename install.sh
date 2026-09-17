#!/usr/bin/env bash
# Install the ai-writing-cleanup skill for Claude Code or Claude Desktop.
#
#   ./install.sh                install for your user  (~/.claude/skills)
#   ./install.sh --project      install into the current project (./.claude/skills)
#   ./install.sh --into DIR     install into DIR/.claude/skills
#   ./install.sh --link         symlink instead of copy, so git pull updates it
#   ./install.sh --uninstall    remove an existing install
#
# Works from any directory. The last lines of output are SKILL_PATH=... and
# CHECKER=..., so a caller can parse them.
#
set -euo pipefail

SKILL_NAME="ai-writing-cleanup"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills/$SKILL_NAME"

scope="user"
mode="copy"
action="install"
into=""

while [ $# -gt 0 ]; do
  case "$1" in
    --project)   scope="project" ;;
    --user)      scope="user" ;;
    --into)      shift; into="${1:-}"
                 [ -n "$into" ] || { echo "--into needs a directory" >&2; exit 2; }
                 scope="into" ;;
    --into=*)    into="${1#--into=}"; scope="into" ;;
    --link)      mode="link" ;;
    --uninstall) action="uninstall" ;;
    -h|--help)   sed -n '2,11p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)           echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

case "$scope" in
  into)
    [ -d "$into" ] || { echo "no such directory: $into" >&2; exit 2; }
    DEST_DIR="$(cd "$into" && pwd)/.claude/skills" ;;
  project)
    DEST_DIR="$PWD/.claude/skills" ;;
  *)
    DEST_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills" ;;
esac
DEST="$DEST_DIR/$SKILL_NAME"

if [ "$action" = "uninstall" ]; then
  if [ -e "$DEST" ] || [ -L "$DEST" ]; then
    rm -rf "$DEST"
    echo "removed $DEST"
  else
    echo "nothing installed at $DEST"
  fi
  exit 0
fi

if [ ! -f "$SRC/SKILL.md" ]; then
  echo "cannot find $SRC/SKILL.md. Run this script from the repository." >&2
  exit 1
fi

mkdir -p "$DEST_DIR"
rm -rf "$DEST"

if [ "$mode" = "link" ]; then
  ln -s "$SRC" "$DEST"
  echo "linked $DEST -> $SRC"
else
  cp -R "$SRC" "$DEST"
  # Drop build cruft that cp -R picks up from a source tree someone has run.
  find "$DEST" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
  find "$DEST" -name '*.py[co]' -delete 2>/dev/null || true
  echo "installed $DEST"
fi

chmod +x "$DEST/scripts/check_writing.py" 2>/dev/null || true

echo
echo "Start a new Claude session, then ask it to clean up a draft."
echo "SKILL_PATH=$DEST"
echo "CHECKER=$DEST/scripts/check_writing.py"
