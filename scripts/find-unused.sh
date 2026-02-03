#!/usr/bin/env bash
# scripts/find-unused.sh
#
# Lists .adoc files in modules/ that are NOT referenced by AsciiDoc include:: statements.
# Usage: scripts/find-unused.sh [--remove] [modules_dir] [repo_root]
# Optionally removes unused files with --remove.

set -e

REMOVE=0
# Parse optional flags before positional args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --remove) REMOVE=1; shift ;;
    --) shift; break ;;
    -*) echo "Unknown option: $1" >&2; exit 2 ;;
    *) break ;;
  esac
done

MODULES_DIR="${1:-modules}"
ROOT_DIR="${2:-.}"

# Collect *.adoc files in modules/, ignore symlinks
mapfile -d '' MODULE_FILES < <(find "$MODULES_DIR" -type f -name '*.adoc' -not -xtype l -print0)

# Collect *.adoc files outside modules/ (don’t descend into modules/)
mapfile -d '' SEARCH_FILES < <(find "$ROOT_DIR" -path "$MODULES_DIR" -prune -o -type f -name '*.adoc' -not -xtype l -print0)

# Extract referenced module paths from include::...[] statements
declare -A USED=()
if ((${#SEARCH_FILES[@]})); then
  while IFS= read -r ref; do
    ref="${ref#./}"   # normalize leading ./
    USED["$ref"]=1
  done < <(
    printf '%s\0' "${SEARCH_FILES[@]}" |
      xargs -0r grep -h -o -E '^[[:space:]]*include::[^[]*modules/[^[]*\.adoc' |
      sed -E 's/^[[:space:]]*include:://' |
      sed -E 's#^\./##' |
      LC_ALL=C sort -u
  )
fi

# Report or remove unused modules
unused=()
for f in "${MODULE_FILES[@]}"; do
  rel="${f#./}"
  if [[ -z "${USED["$rel"]+y}" ]]; then
    unused+=("$rel")
  fi
done

if ((${#unused[@]})); then
  echo -e "\nUnused modules:"
  printf '%s\n' "${unused[@]}" | LC_ALL=C sort
  if ((REMOVE)); then
    echo -e "\nRemoved modules:"
    rm -v "${unused[@]}"
  fi
else
  echo "All module .adoc files are referenced."
fi
