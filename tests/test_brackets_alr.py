from src.gof_validations import (
    State,
    compute_journey,
    parse_parenthesized,
    eval_tree,
    tokens_from_expr,
    tokens_random_tree,
    full_alr,
    token_list_to_str,
)
import random


def test_parse_and_eval_tree():
    tree = parse_parenthesized("((1 x 2) x 4)")
    tokens, final_state = eval_tree(State.unit(1), tree)
    left_tokens, left_state = compute_journey(State.unit(1), [2, 4])
    assert token_list_to_str(tokens) == token_list_to_str(left_tokens)
    assert final_state.kind == left_state.kind and final_state.sign == left_state.sign


def test_tokens_from_expr_right_assoc():
    toks = tokens_from_expr(1, "(1 x (2 x (4 x 6)))")
    tree = parse_parenthesized("(1 x (2 x (4 x 6)))")
    direct, _ = eval_tree(State.unit(1), tree)
    assert token_list_to_str(toks) == token_list_to_str(direct)


def test_tokens_random_tree_reproducible():
    rng = random.Random(123)
    chain = [2, 4, 6]
    toks = tokens_random_tree(1, chain, rng)
    assert len(toks) == len(chain)


def test_full_alr_deletes_block_and_preserves_parity():
    start = State.unit(1)
    toks, _ = compute_journey(start, [2, 4, 3])
    nf, audit = full_alr(toks, start)
    assert nf == []
    assert audit and audit[0]["before"] == token_list_to_str(toks)
