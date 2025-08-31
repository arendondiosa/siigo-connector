#!/bin/bash

set -e

uv build
V="$(uv version --short)"                 # e.g. 0.1.4rc1
TAG="v$(echo "$V" | sed -E 's/rc([0-9]+)$/-rc\1/')"
git tag "$TAG"
git push origin "$TAG"
