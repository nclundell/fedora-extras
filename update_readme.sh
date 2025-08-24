#!/bin/bash

COPR_URL="https://copr.fedorainfracloud.org/coprs/nclundell/fedora-extras/packages/"
TMP_HTML=$(mktemp)
TMP_ROWS=$(mktemp)

# Get the HTML content
curl -s "$COPR_URL" | tr '\n' ' ' > "$TMP_HTML"

# Extract data rows from the package table
perl -0777 -ne '
    while (/<table[^>]*class="[^"]*datatable[^"]*dataTable[^"]*"[^>]*>.*?<\/table>/gs) {
        my $table = $&;
        while ($table =~ /<tr[^>]*>.*?<td.*?<\/td>.*?<\/tr>/gs) {
            print "$&\n";
        }
    }
' "$TMP_HTML" > "$TMP_ROWS"

# Prepare README.md with header
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
    [ -z "$row" ] && continue  # Skip blank lines

    # Extract all <td>...</td> fields into an array, robust to newlines
    mapfile -t tds < <(echo "$row" | perl -nle 'print for /<td[^>]*>.*?<\/td>/gs')

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

rm "$TMP_HTML" "$TMP_ROWS"
