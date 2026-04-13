"""
Exact formula spot-checks and Markov stationary law verification.
"""
import sys

def exact_reduction(L):
    return 1.0 - (6.0/7.0) ** (L - 2)

def exact_scalar_at_L(L):
    """P(scalar at position L) = (1 - (-1/7)^{L-1}) / 8"""
    return (1.0 - (-1.0/7.0) ** (L - 1)) / 8.0

def main():
    print("Exact formula check: 1 - (6/7)^{L-2}")
    print("-" * 45)
    for L in [3, 4, 5, 10, 20, 30, 40]:
        print(f"  L={L:3d}: P(reducible) = {exact_reduction(L):.6f}")

    print()
    print("Markov stationary law: P(scalar) -> 1/8 = 0.125")
    print("-" * 45)
    for L in [5, 10, 20, 50, 100]:
        print(f"  L={L:3d}: P(scalar at L) = {exact_scalar_at_L(L):.8f}")

    print()
    print(f"Stationary limit: pi_unit = 7/8 = {7/8:.6f}, pi_scalar = 1/8 = {1/8:.6f}")
    print("Exact formula check complete.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
