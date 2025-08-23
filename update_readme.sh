#!/bin/bash

COPR_URL="https://copr.fedorainfracloud.org/coprs/nclundell/fedora-extras/packages/"
TMP_HTML=$(mktemp)
TMP_TABLE=$(mktemp)

curl -s "$COPR_URL" > "$TMP_HTML"

# Extract the table with id="DataTables_Table_0"
awk '/<table[^>]*id="DataTables_Table_0"/,/<\/table>/' "$TMP_HTML" > "$TMP_TABLE"

 # Collapse each <tr>...</tr> to a single line for easier parsing
awk '/<tr /,/<\/tr>/' "$TMP_TABLE" | tr -d '\n' | sed 's|</tr>|</tr>\n|g' > "$TMP_TABLE.rows"

cat > README.md <<EOF
## 🐉 HERE BE DRAGONS 🐉

**⚠️ Warning ⚠️**
The package selection in this repository is subject to change at any time, based on my whimsy.
Use at your own risk!

## Packages and Copr Build Status

| Package   | Version   | Status |
|-----------|-----------|:------:|
EOF

for spec in */*.spec; do
    name=$(awk '/^Name:/ {print $2}' "$spec")
    # Find the row for this package (look for <a ...>name</a>)
    row=$(grep -i "<a [^>]*>$name</a>" "$TMP_TABLE.rows")
    if [ -z "$row" ]; then
        last_build_version=""
        last_build_status=""
        status_icon="❔"
    else
        # Extract all <td>...</td> fields
        IFS=$'\n' read -rd '' -a tds <<<"$(echo "$row" | grep -o '<td[^>]*>.*</td>' | sed 's/<[^>]*>//g')"
        last_build_version=$(echo "${tds[1]}" | xargs)
        last_build_status=$(echo "${tds[3]}" | awk '{print $NF}' | xargs)
        case "$last_build_status" in
            succeeded) status_icon="✅" ;;
            failed)    status_icon="❌" ;;
            skipped)   status_icon="⏭️" ;;
            canceled)  status_icon="🚫" ;;
            waiting)   status_icon="⏳" ;;
            running)   status_icon="🏃" ;;
            *)         status_icon="❔" ;;
        esac
    fi
    url="https://copr.fedorainfracloud.org/coprs/nclundell/fedora-extras/package/$name/"
    status="<div align=\"center\">$status_icon</div>"
    echo "| [$name]($url) | $last_build_version | $status |" >> README.md
done

rm "$TMP_HTML" "$TMP_TABLE" "$TMP_TABLE.rows"
