---
description: Publish iil-weltenfw to PyPI
---

# Release — PyPI Publish

## Build + Publish

```bash
bash ~/github/platform/scripts/publish-package.sh ~/github/weltenfw
```

## Test-Upload

```bash
bash ~/github/platform/scripts/publish-package.sh ~/github/weltenfw --test
```

## Verify

```bash
pip index versions iil-weltenfw 2>/dev/null | head -3
```
