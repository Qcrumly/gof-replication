# gof-replication

Replication and validation suite for the **Graves Octonionic Framework (GOF)**.

Companion repository for: *Graves Octonionic Framework (GOF): Journeys, Anchor-Local Reduction, Parity-Sign Identity, and an Exact Reduction Law* by Quintin Crumly.

## Quick start
```bash
python -m pip install -r requirements.txt
pytest -q
python scripts/run_all.py --seed 123
```

Results land in `results/summary.json`.

## What's included

**Core engine** (`src/gof_validations.py`):
- Programmatic multiplication tables from the 7 oriented Fano triples
- Journey engine (unit_step, collapse, scalar_step)
- Parity invariant (two-term formula: #{backward} + #{collapses} mod 2)
- ALR normal form (anchored 3-block replacement)
- Bracket-aware journeys (tree evaluation for left/right/random association)

**Verification scripts** (`verification/`):
- `exact_formula_verify.py` — exhaustive enumeration confirming P(reducible) = 1 − (6/7)^{L−2} at L=3–8
- `exact_formula_check.py` — spot-checks of the exact formula and Markov stationary law P(scalar) → 1/8
- `associator_check.py` — full associator census: 42/168 split, magnitude 2, sign balance 84/84, W(𝕆) = 11/32
- `replay_logs.py` — deterministic replay and ALR parity invariance checks

**Panel runner** (`scripts/run_panel.py`):
- Length sweep across L ∈ {10, 20, 30, 40}
- Three bracketing modes: left, right, random
- Audit logging for every ALR deletion

**CI workflows** (`.github/workflows/`):
- `ci.yml` — runs tests and a small demo on every push
- `length_sweep.yml` — full panel matrix (manual dispatch)
- `panel.yml` — single panel + dashboard

## Key results verified by this repo

| Claim | Script / Test |
|-------|--------------|
| Exact reduction law: P(reducible) = 1 − (6/7)^{L−2} | `verification/exact_formula_verify.py` |
| Markov stationary law: P(scalar) → 1/8 | `verification/exact_formula_check.py` |
| Associator census: 42 zero, 168 nonzero, W = 11/32 | `verification/associator_check.py` |
| Parity invariance under ALR | `tests/test_brackets_alr.py` |
| Journey determinism and replay | `verification/replay_logs.py` |
| Panel statistics match exact formula | `scripts/run_panel.py` + CI artifacts |

## Running a panel

```bash
python scripts/run_panel.py \
  --length 30 \
  --samples 50000 \
  --seed 123 \
  --expr-mode random \
  --panel-out results/panel_random_L30.jsonl \
  --audit
```

## Dependencies

- Python ≥ 3.10
- pytest (see `requirements.txt`)
- matplotlib (optional; installed by CI for dashboard generation)

## License

CC BY-NC 4.0 — Non-commercial reuse with attribution. Commercial use requires permission from the author.

## Citation

Crumly, Q. (2026). *Graves Octonionic Framework (GOF): Journeys, Anchor-Local Reduction, Parity-Sign Identity, and an Exact Reduction Law.* Repository: https://github.com/Qcrumly/gof-replication
