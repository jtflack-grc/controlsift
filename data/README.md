# Data

- `raw/` — points to scenario YAML + generator as the unchanged source material (no private corpora)
- `scenarios/scenario_families.yaml` — generation templates
- `processed/*.jsonl` — train / validation / test / challenge
- `manifests/dataset_manifest.json` — hashes and counts
- `review_log.csv` — label audit tracking (structural + spot-check; not full human gold)

All evidence is synthetic. Never commit real organizational evidence.
