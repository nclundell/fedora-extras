#!/bin/sh

cat > README.md <<EOF
## 🐉 HERE BE DRAGONS 🐉

**⚠️ Warning: ⚠️**
The package selection in this repository is subject to change at any time, based on my whimsy.
Use at your own risk!

## Packages and Copr Build Status

| Package   | Version   | Status |
|-----------|-----------|:------:|


## Packages and Copr Build Status

| Package   | Version   | Status |
|-----------|-----------|:------:|
EOF

for spec in */*.spec; do
    name=$(awk '/^Name:/ {print $2}' "$spec")
    version=$(awk '/^Version:/ {print $2}' "$spec")
    url="https://copr.fedorainfracloud.org/coprs/nclundell/fedora-extras/package/$name/"
    # You may want to set status manually, or default to ✅
    status='<div align="center">✅</div>'
    echo "| [$name]($url) | v$version | $status |" >> README.md
done
