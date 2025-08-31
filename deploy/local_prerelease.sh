#!/bin/bash

set -e

uv version --bump rc
uv build
V="$(uv version --short)"
TAG="v$(echo "$V" | sed -E 's/rc([0-9]+)$/-rc\1/')"
git tag "$TAG"
git push origin "$TAG"
uv publish --publish-url https://test.pypi.org/legacy/ --token "<pypi-token>"
