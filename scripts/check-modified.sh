#!/bin/bash
#
# Checks for 404 links in a compiled list of modified books

ERRORS=0

FILES=$(git diff --name-only origin/main...HEAD --diff-filter=d -- "*.adoc")

MODULES=$(echo "$FILES" | grep '^modules/.*\.adoc$')
ASSEMBLIES=$(echo "$FILES" | grep '^assemblies/.*\.adoc$')
BOOKS=$(echo "$FILES" | grep -E '^[^/]+\.adoc$')

UPDATED_BOOKS=()

if [ -n "$MODULES" ]; then
  # Check for assemblies and books that include modified modules
  while IFS= read -r module; do
    mapfile -t updated_books < <(grep -rnwl . --include="*.adoc" --exclude-dir={_artifacts,modules,assemblies} -e "$(basename "$module")")
    UPDATED_BOOKS+=( "${updated_books[@]}" )

    mapfile -t updated_books < <(grep -rnwl assemblies --include="*.adoc" --exclude-dir={_artifacts,modules} -e "$(basename "$module")")
    UPDATED_BOOKS+=( "${updated_books[@]}" )
  done <<< "$MODULES"
fi

# Check for books that include modified assemblies
if [ -n "$ASSEMBLIES" ]; then
  while IFS= read -r assembly; do
    mapfile -t results3 < <(grep -rnwl . --include="*.adoc" --exclude-dir={_artifacts,modules,assemblies} -e "$(basename "$assembly")")
    UPDATED_BOOKS+=( "${results3[@]}" )
  done <<< "$ASSEMBLIES"
fi

# Check for directly updated books
if [ -n "$BOOKS" ]; then
  while IFS= read -r book; do
    UPDATED_BOOKS+=( "$book" )
  done <<< "$BOOKS"
fi

if [ ${#UPDATED_BOOKS[@]} -eq 0 ]; then
  echo "No modified books. Skipping link check."
  exit 0
fi

# Check links in the compiled list of books

for f in "${UPDATED_BOOKS[@]}"; do
  echo "Checking: $f"
  if ! ./scripts/check-links.sh "$f"; then
    echo "❌ Link check failed for: $f"
    ERRORS=1
  fi
done

if [ "$ERRORS" -ne 0 ]; then
  echo "One or more link checks failed."
  exit 1
fi