#!/usr/bin/env bash
set -euo pipefail

uv version --bump patch
V="$(uv version --short)"
TAG="v$V"

# Commit the version bump
git add pyproject.toml            # add uv.lock too if you track it
# git add uv.lock || true
git commit -m "chore(release): $TAG"

# (optional) build locally; CI will build again
uv build

# Create an annotated tag on the NEW commit
git tag -a "$TAG" -m "Release $TAG"

# Push the commit and the tag together
git push origin HEAD --follow-tags
