"""
Exhaustive verification of the exact reduction law.
For L=3..8, enumerate all 7^L chains, run left-fold evaluation,
check for at least one non-terminal collapse, and compare
the reducible fraction to 1 - (6/7)^{L-2}.
"""
import itertools
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.gof_validations import State, step_token

def has_nonterminal_collapse(start_unit, chain):
    """Check if any non-terminal position produces a collapse."""
    state = State.unit(start_unit)
    for i, j in enumerate(chain):
        tok, state = step_token(state, j)
        if tok.ttype == "collapse" and i < len(chain) - 1:
            return True
    return False

def exact_formula(L):
    return 1.0 - (6.0/7.0) ** (L - 2)

def main():
    print("Exact Reduction Law — Exhaustive Verification")
    print("=" * 55)
    all_pass = True
    for L in range(3, 9):
        total = 0
        reducible = 0
        for start in range(1, 8):
            for chain in itertools.product(range(1, 8), repeat=L):
                total += 1
                if has_nonterminal_collapse(start, list(chain)):
                    reducible += 1
        empirical = reducible / total
        predicted = exact_formula(L)
        match = abs(empirical - predicted) < 1e-10
        status = "PASS" if match else "FAIL"
        if not match:
            all_pass = False
        print(f"L={L}: empirical={empirical:.10f}, exact={predicted:.10f}, diff={abs(empirical-predicted):.2e} [{status}]")
    print()
    if all_pass:
        print("ALL LENGTHS PASS — exact formula verified to full precision.")
    else:
        print("SOME LENGTHS FAILED — check implementation.")
    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(main())
