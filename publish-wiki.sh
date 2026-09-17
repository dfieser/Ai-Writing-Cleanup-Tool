#!/usr/bin/env bash
# Publish the pages in wiki/ to this repository's GitHub wiki.
#
#   ./publish-wiki.sh             push to the default wiki remote
#   ./publish-wiki.sh <clone-url> push to a different wiki
#   ./publish-wiki.sh --dry-run   show what would change, push nothing
#
# The wiki is a separate git repository, so this clones it, replaces its
# top-level pages with the ones in wiki/, and pushes the difference.
set -euo pipefail

DEFAULT_REMOTE="https://github.com/dfieser/Ai-Writing-Cleanup-Tool.wiki.git"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/wiki"

dry_run=0
remote="$DEFAULT_REMOTE"
for arg in "$@"; do
  case "$arg" in
    --dry-run) dry_run=1 ;;
    -h|--help) sed -n '2,9p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)         remote="$arg" ;;
  esac
done

if [ ! -d "$SRC" ]; then
  echo "no wiki/ directory next to this script" >&2
  exit 1
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

echo "cloning $remote"
git clone --quiet "$remote" "$tmp"

find "$tmp" -maxdepth 1 -name '*.md' -delete
cp "$SRC"/*.md "$tmp"/

cd "$tmp"
git add -A

if git diff --cached --quiet; then
  echo "wiki is already up to date"
  exit 0
fi

echo
git diff --cached --stat
echo

if [ "$dry_run" -eq 1 ]; then
  echo "dry run, nothing pushed"
  exit 0
fi

git commit --quiet -m "Sync wiki from the repository"
git push --quiet origin HEAD
echo "pushed to $remote"
