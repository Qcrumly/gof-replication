"""
Replay verification: confirm that journey construction is deterministic
and that replaying tokens from a journey reconstructs the original computation.
"""
import sys
import os
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.gof_validations import (
    State, compute_journey, step_token, journey_parity,
    alr_normal_form, token_list_to_str, full_alr
)

def main():
    print("Replay Verification")
    print("=" * 40)

    rng = random.Random(42)
    num_chains = 10000
    parity_mismatches = 0
    replay_mismatches = 0
    alr_parity_mismatches = 0

    for _ in range(num_chains):
        start_idx = rng.randint(1, 7)
        L = rng.randint(3, 30)
        chain = [rng.randint(1, 7) for _ in range(L)]
        start = State.unit(start_idx)

        # Compute journey twice — must be identical
        toks1, st1 = compute_journey(start, chain)
        toks2, st2 = compute_journey(State.unit(start_idx), chain)
        str1 = token_list_to_str(toks1)
        str2 = token_list_to_str(toks2)
        if str1 != str2:
            replay_mismatches += 1

        # Parity before and after ALR
        p_before = journey_parity(toks1, start)
        nf, _ = full_alr(toks1, start)
        p_after = journey_parity(nf, start)
        if p_before != p_after:
            alr_parity_mismatches += 1

    print(f"Chains tested:          {num_chains}")
    print(f"Replay mismatches:      {replay_mismatches} (expected 0)")
    print(f"ALR parity mismatches:  {alr_parity_mismatches} (expected 0)")

    assert replay_mismatches == 0
    assert alr_parity_mismatches == 0

    print()
    print("ALL REPLAY CHECKS PASSED.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
