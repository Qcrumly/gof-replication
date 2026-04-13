"""
Associator census verification (Proposition 3.7 and 3.8).
Checks:
  - 42 zero associators (on-line triples)
  - 168 nonzero associators (off-line triples)
  - All nonzero associators have magnitude exactly 2
  - Sign distribution: 84 positive, 84 negative
  - Association fidelity W(O) = 11/32
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.gof_validations import multiply_units, ORIENTED_TRIPLES

def octonion_multiply(i, j):
    """Multiply e_i * e_j. Returns (sign, index) where index=0 means scalar."""
    if i == 0:
        return (+1, j)
    if j == 0:
        return (+1, i)
    if i == j:
        return (-1, 0)
    s, k = multiply_units(i, j)
    return (s, k)

def associator_triple(a, b, c):
    """
    Compute [e_a, e_b, e_c] = (e_a e_b) e_c - e_a (e_b e_c).
    Returns the result as (sign, index) or (0, 0) if zero.
    Both products always land on the same basis element (possibly with opposite signs).
    """
    # Left association: (e_a * e_b) * e_c
    s1, k1 = octonion_multiply(a, b)
    if k1 == 0:
        # scalar * e_c
        s_left, idx_left = s1, c
    else:
        s2, k2 = octonion_multiply(k1, c)
        s_left, idx_left = s1 * s2, k2

    # Right association: e_a * (e_b * e_c)
    s3, k3 = octonion_multiply(b, c)
    if k3 == 0:
        s_right, idx_right = s3, a
    else:
        s4, k4 = octonion_multiply(a, k3)
        s_right, idx_right = s3 * s4, k4

    # Associator = left - right
    assert idx_left == idx_right, f"Products land on different basis elements: {idx_left} vs {idx_right}"

    diff_sign = s_left - s_right  # will be 0, +2, or -2
    return diff_sign, idx_left

def main():
    print("Associator Census (Proposition 3.7)")
    print("=" * 50)

    # Check all 210 ordered triples of distinct imaginary units
    zero_count = 0
    nonzero_count = 0
    positive_count = 0
    negative_count = 0
    magnitude_errors = 0

    for a in range(1, 8):
        for b in range(1, 8):
            for c in range(1, 8):
                if a == b or b == c or a == c:
                    continue
                diff, idx = associator_triple(a, b, c)
                if diff == 0:
                    zero_count += 1
                else:
                    nonzero_count += 1
                    if abs(diff) != 2:
                        magnitude_errors += 1
                    if diff > 0:
                        positive_count += 1
                    else:
                        negative_count += 1

    total = zero_count + nonzero_count
    print(f"Total distinct triples: {total} (expected 210)")
    print(f"Zero associators:    {zero_count} (expected 42)")
    print(f"Nonzero associators: {nonzero_count} (expected 168)")
    print(f"Magnitude errors:    {magnitude_errors} (expected 0)")
    print(f"Positive:            {positive_count} (expected 84)")
    print(f"Negative:            {negative_count} (expected 84)")
    print(f"f_fund = {nonzero_count}/{total} = {nonzero_count/total:.4f} (expected 4/5 = 0.8000)")

    assert total == 210
    assert zero_count == 42
    assert nonzero_count == 168
    assert magnitude_errors == 0
    assert positive_count == 84
    assert negative_count == 84

    print()
    print("Association Fidelity W(O) (Proposition 3.8)")
    print("=" * 50)

    # All 8^3 = 512 triples including e_0 = 1
    agree = 0
    disagree = 0
    for i in range(8):
        for j in range(8):
            for k in range(8):
                # Left: (e_i e_j) e_k
                s1, k1 = octonion_multiply(i, j)
                if k1 == 0:
                    s_left, idx_left = octonion_multiply(0, k)
                    s_left = s1 * s_left
                else:
                    s2, k2 = octonion_multiply(k1, k)
                    s_left, idx_left = s1 * s2, k2

                # Right: e_i (e_j e_k)
                s3, k3 = octonion_multiply(j, k)
                if k3 == 0:
                    s_right, idx_right = octonion_multiply(i, 0)
                    s_right = s3 * s_right
                else:
                    s4, k4 = octonion_multiply(i, k3)
                    s_right, idx_right = s3 * s4, k4

                assert idx_left == idx_right
                if s_left == s_right:
                    agree += 1
                else:
                    disagree += 1

    W = (agree - disagree) / 512
    print(f"Associative triples: {agree} (expected 344)")
    print(f"Non-associative:     {disagree} (expected 168)")
    print(f"W(O) = ({agree} - {disagree}) / 512 = {W:.10f}")
    print(f"Expected: 11/32 = {11/32:.10f}")

    assert agree == 344
    assert disagree == 168
    assert W == 11/32

    print()
    print("ALL CHECKS PASSED.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
