# UV Version Bump Options

Here are the different bump options and what they would produce:

## Stable Version Bumps

``` bash
# Patch version (0.1.4 → 0.1.5)
uv version --bump patch

# Minor version (0.1.4 → 0.2.0)
uv version --bump minor

# Major version (0.1.4 → 1.0.0)
uv version --bump major

# Stable (same as patch - 0.1.4 → 0.1.5)
uv version --bump stable
```

## Pre-release Bumps

```bash
# Alpha (0.1.4 → 0.1.5a1)
uv version --bump alpha

# Beta (0.1.4 → 0.1.5b1)
uv version --bump beta

# Release Candidate (0.1.4 → 0.1.5rc1)
uv version --bump rc

# Post-release (0.1.4 → 0.1.4.post1)
uv version --bump post

# Development (0.1.4 → 0.1.5.dev1)
uv version --bump dev
```
