from __future__ import annotations
import argparse
import json
import random
from pathlib import Path
from typing import List

from src.gof_validations import (
    State,
    tokens_from_expr,
    tokens_random_tree,
    full_alr,
    journey_parity,
    step_token,
    parse_parenthesized,
    eval_tree,
)


def _tokens_left(start_unit: int, chain: List[int]):
    state = State.unit(start_unit)
    tokens = []
    for j in chain:
        tok, state = step_token(state, j)
        tokens.append(tok)
    return tokens


def _tokens_right(start_unit: int, chain: List[int]):
    if not chain:
        return []
    expr = str(chain[-1])
    for val in reversed(chain[:-1]):
        expr = f"({val} x {expr})"
    expr = f"({start_unit} x {expr})"
    return tokens_from_expr(start_unit, expr)


def _token_stream(mode: str, seed: int, length: int, samples: int, expr_file: Path | None):
    rng = random.Random(seed)
    if mode == "fromfile":
        if expr_file is None:
            raise ValueError("--expr-file required for fromfile mode")
        for raw in expr_file.read_text().splitlines():
            line = raw.strip()
            if not line:
                continue
            tree = parse_parenthesized(line)
            node = tree
            while isinstance(node, tuple):
                node = node[1]
            if not isinstance(node, int):
                raise ValueError("Invalid expression in file")
            start = node
            tokens, _ = eval_tree(State.unit(start), tree)
            yield start, tokens
        return

    generators = {
        "left": _tokens_left,
        "right": _tokens_right,
        "random": lambda start_unit, chain: tokens_random_tree(start_unit, chain, rng),
    }
    gen = generators.get(mode)
    if gen is None:
        raise ValueError(f"Unsupported mode {mode}")

    for _ in range(samples):
        start = rng.randint(1, 7)
        chain = [rng.randint(1, 7) for _ in range(length)]
        if not chain:
            yield start, []
            continue
        tokens = gen(start, chain)
        yield start, tokens


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--length", type=int, default=30)
    parser.add_argument("--samples", type=int, default=20000)
    parser.add_argument("--expr-mode", choices=["left", "right", "random", "fromfile"], default="random")
    parser.add_argument("--panel-out", type=str, default=None)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--expr-file", type=str, default=None)
    args = parser.parse_args()

    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)

    if args.panel_out:
        panel_path = Path(args.panel_out)
    else:
        panel_path = out_dir / f"panel_{args.expr_mode}_L{args.length}_N{args.samples}.jsonl"

    survivor_count = 0
    even_parity = 0
    total_deleted = 0
    parity_preserve = 0
    processed = 0

    with panel_path.open("w", encoding="utf-8") as handle:
        for start, tokens in _token_stream(
            args.expr_mode,
            args.seed,
            args.length,
            args.samples,
            Path(args.expr_file) if args.expr_file else None,
        ):
            processed += 1
            parity_before = journey_parity(tokens, State.unit(start))
            nf_tokens, audit = full_alr(tokens, State.unit(start))
            parity_after = journey_parity(nf_tokens, State.unit(start))
            parity_preserve += int(parity_before == parity_after)
            survivor_count += int(len(nf_tokens) == len(tokens))
            even_parity += int(parity_before == 0)
            deleted_triplets = (len(tokens) - len(nf_tokens)) // 3
            total_deleted += deleted_triplets

            record = {
                "start": start,
                "len_tokens": len(tokens),
                "len_nf": len(nf_tokens),
                "deleted_triplets": deleted_triplets,
                "parity0": parity_before,
                "parity1": parity_after,
            }
            if args.audit and audit:
                record["audit"] = audit
            handle.write(json.dumps(record) + "\n")

    if processed == 0:
        raise RuntimeError("No samples generated")

    summary = {
        "mode": args.expr_mode,
        "length": args.length,
        "samples": processed,
        "reduced_frac": 1.0 - (survivor_count / processed),
        "survivor_frac": survivor_count / processed,
        "parity_even_frac": even_parity / processed,
        "mean_deleted_triplets": total_deleted / processed,
        "preserve_parity_rate": parity_preserve / processed,
    }

    summary_path = out_dir / f"panel_summary_{args.expr_mode}_L{args.length}_N{args.samples}.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("Summary:", json.dumps(summary, indent=2))
    print("Wrote:", panel_path)


if __name__ == "__main__":
    main()
