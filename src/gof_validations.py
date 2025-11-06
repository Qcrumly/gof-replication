# gof_validations.py — core validation/replication module
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
import random, re

# Single source of truth: oriented Fano triples
ORIENTED_TRIPLES = [
    (1,2,4),
    (2,3,5),
    (3,4,6),
    (4,5,7),
    (5,6,1),
    (6,7,2),
    (7,1,3),
]

# Build lookup maps
_FORWARD = {}
_BACKWARD = {}
_DIM = {}
for d,(a,b,c) in enumerate(ORIENTED_TRIPLES, start=1):
    for (x,y,z) in [(a,b,c),(b,c,a),(c,a,b)]:
        _FORWARD[(x,y)] = (z,d)
        _DIM[(x,y)] = d
        _DIM[(y,x)] = d
    for (x,y,z) in [(b,a,c),(c,b,a),(a,c,b)]:
        _BACKWARD[(x,y)] = (z,d)
        _DIM[(x,y)] = d

def build_tables():
    DIM = [[0]*8 for _ in range(8)]
    RES = [[[0]*8 for _ in range(8)] for _ in range(8)]  # RES[d][i][j]
    SGN = [[[0]*8 for _ in range(8)] for _ in range(8)]  # SGN[d][i][j]
    for i in range(1,8):
        DIM[i][i] = 0
        RES[0][i][i] = 0
        SGN[0][i][i] = -1
    for d,(a,b,c) in enumerate(ORIENTED_TRIPLES, start=1):
        for (x,y,z) in [(a,b,c),(b,c,a),(c,a,b)]:
            DIM[x][y] = d; RES[d][x][y] = z; SGN[d][x][y] = +1
        for (x,y,z) in [(b,a,c),(c,b,a),(a,c,b)]:
            DIM[x][y] = d; RES[d][x][y] = z; SGN[d][x][y] = -1
    return DIM, RES, SGN

def multiply_units(i:int, j:int) -> Tuple[int,int]:
    if i == j:
        return (-1, 0)  # -1 scalar
    if (i,j) in _FORWARD:
        k,_ = _FORWARD[(i,j)]
        return (+1, k)
    if (i,j) in _BACKWARD:
        k,_ = _BACKWARD[(i,j)]
        return (-1, k)
    raise ValueError("Units not connected on a Fano line")

@dataclass
class State:
    kind: str   # "unit" | "scalar"
    sign: int   # +1|-1
    idx: int    # 1..7 for unit, 0 for scalar
    @staticmethod
    def unit(i:int, sign:int=+1): return State("unit", +1 if sign>=0 else -1, i)
    @staticmethod
    def scalar(sign:int=+1): return State("scalar", +1 if sign>=0 else -1, 0)

@dataclass
class Token:
    ttype: str             # "unit_step" | "collapse" | "scalar_step"
    dim: int               # 1..7, 0 collapse, -1 scalar_step
    mult: int              # multiplicand 1..7
    forward: Optional[bool]=None
    produced_unit: Optional[int]=None
    result_sign: Optional[int]=None

def _abs_mult(i:int, j:int):
    if i==j: return (0,0,-1)
    if (i,j) in _FORWARD:  k,d = _FORWARD[(i,j)]; return (d,k,+1)
    if (i,j) in _BACKWARD: k,d = _BACKWARD[(i,j)]; return (d,k,-1)
    raise ValueError

def step_token(st:State, j:int):
    if st.kind=="scalar":
        ns = State.unit(j, st.sign)
        return Token("scalar_step",-1,j,None,j,ns.sign), ns
    if st.idx==j:
        ns = State.scalar(-st.sign)
        return Token("collapse",0,j,None,0,ns.sign), ns
    d,k,s = _abs_mult(st.idx, j)
    ns = State.unit(k, st.sign*s)
    return Token("unit_step",d,j,(s==+1),k,ns.sign), ns

def compute_journey(start:State, chain:List[int]):
    st = start; toks=[]
    for j in chain:
        t, st = step_token(st,j)
        toks.append(t)
    return toks, st

def journey_parity(tokens:List[Token], start:State)->int:
    p=0; st=start
    for t in tokens:
        if t.ttype=="collapse": p^=1; st=State.scalar(-st.sign)
        elif t.ttype=="scalar_step": 
            if st.kind!="scalar": raise ValueError("scalar_step from unit")
            if st.sign<0: p^=1
            st=State.unit(t.mult, st.sign)
        else:  # unit_step
            if t.forward is False: p^=1
            st=State.unit(t.produced_unit or 0, t.result_sign or +1)
    return p

def alr_once(tokens:List[Token]):
    out=tokens[:]; i=0; changed=False
    while i<=len(out)-3:
        a,b,c = out[i], out[i+1], out[i+2]
        if (a.ttype=="unit_step" and b.ttype=="collapse" and c.ttype=="scalar_step"
            and a.produced_unit==b.mult):
            del out[i:i+3]; changed=True; continue
        i+=1
    return out, changed

def alr_normal_form(tokens:List[Token]):
    cur=tokens[:]
    while True:
        cur,ch=alr_once(cur)
        if not ch: return cur

