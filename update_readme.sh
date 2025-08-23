#!/bin/sh

COPR_URL="https://copr.fedorainfracloud.org/coprs/nclundell/fedora-extras/packages/"
TMP_HTML=$(mktemp)

curl -s "$COPR_URL" > "$TMP_HTML"

cat > README.md <<EOF
## 🐉 HERE BE DRAGONS 🐉

### ⚠️ Warning ⚠️
The package selection in this repository is subject to change at any time, based on my whimsy.
Use at your own risk!

## Packages and Copr Build Status

| Package   | Version   | Status |
|-----------|-----------|:------:|
EOF

for spec in */*.spec; do
    name=$(awk '/^Name:/ {print $2}' "$spec")
    # Find the table row for this package
    row=$(awk -v pkg="$name" 'BEGIN{IGNORECASE=1}/<tr/{inrow=0}/<td[^>]*>'pkg'<\/td>/{inrow=1; print; next} inrow && /<\/tr>/{print; exit} inrow{print}' "$TMP_HTML" | tr '\n' ' ')
    # Extract last build version (second <td>), and last build status (fourth <td>)
    last_build_version=$(echo "$row" | sed -n 's/.*<td[^>]*>[^<]*<\/td><td[^>]*>\([^<]*\)<\/td>.*/\1/p')
    last_build_status=$(echo "$row" | sed -n 's/.*<td[^>]*>[^<]*<\/td><td[^>]*>[^<]*<\/td><td[^>]*>[^<]*<\/td><td[^>]*>\([^<]*\)<\/td>.*/\1/p')
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

rm "$TMP_HTML"
