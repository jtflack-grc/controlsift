# Git tags vs HEAD

## `protocol-v1-locked`

**What it seals:** dataset v1.1.0 split hashes, canonical seed `42`, primary metric macro F1, model id, and the frozen prompt module path - as recorded in `governance/PROTOCOL_SEAL.json`.

**What it isn't:** a freeze of every later documentation, site-copy, or portfolio honesty fix.

| Ref | Role |
|-----|------|
| Tag `protocol-v1-locked` | Evaluation contract + data hashes (don't move) |
| Branch `master` / HEAD | May advance with docs, site, packaging, audit notes that **don't** relabel sealed splits or edit the frozen prompt |

If you need a new dataset or prompt, cut **dataset v1.2+** and a new protocol tag. Don't retcon `protocol-v1-locked`.

## Future tags

| Tag | When |
|-----|------|
| `v1.0.0` | After Gemma ladder metrics exist and public claims are backed by `results/` JSON |
| `protocol-v1.2-*` | Only if a new sealed surface (e.g. prose-hardened packets) is intentionally opened |