def run_demo(seed:int=42):
    DIM,RES,SGN = build_tables()
    # sanity: e1*e2=+e4, e2*e1=-e4
    assert RES[1][1][2]==4 and SGN[1][1][2]==+1
    assert RES[1][2][1]==4 and SGN[1][2][1]==-1
    # example parity: [2,4] starting e1 → -1 and parity 1
    toks, st = compute_journey(State.unit(1), [2,4])
    assert st.kind=="scalar" and st.sign==-1
    assert journey_parity(toks, State.unit(1))==1

    rng=random.Random(seed)
    # Monte Carlo constants
    steps=200000
    collapses=sum(1 for _ in range(steps) if rng.randint(1,7)==rng.randint(1,7))
    lambda_hat = collapses/steps
    # p0 = (1/7)*(1/2)
    trials=200000
    p0_hat = sum(1 for _ in range(trials) if (rng.randint(1,7)==rng.randint(1,7) and rng.randint(0,1)==1))/trials

    # chain stats
    L=30
    chains=[[rng.randint(1,7) for _ in range(L)] for _ in range(2000)]
    survivors=0
    parities=[]
    for ch in chains:
        s=State.unit(rng.randint(1,7))
        toks,_=compute_journey(s,ch)
        nf=alr_normal_form(toks)
        if len(nf)==len(toks): survivors+=1
        parities.append(journey_parity(toks,s))
    return {
        "lambda_hat": lambda_hat,
        "p0_hat": p0_hat,
        "parity_even_frac": sum(1 for p in parities if p==0)/len(parities),
        "alr_survivor_rate_upper_bound": survivors/len(chains)
    }

# ------------------------------
# Bracket-aware journeys
# ------------------------------
def _norm_expr(s: str) -> str:
    return re.sub(r"\s+", "", s.replace("×", "x"))

def parse_parenthesized(expr: str):
    """
    Parse strings like "(((1x2)x4)x6)" or "(1x(2x(4x6)))".
    Returns a tree composed of ints and ('*', left, right) tuples.
    """
    s = _norm_expr(expr)
    if not s:
        raise ValueError("Empty expression")
    i = 0

    def parse():
        nonlocal i
        if i >= len(s):
            raise ValueError("Unexpected end of expression")
        ch = s[i]
        if ch.isdigit():
            v = int(ch)
            if v < 1 or v > 7:
                raise ValueError("Unit index out of range")
            i += 1
            return v
        if ch == '(':  # parse compound
            i += 1
            left = parse()
            if i >= len(s) or s[i] != 'x':
                raise ValueError("Expected 'x' operator")
            i += 1
            right = parse()
            if i >= len(s) or s[i] != ')':
                raise ValueError("Expected closing ')'")
            i += 1
            return ('*', left, right)
        raise ValueError(f"Unexpected token {ch!r} at position {i}")

    tree = parse()
    if i != len(s):
        raise ValueError("Trailing characters in expression")
    return tree

def _eval_tree_rec(start: State, node, consumed_first: bool) -> Tuple[List[Token], State, bool]:
    if isinstance(node, int):
        if not consumed_first:
            if start.kind != "unit" or start.idx != node:
                raise ValueError("Expression base does not match start unit")
            return [], start, True
        tok, st = step_token(start, node)
        return [tok], st, True
    op, left, right = node
    if op != '*':
        raise ValueError("Unknown node operator")
    toks_left, state_left, consumed_left = _eval_tree_rec(start, left, consumed_first)
    toks_right, state_right, consumed_right = _eval_tree_rec(state_left, right, consumed_left)
    return toks_left + toks_right, state_right, consumed_right

def eval_tree(start: State, tree) -> Tuple[List[Token], State]:
    tokens, state, consumed = _eval_tree_rec(start, tree, False)
    if not consumed:
        raise ValueError("Expression did not contain a starting unit")
    return tokens, state

def tokens_from_expr(start_unit: int, expr: str) -> List[Token]:
    tree = parse_parenthesized(expr)
    toks, _ = eval_tree(State.unit(start_unit), tree)
    return toks

def tokens_random_tree(start_unit: int, chain: List[int], rng: random.Random) -> List[Token]:
    """Generate tokens by evaluating a random full binary tree over `chain`."""
    if not chain:
        return []

    def build(seq: List[int]):
        if len(seq) == 1:
            return seq[0]
        split = rng.randint(1, len(seq) - 1)
        return ('*', build(seq[:split]), build(seq[split:]))

    seq = [start_unit] + chain
    tree = build(seq)
    toks, _ = eval_tree(State.unit(start_unit), tree)
    return toks

# ------------------------------
# Full ALR with audit logging
# ------------------------------
def token_to_str(tok: 'Token') -> str:
    if tok.ttype == "collapse":
        return f"d0*x{tok.mult}"
    if tok.ttype == "scalar_step":
        return f"scalarx{tok.mult}"
    return f"d{tok.dim}x{tok.mult}"

def token_list_to_str(tokens: List['Token']) -> List[str]:
    return [token_to_str(t) for t in tokens]

def full_alr(tokens: List['Token'], start_state: State):
    """Apply anchored three-block deletions with audit logging."""
    current = tokens[:]
    audit: List[dict] = []
    while True:
        changed = False
        i = 0
        while i <= len(current) - 3:
            a, b, c = current[i], current[i + 1], current[i + 2]
            if (a.ttype == "unit_step" and b.ttype == "collapse" and c.ttype == "scalar_step"
                and a.produced_unit == b.mult):
                audit.append({
                    "i": i,
                    "before": token_list_to_str([a, b, c]),
                    "after_len": len(current) - 3,
                })
                del current[i:i + 3]
                changed = True
                continue  # re-check at same index for overlapping deletions
            i += 1
        if not changed:
            break

    parity_before = journey_parity(tokens, start_state)
    parity_after = journey_parity(current, start_state)
    assert parity_before == parity_after, "ALR must preserve parity"
    return current, audit
