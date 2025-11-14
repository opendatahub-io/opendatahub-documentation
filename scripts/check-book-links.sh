#!/usr/bin/env bash
# Checks for invalid or broken links in HTML built from root adoc files using Asciidoctor and curl
# Usage: ./check-book-links.sh [adoc file]
# If no file is specified, runs on all adoc files in the root folder
# Requires Bash 4.0+
if ((BASH_VERSINFO[0] < 4)); then
    echo "Error: This script requires Bash 4.0 or later" >&2
    exit 1
fi

if ! asciidoctor -v >/dev/null 2>&1; then
    echo "Error: Asciidoctor is not installed" >&2
    exit 1
fi

# URL ignore patterns
IGNORE_FILE="$(dirname "$0")/.links_ignore"
IGNORE_PATTERNS=""

# Read patterns, skipping empty lines and comments
if [[ -f "$IGNORE_FILE" ]]; then
    IGNORE_PATTERNS=$(grep -v '^#' "$IGNORE_FILE" | grep -v '^[[:space:]]*$' || true)
fi

export IGNORE_PATTERNS

# shellcheck disable=SC2317  # called via bash -c / xargs
check_url() {
    local URL STATUS
    # Strip . , ; : ) ] } but preserve URL-safe chars like + = & #
    URL=$(echo "$1" | sed 's/[.,;:)\]}]*$//')

    # Skip ignored URLs by checking against each pattern
    if [[ -n "$IGNORE_PATTERNS" ]]; then
        while IFS= read -r pattern; do
            if [[ "$URL" =~ $pattern ]]; then
                return 0
            fi
        done <<< "$IGNORE_PATTERNS"
    fi

    STATUS=$(curl -Ls -o /dev/null -w "%{http_code}" --max-time 5 --connect-timeout 2 "$URL")
    if [[ "$STATUS" != "000" && "$STATUS" != "403" && ! "$STATUS" =~ ^(2|3)[0-9]{2}$ ]]; then
        printf 'Invalid URL (HTTP status %s): \n\033[31m%s\033[0m\n' "$STATUS" "$URL"
        return 1
    fi
}

export -f check_url

run_url_checks() {
    local FILE="$1"
    echo -e "\n\033[32mChecking: $FILE\033[0m"

    # Extract HTTP(S) URLs from the rendered HTML
    asciidoctor "$FILE" -a doctype=book -o - |
        # Match URLs and special chars like + & # ~ etc. that are valid in URLs
        grep -Eo '(http|https)://[a-zA-Z0-9./?=%_&+~#:@!$*,;-]*' |
        sort -u |
        xargs -P 10 -I{} bash -c 'check_url "$1"' _ '{}'
}

# Determine which files to check
if [ $# -eq 0 ]; then
    # No input file passed, check all root folder adoc files
    mapfile -d '' FILES < <(find . -maxdepth 1 -name "*.adoc" -type f -print0)
elif [ $# -eq 1 ]; then
    # Check input file
    FILES=("$1")
fi

BROKEN=0
for FILE in "${FILES[@]}"; do
    if ! run_url_checks "$FILE"; then
        BROKEN=1
    fi
done

if [ "$BROKEN" -ne 0 ]; then
  exit 1
else
  echo -e "\n✅ \033[32mAll links are valid!\033[0m"
fi
