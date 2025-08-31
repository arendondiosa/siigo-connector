#!/bin/bash

set -e

uv version --bump patch
uv build
V="$(uv version --short)"
TAG="v$V"
git tag "$TAG"
git push origin "$TAG"
