#!/bin/bash
#
# Checks for 404 links using Asciidoctor and curl

usage() {
    echo "Usage: $0 [<adoc_file>]"
    exit 1
}

# Parse arguments
INPUT_FILE=""

# Check dependencies
if ! asciidoctor -v >/dev/null 2>&1; then
    echo "Error: Asciidoctor is not installed" >&2
    exit 1
fi

INPUT_FILE="$1"

if [ $# -eq 0 ]; then
    usage
fi

# Create temp file for flagging broken links
TMP_FILE=$(mktemp)
echo "0" > "$TMP_FILE"

# Load ignore patterns from external file
IGNORE_FILE="$(dirname "$0")/links.ignore"

if [ ! -f "$IGNORE_FILE" ]; then
    echo "Error: Missing ignore patterns file: $IGNORE_FILE" >&2
    exit 1
fi

mapfile -t IGNORE_PATTERNS < "$IGNORE_FILE"
PATTERNS_DECL=$(declare -p IGNORE_PATTERNS)

check_url() {
    local URL=$1
    eval "$PATTERNS_DECL"

    URL=${URL%[.,;:?!\]\)]}

    for PATTERN in "${IGNORE_PATTERNS[@]}"; do
        if [[ "$URL" =~ $PATTERN ]]; then
            exit 0
        fi
    done

    STATUS=$(curl -Ls -o /dev/null -w "%{http_code}" --max-time 5 --connect-timeout 2 "$URL")

    if [[ "$STATUS" != "000" && "$STATUS" != "403" && ! "$STATUS" =~ ^(2|3)[0-9]{2}$ ]]; then
        echo -e "Invalid URL (HTTP status $STATUS): \n\033[31m$URL\033[0m"
        echo "1" > "$TMP_FILE"
    fi
}

export TMP_FILE
export -f check_url

run_url_checks() {
    local FILE="$1"
    echo -e "\033[32mChecking: $FILE\033[0m"
    asciidoctor "$FILE" -a doctype=book -o - | \
        grep -Eo '(http|https)://[a-zA-Z0-9./?=%_-]*' | \
        sort -u | \
        xargs -P 10 -n 1 bash -c "$PATTERNS_DECL; check_url \"\$0\""
}

run_url_checks "$INPUT_FILE"

if [ "$(cat "$TMP_FILE")" -eq 1 ]; then
    echo "Errors found"
    exit 1
fi
