#!/bin/sh

COPR_URL="https://copr.fedorainfracloud.org/coprs/nclundell/fedora-extras/packages/"
TMP_HTML=$(mktemp)

curl -s "$COPR_URL" > "$TMP_HTML"

cat > README.md <<EOF
## 🐉 HERE BE DRAGONS 🐉

⚠️ Warning ⚠️
The package selection in this repository is subject to change at any time, based on my whimsy.

Use at your own risk!

## Packages and Copr Build Status

| Package   | Version   | Status |
|-----------|-----------|:------:|
EOF

# Collapse each <tr>...</tr> to a single line for easier parsing
awk '/<tr /,/<\/tr>/' "$TMP_HTML" | tr -d '\n' | sed 's|</tr>|</tr>\n|g' > "$TMP_HTML.rows"

for spec in */*.spec; do
    name=$(awk '/^Name:/ {print $2}' "$spec")
    # Find the row for this package
    row=$(grep -i "<td[^>]*>$name</a></b></td>" "$TMP_HTML.rows")
    if [ -z "$row" ]; then
        # fallback: try matching just the name
        row=$(grep -i "<td[^>]*>$name" "$TMP_HTML.rows")
    fi
    # Extract version (second <td>)
    last_build_version=$(echo "$row" | sed -n 's/.*<td[^>]*>[^<]*<\/td><td[^>]*>\([^<]*\)<\/td>.*/\1/p' | xargs)
    # Extract status text (fourth <td>)
    last_build_status=$(echo "$row" | sed -n 's/.*<td[^>]*>[^<]*<\/td><td[^>]*>[^<]*<\/td><td[^>]*>[^<]*<\/td><td[^>]*>[^<]*<span[^>]*>[^<]*<\/span> *\([^< ]*\).*/\1/p')
    case "$last_build_status" in
        succeeded) status_icon="✅" ;;
        failed)    status_icon="❌" ;;
        skipped)   status_icon="⏭️" ;;
        canceled)  status_icon="🚫" ;;
        waiting)   status_icon="⏳" ;;
        running)   status_icon="🏃" ;;
        *)         status_icon="❔" ;;
    esac
    url="https://copr.fedorainfracloud.org/coprs/nclundell/fedora-extras/package/$name/"
    status="<div align=\"center\">$status_icon</div>"
    echo "| [$name]($url) | $last_build_version | $status |" >> README.md
done

rm "$TMP_HTML" "$TMP_HTML.rows"
