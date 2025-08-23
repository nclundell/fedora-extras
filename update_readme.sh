#!/bin/bash

COPR_URL="https://copr.fedorainfracloud.org/coprs/nclundell/fedora-extras/packages/"
TMP_HTML=$(mktemp)
TMP_TABLE=$(mktemp)
TMP_BODY=$(mktemp)
TMP_ROWS=$(mktemp)

curl -s "$COPR_URL" > "$TMP_HTML"

# Extract the table with id="DataTables_Table_0"
awk '/<table[^>]*id="DataTables_Table_0"/,/<\/table>/' "$TMP_HTML" > "$TMP_TABLE"

# Now extract only the tbody section from that table
awk '/<tbody>/,/<\/tbody>/' "$TMP_TABLE" > "$TMP_BODY"

# Collapse each <tr>...</tr> to a single line for easier parsing
awk '/<tr /,/<\/tr>/' "$TMP_BODY" | tr -d '\n' | sed 's|</tr>|</tr>\n|g' > "$TMP_ROWS"

cat > README.md <<EOF
## 🐉 HERE BE DRAGONS 🐉
The package selection in this repository is subject to change at any time, based on my whimsy.

Use at your own risk!

## Packages and Copr Build Status

| Package   | Version   | Status |
|-----------|-----------|:------:|
EOF

# Now iterate over each row
while read -r row; do
    # Extract all <td>...</td> fields into an array
    tds=()
    while read -r td; do
        tds+=("$td")
    done < <(echo "$row" | grep -o '<td[^>]*>.*</td>')

    # Data from the Name column (first <td>)
    pkg_link=$(echo "${tds[0]}" | sed -n 's/.*<a href="\([^"]*\)">.*<\/a>.*/\1/p')
    pkg_name=$(echo "${tds[0]}" | sed -n 's/.*<a href="[^"]*">\([^<]*\)<\/a>.*/\1/p')
    pkg_url="https://copr.fedorainfracloud.org${pkg_link}"

    # Data from the Last Build Version column (second <td>)
    version=$(echo "${tds[1]}" | sed -n 's/.*<td[^>]*>\s*\([^<]*\)\s*<\/td>.*/\1/p' | xargs)

    # Data from the Last Build Status column (fourth <td>)
    status_text=$(echo "${tds[3]}" | grep -oE '(succeeded|failed|skipped|canceled|waiting|running)' | head -1)

    # Assign status_icon an emoji based on status_text
    case "$status_text" in
        succeeded) status_icon="✅" ;;
        failed)    status_icon="❌" ;;
        skipped)   status_icon="⏭️" ;;
        canceled)  status_icon="🚫" ;;
        waiting)   status_icon="⏳" ;;
        running)   status_icon="🏃" ;;
        *)         status_icon="❔" ;;
    esac

    # Print the Markdown table row
    echo "| [$pkg_name]($pkg_url) | $version | <div align=\"center\">$status_icon</div> |" >> README.md
done < $TMP_ROWS

rm "$TMP_HTML" "$TMP_TABLE" "$TMP_BODY" "$TMP_ROWS"
