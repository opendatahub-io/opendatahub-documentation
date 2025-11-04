#!/usr/bin/env bash
# Compiles a list of updated root adoc books in the current PR, and then checks each book for 404 errors using check-book-links.sh
# Requires Bash 4.0+
if ((BASH_VERSINFO[0] < 4)); then
    echo "Error: This script requires Bash 4.0 or later" >&2
    exit 1
fi

ERRORS=0

FILES=$(git diff --name-only HEAD~1 HEAD --diff-filter=d "*.adoc")

MODULES=$(echo "$FILES" | grep '^modules/.*\.adoc$')
ASSEMBLIES=$(echo "$FILES" | grep '^assemblies/.*\.adoc$')
BOOKS=$(echo "$FILES" | grep -E '^[^/]+\.adoc$')

UPDATED_BOOKS=()

if [ -n "$MODULES" ]; then
  # Check for books that include modified modules (directly or via assemblies)
  while IFS= read -r module; do
    # Find root adoc books that directly include the module
    mapfile -t files < <(find . -maxdepth 1 -name "*.adoc" -type f -print0 2>/dev/null || true)
    if [ ${#files[@]} -gt 0 ]; then
      mapfile -t updated_books < <(grep -l "include::.*$(basename "$module")" "${files[@]}" 2>/dev/null || true)
      UPDATED_BOOKS+=( "${updated_books[@]}" )
    fi

    # Find assemblies that include the module, then find root adoc books that include those assemblies
    if [ -d assemblies ]; then
      mapfile -t assembly_files < <(find assemblies -name "*.adoc" -type f -print0 2>/dev/null)
      if [ ${#assembly_files[@]} -gt 0 ]; then
        mapfile -t updated_assemblies < <(grep -l "include::.*$(basename "$module")" "${assembly_files[@]}" 2>/dev/null || true)
        for assembly in "${updated_assemblies[@]}"; do
          mapfile -t book_files < <(find . -maxdepth 1 -name "*.adoc" -type f -print0 2>/dev/null)
          if [ ${#book_files[@]} -gt 0 ]; then
            mapfile -t books_with_assembly < <(grep -l "$(basename "$assembly")" "${book_files[@]}" 2>/dev/null || true)
            UPDATED_BOOKS+=( "${books_with_assembly[@]}" )
          fi
        done
      fi
    fi
  done <<< "$MODULES"
fi

# Check for books that include modified assemblies
if [ -n "$ASSEMBLIES" ]; then
  while IFS= read -r assembly; do
    mapfile -t book_files < <(find . -maxdepth 1 -name "*.adoc" -type f -print0 2>/dev/null || true)
    if [ ${#book_files[@]} -gt 0 ]; then
      mapfile -t books_with_modified_assembly < <(grep -l "$(basename "$assembly")" "${book_files[@]}" 2>/dev/null || true)
      UPDATED_BOOKS+=( "${books_with_modified_assembly[@]}" )
    fi
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

# Remove duplicates from UPDATED_BOOKS
mapfile -t UPDATED_BOOKS < <(printf '%s\n' "${UPDATED_BOOKS[@]}" | sort -u)

# Check links in the compiled list of books
for f in "${UPDATED_BOOKS[@]}"; do
  if ! ./scripts/check-book-links.sh "$f"; then
    ERRORS=1
  fi
done

if [ "$ERRORS" -ne 0 ]; then
  exit 1
fi
