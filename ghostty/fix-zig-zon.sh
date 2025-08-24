#!/bin/sh
set -e

# Fix .name fields in all build.zig.zon files
find . -name build.zig.zon | while read f; do
    # Replace .name = "foo-bar", with .name = .foo_bar,
    name=$(sed -n 's/.*\.name = "\([a-zA-Z0-9_-]*\)",.*/\1/p' "$f" | head -n1 | tr '-' '_')
    if [ -n "$name" ]; then
        sed "s/\.name = \"[a-zA-Z0-9_-]*\",/.name = .$name,/" "$f" > "$f.tmp" && mv "$f.tmp" "$f"
    fi
done

# Add fingerprint to main build.zig.zon if missing
if grep -q '^\.{' build.zig.zon && ! grep -q 'fingerprint' build.zig.zon; then
    awk 'NR==2{print "    .fingerprint = 0x64407a2a5e48abdf,"} 1' build.zig.zon > build.zig.zon.tmp && mv build.zig.zon.tmp build.zig.zon
fi
