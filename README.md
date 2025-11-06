# gof-replication

Replication and validation suite for the Graves Octonionic Framework (GOF).

## Quick start
```bash
python -m pip install -r requirements.txt
pytest -q
python scripts/run_all.py --seed 123


Results land in results/summary.json.

What’s included

Programmatic tables from the 7 oriented Fano triples

Journey engine (unit_step, collapse, scalar_step)

Parity invariant

Minimal ALR normal form (anchored 3-block delete)

Sanity Monte Carlo (lambda, p0, survivor upper bound)

Next steps (roadmap)

Bracket-aware journeys (tree evaluation)

Full ALR with audit log

Larger Monte Carlo panel + plots
