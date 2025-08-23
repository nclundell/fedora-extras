#!/bin/sh

git config --global user.name "github-actions[bot]"
git config --global user.email "github-actions[bot]@users.noreply.github.com"

for spec in */*.spec; do
    # Skip if "# skip update" is in the first line
    if head -n 1 "$spec" | grep -qi '# *skip update'; then
        echo "Skipping $spec (skip update present on first line)"
        continue
    fi

    name=$(awk '/^Name:/ {print $2}' "$spec")
    version=$(awk '/^Version:/ {print $2}' "$spec")
    url=$(awk '/^URL:/ {print $2}' "$spec")

    repo=$(echo "$url" | sed -n 's|https://github.com/\([^/]\+\)/\([^/]\+\).*|\1/\2|p')
    if [ -z "$repo" ]; then
        msg="Could not parse repo from URL in $spec"
        echo "$msg"
        # Create issue if not exists
        if ! gh issue list --state open --search "$name: $msg" | grep -q "$msg"; then
            gh issue create --title "$name: $msg" --body "$msg"
        fi
        continue
    fi

    latest=$(curl -s "https://api.github.com/repos/$repo/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v?([^"]+)".*/\1/')
    if [ -z "$latest" ]; then
        latest=$(curl -s "https://api.github.com/repos/$repo/tags" | grep '"name":' | head -1 | sed -E 's/.*"v?([^"]+)".*/\1/')
    fi

    if [ -z "$latest" ]; then
        msg="Could not fetch latest version for $name ($repo)"
        echo "$msg"
        if ! gh issue list --state open --search "$name: $msg" | grep -q "$msg"; then
            gh issue create --title "$name: $msg" --body "$msg"
        fi
        continue
    fi

    if [ "$version" != "$latest" ]; then
        branch="update-${name}-to-v${latest}"
        echo "Updating $name: $version -> $latest (branch $branch)"
        git checkout -b "$branch"
        sed -i "s/^Version:.*/Version: $latest/" "$spec"
        git add "$spec"
        git commit -m "Update $name spec to v$latest"
        git push origin "$branch" || {
            msg="Failed to push branch $branch for $name"
            echo "$msg"
            if ! gh issue list --state open --search "$name: $msg" | grep -q "$msg"; then
                gh issue create --title "$name: $msg" --body "$msg"
            fi
            git checkout main
            git branch -D "$branch"
            continue
        }
        gh pr create --fill --title "Update $name to v$latest" --body "Automated update of $name spec from $version to $latest."
        git checkout main
        git branch -D "$branch"
    else
        echo "$name is up to date (version $version)"
    fi
done
