# gof-replication

Replication and validation suite for the Graves Octonionic Framework (GOF).

## Quick start
```bash
python -m pip install -r requirements.txt
pytest -q
python scripts/run_all.py --seed 123
```

Results land in `results/summary.json`.

Dependencies: see `requirements.txt` (pytest, matplotlib). No pandas required.

## What’s included
- Programmatic tables from the 7 oriented Fano triples
- Journey engine (unit_step, collapse, scalar_step)
- Parity invariant
- Minimal ALR normal form (anchored 3-block delete)
- Sanity Monte Carlo (lambda, p0, survivor upper bound)

Now included:
- Bracket-aware journeys (tree evaluation)
- Full ALR with audit log
- Larger Monte Carlo panel + dashboard plots

## New commands
Run a panel and create summary:
```bash
python scripts/run_panel.py \
  --length 30 \
  --samples 50000 \
  --seed 123 \
  --expr-mode random \
  --panel-out results/panel_random_L30.jsonl \
  --audit
```

Build dashboard images:
```bash
python scripts/dashboard.py
```

### Results & artifacts
Large outputs (JSONL/PNGs) are not committed to the repo. The CI workflows produce them and upload as downloadable Artifacts in the GitHub Actions run.
