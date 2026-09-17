#!/usr/bin/env bash
# Install the ai-writing-cleanup skill for Claude Code or Claude Desktop.
#
#   ./install.sh              install for your user  (~/.claude/skills)
#   ./install.sh --project    install into the current project (./.claude/skills)
#   ./install.sh --link       symlink instead of copy, so git pull updates it
#   ./install.sh --uninstall  remove an existing install
#
set -euo pipefail

SKILL_NAME="ai-writing-cleanup"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills/$SKILL_NAME"

scope="user"
mode="copy"
action="install"

for arg in "$@"; do
  case "$arg" in
    --project)   scope="project" ;;
    --user)      scope="user" ;;
    --link)      mode="link" ;;
    --uninstall) action="uninstall" ;;
    -h|--help)   sed -n '2,8p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)           echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

if [ "$scope" = "project" ]; then
  DEST_DIR="$PWD/.claude/skills"
else
  DEST_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
fi
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
  echo "installed $DEST"
fi

chmod +x "$DEST/scripts/check_writing.py" 2>/dev/null || true

echo
echo "Start a new Claude session, then ask it to clean up a draft."
echo "Check the script directly with:"
echo "  python3 $SRC/scripts/check_writing.py your-draft.md"
