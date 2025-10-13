#!/bin/bash
# Use in the CI to create index.html and build AsciiDoctor output

set -euo pipefail

# Copy images to out/
mkdir -p out/
cp -r images/ out/

# Create index.html
mkdir -p out
cat << 'EOF' > out/index.html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Open Data Hub docs</title>
  </head>
  <body>
    <ul>
EOF

# Loop over each first-level asciidoc assembly
for file in *.adoc; do
  if [ -f "$file" ]; then
    name=${file%.adoc}
    # Convert "file_name" > "File Name"
    display=$(echo "$name" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++){ $i=toupper(substr($i,1,1)) substr($i,2) } print}')
    echo "      <li><a href=\"${name}/index.html\">${display}</a></li>" >> out/index.html

    mkdir -p "out/${name}"
    asciidoctor \
      -a toc=left \
      -a doctype=book \
      -a allow-uri-read \
      -a sectanchors \
      -a skip-front-matter \
      "${file}" \
      -o "out/${name}/index.html"
  fi
done

# Close index.html
cat << 'EOF' >> out/index.html
    </ul>
  </body>
</html>
EOF
