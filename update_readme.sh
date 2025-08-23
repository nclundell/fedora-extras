#!/bin/sh

cat > README.md <<EOF
## 🐉 HERE BE DRAGONS 🐉

**⚠️ Warning ⚠️**
The package selection in this repository is subject to change at any time, based on my whimsy.
Use at your own risk!

## Packages and Copr Build Status

| Package   | Version   | Status |
|-----------|-----------|:------:|
EOF

# Fetch package info from Copr API once
api_json=$(curl -s "$COPR_API")

for spec in */*.spec; do
    name=$(awk '/^Name:/ {print $2}' "$spec")
    version=$(awk '/^Version:/ {print $2}' "$spec")
    url="https://copr.fedorainfracloud.org/coprs/nclundell/fedora-extras/package/$name/"

    # Extract last_build_status for this package from API JSON
    status_raw=$(echo "$api_json" | jq -r --arg pkg "$name" '.packages[] | select(.name==$pkg) | .last_build_status')
    case "$status_raw" in
        "succeeded") status_icon="✅" ;;
        "failed")    status_icon="❌" ;;
        "skipped")   status_icon="⏭️" ;;
        "canceled")  status_icon="🚫" ;;
        "waiting")   status_icon="⏳" ;;
        "running")   status_icon="🏃" ;;
        *)           status_icon="❔" ;;
    esac

    status="<div align=\"center\">$status_icon</div>"
    echo "| [$name]($url) | v$version | $status |" >> README.md
done
